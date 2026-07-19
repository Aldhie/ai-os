# AI-0005 — Free Tier Strategy

| Field | Value |
|-------|-------|
| **Title** | NVIDIA NIM Free Tier Optimization Strategy |
| **Purpose** | Maximize capability within NVIDIA NIM free tier constraints |
| **Scope** | Token budgeting, prompt compression, caching, request batching |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | AI-0002-NVIDIA-NIM-API.md |
| **References** | NVIDIA NIM pricing page |

---

## 1. Free Tier Constraints

> Verify current limits at https://build.nvidia.com/explore/reasoning

| Limit | Estimated Value | Notes |
|-------|-----------------|-------|
| Requests per minute | ~5-10 | Subject to change |
| Tokens per day | ~50,000 | Subject to change |
| Max context per request | TBD | Verify with API |

## 2. Token Budget Strategy

### System Prompt Compression

- Keep system prompt under **1,000 tokens** in production
- Use a minimal system prompt for testing; full persona for production
- Audit system prompt token count with every version update

### Conversation History Pruning

- Prune conversation history when context exceeds **80% of limit**
- Use summarization to compress older turns
- Implement sliding window with summary injection

### Response Length Control

- Set `max_tokens` conservatively per use case
- For structured tasks (JSON, code), use strict output formatting to minimize verbosity
- Avoid open-ended prompts that generate long preambles

## 3. Caching Strategy

| Cache Type | Mechanism | Benefit |
|------------|-----------|----------|
| Exact match | Redis key-value | Eliminate duplicate requests |
| Semantic cache | Embedding similarity | Reuse near-duplicate responses |
| Template cache | Pre-computed outputs | Fast responses for common queries |

## 4. Request Batching

- Batch independent queries where API supports it
- Avoid sequential calls that can be parallelized

## 5. Monitoring

- Track daily token usage against limit
- Alert at 70% daily token consumption
- Log prompt and completion token counts per request

---

## TODO

- [ ] Confirm exact free tier limits
- [ ] Implement token counting middleware
- [ ] Build Redis cache for exact-match responses
- [ ] Design conversation summarization module
- [ ] Set up usage dashboard
