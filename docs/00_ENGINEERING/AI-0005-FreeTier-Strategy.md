# AI-0005: NVIDIA NIM Free Tier Engineering Strategy
## Token Budget Management for Development Environments

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-0005 |
| **Version** | 2.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **REQ** | REQ-AI-0011 |

---

## Related Documents

- ↑ [AI-0002 NIM API Reference](./AI-0002-NVIDIA-NIM-API.md)
- ↑ [AI-0003 Compatibility Matrix](./AI-0003-OpenWebUI-Compatibility.md)
- ↑ [REQ-INDEX](./REQ-INDEX.md) REQ-AI-0011
- ↓ [EXP-0003 Thinking Token Cost](../05_EXPERIMENTS/EXP-0003-Thinking.md)

---

## 1. Purpose

NVIDIA NIM free tier has request and token limits. This document defines the engineering strategy to maximize development velocity while staying within those limits. Every design decision must trade off token cost vs capability gain.

---

## 2. Free Tier Limits

> **Note:** NVIDIA does not publicly publish exact free tier limits in documentation. The values below are based on community observations and practical experience.
> **[ASSUMPTION]** Exact limits may differ from actual. Verify via NIM dashboard.

| Resource | Estimated Limit | Confidence | Source |
|----------|----------------|------------|--------|
| Requests per minute (RPM) | 1–5 RPM | Low | Community observation |
| Tokens per minute (TPM) | 10,000–50,000 | Low | Community observation |
| Tokens per day | 100,000–1,000,000 | Low | Community observation |
| Context per request | 256K tokens | High | Official docs (default deployment) |
| Models available | All listed at build.nvidia.com | High | Official |

**Action (REQ-AI-0011):** Instrument OW analytics to measure actual limits empirically.

---

## 3. Token Cost Analysis

### 3.1 Per-Request Cost by Profile

| Profile | System Prompt | User Prompt | Thinking Trace | Output | Total Estimate |
|---------|--------------|-------------|----------------|--------|----------------|
| `general` (thinking OFF) | ~100 | ~200 | 0 | ~500 | ~800 |
| `reasoning` (thinking ON) | ~100 | ~200 | ~5,000–15,000 | ~1,000 | ~6,300–16,300 |
| `medium_effort` | ~100 | ~200 | ~1,000–4,000 | ~800 | ~2,100–5,100 |
| `code` (thinking ON) | ~100 | ~500 | ~5,000–15,000 | ~3,000 | ~8,600–18,600 |
| `rag` (RAG + thinking OFF) | ~100 | ~200+4,096 | 0 | ~800 | ~5,196 |
| `agent` (tool calls) | ~200 | ~300 | ~3,000 | ~500+tools | ~4,000–7,000 |

**Key Finding:** A single `reasoning` call can consume 16K+ tokens. At estimated 100K/day limit, that allows only ~6 reasoning calls per day.

### 3.2 Token Multiplier by Thinking Mode

| Mode | Token Multiplier | Use When |
|------|-----------------|----------|
| Thinking OFF | 1× (baseline) | Simple Q&A, summaries, generation |
| medium_effort | 3–7× | Complex problems where full thinking is overkill |
| Thinking ON | 8–20× | Hard math, complex debugging, multi-step reasoning |

**[ASSUMPTION]** Multipliers are estimated from model documentation and community reports. EXP-0003 will validate these empirically.

---

## 4. Free Tier Development Strategy

### 4.1 Profile Assignment Strategy

Rule: **Start with `general` profile. Escalate only when needed.**

```
Query Type                  → Profile
────────────────────────────────────────────────
"explain X"                 → general  (~800 tokens)
"summarize this"            → general  (~800 tokens)
"write a story about"       → creative (~800 tokens)
"debug this code"           → medium_effort (~3,000 tokens)
"implement this feature"    → code     (~12,000 tokens)
"design this system"        → reasoning (~12,000 tokens)
"prove this theorem"        → reasoning (~16,000 tokens)
```

### 4.2 Context Budget Discipline

**Rule:** Never send more context than the task requires.

```
Task: Simple Q&A → No RAG injection. Max context: 1,000 tokens.
Task: Document Q&A → RAG injection limited to 4,096 tokens.
Task: Code review → Send only relevant code sections. < 8,000 tokens.
Task: Architecture design → May use full context budget. < 32,000 tokens.
```

### 4.3 Development Session Budgeting

Estimated token budget per development session (general profile):

| Session Type | Requests | Tokens/Request | Session Total |
|-------------|----------|----------------|---------------|
| Quick exploration | 20 | 800 | 16,000 |
| Code development | 15 | 5,000 | 75,000 |
| Architecture design | 5 | 15,000 | 75,000 |
| Benchmark run (all 36 tests) | 36 | 3,000 avg | 108,000 |

**Implication:** Full benchmark run may exhaust daily free tier in one session.
**Mitigation:** Run benchmark categories incrementally across days.

---

## 5. Token Optimization Techniques

### 5.1 System Prompt Optimization

| Technique | Token Saving | Implementation |
|-----------|-------------|----------------|
| Use `/nothink` for non-reasoning tasks | 5,000–15,000/request | Set in profile system prompt |
| Minimize system prompt length | 50–200/request | Keep system prompts under 200 words |
| Avoid redundant instructions | 20–100/request | Audit system prompts |

### 5.2 History Management

| Technique | Token Saving | Implementation |
|-----------|-------------|----------------|
| Clear history for new topics | Full history size | New OW chat session |
| Summarize long histories | 50–80% reduction | Context summarization pipeline |
| Set history budget to 8,192 | Predictable cost | parameters.json |

### 5.3 RAG Optimization

| Technique | Token Saving | Implementation |
|-----------|-------------|----------------|
| Set RAG top_k=3 for short answers | 40–60% | capabilities.json |
| Use hybrid search → higher precision | Fewer chunks needed | capabilities.json |
| Increase chunk_size for denser context | Fewer chunks | capabilities.json |

---

## 6. Monitoring Strategy

### 6.1 OW Analytics Metrics to Monitor

| Metric | Warning Threshold | Action |
|--------|------------------|--------|
| Daily tokens used | >70% of limit | Switch to general profile only |
| Reasoning calls per day | >10 | Review necessity |
| Average tokens per request | >5,000 | Investigate high-cost sessions |
| Failed requests (429) | Any | Reduce RPM, check token budget |

### 6.2 Alert Response Protocol

```
70% daily budget consumed before 12:00 WIB:
  → Stop reasoning profile for rest of day
  → General profile only
  → No benchmark runs

429 Rate Limit error:
  → Wait 60 seconds
  → Retry with smaller context
  → If persistent: check account quota at build.nvidia.com

Quota exhausted (0% remaining):
  → Pause development until quota resets
  → Use Super 49B as fallback (smaller model, higher free tier quota)
  → Document what was blocked in dev log
```

---

## 7. Fallback Model Strategy

When Ultra 550B quota is exhausted:

| Fallback Model | Use Case | Context | Quota |
|----------------|----------|---------|-------|
| `nvidia/llama-3.1-nemotron-70b-instruct` | General tasks | 128K | Higher free tier |
| `nvidia/nemotron-3-super-49b-a33b` (hypothetical) | Complex reasoning | 128K | Higher free tier |
| Local Ollama model | No quota | Limited | Unlimited |

**Strategy:** Configure OW model fallback chain: Ultra 550B → 70B → Local.

---

## 8. Free Tier vs Paid Tier Decision

| Trigger | Decision |
|---------|----------|
| Daily development blocked by quota consistently | Upgrade to paid tier |
| Benchmark suite cannot complete in one day | Upgrade |
| Production use (any user other than developer) | Upgrade required |
| SLA required | Upgrade required |

---

*AI-0005 v2.0.0 — Upgraded from skeleton to full engineering strategy 2026-07-20*
