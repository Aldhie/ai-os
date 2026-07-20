# EXP-0002: Top-P (Nucleus Sampling) Calibration

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0002 |
| **Title** | Top-P Nucleus Sampling Calibration |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Inference Parameters |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) | API parameter reference |
| [EXP-0001](EXP-0001-Temperature.md) | Depends on — run after temperature calibration |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0004 |

---

## 1. Objective

Determine the optimal `top_p` value for Nemotron Ultra 550B at the temperature values established in EXP-0001. Validate that NVIDIA's recommended `top_p=0.95` is optimal or identify a better value.

---

## 2. Background

Top-P (nucleus sampling) controls diversity by restricting token selection to the top-P probability mass. [FACT: Official Doc — NVIDIA uses top_p=0.95 in all examples]

Interaction with temperature: top_p and temperature are not independent. High temperature with low top_p creates a different distribution than low temperature with high top_p. [HYPOTHESIS — needs EXP-0001 results first]

---

## 3. Hypothesis

**H1:** `top_p=0.95` (NVIDIA default) is optimal for all task categories when combined with `temperature=1.0`. [HYPOTHESIS]

**H2:** For coding tasks, `top_p=0.85` combined with `temperature=1.0` produces fewer syntax errors than `top_p=0.95`. [HYPOTHESIS]

**H3:** For creative tasks, `top_p=0.98` combined with `temperature=1.0` increases output variety without losing coherence. [HYPOTHESIS]

---

## 4. Variables

### Independent Variable
| Variable | Values |
|----------|--------|
| `top_p` | 0.7, 0.8, 0.85, 0.9, 0.95, 0.98, 1.0 |

### Controlled Variables
| Variable | Value | Reason |
|----------|-------|--------|
| `temperature` | [Best value from EXP-0001] | Use calibrated temperature |
| `max_tokens` | 4096 | Standard |
| `model` | nvidia/nemotron-3-ultra-550b-a55b | Target |
| `seed` | 42 | Reproducibility |

---

## 5. Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Endpoint | https://integrate.api.nvidia.com/v1 |
| Temperature | [Value from EXP-0001 — PENDING] |
| Pipeline | Disabled |

---

## 6. Procedure

Identical task sets as EXP-0001 (reasoning, code, factual, creative).
Run each task at each `top_p` value, holding temperature constant.
Record: output quality, diversity (measured as avg edit distance between 3 runs).

---

## 7. Expected Results

| top_p | Effect |
|-------|--------|
| 0.7 | Conservative, repetitive but coherent |
| 0.85 | Balanced, good for code |
| 0.95 | NVIDIA recommendation — expected to be near-optimal |
| 1.0 | Full distribution — possibly incoherent |

---

## 8. Actual Results

> **Status: PENDING EXECUTION (depends on EXP-0001)**

---

## 9. Conclusion

> **PENDING**

---

## 10. Decision

> **PENDING** — Will update per-profile `top_p` values in `parameters.json`.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial design |
