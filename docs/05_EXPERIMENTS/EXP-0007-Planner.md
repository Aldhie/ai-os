# EXP-0007: Planner Capability — Multi-Step Task Planning Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **EXP ID** | EXP-0007 |
| **Version** | 1.0.0 |
| **Status** | 📋 Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **REQ** | REQ-AI-0004, REQ-AI-0005 |

## Related Documents

- ↑ [REQ-AI-0004](../00_ENGINEERING/REQ-INDEX.md#req-ai-0004)
- → [EXP-0008 Reflection](./EXP-0008-Reflection.md)
- → [EXP-0010 Agent](./EXP-0010-Agent.md)

---

## Objective

Evaluate Nemotron Ultra 550B's ability to decompose complex goals into executable multi-step plans. Measure plan completeness, feasibility, and step sequencing correctness.

---

## Hypothesis

**H1:** Thinking ON (/think) produces more complete and feasible plans than Thinking OFF for tasks requiring >5 steps.

**H2:** The model correctly identifies dependencies between plan steps and sequences them accordingly.

**H3:** Plans produced without role/context in system prompt are less specific than plans with domain context.

---

## Variables

| Variable | Type | Values |
|----------|------|--------|
| Thinking mode | Independent | OFF, ON |
| System prompt context | Independent | Generic, Domain-specific |
| Task complexity | Independent | 3-step, 5-step, 10-step |
| Domain | Controlled | Software engineering, Business |

---

## Procedure

1. Create 6 planning prompts across complexity levels.
2. For each: run with thinking OFF and ON, generic and domain-specific prompts.
3. Evaluate: (a) completeness (all required steps present), (b) feasibility (steps are executable), (c) sequencing (dependencies respected), (d) specificity (actionable vs vague).
4. Score 0–5 per criterion.

---

## Expected Result

| Condition | Completeness | Feasibility | Sequencing |
|-----------|-------------|-------------|------------|
| Think OFF, Generic | 3/5 | 3/5 | 3/5 |
| Think ON, Generic | 4/5 | 4/5 | 4/5 |
| Think ON, Domain | 5/5 | 5/5 | 5/5 |

---

## Actual Result

*Status: Not yet executed.*

---

## Benchmark Result

*Pending PLAN-TC-* execution.*

---

*EXP-0007 v1.0.0 — Created 2026-07-20*
