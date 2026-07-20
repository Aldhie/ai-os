# EXP-0002: Top-P (Nucleus Sampling) Parameter Study

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0002 |
| **Title** | Top-P Nucleus Sampling — Diversity vs. Quality Trade-off |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-12 |
| **Related REQ** | REQ-AI-0003 |
| **Depends On** | EXP-0001 (optimal temperature must be known first) |
| **Cross-References** | [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) · [EXP-0001](EXP-0001-Temperature.md) · [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) |

---

## 1. Objective

Determine the optimal `top_p` value for NVIDIA Nemotron Ultra 550B. Validate or refute the official NVIDIA recommendation of `top_p=0.95`. Understand how `top_p` interacts with `temperature=1.0`.

**Engineering Question:** Does `top_p=0.95` (NVIDIA recommendation) produce meaningfully different output from `top_p=0.9` or `top_p=1.0` for this model?

---

## 2. Hypothesis

> **H1:** `top_p=0.95` will produce slightly better output diversity than `top_p=0.9` without sacrificing accuracy.
>
> **H2:** `top_p=1.0` (unconstrained) combined with `temperature=1.0` may produce less coherent output due to unrestricted token sampling.
>
> **H3:** For code generation, lower `top_p` (0.85–0.90) may improve precision by eliminating long-tail token noise.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | `top_p` | 0.70, 0.80, 0.85, 0.90, 0.95, 0.98, 1.00 |
| **Dependent** | Output quality score | 1-10 rubric |
| **Dependent** | Lexical diversity (unique bigrams / total) | Computed |
| **Controlled** | `temperature` | Optimal from EXP-0001 |
| **Controlled** | `max_tokens` | 2048 |
| **Controlled** | Reasoning mode | `/nothink` |

---

## 4. Environment

| Component | Version/Config |
|-----------|---------------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Endpoint | https://integrate.api.nvidia.com/v1 |
| Prerequisite | EXP-0001 must be completed |
| Runs per value | 5 minimum |

---

## 5. Procedure

1. Use optimal temperature from EXP-0001
2. Sweep `top_p` values: [0.70, 0.80, 0.85, 0.90, 0.95, 0.98, 1.00]
3. Use same test prompts as EXP-0001 for comparability
4. Score quality and measure lexical diversity per response
5. Compute mean ± std per value
6. Identify optimal `top_p` per task type

---

## 6. Expected Result

- `top_p=0.95` expected to score ≥8.0/10 per NVIDIA recommendation
- `top_p=1.00` expected to show higher diversity but lower consistency
- Code tasks expected to prefer `top_p` ≤ 0.90

---

## 7. Actual Result

> **STATUS: PENDING** — Blocked on EXP-0001 completion.

---

## 8–12. Analysis / Conclusion / Decision / Future Work / Benchmark Table

> **PENDING** — Complete after EXP-0001 and this experiment are executed.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
