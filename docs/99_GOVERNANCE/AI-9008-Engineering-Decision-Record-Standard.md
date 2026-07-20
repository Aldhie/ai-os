# AI-9008: Engineering Decision Record Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9008 |
| **Title** | Engineering Decision Record Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9001 — Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9007 — Architecture Principles](AI-9007-Architecture-Principles.md)
- [AI-0006 — Architecture Decision Record](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md)

---

## 1. Purpose

An Engineering Decision Record (EDR) captures a significant engineering decision: what was decided, why it was decided, what alternatives were considered, and what consequences follow. EDRs are immutable once Active — they are never edited, only superseded.

---

## 2. Mandatory EDR Template

```markdown
# ADR-[NUMBER]: [Title]

## Metadata
| Field | Value |
|-------|-------|
| ADR ID | ADR-[NUMBER] |
| Date | [ISO 8601] |
| Status | Proposed / Accepted / Superseded / Deprecated |
| Deciders | [Names] |
| Technical Area | [API / Config / Prompt / Architecture / ...] |

## Context
[What situation forced this decision? Include relevant constraints.]

## Decision
[What was decided, in a single clear sentence.]

## Alternatives Considered
| Option | Pros | Cons | Why Rejected |
|--------|------|------|---------------|

## Rationale
[Why this option was selected over alternatives. Must reference evidence.]

## Consequences
### Positive
- [Benefit 1]

### Negative / Tradeoffs
- [Tradeoff 1]

### Neutral
- [Side effect 1]

## Related Documents
- [Link to relevant AI-xxxx, EXP-xxxx, TC-xxxx]

## Superseded By
[ADR-xxx — Title] or N/A
```

---

## 3. When to Create an EDR

Create an EDR when:
- A new tool, model, or infrastructure component is adopted
- A configuration is changed for a non-obvious reason
- An audit finding results in a breaking change
- Two valid approaches were considered and one was selected
- A principle from AI-9007 is violated (requires explicit justification)

**Do not** create an EDR for:
- Typo fixes
- Pure documentation improvements
- Version bumps without behavioral change

---

## 4. EDR Immutability Rule

Once an EDR has Status: `Accepted`, its content must not be modified. If the decision changes:
1. Create a new ADR
2. Set the old ADR Status to `Superseded`
3. Link `Superseded By` to the new ADR

This preserves the full decision history and makes the evolution of engineering thinking traceable.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial EDR standard |
