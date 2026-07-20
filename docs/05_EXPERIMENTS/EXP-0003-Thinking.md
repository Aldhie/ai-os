# EXP-0003: Thinking Mode Behavior Validation

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0003 |
| **Title** | Thinking Mode Behavior Validation |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Reasoning Control |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Reasoning capability spec |
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | Thinking mode compatibility |
| [AI-0003-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) | Identified 4 reasoning control methods |
| [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) | Thinking mode control standard |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0005 |

---

## 1. Objective

Validate all four thinking mode control methods available for Nemotron Ultra 550B:
1. System prompt `/think`
2. System prompt `/nothink`
3. `extra_body.chat_template_kwargs.enable_thinking` via Pipeline
4. `medium_effort` mode via Pipeline

Measure: token cost, response quality, and behavioral consistency across each method.

---

## 2. Background

Nemotron Ultra 550B supports selective reasoning. [FACT: Official Doc — NVIDIA NIM API Reference]

Four methods are documented:
- `/think` and `/nothink` in system prompt [FACT: Official Doc]
- `extra_body.chat_template_kwargs.enable_thinking: true/false` [FACT: Official Doc]
- `medium_effort: true` in `chat_template_kwargs` [FACT: Official Doc]
- `reasoning_budget` hard token cap [FACT: Official Doc]

Critical question: When called via Open WebUI with only system prompt method, does the model behave identically to when called with `extra_body` method? [HYPOTHESIS]

---

## 3. Hypothesis

**H1:** `/think` system prompt produces a reasoning trace in `<think>` tags, identical in structure to `enable_thinking: true`. [HYPOTHESIS]

**H2:** `medium_effort` mode produces reasoning traces that are 30-50% shorter than full thinking mode for equivalent task quality. [HYPOTHESIS — to validate]

**H3:** `reasoning_budget=512` effectively truncates reasoning traces at ~512 tokens as documented. [HYPOTHESIS — to validate]

**H4:** When reasoning is OFF via `/nothink`, token consumption is reduced by at least 40% compared to reasoning ON. [HYPOTHESIS]

---

## 4. Variables

### Independent Variable: Thinking Mode
| Mode | Method | Parameters |
|------|--------|------------|
| Full ON (system) | System prompt `/think` | No extra_body |
| Full ON (API) | Pipeline `enable_thinking: true` | extra_body |
| Medium Effort | Pipeline `medium_effort: true` | extra_body |
| OFF (system) | System prompt `/nothink` | No extra_body |
| OFF (API) | Pipeline `enable_thinking: false` | extra_body |
| Budget 512 | Pipeline `reasoning_budget: 512` | extra_body |

### Metrics
| Metric | Measurement |
|--------|-------------|
| Thinking tokens | Count tokens in `<think>...</think>` |
| Answer tokens | Count tokens after `</think>` |
| Answer quality | Score against benchmark ground truth |
| Behavioral equivalence | System vs API method — compare outputs |

---

## 5. Environment

| Component | Value |
|-----------|-------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Temperature | 1.0 (NVIDIA default) |
| Top-P | 0.95 |
| Max Tokens | 16000 |
| Test Tasks | reasoning/TC-0001, coding/TC-0001, nim/TC-0001 |

---

## 6. Procedure

**Phase 1: System prompt method**
1. Run reasoning/TC-0001 with system prompt `/think` — record output, count thinking tokens
2. Run same TC with system prompt `/nothink` — record output, count output tokens

**Phase 2: API method via Pipeline**
1. Enable Pipeline that injects `chat_template_kwargs`
2. Run same TC with `enable_thinking: true` — record output
3. Compare Phase 1 and Phase 2 outputs for structural equivalence

**Phase 3: Medium effort**
1. Run TC with `medium_effort: true` — count thinking tokens
2. Compare answer quality vs Full ON

**Phase 4: Reasoning budget**
1. Run TC with `reasoning_budget: 512` — verify truncation behavior
2. Observe: does it truncate at `~512 + 500` tokens as documented?

---

## 7. Expected Results

| Mode | Thinking Tokens | Answer Quality | Use Case |
|------|-----------------|----------------|----------|
| Full ON | 500-3000 | Highest | Complex reasoning, code |
| Medium Effort | 150-800 | High | Standard Q&A, analysis |
| Budget 512 | ≤ 1012 | Medium-High | Token-constrained |
| OFF | 0 | Medium | Simple Q&A, RAG |

---

## 8. Actual Results

> **Status: PENDING EXECUTION**

| Mode | Thinking Tokens | Answer Quality | Behavioral Match |
|------|-----------------|----------------|-------------------|
| Full ON (system) | PENDING | PENDING | PENDING |
| Full ON (API) | PENDING | PENDING | PENDING |
| Medium Effort | PENDING | PENDING | PENDING |
| Budget 512 | PENDING | PENDING | PENDING |
| OFF (system) | PENDING | PENDING | PENDING |
| OFF (API) | PENDING | PENDING | PENDING |

---

## 9. Analysis

> **PENDING**

Analysis framework:
1. Are system prompt and API methods behaviorally equivalent? (Critical: determines if Pipeline is required)
2. What is the token cost ratio: Full ON vs Medium Effort vs OFF?
3. Does reasoning_budget behave as documented (truncate at budget+500)?

---

## 10. Conclusion

> **PENDING**

---

## 11. Decision

> **PENDING** — Will determine:
> - Whether Pipeline is required for basic use or only advanced use
> - Recommended thinking mode per agent profile
> - Token budget allocations per profile

---

## 12. Future Work

- EXP-0004: Use findings here to optimize system prompt design
- BM-11: Add as benchmark TC for regression testing

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design |
