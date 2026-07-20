# Cache Strategy — Performance Layer

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Cache Architecture

```
┌────────────────────────────────┐
│  L1: In-process cache          │  (session scope, ~100ms TTL)
│  - System prompt token count   │
│  - Active mode config          │
│  - Task classification result  │
└────────────────────────────────┘

┌────────────────────────────────┐
│  L2: Redis cache (5-15min TTL) │  (cross-session)
│  - Memory retrieval results    │
│  - RAG chunk results           │
│  - Tool definition schemas     │
└────────────────────────────────┘

┌────────────────────────────────┐
│  L3: NIM Prefix Cache          │  (NVIDIA-side, server prefix)
│  - System prompt prefix        │
│  - Tool definition prefix      │
└────────────────────────────────┘
```

---

## Cache Key Strategy

```python
# Memory retrieval cache key
memory_cache_key = f"mem:{user_id}:{hash(query_embedding)}"

# RAG chunk cache key  
rag_cache_key = f"rag:{collection_id}:{hash(query_embedding)}"

# NIM prefix cache maximization:
# System prompt must be IDENTICAL byte-for-byte to hit prefix cache
# Do NOT inject dynamic timestamps or session IDs into system prompt
```

---

## Cache Hit Rate Targets

```yaml
targets:
  nim_prefix_cache:    > 70%   # same system prompt repeated across session
  rag_cache:           > 40%   # similar queries within 15min window
  memory_cache:        > 60%   # user preferences don't change mid-session
```

---

*File: runtime/openwebui/performance/cache.md | Last updated: 2026-07-20*
