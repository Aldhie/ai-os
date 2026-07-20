# EXP-0001: Temperature Parameter Sweep

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0001 |
| **Title** | Temperature Parameter Sweep for Nemotron Ultra 550B |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | Critical |

---

## Cross References

- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0002 — NVIDIA NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- [AI-0003-Audit — Critical Findings](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) — Corrected `temperature` from 0.6 to 1.0
- [AI-9002 — Benchmark Standard](../99_GOVERNANCE/AI-9002-Benchmark-Standard.md)
- [TC-NIM-0001 — Temperature Benchmark](../../benchmark/tests/nim/TC-NIM-0001.md)
- [configs/openwebui/parameters.json](../../configs/openwebui/parameters.json)

---

## 1. Objective

Determine the optimal `temperature` value for Nemotron Ultra 550B on NVIDIA Cloud NIM across four task profiles: **general conversation**, **reasoning/analysis**, **creative writing**, and **code generation**.

---

## 2. Hypothesis

> `[HYPOTHESIS]` NVIDIA documentation consistently uses `temperature: 1.0` in all official examples. We hypothesize that `temperature: 1.0` is optimal for this model across all profiles, and that the previous value of `0.6` (from AI-0003 v1.0.0) was an incorrect assumption derived from general LLM folklore. However, we further hypothesize that code generation and structured output tasks may benefit from lower temperatures (`0.0–0.3`) to reduce syntactic variability.

**AI-0003-Audit Correction:** `temperature: 0.6` in `parameters.json` was identified as an assumption. Official docs show `temperature: 1.0`. This experiment validates which value produces better outputs across task types.

---

## 3. Variables

### Independent Variable

| Parameter | Test Values |
|-----------|-------------|
| `temperature` | `0.0`, `0.3`, `0.6`, `0.8`, `1.0`, `1.2`, `1.5` |

### Controlled Variables

| Parameter | Value |
|-----------|-------|
| `top_p` | `0.95` |
| `max_tokens` | `2048` |
| `model` | `nvidia/nemotron-3-ultra-550b-a55b` |
| `thinking` | OFF (`/nothink`) for general/code; ON (`/think`) for reasoning |
| `seed` | `42` (fixed per run) |

### Dependent Variables

- Response coherence (human eval 1–5)
- Response diversity across 3 runs at same temperature
- Task accuracy (correct answer: 0/1 for factual, rubric for creative)
- Token count (efficiency proxy)

---

## 4. Environment

| Component | Value |
|-----------|-------|
| API Endpoint | `https://integrate.api.nvidia.com/v1/chat/completions` |
| Model | `nvidia/nemotron-3-ultra-550b-a55b` |
| Client | Python `openai` SDK v1.x |
| Open WebUI | Latest stable (for OW-integrated runs) |
| Date | `[PENDING — fill on execution]` |
| NIM Version | `[PENDING — check response headers]` |

---

## 5. Procedure

For each temperature value `t` in `[0.0, 0.3, 0.6, 0.8, 1.0, 1.2, 1.5]`:

1. Send each of the four task prompts (one per profile) with `temperature: t`
2. Repeat each prompt 3 times to measure variance
3. Record: raw response text, token count, latency (TTFT + total)
4. Score response using the Evaluation Criteria below
5. Record mean score and variance per temperature

**Task Prompts:**

- **General:** `"Explain the concept of entropy in thermodynamics and information theory. Describe the relationship between the two."`
- **Reasoning:** `"A researcher claims that correlation implies causation in medical studies if the sample size is large enough. Is this claim correct? Provide a rigorous analysis."`
- **Creative:** `"Write the opening paragraph of a novel set in a hotel during a power outage. Convey atmosphere and tension without dialogue."`
- **Code:** `"Write a Python function that takes a list of integers and returns a new list containing only prime numbers, using no external libraries. Include type hints and docstring."`

---

## 6. Evaluation Criteria

| Task | Criterion | Weight |
|------|-----------|--------|
| General | Factual accuracy | 40% |
| General | Depth and completeness | 30% |
| General | Clarity of explanation | 30% |
| Reasoning | Logical validity | 50% |
| Reasoning | Identifies key fallacy/nuance | 30% |
| Reasoning | Cites relevant counterexamples | 20% |
| Creative | Atmospheric quality | 40% |
| Creative | Originality | 30% |
| Creative | Narrative tension | 30% |
| Code | Correctness (test against input `[2, 3, 4, 5, 6, 7]`) | 50% |
| Code | Code quality (readability, type hints) | 30% |
| Code | Efficiency (no O(n³) algorithms) | 20% |

---

## 7. Expected Result

- General: `temperature: 0.8–1.0` expected optimal (balance of diversity + coherence)
- Reasoning: `temperature: 0.6–0.8` expected optimal (structured, consistent)
- Creative: `temperature: 1.0–1.2` expected optimal (diversity valued)
- Code: `temperature: 0.0–0.3` expected optimal (deterministic, correct syntax)

---

## 8. Actual Result

> `[PENDING — execute experiment and fill this section]`

| Temperature | General Score | Reasoning Score | Creative Score | Code Score | Mean |
|-------------|---------------|-----------------|----------------|------------|------|
| 0.0 | TBD | TBD | TBD | TBD | TBD |
| 0.3 | TBD | TBD | TBD | TBD | TBD |
| 0.6 | TBD | TBD | TBD | TBD | TBD |
| 0.8 | TBD | TBD | TBD | TBD | TBD |
| 1.0 | TBD | TBD | TBD | TBD | TBD |
| 1.2 | TBD | TBD | TBD | TBD | TBD |
| 1.5 | TBD | TBD | TBD | TBD | TBD |

---

## 9. Analysis

> `[PENDING — fill after execution]`

---

## 10. Conclusion

> `[PENDING — fill after execution]`

---

## 11. Decision

> `[PENDING]` Upon completion, update `parameters.json` with the validated `temperature` values per profile. Close the hypothesis in AI-0003-Audit NEW-04.

**Tracking:** This experiment was created as a direct result of AI-0003-Audit finding that `temperature: 0.6` was an unvalidated assumption (Correction BM-12).

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design — created from AI-0003-Audit temperature correction |
