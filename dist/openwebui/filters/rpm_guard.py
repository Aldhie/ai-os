# AI-OS Production Filter: RPM Guard v1.0.0
# Copy of runtime/openwebui/filters/rpm_guard.py
# See that file for full documentation.
# This copy is in dist/ for direct deployment without cloning full repo.

from pydantic import BaseModel, Field
from typing import Optional
import time
import collections


class Filter:
    class Valves(BaseModel):
        max_rpm: int = Field(default=32, description="Maximum NIM requests per minute")
        window_seconds: int = Field(default=60, description="Rolling window in seconds")
        enabled: bool = Field(default=True, description="Enable/disable RPM guard")

    def __init__(self):
        self.valves = self.Valves()
        self._timestamps: collections.deque = collections.deque()

    def _prune(self):
        cutoff = time.time() - self.valves.window_seconds
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        if not self.valves.enabled:
            return body
        self._prune()
        if len(self._timestamps) >= self.valves.max_rpm:
            oldest = self._timestamps[0]
            wait = int(self.valves.window_seconds - (time.time() - oldest)) + 1
            raise ValueError(f"[AI-OS RPM Guard] NIM Free Tier limit reached. Wait ~{wait}s.")
        self._timestamps.append(time.time())
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
