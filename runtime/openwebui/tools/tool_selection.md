# Tool Selection

> **Version**: 1.0.0
> **Spec Ref**: AI-0001-Part2 §6

---

## Selection Algorithm

```
For each candidate tool T:
  score(T) = (
    relevance(T, query)           # 0-100: how well tool addresses the need
    - rpm_cost(T) * 10            # penalty for expensive tools
    - latency_penalty(T)          # penalty for slow tools
    + cache_bonus(T)              # bonus if result likely cached
  )

select tool with highest score where score > 50
if no tool scores > 50: answer from model knowledge
```

---

## Selection by Profile

| Profile | Allowed Tools | Auto-Invoke |
|---------|--------------|-------------|
| discussion | web_search, calculator | No |
| coding | code_interpreter, file_reader | No |
| architecture | all | Yes (high confidence tasks) |
| creative | web_search | No |
| analysis | web_search, calculator, file_reader | No |
