# Token Budget Specification

> **Status**: RUNTIME | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Philosophy

Every token costs latency and quota. The objective is not to minimize quality — it is to achieve maximum quality at minimum token cost. These are not in conflict; they are the same goal.

A 300-token answer that fully solves the problem is better than a 2000-token answer that partially solves it.

---

## Token Budget Tiers

```yaml
output_budgets:

  nano:                          # greeting, acknowledgment
    max_output_tokens: 150
    use_when: greeting, ack, simple yes/no

  small:                         # quick facts, short answers
    max_output_tokens: 400
    use_when: simple_fact, short_explanation, command_response

  standard:                      # most responses
    max_output_tokens: 1000
    use_when: explanation, analysis, recommendation, casual

  large:                         # detailed technical responses
    max_output_tokens: 2000
    use_when: architecture, complex_analysis, code_with_explanation

  maximum:                       # document generation, specs
    max_output_tokens: 4096
    use_when: full_document, spec_generation, long_code
    warning: high token cost; use only when necessary
```

---

## Free Tier Daily Budget

```
Daily requests:       1000 (NIM free tier)
Avg output tokens:    800
Avg thinking tokens:  4000

Estimated daily output:  800K tokens output
Estimated daily thinking: 4M thinking tokens

Conservative target: stay within 800 requests/day
→ leaves 200 request buffer for batch/spike
```

---

## Token Waste Prevention Rules

1. **No preamble**: never start response with restatement of question
2. **No summary**: never end response with "in summary, we covered..."
3. **No padding**: never add content purely to appear thorough
4. **No redundancy**: never repeat a point already made
5. **Appropriate format**: bullets reduce tokens vs prose for list content
6. **Code over prose**: for technical content, code block is usually more precise and shorter

---

*File: runtime/openwebui/token/token_budget.md | Last updated: 2026-07-20*
