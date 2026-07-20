# Task Classification and Reasoning Selector

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Task Classification Matrix

| Task Class | Thinking | Budget | Latency Target | Tokens (est.) | Planner | Critic | Reflection | Memory | Knowledge |
|------------|----------|--------|----------------|---------------|---------|--------|------------|--------|----------|
| Greeting | No | 0 | < 2s | 100-200 | No | No | No | No | No |
| Simple Question | No | 0 | < 3s | 200-400 | No | No | No | No | No |
| Casual Discussion | Yes | 1000 | < 5s | 300-600 | No | No | No | Yes | No |
| Business Analysis | Yes | 8000 | < 15s | 600-1200 | No | No | Yes | Yes | Yes |
| Architecture Design | Yes | 16000 | < 35s | 1000-2500 | Yes | Yes | Yes | Yes | Yes |
| Coding | Yes | 8000 | < 20s | 500-2000 | No | Yes | No | Yes | Yes |
| Debugging | Yes | 10000 | < 25s | 400-1500 | No | Yes | No | Yes | Yes |
| Security Analysis | Yes | 14000 | < 30s | 600-2000 | No | Yes | Yes | Yes | Yes |
| Hospitality | Yes | 6000 | < 12s | 400-800 | No | No | Yes | Yes | No |
| Research | Yes | 12000 | < 30s | 800-2000 | Yes | No | Yes | Yes | Yes |
| Planning | Yes | 10000 | < 25s | 600-1500 | Yes | No | Yes | Yes | Yes |

---

## Classification Signals

```yaml
signals:
  greeting:          ["halo", "hi", "hey", "selamat", "pagi", "siang", "malam"]
  simple_question:   [single sentence, ends with "?", < 15 words]
  business:          ["analisis", "strategi", "revenue", "profit", "market", "LTV", "CAC"]
  architecture:      ["design", "system", "architecture", "schema", "scale", "infrastructure"]
  coding:            ["code", "function", "implement", "write", "class", "API", "script"]
  debugging:         ["error", "bug", "fix", "broken", "not working", "exception", "crash"]
  security:          ["vulnerability", "CVE", "attack", "injection", "exploit", "OWASP"]
  hospitality:       ["tamu", "kamar", "hotel", "restoran", "complaint", "check-in", "checkout"]
  research:          ["riset", "research", "literature", "compare", "survey", "review"]
  planning:          ["plan", "roadmap", "milestone", "schedule", "sprint", "phase"]
```

---

## Override Signals

```
/think         → force MAXIMUM profile
/nothink       → force NONE profile
/fast          → force NONE profile + minimal context
/deep          → force DEEP profile + full context
```

---

*File: runtime/openwebui/reasoning/reasoning_selector.md | Last updated: 2026-07-20*
