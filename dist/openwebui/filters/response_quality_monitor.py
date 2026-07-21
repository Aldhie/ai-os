# AI-OS Production Filter: Response Quality Monitor v1.0.0
# Source: runtime/openwebui/filters/response_quality_monitor.py
# Install: Open WebUI Admin > Functions > New Function (type: Filter) > Paste > Enable
# Priority: 5 (outlet filter — runs after NIM response)

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True)
        append_quality_metadata: bool = Field(default=False)

    LENGTH_TARGETS = {
        "discussion": 600, "coding": 3000, "architecture": 2500,
        "analysis": 1500, "research": 2000, "debugging": 1500, "creative": 1200,
    }
    PROHIBITED = re.compile(
        r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!|Happy to|I\'d be happy)',
        re.IGNORECASE | re.MULTILINE
    )
    VERIFY = re.compile(r'\[verify\]', re.IGNORECASE)
    CITATION = re.compile(r'\[Source:', re.IGNORECASE)

    def __init__(self):
        self.valves = self.Valves()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        text = next((m["content"] for m in reversed(messages)
                     if m.get("role") == "assistant" and isinstance(m.get("content"), str)), "")
        if not text:
            return body
        tc = body.get("_ai_os_task_class", "discussion")
        target = self.LENGTH_TARGETS.get(tc, 600)
        actual = int(len(text) * 0.25)
        ratio = actual / target if target else 1.0
        body["_ai_os_quality"] = {
            "task_class": tc,
            "target_tokens": target,
            "actual_tokens": actual,
            "length_ratio": round(ratio, 2),
            "length_compliant": 0.5 <= ratio <= 1.5,
            "prohibited_pattern_hits": len(self.PROHIBITED.findall(text)),
            "verify_tag_count": len(self.VERIFY.findall(text)),
            "citation_count": len(self.CITATION.findall(text)),
            "hallucination_risk": "HIGH" if len(self.VERIFY.findall(text)) >= 5 else
                                  ("MEDIUM" if len(self.VERIFY.findall(text)) >= 2 else "LOW"),
        }
        return body
