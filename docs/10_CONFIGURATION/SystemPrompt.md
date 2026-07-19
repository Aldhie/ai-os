# System Prompt

| Field | Value |
|-------|-------|
| **Title** | AI OS System Prompt |
| **Purpose** | Define the master system prompt injected into every conversation with Nemotron Ultra |
| **Scope** | Identity, behavior, capability boundaries, tone, and safety guardrails |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Dependencies** | Persona.md, ToolPolicy.md, MemoryPolicy.md |
| **References** | AI-0001, Parameters.md |

---

## Design Principles

1. **Minimal footprint** — Under 2,000 tokens to preserve context budget
2. **Explicit identity** — Model must know who it is and what it does
3. **Clear boundaries** — What to do, what not to do
4. **Tool awareness** — Know which tools are available and when to use them
5. **Memory integration** — Reference and update memory when appropriate

---

## Prompt Structure

```
[IDENTITY]
[CAPABILITIES]
[BEHAVIOR RULES]
[TOOL USAGE POLICY]
[MEMORY POLICY]
[KNOWLEDGE POLICY]
[SAFETY GUARDRAILS]
[OUTPUT FORMAT]
```

---

## Current Prompt (v0.1.0 — Draft)

> Stored in: `prompts/nemotron-ultra/system.txt`

---

## Prompt Changelog

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 0.1.0 | 2026-07-20 | Initial draft template | Aldhie |

---

## Evaluation Criteria

A good system prompt should produce:

- [ ] Consistent persona across sessions
- [ ] Correct tool selection without over-calling
- [ ] Appropriate refusals for out-of-scope requests
- [ ] Concise, structured responses
- [ ] Memory usage without user prompting

---

## TODO

- [ ] Write v0.1 system prompt content
- [ ] Run against benchmark cases (BenchmarkCases.md)
- [ ] Optimize for token count
- [ ] Test persona consistency across 20+ turns
- [ ] Review safety guardrails with adversarial inputs
