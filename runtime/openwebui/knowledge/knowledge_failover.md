# Knowledge Failover

> **Version**: 1.0.0

---

## Failure Scenarios

| Scenario | Detected By | Failover Action |
|----------|------------|------------------|
| RAG returns 0 results | Empty chunk list | Fall back to model parametric knowledge |
| Retrieval latency > 3s | Timeout check | Proceed without RAG; note in response |
| Source document unavailable | 404/missing file | Skip that source; continue with others |
| Chunk quality too low (all < 0.75) | Ranking check | Fall back to model knowledge |
| Token budget exhausted before injection | Token count check | Inject top 1 chunk only; skip rest |

---

## Fallback Statement

When RAG fails and model knowledge is used instead:

> "No relevant documents were retrieved for this query. Responding from model knowledge only. Verify critical claims independently."

This statement is included in the response when:
- RAG was expected (profile has rag_enabled: true)
- Query was retrieval-intent (user referenced a document)
- Retrieval returned no usable results

Do NOT include this statement when RAG was not expected (disabled by profile).
