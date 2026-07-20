# EXP-0004: System Prompt Engineering

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0004 |
| **Title** | System Prompt Structure and Effectiveness |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-9003 Prompt Engineering Standard](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md)
- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [prompts/system/](../../prompts/system/)
- [benchmark/tests/discussion/TC-0001.md](../../benchmark/tests/discussion/TC-0001.md)

---

## 1. Objective

Determine the optimal system prompt structure for Nemotron Ultra 550B across different task types. Specifically: does prompt length, role framing, and constraint specification significantly affect output quality?

---

## 2. Background

**[FACT]** Open WebUI injects system prompts as `{role: "system"}` messages. NIM processes these correctly.

**[FACT]** System prompt `/think` or `/nothink` controls reasoning mode on Nemotron Ultra 550B.

**[HYPOTHESIS]** Longer, more structured system prompts increase benchmark scores but also increase token cost.

**[HYPOTHESIS]** Role-framing ("You are an expert X") improves domain-specific response quality.

---

## 3. Hypotheses

| ID | Hypothesis |
|----|----------|
| H1 | Explicit role framing improves domain accuracy by >= 0.5 score points |
| H2 | Constraint specification (what NOT to do) reduces harmful outputs and hallucinations |
| H3 | System prompts over 300 tokens produce diminishing returns |
| H4 | Output format specification in system prompt improves structured output adherence |

---

## 4. Variables

**Independent:** System prompt variants (A: minimal, B: role-framed, C: role+constraints, D: full structured)
**Controlled:** user prompt fixed, temperature: 1.0, top_p: 0.95, thinking mode: per task
**Dependent:** Benchmark score, format compliance, hallucination rate, token cost

---

## 5. Procedure

**Variant A (Minimal):**
```
/nothink
```

**Variant B (Role-framed):**
```
You are an expert AI assistant specializing in technical analysis. /nothink
```

**Variant C (Role + Constraints):**
```
You are an expert AI assistant specializing in technical analysis.
Do not speculate beyond provided information.
Always cite the specific document or data source when making claims.
/nothink
```

**Variant D (Full Structured):**
```
# Role
You are a Senior AI Engineer assistant for the ai-os project.

# Behavioral Constraints
- Do not speculate beyond provided context
- Always acknowledge uncertainty explicitly
- Prefer structured outputs (tables, lists) for technical information
- For code: include comments and explain design decisions

# Output Format
- Use markdown headers for multi-section responses
- Limit responses to task scope — do not add unsolicited information

/nothink
```

Run each variant against TC-discussion-0001, TC-reasoning-0001, TC-coding-0001 × 5 reps each.

---

## 6. Expected Results

| Variant | Expected Score | Token Cost |
|---------|---------------|------------|
| A (minimal) | 3.0 | 1x |
| B (role) | 3.5 | 1.1x |
| C (role+constraints) | 4.0 | 1.2x |
| D (full) | 4.2 | 1.4x |

H3 prediction: D vs C delta < 0.3, but D costs 15% more tokens.

---

## 7–13. Actual Result / Analysis / Conclusion / Decision / Future Work / Benchmark Results

> ⏳ **PENDING**

**Decision will feed:** prompts/system/ canonical prompt files, AI-9003 standard update.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design |
