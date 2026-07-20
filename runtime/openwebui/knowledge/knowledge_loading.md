# Knowledge Loading

> **Version**: 1.0.0
> **Module**: Knowledge Orchestration
> **Spec Ref**: AI-0001-Part2 §5 (RAG Design), AI-0005-FreeTier-Strategy.md
> **Benchmark Ref**: benchmark/tests/rag/

---

## When RAG Is Used

Retrieval-Augmented Generation (RAG) activates when:
- User references a document, file, or knowledge base by name
- Query contains technical terminology specific to a loaded knowledge base
- Profile config has `rag_enabled: true` AND query matches knowledge scope
- User asks "based on [document]" or equivalent
- Confidence in model knowledge is low for a specialized domain

## When RAG Is Skipped

RAG is explicitly skipped when:
- Query is conversational or general knowledge
- Query matches T1-T4 memory (personal preferences, identity)
- No relevant knowledge base exists for the domain
- Profile config has `rag_enabled: false`
- Token budget for knowledge injection is exhausted
- Previous retrieval returned empty results for similar query

---

## Loading Sequence

```
1. Detect retrieval intent from query
2. Select candidate knowledge bases (by profile + domain match)
3. Generate retrieval query (may differ from user query)
4. Retrieve top-N chunks (see knowledge_chunking.md for N)
5. Rank chunks (see knowledge_ranking.md)
6. Check token budget: discard lowest-ranked chunks if over budget
7. Inject ranked chunks into context BEFORE user message
8. Track which sources were used (for citation)
```

---

## Knowledge Source Types

| Type | Access Pattern | Use Case |
|------|---------------|----------|
| Engineering Specs | Always available | Technical Q&A about this project |
| Project Docs | Session-scoped | Code, architecture questions |
| Research Papers | On-demand | Academic or deep technical synthesis |
| API References | On-demand | Integration and coding support |
| Custom Uploads | Per-session | User-provided documents |

---

## Token Budget for Knowledge

| Profile | Max Knowledge Tokens |
|---------|---------------------|
| discussion | 0 (RAG disabled) |
| coding | 2,000 |
| architecture | 4,000 |
| creative | 0 (RAG disabled) |
| analysis | 3,000 |
