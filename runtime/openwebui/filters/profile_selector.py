"""
AI-OS Filter: Profile Selector
Version: 1.3.0
Responsibility: Classify user query into task_class and apply the matching
parameter profile (temperature, max_tokens) before the NIM call.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY this filter exists:
  A single parameter set cannot be optimal for both creative writing (needs high
  temperature) and production code generation (needs low temperature + high reasoning).
  This filter dynamically selects the right profile per turn without requiring
  the user to manually switch models.

Parameter key reference (Open WebUI + NIM Free Tier):
  temperature          -> top-level body key, OpenAI spec, accepted by OWU + NIM
  max_tokens           -> top-level body key, OpenAI spec, accepted by OWU + NIM
  chat_template_kwargs -> ONLY works on self-hosted NIM or NIM Enterprise.
                          NIM Free Tier (integrate.api.nvidia.com) REJECTS this
                          key with 'Inference connection error'. Keep
                          enable_thinking = False on Free Tier at all times.

CHANGELOG:
  1.0.0  Initial release
  1.1.0  Removed unsupported body keys (options, extra_body, _ai_os_*)
  1.2.0  Replaced num_predict with max_tokens (OpenAI spec)
  1.3.0  enable_thinking default False -- NIM Free Tier rejects chat_template_kwargs
"""

from pydantic import BaseModel, Field
from typing import Optional
import re

# Module-level registry: response_quality_monitor reads task_class from here
# without polluting the body dict. Key = user_id or "default".
_TASK_CLASS_REGISTRY: dict = {}


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True,
            description="Enable/disable profile selection"
        )
        default_profile: str = Field(
            default="discussion",
            description="Fallback profile if no task class matches"
        )
        enable_thinking: bool = Field(
            default=False,
            description=(
                "[WARNING] Only enable on self-hosted NIM or NIM Enterprise. "
                "NIM Free Tier (integrate.api.nvidia.com) rejects chat_template_kwargs "
                "and returns 'Inference connection error'. Keep False on Free Tier."
            )
        )

    # Task classification rules -- ordered by specificity, first match wins.
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

    # reasoning_budget kept for future use when enable_thinking is supported
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

    def _classify(self, text: str) -> str:
        for pattern, task_class in self.TASK_RULES:
            if pattern.search(text):
                return task_class
        return self.valves.default_profile

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        1. Classify last user message -> task_class
        2. Write temperature + max_tokens directly to body top-level
        3. Only inject chat_template_kwargs if enable_thinking is explicitly True
           (not safe on NIM Free Tier -- see Valves warning above)
        4. Store task_class in module registry for response_quality_monitor
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

        # OpenAI-spec keys -- accepted by Open WebUI + NIM Free Tier
        body["temperature"] = profile["temperature"]
        body["max_tokens"] = profile["max_tokens"]

        # GUARD: only inject chat_template_kwargs on supported endpoints.
        # NIM Free Tier will return 'Inference connection error' if this is present.
        if self.valves.enable_thinking:
            body["chat_template_kwargs"] = {
                "enable_thinking": True,
                "reasoning_budget": profile["reasoning_budget"]
            }

        # Store task_class for response_quality_monitor outlet
        user_id = (__user__ or {}).get("id", "default")
        _TASK_CLASS_REGISTRY[user_id] = task_class

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Profile selection is inlet-only."""
        return body
