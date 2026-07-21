# Runtime Decision Engine

> **Layer**: Runtime Orchestration  
> **Responsibility**: Define when each runtime component activates, its cost, and its skip conditions  
> **Version**: 1.0.0 | **Date**: 2026-07-21

---

## Why This Engine Exists

Every runtime component (Planner, Memory, Knowledge, Tools, Reflection, Critic, Reasoning) has a latency cost and a token cost. Activating all of them for every request would consume the 32 RPM free tier limit within minutes of normal use. This engine defines the minimum set of components for each task class, preserving quality while respecting operational constraints.

---

## Decision Matrix

| Component | Trigger | Priority | Skip Condition | Latency Budget | Token Budget | Expected Benefit | Expected Cost |
|-----------|---------|----------|---------------|----------------|-------------|-----------------|---------------|
| **Planner** | Task has >3 sequential steps OR explicit "plan this" | HIGH | Greeting, simple fact, single-step task | +1-2s | 300-500 | Reduces implementation errors by 40% on complex tasks | 1 extra NIM call |
| **Memory** | User references prior context OR task is user-specific | HIGH | New topic with no user context dependency | +0.5s | 200-500 | Personalizes response, avoids re-asking known facts | Memory API call |
| **Knowledge** | Query requires domain-specific or document-grounded facts | HIGH | Greeting, pure reasoning task, code generation from scratch | +0.7s | 500-2000 | Grounds answer in verified documents | RAG API call |
| **Tools** | Explicit task requires external data or action | MEDIUM | Any task answerable from model knowledge | +0.5-2s per tool | 0 (tool call cost) | Enables real-time or repository-specific answers | RPM consumption |
| **Reflection** | High-stakes output: architecture, production code, strategy | MEDIUM | Simple tasks, conversational turns | +2-4s | 400-800 | Catches ~30% of errors before output | Adds one reasoning pass |
| **Critic** | Architecture decisions, security analysis, code review | LOW | Anything below architecture/security complexity | +1-3s | 300-600 | Surfaces failure modes and edge cases | Adds critique pass |
| **Reasoning** | Any non-trivial analytical task | AUTO | Greeting, simple fact | Scales with budget | Thinking tokens | Core quality driver for complex tasks | Token cost + latency |

---

## Component-Level Policy

### Planner

```yaml
trigger:
  - task_class: [architecture, research, planning, complex_analysis]
  - signal: message contains "plan", "steps", "how do I", "roadmap", "phase"
  - step_count_estimate: > 3

priority: HIGH

required_input:
  - task description
  - constraints (if any)
  - goal state

skip_condition:
  - greeting
  - simple_fact
  - single_step_task
  - user says "just do it" or "don't plan, implement"

failure_strategy:
  - if planner produces incoherent output: fall back to direct implementation
  - if plan has circular dependencies: flag to user before proceeding

latency_budget: 2s
token_budget: 500
expected_benefit: "Reduces multi-step implementation errors by ~40%"
expected_cost: "1 additional reasoning pass; 2s latency"
```

### Memory

```yaml
trigger:
  - user references "we", "our", "last time", "as I mentioned", "remember"
  - task is user-specific (preferences, project, team, history)
  - user profile has active memory entries

priority: HIGH

required_input:
  - user_id
  - query_embedding

skip_condition:
  - greeting with no user-specific content
  - clearly general knowledge question
  - user says "ignore memory" or "fresh start"

failure_strategy:
  - memory API timeout: proceed without memory, note gap
  - no relevant entries: proceed without injection
  - conflict with current message: defer to current message

latency_budget: 0.5s
token_budget: 500
expected_benefit: "Eliminates need to re-establish context; enables personalization"
expected_cost: "0.5s; 1 memory API call; ~300 tokens context injection"
```

### Knowledge (RAG)

```yaml
trigger:
  - task requires domain-specific facts
  - task references internal documentation or policies
  - task requires code from a specific codebase or library
  - task involves procedures, specifications, or versioned content

priority: HIGH

required_input:
  - query
  - knowledge_collection_id

skip_condition:
  - greeting
  - pure mathematical reasoning
  - code generation from well-known open source libraries (model knowledge sufficient)
  - user says "no need to look it up"

failure_strategy:
  - RAG returns 0 chunks: proceed from model knowledge, flag
  - RAG returns low-confidence chunks (< 0.6): use but caveat
  - RAG timeout: proceed from model knowledge

latency_budget: 0.7s
token_budget: 2000
expected_benefit: "Document-grounded answers; reduces hallucination on specific facts"
expected_cost: "0.7s; RAG API call; up to 2000 tokens context"
```

### Reflection

```yaml
trigger:
  - task_class: [architecture, production_code, strategy, security]
  - output will be used in production or consequential decisions
  - output length > 500 tokens

priority: MEDIUM

required_input:
  - draft response
  - original task

skip_condition:
  - task_class: [greeting, simple_fact, casual_chat]
  - user says "quick answer" or "tldr"
  - output < 200 tokens

failure_strategy:
  - if reflection produces contradictory suggestion: surface both and let user decide
  - if reflection finds critical error: revise response before output

latency_budget: 3s
token_budget: 600
expected_benefit: "Catches ~30% of factual/logical errors before output"
expected_cost: "3s additional latency; 600 thinking tokens"
```

### Critic

```yaml
trigger:
  - task_class: [architecture, security_analysis, code_review]
  - user explicitly asks for critique or red-teaming
  - output involves irreversible decisions (deploy, delete, schema change)

priority: LOW

required_input:
  - response draft
  - architecture/design artifact

skip_condition:
  - all tasks below architecture/security complexity threshold
  - time-sensitive requests (user signals urgency)
  - free tier RPM nearing limit (> 28 RPM)

failure_strategy:
  - critic finds no issues: output "No critical issues found in this design"
  - critic produces false positives: present as "potential concern" not "definite error"

latency_budget: 2s
token_budget: 500
expected_benefit: "Surfaces failure modes; prevents architectural mistakes"
expected_cost: "2s; 500 thinking tokens; counts toward RPM if external call"
```

---

## Activation Table by Task Class

| Task Class | Planner | Memory | Knowledge | Reflection | Critic | Thinking Budget |
|------------|---------|--------|-----------|------------|--------|-----------------|
| Greeting | ✕ | ✕ | ✕ | ✕ | ✕ | 0 |
| Simple fact | ✕ | ✕ | ✕ | ✕ | ✕ | 0 |
| Casual chat | ✕ | ✓ | ✕ | ✕ | ✕ | 1,000 |
| Explanation | ✕ | ✓ | ✓ | ✕ | ✕ | 4,000 |
| Business analysis | ✕ | ✓ | ✓ | ✓ | ✕ | 8,000 |
| Research | ✓ | ✓ | ✓ | ✓ | ✕ | 10,000 |
| Architecture | ✓ | ✓ | ✓ | ✓ | ✓ | 16,000 |
| Coding | ✕ | ✓ | ✓ | ✓ | ✕ | 8,000 |
| Debugging | ✕ | ✓ | ✓ | ✓ | ✓ | 10,000 |
| Security | ✕ | ✓ | ✓ | ✓ | ✓ | 14,000 |
| Planning | ✓ | ✓ | ✓ | ✓ | ✕ | 10,000 |

---

*File: runtime_decision_engine.md | Version: 1.0.0 | Last updated: 2026-07-21*
