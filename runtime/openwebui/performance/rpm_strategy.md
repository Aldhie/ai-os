# RPM (Requests Per Minute) Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Free Tier Limits

```yaml
nvidi_nim_free_tier:
  rpm_limit: 40
  daily_request_limit: 1000
  context_window: 128000
  sla: none
```

---

## RPM Usage Patterns

### Normal Usage (safe)

```
Conversation: 1 request per user turn
Typical turn cadence: 30-60 seconds between turns
Effective RPM: 1-2 RPM
Status: SAFE (40 RPM limit not threatened)
```

### Batch Risk

```
Document analysis: 5-10 chunks, each = 1 request
If processed simultaneously: 5-10 RPM spike
If 3+ batch jobs simultaneously: can approach 30+ RPM
Status: WATCH — add inter-request delay of 2-3s
```

### Danger Zone

```
Pipeline with tool calls + RAG + reflection each calling NIM:
  1 user turn → up to 4 NIM calls
  10 simultaneous users → 40 NIM calls/min
  Status: DANGER — hits RPM limit
Mitigation: Queue requests; batch compression
```

---

## RPM Guard Strategy

```python
# Pseudocode for RPM management
class NIMRateLimiter:
    RPM_LIMIT = 38  # 2 request safety margin
    DAILY_LIMIT = 950  # 50 request safety margin
    
    def should_throttle(self) -> bool:
        return (
            self.requests_this_minute >= self.RPM_LIMIT or
            self.requests_today >= self.DAILY_LIMIT
        )
    
    def get_wait_time(self) -> float:
        # If near RPM limit, wait until next minute window
        return max(0, 60 - self.seconds_in_current_window)
```

---

## Daily Limit Conservation

```
Rule 1: Disable automatic reflection for simple tasks (saves 1 NIM call)
Rule 2: Disable automatic planner for tasks < "complex" class
Rule 3: Use NONE thinking for greeting + simple queries (saves thinking tokens)
Rule 4: Merge tool call results; avoid separate NIM calls per tool
Rule 5: Alert at 800 requests/day; hard stop at 950
```

---

*File: runtime/openwebui/performance/rpm_strategy.md | Last updated: 2026-07-20*
