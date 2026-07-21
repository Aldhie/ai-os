# Runtime Decision Engine
> **Role**: WHICH runtime components activate per request | **Version**: 1.0.0

---

## Component Registry

Seven runtime components are available. Each has a cost and a benefit. The engine activates only what a request requires.

```
Components: Planner | Memory | Knowledge | Tools | Reflection | Critic | Reasoning
```

---

## Component: Planner

| Attribute | Value |
|-----------|-------|
| **Trigger** | Task requires > 3 sequential steps; user asks for roadmap/plan/design |
| **Priority** | 3 (after Memory and Knowledge are loaded) |
| **Required Input** | Goal statement, known constraints |
| **Skip Condition** | Greeting, simple fact, single-step request, casual chat |
| **Failure Strategy** | If planner output is incoherent: proceed without it; note limitation |
| **Latency Budget** | +2s |
| **Token Budget** | 800 tokens output |
| **Expected Benefit** | Structured decomposition; prevents missed dependencies |
| **Expected Cost** | 800 tokens context; additional reasoning overhead |

---

## Component: Memory

| Attribute | Value |
|-----------|-------|
| **Trigger** | User preference question; continuation of known topic; personalized recommendation |
| **Priority** | 1 (loaded before Knowledge and Planner) |
| **Required Input** | User ID; query embedding for retrieval |
| **Skip Condition** | Greeting; general knowledge question; first turn with no established context |
| **Failure Strategy** | If memory unavailable: proceed without it; do not fail the request |
| **Latency Budget** | +0.5s (cached: +0ms) |
| **Token Budget** | 2,000 tokens |
| **Expected Benefit** | Personalization; continuity across sessions |
| **Expected Cost** | 2,000 tokens context; retrieval latency |

---

## Component: Knowledge (RAG)

| Attribute | Value |
|-----------|-------|
| **Trigger** | Domain-specific question; specific library/API question; user says "check the docs" |
| **Priority** | 2 (after Memory, before Planner) |
| **Required Input** | Query; knowledge collection ID |
| **Skip Condition** | Greeting; general question answerable from model reasoning; no relevant collection |
| **Failure Strategy** | If RAG unavailable: continue with model knowledge + flag `[verify with docs]` |
| **Latency Budget** | +0.7s (cached: +0ms) |
| **Token Budget** | 4,000 tokens (standard), 8,000 tokens (deep) |
| **Expected Benefit** | Grounded, current, domain-accurate answers |
| **Expected Cost** | 4,000–8,000 tokens context; retrieval latency |

---

## Component: Tools

| Attribute | Value |
|-----------|-------|
| **Trigger** | Request requires external data (repo, web, memory write), calculation, or file access |
| **Priority** | 4 (after context loading) |
| **Required Input** | Tool definition in context; tool-specific parameters |
| **Skip Condition** | All required information is available in context or model reasoning |
| **Failure Strategy** | If tool fails: note the failure; continue with available data; do not retry silently |
| **Latency Budget** | +1–3s per tool (depends on tool) |
| **Token Budget** | Tool definitions: 500 tokens; results: varies |
| **Expected Benefit** | Real-time data; user-specific repo access; persistent memory writes |
| **Expected Cost** | Latency; RPM consumption (each tool call may trigger a NIM call) |

---

## Component: Reflection

| Attribute | Value |
|-----------|-------|
| **Trigger** | Architecture design; complex code; research synthesis; business recommendation |
| **Priority** | 6 (after draft response is generated) |
| **Required Input** | Draft response |
| **Skip Condition** | Simple questions; explanations; casual conversation; greetings |
| **Failure Strategy** | If reflection loop produces no improvement: use original draft |
| **Latency Budget** | +3–8s |
| **Token Budget** | 500 tokens reflection output |
| **Expected Benefit** | Catches logical errors, missed requirements, format issues |
| **Expected Cost** | Additional latency; token overhead |

---

## Component: Critic

| Attribute | Value |
|-----------|-------|
| **Trigger** | Architecture decisions; security analysis; business strategy; consequential recommendations |
| **Priority** | 7 (after reflection) |
| **Required Input** | Draft response + reflection output |
| **Skip Condition** | Explanation; code generation; casual; anything non-consequential |
| **Failure Strategy** | If critic cannot identify a meaningful challenge: skip it |
| **Latency Budget** | +2–5s |
| **Token Budget** | 300 tokens critic output |
| **Expected Benefit** | Identifies weakest assumption; flags potential failure modes |
| **Expected Cost** | Latency; token overhead |

---

## Component: Reasoning (Thinking Tokens)

| Attribute | Value |
|-----------|-------|
| **Trigger** | Any task with thinking budget > 0 (see thinking.md) |
| **Priority** | 5 (concurrent with response generation via extended thinking) |
| **Required Input** | Task classification; thinking budget |
| **Skip Condition** | Greeting; simple fact; when `/nothink` or `/fast` is set |
| **Failure Strategy** | If thinking budget exhausted mid-response: complete with available reasoning |
| **Latency Budget** | Proportional to budget: ~0.5ms/token |
| **Token Budget** | 0–20,000 thinking tokens (see thinking.md) |
| **Expected Benefit** | Improved accuracy; better code logic; stronger architecture reasoning |
| **Expected Cost** | Latency; token quota consumption |

---

## Decision Matrix by Task Class

| Task | Planner | Memory | Knowledge | Tools | Reflection | Critic | Thinking |
|------|---------|--------|-----------|-------|------------|--------|----------|
| Greeting | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | None |
| Simple fact | ✗ | ✗ | ✗ | ✗ | ✗ | ✗ | None |
| Explanation | ✗ | ✓ | ✓ | ✗ | ✗ | ✗ | Light |
| Business | ✗ | ✓ | ✓ | ✗ | ✓ | ✓ | Standard |
| Architecture | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | Deep |
| Coding | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | Standard |
| Debugging | ✗ | ✓ | ✓ | ✓ | ✗ | ✓ | Deep |
| Security | ✗ | ✓ | ✓ | ✓ | ✓ | ✓ | Deep |
| Research | ✓ | ✓ | ✓ | ✓ | ✓ | ✗ | Standard |
| Planning | ✓ | ✓ | ✓ | ✗ | ✓ | ✗ | Standard |
| Creative | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | Light |
| Casual | ✗ | ✓ | ✗ | ✗ | ✗ | ✗ | Light |

---

*File: runtime/openwebui/model/decision_engine.md | Last updated: 2026-07-21*
