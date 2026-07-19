# Knowledge Policy

| Field | Value |
|-------|-------|
| **Title** | Knowledge Policy |
| **Purpose** | Define how the AI OS handles knowledge retrieval, RAG, and knowledge boundaries |
| **Scope** | RAG configuration, knowledge sources, freshness policy, citation requirements |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | SystemPrompt.md, ToolPolicy.md |
| **References** | AI-0003 (Open WebUI Compatibility) |

---

## 1. Knowledge Hierarchy

```
Priority 1: User-provided documents (RAG)
Priority 2: Memory (long-term learned facts)
Priority 3: Web search (via tool)
Priority 4: Model parametric knowledge (cutoff date)
```

---

## 2. RAG Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| Chunk size | 1000 tokens | Balance between context and precision |
| Overlap | 200 tokens | Maintains coherence across chunks |
| Top-K retrieval | 5 | Number of chunks per query |
| Similarity threshold | 0.7 | Minimum relevance score |

---

## 3. Knowledge Freshness Policy

| Source | Freshness | Action |
|--------|-----------|--------|
| User documents | User-defined | Notify user if document > 1 year old |
| Web search | Real-time | Use for time-sensitive queries |
| Model knowledge | Training cutoff | Acknowledge when uncertain |

---

## 4. Citation Policy

- Always cite the source when using RAG-retrieved information
- Distinguish between model knowledge and retrieved knowledge
- Use web search tool when user asks about recent events

---

## 5. Knowledge Boundaries

The AI OS should explicitly acknowledge when:

- Information may be outdated (post training-cutoff)
- Information is uncertain or contested
- User should consult a domain expert (medical, legal, financial)

---

## TODO

- [ ] Configure RAG chunking in Open WebUI
- [ ] Test RAG retrieval accuracy with sample documents
- [ ] Define knowledge base document structure
- [ ] Implement freshness checks
- [ ] Create citation format standard
