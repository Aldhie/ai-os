# AI-0004 — Benchmark Strategy

| Field | Value |
|-------|-------|
| **Title** | AI-OS Benchmark Strategy |
| **Purpose** | Define the benchmarking framework, metrics, and evaluation methodology for AI-OS |
| **Scope** | Benchmark categories, test case design, scoring rubrics, regression policy |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | AI-0001-Nemotron-Engineering-Spec.md |
| **References** | docs/90_TESTING/BenchmarkCases.md, benchmark/README.md |

---

## 1. Benchmark Philosophy

Benchmarks must reflect **real-world usage**, not synthetic metrics. Every benchmark case should map to a user scenario that matters in production.

## 2. Benchmark Categories

| Category | Weight | Description |
|----------|--------|-------------|
| Instruction Following | 25% | Ability to follow complex, multi-step instructions |
| Reasoning | 25% | Chain-of-thought, logic, and deduction |
| Code Generation | 20% | Correctness, style, and production readiness |
| Factual Accuracy | 15% | Grounded, accurate responses |
| Tone & Persona | 10% | Consistent persona adherence |
| Edge Cases | 5% | Handling ambiguous or adversarial inputs |

## 3. Scoring Rubric

| Score | Label | Criteria |
|-------|-------|----------|
| 5 | Excellent | Fully correct, complete, well-structured |
| 4 | Good | Correct with minor issues |
| 3 | Acceptable | Mostly correct, some gaps |
| 2 | Poor | Significant errors or omissions |
| 1 | Fail | Incorrect or harmful output |

## 4. Evaluation Process

1. Run test cases from `docs/90_TESTING/BenchmarkCases.md`
2. Record raw model output in `benchmark/results/`
3. Score each case using the rubric above
4. Calculate weighted category scores
5. Compare against previous version baseline
6. Flag regressions (score drop > 0.5 on any category)

## 5. Regression Policy

- Any configuration change requires a benchmark run before merging
- Regressions must be documented in `docs/90_TESTING/Regression.md`
- No release is approved with an unresolved regression

## 6. Baseline

| Metric | Target (v1.0) |
|--------|---------------|
| Overall score | ≥ 4.0 / 5.0 |
| Instruction Following | ≥ 4.2 |
| Reasoning | ≥ 4.0 |
| Code Generation | ≥ 3.8 |
| Factual Accuracy | ≥ 4.0 |

---

## TODO

- [ ] Create first 50 benchmark test cases
- [ ] Build automated scoring script in `scripts/`
- [ ] Run baseline benchmark on Nemotron 550B
- [ ] Compare against GPT-4o and Claude 3.5 Sonnet baselines
- [ ] Publish results in `benchmark/results/`
