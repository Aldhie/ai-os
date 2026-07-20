# EXP-0006: Retrieval-Augmented Generation Optimization

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0006 |
| **Title** | RAG Pipeline Optimization — Chunk Size, Top-K, Embedding, Hybrid Search |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0003 §3 Knowledge & RAG Matrix](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [AI-0003-Critical-Findings-Audit R-04](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md)
- [benchmark/tests/rag/TC-0001.md](../../benchmark/tests/rag/TC-0001.md)
- [EXP-0005 Memory](EXP-0005-Memory.md)

---

## 1. Objective

Optimize the Open WebUI RAG pipeline for Nemotron Ultra 550B: determine optimal chunk size, top-k retrieval count, embedding model, and hybrid search configuration.

---

## 2. Background

**[FACT]** Cloud NIM does not provide `/v1/embeddings` endpoint for Nemotron Ultra 550B. A separate embedding provider is required. (AI-0003-Critical-Findings-Audit R-04)

**[FACT]** Open WebUI supports ChromaDB (default), PGVector, and Qdrant as vector stores.

**[FACT]** Open WebUI supports hybrid search (BM25 + vector) with configurable reranking.

**[ASSUMPTION]** `chunk_size: 512` is a reasonable default, but domain-specific documents may benefit from larger chunks (1024) to preserve context.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | `chunk_size: 512` outperforms `1024` on short-answer factual queries |
| H2 | `chunk_size: 1024` outperforms `512` on questions requiring multi-sentence context |
| H3 | Hybrid search (BM25 + vector) outperforms vector-only by > 0.5 score on domain-specific queries |
| H4 | `top_k: 5` is sufficient; `top_k: 10` does not improve quality and increases token cost |

---

## 4. Variables

**Independent:** chunk_size `[256, 512, 1024]`, top_k `[3, 5, 10]`, search mode `[vector, hybrid]`
**Controlled:** embedding model (nomic-embed-text via Ollama), Nemotron Ultra 550B, thinking OFF
**Dependent:** Answer accuracy, hallucination rate, prompt_tokens

---

## 5. Procedure

1. Prepare test document set (5 technical docs, total ~50 pages)
2. For each chunk_size × top_k × search_mode combination (18 combinations):
   - Index documents
   - Run TC-rag-0001, TC-rag-0002, TC-rag-0003 × 3 reps
   - Record accuracy score, hallucination instances, prompt_tokens
3. Identify best combination via F1 score (accuracy vs token cost)

---

## 6. Expected Results

| Config | Expected Accuracy | Token Cost |
|--------|------------------|------------|
| chunk=512, k=5, hybrid | 4.2/5 | medium |
| chunk=1024, k=5, hybrid | 4.0/5 | high |
| chunk=512, k=10, hybrid | 4.0/5 | high |
| chunk=256, k=5, vector | 3.5/5 | low |

---

## 7–13. Actual Result through Benchmark Results

> ⏳ **PENDING** — Requires separate embedding provider setup first.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
