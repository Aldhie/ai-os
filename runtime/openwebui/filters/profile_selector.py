"""
AI-OS Filter: Profile Selector
Version: 1.0.0
Responsibility: Map task_class (set by Task Classifier) to a parameter
                profile and override the request body parameters accordingly.
Rationale: Different task classes require fundamentally different model
           behaviour. Coding needs low temperature and high reasoning budget.
           Creative needs high temperature and low reasoning budget.
           Applying a single static parameter set to all tasks degrades
           quality across all task classes simultaneously.
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
Dependency: Task Classifier filter must run before this filter (lower priority
            number = runs first in Open WebUI filter chain).
"""

from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------------------------
# Profile definitions — mirrors runtime/openwebui/profiles/*.json
# Single source of truth is the JSON files; this is the runtime application.
# ---------------------------------------------------------------------------
PROFILES: dict[str, dict] = {
    "greeting": {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 50,
        "max_tokens": 256,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.1,
        "reasoning_budget": 512,
    },
    "conversational": {
        "temperature": 0.75,
        "top_p": 0.95,
        "top_k": 50,
        "max_tokens": 2048,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.1,
        "reasoning_budget": 2048,
    },
    "coding": {
        "temperature": 0.2,
        "top_p": 0.95,
        "top_k": 20,
        "max_tokens": 4096,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.1,
        "reasoning_budget": 4096,
    },
    "debugging": {
        "temperature": 0.1,
        "top_p": 0.90,
        "top_k": 10,
        "max_tokens": 3072,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.0,
        "reasoning_budget": 6144,
    },
    "architecture": {
        "temperature": 0.4,
        "top_p": 0.95,
        "top_k": 40,
        "max_tokens": 6144,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "reasoning_budget": 8192,
    },
    "research": {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 50,
        "max_tokens": 8192,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "reasoning_budget": 8192,
    },
    "analysis": {
        "temperature": 0.3,
        "top_p": 0.92,
        "top_k": 30,
        "max_tokens": 4096,
        "presence_penalty": 0.0,
        "frequency_penalty": 0.1,
        "reasoning_budget": 6144,
    },
    "planning": {
        "temperature": 0.5,
        "top_p": 0.95,
        "top_k": 50,
        "max_tokens": 4096,
        "presence_penalty": 0.1,
        "frequency_penalty": 0.1,
        "reasoning_budget": 4096,
    },
    "creative": {
        "temperature": 0.9,
        "top_p": 0.98,
        "top_k": 80,
        "max_tokens": 3000,
        "presence_penalty": 0.3,
        "frequency_penalty": 0.2,
        "reasoning_budget": 2048,
    },
}

DEFAULT_PROFILE = "conversational"


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True,
            description="Disable profile switching (all requests use default parameters)."
        )
        enable_thinking: bool = Field(
            default=True,
            description="Set enable_thinking=true in extra_body for all requests."
        )
        debug_log: bool = Field(
            default=False,
            description="Log the applied profile for each request."
        )

    def __init__(self):
        self.valves = self.Valves()

    # -----------------------------------------------------------------------
    # INLET
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body

        task_class = body.get('metadata', {}).get('task_class', DEFAULT_PROFILE)
        profile = PROFILES.get(task_class, PROFILES[DEFAULT_PROFILE])

        # Apply profile parameters to request body options
        options = body.setdefault('options', {})
        options['temperature'] = profile['temperature']
        options['top_p'] = profile['top_p']
        options['top_k'] = profile['top_k']
        options['num_predict'] = profile['max_tokens']  # Open WebUI uses num_predict
        options['presence_penalty'] = profile['presence_penalty']
        options['frequency_penalty'] = profile['frequency_penalty']

        # Apply NIM-specific thinking parameters via extra_body
        if self.valves.enable_thinking:
            extra_body = body.setdefault('extra_body', {})
            extra_body.setdefault('chat_template_kwargs', {})['enable_thinking'] = True
            extra_body['reasoning_budget'] = profile['reasoning_budget']

        if self.valves.debug_log:
            print(
                f"[AI-OS Profile Selector] Applied profile={task_class} | "
                f"temp={profile['temperature']} | reasoning_budget={profile['reasoning_budget']}"
            )

        return body

    # -----------------------------------------------------------------------
    # OUTLET — passthrough
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
