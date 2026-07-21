"""
AI-OS Filter: RPM Guard
Version: 1.0.0
Responsibility: Enforce NVIDIA Cloud NIM Free Tier 32 RPM ceiling.
Install: Open WebUI Admin > Functions > New Function (type: Filter)

WHY: NIM Free Tier hard-limits at 32 RPM on shared infrastructure.
A 429 from NIM breaks the active streaming session with no graceful recovery.
Proactive rejection at the Open WebUI layer surfaces a clean error message
before the request reaches NIM, preserving session integrity.
"""

from pydantic import BaseModel, Field
from typing import Optional
import time
import collections


class Filter:
    class Valves(BaseModel):
        max_rpm: int = Field(default=32, description="Maximum NIM requests per minute (Free Tier = 32)")
        window_seconds: int = Field(default=60, description="Rolling window in seconds")
        enabled: bool = Field(default=True, description="Enable/disable RPM guard")

    def __init__(self):
        self.valves = self.Valves()
        # Deque stores Unix timestamps of recent requests within the rolling window
        self._timestamps: collections.deque = collections.deque()

    def _prune(self) -> None:
        """Remove timestamps outside the rolling window."""
        cutoff = time.time() - self.valves.window_seconds
        while self._timestamps and self._timestamps[0] < cutoff:
            self._timestamps.popleft()

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Pre-NIM filter. Counts requests in the rolling window.
        Raises ValueError (surfaced as error message in OWU) if limit reached.
        """
        if not self.valves.enabled:
            return body

        self._prune()
        current_count = len(self._timestamps)

        if current_count >= self.valves.max_rpm:
            oldest = self._timestamps[0]
            wait_seconds = int(self.valves.window_seconds - (time.time() - oldest)) + 1
            raise ValueError(
                f"[AI-OS RPM Guard] NIM Free Tier limit reached ({self.valves.max_rpm} RPM). "
                f"Please wait approximately {wait_seconds} seconds before sending another message."
            )

        self._timestamps.append(time.time())
        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """Pass-through. RPM is counted at inlet only."""
        return body
