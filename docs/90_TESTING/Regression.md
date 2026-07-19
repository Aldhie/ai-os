# Regression Test Suite

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | Regression.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the regression test suite for the AI OS. Regression tests ensure that changes to prompts, parameters, or configuration do not degrade previously working behavior.

---

## Scope

- Regression test case catalog
- Pass/fail criteria
- Execution procedure
- Tracking and reporting

---

## Dependencies

- `docs/90_TESTING/BenchmarkCases.md` — test cases
- `docs/00_ENGINEERING/AI-0004-Benchmark.md` — benchmark strategy
- `benchmark/` — results storage

---

## Regression Test Categories

| Category | Description | Case Count |
|----------|-------------|------------|
| Core Instructions | System prompt adherence | TBD |
| Safety | Refusal of harmful requests | TBD |
| Persona Consistency | Tone and identity stability | TBD |
| Memory Recall | Correct memory retrieval | TBD |
| Tool Use | Correct tool invocation | TBD |
| Reasoning | Multi-step logical reasoning | TBD |

---

## Pass/Fail Criteria

- A regression test **passes** if the response score is ≥ 4/5
- A regression test **fails** if the response score is ≤ 2/5
- A **regression** is detected when a previously passing test now fails

---

## Execution Procedure

1. Run all regression cases against current configuration
2. Score each response using the standard rubric (see AI-0004)
3. Compare scores against the last stable baseline
4. Flag any regressions (previously passing cases now failing)
5. Document and investigate all regressions before release

---

## TODO

- [ ] Write initial regression test cases (minimum 20)
- [ ] Automate regression test execution
- [ ] Define baseline snapshot from first stable release
- [ ] Build regression report template
- [ ] Integrate regression tests into CI/CD workflow
