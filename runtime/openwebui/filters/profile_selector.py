"""
AI-OS Filter: Profile Selector
Version: 1.0.0
Responsibility: Classify user query into task_class and apply the matching
parameter profile (temperature, max_tokens, reasoning_budget) before the NIM call.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: A single parameter set cannot be optimal for both creative writing (needs high
temperature) and production code generation (needs low temperature + high reasoning).
This filter dynamically selects the right profile per turn, giving per-task optimal
parameters without requiring the user to manually switch models.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable profile selection")
        default_profile: str = Field(default="discussion", description="Fallback profile if no task class matches")

    # Task classification rules — ordered by specificity.
    # First matching rule wins.
    TASK_RULES = [
        # Debugging: must come before coding to catch 'error', 'traceback', 'exception'
        (re.compile(
            r'\b(debug|traceback|stack trace|exception|error:|TypeError|ValueError|'
            r'AttributeError|KeyError|segfault|null pointer|undefined|NaN|unexpected behaviour)\b',
            re.IGNORECASE
        ), "debugging"),
        # Coding
        (re.compile(
            r'\b(write|implement|create|generate|refactor|optimise|code|function|class|'
            r'method|API|endpoint|script|program|algorithm|SQL|query|regex|unit test)\b',
            re.IGNORECASE
        ), "coding"),
        # Architecture
        (re.compile(
            r'\b(architecture|system design|infrastructure|scalab|microservice|monolith|'
            r'event.driven|CQRS|DDD|service mesh|kubernetes|distributed|deployment topology)\b',
            re.IGNORECASE
        ), "architecture"),
        # Research
        (re.compile(
            r'\b(research|survey|literature|compare|contrast|study|review|state of the art|'
            r'benchmark|paper|publication|academic|citation)\b',
            re.IGNORECASE
        ), "research"),
        # Analysis
        (re.compile(
            r'\b(analyse|analyze|analysis|evaluate|assess|diagnose|measure|metric|'
            r'performance|bottleneck|root cause|trade.off|pros.*cons)\b',
            re.IGNORECASE
        ), "analysis"),
        # Creative
        (re.compile(
            r'\b(write.*story|creative|blog post|essay|narrative|brainstorm|idea|'
            r'marketing copy|tagline|slogan)\b',
            re.IGNORECASE
        ), "creative"),
    ]

    # Profile parameter overrides mapped by task_class
    PROFILES = {
        "discussion":  {"temperature": 0.7,  "max_tokens": 4096, "reasoning_budget": 4096},
        "coding":      {"temperature": 0.2,  "max_tokens": 4096, "reasoning_budget": 4096},
        "architecture":{"temperature": 0.4,  "max_tokens": 6144, "reasoning_budget": 8192},
        "analysis":    {"temperature": 0.4,  "max_tokens": 4096, "reasoning_budget": 6144},
        "creative":    {"temperature": 0.9,  "max_tokens": 3000, "reasoning_budget": 2048},
        "research":    {"temperature": 0.5,  "max_tokens": 8192, "reasoning_budget": 8192},
        "debugging":   {"temperature": 0.1,  "max_tokens": 3072, "reasoning_budget": 6144},
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
        Classify the last user message and apply matching parameter profile
        to body["options"] before the NIM API call.
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

        # Apply profile to body options
        if "options" not in body:
            body["options"] = {}

        body["options"]["temperature"] = profile["temperature"]
        body["options"]["num_predict"] = profile["max_tokens"]  # OWU uses num_predict

        # Inject reasoning budget via extra_body for NIM
        if "extra_body" not in body:
            body["extra_body"] = {}
        body["extra_body"]["chat_template_kwargs"] = {"enable_thinking": True}
        body["extra_body"]["reasoning_budget"] = profile["reasoning_budget"]

        # Tag metadata for outlet filters and benchmark
        body["_ai_os_task_class"] = task_class
        body["_ai_os_profile"] = task_class

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Profile selection is inlet-only."""
        return body
