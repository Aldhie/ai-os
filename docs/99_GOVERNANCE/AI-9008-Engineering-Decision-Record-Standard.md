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
| [AI-9007](AI-9007-Architecture-Principles.md) | Principles that EDRs must implement |
| [AI-0006](../00_ENGINEERING/AI-0006-Architecture-Decision-Record.md) | Active EDR log |
| [AI-9001](AI-9001-Documentation-Standard.md) | Documentation standard |

---

## 1. Purpose

This document defines the Engineering Decision Record (EDR) standard for the `ai-os` repository. An EDR is the authoritative record of a significant engineering decision: what was decided, why, what alternatives were considered, and what evidence supported the decision.

---

## 2. When to Write an EDR

Write an EDR when:

| Trigger | Example |
|---------|--------|
| A configuration value changes from default | temperature: 0.6 → 1.0 |
| A platform integration choice is made | Use Pipeline vs. system prompt for thinking control |
| A benchmark reveals an unexpected result | temperature=1.0 scores lower than 0.6 on factual Q&A |
| A previously-held assumption is invalidated | Memory injection at 50+ facts causes quality degradation |
| A new capability is adopted or rejected | Tool calling: adopt/reject for primary profile |

---

## 3. EDR Structure

All EDRs MUST use this structure (stored in AI-0006):

```markdown
### EDR-XXX: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed / Accepted / Superseded / Rejected
**Supersedes:** EDR-YYY (if applicable)

#### Context
[The situation and problem that required a decision. What was the constraint?]

#### Decision
[What was decided, in one clear sentence.]

#### Alternatives Considered
| Alternative | Reason Rejected |
|-------------|----------------|
| Option A | [reason] |
| Option B | [reason] |

#### Evidence
[FACT/HYPOTHESIS/ASSUMPTION labels required]
- [FACT: Benchmark] TC-XXXX score: ...
- [HYPOTHESIS] Expected that ... — pending EXP-XXXX

#### Consequences
| Consequence | Positive/Negative | Mitigated By |
|-------------|-------------------|--------------|
| ... | | |

#### Validation
[How will this decision be validated? Link to EXP or benchmark TC.]

#### Changelog
| Date | Change |
|------|--------|
| YYYY-MM-DD | Initial record |
```

---

## 4. EDR Numbering

| Range | Category |
|-------|----------|
| EDR-001 to EDR-099 | Model configuration decisions |
| EDR-100 to EDR-199 | Platform integration decisions |
| EDR-200 to EDR-299 | Benchmark framework decisions |
| EDR-300 to EDR-399 | Memory and RAG decisions |
| EDR-400 to EDR-499 | Agentic workflow decisions |
| EDR-900 to EDR-999 | Governance and process decisions |

---

## 5. EDR Lifecycle

```
Proposed → Accepted → (Superseded | Archived)
     ↑              ↓
   Rejected      Rejected (with reason)
```

- **Proposed:** Written, not yet validated by experiment/benchmark
- **Accepted:** Validated by evidence; configuration updated
- **Superseded:** A newer EDR replaces this one; original kept
- **Rejected:** Proposal was evaluated and not adopted; kept for learning

---

## 6. EDR Immutability

Once an EDR reaches **Accepted** status:
- The **Decision** field is immutable
- The **Evidence** field may be updated with new facts
- The **Consequences** field may be annotated with observed outcomes
- To change the decision: write a new EDR that supersedes this one

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial EDR standard |
