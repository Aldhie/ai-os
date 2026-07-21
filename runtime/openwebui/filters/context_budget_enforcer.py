"""
AI-OS Filter: Context Budget Enforcer
Version: 1.0.0
Responsibility: Enforce 65,536 token context ceiling on Free Tier.
Prevents context overflow errors and runaway latency on long conversations.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: Nemotron Ultra supports 1M context but NIM Free Tier on shared infrastructure
produces extreme latency and eventual timeout/overflow errors when context grows
beyond ~64K tokens. Proactive truncation at the gateway layer prevents both.
Truncation strategy: preserve system prompt + last 3 turns + current message.
Oldest conversation history is dropped first.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable context budget enforcement")
        max_context_tokens: int = Field(
            default=65536,
            description="Hard token ceiling. Messages exceeding this trigger truncation."
        )
        tokens_per_char_estimate: float = Field(
            default=0.25,
            description="Characters-to-tokens estimate. 0.25 = ~4 chars per token (conservative for mixed EN/ID)."
        )
        min_history_turns: int = Field(
            default=3,
            description="Minimum number of recent conversation turns to always preserve."
        )

    def __init__(self):
        self.valves = self.Valves()

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text) * self.valves.tokens_per_char_estimate)

    def _message_tokens(self, message: dict) -> int:
        content = message.get("content", "")
        if isinstance(content, str):
            return self._estimate_tokens(content)
        if isinstance(content, list):
            return sum(self._estimate_tokens(c.get("text", "")) for c in content if isinstance(c, dict))
        return 0

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Measure total estimated context tokens.
        If over ceiling, truncate oldest non-system messages until within budget.
        Always preserves: system message + last min_history_turns turn-pairs + current message.
        """
        if not self.valves.enabled:
            return body

        messages = body.get("messages", [])
        if not messages:
            return body

        # Separate system messages from conversation
        system_messages = [m for m in messages if m.get("role") == "system"]
        conv_messages = [m for m in messages if m.get("role") != "system"]

        # Calculate current total
        total_tokens = sum(self._message_tokens(m) for m in messages)
        ceiling = self.valves.max_context_tokens

        if total_tokens <= ceiling:
            return body

        # Need to truncate. Preserve last N turn-pairs (user+assistant) + current user message.
        # Work from oldest conversation message forward, dropping until within budget.
        min_preserve = self.valves.min_history_turns * 2  # pairs of user+assistant
        # Always preserve the last message (current user turn)
        protected = conv_messages[-max(min_preserve, 1):]
        candidates = conv_messages[:-max(min_preserve, 1)]

        # Drop from oldest until within budget
        while candidates and total_tokens > ceiling:
            dropped = candidates.pop(0)
            total_tokens -= self._message_tokens(dropped)

        truncated_messages = system_messages + candidates + protected
        body["messages"] = truncated_messages
        body["_ai_os_context_truncated"] = True
        body["_ai_os_estimated_tokens"] = total_tokens

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Truncation is inlet-only."""
        return body
