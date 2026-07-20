# Parallelism Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## What Can Be Parallelized

```yaml
parallel_safe:
  - memory_retrieval + rag_retrieval    # both are read-only, independent
  - tool_execution (multiple tools)     # when results are independent
  - context_assembly components         # each source is independent

not_parallel_safe:
  - planner → execution                # planner must complete first
  - execution → reflection             # reflection needs result
  - reflection → critic                # critic needs reflection
  - any NIM call → next NIM call      # RPM limit; must sequence
```

---

## Parallel Context Loading

```python
import asyncio

async def load_context(query: str, user_id: str) -> Context:
    # Parallel: memory and RAG retrieval
    memory_task = asyncio.create_task(retrieve_memory(user_id, query))
    rag_task = asyncio.create_task(retrieve_rag(query))
    
    memory, rag = await asyncio.gather(memory_task, rag_task)
    
    return assemble_context(memory, rag)

# Saves: max(memory_time, rag_time) instead of sum
# Typical saving: 0.5s per request
```

---

## NIM Calls Must Be Sequential

```
DO NOT fire multiple NIM API calls simultaneously.
Reason: Each call counts toward RPM limit independently.
Approach: Queue and sequence; use parallelism only for non-NIM work.
```

---

*File: runtime/openwebui/performance/parallelism.md | Last updated: 2026-07-20*
