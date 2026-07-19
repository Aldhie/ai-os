# AI-0005: Free Tier Strategy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0005 |
| **Title** | Free Tier Strategy |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the strategy for operating the AI OS within the constraints of free and low-cost tiers, specifically targeting NVIDIA NIM free tier limits. It covers quota management, cost optimization, and graceful degradation.

---

## Scope

- NVIDIA NIM free tier quota and limits
- Token budget management
- Cost optimization techniques
- Fallback strategies
- Monitoring and alerting for quota usage

---

## Dependencies

- `AI-0002-NVIDIA-NIM-API.md` — API layer and error handling
- `docs/10_CONFIGURATION/Parameters.md` — token limits

---

## References

- [NVIDIA Build Free Tier](https://build.nvidia.com/)
- [NIM Pricing](https://www.nvidia.com/en-us/ai/)

---

## NVIDIA NIM Free Tier Limits

> **Note:** Verify current limits from the NVIDIA Build platform dashboard. Limits change frequently.

| Limit | Value (TBD) | Notes |
|-------|-------------|-------|
| API calls per day | TBD | Verify on dashboard |
| Tokens per minute | TBD | Rate limit |
| Tokens per day | TBD | Daily quota |
| Max context per request | TBD | Model limit |

---

## Token Budget Strategy

### System Prompt Optimization

- Keep system prompt concise and minimal
- Avoid embedding large knowledge bases in system prompt
- Use RAG (via Open WebUI) to inject context dynamically

### Context Window Management

```
Total Context = System Prompt + History + Current Message + Reserved Output

Budget allocation:
- System Prompt:    10%
- Conversation History: 40%
- Current Message:  30%
- Reserved Output:  20%
```

### Request Optimization

- Use streaming to detect early stops
- Set appropriate `max_tokens` per request type
- Implement request deduplication where possible
- Cache frequent, deterministic responses where appropriate

---

## Fallback Strategy

If NIM quota is exhausted:

1. Return a graceful error message to the user
2. Log quota exhaustion event
3. Display estimated quota reset time
4. Optionally: route to a smaller, faster backup model

---

## TODO

- [ ] Verify and document current NIM free tier limits
- [ ] Implement token counter in Open WebUI pipeline
- [ ] Set up quota usage dashboard or monitoring
- [ ] Define quota reset schedule and user notifications
- [ ] Evaluate paid tier cost model for scaling
