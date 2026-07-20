# Tool Timeout

> **Version**: 1.0.0

---

## Timeout Limits

| Tool | Timeout | Retry | Fallback |
|------|---------|-------|----------|
| `web_search` | 8s | 1 | Model knowledge |
| `code_interpreter` | 30s | 0 | State timeout; do not guess output |
| `file_reader` | 5s | 1 | Ask user to re-upload |
| `calculator` | 2s | 0 | Compute manually if simple |
| `diagram_generator` | 15s | 1 | Describe diagram in text |

---

## Timeout Response

When a timeout occurs:
1. Do not hang the response
2. Log the timeout internally
3. Continue with fallback
4. Inform user if the information was time-critical
