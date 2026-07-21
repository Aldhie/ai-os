# AI-OS Production Filter: Context Budget Enforcer v1.0.0
# Source: runtime/openwebui/filters/context_budget_enforcer.py
# Install: Open WebUI Admin > Functions > New Function (type: Filter)
# Install order: 4 (last inlet, before NIM call)

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True)
        max_context_tokens: int = Field(default=65536)
        tokens_per_char_estimate: float = Field(default=0.25)
        min_history_turns: int = Field(default=3)

    def __init__(self):
        self.valves = self.Valves()

    def _est(self, text: str) -> int:
        return int(len(text) * self.valves.tokens_per_char_estimate)

    def _msg_tokens(self, msg: dict) -> int:
        c = msg.get("content", "")
        if isinstance(c, str):
            return self._est(c)
        if isinstance(c, list):
            return sum(self._est(x.get("text", "")) for x in c if isinstance(x, dict))
        return 0

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        if not messages:
            return body
        system = [m for m in messages if m.get("role") == "system"]
        conv = [m for m in messages if m.get("role") != "system"]
        total = sum(self._msg_tokens(m) for m in messages)
        ceiling = self.valves.max_context_tokens
        if total <= ceiling:
            return body
        min_p = self.valves.min_history_turns * 2
        protected = conv[-max(min_p, 1):]
        candidates = conv[:-max(min_p, 1)]
        while candidates and total > ceiling:
            dropped = candidates.pop(0)
            total -= self._msg_tokens(dropped)
        body["messages"] = system + candidates + protected
        body["_ai_os_context_truncated"] = True
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
