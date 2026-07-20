# Timeout Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Timeout Tiers

```yaml
timeouts:

  connection_timeout:     5s    # TCP connection to NIM API
  read_timeout:         120s    # Streaming response timeout
  first_token_timeout:   15s    # Max wait for first token
  total_request_timeout: 180s   # Hard ceiling per request

  context_assembly:       2s    # Memory + RAG retrieval
  memory_retrieval:       1s    # Brain Memory API call
  rag_retrieval:          2s    # Knowledge base search
```

---

## Timeout Behavior

```
Connection timeout exceeded  → Immediate retry with backoff
First token timeout exceeded → Cancel + retry (may indicate overloaded)
Read timeout exceeded        → Return partial response if > 100 tokens received
                               Otherwise retry
Total timeout exceeded       → Return: "Request timed out. Please try again."
                               Log for monitoring
```

---

## Partial Response Handling

```python
# If streaming is cut at > 100 tokens:
# Append: "\n\n[Response truncated due to timeout]"
# This is better than losing all work

# If streaming is cut at < 100 tokens:
# Discard and retry (partial answer worse than no answer)
```

---

*File: runtime/openwebui/performance/timeout_strategy.md | Last updated: 2026-07-20*
