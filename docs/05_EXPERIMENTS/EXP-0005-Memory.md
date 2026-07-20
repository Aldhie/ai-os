# EXP-0005: Memory Policy — Recall Accuracy and Context Impact

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0005 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0009 |
| **BM** | MEM-TC-0001, MEM-TC-0002 |

## Related Documents

- ↑ [REQ-AI-0009](../00_ENGINEERING/REQ-INDEX.md#req-ai-0009)
- → [EXP-0006 RAG](./EXP-0006-RAG.md)

---

## Objective

Measure the accuracy of Open WebUI memory recall, the impact of memory injection on context budget, and identify conditions where memory helps vs hurts response quality.

---

## Hypothesis

**H1:** Auto-recall of relevant memories improves response personalization without the user needing to re-state preferences.

**H2:** Stale memories (>14 days old, no longer accurate) injected into context decrease response quality by introducing contradictory information.

**H3:** Memory injection > 2,048 tokens begins to degrade quality by consuming tokens that would otherwise be used for task context.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Memory relevance | Independent | Relevant, Partially relevant, Irrelevant |
| Memory age | Independent | Fresh (0–7 days), Stale (30+ days) |
| Memory injection size | Independent | 512, 1024, 2048, 4096 tokens |
| Task type | Controlled | Personalization, General Q&A |

---

## Procedure

1. **Setup:** Create 5 memory entries with varying relevance and age.
2. **Test cases:**
   a. Relevant memory — ask question directly addressed by memory
   b. Irrelevant memory — ask question unrelated to any memory
   c. Stale memory — ask about topic where memory is outdated
   d. Large injection — create 4,096-token memory block, measure quality impact
3. Evaluate: (a) Was memory used correctly? (b) Did memory improve/hurt response? (c) Token overhead?

---

## Expected Result

| Condition | Expected Outcome |
|-----------|------------------|
| Relevant memory | Improves personalization |
| Irrelevant memory | Neutral (memory ignored) |
| Stale memory | Degrades quality (contradictions) |
| Large injection (4096+) | Reduces output quality |

---

## Actual Result

*Status: Not yet executed.*

---

## Decision

*Current: Memory injection cap 2,048 tokens. Short-term retention 7 days.*

---

## Benchmark Result

*Pending MEM-TC-0001, MEM-TC-0002 execution.*

---

*EXP-0005 v1.0.0 — Created 2026-07-20*
