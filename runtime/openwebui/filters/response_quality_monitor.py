"""
AI-OS Filter: Response Quality Monitor
Version: 1.0.0
Responsibility: Outlet filter that checks response quality signals:
  1. Response length vs task-class target
  2. Prohibited pattern detection (filler affirmations, question restatement)
  3. [verify] tag frequency as hallucination risk signal
  4. Citation presence when RAG was used
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: Quality monitoring at the outlet layer creates the data needed to tune
the system prompt and benchmark. Without measurement, quality is aspirational.
This filter does NOT modify the response — it appends metadata that the
benchmark harness reads to produce quality scores.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable quality monitoring")
        append_quality_metadata: bool = Field(
            default=False,
            description="Append quality metadata JSON block at end of response (debug mode only)"
        )

    # Length targets in tokens per task class (from response.md)
    LENGTH_TARGETS = {
        "greeting":      80,
        "discussion":    600,
        "coding":        3000,
        "architecture":  2500,
        "analysis":      1500,
        "research":      2000,
        "debugging":     1500,
        "creative":      1200,
    }

    PROHIBITED_PATTERNS = [
        re.compile(r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!|Happy to|I\'d be happy)', re.IGNORECASE),
        re.compile(r'Is there anything else I can help', re.IGNORECASE),
        re.compile(r'^I\s', re.MULTILINE),  # Starting response with "I"
    ]

    VERIFY_PATTERN = re.compile(r'\[verify\]', re.IGNORECASE)
    CITATION_PATTERN = re.compile(r'\[Source:', re.IGNORECASE)

    def __init__(self):
        self.valves = self.Valves()

    def _estimate_tokens(self, text: str) -> int:
        return int(len(text) * 0.25)

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Quality monitoring is outlet-only."""
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Analyse the assistant response for quality signals.
        Attaches _ai_os_quality dict to body for benchmark harness consumption.
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

        task_class = body.get("_ai_os_task_class", "discussion")
        target_tokens = self.LENGTH_TARGETS.get(task_class, 600)
        actual_tokens = self._estimate_tokens(assistant_text)
        length_ratio = actual_tokens / target_tokens if target_tokens > 0 else 1.0

        prohibited_hits = sum(
            1 for p in self.PROHIBITED_PATTERNS if p.search(assistant_text)
        )
        verify_count = len(self.VERIFY_PATTERN.findall(assistant_text))
        citation_count = len(self.CITATION_PATTERN.findall(assistant_text))
        rag_was_used = body.get("_ai_os_rag_used", False)

        quality = {
            "task_class": task_class,
            "target_tokens": target_tokens,
            "actual_tokens": actual_tokens,
            "length_ratio": round(length_ratio, 2),
            "length_compliant": 0.5 <= length_ratio <= 1.5,
            "prohibited_pattern_hits": prohibited_hits,
            "verify_tag_count": verify_count,
            "citation_count": citation_count,
            "citation_compliant": (not rag_was_used) or (citation_count > 0),
            "hallucination_risk": "HIGH" if verify_count >= 5 else (
                "MEDIUM" if verify_count >= 2 else "LOW"
            ),
        }

        body["_ai_os_quality"] = quality
        return body
