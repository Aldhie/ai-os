# System Prompt Specification

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | SystemPrompt.md |
| **Version** | 0.1.0-draft |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the system prompt for the AI OS powered by Nemotron 3 Ultra 550B. The system prompt is the primary mechanism for configuring the model's persona, behavior, capabilities, and constraints.

---

## Scope

- System prompt design principles
- Versioned system prompt content
- Prompt engineering guidelines
- Token budget for system prompt

---

## Dependencies

- `docs/10_CONFIGURATION/Persona.md` — persona definition
- `docs/20_RUNTIME/Planner.md` — planning instructions
- `docs/20_RUNTIME/Reflection.md` — reflection instructions
- `prompts/nemotron-ultra/system.txt` — raw prompt file

---

## References

- [Open WebUI System Prompt Docs](https://docs.openwebui.com/)
- [Nemotron System Prompt Best Practices](https://docs.nvidia.com/nim/)

---

## Design Principles

1. **Clarity** — Instructions must be unambiguous
2. **Conciseness** — Minimize token usage while maximizing guidance
3. **Modularity** — Separate concerns: persona, behavior, tools, memory
4. **Safety** — Include explicit safety and refusal instructions
5. **Versioning** — Every prompt change gets a version bump

---

## System Prompt Structure

```
[IDENTITY]
Who the assistant is.

[CAPABILITIES]
What the assistant can do.

[BEHAVIOR]
How the assistant should behave.

[MEMORY]
How to use and reference memory.

[TOOLS]
How and when to use available tools.

[CONSTRAINTS]
What the assistant must not do.

[FORMAT]
Output formatting requirements.
```

---

## Current System Prompt (v0.1.0-draft)

See `prompts/nemotron-ultra/system.txt` for the current working prompt.

---

## Prompt Change Log

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0-draft | 2026-07-20 | Initial draft |

---

## TODO

- [ ] Write initial system prompt v0.1.0
- [ ] Test system prompt with benchmark cases
- [ ] Define persona section
- [ ] Add tool use instructions
- [ ] Add memory recall instructions
- [ ] Evaluate token count vs. performance trade-off
