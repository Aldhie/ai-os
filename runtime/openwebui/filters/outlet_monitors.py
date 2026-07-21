"""
AI-OS Filter: Outlet Monitors
Version: 1.0.0
Responsibility: Post-inference quality monitoring.
  1. Response Length Monitor — log if output exceeds 1.5x task_class target.
  2. Hallucination Flag Checker — count [verify] tags per turn.
  3. Citation Validator — warn if RAG was used but no [Source: ...] citation present.
Rationale: Outlet filters create the observability data needed to tune
           the runtime. Without measurement, quality degradation is invisible.
           Logging does not modify the response — it only instruments it.
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


# Target token counts per task_class for length monitoring
LENGTH_TARGETS: dict[str, int] = {
    "greeting": 80,
    "conversational": 512,
    "coding": 1500,
    "debugging": 1200,
    "architecture": 2500,
    "research": 3000,
    "analysis": 2000,
    "planning": 1500,
    "creative": 1200,
}
DEFAULT_LENGTH_TARGET = 1000


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Disable all outlet monitors.")
        length_monitor: bool = Field(default=True, description="Enable response length monitoring.")
        hallucination_monitor: bool = Field(default=True, description="Enable [verify] tag counting.")
        citation_monitor: bool = Field(default=True, description="Enable citation presence check.")
        length_warn_ratio: float = Field(
            default=1.5,
            description="Warn if output token count exceeds target * this ratio."
        )
        session_stats: dict = Field(default_factory=dict, description="Internal session statistics.")

    def __init__(self):
        self.valves = self.Valves()
        self._session_verify_count = 0
        self._session_turn_count = 0
        self._session_rag_turns = 0
        self._session_cited_turns = 0

    @staticmethod
    def _extract_assistant_text(body: dict) -> str:
        messages = body.get('messages', [])
        for msg in reversed(messages):
            if msg.get('role') == 'assistant':
                content = msg.get('content', '')
                if isinstance(content, list):
                    return ' '.join(p.get('text', '') for p in content if isinstance(p, dict))
                return str(content)
        return ''

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        return max(1, len(text) // 4)

    # -----------------------------------------------------------------------
    # INLET — passthrough, capture RAG usage flag if set
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body

    # -----------------------------------------------------------------------
    # OUTLET — monitoring only, never modify response content
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body

        assistant_text = self._extract_assistant_text(body)
        if not assistant_text:
            return body

        task_class = body.get('metadata', {}).get('task_class', 'conversational')
        rag_used = body.get('metadata', {}).get('rag_used', False)
        self._session_turn_count += 1

        # --- 1. Response Length Monitor ---
        if self.valves.length_monitor:
            target = LENGTH_TARGETS.get(task_class, DEFAULT_LENGTH_TARGET)
            actual = self._estimate_tokens(assistant_text)
            ratio = actual / target if target > 0 else 1.0
            if ratio > self.valves.length_warn_ratio:
                print(
                    f"[AI-OS Length Monitor] OVER-GENERATION | "
                    f"task_class={task_class} | actual={actual} tokens | "
                    f"target={target} tokens | ratio={ratio:.2f}x"
                )

        # --- 2. Hallucination Flag Checker ---
        if self.valves.hallucination_monitor:
            verify_count = len(re.findall(r'\[verify\]', assistant_text, re.IGNORECASE))
            self._session_verify_count += verify_count
            if verify_count > 0:
                print(
                    f"[AI-OS Hallucination Monitor] {verify_count} [verify] tag(s) in response. "
                    f"Session total: {self._session_verify_count} across {self._session_turn_count} turn(s)."
                )

        # --- 3. Citation Validator ---
        if self.valves.citation_monitor and rag_used:
            self._session_rag_turns += 1
            has_citation = bool(re.search(r'\[Source:', assistant_text))
            if has_citation:
                self._session_cited_turns += 1
            else:
                print(
                    f"[AI-OS Citation Validator] WARNING: RAG was used but no [Source: ...] "
                    f"citation found in response. Session citation rate: "
                    f"{self._session_cited_turns}/{self._session_rag_turns}"
                )

        return body
