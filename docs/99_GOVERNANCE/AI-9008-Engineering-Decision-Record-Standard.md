# AI-9008: Engineering Decision Record Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9008 |
| **Title** | Engineering Decision Record (EDR) Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All engineering decisions in `Aldhie/ai-os` |
| **Cross-References** | [AI-9007](AI-9007-Architecture-Principles.md) · [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) · [AI-9001](AI-9001-Documentation-Standard.md) |

---

## 1. Purpose

An Engineering Decision Record (EDR) documents WHY a decision was made, not just WHAT was decided. This repository distinguishes between Architecture Decision Records (ADRs — system-level) and Engineering Decision Records (EDRs — implementation-level).

---

## 2. When to Write an EDR

Write an EDR when:
- A configuration value is chosen over alternatives
- A feature is explicitly disabled (and why)
- A workaround is used instead of the ideal solution
- A standard is adopted or rejected
- A benchmark result changes a previous decision

Do NOT write an EDR for:
- Routine document updates
- Typo fixes
- Adding benchmarks (those go in EXP documents)

---

## 3. EDR Template

```markdown
## EDR-xxxx: <Title>

| Field | Value |
|-------|-------|
| **EDR ID** | EDR-xxxx |
| **Status** | Proposed / Accepted / Superseded / Rejected |
| **Date** | YYYY-MM-DD |
| **Deciders** | <GitHub usernames> |
| **Supersedes** | EDR-xxxx (if applicable) |
| **Superseded by** | EDR-xxxx (if applicable) |

### Context
<What situation prompted this decision? What constraints exist?>

### Decision
<What was decided, stated precisely>

### Rationale
<Why this option over alternatives — cite evidence>

### Alternatives Considered
| Option | Reason Rejected |
|--------|-----------------|
| Option A | ... |
| Option B | ... |

### Consequences
- Positive: ...
- Negative: ...
- Risk: ...

### Verification
<How will we know this decision is correct? Link to EXP or BM.>

### References
<Official docs, experiments, benchmarks>
```

---

## 4. Existing Engineering Decisions (Registered)

| EDR ID | Title | Status | Date |
|--------|-------|--------|------|
| EDR-0001 | Remove `top_k` from parameters.json | Accepted | 2026-07-20 |
| EDR-0002 | Remove `repetition_penalty` from parameters.json | Accepted | 2026-07-20 |
| EDR-0003 | Use `/think` system prompt instead of `extra_body` for basic reasoning toggle | Accepted | 2026-07-20 |
| EDR-0004 | Set `temperature: 1.0` per official NVIDIA docs | Accepted | 2026-07-20 |
| EDR-0005 | Configure separate embedding provider for RAG | Accepted | 2026-07-20 |
| EDR-0006 | Defer function calling enablement pending BM-09 | Proposed | 2026-07-20 |
| EDR-0007 | Use Open WebUI Pipeline for `extra_body` injection | Accepted | 2026-07-20 |
| EDR-0008 | Set default context budget to 256K tokens | Accepted | 2026-07-20 |

---

## 5. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — 8 founding EDRs registered |
