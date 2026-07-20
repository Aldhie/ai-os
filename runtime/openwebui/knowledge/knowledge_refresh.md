# Knowledge Refresh

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md

---

## Refresh Triggers

| Trigger | Action |
|---------|---------|
| Source file modified (file watcher) | Re-chunk and re-embed modified document |
| User uploads new version of document | Replace old chunks, re-rank |
| Retrieval precision drops below 70% | Flag for manual review |
| Model detects "outdated" in retrieval | Prompt user to refresh source |

---

## Refresh Frequency by Source

| Source | Refresh Interval |
|--------|------------------|
| Engineering specs (this repo) | On push to main (CI trigger) |
| User project docs | On user upload |
| API references | Monthly |
| Research papers | On user request |

---

## Free Tier Constraint

Embedding generation is NOT counted against NIM inference RPM.
However, re-embedding large documents at high frequency may:
- Slow down session initialization
- Increase latency for first RAG query

Recommendation: Batch re-embedding during off-peak hours.
Never trigger re-embedding during active user session.
