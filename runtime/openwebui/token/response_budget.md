# Response Budget Rules

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Response Length Calibration

Response length must match task complexity. Neither over-answering nor under-answering is acceptable.

### Calibration Table

| Task | Target Length | Max Length | Format |
|------|--------------|------------|--------|
| Greeting | 1-2 sentences | 50 tokens | Prose |
| Simple fact | 1-3 sentences | 150 tokens | Prose |
| How-to (simple) | 3-8 steps | 300 tokens | Numbered |
| Explanation (concept) | 2-4 paragraphs | 600 tokens | Prose + bullets |
| Business analysis | structured | 1000 tokens | Headers + table |
| Architecture design | full spec | 2000 tokens | Full structured |
| Code generation | complete | 2000 tokens | Code + minimal prose |
| Document generation | full | 4096 tokens | Full document |

---

## Length Enforcement

```python
max_tokens_for_task = TASK_TOKEN_BUDGET[task_class]
# Set in NIM API call as: max_tokens=max_tokens_for_task
# Never use max_tokens=4096 by default
# Always set to minimum sufficient for the task class
```

---

## Quality Over Length Test

Before finalizing output, self-check:
```
1. Does this answer the question completely? (must be YES)
2. Is every paragraph necessary? (remove if NO)
3. Does the length match the task complexity? (must be PROPORTIONATE)
4. Is there any padding, filler, or repetition? (must be NONE)
```

---

*File: runtime/openwebui/token/response_budget.md | Last updated: 2026-07-20*
