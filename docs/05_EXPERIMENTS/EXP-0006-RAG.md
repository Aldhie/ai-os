# EXP-0006: RAG Pipeline Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0006 |
| **Title** | RAG Pipeline: Retrieval Quality, Chunk Strategy, and Embedding Provider |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | Critical |

---

## Cross References

- [AI-0003 — Compatibility Matrix, Section 3](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [AI-0003-Audit — R-04 (Embeddings)](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md)
- [TC-RAG-0001 — RAG Retrieval Accuracy](../../benchmark/tests/rag/TC-RAG-0001.md)

---

## 1. Objective

Validate the RAG pipeline for Nemotron Ultra 550B: (1) which embedding provider is most accurate, (2) optimal chunk size and overlap, (3) hybrid vs vector-only search quality.

---

## 2. Hypothesis

> `[HYPOTHESIS]` Since Cloud NIM does not expose `/v1/embeddings` (AI-0003-Audit R-04), a separate embedding provider is mandatory. We hypothesize that `nomic-embed-text` via Ollama provides 85%+ retrieval recall for domain-specific hospitality documents with chunk_size=512, overlap=64.

---

## 3. Variables

### Independent Variables

| Variable | Test Values |
|----------|-------------|
| Embedding provider | `nomic-embed-text`, `mxbai-embed-large`, `text-embedding-3-small` |
| Chunk size | `256`, `512`, `1024`, `2048` tokens |
| Search mode | Vector-only, BM25-only, Hybrid |
| Top-K retrieved chunks | `3`, `5`, `10` |

---

## 4. Test Documents

Use Ezy Stay hospitality domain documents:
- Hotel SOP manual
- Room service menu
- Guest complaint handling policy
- Loyalty program terms

---

## 5. Expected Result

- `nomic-embed-text` + chunk_size=512 + hybrid search + top_k=5 is the optimal combination
- Retrieval recall >80% on domain-specific queries
- Hybrid search outperforms vector-only by >10%

---

## 6. Actual Result

> `[PENDING]`

---

## 7. Decision

> `[PENDING]` Update `capabilities.json` RAG section with validated configuration.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — R-04 embedding gap |
