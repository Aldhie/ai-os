# AI-9003: Prompt Engineering Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9003 |
| **Title** | Prompt Engineering Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |
| **Evidence Level** | Official Doc + Experiment |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Model capabilities spec |
| [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) | API parameters |
| [AI-9001](AI-9001-Documentation-Standard.md) | Parent standard |
| [EXP-0004](../05_EXPERIMENTS/EXP-0004-SystemPrompt.md) | System prompt experiments |
| [EXP-0003](../05_EXPERIMENTS/EXP-0003-Thinking.md) | Thinking mode experiments |

---

## 1. Purpose

This standard defines the engineering rules for all prompts in `Aldhie/ai-os`. Prompts are treated as **software artifacts** with version control, testing, and quality requirements.

---

## 2. Nemotron Ultra 550B — Model-Specific Rules

Based on [FACT: Official Doc — NVIDIA NIM API Reference]:

### 2.1 Thinking Mode Control

| Method | Mechanism | Use When |
|--------|-----------|----------|
| System prompt `/think` | `{"role": "system", "content": "/think"}` | Default reasoning ON |
| System prompt `/nothink` | `{"role": "system", "content": "/nothink"}` | Disable reasoning |
| `extra_body` (Pipeline only) | `{"chat_template_kwargs": {"enable_thinking": true}}` | Programmatic control |
| `medium_effort` (Pipeline only) | `{"chat_template_kwargs": {"medium_effort": true}}` | Token-efficient reasoning |

**Rule:** Never mix `/think` and `/nothink` in the same system prompt. The last directive wins.

### 2.2 Recommended Base Parameters

[FACT: Official Doc — NVIDIA NIM examples use `temperature=1.0, top_p=0.95` for all tasks]

```json
{
 "temperature": 1.0,
 "top_p": 0.95
}
```

**Forbidden parameters** (silently ignored by NIM):
- `top_k` — not supported [FACT: Official Doc]
- `repetition_penalty` — not supported [FACT: Official Doc]

### 2.3 System Prompt Architecture

```
[Role Definition]
[Thinking Mode: /think or /nothink]
[Behavioral Constraints]
[Output Format]
[Domain Context if applicable]
```

Maximum system prompt: 500 tokens (reserve budget). [HYPOTHESIS: Longer system prompts reduce effective reasoning budget — needs EXP-0004 validation]

---

## 3. Prompt File Naming Convention

```
prompts/
 system/
 [profile-name]-system.md     # e.g., reasoning-system.md
 task/
 [task-name]-task.md          # e.g., code-review-task.md
 few-shot/
 [task-name]-fewshot.md       # e.g., classification-fewshot.md
```

---

## 4. Prompt Version Header

Every prompt file MUST include:

```markdown
---
Prompt ID: PROMPT-[XXXX]
Version: X.Y.Z
Profile: [general / reasoning / code / creative / medium_effort]
Thinking Mode: [on / off / medium_effort]
Temperature: [value]
Top-P: [value]
Max Tokens: [value]
Last Validated: [YYYY-MM-DD]
Benchmark: [BM-XX or PENDING]
---
```

---

## 5. Prompt Quality Criteria

| Criterion | Standard |
|-----------|----------|
| Specificity | Every instruction is unambiguous |
| Completeness | No implicit expectations |
| Testability | Has at least one benchmark TC |
| Mode declaration | Explicit thinking mode |
| Format declaration | Explicit output format |
| Token efficiency | No unnecessary verbose phrases |

---

## 6. Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `Be helpful and accurate` | Vague — model default anyway | Specify exact behavior |
| `Think step by step` | Redundant with `/think` mode | Remove, use system directive |
| Mixed `/think` + `/nothink` | Undefined behavior | Choose one |
| Prompt > 1000 tokens | Exceeds system prompt budget | Compress or move to knowledge base |
| No output format | Model chooses format | Specify markdown/json/plain |
| `Answer in any language` | Inconsistent UX | Specify language policy |

---

## 7. Prompt Testing Requirements

Before any system prompt is promoted to `Active`:

```
[ ] Runs successfully on at least 3 test cases
[ ] Thinking mode behavior verified (on/off as intended)
[ ] Output format is consistent
[ ] Token count within budget
[ ] Benchmark TC assigned
[ ] No forbidden parameters referenced
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial prompt engineering standard |
