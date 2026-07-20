# AI-0004: Benchmark Framework
## NVIDIA Nemotron Ultra 550B × Open WebUI

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0004 |
| **Version** | 2.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **REQ** | REQ-AI-0012 |

---

## Related Documents

- ↑ [AI-0001 Engineering Spec](./AI-0001-Nemotron-Engineering-Spec.md)
- ↑ [AI-0002 NIM API Reference](./AI-0002-NVIDIA-NIM-API.md)
- ↑ [AI-0003 Compatibility Matrix](./AI-0003-OpenWebUI-Compatibility.md)
- ↓ [REQ-INDEX](./REQ-INDEX.md) REQ-AI-0012
- ↓ [benchmark/tests/](../../benchmark/tests/)
- ↓ [docs/05_EXPERIMENTS/](../05_EXPERIMENTS/)

---

## 1. Purpose

This document defines the benchmark framework for validating NVIDIA Nemotron Ultra 550B capabilities via Open WebUI. Every benchmark item has a unique BM-ID, hypothesis, evaluation criteria, and must produce a measurable result.

**Engineering Principle:** An undocumented capability is an unverified capability. Every claim in AI-0001 through AI-0003 must be traceable to a BM-ID.

---

## 2. Benchmark Categories

| Category | Code | Test Cases | Status | Priority |
|----------|------|------------|--------|----------|
| Discussion | DISC | TC-0001–0003 | ❌ Pending | 🟡 High |
| Reasoning | REAS | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| Planning | PLAN | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| Architecture | ARCH | TC-0001–0003 | ❌ Pending | 🟡 High |
| Coding | CODE | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| Debugging | DBG | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| Hospitality | HOSP | TC-0001–0003 | ❌ Pending | 🟢 Medium |
| Business | BIZ | TC-0001–0003 | ❌ Pending | 🟢 Medium |
| Docker/Infra | DOCK | TC-0001–0003 | ❌ Pending | 🟡 High |
| OpenWebUI | OWU | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| NIM API | NIM | TC-0001–0003 | ❌ Pending | 🔴 Critical |
| Memory/RAG | MEM | TC-0001–0003 | ❌ Pending | 🔴 Critical |

---

## 3. Integration Test Registry (BM-IDs)

These are cross-cutting integration benchmarks that span multiple categories.

| BM-ID | Description | Source | Priority | Status |
|-------|-------------|--------|----------|--------|
| BM-01 | Parallel tool calls — does Ultra 550B return multiple tool_calls in one response? | AI-0003-Audit | 🟡 High | ❌ Pending |
| BM-02 | Agentic RAG — tool calling + retrieval round-trip | AI-0003 | 🔴 Critical | ❌ Pending |
| BM-03 | MCP tool server — OW MCP → NIM tool calling round-trip | AI-0003 | 🟡 High | ❌ Pending |
| BM-04 | OpenAPI tool server — auto-discovered schema → NIM | AI-0003 | 🟢 Medium | ❌ Pending |
| BM-05 | Bound tools per model — forced tool in model config | AI-0003 | 🟢 Medium | ❌ Pending |
| BM-06 | Streaming + tool call accumulation | AI-0003 | 🟡 High | ❌ Pending |
| BM-07 | 429 error display — user-friendly vs raw error | AI-0003 | 🟢 Medium | ❌ Pending |
| BM-08 | Logprobs — OW expose + NIM return | AI-0003 | ⚪ Low | ❌ Pending |
| BM-09 | qwen3_coder tool call format — OW compatibility with Cloud NIM format | AI-0003-Audit | 🔴 Critical | ❌ Pending |
| BM-10 | Context length limit — confirm 256K or 1M on Cloud NIM public endpoint | AI-0003-Audit | 🔴 Critical | ❌ Pending |
| BM-11 | medium_effort via Pipeline — verify Pipeline injection of extra_body | AI-0003-Audit | 🟡 High | ❌ Pending |
| BM-12 | Temperature quality — empirical comparison 1.0 vs 0.6 vs 0.0 | AI-0003-Audit | 🔴 Critical | ❌ Pending |

---

## 4. Benchmark Test Case Template

Every test case in `benchmark/tests/` must follow this structure:

```markdown
# [CATEGORY]-TC-[NNN]: [Title]

## Metadata
- BM-ID: [BM-ID if applicable]
- Category: [Category]
- REQ: [REQ-AI-XXXX]
- Difficulty: [Easy | Medium | Hard | Expert]
- Required Capability: [list]

## Question / Input
[Exact input to model]

## Expected Behaviour
[What the model should do]

## Evaluation Criteria
| Criterion | Weight | Pass Condition |
|-----------|--------|---------------|
| [criterion] | [N%] | [condition] |

## Scoring
| Score | Meaning |
|-------|---------|
| 5/5 | Perfect — all criteria met |
| 4/5 | Good — minor gaps |
| 3/5 | Acceptable — main criteria met |
| 2/5 | Weak — significant gaps |
| 1/5 | Fail — wrong direction |
| 0/5 | Hard fail — error or refusal |

## Failure Conditions
[What constitutes a failure]

## Success Conditions
[What constitutes success]

## Baseline Result
[To be filled after first run]

## References
[REQ-IDs, experiment docs, official docs]
```

---

## 5. Scoring Framework

### 5.1 Per-Test Scoring

Every test case uses a 0–5 scale with weighted criteria.

### 5.2 Category Score

```
Category Score = (Sum of test scores) / (Max possible score) × 100%
```

### 5.3 System Benchmark Score

```
System Score = Weighted average across categories

Weights:
  Critical categories (REAS, PLAN, CODE, DBG, OWU, NIM, MEM): 10% each × 7 = 70%
  High categories (DISC, ARCH, DOCK): 7% each × 3 = 21%
  Medium categories (HOSP, BIZ): 4.5% each × 2 = 9%
  Total: 100%
```

### 5.4 Regression Threshold

- **Green:** Score >= baseline (no regression)
- **Yellow:** Score 1–5% below baseline (investigation needed)
- **Red:** Score >5% below baseline (block deployment)

---

## 6. Benchmark Execution Protocol

### Pre-Run Checklist
```
[ ] configs/openwebui/parameters.json version noted
[ ] configs/openwebui/capabilities.json version noted
[ ] Model version noted (model_id + date)
[ ] OW version noted
[ ] Session memory cleared (benchmark must not use prior memory)
[ ] New OW user session created (avoid RBAC interference)
```

### Execution
```
1. For each category:
   a. Open new chat session
   b. Select Nemotron Ultra 550B model
   c. Apply profile from parameters.json matching test type
   d. Send exact question from TC-NNNN.md
   e. Record response
   f. Score against criteria
   g. Note token usage from OW analytics
   h. Note response time (TTFT + completion time)

2. Record all scores in benchmark/results/YYYY-MM-DD-run.json

3. Calculate category scores and system score

4. Compare to baseline

5. Flag regressions
```

### Post-Run
```
[ ] Results committed to benchmark/results/
[ ] Regression report generated
[ ] Any new failures create GitHub issues
[ ] Baseline updated if config intentionally changed
```

---

## 7. Benchmark Results Baseline

*Status: No baseline exists yet. First run after benchmark framework implementation establishes baseline.*

| Category | Baseline Score | Date Set | Config Version |
|----------|---------------|----------|----------------|
| Discussion | TBD | — | — |
| Reasoning | TBD | — | — |
| Planning | TBD | — | — |
| Architecture | TBD | — | — |
| Coding | TBD | — | — |
| Debugging | TBD | — | — |
| Hospitality | TBD | — | — |
| Business | TBD | — | — |
| Docker/Infra | TBD | — | — |
| OpenWebUI | TBD | — | — |
| NIM API | TBD | — | — |
| Memory/RAG | TBD | — | — |
| **System** | **TBD** | — | — |

---

## 8. Integration with REQ Traceability

Every benchmark maps back to a requirement:

| BM-ID | REQ-ID | Verifies |
|-------|--------|----------|
| BM-01 | REQ-AI-0005 | Parallel tool calls work |
| BM-02 | REQ-AI-0005, REQ-AI-0006 | Agentic RAG end-to-end |
| BM-03 | REQ-AI-0005 | MCP tool server integration |
| BM-09 | REQ-AI-0005 | qwen3_coder format compatibility |
| BM-10 | REQ-AI-0007 | Context window limit |
| BM-11 | REQ-AI-0004 | medium_effort Pipeline |
| BM-12 | REQ-AI-0003 | Temperature=1.0 quality |
| CODE-TC-* | REQ-AI-0002 | Parameter correctness |
| REAS-TC-* | REQ-AI-0004 | Reasoning mode control |
| MEM-TC-* | REQ-AI-0006 | RAG + embeddings |

---

*AI-0004 v2.0.0 — Upgraded from skeleton to full engineering framework 2026-07-20*
