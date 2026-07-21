"""
AI-OS Filter: Credential Scrub
Version: 1.0.0
Responsibility: Detect and redact API keys, tokens, and passwords from
                user messages before they are sent to NVIDIA NIM.
Rationale: Users occasionally paste credentials into chat during debugging.
           Sending nvapi- keys, sk- tokens, or Bearer headers to NIM creates
           an external data exposure risk. Redaction happens at inlet so the
           NIM inference call never receives the credential.
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
"""

from pydantic import BaseModel, Field
from typing import Optional
import re


CREDENTIAL_PATTERNS = [
    # NVIDIA NIM API keys
    (re.compile(r'nvapi-[A-Za-z0-9_\-]{20,}'), 'nvapi-[REDACTED]'),
    # OpenAI-style secret keys
    (re.compile(r'sk-[A-Za-z0-9]{20,}'), 'sk-[REDACTED]'),
    # Bearer tokens in Authorization headers pasted as text
    (re.compile(r'Bearer\s+[A-Za-z0-9\-._~+/]{20,}'), 'Bearer [REDACTED]'),
    # Generic API key patterns: apikey=..., api_key=..., API_KEY=...
    (re.compile(r'(?i)(api[_-]?key\s*[=:]\s*)[A-Za-z0-9\-._]{16,}'), r'\1[REDACTED]'),
    # AWS-style access key IDs
    (re.compile(r'(?<![A-Z0-9])[A-Z0-9]{20}(?![A-Z0-9])'), '[REDACTED-AWS-KEY]'),
    # Generic password fields: password=..., passwd=..., secret=...
    (re.compile(r'(?i)(password|passwd|secret|token)\s*[=:]\s*[^\s"]{8,}'), r'\1=[REDACTED]'),
]


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(
            default=True,
            description="Disable credential scrubbing (use only in testing)."
        )
        log_redactions: bool = Field(
            default=True,
            description="Log a warning message when credentials are redacted (no credential value is logged)."
        )

    def __init__(self):
        self.valves = self.Valves()

    def _scrub_text(self, text: str) -> tuple[str, int]:
        """Apply all credential patterns. Returns (scrubbed_text, redaction_count)."""
        count = 0
        for pattern, replacement in CREDENTIAL_PATTERNS:
            new_text, n = pattern.subn(replacement, text)
            count += n
            text = new_text
        return text, count

    # -----------------------------------------------------------------------
    # INLET — scrub messages before NIM call
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body

        total_redactions = 0
        messages = body.get('messages', [])

        for message in messages:
            if message.get('role') == 'user' and isinstance(message.get('content'), str):
                cleaned, count = self._scrub_text(message['content'])
                if count > 0:
                    message['content'] = cleaned
                    total_redactions += count

        if total_redactions > 0 and self.valves.log_redactions:
            # Add a system note to the last user message (not the credential value)
            print(
                f"[AI-OS Credential Scrub] Redacted {total_redactions} potential "
                f"credential(s) from user message before NIM call."
            )

        return body

    # -----------------------------------------------------------------------
    # OUTLET — passthrough
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
