# AI-OS Production Filter: Profile Selector v1.2.0
# Fix v1.2.0: num_predict -> max_tokens (OpenAI spec, required for NIM endpoint)
# Fix v1.1.0: removed unsupported body keys (options, extra_body, _ai_os_*)
# See runtime/openwebui/filters/profile_selector.py for full annotated version.

from pydantic import BaseModel, Field
from typing import Optional
import re

_TASK_CLASS_REGISTRY: dict = {}


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True)
        default_profile: str = Field(default="discussion")
        enable_thinking: bool = Field(default=True)

    TASK_RULES = [
        (re.compile(r'\b(debug|traceback|exception|error:|TypeError|ValueError|AttributeError)\b', re.IGNORECASE), "debugging"),
        (re.compile(r'\b(write|implement|create|generate|refactor|code|function|class|API|script|algorithm|SQL)\b', re.IGNORECASE), "coding"),
        (re.compile(r'\b(architecture|system design|infrastructure|scalab|microservice|distributed|kubernetes)\b', re.IGNORECASE), "architecture"),
        (re.compile(r'\b(research|survey|literature|compare|benchmark|paper|academic)\b', re.IGNORECASE), "research"),
        (re.compile(r'\b(analyse|analyze|analysis|evaluate|assess|diagnose|trade.off|pros.*cons)\b', re.IGNORECASE), "analysis"),
        (re.compile(r'\b(creative|blog post|essay|narrative|brainstorm|marketing copy)\b', re.IGNORECASE), "creative"),
    ]

    # max_tokens = OpenAI spec = correct key for NIM (OpenAI-compatible endpoint)
    PROFILES = {
        "discussion":   {"temperature": 0.7, "max_tokens": 4096,  "reasoning_budget": 4096},
        "coding":       {"temperature": 0.2, "max_tokens": 4096,  "reasoning_budget": 4096},
        "architecture": {"temperature": 0.4, "max_tokens": 6144,  "reasoning_budget": 8192},
        "analysis":     {"temperature": 0.4, "max_tokens": 4096,  "reasoning_budget": 6144},
        "creative":     {"temperature": 0.9, "max_tokens": 3000,  "reasoning_budget": 2048},
        "research":     {"temperature": 0.5, "max_tokens": 8192,  "reasoning_budget": 8192},
        "debugging":    {"temperature": 0.1, "max_tokens": 3072,  "reasoning_budget": 6144},
    }

    def __init__(self):
        self.valves = self.Valves()

    def _classify(self, text):
        for pattern, tc in self.TASK_RULES:
            if pattern.search(text):
                return tc
        return self.valves.default_profile

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        last_text = next(
            (m["content"] for m in reversed(messages)
             if m.get("role") == "user" and isinstance(m.get("content"), str)),
            ""
        )
        tc = self._classify(last_text)
        p = self.PROFILES.get(tc, self.PROFILES["discussion"])

        # OpenAI-spec keys only — accepted by Open WebUI + NIM
        body["temperature"] = p["temperature"]
        body["max_tokens"] = p["max_tokens"]

        if self.valves.enable_thinking:
            body["chat_template_kwargs"] = {
                "enable_thinking": True,
                "reasoning_budget": p["reasoning_budget"]
            }

        user_id = (__user__ or {}).get("id", "default")
        _TASK_CLASS_REGISTRY[user_id] = tc
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
