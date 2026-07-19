# Memory Policy

| Field | Value |
|-------|-------|
| **Title** | Memory Policy |
| **Purpose** | Define rules for when and how the AI OS stores, retrieves, and manages long-term memory |
| **Scope** | Memory triggers, retention rules, privacy constraints, memory types |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | SystemPrompt.md, ToolPolicy.md |
| **References** | Open WebUI Memory Docs |

---

## 1. Memory Types

| Type | Description | Retention |
|------|-------------|----------|
| **Factual** | User preferences, facts about the user | Permanent |
| **Episodic** | Past conversations and events | 90 days |
| **Procedural** | How-to knowledge learned from user | Permanent |
| **Contextual** | Session-specific context | Session only |

---

## 2. Storage Triggers

Store a memory when:

- User states a preference explicitly ("I prefer...", "I always...", "I like...")
- User shares a persistent fact about themselves or their environment
- A decision is made that will affect future behavior
- User corrects the AI's behavior (negative feedback = learning event)

---

## 3. Retrieval Policy

- Always search memory at the start of a new session
- Search memory when context is ambiguous ("my project", "that document")
- Do not retrieve memory for purely factual/informational queries

---

## 4. Privacy Rules

- Do not store passwords, API keys, or credentials
- Do not store sensitive personal information without explicit user consent
- User can request memory deletion at any time
- Memory is scoped to the user's account only

---

## 5. Memory Format

```
Type: [factual|episodic|procedural]
Title: Short description (< 100 chars)
Content: Full memory content
Tags: [relevant tags]
Created: YYYY-MM-DD
Expires: YYYY-MM-DD or never
```

---

## TODO

- [ ] Implement memory search at session start
- [ ] Define memory namespace structure
- [ ] Test memory retrieval accuracy
- [ ] Create memory cleanup script
- [ ] Define consent flow for sensitive information
