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
| **Updated** | 2026-07-20 |

## Cross-References

- [AI-9007 Architecture Principles](AI-9007-Architecture-Principles.md)
- [AI-9001 Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-0006 Architecture Decision Record](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md)

---

## 1. Purpose

Defines the mandatory structure for Engineering Decision Records (EDRs) in this repository. Every significant engineering decision — parameter choice, architecture pattern, integration approach, tool selection — requires an EDR.

---

## 2. When to Write an EDR

An EDR is required when:

1. A configuration parameter is changed from default
2. A new external service or API is integrated
3. A previously used approach is abandoned
4. An architecture principle (AI-9007) is deviated from
5. A benchmark result contradicts previous assumptions
6. A security-relevant decision is made
7. A performance trade-off is accepted

An EDR is NOT required for:
- Typo fixes
- Formatting changes
- Adding documentation without changing behavior
- Running a benchmark (use EXP-xxxx instead)

---

## 3. EDR Template

EDRs are stored in `AI-0006-Architecture-Decision-Record.md` as numbered sections. Each EDR follows:

```markdown
### EDR-NNNN: [Decision Title]

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Superseded / Deprecated
**Decider:** [name]
**Supersedes:** [EDR-NNNN or None]

#### Context

[What situation or problem required a decision? What constraints existed?]

#### Decision

[What was decided? Be specific. Include exact parameter values, API choices, etc.]

#### Alternatives Considered

| Alternative | Reason Rejected |
|-------------|----------------|
| [Option A] | [Why not] |
| [Option B] | [Why not] |

#### Rationale

[Why was this decision made? What evidence supports it? Reference [FACT] tags.]

#### Consequences

**Positive:**
- [What improves]

**Negative:**
- [What gets worse or is lost]

**Risks:**
- [Known risks]

#### Verification

[How do we know this decision is correct? Which benchmark or experiment validates it?]

#### References

- [Official doc URL or experiment reference]
```

---

## 4. EDR Index Format

`AI-0006` must maintain an index table at the top:

```markdown
## EDR Index

| ID | Title | Status | Date | Decider |
|----|-------|--------|------|---------|
| EDR-0001 | Use temperature=1.0 not 0.6 | Accepted | 2026-07-20 | Aldhie |
| EDR-0002 | Remove top_k from parameters.json | Accepted | 2026-07-20 | Aldhie |
```

---

## 5. EDR Lifecycle

```
Proposed → Accepted → [Superseded]
         → Rejected
```

Superseded EDRs are NOT deleted. The superseding EDR references the old one.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
