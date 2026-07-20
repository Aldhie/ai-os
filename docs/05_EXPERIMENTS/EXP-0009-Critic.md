# EXP-0009: Critic Agent Pattern

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0009 |
| **Title** | Critic Agent — Quality of Self-Evaluation and Error Detection |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related REQ** | REQ-AI-0010 (critic agent) |
| **Cross-References** | [EXP-0008](EXP-0008-Reflection.md) · [EXP-0010](EXP-0010-Agent.md) · [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) |

---

## 1. Objective

Evaluate whether Nemotron Ultra 550B can act as a **critic agent** — evaluating the output of another agent (or itself in a separate role) and producing actionable, accurate critique.

Critic agent pattern: Generator produces output → Critic evaluates → Generator revises.

---

## 2. Hypothesis

> **H1:** Critic agent with a separate system prompt ("You are a strict technical reviewer") will produce more accurate critiques than asking the generator to self-evaluate in the same turn.
>
> **H2:** Critic agent in reasoning ON mode will identify 20–40% more errors than reasoning OFF mode.
>
> **H3:** Critic-revision loop will converge to higher quality output in 2–3 iterations.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | Critic role | Same-turn self-eval, Separate-turn same model, Separate-turn different prompt |
| **Independent** | Reasoning mode | OFF, ON |
| **Dependent** | Error detection rate (%) | Errors found / total errors |
| **Dependent** | Critique actionability | Binary |
| **Dependent** | Quality after revision | 1-10 rubric |
| **Dependent** | Iteration count to convergence | Integer |

---

## 4. Test Artifacts

Create 5 deliberately flawed responses:
1. Code with 3 intentional bugs
2. Plan with 2 missing dependencies
3. Analysis with 1 factual error
4. Security design with 1 vulnerability
5. API design with 2 RESTful violations

---

## 5. Procedure

1. Present each flawed artifact to critic in each role configuration
2. Score error detection rate against known-flaw list
3. Rate critique actionability
4. Feed critique back to generator; score revised output
5. Repeat for up to 3 iterations

---

## 6. Expected Result

- Separate-turn critic: 80–90% error detection
- Same-turn self-eval: 50–65% error detection
- Reasoning ON delta: +20–25% detection rate
- Convergence: 2 iterations for most artifacts

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
