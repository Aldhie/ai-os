# Knowledge Priority

> **Version**: 1.0.0
> **Spec Ref**: AI-0001-Part2 §5

---

## Priority Framework

When multiple knowledge sources are available, they are ranked by:

| Priority | Source Type | Rationale |
|----------|------------|----------|
| 1 | Engineering specs (this repo) | Authoritative for this AI-OS project |
| 2 | User-uploaded documents | Most specific to current task |
| 3 | Project docs | Project-specific, high relevance |
| 4 | API references | High precision, low noise |
| 5 | Research papers | Broad but validated |
| 6 | General web knowledge | Lowest priority, highest noise |

---

## Chunk-Level Priority

Within a source, individual chunks are ranked by:
1. Semantic similarity to retrieval query (weight: 0.5)
2. Recency of the source document (weight: 0.2)
3. Source authority tier (weight: 0.2)
4. Token efficiency (fewer tokens for same info = higher rank) (weight: 0.1)

---

## Override Rules

- User explicitly cites a source → that source gets priority 1 override
- Source is in project's canonical spec set → treated as ground truth
- Source contradicts a higher-priority source → flag contradiction, do not average
