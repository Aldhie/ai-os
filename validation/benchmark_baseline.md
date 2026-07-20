# Benchmark Automation Specification

> **Status**: RUNTIME | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Overview

Every benchmark run must produce:
1. A JSON result file conforming to `benchmark_schema.json`
2. A Markdown report from this template
3. A numerical overall score (0-100)
4. A regression check against the previous run

---

## Scoring Formula

```
overall = (
  capability  × 0.30 +
  reasoning   × 0.25 +
  latency     × 0.20 +
  knowledge   × 0.10 +
  tool_usage  × 0.10 +
  memory      × 0.05
)
```

---

## Regression Gate

```
A regression is declared if:
  current_overall < previous_overall - 3 points

On regression:
  1. Block the change from merging to main
  2. Generate regression report
  3. Require architecture review
  4. Must identify root cause before merge allowed
```

---

## Test Case Library Structure

```
validation/prompts/
  greeting_01.txt       → class: greeting
  simple_fact_01.txt    → class: simple_fact
  business_01.txt       → class: business_analysis
  architecture_01.txt   → class: architecture
  code_01.txt           → class: coding
  debug_01.txt          → class: debugging
  memory_01.txt         → class: memory_recall
  knowledge_01.txt      → class: domain_knowledge
  planning_01.txt       → class: planning
  security_01.txt       → class: security
  tool_01.txt           → class: tool_usage
  reasoning_01.txt      → class: reasoning
```

---

## Report Template

See `validation/reports/REPORT_TEMPLATE.md`

---

*File: validation/benchmark_baseline.md | Last updated: 2026-07-20*
