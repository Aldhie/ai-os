# Context Resolution Policy

> **Status**: RUNTIME | **Version**: 1.0.0 | **Owner**: Chief AI Systems Architect

---

## Policy Statement

Context is a finite resource. Every token loaded into context costs latency and reduces space for the answer. This policy defines what gets loaded, when, and in what order.

**Core principle**: Load the minimum context necessary to produce a maximally correct answer.

---

## Context Loading Decision Tree

```
Incoming message
      │
      ├── Is this a greeting or simple 1-turn question?
      │       └── YES → SKIP: memory, RAG, planner, critic, reflection
      │                    LOAD: system prompt only
      │
      ├── Is this a factual recall question about the user?
      │       └── YES → LOAD: memory retrieval
      │                    SKIP: RAG (unless topic-specific), planner, critic
      │
      ├── Is this a domain knowledge question?
      │       └── YES → LOAD: RAG (knowledge base)
      │                    SKIP: planner, reflection (unless answer is long)
      │
      ├── Is this a multi-step task or architecture/design request?
      │       └── YES → LOAD: memory, knowledge, planner, reflection
      │                    MAYBE: critic (if output is consequential)
      │
      └── Is this a continuation of an ongoing conversation?
              └── YES → LOAD: chat history (compressed), memory
                             SKIP: RAG unless topic shifts
```

---

## Loading Decisions Table

| Trigger | Chat History | Memory | RAG | Planner | Critic | Reflection |
|---------|-------------|--------|-----|---------|--------|------------|
| Greeting | No | No | No | No | No | No |
| Simple fact | No | No | No | No | No | No |
| User preference query | Yes (last 3) | Yes | No | No | No | No |
| Domain knowledge query | Yes (last 3) | Yes | Yes | No | No | No |
| Complex analysis | Yes (last 5) | Yes | Yes | Yes | No | Yes |
| Architecture design | Yes (last 5) | Yes | Yes | Yes | Yes | Yes |
| Creative task | Yes (last 3) | Yes | No | Yes | No | No |
| Debugging | Yes (last 5) | Yes | Yes | No | Yes | No |

---

*File: runtime/openwebui/context/resolution_policy.md | Last updated: 2026-07-20*
