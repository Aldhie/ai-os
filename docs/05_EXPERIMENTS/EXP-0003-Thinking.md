# EXP-0003: Thinking Mode — Token Cost vs Quality Tradeoff

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0003 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0004, REQ-AI-0011 |
| **BM** | BM-11, BM-12 |

## Related Documents

- ↑ [REQ-AI-0004](../00_ENGINEERING/REQ-INDEX.md#req-ai-0004)
- ↑ [REQ-AI-0011](../00_ENGINEERING/REQ-INDEX.md#req-ai-0011)
- ↑ [AI-0005 Free Tier Strategy](../00_ENGINEERING/AI-0005-FreeTier-Strategy.md)

---

## Objective

Measure the actual token cost of thinking modes (OFF, medium_effort, ON) and quantify the quality improvement per token spent. Establish data-driven thresholds for when thinking mode is worth the token cost.

---

## Hypothesis

**H1:** Thinking ON produces statistically significant quality improvement on reasoning tasks (math, logic, multi-step planning) vs Thinking OFF.

**H2:** Thinking ON does NOT significantly improve quality on simple Q&A, factual recall, or creative tasks.

**H3:** medium_effort produces 70–85% of Thinking ON quality at 30–40% of the token cost.

**H4:** Thinking trace token count scales with problem complexity, not prompt length.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Thinking mode | Independent | OFF (/nothink), medium_effort, ON (/think) |
| Task difficulty | Independent | Easy, Medium, Hard |
| Task type | Independent | Math, Logic, Coding, Discussion |
| temperature | Controlled | 1.0 |
| top_p | Controlled | 0.95 |

---

## Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Backend | NVIDIA Cloud NIM |
| Interface | Open WebUI |
| Metric | OW token usage display + manual counting |

---

## Procedure

1. Create test matrix:
   - 4 task types × 3 difficulties = 12 prompts
2. For each prompt, run all 3 thinking modes.
3. Record: (a) thinking trace token count, (b) response token count, (c) total tokens, (d) response quality score 0–5.
4. Calculate:
   - Quality gain per 1,000 tokens spent on thinking
   - Break-even point: minimum difficulty where thinking is worth cost
5. Note medium_effort results specifically — Pipeline injection required.

---

## Expected Result

| Thinking Mode | Avg Token Cost | Quality Gain (Easy) | Quality Gain (Hard) |
|--------------|----------------|---------------------|---------------------|
| OFF | ~800 | Baseline | Baseline |
| medium_effort | ~3,000 | Minimal | +1.0–1.5 pts |
| ON | ~12,000 | Minimal | +1.5–2.0 pts |

---

## Actual Result

*Status: Not yet executed.*

| Mode | Easy Math | Medium Math | Hard Math | Coding | Logic |
|------|-----------|-------------|-----------|--------|-------|
| OFF | TBD | TBD | TBD | TBD | TBD |
| medium_effort | TBD | TBD | TBD | TBD | TBD |
| ON | TBD | TBD | TBD | TBD | TBD |

---

## Analysis

*Pending execution. Will produce: Thinking Break-Even Chart (task complexity vs thinking ROI).*

---

## Conclusion

*Pending execution.*

---

## Decision

**Current (provisional):** Use thinking OFF for general tasks, thinking ON for hard reasoning. This is conservative — EXP-0003 will validate or refine.

---

## Future Work

- Automate thinking mode selection via Pipeline based on task classification.
- Extend to reasoning_budget parameter (granular thinking depth control).

---

## Benchmark Result

*BM-11 and BM-12 pending.*

---

*EXP-0003 v1.0.0 — Created 2026-07-20*
