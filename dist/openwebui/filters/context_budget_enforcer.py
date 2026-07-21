# AI-OS Production Filter: Context Budget Enforcer v1.1.0
# Fixed: removed _ai_os_* keys from body. See runtime/openwebui/filters/context_budget_enforcer.py

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
        self._state = {"last_truncated": False, "last_dropped_count": 0}

    def _tok(self, text: str) -> int:
        return int(len(text) * self.valves.tokens_per_char_estimate)

    def _msg_tok(self, m: dict) -> int:
        c = m.get("content", "")
        if isinstance(c, str): return self._tok(c)
        if isinstance(c, list): return sum(self._tok(x.get("text", "")) for x in c if isinstance(x, dict))
        return 0

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        if not messages:
            return body
        sys_msgs = [m for m in messages if m.get("role") == "system"]
        conv = [m for m in messages if m.get("role") != "system"]
        total = sum(self._msg_tok(m) for m in messages)
        self._state["last_truncated"] = False
        if total <= self.valves.max_context_tokens:
            return body
        min_p = self.valves.min_history_turns * 2
        protected = conv[-max(min_p, 1):]
        candidates = list(conv[:-max(min_p, 1)])
        dropped = 0
        while candidates and total > self.valves.max_context_tokens:
            total -= self._msg_tok(candidates.pop(0))
            dropped += 1
        self._state["last_truncated"] = True
        self._state["last_dropped_count"] = dropped
        body["messages"] = sys_msgs + candidates + protected
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
