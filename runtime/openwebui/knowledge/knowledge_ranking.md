# Knowledge Ranking

> **Version**: 1.0.0
> **Benchmark Ref**: benchmark/tests/rag/TC-0001.md, TC-0002.md

---

## Ranking Formula

```
score(chunk) = (
    0.50 * semantic_similarity(chunk, query)
  + 0.20 * recency_score(chunk.source_date)
  + 0.20 * source_authority(chunk.source_type)
  + 0.10 * token_efficiency(chunk)
)
```

## Target Metrics

| Metric | Target | Source |
|--------|--------|--------|
| RAGAS Context Recall | ≥80% | benchmark/tests/rag/ |
| RAGAS Context Precision | ≥75% | benchmark/tests/rag/ |
| RAGAS Answer Relevance | ≥85% | benchmark/tests/rag/ |
| RAGAS Faithfulness | ≥80% | benchmark/tests/rag/ |

---

## Ranking Failure Modes

| Failure | Detection | Response |
|---------|-----------|----------|
| No chunks above 0.75 similarity | No injection | Use model knowledge only; state this |
| All chunks below 0.5 similarity | Empty retrieval | Explicitly tell user no relevant docs found |
| Source contradiction detected | Flag in response | Present both sources; let user decide |
| Chunk is outdated (>1 year old) | Recency score low | Use but flag as potentially outdated |
