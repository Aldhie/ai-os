"""
AI-OS Filter: Profile Selector
Version: 1.1.0
Responsibility: Classify user query into task_class and apply the matching
parameter profile (temperature, num_predict, reasoning_budget) before the NIM call.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: A single parameter set cannot be optimal for both creative writing (needs high
temperature) and production code generation (needs low temperature + high reasoning).
This filter dynamically selects the right profile per turn, giving per-task optimal
parameters without requiring the user to manually switch models.

FIX v1.1.0: Removed unsupported top-level body keys (_ai_os_task_class, _ai_os_profile,
extra_body, options). Open WebUI validates body schema strictly — only known top-level
keys are allowed. Parameters are now written directly to body top-level. task_class is
stored in self._last_task_class for consumption by response_quality_monitor (same
process, shared filter state via class-level registry).
"""

from pydantic import BaseModel, Field
from typing import Optional
import re

# Module-level registry allows response_quality_monitor to read task_class
# without polluting the body dict. Key = user_id or "default".
_TASK_CLASS_REGISTRY: dict = {}


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable profile selection")
        default_profile: str = Field(
            default="discussion",
            description="Fallback profile if no task class matches"
        )
        enable_thinking: bool = Field(
            default=True,
            description="Pass enable_thinking=true to NIM via chat_template_kwargs"
        )

    # Task classification rules — ordered by specificity. First match wins.
    TASK_RULES = [
        (re.compile(
            r'\b(debug|traceback|stack trace|exception|error:|TypeError|ValueError|'
            r'AttributeError|KeyError|segfault|null pointer|undefined|NaN|unexpected behaviour)\b',
            re.IGNORECASE
        ), "debugging"),
        (re.compile(
            r'\b(write|implement|create|generate|refactor|optimise|code|function|class|'
            r'method|API|endpoint|script|program|algorithm|SQL|query|regex|unit test)\b',
            re.IGNORECASE
        ), "coding"),
        (re.compile(
            r'\b(architecture|system design|infrastructure|scalab|microservice|monolith|'
            r'event.driven|CQRS|DDD|service mesh|kubernetes|distributed|deployment topology)\b',
            re.IGNORECASE
        ), "architecture"),
        (re.compile(
            r'\b(research|survey|literature|compare|contrast|study|review|state of the art|'
            r'benchmark|paper|publication|academic|citation)\b',
            re.IGNORECASE
        ), "research"),
        (re.compile(
            r'\b(analyse|analyze|analysis|evaluate|assess|diagnose|measure|metric|'
            r'performance|bottleneck|root cause|trade.off|pros.*cons)\b',
            re.IGNORECASE
        ), "analysis"),
        (re.compile(
            r'\b(write.*story|creative|blog post|essay|narrative|brainstorm|idea|'
            r'marketing copy|tagline|slogan)\b',
            re.IGNORECASE
        ), "creative"),
    ]

    # Profile parameters — all values map to Open WebUI / NIM supported keys
    PROFILES = {
        "discussion":   {"temperature": 0.7, "num_predict": 4096, "reasoning_budget": 4096},
        "coding":       {"temperature": 0.2, "num_predict": 4096, "reasoning_budget": 4096},
        "architecture": {"temperature": 0.4, "num_predict": 6144, "reasoning_budget": 8192},
        "analysis":     {"temperature": 0.4, "num_predict": 4096, "reasoning_budget": 6144},
        "creative":     {"temperature": 0.9, "num_predict": 3000, "reasoning_budget": 2048},
        "research":     {"temperature": 0.5, "num_predict": 8192, "reasoning_budget": 8192},
        "debugging":    {"temperature": 0.1, "num_predict": 3072, "reasoning_budget": 6144},
    }

    def __init__(self):
        self.valves = self.Valves()

    def _classify(self, text: str) -> str:
        for pattern, task_class in self.TASK_RULES:
            if pattern.search(text):
                return task_class
        return self.valves.default_profile

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Classify the last user message and apply the matching parameter profile.
        Writes supported keys directly to body top-level (temperature, num_predict).
        Passes reasoning_budget via body[chat_template_kwargs] which Open WebUI
        forwards as-is to NIM without schema validation.
        Stores task_class in module-level registry for response_quality_monitor.
        """
        if not self.valves.enabled:
            return body

        messages = body.get("messages", [])
        last_user_text = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                content = msg.get("content", "")
                last_user_text = content if isinstance(content, str) else ""
                break

        task_class = self._classify(last_user_text)
        profile = self.PROFILES.get(task_class, self.PROFILES["discussion"])

        # Write parameters directly to body top-level — Open WebUI supported keys
        body["temperature"] = profile["temperature"]
        body["num_predict"] = profile["num_predict"]

        # chat_template_kwargs is forwarded by Open WebUI to NIM without schema check
        if self.valves.enable_thinking:
            body["chat_template_kwargs"] = {
                "enable_thinking": True,
                "reasoning_budget": profile["reasoning_budget"]
            }

        # Store task_class in module registry for response_quality_monitor outlet
        user_id = (__user__ or {}).get("id", "default")
        _TASK_CLASS_REGISTRY[user_id] = task_class

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Profile selection is inlet-only."""
        return body
