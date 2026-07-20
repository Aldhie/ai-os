# Workflow Runtime

> **Version**: 1.0.0
> **Module**: Planner / Reflection / Critic
> **Spec Ref**: AI-0001-Part2 §3 (Planner), £7 (Reflection), £8 (Critic)

---

## Complete Runtime Workflow

```
User Message
    │
    ▼
[① GREETING / SESSION INIT]
    │
    ▼
[② INTENT DETECTION]
    │
    ▼
[③ PLANNER]          → (skip if simple query)
    │
    ▼
[④ MEMORY DECISION]  → Load or skip?
    │
    ▼
[⑤ KNOWLEDGE DECISION] → RAG or skip?
    │
    ▼
[⑥ TOOL DECISION]    → Invoke or skip?
    │
    ▼
[⑦ REASONING]        → thinking budget allocated
    │
    ▼
[⑧ CRITIC]           → (skip if Mode 0)
    │
    ▼
[⑨ REFLECTION]       → (skip if Mode 0)
    │
    ▼
[⑩ RESPONSE]
```

---

## Stage 1 — Greeting / Session Init

| Attribute | Value |
|-----------|-------|
| Trigger | New conversation |
| Input | First user message |
| Output | Loaded session context (memory, profile) |
| Skip Condition | Mid-conversation (never skipped for first turn) |
| Failure Strategy | Proceed with defaults if memory unavailable |
| Latency Budget | <500ms |
| Token Budget | 0 (no LLM call) |

**Actions**:
1. Detect language
2. Detect domain
3. Detect expertise level
4. Load memory (per memory_loading_strategy.md)
5. Select profile (per profile configs)
6. Initialize session token counter

---

## Stage 2 — Intent Detection

| Attribute | Value |
|-----------|-------|
| Trigger | Every user message |
| Input | User message text |
| Output | Intent class, complexity score, thinking mode |
| Skip Condition | None (always runs) |
| Failure Strategy | Default to `general` intent |
| Latency Budget | <200ms (local classification) |
| Token Budget | 0 (rule-based classification, no LLM call) |

**Intent Classes**:
- `factual` → Mode 0, no tools
- `technical` → Mode 1, possible RAG
- `coding` → Mode 1-2, coding profile
- `planning` → Mode 1-2, planner activated
- `creative` → Mode 1, creative profile
- `analysis` → Mode 1-2, analysis profile
- `general` → Mode 0-1, discussion profile

---

## Stage 3 — Planner

| Attribute | Value |
|-----------|-------|
| Trigger | Intent = planning/architecture/complex coding |
| Input | User goal, available context |
| Output | Step-by-step plan with decision points |
| Skip Condition | Intent = factual OR general |
| Failure Strategy | Skip plan; respond directly |
| Latency Budget | +5-10s |
| Token Budget | 2,000 (plan generation) |

**Plan Output Format**:
```
Goal: [user goal]
Plan:
  1. [step] → [output]
  2. [step] → [output]
  Decision: [what determines if step 3 is needed?]
  3. [step] → [output]
Blockers: [any unknowns]
```

---

## Stage 4 — Memory Decision

| Attribute | Value |
|-----------|-------|
| Trigger | After intent classification |
| Input | Intent class, user_id, session state |
| Output | Memory items injected (or null) |
| Skip Condition | Intent = factual; no user_id; token budget exhausted |
| Failure Strategy | Proceed without memory |
| Latency Budget | <300ms |
| Token Budget | ≤500 injected tokens |

Ref: `memory_loading_strategy.md`, `memory_priority.md`

---

## Stage 5 — Knowledge Decision

| Attribute | Value |
|-----------|-------|
| Trigger | After memory load |
| Input | Intent class, profile, query |
| Output | Knowledge chunks injected (or null) |
| Skip Condition | RAG disabled in profile; no relevant knowledge base |
| Failure Strategy | Fall back per `knowledge_failover.md` |
| Latency Budget | <1s (retrieval) |
| Token Budget | ≤4,000 injected tokens |

Ref: `knowledge_loading.md`, `knowledge_ranking.md`

---

## Stage 6 — Tool Decision

| Attribute | Value |
|-----------|-------|
| Trigger | After knowledge injection |
| Input | Intent, context, profile tool config |
| Output | Tool results or null |
| Skip Condition | No tool justified (see tool_routing.md) |
| Failure Strategy | Fall back per `tool_failover.md` |
| Latency Budget | 2-30s depending on tool |
| Token Budget | Tool result: ≤1,000 tokens injected |

---

## Stage 7 — Reasoning

| Attribute | Value |
|-----------|-------|
| Trigger | Every message |
| Input | Full context (system + memory + knowledge + tools + conversation) |
| Output | Raw reasoning output + draft response |
| Skip Condition | None (always runs, even if budget_tokens=0) |
| Failure Strategy | Reduce thinking budget; deliver response anyway |
| Latency Budget | 2s (Mode 0) to 90s (Mode 2) |
| Token Budget | 0–32,000 thinking + 2,000–8,000 response |

Ref: `reasoning_policy.md`, `thinking_policy.md`

---

## Stage 8 — Critic

| Attribute | Value |
|-----------|-------|
| Trigger | After reasoning, before delivery |
| Input | Draft response |
| Output | Validated or revised response |
| Skip Condition | Mode 0; response < 100 tokens; conversational reply |
| Failure Strategy | Deliver draft with uncertainty flag |
| Latency Budget | +2-5s |
| Token Budget | 1,000 (critique pass) |

**Critic Checks**:
- Factual accuracy
- Completeness
- Hallucination scan
- Code correctness (if applicable)
- Signal-to-noise ratio

Ref: `quality_policy.md`

---

## Stage 9 — Reflection

| Attribute | Value |
|-----------|-------|
| Trigger | After critic, for complex/planning responses |
| Input | Validated response, original goal |
| Output | Self-assessment + potential follow-up actions |
| Skip Condition | Mode 0; simple Q&A; conversational |
| Failure Strategy | Skip reflection; deliver critic output |
| Latency Budget | +2-3s |
| Token Budget | 500 (reflection note) |

**Reflection Questions**:
- Did I fully address the user's goal?
- Are there follow-up steps the user needs?
- Should I proactively offer something they didn't ask for?

---

## Stage 10 — Response

| Attribute | Value |
|-----------|-------|
| Trigger | Always (final stage) |
| Input | Post-critic, post-reflection output |
| Output | Delivered response to user |
| Skip Condition | None |
| Failure Strategy | Deliver partial response with explicit failure note |
| Latency Budget | Streaming; first token < 3s |
| Token Budget | Per profile max_tokens |

Ref: `response_policy.md`
