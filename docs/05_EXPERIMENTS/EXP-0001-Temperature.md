# EXP-0001: Temperature Parameter Effect on Output Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0001 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned — Not Yet Executed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0003 |
| **BM** | BM-12 |

## Related Documents

- ↑ [REQ-AI-0003](../00_ENGINEERING/REQ-INDEX.md#req-ai-0003)
- ↑ [AI-0002 NIM API Reference](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md)
- → [EXP-0002 Top-P](./EXP-0002-TopP.md)
- → [EXP-0003 Thinking](./EXP-0003-Thinking.md)

---

## Objective

Determine the optimal temperature value for NVIDIA Nemotron Ultra 550B on qualitative and quantitative tasks. Verify whether NVIDIA's recommendation of temperature=1.0 is correct for this repository's use cases.

---

## Hypothesis

**H1:** temperature=1.0 produces higher quality and more diverse outputs than temperature=0.6 for open-ended tasks (discussion, creative, architecture).

**H2:** temperature=1.0 does not significantly degrade accuracy on deterministic tasks (math, coding, debugging) compared to temperature=0.6.

**H3:** temperature=0.0 (greedy decoding) produces the lowest diversity but highest consistency on deterministic tasks.

**Evidence basis for H1:** All official NVIDIA NIM example requests use temperature=1.0. Source: docs.api.nvidia.com/nim/reference.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| temperature | Independent | 0.0, 0.6, 1.0 |
| Task type | Controlled | Discussion, Coding, Math reasoning |
| thinking mode | Controlled | /nothink for all tests |
| max_tokens | Controlled | 2048 for all tests |
| System prompt | Controlled | Identical for all runs |
| top_p | Controlled | 0.95 |

---

## Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Backend | NVIDIA Cloud NIM |
| Interface | Open WebUI |
| Session | Fresh session per temperature value (no memory) |
| Date | To be filled at execution |

---

## Procedure

1. For each task type (Discussion, Coding, Math):
   a. Create 3 representative test prompts.
   b. For each prompt, run at temperature 0.0, 0.6, and 1.0 (9 runs per task type).
   c. Use identical system prompt and max_tokens for all runs.
   d. Record full response text.
   e. Record token usage.
2. Score each response on a 0–5 scale:
   - Discussion: diversity, coherence, insight depth
   - Coding: correctness, efficiency, documentation
   - Math: step correctness, final answer correctness
3. Calculate mean score per temperature per task type.
4. Run each temperature 3× per prompt to measure variance (27 total runs per task type).

---

## Expected Result

| Temperature | Discussion | Coding | Math |
|-------------|-----------|--------|------|
| 0.0 | Low diversity, correct but flat | Consistent but minimal | Consistent, correct |
| 0.6 | Medium diversity | Good quality | Good quality |
| 1.0 | High diversity, rich insight | Slightly variable but high average | High quality, some variance |

---

## Actual Result

*Status: Not yet executed.*

| Temperature | Discussion Score | Coding Score | Math Score | Mean |
|-------------|-----------------|--------------|------------|------|
| 0.0 | TBD | TBD | TBD | TBD |
| 0.6 | TBD | TBD | TBD | TBD |
| 1.0 | TBD | TBD | TBD | TBD |

---

## Analysis

*To be completed after execution.*

---

## Conclusion

*To be completed after execution.*

---

## Decision

*Pending execution. Current decision: temperature=1.0 based on official NVIDIA documentation (REQ-AI-0003).*

---

## Future Work

- Extend to reasoning mode (thinking ON) to see interaction effect between temperature and thinking depth.
- Test temperature effect on tool call accuracy (EXP-0010).

---

## Benchmark Result

*Status: BM-12 pending execution. No baseline established.*

---

*EXP-0001 v1.0.0 — Created 2026-07-20*
