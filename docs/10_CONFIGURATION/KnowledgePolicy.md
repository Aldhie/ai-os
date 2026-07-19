# Knowledge Policy

| Field | Value |
|---|---|
| **Title** | AI-OS Knowledge & RAG Policy |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines how AI-OS retrieves, uses, and cites external knowledge via Retrieval-Augmented Generation (RAG). Covers knowledge base organization, retrieval configuration, source trust levels, and citation policy.

---

## Scope

- Open WebUI Knowledge (RAG) feature
- Document ingestion, chunking, retrieval
- All user queries that may benefit from external knowledge

---

## Knowledge Base Organization

| Collection | Content | Update Frequency |
|---|---|---|
| `ai-os-docs` | This repository's own documentation | On every commit |
| `nvidia-nim-docs` | NVIDIA NIM API documentation | Monthly |
| `openwebui-docs` | Open WebUI documentation | Monthly |
| `research-papers` | Relevant AI research papers | As needed |
| `user-documents` | User-uploaded documents | Real-time |

---

## Retrieval Configuration

```json
{
  "top_k": 3,
  "similarity_threshold": 0.75,
  "chunk_size": 512,
  "chunk_overlap": 64,
  "embedding_model": "nvidia/nv-embedqa-e5-v5",
  "reranker": "nvidia/llama-3.2-nv-rerankqa-1b-v2"
}
```

---

## Trust Levels

| Source | Trust Level | Citation Required |
|---|---|---|
| NVIDIA official docs | High | Yes |
| Open WebUI official docs | High | Yes |
| AI-OS repo docs | High | No (internal) |
| Research papers (arXiv) | Medium | Yes |
| Blog posts / web | Low | Yes + verify |
| User-provided docs | Medium | Yes |

---

## Retrieval Rules

1. **Always retrieve** when the query involves technical specifications or external facts.
2. **Never fabricate** citations — only cite what was retrieved.
3. **Prefer recency** — more recent documents should be ranked higher for versioned topics.
4. **Token budget:** Max 4,000 tokens of retrieved context per query.
5. **Cite sources:** Always tell the user which document was used.

---

## Dependencies

- `docs/10_CONFIGURATION/SystemPrompt.md`
- Open WebUI RAG module
- `dataset/` for curated knowledge

---

## References

- [Open WebUI RAG Docs](https://docs.openwebui.com/features/workspace/knowledge)
- [NVIDIA NV-Embed Models](https://build.nvidia.com/)

---

## TODO

- [ ] Set up `ai-os-docs` knowledge collection in Open WebUI
- [ ] Configure NVIDIA embedding model
- [ ] Test retrieval quality on AI-OS documentation
- [ ] Define document ingestion pipeline
- [ ] Set up automatic re-indexing on repo commit
