# Memory Loading Strategy

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md
> **Benchmark Ref**: benchmark/tests/memory/TC-0001.md, TC-0002.md

---

## Loading Algorithm

```
SESSION_START:
  query = extract_intent(first_message)
  candidates = memory_store.semantic_search(query, top_k=10)
  ranked = priority_rank(candidates)  # see memory_priority.md
  budget = 500  # tokens
  loaded = []
  
  for item in ranked:
    if item.tokens + sum(loaded.tokens) <= budget:
      loaded.append(item)
    else:
      break
  
  inject_into_context(loaded)
  return loaded
```

---

## When to Load at Session Start

| Condition | Memory Load |
|-----------|-------------|
| First message contains name/project reference | Full load |
| First message is casual greeting | T1 + T4 only |
| First message is technical (code/system) | T1 + T2 + T4 |
| First message references past conversation | Full load |
| First message is one-word or trivial | Minimal load (T1 only) |

---

## Mid-Session Loading

Memory may be loaded mid-session if:
- User switches topic to a new project (load T3 for that project)
- User explicitly references past context ("remember when I told you...")
- User corrects a previous assumption (triggers preference update + re-load)

---

## Load Cancellation

Do NOT load memory when:
- Request is classified as benchmark/test (detected via metadata)
- User explicitly says "ignore my preferences"
- Token budget is critically low
- Request is anonymous (no user_id)

---

## Memory Load Confirmation

Do NOT announce memory loads verbally.
Example of prohibited behavior:
> ❌ "I remember you prefer Python and Indonesian. Loading your context..."

Correct behavior:
Silently apply preferences. The user will observe the effect in the response.
