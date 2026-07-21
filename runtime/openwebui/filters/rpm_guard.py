"""
AI-OS Filter: RPM Guard
Version: 1.0.0
Responsibility: Enforce NVIDIA Cloud NIM Free Tier 32 RPM ceiling.
Rationale: NIM Free Tier shared infrastructure returns hard 429 errors
           when quota is exceeded, breaking the session state. Proactive
           rejection at the Open WebUI gateway is cleaner and produces a
           user-facing message instead of a silent API failure.
Install: Open WebUI > Admin > Functions > + New Function > paste this file.
"""

from pydantic import BaseModel, Field
from typing import Optional
import time
import threading


# ---------------------------------------------------------------------------
# Valve configuration exposed in Open WebUI Admin > Functions UI
# ---------------------------------------------------------------------------
class Filter:
    class Valves(BaseModel):
        max_rpm: int = Field(
            default=32,
            description="Maximum NIM API requests per 60-second window. NVIDIA Free Tier hard limit is 32."
        )
        safety_margin: int = Field(
            default=2,
            description="Reserve this many RPM slots as safety buffer. Effective limit = max_rpm - safety_margin."
        )
        enabled: bool = Field(
            default=True,
            description="Disable to bypass RPM guard (use only in testing)."
        )

    def __init__(self):
        self.valves = self.Valves()
        self._lock = threading.Lock()
        self._request_timestamps: list[float] = []

    # -----------------------------------------------------------------------
    # INLET — called before each NIM request
    # -----------------------------------------------------------------------
    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        """
        Count requests in the last 60 seconds.
        Reject with HTTP 429-equivalent if effective limit is reached.
        """
        if not self.valves.enabled:
            return body

        effective_limit = self.valves.max_rpm - self.valves.safety_margin
        now = time.monotonic()
        window_start = now - 60.0

        with self._lock:
            # Purge timestamps outside the 60-second window
            self._request_timestamps = [
                ts for ts in self._request_timestamps if ts > window_start
            ]
            current_count = len(self._request_timestamps)

            if current_count >= effective_limit:
                oldest = self._request_timestamps[0]
                wait_seconds = int(60.0 - (now - oldest)) + 1
                raise Exception(
                    f"[AI-OS RPM Guard] Rate limit reached: {current_count}/{effective_limit} "
                    f"requests in the last 60 seconds. "
                    f"Please wait approximately {wait_seconds} seconds before retrying. "
                    f"(NVIDIA Cloud NIM Free Tier: {self.valves.max_rpm} RPM)"
                )

            # Record this request
            self._request_timestamps.append(now)

        return body

    # -----------------------------------------------------------------------
    # OUTLET — passthrough, no modification needed
    # -----------------------------------------------------------------------
    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        return body
