# AI-9002: Benchmark Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9002 |
| **Title** | Benchmark and Experiment Engineering Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All experiments and benchmarks in `Aldhie/ai-os` |
| **Cross-References** | [AI-9001](AI-9001-Documentation-Standard.md) · [AI-9003](AI-9003-Prompt-Engineering-Standard.md) · [AI-0004](../00_ENGINEERING/AI-0004-Benchmark.md) |

---

## 1. Purpose

This standard defines the required structure, methodology, and reporting format for all benchmarks and experiments in this repository. A benchmark without a reproducible procedure has no engineering value. A result without an expected baseline cannot be interpreted.

---

## 2. Benchmark ID System

| Prefix | Type | Example |
|--------|------|---------|
| `BM-xx` | API/Integration Benchmark | `BM-09: qwen3_coder tool call format` |
| `TC-xxxx` | Functional Test Case | `TC-0001: Basic reasoning response` |
| `EXP-xxxx` | Experiment Document | `EXP-0001-Temperature.md` |

---

## 3. Required Experiment Structure

Every `EXP-xxxx` document MUST contain all of the following sections:

### 3.1 Header
```markdown
| Field | Value |
|-------|-------|
| Experiment ID | EXP-xxxx |
| Title | ... |
| Status | Planned / In Progress / Complete / Cancelled |
| Hypothesis | One sentence |
| Owner | Aldhie |
| Date | YYYY-MM-DD |
| Related BM | BM-xx (if applicable) |
```

### 3.2 Required Sections

1. **Objective** — What engineering question does this answer?
2. **Hypothesis** — Specific, falsifiable prediction with expected direction
3. **Variables**
 - Independent: what you change
 - Dependent: what you measure
 - Controlled: what you hold constant
4. **Environment** — Model, API version, Open WebUI version, date, hardware
5. **Procedure** — Step-by-step, reproducible instructions
6. **Expected Result** — Quantified baseline prediction
7. **Actual Result** — Raw data, not interpreted
8. **Analysis** — Statistical or qualitative interpretation
9. **Conclusion** — Was hypothesis confirmed, refuted, or inconclusive?
10. **Engineering Decision** — What config change does this result mandate?
11. **Future Work** — What follow-up experiments does this open?
12. **Benchmark Result Table** — Required for all completed experiments

---

## 4. Benchmark Result Table Format

```markdown
| Run | Variable Value | Metric | Result | Pass/Fail | Notes |
|-----|---------------|--------|--------|-----------|-------|
| 1 | temperature=0.0 | coherence_score | 7.2/10 | Pass | ... |
| 2 | temperature=0.6 | coherence_score | 8.1/10 | Pass | ... |
| 3 | temperature=1.0 | coherence_score | 8.4/10 | Pass | ... |
```

---

## 5. Test Case Structure (TC-xxxx)

Every `TC-xxxx.md` MUST contain:

```markdown
## TC-xxxx: <Title>

| Field | Value |
|-------|-------|
| ID | TC-xxxx |
| Category | reasoning / coding / discussion / planning / ... |
| Difficulty | Easy / Medium / Hard / Expert |
| Required Capability | tool_calling / RAG / reasoning / ... |

### Question
<Exact prompt to send>

### Expected Behaviour
<What a correct response looks like>

### Evaluation Criteria
- Criterion 1: weight xx%
- Criterion 2: weight xx%

### Scoring
| Score | Meaning |
|-------|---------|
| 5 | Perfect |
| 4 | Good with minor gaps |
| 3 | Acceptable |
| 2 | Partial |
| 1 | Fail |

### Failure Condition
<What constitutes a test failure>

### Success Condition
<Minimum acceptable score and behavior>

### References
<Links to related docs>
```

---

## 6. Statistical Requirements

- Minimum 3 runs per variable value for quantitative benchmarks
- Report mean ± standard deviation when n ≥ 3
- State confidence level for any threshold claims
- Never report single-run results as representative without explicit caveat

---

## 7. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
