# AI-0005 — Free Tier Strategy

| Field | Value |
|-------|-------|
| **Title** | NVIDIA NIM Free Tier Optimization Strategy |
| **Purpose** | Maximize value and minimize cost when operating under NVIDIA NIM Free Tier limits |
| **Scope** | Rate limit management, token optimization, caching, graceful degradation |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | AI-0002 (NIM API) |
| **References** | [NVIDIA Build Pricing](https://build.nvidia.com/), [NVIDIA NIM Docs](https://docs.api.nvidia.com/) |

---

## 1. Free Tier Constraints

| Limit | Value | Impact |
|-------|-------|--------|
| Requests per minute | ~10 RPM | Limits concurrent sessions |
| Daily token budget | TBD | Limits total daily usage |
| Max context per call | 128K tokens | Can bloat token usage fast |
| Rate limit recovery | 60s rolling | Requires backoff strategy |

---

## 2. Token Optimization Strategies

### 2.1 System Prompt Compression

- Keep system prompt under 2,000 tokens
- Use references instead of inline content: `See policy: [TOOL_POLICY]`
- Remove redundant instructions covered by the model's default behavior

### 2.2 Conversation Pruning

- Summarize old turns when conversation exceeds 8K tokens
- Use Open WebUI's context window management features
- Store important facts in memory rather than re-injecting full history

### 2.3 Request Batching

- Avoid redundant API calls for the same intent
- Cache responses for identical inputs where appropriate

---

## 3. Rate Limit Handling

```
On 429 error:
  1. Wait 60 seconds (base)
  2. Retry request
  3. If still 429: wait 120 seconds
  4. If still 429: surface error to user gracefully
  5. Log incident for capacity planning
```

---

## 4. Usage Monitoring

| Metric to Track | Method |
|----------------|--------|
| Daily token usage | NVIDIA dashboard |
| RPM utilization | Open WebUI logs |
| Peak usage hours | Application logs |
| Cost per session | Token count × rate |

---

## 5. Upgrade Triggers

Consider upgrading from Free Tier when:

- Daily rate limit hit more than 3 times per week
- Response latency degraded due to queuing
- Use case requires > 10 concurrent users
- Fine-tuning or higher throughput needed

---

## TODO

- [ ] Confirm exact Free Tier limits from NVIDIA
- [ ] Implement token counter in scripts
- [ ] Create daily usage report script
- [ ] Test graceful degradation behavior
- [ ] Document upgrade path to paid tier
