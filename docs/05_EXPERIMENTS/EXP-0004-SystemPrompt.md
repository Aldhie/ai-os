# EXP-0004: System Prompt Engineering

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0004 |
| **Title** | System Prompt Structure and Length Impact on Response Quality |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related REQ** | REQ-AI-0004 (system prompt design) |
| **Cross-References** | [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) · [EXP-0003](EXP-0003-Thinking.md) |

---

## 1. Objective

Determine the optimal system prompt structure for Nemotron Ultra 550B. Specifically:
- Does system prompt length affect response quality or token efficiency?
- Does prompt structure (bullets vs. prose vs. numbered rules) matter?
- What is the minimum viable system prompt?

---

## 2. Hypothesis

> **H1:** System prompts longer than 300 tokens provide diminishing returns on response quality.
>
> **H2:** Structured prompts (numbered rules) will produce more consistent behavior than prose prompts.
>
> **H3:** The `/think` or `/nothink` declaration MUST be first line; placing it elsewhere will reduce reasoning consistency. [HYPOTHESIS — based on chat template behavior, not confirmed]

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | System prompt length | 50, 100, 200, 300, 500 tokens |
| **Independent** | Prompt structure | Prose, bullets, numbered rules |
| **Independent** | `/think` position | Line 1, Line 3, End, Absent |
| **Dependent** | Response consistency (std dev across 5 runs) | Measured |
| **Dependent** | Task completion accuracy | 1-10 rubric |
| **Controlled** | `temperature` | 1.0 |
| **Controlled** | Task | Same 3 prompts across all runs |

---

## 4. Environment

| Component | Config |
|-----------|--------|
| Model | nvidia/nemotron-3-ultra-550b-a55b |
| Runs per condition | 5 |

---

## 5. Procedure

1. Define 6 system prompt variants of increasing length and different structure
2. Test each variant with the same 3 task prompts
3. Score response quality and measure consistency (coefficient of variation)
4. Test `/think` position variants with same prompt
5. Identify optimal minimum-viable system prompt structure

---

## 6. Expected Result

- Prompts ≤ 300 tokens expected to be as effective as 500-token prompts
- Numbered structure expected to show lower std dev (more consistent)
- `/think` on line 1 expected to produce more reliable reasoning activation

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING**

Decision on completion: Update `AI-9003-Prompt-Engineering-Standard.md` Section 4.3 token budget guidelines.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
