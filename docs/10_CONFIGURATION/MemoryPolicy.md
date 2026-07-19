# Memory Policy

| Field | Value |
|---|---|
| **Title** | AI-OS Memory Policy |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Defines what the AI-OS should remember, for how long, and how memory is managed across sessions. Memory is a critical component of persistent, context-aware AI behavior.

---

## Scope

- Open WebUI memory feature
- Cross-session user context retention
- Applies to all user interactions

---

## Memory Categories

### 1. User Identity

**What:** Name, profession, location, language preference, timezone.

**Retention:** Permanent (until explicitly deleted).

**Example:**

```text
User prefers responses in Indonesian.
User is a software engineer based in Indonesia.
```

---

### 2. User Preferences

**What:** Communication style, response format, depth level, topic interests.

**Retention:** Permanent (updated on change).

**Example:**

```text
User prefers bullet-point summaries for technical topics.
User dislikes verbose preambles.
```

---

### 3. Project Context

**What:** Active projects, goals, current tasks, blockers.

**Retention:** Active project lifetime + 90 days.

**Example:**

```text
User is building an AI Operating System called AI-OS.
Current phase: Engineering documentation.
```

---

### 4. Conversation History

**What:** Recent conversation turns (last N exchanges).

**Retention:** Session-scoped + 7 days in memory.

**Pruning:** Summarize after 20 turns; keep summary + last 5 turns.

---

### 5. Factual Corrections

**What:** Facts the user has explicitly corrected.

**Retention:** Permanent.

**Example:**

```text
User corrected: The project uses NIM API, not local Ollama.
```

---

## Memory Rules

1. **Never assume** — Only store what is explicitly stated or confirmed.
2. **Never hallucinate memory** — Do not invent stored facts.
3. **Respect deletion requests** — Remove memory immediately when asked.
4. **Flag conflicts** — If new information conflicts with stored memory, ask for clarification.
5. **Privacy first** — Never store sensitive data (passwords, API keys, PII).

---

## Memory Injection Format

When injecting memory into system prompt:

```xml
<memory>
  <user_identity>Name: Aldhie. Language: Indonesian/English. Timezone: WIB (UTC+7).</user_identity>
  <preferences>Prefers concise answers. Bullet points for technical topics.</preferences>
  <project>Currently working on AI-OS: engineering repo for Nemotron Ultra + Open WebUI.</project>
</memory>
```

---

## Dependencies

- `docs/10_CONFIGURATION/SystemPrompt.md`
- Open WebUI Memory module

---

## References

- [Open WebUI Memory Docs](https://docs.openwebui.com/features/workspace/memory)

---

## TODO

- [ ] Implement memory injection in system prompt
- [ ] Build memory review script
- [ ] Define memory export format (JSON)
- [ ] Set up memory backup policy
- [ ] Test memory conflict resolution behavior
