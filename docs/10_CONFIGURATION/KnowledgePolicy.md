# Knowledge Policy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | KnowledgePolicy.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the knowledge policy for the AI OS. It governs how external knowledge is ingested, indexed, retrieved, and cited in AI responses.

---

## Scope

- Knowledge base architecture (RAG)
- Supported document types
- Ingestion pipeline
- Retrieval configuration
- Citation policy

---

## Dependencies

- `docs/10_CONFIGURATION/SystemPrompt.md` — RAG instructions in prompt
- Open WebUI Knowledge / RAG module
- `docs/30_DATASET/README.md` — dataset sources

---

## References

- [Open WebUI RAG Documentation](https://docs.openwebui.com/features/rag/)
- [RAG Best Practices](https://arxiv.org/abs/2312.10997)

---

## Knowledge Architecture

```
Documents → Ingestion Pipeline → Vector Store → Retrieval → Context Injection
```

### Supported Document Types

| Format | Support | Notes |
|--------|---------|-------|
| PDF | ✅ | Via Open WebUI |
| Markdown (.md) | ✅ | Native |
| Plain Text (.txt) | ✅ | Native |
| DOCX | ✅ | Via Open WebUI |
| HTML | ✅ | Via Open WebUI |
| CSV | ⚠️ | Limited |
| JSONL | ❌ | Not supported natively |

---

## Retrieval Configuration

| Parameter | Value | Notes |
|-----------|-------|-------|
| Chunk size | 512 tokens | Adjust based on testing |
| Chunk overlap | 50 tokens | Ensure context continuity |
| Top-K retrieval | 5 chunks | Retrieve top 5 relevant chunks |
| Similarity threshold | 0.75 | Minimum cosine similarity |

---

## Citation Policy

- The assistant MUST cite sources when using retrieved knowledge
- Citations must include document name and section
- Conflicting knowledge sources must be flagged to the user
- Outdated knowledge must be noted with a date caveat

---

## TODO

- [ ] Define knowledge base structure and naming conventions
- [ ] Document ingestion pipeline setup in Open WebUI
- [ ] Test retrieval quality with benchmark queries
- [ ] Define knowledge update and version control process
- [ ] Set up automatic re-indexing schedule
