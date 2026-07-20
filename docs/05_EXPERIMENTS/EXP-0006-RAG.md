# EXP-0006: RAG Pipeline Quality and Configuration

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0006 |
| **Title** | RAG Pipeline Quality and Configuration |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — RAG |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | RAG compatibility matrix |
| [AI-0003-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) | Confirmed: no embeddings on Cloud NIM |
| [benchmark/rag/](../../benchmark/tests/rag/) | RAG benchmark TCs |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0013 |

---

## 1. Objective

Determine optimal RAG configuration for Open WebUI + Nemotron Ultra 550B: chunk size, retrieval top-k, embedding model selection, and hybrid search vs pure vector search quality.

Critical pre-requisite: identify and validate a working embedding provider (Cloud NIM does not provide embeddings). [FACT: Official Doc — confirmed in AI-0003-Audit]

---

## 2. Background

RAG in Open WebUI is entirely client-side. NIM only receives the augmented prompt. [FACT: OW docs]

Embedding provider options (since Cloud NIM has no `/v1/embeddings`):
- `nomic-embed-text` via Ollama [HYPOTHESIS: available, good quality/cost ratio]
- `mxbai-embed-large` via Ollama [HYPOTHESIS: higher quality but larger]
- `nvidia/nv-embedqa-e5-v5` via NVIDIA Cloud NIM (separate model) [HYPOTHESIS: best NVIDIA-native integration]

---

## 3. Hypothesis

**H1:** `chunk_size=512, chunk_overlap=50, top_k=5` is optimal for standard document Q&A. [HYPOTHESIS]

**H2:** Hybrid search (BM25 + vector) outperforms pure vector search by >15% on domain-specific terminology queries. [HYPOTHESIS]

**H3:** `nomic-embed-text` provides sufficient quality for standard RAG while avoiding Cloud API dependency. [HYPOTHESIS]

---

## 4. Variables

| Variable | Test Values |
|----------|------------|
| chunk_size | 256, 512, 1024, 2048 |
| chunk_overlap | 0, 50, 100 |
| retrieval top_k | 3, 5, 10 |
| search mode | vector-only, BM25-only, hybrid |
| embedding model | nomic-embed-text, mxbai-embed-large, nv-embedqa-e5-v5 |

---

## 5. Evaluation Dataset

Use domain-specific documents from `dataset/` folder.
Create 20 ground-truth Q&A pairs.
Metric: Recall@K (does correct answer appear in retrieved chunks).

---

## 6. Actual Results

> **Status: PENDING EXECUTION**

---

## 7. Conclusion

> **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
