# EXP-0005: Long-Term Memory Effectiveness

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0005 |
| **Title** | Long-Term Memory Recall Accuracy and Context Impact |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0003 §6 Memory Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [benchmark/tests/memory/TC-0001.md](../../benchmark/tests/memory/TC-0001.md)
- [EXP-0006 RAG](EXP-0006-RAG.md)

---

## 1. Objective

Measure Open WebUI long-term memory recall precision, false positive injection rate, and token cost per conversation. Determine optimal memory injection strategy for Nemotron Ultra 550B.

---

## 2. Background

**[FACT]** Open WebUI memory injection works client-side: relevant memories are retrieved from vector DB and prepended to the conversation context before the NIM API call. NIM sees memories as plain text context.

**[HYPOTHESIS]** Memory injection from unrelated topics reduces response quality by introducing noise into the context.

**[HYPOTHESIS]** `auto_recall: true` with a large memory store increases average prompt_tokens by 200–500 tokens per message.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | Memory recall precision > 80% for facts explicitly saved in current session |
| H2 | Memory injection from >7-day-old entries increases off-topic responses |
| H3 | Memory injection adds avg 150–400 tokens to prompt_tokens |
| H4 | With `auto_recall: true`, user preference memories improve satisfaction score by 0.5 points |

---

## 4. Procedure

1. **Setup:** Seed memory store with 20 facts (10 relevant, 10 unrelated)
2. **Phase 1:** Ask 10 questions referencing seeded relevant facts. Measure recall accuracy.
3. **Phase 2:** Ask 5 questions unrelated to any memory. Count false memory injections.
4. **Phase 3:** Measure prompt_tokens with memory ON vs OFF for 20 standard queries.
5. **Phase 4:** Evaluate response quality (blind scoring) with and without memory injection.

---

## 5. Expected Results

| Metric | Expected Value |
|--------|---------------|
| Recall precision | > 80% |
| False injection rate | < 15% |
| Token overhead | 150–400 tokens |
| Quality delta | +0.3–0.5 score |

---

## 6–13. Actual Result through Benchmark Results

> ⏳ **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
