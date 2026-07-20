# Latency Optimization Specification

> **Status**: RUNTIME | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Latency Sources and Optimizations

### Source 1: Context Assembly

```
Problem:  Assembling large context from multiple sources adds latency
Target:   < 200ms for context assembly
Strategy:
  - Cache system prompt (never re-assemble each call)
  - Cache memory retrieval (5min TTL)
  - Cache RAG chunks (15min TTL)
  - Async parallel: retrieve memory + RAG simultaneously
  - Pre-filter context BEFORE sending to NIM
```

### Source 2: NIM API Network

```
Problem:  Round-trip to NVIDIA Cloud adds baseline latency
Target:   Minimize by maximizing prefix cache hits
Strategy:
  - Always stream (reduces perceived latency dramatically)
  - Keep system prompt identical across requests (prefix cache)
  - Batch requests during off-peak when possible
```

### Source 3: Thinking Tokens

```
Problem:  Thinking tokens add ~0.5-1ms per token of thinking budget
Target:   Never exceed thinking budget for the task class
Strategy:
  - Use NONE profile for greeting/simple
  - Use LIGHT profile for casual
  - Reserve DEEP/MAXIMUM for architecture/proof
  - budget_tokens controls the MAXIMUM, not guaranteed usage
```

---

## Latency Measurement

```yaml
metrics_to_track:
  - time_to_first_token (TTFT): most important for UX
  - total_response_time: SLA metric
  - context_assembly_time: internal optimization metric
  - thinking_token_count: actual vs budget
  - output_token_count: calibration metric
```

---

*File: runtime/openwebui/performance/latency.md | Last updated: 2026-07-20*
