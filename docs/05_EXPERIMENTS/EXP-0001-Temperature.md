# EXP-0001: Temperature Calibration for Nemotron Ultra 550B

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0001 |
| **Title** | Temperature Calibration for Nemotron Ultra 550B |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Inference Parameters |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Model spec |
| [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) | API parameter reference |
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | Compatibility matrix — temperature row |
| [AI-0003-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) | Identified temperature=1.0 vs 0.6 discrepancy |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0003 |
| [BM-12](../../benchmark/tests/nim/TC-0003.md) | Temperature benchmark TC |

---

## 1. Objective

Determine the optimal `temperature` value for NVIDIA Nemotron Ultra 550B across four task categories: **reasoning**, **code generation**, **creative writing**, and **factual Q&A**. Resolve the discrepancy between original config (`0.6`) and NVIDIA official recommendation (`1.0`).

---

## 2. Background

During AI-0003 Critical Findings Audit, it was discovered that:
- AI-0003 v1.0.0 recommended `temperature: 0.6` for reasoning tasks [ASSUMPTION — from OpenAI convention]
- NVIDIA official documentation uses `temperature: 1.0` in ALL examples [FACT: Official Doc]
- Nemotron Ultra uses a thinking-first architecture where temperature affects the **reasoning trace** differently from standard autoregressive models [HYPOTHESIS — needs validation]

This experiment resolves the hypothesis and establishes evidence-based temperature profiles.

---

## 3. Hypothesis

**H1:** `temperature=1.0` produces higher quality reasoning traces than `temperature=0.6` for complex multi-step problems. [HYPOTHESIS]

**H2:** `temperature=0.6` produces better factual accuracy on RAG-based Q&A where determinism is preferred. [HYPOTHESIS]

**H3:** For code generation with reasoning ON, `temperature=1.0` produces correct code more consistently than `temperature=0.6`. [HYPOTHESIS]

---

## 4. Variables

### Independent Variable
| Variable | Values |
|----------|--------|
| `temperature` | 0.0, 0.3, 0.6, 0.8, 1.0, 1.2, 1.5 |

### Controlled Variables
| Variable | Value | Reason |
|----------|-------|--------|
| `top_p` | 0.95 | NVIDIA recommended default [FACT: Official Doc] |
| `max_tokens` | 8192 | Sufficient for reasoning trace + answer |
| `thinking_mode` | ON (`/think`) | Test reasoning quality specifically |
| `model` | nvidia/nemotron-3-ultra-550b-a55b | Target model |
| `seed` | 42 | Reproducibility |
| `n_runs` | 3 per value | Stochastic average |

### Dependent Variables
| Metric | Measurement Method |
|--------|-------------------|
| Reasoning trace quality | Manual scoring 0-100 |
| Answer accuracy | Compare to ground truth |
| Response coherence | Human evaluation |
| Thinking token count | Count `<think>` section tokens |

---

## 5. Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Endpoint | https://integrate.api.nvidia.com/v1 |
| Open WebUI Version | Latest stable |
| Pipeline | Disabled (direct API calls for isolation) |
| Date of Run | PENDING |

---

## 6. Procedure

### Task Set A: Multi-Step Reasoning
Use benchmark TCs from `benchmark/tests/reasoning/` — TC-0001, TC-0002, TC-0003.
Run each TC at each temperature value. Record response and reasoning trace token count.

### Task Set B: Code Generation
Use benchmark TCs from `benchmark/tests/coding/` — TC-0001, TC-0002, TC-0003.
Evaluate: does the code run correctly (pass/fail).

### Task Set C: Factual Q&A
Use benchmark TCs from `benchmark/tests/nim/` — TC-0001, TC-0002.
Evaluate factual accuracy against known ground truth.

### Task Set D: Creative Writing
Use benchmark TCs from `benchmark/tests/discussion/` — TC-0001.
Evaluate coherence and creativity via human scoring.

---

## 7. Expected Results

| Temperature | Reasoning | Code | Factual | Creative |
|-------------|-----------|------|---------|----------|
| 0.0 | Deterministic, possibly repetitive | High accuracy | High accuracy | Poor diversity |
| 0.6 | Good quality | Good | Good | Moderate |
| 1.0 | High quality (NVIDIA recommendation) | Good | Good | High diversity |
| 1.5 | Possibly incoherent | Degraded | Degraded | Very high but incoherent |

---

## 8. Actual Results

> **Status: PENDING EXECUTION**
>
> This experiment has not been run yet. Results will be recorded here upon execution.
> Target execution date: Next benchmark cycle.

| Temperature | Reasoning Score | Code Pass Rate | Factual Accuracy | Creative Score | Thinking Tokens |
|-------------|----------------|----------------|-----------------|----------------|------------------|
| 0.0 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 0.3 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 0.6 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 0.8 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1.0 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1.2 | PENDING | PENDING | PENDING | PENDING | PENDING |
| 1.5 | PENDING | PENDING | PENDING | PENDING | PENDING |

---

## 9. Analysis

> **PENDING — to be written after execution**

Analysis framework (pre-defined):
1. Plot temperature vs. score per task category
2. Identify the Pareto-optimal temperature for each category
3. Determine if a single temperature can serve all categories or if profiles are needed
4. Compare to NVIDIA recommendation (`1.0`) and previous config (`0.6`)

---

## 10. Conclusion

> **PENDING**

---

## 11. Decision

> **PENDING** — Will update `configs/openwebui/parameters.json` with validated temperature values per profile.

Decision will be recorded as EDR-003 in [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md).

---

## 12. Future Work

- EXP-0002: Run Top-P calibration at the optimal temperature found here
- Cross-validate with EXP-0003 (Thinking mode) to check interaction effects

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design, pending execution |
