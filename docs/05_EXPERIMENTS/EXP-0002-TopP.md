# EXP-0002: Top-P (Nucleus Sampling) Effect on Output Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0002 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0002, REQ-AI-0003 |

## Related Documents

- ↑ [REQ-AI-0002](../00_ENGINEERING/REQ-INDEX.md#req-ai-0002)
- → [EXP-0001 Temperature](./EXP-0001-Temperature.md)

---

## Objective

Determine the optimal top_p value for NVIDIA Nemotron Ultra 550B. Evaluate whether the NVIDIA-recommended top_p=0.95 is optimal, or if lower values (0.7, 0.85) improve coherence on structured tasks.

---

## Hypothesis

**H1:** top_p=0.95 produces higher diversity without quality loss vs top_p=0.7 for reasoning tasks.

**H2:** For deterministic tasks (code generation), top_p=0.85 may outperform top_p=0.95 by reducing irrelevant token candidates.

**Note:** top_p and temperature interact multiplicatively. This experiment must control temperature at 1.0 (per REQ-AI-0003) across all runs.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| top_p | Independent | 0.7, 0.85, 0.95, 1.0 |
| temperature | Controlled | 1.0 (per REQ-AI-0003) |
| thinking mode | Controlled | /nothink |
| max_tokens | Controlled | 2048 |

---

## Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Backend | NVIDIA Cloud NIM |
| Interface | Open WebUI |
| Session | Fresh session per top_p value |

---

## Procedure

1. Select 3 test prompts: (a) coding problem, (b) reasoning problem, (c) creative writing.
2. For each prompt, run at top_p = 0.7, 0.85, 0.95, 1.0.
3. Repeat each configuration 3× to measure variance.
4. Score on 0–5 scale per task type criteria.
5. Calculate mean score and variance per top_p value.

---

## Expected Result

| top_p | Coding | Reasoning | Creative |
|-------|--------|-----------|----------|
| 0.70 | High coherence, low diversity | May miss reasoning paths | Repetitive |
| 0.85 | Good balance | Good | Good |
| 0.95 | Good balance | NVIDIA recommended | High diversity |
| 1.00 | Slightly noisy | Max diversity | Maximum diversity |

---

## Actual Result

*Status: Not yet executed.*

---

## Conclusion

*Pending execution. Provisional: top_p=0.95 per NVIDIA recommendation.*

---

## Decision

*Pending execution. Current: top_p=0.95 (all profiles).*

---

## Benchmark Result

*Pending.*

---

*EXP-0002 v1.0.0 — Created 2026-07-20*
