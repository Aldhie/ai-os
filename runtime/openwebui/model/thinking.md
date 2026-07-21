# Module: Thinking
> **Role**: HOW extended thinking tokens are used | **Compiler Section**: 14 | **Version**: 1.0.0

---

## Thinking Token Policy

Thinking tokens are a premium resource on NVIDIA NIM free tier. They are invisible to the user but consume quota and add latency.

**Use thinking tokens to reason before generating.** Do not use them to produce verbose internal monologue.

## Thinking Budget by Task

```yaml
greeting:          budget: 0,     type: disabled
simple_fact:       budget: 0,     type: disabled
casual_chat:       budget: 1000,  type: enabled
explanation:       budget: 3000,  type: enabled
business_analysis: budget: 8000,  type: enabled
architecture:      budget: 14000, type: enabled
coding:            budget: 8000,  type: enabled
debugging:         budget: 10000, type: enabled
security:          budget: 14000, type: enabled
research:          budget: 10000, type: enabled
planning:          budget: 8000,  type: enabled
mathematical:      budget: 20000, type: enabled
```

## API Configuration

```json
{
  "extra_body": {
    "thinking": {
      "type": "enabled",
      "budget_tokens": 8000
    }
  }
}
```

For disabled:
```json
{
  "extra_body": {
    "thinking": {
      "type": "disabled"
    }
  }
}
```

## Thinking Quality Rules

- Use thinking to explore failure modes before recommending
- Use thinking to verify code logic before writing the final version
- Use thinking to check reasoning chains for circular logic
- Do not use thinking to rehearse pleasantries or structuring text
