# Context Cache Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## What Gets Cached

```yaml
cacheable:
  system_prompt: true        # static; never changes per session
  persona_active: true       # changes only on mode switch
  rag_chunks: true           # cache per query hash (15min TTL)
  memory_retrieval: true     # cache per user + query hash (5min TTL)
  tool_definitions: true     # static; cache permanently

not_cacheable:
  user_messages: false       # always fresh
  current_response: false    # never cache output
  thinking_trace: false      # ephemeral
```

---

## Cache TTL Policy

| Cache Type | TTL | Invalidation Trigger |
|-----------|-----|---------------------|
| System prompt | Session | Mode switch |
| RAG chunks | 15 min | Query hash change |
| Memory retrieval | 5 min | New memory written |
| Tool definitions | Permanent | Tool list update |

---

## NIM API Prompt Caching

NVIDIA NIM supports prefix caching. Maximize cache hit rate by:

1. **Keep system prompt IDENTICAL across requests** — no dynamic content in system prompt
2. **Place system prompt first** in the context — before any variable content
3. **Avoid modifying tool definitions** between requests in the same session
4. Prefix cache hit → ~50% latency reduction on repeated structure

---

## Free Tier Cache Impact

```
Without cache: 40 RPM limit hit faster (full token processing each call)
With cache:    Effective capacity increases; fewer tokens processed = lower cost
Target:        > 60% prefix cache hit rate in active sessions
```

---

*File: runtime/openwebui/context/cache_strategy.md | Last updated: 2026-07-20*
