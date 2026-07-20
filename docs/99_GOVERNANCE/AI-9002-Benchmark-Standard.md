# AI-9002: Benchmark Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9002 |
| **Title** | Benchmark Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9001 — Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9003 — Prompt Engineering Standard](AI-9003-Prompt-Engineering-Standard.md)
- [AI-0004 — Benchmark Index](../00_ENGINEERING/AI-0004-Benchmark.md)
- [EXP-0001 to EXP-0010](../05_EXPERIMENTS/)

---

## 1. Purpose

Defines the mandatory structure, scoring methodology, and execution process for all benchmark test cases in `benchmark/tests/`. Benchmarks are the empirical foundation of every engineering decision. A claim without a benchmark is a hypothesis; a hypothesis without a benchmark is folklore.

---

## 2. Test Case Mandatory Structure

Every `TC-xxxx.md` file must contain all of the following sections:

```markdown
# TC-[CATEGORY]-[NUMBER]: [Title]

## Metadata
| Field | Value |
|-------|-------|
| Test ID | TC-[CATEGORY]-[NUMBER] |
| Category | [discussion/reasoning/planning/...] |
| Difficulty | Easy / Medium / Hard / Expert |
| Required Capability | [tool_calling / reasoning / RAG / ...] |
| Status | Pending / Running / Complete |
| Last Run | [ISO 8601 date or N/A] |
| References | [AI-xxx links] |

## Objective
[One sentence: what specifically is being measured]

## Question / Prompt
[Exact prompt sent to the model — no paraphrase]

## System Prompt Used
[Exact system prompt, or "none"]

## Parameters Used
| Parameter | Value |
| temperature | 1.0 |
| top_p | 0.95 |
| max_tokens | [N] |
| thinking | on / off / medium_effort |

## Expected Behavior
[Precise description of what a correct response contains]

## Evaluation Criteria
| Criterion | Weight | Pass Condition |
|-----------|--------|----------------|

## Scoring
| Score | Condition |
|-------|----------|
| 5 | All criteria met; response is exemplary |
| 4 | All criteria met; minor quality issues |
| 3 | Most criteria met; one significant gap |
| 2 | Partial; multiple gaps |
| 1 | Minimal; major failure |
| 0 | Complete failure or harmful output |

## Failure Condition
[Exact condition under which the test is marked FAIL]

## Success Condition
[Exact condition under which the test is marked PASS — minimum score 3]

## Actual Result
[Filled in after execution — verbatim or summarized response]

## Score Achieved
[Number 0–5]

## Analysis
[Engineering analysis of result]

## Decision
[What engineering decision follows from this result]
```

---

## 3. Benchmark Categories

| Category | Directory | Measures |
|----------|-----------|----------|
| `discussion` | `benchmark/tests/discussion/` | General reasoning, conversation quality |
| `reasoning` | `benchmark/tests/reasoning/` | Multi-step reasoning, chain-of-thought |
| `planning` | `benchmark/tests/planning/` | Task decomposition, agentic planning |
| `architecture` | `benchmark/tests/architecture/` | System design quality |
| `coding` | `benchmark/tests/coding/` | Code correctness, debugging |
| `debugging` | `benchmark/tests/debugging/` | Root cause analysis, error diagnosis |
| `hospitality` | `benchmark/tests/hospitality/` | Domain knowledge (Ezy Stay) |
| `business` | `benchmark/tests/business/` | Business analysis, strategy |
| `docker` | `benchmark/tests/docker/` | Container engineering |
| `openwebui` | `benchmark/tests/openwebui/` | Open WebUI feature behavior |
| `nim` | `benchmark/tests/nim/` | NVIDIA NIM API behavior |
| `memory` | `benchmark/tests/memory/` | Memory retention, recall accuracy |
| `rag` | `benchmark/tests/rag/` | RAG retrieval quality |

---

## 4. Scoring Methodology

### 4.1 Multi-Criterion Scoring

For each test case with `n` criteria:

```
Final Score = Σ(criterion_score × weight) / Σ(weights)
```

Where `criterion_score` is 0 (fail) or 1 (pass) per criterion, and `weight` is the assigned weight from the evaluation criteria table.

### 4.2 Pass/Fail Threshold

- **PASS:** Final Score ≥ 3.0 / 5.0 (60%)
- **FAIL:** Final Score < 3.0 / 5.0
- **CRITICAL FAIL:** Score = 0 or harmful output

### 4.3 Benchmark Run Requirements

A benchmark result is only valid if:
- Run 3 times minimum (to account for model stochasticity at `temperature: 1.0`)
- All 3 runs use identical parameters
- Mean and variance reported
- Run date and model version recorded

---

## 5. Benchmark Traceability

Every benchmark must map to at least one of:
- An engineering requirement (`REQ-AI-xxxx`)
- A configuration parameter (in `configs/`)
- An experiment (`EXP-xxxx`)
- A risk item from the Risk Register

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial benchmark standard |
