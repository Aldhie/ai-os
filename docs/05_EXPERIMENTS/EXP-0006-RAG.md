# EXP-0006: RAG Pipeline Quality and Token Efficiency

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0006 |
| **Title** | RAG Pipeline Quality — Chunk Size, Top-K Retrieval, and Hybrid Search |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-02 (Agentic RAG) |
| **Related REQ** | REQ-AI-0007 (RAG configuration) |
| **Cross-References** | [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) · [AI-0003-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) · [EXP-0005](EXP-0005-Memory.md) |

---

## 1. Objective

Optimize the RAG pipeline configuration for Open WebUI × Nemotron Ultra 550B. Key questions:
1. What chunk size produces best retrieval quality?
2. How many retrieved chunks (top-k) is optimal?
3. Does hybrid search (BM25 + vector) outperform pure vector search for this use case?
4. What is the token overhead of RAG context injection?

**Critical prerequisite:** Embeddings must be configured via a separate provider (NOT NIM) before this experiment can run. See EDR-0005.

---

## 2. Hypothesis

> **H1:** `chunk_size=512` with `top_k=5` (current config) is suboptimal; `chunk_size=256` with `top_k=8` will produce better recall for dense technical documents.
>
> **H2:** Hybrid search (BM25 + vector) will outperform pure vector search by ≥1 point on domain-specific terminology retrieval.
>
> **H3:** RAG context of 5 chunks consumes ~1500–2500 tokens, well within budget. Context overflow becomes risk at 20+ chunks.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | `chunk_size` | 128, 256, 512, 1024 tokens |
| **Independent** | `top_k` (retrieved chunks) | 3, 5, 8, 12 |
| **Independent** | Search type | Vector only, BM25 only, Hybrid |
| **Dependent** | Retrieval recall@k | RAGAS metric |
| **Dependent** | Answer faithfulness | RAGAS metric |
| **Dependent** | Tokens per RAG context | Counted |
| **Controlled** | Embedding model | nomic-embed-text (fixed) |
| **Controlled** | Test documents | 3 fixed technical docs |
| **Controlled** | Test questions | 10 fixed questions |

---

## 4. Prerequisite

- [ ] Configure `nomic-embed-text` (or equivalent) as embedding provider in Open WebUI
- [ ] Verify embeddings endpoint working (EDR-0005 implemented)
- [ ] ChromaDB instance running and accessible

---

## 5. Procedure

1. Ingest 3 technical documents with each chunk_size variant
2. Run 10 test questions per configuration
3. Evaluate using RAGAS (recall, precision, faithfulness, context relevance)
4. Count tokens in injected RAG context per configuration
5. Identify optimal chunk_size + top_k combination
6. Compare hybrid vs. vector search on same questions

---

## 6. Expected Result

| Config | Recall@k | Faithfulness | Tokens |
|--------|---------|--------------|--------|
| 512 / top5 / vector | 0.65 | 0.80 | ~1800 |
| 256 / top8 / hybrid | 0.80 | 0.85 | ~2400 |
| 1024 / top3 / vector | 0.55 | 0.75 | ~3200 |

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING** — Blocked on embedding provider configuration (EDR-0005).

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
