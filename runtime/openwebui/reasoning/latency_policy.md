# Latency Policy Specification

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Latency Targets

```yaml
latency_targets:

  p50_greeting:       2s
  p50_simple_fact:    3s
  p50_casual:         5s
  p50_analysis:       12s
  p50_architecture:   25s
  p50_deep_reasoning: 45s

  p95_max_acceptable: 90s
  absolute_timeout:   120s
```

---

## Latency Budget Breakdown

For a standard analysis request (target: 12s):
```
Request classification:   <0.1s
Context loading:           0.3s
Memory retrieval:          0.5s
RAG retrieval:             0.7s
Context assembly:          0.2s
NIM API (thinking):        8.0s
NIM API (generation):      2.0s
Post-processing:           0.2s
────────────────────────────────
Total:                    ~12.0s
```

---

## Latency vs. Quality Trade-offs

| Latency Budget | Quality Trade-off |
|---------------|------------------|
| < 5s | Disable thinking; no RAG; minimal history |
| 5-15s | Standard profile; RAG enabled; history enabled |
| 15-45s | Deep profile; full context; planner + reflection |
| > 45s | Maximum profile; explicit user-initiated only |

---

## Streaming Policy

```yaml
streaming: always_enabled  # reduces perceived latency significantly
first_token_target: < 2s   # time to first visible token
user_perception:           # perceived as fast even if total duration is 30s
```

---

*File: runtime/openwebui/reasoning/latency_policy.md | Last updated: 2026-07-20*
