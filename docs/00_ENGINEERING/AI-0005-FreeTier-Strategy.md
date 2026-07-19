# AI-0005 — Free Tier Strategy

| Field | Value |
|-------|-------|
| **Title** | Free Tier Strategy |
| **Document ID** | AI-0005 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | @Aldhie |
| **Created** | 2026-07-19 |
| **Updated** | 2026-07-19 |
| **Dependencies** | AI-0002 |

---

## Purpose

Documents the strategy for operating AI-OS within the constraints of the NVIDIA NIM free tier, including token budgeting, request queuing, caching, and graceful degradation.

---

## Scope

- Free tier limits (as known)
- Token budget management
- Request rate control
- Caching strategy
- Fallback strategy
- Cost monitoring

---

## Known Free Tier Limits

> Note: Limits subject to change. Always verify at [build.nvidia.com](https://build.nvidia.com).

| Limit Type | Estimated Value | Source |
|------------|----------------|--------|
| Credits on signup | ~1000 API credits | NVIDIA Build Portal |
| RPM (Requests/min) | ~10 | Empirical observation |
| TPM (Tokens/min) | ~50,000 | Estimated |
| Max tokens/request | 4096 output | Verified |

---

## Token Budget Management

| Strategy | Description |
|----------|-------------|
| System prompt compression | Keep system prompt under 2000 tokens |
| Memory truncation | Inject only top-3 most relevant memories |
| RAG truncation | Max 3 RAG chunks, 500 tokens each |
| Conversation pruning | Keep last 20 turns maximum in context |
| Response capping | Default max_tokens = 2048 in free tier mode |

---

## Request Rate Control

```
Incoming Request
      │
      ▼
  Rate Limiter (token bucket, 10 RPM)
      │
  ├── Queue if burst
  └── Pass if within limit
      │
      ▼
  Cache Check ─── Hit → Return cached
      │ Miss
      ▼
  NIM API Call
      │
      ▼
  Cache Store → Return response
```

---

## Caching Strategy

| Cache Type | TTL | Scope |
|------------|-----|-------|
| Exact match (identical prompt) | 1 hour | In-memory |
| Semantic similarity (>0.95 cosine) | 30 min | Vector cache |
| System prompt + config hash | Session | Persistent |

---

## Fallback Strategy

If NIM free tier is exhausted:

1. **Degraded mode**: Route to a smaller, free-tier model (e.g., Mistral 7B via Ollama)
2. **Queue mode**: Accept request, queue for next rate window
3. **Notify user**: Surface a clear message about quota status

---

## References

- [NVIDIA Build Portal](https://build.nvidia.com)
- [NVIDIA API Rate Limits](https://docs.api.nvidia.com)
- AI-0002-NVIDIA-NIM-API.md

---

## TODO

- [ ] Implement token bucket rate limiter in scripts/
- [ ] Add quota monitoring dashboard
- [ ] Test fallback to Ollama local model
- [ ] Document exact current free tier limits
- [ ] Add credit burn rate calculator
