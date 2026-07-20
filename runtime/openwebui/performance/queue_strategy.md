# Queue Strategy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## When Queuing is Needed

Queuing is needed when:
- RPM approaches 35+ (near free tier limit)
- Batch processing > 5 documents
- Multiple pipeline steps each requiring a NIM call
- Non-interactive background tasks

---

## Queue Policy

```yaml
queue_policy:

  interactive_priority: HIGH      # user is waiting
  batch_priority: LOW             # background; user not waiting
  background_priority: LOWEST     # scheduled tasks

  max_queue_depth: 20
  max_wait_interactive: 30s       # fail fast if user waiting too long
  max_wait_batch: 10min           # batch can wait

  inter_request_delay:
    default: 0s                   # no delay for normal conversation
    batch: 2.5s                   # throttle batch to stay within RPM
    background: 5s                # aggressive throttle for background
```

---

## Batch Processing Pattern

```python
# For document batch analysis (5+ documents):
import asyncio

async def batch_analyze(docs: list, delay_between: float = 2.5):
    results = []
    for i, doc in enumerate(docs):
        result = await analyze_document(doc)
        results.append(result)
        if i < len(docs) - 1:
            await asyncio.sleep(delay_between)  # RPM protection
    return results

# At 2.5s delay: 24 docs/min = 24 RPM (safe under 40 RPM limit)
```

---

*File: runtime/openwebui/performance/queue_strategy.md | Last updated: 2026-07-20*
