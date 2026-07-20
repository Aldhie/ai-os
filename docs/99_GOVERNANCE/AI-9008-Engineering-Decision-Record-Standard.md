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
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9001](AI-9001-Documentation-Standard.md) | Parent standard |
| [AI-9007](AI-9007-Architecture-Principles.md) | Principles that drive ADRs |
| [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) | ADR register |

---

## 1. Purpose

An Engineering Decision Record (EDR) documents **why** an engineering decision was made, not just **what** was decided. EDRs prevent the same debates from recurring and enable future engineers to understand the context of decisions.

**Engineering Principle:** The cost of re-litigating a past decision exceeds the cost of documenting it the first time.

---

## 2. When to Write an EDR

Write an EDR when:
- Choosing between two or more valid technical approaches
- Accepting a known limitation or risk
- Overturning a previous decision based on new evidence
- Making a decision that will be expensive to reverse
- Establishing a new default or policy

---

## 3. EDR Template

```markdown
## EDR-[XXXX]: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by EDR-XXXX
**Owner:** [username]

### Context

[What situation forced this decision? What were the constraints?]

### Decision

[What was decided, stated clearly and unambiguously]

### Options Considered

| Option | Pros | Cons | Evidence |
|--------|------|------|----------|
| Option A | | | |
| Option B | | | |

### Rationale

[Why this option over the others. Must reference evidence.]

### Consequences

**Positive:**
- [expected benefit 1]

**Negative / Trade-offs:**
- [expected cost or limitation 1]

**Risks:**
- [risk if decision proves wrong]

### Validation Plan

- Benchmark: [BM-XX or N/A]
- Experiment: [EXP-XX or N/A]
- Target Date: [YYYY-MM-DD]

### References

- [Official doc URL, paper, benchmark result]
```

---

## 4. EDR Lifecycle

```
Proposed → Accepted → (optionally) Deprecated
                              ↓
                      Superseded by EDR-XXXX
```

An EDR is never deleted. A superseded EDR is marked `Superseded by EDR-XXXX` and remains in the record as historical context.

---

## 5. EDR Quality Rules

| Rule | Requirement |
|------|-------------|
| Every decision has evidence | At least one `[FACT]` or explicit `[HYPOTHESIS]` |
| Options are evaluated | Minimum 2 options considered |
| Consequences are honest | Both positive AND negative consequences documented |
| Validation planned | Every `[HYPOTHESIS]` decision has a validation plan |
| Cross-referenced | Linked from the engineering spec it affects |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial EDR standard |
