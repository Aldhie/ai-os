# Memory Policy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | MemoryPolicy.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the memory policy for the AI OS. It governs how the assistant creates, retrieves, updates, and expires memories across conversation sessions.

---

## Scope

- Types of memory supported
- Memory creation triggers
- Memory retrieval strategy
- Memory retention and expiry
- Privacy and security considerations

---

## Dependencies

- `docs/10_CONFIGURATION/SystemPrompt.md` — memory instructions in system prompt
- `docs/20_RUNTIME/Reflection.md` — memory extraction from reflections
- Open WebUI Memory Module

---

## References

- [Open WebUI Memory Documentation](https://docs.openwebui.com/features/memories/)

---

## Memory Types

| Type | Description | Retention |
|------|-------------|----------|
| **Ephemeral** | Within-session context only | Session end |
| **Short-term** | Recent interactions, last 7 days | 7 days |
| **Long-term** | User preferences, goals, facts | Indefinite |
| **Procedural** | How the user prefers tasks done | Indefinite |

---

## Memory Creation Policy

The assistant SHOULD create a memory entry when:

- The user states a preference or constraint (e.g., "I prefer concise answers")
- The user shares a personal fact relevant to future interactions
- A significant goal or project is initiated
- The user corrects the assistant's behavior

The assistant MUST NOT create memory entries for:

- Sensitive personal data (passwords, financial data)
- One-off requests with no future relevance
- Information the user has not consented to store

---

## Memory Retrieval Policy

- Retrieve relevant memories at the start of each conversation
- Inject retrieved memories into the context window
- Prioritize recent and high-relevance memories
- Do not inject memories that are outdated or contradicted

---

## Memory Update and Expiry

- Update existing memory entries when new information supersedes old
- Do not create duplicates — update in place
- Mark memories as expired after the defined retention period
- User can explicitly delete memories at any time

---

## TODO

- [ ] Define maximum memory entries per user
- [ ] Define memory relevance scoring algorithm
- [ ] Implement memory injection format in system prompt
- [ ] Define privacy controls and user consent mechanism
- [ ] Test memory recall accuracy with benchmark cases
