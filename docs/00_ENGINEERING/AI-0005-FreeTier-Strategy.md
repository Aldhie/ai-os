# AI-0005 — Free Tier Strategy

| Field | Value |
|---|---|
| **Title** | NVIDIA NIM Free Tier Strategy |
| **Document ID** | AI-0005 |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines the strategy for operating AI-OS efficiently within NVIDIA NIM free tier limits. Covers prompt optimization, token budgeting, caching strategies, and graceful degradation patterns.

---

## Scope

- NVIDIA NIM free tier API
- Open WebUI frontend
- Daily operational usage, testing, and development

---

## Free Tier Constraints

> Note: Verify current limits at [build.nvidia.com](https://build.nvidia.com/).

| Resource | Estimated Limit | Notes |
|---|---|---|
| API calls/day | ~40 (nemotron-ultra) | Check dashboard |
| Tokens/minute | TBD | Monitor |
| Tokens/day | TBD | Monitor |
| Context per call | 128K max | Stay under 16K |

---

## Token Budget Guidelines

### System Prompt Budget

```text
System Prompt:    ≤ 2,000 tokens
Conversation:     ≤ 8,000 tokens
RAG Context:      ≤ 4,000 tokens
Response:         ≤ 2,048 tokens
Total Target:     ≤ 16,000 tokens per call
```

### Optimization Techniques

1. **Compress system prompts** — Remove redundancy, use bullet points over prose.
2. **Conversation pruning** — Summarize or truncate older turns beyond 10 exchanges.
3. **RAG snippet limiting** — Retrieve top-3 chunks only, max 500 tokens each.
4. **Lazy tool calling** — Only invoke tools when explicitly needed.
5. **Batch similar queries** — Combine related questions into one turn.

---

## Rate Limit Handling

### Retry Strategy

```text
On 429 (Rate Limited):
  1. Wait: 60 seconds
  2. Retry with backoff: 60s, 120s, 240s
  3. After 3 retries: notify user, halt
```

### Graceful Degradation

When limits are exhausted:

1. Show user a friendly "API limit reached" message.
2. Log the failed request for retry later.
3. Switch to cached response if available.
4. Resume when limit resets (usually UTC midnight).

---

## Cost Optimization Checklist

- [ ] System prompt reviewed for token efficiency
- [ ] Conversation history pruning enabled
- [ ] RAG chunk limit set to ≤3
- [ ] Tool calling policy reviewed (see `docs/10_CONFIGURATION/ToolPolicy.md`)
- [ ] Streaming enabled (improves perceived latency, same token cost)
- [ ] Temperature set appropriately (lower = faster convergence)

---

## Dependencies

- [AI-0002-NVIDIA-NIM-API.md](AI-0002-NVIDIA-NIM-API.md)
- `docs/10_CONFIGURATION/Parameters.md`
- `docs/10_CONFIGURATION/ToolPolicy.md`

---

## References

- [NVIDIA Build Platform](https://build.nvidia.com/)
- [NIM API Pricing](https://www.nvidia.com/en-us/ai/)

---

## TODO

- [ ] Confirm exact free tier limits from NVIDIA dashboard
- [ ] Implement token counter in Open WebUI filter
- [ ] Build daily usage tracking script
- [ ] Document reset schedule (UTC midnight?)
- [ ] Test graceful degradation behavior
