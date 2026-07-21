"""
AI-OS Filter: Context Budget Enforcer
Version: 1.1.0
Responsibility: Enforce 65,536 token context ceiling on NIM Free Tier.
Prevents context overflow errors and runaway latency on long conversations.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: Nemotron Ultra supports 1M context but NIM Free Tier on shared infrastructure
produces extreme latency and eventual 504/timeout errors when context grows beyond
~64K tokens. Proactive truncation at the gateway layer prevents both failure modes.
Truncation strategy: preserve system prompt + last N turn-pairs + current message.
Oldest conversation history is dropped first (FIFO eviction).

FIX v1.1.0: Removed _ai_os_context_truncated and _ai_os_estimated_tokens from
body top-level. Open WebUI validates body schema and rejects unknown keys.
Truncation state is now stored in self._state (instance-level) for internal
logging only. Body is returned clean.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True,
            description="Enable/disable context budget enforcement"
        )
        max_context_tokens: int = Field(
            default=65536,
            description="Hard token ceiling. Messages exceeding this trigger truncation."
        )
        tokens_per_char_estimate: float = Field(
            default=0.25,
            description=(
                "Characters-to-tokens ratio estimate. "
                "0.25 = ~4 chars/token, conservative for mixed EN/ID text."
            )
        )
        min_history_turns: int = Field(
            default=3,
            description="Minimum number of recent turn-pairs (user+assistant) to always preserve."
        )

    def __init__(self):
        self.valves = self.Valves()
        # Internal state — never written to body
        self._state = {
            "last_truncated": False,
            "last_estimated_tokens": 0,
            "last_dropped_count": 0,
        }

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text) * self.valves.tokens_per_char_estimate)

    def _message_tokens(self, message: dict) -> int:
        content = message.get("content", "")
        if isinstance(content, str):
            return self._estimate_tokens(content)
        if isinstance(content, list):
            return sum(
                self._estimate_tokens(c.get("text", ""))
                for c in content
                if isinstance(c, dict)
            )
        return 0

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Measure total estimated context tokens.
        If over ceiling, truncate oldest non-system messages until within budget.
        Always preserves: system messages + last min_history_turns turn-pairs + current message.
        Returns body with only body["messages"] modified — no new keys added to body.
        """
        if not self.valves.enabled:
            return body

        messages = body.get("messages", [])
        if not messages:
            return body

        system_messages = [m for m in messages if m.get("role") == "system"]
        conv_messages = [m for m in messages if m.get("role") != "system"]

        total_tokens = sum(self._message_tokens(m) for m in messages)
        ceiling = self.valves.max_context_tokens

        # Update internal state
        self._state["last_estimated_tokens"] = total_tokens
        self._state["last_truncated"] = False
        self._state["last_dropped_count"] = 0

        if total_tokens <= ceiling:
            return body

        # Truncation required.
        # Protect last N turn-pairs + current user message (always the last item).
        min_preserve = self.valves.min_history_turns * 2
        protected = conv_messages[-max(min_preserve, 1):]
        candidates = list(conv_messages[:-max(min_preserve, 1)])

        dropped = 0
        while candidates and total_tokens > ceiling:
            evicted = candidates.pop(0)
            total_tokens -= self._message_tokens(evicted)
            dropped += 1

        # Record truncation in internal state only
        self._state["last_truncated"] = True
        self._state["last_estimated_tokens"] = total_tokens
        self._state["last_dropped_count"] = dropped

        body["messages"] = system_messages + candidates + protected
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Truncation is inlet-only."""
        return body
