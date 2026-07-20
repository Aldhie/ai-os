# EXP-0001: Temperature Parameter Optimization

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0001 |
| **Title** | Temperature Parameter Optimization for Nemotron Ultra 550B |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Model** | nvidia/nemotron-3-ultra-550b-a55b |
| **Endpoint** | https://integrate.api.nvidia.com/v1 |

## Cross-References

- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0002 NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [AI-0003 Compatibility Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [AI-0003-Critical-Findings-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) — temperature correction from 0.6 → 1.0
- [REQ-AI-0001](../00_ENGINEERING/REQ-INDEX.md)
- [benchmark/tests/reasoning/TC-0001.md](../../benchmark/tests/reasoning/TC-0001.md)
- [benchmark/tests/reasoning/TC-0002.md](../../benchmark/tests/reasoning/TC-0002.md)
- [benchmark/tests/coding/TC-0001.md](../../benchmark/tests/coding/TC-0001.md)

---

## 1. Objective

Determine the optimal `temperature` value for Nemotron Ultra 550B across four task categories: **reasoning**, **coding**, **creative writing**, and **RAG synthesis**. Specifically resolve the conflict between the original AI-0003 recommendation (`temperature: 0.6`) and NVIDIA official documentation (`temperature: 1.0`).

---

## 2. Background

**[FACT]** AI-0003-Critical-Findings-Audit discovered that AI-0003 v1.0.0 recommended `temperature: 0.6` for reasoning tasks. However, ALL official NVIDIA examples for Nemotron Ultra 550B use `temperature: 1.0`. Reference: [NVIDIA NIM API Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b).

**[FACT]** Nemotron Ultra 550B is a MoE + Mamba-2 hybrid architecture, fundamentally different from dense transformers. Temperature behavior may differ from standard OpenAI GPT models where lower temperature = better reasoning.

**[ASSUMPTION]** The `temperature: 1.0` recommendation in NVIDIA docs may be a general default, not task-optimized.

---

## 3. Hypotheses

| ID | Hypothesis | Confidence |
|----|-----------|------------|
| H1 | `temperature: 1.0` performs better than `0.6` on reasoning tasks with thinking ON | Low — counterintuitive |
| H2 | `temperature: 0.6` produces more consistent code than `1.0` | Medium — standard assumption |
| H3 | `temperature: 1.0` produces better creative writing than `0.6` | High — expected |
| H4 | For RAG synthesis with thinking OFF, temperature has minimal impact | Medium |

---

## 4. Variables

### 4.1 Independent Variable
`temperature` values tested: `[0.0, 0.3, 0.6, 0.8, 1.0, 1.2, 1.5]`

### 4.2 Controlled Variables

```yaml
model: nvidia/nemotron-3-ultra-550b-a55b
top_p: 0.95
max_tokens: 2048
seed: 42  # fixed for reproducibility
thinking_mode: per task (see procedure)
repetitions: 5  # each prompt run 5 times per temperature
```

### 4.3 Dependent Variables

- Benchmark score (0–5 scale per AI-9002)
- Response consistency (std dev across 5 runs)
- Token count (completion_tokens from API response)
- Response latency (TTFT where measurable)

---

## 5. Environment

```yaml
platform: NVIDIA Cloud NIM (integrate.api.nvidia.com)
open_webui_version: [to be recorded at execution]
date: [to be recorded at execution]
api_endpoint: https://integrate.api.nvidia.com/v1/chat/completions
auth: env var NVIDIA_API_KEY
rate_limit_strategy: 1 request per 3 seconds
```

---

## 6. Procedure

### Phase 1 — Reasoning (thinking: ON)

For each temperature value in `[0.0, 0.3, 0.6, 0.8, 1.0, 1.2, 1.5]`:
1. Run TC-reasoning-0001 (math proof) × 5 repetitions
2. Run TC-reasoning-0002 (logical deduction) × 5 repetitions
3. Record: score, token count, latency

### Phase 2 — Coding (thinking: ON)

For each temperature value in `[0.0, 0.3, 0.6, 0.8, 1.0]`:
1. Run TC-coding-0001 (algorithm implementation) × 5 repetitions
2. Record: code correctness (unit test pass rate), style score, token count

### Phase 3 — Creative (thinking: OFF)

For each temperature value in `[0.6, 0.8, 1.0, 1.2, 1.5]`:
1. Run TC-discussion-0001 (story continuation) × 3 repetitions
2. Record: creativity score (human eval), coherence score

### Phase 4 — RAG Synthesis (thinking: OFF)

For each temperature value in `[0.0, 0.3, 0.6, 1.0]`:
1. Run TC-rag-0001 (answer from provided document) × 5 repetitions
2. Record: factual accuracy, hallucination count

---

## 7. Expected Results

| Task | Expected Best Temperature | Rationale |
|------|--------------------------|----------|
| Reasoning | 0.6–0.8 | Lower temp = more focused reasoning |
| Coding | 0.3–0.6 | Deterministic code generation |
| Creative | 1.0–1.2 | Higher entropy = more creative output |
| RAG | 0.0–0.3 | Docs are the ground truth; model should not extrapolate |

**Note:** If H1 is confirmed (1.0 > 0.6 for reasoning), this would be a major finding requiring EDR update.

---

## 8. Actual Result

> ⏳ **Status: PENDING** — Not yet executed. Execute per procedure above and fill in results.

```yaml
execution_date: null
executed_by: null
results:
  reasoning:
    best_temperature: null
    scores: {}
  coding:
    best_temperature: null
    scores: {}
  creative:
    best_temperature: null
    scores: {}
  rag:
    best_temperature: null
    scores: {}
```

---

## 9. Analysis

> ⏳ **To be completed post-execution.**

Analysis will address:
1. Does NVIDIA's `temperature: 1.0` recommendation hold empirically for this model?
2. Is task-specific temperature tuning worth the operational complexity?
3. How does temperature interact with thinking mode (ON vs OFF)?

---

## 10. Conclusion

> ⏳ **To be completed post-execution.**

---

## 11. Decision

> ⏳ **To be completed post-execution.** Will result in EDR update to AI-0006 and parameters.json update.

---

## 12. Future Work

- EXP-0002 will investigate `top_p` interaction with temperature
- If task-specific temperatures are adopted, investigate per-profile parameter sets in parameters.json
- Investigate whether `temperature` interacts differently with `medium_effort` thinking mode

---

## 13. Benchmark Results Table

> ⏳ **To be filled post-execution.**

| Temperature | Task | Score (avg/5) | Std Dev | Token Count (avg) | PASS/FAIL |
|-------------|------|--------------|---------|------------------|-----------|
| 0.0 | reasoning | - | - | - | - |
| 0.6 | reasoning | - | - | - | - |
| 1.0 | reasoning | - | - | - | - |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — pending execution |
