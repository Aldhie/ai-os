# EXP-0004: System Prompt Architecture

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0004 |
| **Title** | System Prompt Architecture: Length, Structure, and Behavioral Impact |
| **Version** | 1.0.0 |
| **Status** | Pending |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Priority** | High |

---

## Cross References

- [AI-9003 — Prompt Engineering Standard](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md)
- [AI-0003 — Open WebUI Compatibility](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md)
- [EXP-0003 — Thinking Mode](EXP-0003-Thinking.md)
- [prompts/system/](../../prompts/system/)

---

## 1. Objective

Determine optimal system prompt structure for Nemotron Ultra 550B: (1) minimal vs structured vs long-form prompts, (2) position of reasoning mode token (`/think`/`/nothink`), (3) impact of explicit output format instructions.

---

## 2. Hypothesis

> `[HYPOTHESIS]` Structured system prompts with explicit behavioral directives, output format specification, and reasoning mode token at the END of the system prompt produce better compliance than minimal prompts. Prompts >1000 tokens do not improve behavior and waste token budget.

---

## 3. Variables

### Independent Variable — Prompt Architecture

| Variant | Structure |
|---------|----------|
| A: Minimal | `"You are a helpful assistant. /think"` |
| B: Structured | Role + 3 directives + output format + reasoning token (200–400 tokens) |
| C: Verbose | Role + detailed persona + 10 directives + examples + reasoning token (800–1200 tokens) |
| D: Token Position | Same as B but `/think` token at START of prompt |

### Controlled Variables

| Parameter | Value |
|-----------|-------|
| `temperature` | `1.0` |
| `top_p` | `0.95` |
| `max_tokens` | `2048` |

---

## 4. Procedure

1. Design prompts A, B, C, D
2. Test against 5 task types (general, reasoning, code, creative, refusal)
3. Score behavioral compliance (did model follow instructions?)
4. Score output quality
5. Compare token efficiency (output quality per token spent on system prompt)

---

## 5. Expected Result

- Variant B outperforms A on compliance without wasteful token use
- Variant C shows no improvement over B (diminishing returns)
- Reasoning token position at end is equivalent to start

---

## 6. Actual Result

> `[PENDING]`

---

## 7. Decision

> `[PENDING]` Establish canonical system prompt templates for each agent profile.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
