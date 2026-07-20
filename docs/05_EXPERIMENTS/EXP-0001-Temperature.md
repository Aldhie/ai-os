# EXP-0001: Temperature Parameter Sweep

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0001 |
| **Title** | Temperature Parameter Sweep — Quality vs. Coherence Trade-off |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-12 |
| **Related REQ** | REQ-AI-0003 (inference parameter configuration) |
| **Cross-References** | [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) · [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) · [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) |

---

## 1. Objective

Determine the optimal `temperature` value for NVIDIA Nemotron Ultra 550B across three task types: reasoning (analytical), creative (generative), and factual (RAG-style). Validate or refute the official NVIDIA recommendation of `temperature=1.0` for this model.

**Engineering Question:** Is `temperature=1.0` (NVIDIA recommendation) objectively better than `temperature=0.6` (previous assumption) for reasoning tasks on this model?

---

## 2. Hypothesis

> **H1:** `temperature=1.0` will produce higher coherence and accuracy scores on reasoning tasks than `temperature=0.6`, consistent with NVIDIA's official recommendation.
>
> **H2:** `temperature=0.0` will produce deterministic but less creative responses, optimal for RAG/factual tasks.
>
> **H3:** For creative tasks, `temperature=1.0` or higher will produce higher diversity scores without sacrificing coherence.

Basis: NVIDIA official examples universally use `temperature=1.0`. Previous config of `0.6` was an unsupported assumption (see AI-0003-Audit).

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | `temperature` | 0.0, 0.3, 0.6, 0.8, 1.0, 1.2 |
| **Dependent** | Coherence score (1-10) | Measured via rubric |
| **Dependent** | Accuracy score (1-10) | Measured via ground truth |
| **Dependent** | Diversity score (1-10) | Measured via n=5 responses |
| **Controlled** | `top_p` | 0.95 (fixed) |
| **Controlled** | `max_tokens` | 2048 (fixed) |
| **Controlled** | Reasoning mode | `/nothink` (fixed for this experiment) |
| **Controlled** | Model | `nvidia/nemotron-3-ultra-550b-a55b` |
| **Controlled** | System prompt | Standard general assistant |

---

## 4. Environment

| Component | Version/Config |
|-----------|---------------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Endpoint | https://integrate.api.nvidia.com/v1 |
| Open WebUI | Latest stable at test date |
| Test date | TBD (Planned) |
| Runs per value | 5 (minimum per AI-9002 standard) |

---

## 5. Procedure

1. Select 3 test cases from benchmark:
 - `benchmark/tests/reasoning/TC-0001.md` (analytical reasoning)
 - `benchmark/tests/coding/TC-0001.md` (code generation)
 - `benchmark/tests/discussion/TC-0001.md` (open-ended discussion)
2. For each temperature value [0.0, 0.3, 0.6, 0.8, 1.0, 1.2]:
 a. Send identical prompt 5 times
 b. Record full response including token count
 c. Score coherence, accuracy, and diversity via rubric in AI-9002
3. Compute mean ± std for each metric per temperature
4. Plot coherence vs. temperature curve
5. Identify optimal value per task type

---

## 6. Expected Result

Based on official NVIDIA documentation and the model's training characteristics:
- `temperature=1.0` expected to score ≥8.0/10 on coherence for reasoning tasks
- `temperature=0.6` expected to score lower or equal (not better)
- `temperature=0.0` expected to score ≥8.5/10 on accuracy for RAG tasks
- `temperature=1.2` expected to score highest on diversity but may reduce accuracy

---

## 7. Actual Result

> **STATUS: PENDING** — Experiment not yet executed.
>
> This section must be completed before this experiment can transition from `Planned` to `Complete`.

| Run | Temperature | Task Type | Coherence (mean) | Accuracy (mean) | Diversity (mean) | Notes |
|-----|-------------|-----------|-----------------|----------------|-----------------|-------|
| - | 0.0 | Reasoning | PENDING | PENDING | PENDING | - |
| - | 0.6 | Reasoning | PENDING | PENDING | PENDING | - |
| - | 1.0 | Reasoning | PENDING | PENDING | PENDING | - |

---

## 8. Analysis

> **PENDING** — Complete after actual results are recorded.

---

## 9. Conclusion

> **PENDING** — H1, H2, H3 to be evaluated.

---

## 10. Engineering Decision

> **PENDING** — Will update `configs/openwebui/parameters.json` per temperature profile based on results.

Current interim decision: Use `temperature=1.0` per NVIDIA official recommendation until BM-12 produces evidence to the contrary. (EDR-0004)

---

## 11. Future Work

- EXP-0002 (Top-P sweep) should be run with the optimal temperature found here
- Extend to `temperature` interaction with `medium_effort` mode (EXP-0003)
- Test temperature stability across seeds (EXP-0001b)

---

## 12. Benchmark Result Table

> **PENDING** — Populated after experiment execution.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
