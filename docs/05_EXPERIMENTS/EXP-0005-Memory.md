# EXP-0005: Long-Term Memory Behavior and Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0005 |
| **Title** | Long-Term Memory Behavior and Quality |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Memory |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | Memory compatibility matrix |
| [benchmark/memory/](../../benchmark/tests/memory/) | Memory benchmark TCs |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0012 |

---

## 1. Objective

Validate Open WebUI long-term memory behavior with Nemotron Ultra 550B: accuracy of memory recall, token overhead from memory injection, and quality degradation over time as memory set grows.

---

## 2. Background

Open WebUI memory is entirely client-side: stored facts are retrieved and injected as context before each NIM call. [FACT: Official Doc — OW memory docs]

Key unknown: what is the quality of semantic retrieval? How many injected memory facts are irrelevant (noise)? How does memory injection interact with the model's own context window management? [ASSUMPTION]

---

## 3. Hypothesis

**H1:** Memory recall accuracy (correct facts retrieved / total relevant facts) exceeds 90% for a memory set of ≤ 50 entries. [HYPOTHESIS]

**H2:** Memory injection of >10 facts per query causes >500 token overhead, noticeably reducing response quality on token-budget-sensitive tasks. [HYPOTHESIS]

**H3:** Memory entries older than 30 days are retrieved with lower relevance scores (due to semantic drift), producing lower-quality injections. [HYPOTHESIS]

---

## 4. Test Scenarios

### Scenario A: Basic Recall
1. Add 10 known facts to memory
2. Ask questions that require those specific facts
3. Measure: correct facts retrieved / questions asked

### Scenario B: Noise Measurement
1. Add 50 mixed facts (10 relevant, 40 irrelevant to test query)
2. Run query
3. Count: how many irrelevant facts were injected

### Scenario C: Scale Test
1. Memory set sizes: 10, 50, 100, 500 entries
2. Measure recall accuracy and injection latency at each scale

### Scenario D: Temporal Decay
1. Add facts; wait 7 days
2. Re-query; compare retrieval quality to day-0 baseline

---

## 5. Environment

| Component | Value |
|-----------|-------|
| Memory backend | Open WebUI default |
| Embedding model | [to be determined based on available provider] |
| Memory retention policy | 7-day short-term, unlimited long-term |
| Model | nvidia/nemotron-3-ultra-550b-a55b |

---

## 6. Actual Results

> **Status: PENDING EXECUTION**

---

## 7. Conclusion

> **PENDING**

---

## 8. Decision

> **PENDING** — Will determine optimal memory set size limits and retention policy.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
