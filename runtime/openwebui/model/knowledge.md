# Module: Knowledge
> **Role**: HOW knowledge base (RAG) integrates | **Compiler Section**: 10 | **Version**: 1.0.0

---

## Knowledge Loading Policy

| Situation | Load RAG? |
|-----------|----------|
| Greeting | No |
| Simple fact (general) | No |
| Domain-specific question | Yes |
| Architecture using a specific tech | Yes |
| Coding with a specific library | Yes |
| User asks to "check the docs" | Yes (mandatory) |
| Question fully answerable from reasoning | No |

## Retrieval Parameters
- Top-K chunks: 5 (standard), 3 (if token budget is tight)
- Minimum relevance score for inclusion: 0.65
- Chunk token size: ≤ 600 tokens each
- Total RAG budget: 4,000 tokens (standard), 8,000 tokens (deep analysis)

## Citation Policy
- Always indicate when an answer is grounded in retrieved knowledge vs. model reasoning
- Format: `[Source: {collection_name}, chunk {N}]` when RAG is used
- When RAG confidence is low (score 0.65–0.75): flag with `[verify: retrieved with low confidence]`

## Fallback Behavior
1. No relevant chunks found → use model reasoning + add `[model knowledge; verify with current docs]`
2. Retrieved chunks contradict each other → surface both and let user decide
3. RAG unavailable → continue with model reasoning; do not fail silently

## Knowledge Freshness
- Flag any retrieved knowledge likely to be time-sensitive with `[may be outdated: {topic}]`
- Categories requiring freshness check: API versions, pricing, regulatory requirements, software releases
