# EXP-0007: Agentic Planning Quality

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0007 |
| **Title** | Agentic Planning — Multi-Step Task Decomposition Quality |
| **Status** | Planned |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Related BM** | BM-02, BM-03 |
| **Related REQ** | REQ-AI-0008 (planning agent) |
| **Cross-References** | [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) · [EXP-0003](EXP-0003-Thinking.md) · [EXP-0010](EXP-0010-Agent.md) |

---

## 1. Objective

Evaluate Nemotron Ultra 550B's ability to decompose complex multi-step tasks into executable sub-tasks. Compare planning quality with reasoning ON vs. OFF. Evaluate plan correctness, completeness, and executability.

---

## 2. Hypothesis

> **H1:** Reasoning ON (`/think`) will produce significantly more complete plans than OFF for tasks with >5 steps.
>
> **H2:** Plans generated with reasoning ON will have fewer logical dependencies missed (≥ 90% dependency completeness vs ~70% OFF).
>
> **H3:** Nemotron Ultra 550B will outperform Super 49B on planning tasks with 10+ steps due to larger reasoning capacity.

---

## 3. Variables

| Type | Variable | Values |
|------|----------|---------|
| **Independent** | Task complexity | 3-step, 7-step, 12-step tasks |
| **Independent** | Reasoning mode | OFF, ON |
| **Dependent** | Plan completeness (%) | Steps covered / steps required |
| **Dependent** | Logical coherence | 1-10 rubric |
| **Dependent** | Executability | Binary (can a human execute this?) |
| **Dependent** | Thinking tokens | From API usage |

---

## 4. Test Tasks

1. **3-step:** "Plan a deployment of a Python Flask app to a VPS"
2. **7-step:** "Design and implement a REST API with authentication, validation, and logging"
3. **12-step:** "Create a complete CI/CD pipeline from scratch with testing, staging, and production environments"

---

## 5. Procedure

1. Run each task with reasoning OFF and ON
2. Grade plan against reference solution (expert-written)
3. Count missed dependencies and logical errors
4. Assess whether each step is actionable/executable
5. Compare token costs between modes

---

## 6. Expected Result

| Task Complexity | Reasoning OFF | Reasoning ON | Delta |
|-----------------|--------------|--------------|-------|
| 3-step | 8.5/10 | 8.7/10 | +0.2 |
| 7-step | 7.0/10 | 8.5/10 | +1.5 |
| 12-step | 5.5/10 | 8.0/10 | +2.5 |

---

## 7–12. Actual Result through Benchmark Table

> **STATUS: PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial experiment design |
