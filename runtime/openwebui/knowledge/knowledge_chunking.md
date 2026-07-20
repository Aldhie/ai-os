# Knowledge Chunking

> **Version**: 1.0.0
> **Spec Ref**: AI-0001-Part2 §5, AI-0005-FreeTier-Strategy.md

---

## Chunking Parameters

| Parameter | Value | Rationale |
|-----------|-------|----------|
| Max chunk size | 512 tokens | Semantic coherence + token efficiency |
| Chunk overlap | 50 tokens | Preserve cross-chunk context |
| Max chunks per query | 5 | Budget-aware; see profile configs |
| Min semantic similarity | 0.75 | Filter low-relevance chunks |
| Max total injection | 4,000 tokens | Hard cap (architecture profile) |

---

## Chunking Strategy

### Document-Type Rules

| Document Type | Chunk Strategy |
|---------------|---------------|
| Markdown specs | Split by heading (##/###) |
| Code files | Split by function/class boundaries |
| JSON/YAML configs | Keep as single unit if < 512 tokens |
| Long prose | Semantic paragraph chunking |
| API reference | Split by endpoint |

---

## Context Window Allocation

```
Total context window: 128,000 tokens
├── System prompt:        800 tokens
├── Memory:              500 tokens  
├── Knowledge chunks:  4,000 tokens  (max, architecture profile)
├── Conversation history: dynamic
├── User message:     variable
└── Response space:   ≥20,000 tokens (reserved)

Safe operating range: 60,000–100,000 tokens of conversation history.
```

---

## Deduplication

Before injection:
- Remove chunks with >90% token overlap with each other
- Remove chunks already present in conversation history
- Remove chunks below minimum similarity threshold (0.75)
