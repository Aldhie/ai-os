# Retry Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Retry Policy

```yaml
retry_policy:

  rate_limit_429:
    max_retries: 3
    initial_delay: 2s
    backoff: exponential
    backoff_multiplier: 2.0
    max_delay: 30s
    jitter: true

  server_error_5xx:
    max_retries: 2
    initial_delay: 1s
    backoff: linear
    max_delay: 5s

  network_timeout:
    max_retries: 2
    initial_delay: 0.5s
    backoff: linear

  no_retry:
    - 400 Bad Request (fix the request)
    - 401 Unauthorized (fix the key)
    - 403 Forbidden
    - 404 Not Found
```

---

## Fallback on Retry Exhaustion

```
Retry exhausted on NIM →
  1. Try Ollama local (if available)
  2. Return degraded response with explanation
  3. Log failure for monitoring
  4. Never silently fail
```

---

## Rate Limit Recovery

```python
# On 429 response:
# 1. Extract Retry-After header if present
# 2. Wait Retry-After seconds
# 3. If no Retry-After: use exponential backoff
# 4. After 3rd retry: fall back to Ollama
# 5. Log: request_id, error_code, wait_time, fallback_used
```

---

*File: runtime/openwebui/performance/retry_strategy.md | Last updated: 2026-07-20*
