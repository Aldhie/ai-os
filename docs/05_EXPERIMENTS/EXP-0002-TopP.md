# EXP-0002: Top-P (Nucleus Sampling) Sensitivity

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0002 |
| **Title** | Top-P Nucleus Sampling Sensitivity for Nemotron Ultra 550B |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [AI-0002 — NVIDIA NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [EXP-0001 — Temperature](EXP-0001-Temperature.md) — `top_p` must be co-analyzed with temperature
- [AI-9002 — Benchmark Standard](../99_GOVERNANCE/AI-9002-Benchmark-Standard.md)
- [configs/openwebui/parameters.json](../../configs/openwebui/parameters.json)

---

## 1. Objective

Measure the sensitivity of Nemotron Ultra 550B output quality to `top_p` values. Determine whether `0.95` (NVIDIA official recommendation) is genuinely optimal or whether task-specific tuning yields meaningful improvement.

---

## 2. Hypothesis

> `[HYPOTHESIS]` NVIDIA recommends `top_p: 0.95` across all tasks. We hypothesize that `top_p` has lower sensitivity than `temperature` for this model, and that values in range `0.85–0.99` produce negligible quality differences. Lower values (`<0.8`) may cause repetitive output.

---

## 3. Variables

### Independent Variable

| Parameter | Test Values |
|-----------|-------------|
| `top_p` | `0.7`, `0.8`, `0.85`, `0.9`, `0.95`, `0.99`, `1.0` |

### Controlled Variables

| Parameter | Value |
|-----------|-------|
| `temperature` | `1.0` (from EXP-0001 optimal, or `1.0` if EXP-0001 pending) |
| `max_tokens` | `2048` |
| `model` | `nvidia/nemotron-3-ultra-550b-a55b` |
| `thinking` | OFF (`/nothink`) |
| `seed` | `42` |

---

## 4. Environment

| Component | Value |
|-----------|-------|
| API Endpoint | `https://integrate.api.nvidia.com/v1/chat/completions` |
| Model | `nvidia/nemotron-3-ultra-550b-a55b` |
| Depends On | EXP-0001 completion (for temperature value) |
| Date | `[PENDING]` |

---

## 5. Procedure

1. Fix `temperature` at EXP-0001 optimal value (or `1.0` if EXP-0001 pending)
2. Sweep `top_p` across `[0.7, 0.8, 0.85, 0.9, 0.95, 0.99, 1.0]`
3. Use same four task prompts as EXP-0001
4. 3 runs per value
5. Score per EXP-0001 Evaluation Criteria
6. Additionally measure: repetition rate (lexical diversity metric)

---

## 6. Expected Result

- Scores relatively flat between `0.85–0.99`
- Degradation below `0.8` (repetition, reduced diversity)
- `1.0` may cause slight quality drop (sampling from full distribution)

---

## 7. Actual Result

> `[PENDING]`

---

## 8. Decision

> `[PENDING]` Update `parameters.json` with validated `top_p` per profile.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
