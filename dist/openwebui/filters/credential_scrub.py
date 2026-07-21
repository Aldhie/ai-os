# AI-OS Production Filter: Credential Scrub v1.0.0
# Source: runtime/openwebui/filters/credential_scrub.py
# Install: Open WebUI Admin > Functions > New Function (type: Filter)
# Install order: 2 (after rpm_guard, before profile_selector)

from pydantic import BaseModel, Field
from typing import Optional
import re


class Filter:
    class Valves(BaseModel):
        enabled: bool = Field(default=True)
        redaction_placeholder: str = Field(default="[REDACTED-CREDENTIAL]")

    PATTERNS = [
        (re.compile(r'nvapi-[A-Za-z0-9\-_]{20,}'), "NVIDIA-API-KEY"),
        (re.compile(r'sk-[A-Za-z0-9]{32,}'), "OPENAI-STYLE-KEY"),
        (re.compile(r'Bearer\s+[A-Za-z0-9\-_.~+/]{20,}={0,2}'), "BEARER-TOKEN"),
        (re.compile(r'AKIA[A-Z0-9]{16}'), "AWS-ACCESS-KEY"),
        (re.compile(r'(?i)password\s*=\s*[\'"]?[^\s\'"]{8,}[\'"]?'), "PASSWORD-FIELD"),
        (re.compile(r'(?i)secret\s*=\s*[\'"]?[^\s\'"]{8,}[\'"]?'), "SECRET-FIELD"),
        (re.compile(r'-----BEGIN\s+(RSA\s+|EC\s+|OPENSSH\s+)?PRIVATE KEY-----'), "PRIVATE-KEY"),
    ]

    def __init__(self):
        self.valves = self.Valves()

    def _scrub(self, text: str) -> tuple:
        detected = []
        for pattern, name in self.PATTERNS:
            if pattern.search(text):
                text = pattern.sub(self.valves.redaction_placeholder, text)
                detected.append(name)
        return text, detected

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        messages = body.get("messages", [])
        for i in range(len(messages) - 1, -1, -1):
            if messages[i].get("role") == "user":
                content = messages[i].get("content", "")
                if isinstance(content, str):
                    scrubbed, detected = self._scrub(content)
                    if detected:
                        messages[i]["content"] = scrubbed
                break
        body["messages"] = messages
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
