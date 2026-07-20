# EXP-0006: RAG Pipeline — Retrieval Quality and Grounding Accuracy

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0006 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0006, REQ-AI-0010 |
| **BM** | BM-02, MEM-TC-0003 |

## Related Documents

- ↑ [REQ-AI-0006](../00_ENGINEERING/REQ-INDEX.md#req-ai-0006)
- ↑ [REQ-AI-0010](../00_ENGINEERING/REQ-INDEX.md#req-ai-0010)
- → [EXP-0005 Memory](./EXP-0005-Memory.md)
- → [EXP-0010 Agent](./EXP-0010-Agent.md)

---

## Objective

Validate that the RAG pipeline (separate embedding provider + NIM) produces accurate, grounded responses. Measure retrieval precision and the model's ability to cite and use retrieved context correctly.

---

## Hypothesis

**H1:** Hybrid search (keyword + semantic) produces higher precision retrieval than pure semantic search for technical documents.

**H2:** chunk_size=512 with chunk_overlap=50 optimally balances context completeness vs injection token cost.

**H3:** The model correctly identifies when retrieved context does not answer the question and avoids hallucination.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Embedding model | Independent | nomic-embed-text, mxbai-embed-large |
| chunk_size | Independent | 256, 512, 1024 |
| top_k retrieval | Independent | 3, 5, 10 |
| Search mode | Independent | Semantic only, Hybrid |
| Document type | Controlled | Technical doc, FAQ, narrative |

---

## Procedure

1. **Baseline:** Ingest 3 technical documents. Ask 10 questions (5 answerable, 5 not in document).
2. Measure: (a) Retrieval hit rate (answerable questions), (b) Hallucination rate (unanswerable questions), (c) Citation accuracy.
3. Vary embedding model, chunk_size, top_k and repeat.
4. Compare hybrid vs semantic search on same document set.

---

## Expected Result

| Config | Hit Rate | Hallucination Rate | Citation Accuracy |
|--------|----------|-------------------|-------------------|
| nomic, 512, k=5, hybrid | >90% | <10% | >85% |
| nomic, 256, k=3, semantic | ~75% | ~15% | ~70% |

---

## Actual Result

*Status: Not yet executed.*

---

## Conclusion

*Pending execution.*

---

## Decision

*Current: chunk_size=512, chunk_overlap=50, top_k=5, hybrid=true per capabilities.json.*

---

## Benchmark Result

*Pending BM-02 execution.*

---

*EXP-0006 v1.0.0 — Created 2026-07-20*
