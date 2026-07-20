# Tool Failover

> **Version**: 1.0.0

---

## Failure Handling

| Failure | Detected By | Action |
|---------|------------|--------|
| Tool returns error | HTTP 4xx/5xx | Retry once; then fail gracefully |
| Tool timeout (≥10s) | Timeout monitor | Abort; respond from model knowledge |
| Tool returns empty result | Empty payload check | State no result; use model knowledge |
| Tool result contradicts model knowledge | Consistency check | Present both; let user evaluate |
| RPM budget exhausted | Rate limiter | Queue or skip tool; prioritize direct response |

---

## Graceful Degradation Statement

When a tool fails and model knowledge is used:

> ⚠️ `[tool_name]` returned no result. Responding from model knowledge. Verify if accuracy is critical.

Include when:
- Tool was expected and failed
- Information is time-sensitive

Do NOT include for silent fallbacks from RAG (handled by knowledge_failover.md).
