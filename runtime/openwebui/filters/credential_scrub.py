"""
AI-OS Filter: Credential Scrub
Version: 1.0.0
Responsibility: Detect and redact API keys, tokens, and secrets from user messages
before they reach NVIDIA Cloud NIM.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: Users occasionally paste credentials into chat (deployment configs, .env files,
CI/CD snippets). Sending these to a third-party API endpoint (NIM) creates an
external data exposure risk. This filter eliminates that risk silently and
reports the redaction in the response metadata.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True, description="Enable/disable credential scrubbing")
        redaction_placeholder: str = Field(
            default="[REDACTED-CREDENTIAL]",
            description="Replacement string for detected credentials"
        )

    # Patterns ordered by specificity (most specific first to avoid double-match)
    PATTERNS = [
        # NVIDIA NIM API keys
        (re.compile(r'nvapi-[A-Za-z0-9\-_]{20,}'), "NVIDIA-API-KEY"),
        # OpenAI-style keys
        (re.compile(r'sk-[A-Za-z0-9]{32,}'), "OPENAI-STYLE-KEY"),
        # Generic Bearer tokens (long alphanumeric)
        (re.compile(r'Bearer\s+[A-Za-z0-9\-_.~+/]{20,}={0,2}'), "BEARER-TOKEN"),
        # AWS-style access keys
        (re.compile(r'AKIA[A-Z0-9]{16}'), "AWS-ACCESS-KEY"),
        # Generic password= patterns
        (re.compile(r'(?i)password\s*=\s*[\'"]?[^\s\'"]{8,}[\'"]?'), "PASSWORD-FIELD"),
        # Generic secret= patterns
        (re.compile(r'(?i)secret\s*=\s*[\'"]?[^\s\'"]{8,}[\'"]?'), "SECRET-FIELD"),
        # Private key header (PEM)
        (re.compile(r'-----BEGIN\s+(RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE KEY-----'), "PRIVATE-KEY"),
    ]

    def __init__(self):
        self.valves = self.Valves()
        self._redaction_log: list = []

    def _scrub_text(self, text: str) -> tuple[str, list[str]]:
        """Return (scrubbed_text, list_of_detected_pattern_names)."""
        detected = []
        for pattern, name in self.PATTERNS:
            if pattern.search(text):
                text = pattern.sub(self.valves.redaction_placeholder, text)
                detected.append(name)
        return text, detected

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Scrub credentials from the last user message before sending to NIM.
        Only processes the last message to avoid re-scanning full history on every turn.
        """
        if not self.valves.enabled:
            return body

        messages = body.get("messages", [])
        if not messages:
            return body

        # Find the last user message
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                original = messages[i].get("content", "")
                if isinstance(original, str):
                    scrubbed, detected = self._scrub_text(original)
                    if detected:
                        messages[i]["content"] = scrubbed
                        self._redaction_log.append({
                            "turn": len(messages),
                            "patterns_detected": detected
                        })
                break

        body["messages"] = messages
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. Scrubbing happens at inlet only."""
        return body
