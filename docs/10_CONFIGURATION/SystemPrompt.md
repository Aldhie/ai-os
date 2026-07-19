# System Prompt

| Field | Value |
|-------|-------|
| **Title** | AI-OS System Prompt Specification |
| **Purpose** | Define, version, and maintain the master system prompt for AI-OS |
| **Scope** | System prompt design, injection strategy, version history |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | Persona.md, Parameters.md |
| **References** | prompts/nemotron-ultra/system.txt |

---

## Design Principles

1. **Clarity** — Instructions must be unambiguous and structured
2. **Brevity** — Under 1,000 tokens in production
3. **Persona consistency** — Tone and style defined in Persona.md must be enforced
4. **Task focus** — System prompt sets constraints, not domain-specific instructions
5. **Versioned** — Every change must increment the version and be logged below

---

## Current Version: v0.1.0

See raw prompt: `prompts/nemotron-ultra/system.txt`

### Token Count

| Section | Estimated Tokens |
|---------|------------------|
| Identity & Persona | ~150 |
| Behavioral Rules | ~200 |
| Output Format Rules | ~150 |
| Tool Use Policy | ~100 |
| **Total** | **~600** |

---

## Vers