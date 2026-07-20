# Context Loading Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Loading Phases

### Phase 1: Request Classification (< 50ms)

Classify the incoming request before loading any context:

```python
def classify_request(message: str) -> RequestClass:
    """
    Classification order (first match wins):
    - greeting: len < 20 and no "?" and no technical terms
    - simple_fact: single direct question, answerable in < 3 sentences
    - memory_recall: references user's past preferences or history
    - domain_knowledge: requires external knowledge base
    - complex_task: multi-step, architecture, analysis
    - continuation: explicitly references prior context
    """
```

### Phase 2: Selective Loading (based on classification)

```yaml
greeting:
  load: [system_prompt]
  skip: [history, memory, rag, planner, reflection, critic]

simple_fact:
  load: [system_prompt, message]
  skip: [history, memory, rag, planner, reflection, critic]

memory_recall:
  load: [system_prompt, history_recent_3, memory_top_3]
  skip: [rag, planner, reflection, critic]

domain_knowledge:
  load: [system_prompt, history_recent_3, memory_top_3, rag_top_5]
  skip: [planner, critic]
  optional: [reflection]

complex_task:
  load: [system_prompt, history_recent_5, memory_top_5, rag_top_5, planner, reflection]
  optional: [critic]

continuation:
  load: [system_prompt, history_recent_5, memory_top_3]
  optional: [rag, reflection]
```

### Phase 3: Compression (if over budget)

See `compression_strategy.md`.

---

*File: runtime/openwebui/context/loading_strategy.md | Last updated: 2026-07-20*
