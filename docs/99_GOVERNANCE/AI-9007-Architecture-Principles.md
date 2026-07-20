# AI-9007: Architecture Principles

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9007 |
| **Title** | Architecture Principles |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Primary model spec |
| [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) | ADR records |
| [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) | ADR standard |

---

## 1. Core Architecture Philosophy

The `ai-os` system is built on **four non-negotiable principles**:

### P1: Separation of Concerns
Every layer has exactly one responsibility:
- **Model layer** (NIM): Token generation only
- **Inference layer** (parameters): Control generation quality
- **Integration layer** (Open WebUI): User interaction, tool execution, memory
- **Knowledge layer** (RAG): Domain context injection
- **Governance layer** (this repo): Engineering decisions and traceability

Violating this separation creates tight coupling that makes the system brittle to model upgrades.

### P2: Evidence-First Engineering
No engineering decision is made without a classification:
- `[FACT: Official Doc]` — directly from vendor documentation
- `[FACT: Benchmark]` — measured in our own benchmark suite
- `[FACT: Experiment]` — validated in controlled experiment
- `[HYPOTHESIS]` — reasonable belief awaiting validation
- `[ASSUMPTION]` — known unknown being tracked

Every `[HYPOTHESIS]` has a validation plan. Every `[ASSUMPTION]` has a risk mitigation.

### P3: Traceability by Default
Every configuration value traces to:
1. A requirement (REQ-AI-XXXX)
2. An engineering decision (AI-0006 ADR)
3. An evidence source (Official Doc, Benchmark, or Experiment)

An undocumented configuration value is a liability, not an asset.

### P4: Graceful Degradation
The system is designed to fail predictably:
- If NIM returns an unsupported parameter error → log, alert, continue with defaults
- If embeddings endpoint is unavailable → fail with explicit error, not silent wrong behavior
- If tool calling fails → return error to user, do not silently ignore
- If context limit is exceeded → explicit truncation warning, not silent truncation

---

## 2. System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                        USER LAYER                           │
│  Browser / API Client / Automated Agent                     │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   OPEN WEBUI LAYER                          │
│  ┌─────────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐  │
│  │ Auth / RBAC │  │  Memory  │  │   RAG    │  │  Tools  │  │
│  └──────┬──────┘  └────┬─────┘  └────┬─────┘  └────┬────┘  │
│         └──────────────┴─────────────┴─────────────┘        │
│                              │                              │
│                    ┌─────────▼──────────┐                   │
│                    │  Pipeline Layer    │                   │
│                    │  (extra_body inj.) │                   │
│                    └─────────┬──────────┘                   │
└──────────────────────────────┼──────────────────────────────┘
                               │ HTTPS POST /v1/chat/completions
┌──────────────────────────────▼──────────────────────────────┐
│              NVIDIA NIM CLOUD LAYER                         │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  integrate.api.nvidia.com/v1                        │    │
│  │  Model: nvidia/nemotron-3-ultra-550b-a55b           │    │
│  │  Backend: vLLM / SGLang / TRT-LLM (NVIDIA-managed) │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Integration Architecture: Open WebUI × NIM

```
Open WebUI Request Pipeline:

User Input
    │
    ├─► Memory Retrieval (OW-side)
    ├─► RAG Document Retrieval (OW-side)
    ├─► Tool Pre-processing (OW-side)
    │
    ▼
Pipeline Filter (if configured)
    │
    ├─► Inject extra_body.chat_template_kwargs [REQUIRED for tools + reasoning]
    ├─► Validate parameters (remove top_k, repetition_penalty)
    ├─► Apply profile parameters
    │
    ▼
NIM API Call
    │
    ▼
NIM Response
    │
    ├─► Stream SSE chunks (if stream: true)
    ├─► Tool call execution (OW-side, if tool_calls in response)
    ├─► Memory save (OW-side)
    │
    ▼
User Display
```

---

## 4. Reasoning Architecture

Nemotron Ultra 550B operates in two distinct modes. [FACT: Official Doc]

```
Reasoning ON (/think):
  ┌─────────────────────────────────────────┐
  │  <think>                                │
  │    [Internal reasoning trace]           │  Hidden from user in standard UI
  │    [Multi-step analysis]                │
  │  </think>                               │
  │  [Final answer]                         │  Visible to user
  └─────────────────────────────────────────┘

Reasoning OFF (/nothink):
  ┌─────────────────────────────────────────┐
  │  [Direct answer, no reasoning trace]    │  Faster, cheaper
  └─────────────────────────────────────────┘
```

Token cost implication: reasoning traces consume tokens. [HYPOTHESIS: reasoning traces average 500-2000 tokens per complex query — needs EXP-0003 validation]

---

## 5. Decision Framework

When making an architectural decision:

```
1. IDENTIFY: What problem are we solving?
2. EVIDENCE: What do official docs say?
3. OPTIONS: What are the alternatives?
4. EVALUATE: What are the trade-offs?
5. DECIDE: Which option and why?
6. RECORD: ADR in AI-0006
7. VALIDATE: Benchmark or experiment assigned
8. REVIEW: Schedule for re-evaluation
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial architecture principles |
