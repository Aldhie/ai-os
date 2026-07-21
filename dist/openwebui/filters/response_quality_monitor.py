# AI-OS Production Filter: Response Quality Monitor v1.1.0
# Fixed: no body mutations on outlet. See runtime/openwebui/filters/response_quality_monitor.py

from pydantic import BaseModel, Field
from typing import Optional
import re

try:
    from profile_selector import _TASK_CLASS_REGISTRY
except ImportError:
    _TASK_CLASS_REGISTRY: dict = {}


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True)
        log_to_console: bool = Field(default=False)

    LENGTH_TARGETS = {
        "greeting": 80, "discussion": 600, "coding": 3000,
        "architecture": 2500, "analysis": 1500,
        "research": 2000, "debugging": 1500, "creative": 1200,
    }
    PROHIBITED = re.compile(r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!)', re.I | re.M)
    VERIFY_TAG = re.compile(r'\[verify\]', re.I)

    def __init__(self):
        self.valves = self.Valves()
        self._state: dict = {}

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        text = next(
            (m.get("content", "") for m in reversed(messages)
             if m.get("role") == "assistant" and isinstance(m.get("content"), str)),
            ""
        )
        if not text:
            return body
        user_id = (__user__ or {}).get("id", "default")
        tc = _TASK_CLASS_REGISTRY.get(user_id, "discussion")
        target = self.LENGTH_TARGETS.get(tc, 600)
        actual = int(len(text) * 0.25)
        ratio = round(actual / target, 2) if target else 1.0
        quality = {
            "task_class": tc,
            "length_ratio": ratio,
            "length_compliant": 0.5 <= ratio <= 1.5,
            "prohibited_hits": len(self.PROHIBITED.findall(text)),
            "verify_count": len(self.VERIFY_TAG.findall(text)),
            "hallucination_risk": "HIGH" if len(self.VERIFY_TAG.findall(text)) >= 5 else "LOW",
        }
        self._state["last_quality"] = quality
        if self.valves.log_to_console:
            print(f"[AI-OS QM] {quality}")
        return body
