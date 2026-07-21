"""
AI-OS Filter: Context Budget Enforcer
Version: 1.0.0
Responsibility: Prevent context overflow by truncating conversation history
                when total token count approaches the 65,536-token ceiling.
Rationale: NVIDIA Cloud NIM Free Tier on shared infrastructure produces
           extreme latency and eventual context overflow errors on large
           contexts. Nemotron Ultra supports 1M tokens but Free Tier
           effectively degrades above ~64K tokens. Proactive truncation
           preserves system prompt integrity and recent conversation state
           while discarding old, lower-value history.
Strategy:
  1. Estimate token count (chars / 4 approximation — no tokeniser needed).
  2. If estimate > ceiling, remove oldest user/assistant pairs first.
  3. Always preserve: system prompt, last 3 turns.
  4. Never truncate mid-turn (always remove complete user+assistant pairs).
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        max_context_tokens: int = Field(
            default=65536,
            description="Token ceiling before truncation is triggered."
        )
        min_turns_to_keep: int = Field(
            default=3,
            description="Minimum number of recent conversation turns to always preserve."
        )
        enabled: bool = Field(
            default=True,
            description="Disable context truncation (use only in testing)."
        )
        debug_log: bool = Field(
            default=False,
            description="Log truncation events."
        )

    def __init__(self):
        self.valves = self.Valves()

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        """Approximate token count: 4 characters per token (GPT-family heuristic)."""
        return max(1, len(text) // 4)

    def _count_body_tokens(self, messages: list) -> int:
        total = 0
        for msg in messages:
            content = msg.get('content', '')
            if isinstance(content, list):
                content = ' '.join(p.get('text', '') for p in content if isinstance(p, dict))
            total += self._estimate_tokens(str(content))
        return total

    # -----------------------------------------------------------------------
    # INLET
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body

        messages = body.get('messages', [])
        if not messages:
            return body

        # Separate system message(s) from conversation
        system_messages = [m for m in messages if m.get('role') == 'system']
        conversation = [m for m in messages if m.get('role') != 'system']

        current_tokens = self._count_body_tokens(messages)

        if current_tokens <= self.valves.max_context_tokens:
            return body  # Within budget, no action needed

        # Build list of turn pairs (user + assistant) from oldest to newest
        # Keep the last N turns (min_turns_to_keep)
        turn_pairs: list[list] = []
        i = 0
        while i < len(conversation):
            if conversation[i].get('role') == 'user':
                pair = [conversation[i]]
                if i + 1 < len(conversation) and conversation[i + 1].get('role') == 'assistant':
                    pair.append(conversation[i + 1])
                    i += 2
                else:
                    i += 1
                turn_pairs.append(pair)
            else:
                i += 1

        min_keep = self.valves.min_turns_to_keep
        removed_turns = 0

        # Remove oldest pairs until within budget
        while len(turn_pairs) > min_keep:
            candidate_tokens = self._count_body_tokens(messages)
            if candidate_tokens <= self.valves.max_context_tokens:
                break
            turn_pairs.pop(0)  # Remove oldest turn pair
            removed_turns += 1
            # Rebuild messages to recount
            flat_conv = [msg for pair in turn_pairs for msg in pair]
            messages = system_messages + flat_conv

        body['messages'] = messages

        if removed_turns > 0 and self.valves.debug_log:
            print(
                f"[AI-OS Context Budget] Truncated {removed_turns} turn pair(s). "
                f"Context was ~{current_tokens} tokens, ceiling is {self.valves.max_context_tokens}."
            )

        return body

    # -----------------------------------------------------------------------
    # OUTLET — passthrough
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
