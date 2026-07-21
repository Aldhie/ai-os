"""
AI-OS Filter: Task Classifier
Version: 1.0.0
Responsibility: Classify the user's query into a task_class and attach it
                as metadata to the request body. Used by Profile Selector
                and Context Budget Enforcer downstream.
Rationale: Task classification must happen before the NIM call so that the
           correct parameter profile and reasoning budget can be applied.
           Classification uses keyword and pattern matching — no NIM call
           is needed for this step, keeping RPM cost at zero.
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


# ---------------------------------------------------------------------------
# Classification rules — evaluated in priority order (first match wins)
# ---------------------------------------------------------------------------
TASK_RULES: list[tuple[str, list[str]]] = [
    # Greetings and acknowledgements
    ("greeting", [
        r"^(hi|hello|hey|halo|selamat|good morning|good afternoon|good evening|thanks|thank you|terima kasih|ok|okay|got it|understood|noted)\b",
        r"^(oke|oks|sip|mantap|baik|siap)\b",
    ]),
    # Debugging and error diagnosis
    ("debugging", [
        r"\b(error|exception|traceback|stack trace|crash|bug|fix|diagnos|root cause|why (is|does|did)|not working|failing|fails|broken)\b",
        r"\b(debug|debugging|troubleshoot)\b",
    ]),
    # Coding
    ("coding", [
        r"\b(write|implement|create|build|generate|code|function|class|method|script|program|algorithm|refactor|review|test)\b",
        r"```[a-z]+",  # code fence in message
        r"\b(python|javascript|typescript|go|rust|java|c\+\+|sql|bash|terraform|yaml|json)\b",
    ]),
    # Architecture and system design
    ("architecture", [
        r"\b(architect|design|system|infrastructure|microservice|monolith|database|schema|api|service mesh|load balancer|scalab|availab|reliab|trade.off)\b",
        r"\b(how (should|would) (i|we|you) design|design pattern|best practice for building)\b",
    ]),
    # Research and synthesis
    ("research", [
        r"\b(research|survey|compare|comparison|vs\.|versus|pros and cons|literature|study|paper|academic|state of the art|benchmark)\b",
        r"\b(what (are|is) the (best|top|main)|overview of|summary of|explain the difference)\b",
    ]),
    # Analysis
    ("analysis", [
        r"\b(analys|evaluate|assess|review|audit|measure|metric|kpi|performance|bottleneck|profil)\b",
    ]),
    # Planning
    ("planning", [
        r"\b(plan|roadmap|phase|milestone|sprint|timeline|schedule|priorit|backlog|epic|story)\b",
        r"\b(how (do|should) (i|we) (approach|structure|organise|organize))\b",
    ]),
    # Creative
    ("creative", [
        r"\b(write a|draft|story|poem|creative|brainstorm|idea|name|slogan|marketing copy)\b",
    ]),
    # Default: conversational
    ("conversational", [r".+"]),
]


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True,
            description="Disable task classification (all requests default to conversational)."
        )
        debug_log: bool = Field(
            default=False,
            description="Log the classified task_class for each request (useful during tuning)."
        )

    def __init__(self):
        self.valves = self.Valves()
        # Pre-compile all patterns
        self._compiled: list[tuple[str, list[re.Pattern]]] = [
            (task_class, [re.compile(p, re.IGNORECASE) for p in patterns])
            for task_class, patterns in TASK_RULES
        ]

    def _classify(self, text: str) -> str:
        for task_class, patterns in self._compiled:
            for pattern in patterns:
                if pattern.search(text):
                    return task_class
        return "conversational"

    # -----------------------------------------------------------------------
    # INLET
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            body.setdefault('metadata', {})['task_class'] = 'conversational'
            return body

        # Extract the last user message
        messages = body.get('messages', [])
        last_user_text = ''
        for msg in reversed(messages):
            if msg.get('role') == 'user':
                last_user_text = msg.get('content', '')
                if isinstance(last_user_text, list):  # multimodal content
                    last_user_text = ' '.join(
                        p.get('text', '') for p in last_user_text if isinstance(p, dict)
                    )
                break

        task_class = self._classify(last_user_text)

        body.setdefault('metadata', {})['task_class'] = task_class

        if self.valves.debug_log:
            print(f"[AI-OS Task Classifier] task_class={task_class} | query_preview={last_user_text[:80]}")

        return body

    # -----------------------------------------------------------------------
    # OUTLET — passthrough
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
