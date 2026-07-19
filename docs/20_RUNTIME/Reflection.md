# Reflection

| Field | Value |
|-------|-------|
| **Title** | Runtime Reflection |
| **Purpose** | Define the self-reflection mechanism for improving AI OS response quality |
| **Scope** | When to reflect, reflection format, integration with output pipeline |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | Critic.md, Planner.md |
| **References** | Reflexion (Shinn et al. 2023), Self-Refine (Madaan et al. 2023) |

---

## 1. Reflection Types

| Type | Trigger | Purpose |
|------|---------|----------|
| **Pre-response** | Before generating answer | Check: do I have enough info? |
| **Post-response** | After generating draft | Check: is this accurate and complete? |
| **Post-task** | After completing multi-step task | Check: did I achieve the goal? |
| **Failure** | After error or tool failure | Check: what went wrong? |

---

## 2. Reflection Prompt Template

```
Review the following response:
[RESPONSE]

Evaluate:
1. Does it fully answer the user's question?
2. Is every claim accurate?
3. Is the format appropriate?
4. Are there unnecessary words to remove?
5. Is there missing context that should be added?

If any answer is NO, rewrite the response.
```

---

## 3. Reflection Depth

| Query Complexity | Reflection Level |
|-----------------|------------------|
| Simple factual | Skip |
| Mu