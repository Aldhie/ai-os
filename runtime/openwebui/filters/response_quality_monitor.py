"""
AI-OS Filter: Response Quality Monitor
Version: 1.1.0
Responsibility: Outlet filter that checks response quality signals:
  1. Response length compliance vs task-class target
  2. Prohibited pattern detection (filler affirmations, first-person openings)
  3. [verify] tag frequency as hallucination risk indicator
  4. Structured format compliance (headers, code blocks)
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: Quality monitoring at the outlet layer creates measurable data to tune
the system prompt and benchmark. Without measurement, quality is aspirational.
This filter does NOT modify response content. It logs quality signals to
self._state for the benchmark harness to query via /api/v1/functions/.

FIX v1.1.0: Removed all body mutations on outlet (body[_ai_os_quality] etc.).
Open WebUI rejects unknown top-level keys. Quality data is stored in self._state
only. task_class is read from profile_selector's module-level registry.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re

# Import task_class registry written by profile_selector
try:
    from profile_selector import _TASK_CLASS_REGISTRY
except ImportError:
    # Fallback when running in isolation (unit tests, direct import)
    _TASK_CLASS_REGISTRY: dict = {}


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable quality monitoring")
        log_to_console: bool = Field(
            default=False,
            description="Print quality report to server console (debug mode)"
        )

    # Token targets per task class (from compiled_prompt_v1.md response targets)
    LENGTH_TARGETS = {
        "greeting":     80,
        "discussion":   600,
        "coding":       3000,
        "architecture": 2500,
        "analysis":     1500,
        "research":     2000,
        "debugging":    1500,
        "creative":     1200,
    }

    PROHIBITED = re.compile(
        r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!|Happy to help|I\'d be happy)',
        re.IGNORECASE | re.MULTILINE
    )
    STARTS_WITH_I = re.compile(r'^I\s', re.MULTILINE)
    VERIFY_TAG = re.compile(r'\[verify\]', re.IGNORECASE)
    CITATION_TAG = re.compile(r'\[Source:', re.IGNORECASE)
    CODE_BLOCK = re.compile(r'```')
    HEADER = re.compile(r'^#{1,3}\s', re.MULTILINE)

    def __init__(self):
        self.valves = self.Valves()
        self._state: dict = {}

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text) * 0.25)

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Quality monitoring is outlet-only."""
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Analyse the last assistant message for quality signals.
        Stores results in self._state only — body is returned unmodified.
        """
        if not self.valves.enabled:
            return body

        messages = body.get("messages", [])
        assistant_text = ""
        for msg in reversed(messages):
            if msg.get("role") == "assistant":
                content = msg.get("content", "")
                assistant_text = content if isinstance(content, str) else ""
                break

        if not assistant_text:
            return body

        # Resolve task_class from registry written by profile_selector
        user_id = (__user__ or {}).get("id", "default")
        task_class = _TASK_CLASS_REGISTRY.get(user_id, "discussion")

        target_tokens = self.LENGTH_TARGETS.get(task_class, 600)
        actual_tokens = self._estimate_tokens(assistant_text)
        length_ratio = round(actual_tokens / target_tokens, 2) if target_tokens > 0 else 1.0

        prohibited_hits = len(self.PROHIBITED.findall(assistant_text))
        starts_with_i = len(self.STARTS_WITH_I.findall(assistant_text))
        verify_count = len(self.VERIFY_TAG.findall(assistant_text))
        citation_count = len(self.CITATION_TAG.findall(assistant_text))
        has_code_block = bool(self.CODE_BLOCK.search(assistant_text))
        has_headers = bool(self.HEADER.search(assistant_text))

        quality = {
            "task_class": task_class,
            "target_tokens": target_tokens,
            "actual_tokens": actual_tokens,
            "length_ratio": length_ratio,
            "length_compliant": 0.5 <= length_ratio <= 1.5,
            "prohibited_hits": prohibited_hits,
            "starts_with_i_count": starts_with_i,
            "verify_tag_count": verify_count,
            "citation_count": citation_count,
            "has_code_block": has_code_block,
            "has_headers": has_headers,
            "hallucination_risk": (
                "HIGH" if verify_count >= 5
                else "MEDIUM" if verify_count >= 2
                else "LOW"
            ),
        }

        # Store internally — never written to body
        self._state["last_quality"] = quality

        if self.valves.log_to_console:
            print(f"[AI-OS Quality Monitor] {quality}")

        return body
