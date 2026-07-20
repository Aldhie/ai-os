# EXP-0003: Thinking Mode Optimization

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0003 |
| **Title** | Thinking Mode Optimization — ON vs OFF vs medium_effort vs reasoning_budget |
| **Version** | 1.0.0 |
| **Status** | Designed |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [AI-0003-Critical-Findings-Audit](../00_ENGINEERING/AI-0003-Critical-Findings-Audit.md) — reasoning mode findings R-03, NEW-01
- [EXP-0001 Temperature](EXP-0001-Temperature.md)
- [AI-9003 Prompt Engineering Standard §6](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md)
- [benchmark/tests/reasoning/](../../benchmark/tests/reasoning/)

---

## 1. Objective

Quantify the quality vs token cost trade-off for Nemotron Ultra 550B across four thinking modes: **OFF**, **ON (full)**, **medium_effort**, and **reasoning_budget** (hard cap). Produce a decision table for Open WebUI model profile configuration.

---

## 2. Background

**[FACT]** Nemotron Ultra 550B supports four thinking control methods per official NVIDIA docs:
1. System prompt `/think` / `/nothink` (Open WebUI compatible)
2. `extra_body.chat_template_kwargs.enable_thinking` (Pipeline required in OW)
3. `extra_body.chat_template_kwargs.medium_effort: true` (Pipeline required)
4. `reasoning_budget: N` (hard token cap, Pipeline required)

Reference: [NVIDIA NIM API Docs](https://docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b)

**[HYPOTHESIS]** `medium_effort` reduces token cost by 30–60% vs full thinking ON, with <15% quality degradation on complex reasoning. Pending empirical validation.

**[HYPOTHESIS]** For coding tasks, `reasoning_budget: 512` provides adequate reasoning at minimal token overhead.

---

## 3. Hypotheses

| ID | Hypothesis | Expected Outcome |
|----|-----------|------------------|
| H1 | Thinking ON significantly outperforms OFF on reasoning tasks | Score delta >= 1.0 on 5-point scale |
| H2 | `medium_effort` achieves 85%+ of full thinking quality at 50% token cost | Token saving >= 40% |
| H3 | Thinking mode has minimal impact on RAG synthesis (doc is ground truth) | Score delta <= 0.3 |
| H4 | `reasoning_budget: 512` sufficient for simple coding; fails on architecture design | Pass rate >= 80% for simple, <= 40% for complex |
| H5 | For customer service tasks, thinking OFF is better (speed > depth) | Latency 3× better, quality acceptable |

---

## 4. Variables

**Independent:** Thinking mode: `[OFF, ON, medium_effort, budget_512, budget_1024, budget_2048]`
**Controlled:** temperature: 1.0, top_p: 0.95, seed: 42
**Dependent:** Benchmark score, `completion_tokens`, estimated time-to-first-token, reasoning token count

---

## 5. Environment

```yaml
model: nvidia/nemotron-3-ultra-550b-a55b
endpoint: https://integrate.api.nvidia.com/v1
temperature: 1.0  # NVIDIA default
top_p: 0.95       # NVIDIA default
method_for_medium_effort: Pipeline injection of extra_body
method_for_budget: Pipeline injection of reasoning_budget
method_for_on_off: system prompt /think and /nothink
```

---

## 6. Procedure

### Phase 1 — Reasoning Benchmark
Tasks: TC-reasoning-0001, TC-reasoning-0002, TC-reasoning-0003
For each thinking mode: run × 5 reps, record score + completion_tokens

### Phase 2 — Coding Benchmark
Tasks: TC-coding-0001, TC-coding-0002
For each thinking mode: run × 3 reps, record unit test pass rate + completion_tokens

### Phase 3 — RAG Synthesis Benchmark
Tasks: TC-rag-0001, TC-rag-0002
For each thinking mode: run × 5 reps, record factual accuracy + hallucination count

### Phase 4 — Hospitality/Customer Service Benchmark
Tasks: TC-hospitality-0001
For each thinking mode: record score + latency

---

## 7. Expected Results

**Table 1 — Expected Thinking Mode Trade-offs**

| Mode | Quality Score | Token Cost | Latency | Best For |
|------|--------------|------------|---------|----------|
| OFF | 3.0/5 | 1x | 1x | RAG, customer service, classification |
| ON | 5.0/5 | 4–8x | 4–8x | Math, logic, complex architecture |
| medium_effort | 4.2/5 | 2–3x | 2–3x | General reasoning, planning |
| budget_512 | 3.8/5 | 1.5x | 1.5x | Simple code, debugging |
| budget_1024 | 4.0/5 | 2x | 2x | Medium complexity tasks |
| budget_2048 | 4.5/5 | 3x | 3x | Complex tasks with budget constraint |

---

## 8. Actual Result

> ⏳ **PENDING** — Requires Pipeline implementation for `medium_effort` and `reasoning_budget` injection.

**Prerequisite:** Build Open WebUI Pipeline for `extra_body` injection before executing phases 1-4.

---

## 9–13. Analysis / Conclusion / Decision / Future Work / Benchmark Results

> ⏳ **To be completed post-execution.**

**Decision will feed:** parameters.json profiles, AI-9003 Thinking Mode Selection Guide, AI-0003 compatibility matrix update.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial design — 4 hypotheses, 4-phase procedure |
