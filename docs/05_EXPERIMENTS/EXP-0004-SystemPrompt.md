# EXP-0004: System Prompt Engineering — Structure and Content Effect

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0004 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0008 |

## Related Documents

- ↑ [REQ-AI-0008](../00_ENGINEERING/REQ-INDEX.md#req-ai-0008)
- ↑ [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- → [EXP-0003 Thinking](./EXP-0003-Thinking.md)

---

## Objective

Determine how system prompt structure, length, and content affect response quality, behaviour consistency, and context budget consumption. Find the optimal system prompt design for this repository's use cases.

---

## Hypothesis

**H1:** System prompts under 200 tokens produce equivalent behaviour to 500-token prompts when content is well-structured.

**H2:** Including explicit behavioural rules ("always cite sources", "never assume") improves compliance vs implicit intent.

**H3:** Placing the /think or /nothink directive on the first line is required for reliable activation — placement elsewhere may fail.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Prompt length | Independent | 50 tokens, 200 tokens, 500 tokens |
| Directive placement | Independent | First line, last line, middle |
| Instruction explicitness | Independent | Implicit intent, explicit rules |
| Task type | Controlled | Discussion, Coding, Reasoning |

---

## Procedure

1. Write 3 system prompt variants:
   - Minimal (50 tokens): directive + 1-line role
   - Standard (200 tokens): directive + role + 5 rules
   - Full (500 tokens): directive + role + 10 rules + domain context
2. Test directive placement: first line vs last line.
3. For each combination, run 5 test prompts.
4. Evaluate: (a) directive compliance, (b) role adherence, (c) rule compliance, (d) response quality.

---

## Expected Result

| Prompt Length | Compliance | Quality | Token Cost |
|---------------|-----------|---------|------------|
| 50 tokens | Partial | Moderate | Minimal |
| 200 tokens | High | High | Low |
| 500 tokens | High | High | Medium |

**Expected finding:** 200-token prompt is optimal — high compliance at low token cost.

---

## Actual Result

*Status: Not yet executed.*

---

## Conclusion

*Pending execution.*

---

## Decision

*Current: Standard 200-token prompt template in use.*

---

## Benchmark Result

*Pending execution.*

---

*EXP-0004 v1.0.0 — Created 2026-07-20*
