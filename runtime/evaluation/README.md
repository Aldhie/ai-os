# Evaluation Framework

> **Version**: 1.0.0
> **Spec Ref**: AI-9002-Benchmark-Standard.md, benchmark/tests/

---

## Purpose

This framework provides structured, numerical evaluation of every major runtime component. Every change to the runtime must be validated against this framework before promotion to production.

---

## Directory Structure

```
runtime/evaluation/
├── README.md                  ← this file
├── baseline/                  ← baseline scores for v1.0.0
├── results/                   ← run results (per evaluation run)
├── scoring/                   ← scoring rubrics and weighting
└── reports/                   ← generated reports (automated)
```

---

## Evaluation Dimensions

| Dimension | What It Tests | Score Target |
|-----------|--------------|-------------|
| Prompt v1 vs v2 | System prompt quality delta | +5% response quality |
| Parameter Profile | Optimal settings per task type | Latency/quality tradeoff |
| Memory Strategy | Preference recall accuracy | ≥90% recall |
| Knowledge Strategy | RAG precision/recall | RAGAS ≥80% |
| Planner | Plan correctness | ≥85% step accuracy |
| Reflection | Self-correction rate | ≥70% error catch rate |
| Critic | False positive/negative rate | <10% false positive |

---

## Scoring Format

Every evaluation run produces a `results/{run_id}.json` with:

```json
{
  "run_id": "eval-20260720-001",
  "component": "system_prompt",
  "version_tested": "v1.0.0",
  "baseline_version": "v1.0.0",
  "scores": {
    "factual_accuracy": 9.2,
    "reasoning_quality": 8.8,
    "code_correctness": 8.5,
    "rag_faithfulness": 8.1,
    "memory_recall": 9.0,
    "latency_p50_seconds": 18.3,
    "latency_p95_seconds": 67.4
  },
  "pass": true,
  "notes": ""
}
```

---

## Running an Evaluation

1. Select the component to evaluate
2. Copy the test suite from `benchmark/tests/{component}/`
3. Run against current runtime configuration
4. Record scores in `results/{run_id}.json`
5. Compare against `baseline/{component}_baseline.json`
6. If regression detected (≥5% drop on any metric): block deployment
