# EXP-0002: Top-P (Nucleus Sampling) Optimization

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0002 |
| **Title** | Top-P Nucleus Sampling Optimization for Nemotron Ultra 550B |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0002 NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [EXP-0001 Temperature](EXP-0001-Temperature.md)
- [benchmark/tests/reasoning/TC-0001.md](../../benchmark/tests/reasoning/TC-0001.md)

---

## 1. Objective

Determine whether `top_p: 0.95` (NVIDIA default) is optimal for Nemotron Ultra 550B, or whether task-specific top_p values improve output quality. Investigate `top_p` × `temperature` interaction.

---

## 2. Background

**[FACT]** NVIDIA official documentation consistently uses `top_p: 0.95` for all examples. Range is `0.0–1.0`. Reference: [NVIDIA NIM API Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b).

**[HYPOTHESIS]** Lower `top_p` (0.7–0.85) combined with `temperature: 1.0` may produce focused outputs without the stochasticity risks of low temperature.

**[HYPOTHESIS]** For RAG tasks, `top_p: 0.7` + `temperature: 0.6` may reduce hallucination by restricting the token probability mass.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | `top_p: 0.95` is optimal for general use (matches NVIDIA default) |
| H2 | `top_p: 0.7` reduces hallucination in RAG synthesis vs `0.95` |
| H3 | `top_p × temperature` interaction is significant on reasoning tasks |

---

## 4. Variables

**Independent:** `top_p` values: `[0.7, 0.8, 0.9, 0.95, 0.98, 1.0]`
**Controlled:** temperature fixed at 1.0 (per EXP-0001 result or NVIDIA default), max_tokens: 2048, seed: 42
**Dependent:** Benchmark score, token count, hallucination rate on RAG tasks

**Prerequisite:** EXP-0001 must be completed to set temperature baseline before running this experiment.

---

## 5. Environment

```yaml
model: nvidia/nemotron-3-ultra-550b-a55b
endpoint: https://integrate.api.nvidia.com/v1
temperature: [best value from EXP-0001]
seed: 42
```

---

## 6. Procedure

1. For each `top_p` in `[0.7, 0.8, 0.9, 0.95, 0.98, 1.0]`:
   - Run TC-reasoning-0001 × 5 reps
   - Run TC-rag-0001 × 5 reps (score for hallucination)
   - Run TC-coding-0001 × 3 reps
2. Record scores, token counts, hallucination instances
3. Plot top_p vs score per task category
4. Test H3: run reasoning TC with `[top_p=0.7, temp=0.6]` vs `[top_p=0.95, temp=1.0]`

---

## 7. Expected Results

| top_p | Task | Expected Behavior |
|-------|------|------------------|
| 0.7 | reasoning | More focused but potentially repetitive |
| 0.95 | reasoning | Best balance (per NVIDIA default) |
| 0.7 | rag | Lower hallucination |
| 1.0 | creative | Maximum diversity |

---

## 8. Actual Result

> ⏳ **PENDING** — Awaiting EXP-0001 completion for temperature baseline.

---

## 9–13. Analysis / Conclusion / Decision / Future Work / Benchmark Results

> ⏳ **To be completed post-execution.**

**Future Work:** EXP-0003 (Thinking mode) will use temperature and top_p values determined by EXP-0001 and EXP-0002.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
