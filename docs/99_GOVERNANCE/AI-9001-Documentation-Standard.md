# AI-9001: Documentation Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9001 |
| **Title** | Documentation Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) | EDR standard |
| [AI-9006](AI-9006-Repository-Structure.md) | Repository structure |
| [AI-9004](AI-9004-Versioning-Policy.md) | Versioning rules |
| [AI-9003](AI-9003-Prompt-Engineering-Standard.md) | Prompt doc standard |

---

## 1. Purpose

This document defines the mandatory documentation standard for all files in the `ai-os` repository. Every document produced in this repository must conform to this standard. The goal is to produce documentation that functions simultaneously as:

- Engineering Design Document (EDD)
- Architecture Decision Record (ADR)
- Technical Specification
- Software Requirements Specification (SRS)
- Production Runbook

Documentation that does not meet this standard is considered **incomplete** and must be updated before merging to `main`.

---

## 2. Document Types

| Type | Prefix | Location | Description |
|------|--------|----------|--------------|
| Engineering Spec | `AI-XXXX` | `docs/00_ENGINEERING/` | Core model and system specifications |
| Experiment | `EXP-XXXX` | `docs/05_EXPERIMENTS/` | Experiments with hypothesis and results |
| Governance | `AI-9XXX` | `docs/99_GOVERNANCE/` | Standards, policies, processes |
| Benchmark TC | `TC-XXXX` | `benchmark/tests/*/` | Individual benchmark test cases |
| Config | `.json/.yaml` | `configs/` | Validated configuration files |

---

## 3. Mandatory Document Structure

Every document in this repository MUST contain the following sections:

### 3.1 Metadata Block

Each document MUST begin with a metadata table:

```markdown
## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-XXXX |
| **Title** | [Full title] |
| **Version** | 0.1.0 |
| **Status** | Draft / Active / Deprecated |
| **Owner** | [GitHub username] |
| **Created** | YYYY-MM-DD |
| **Updated** | YYYY-MM-DD |
| **Category** | [Category] |
```

### 3.2 Cross-References Block

Every document MUST contain a Cross-References table:

```markdown
## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](path/to/AI-0001.md) | Related — reason |
```

Relationship types:
- `Depends on` — this document cannot be understood without the referenced document
- `Referenced by` — another document depends on this one
- `Benchmark for` — provides benchmark evidence
- `Experiment for` — provides experimental evidence
- `Governance for` — provides governance rules
- `Supersedes` — replaces an older document

### 3.3 Fact vs Assumption Marking

All claims in engineering documents MUST be labeled:

| Label | Meaning | Requirement |
|-------|---------|-------------|
| `[FACT: Official Doc]` | Supported by official documentation | Must cite source |
| `[FACT: Benchmark]` | Supported by this repo's benchmark results | Must link to TC |
| `[FACT: Experiment]` | Supported by this repo's experiment results | Must link to EXP |
| `[HYPOTHESIS]` | Engineering hypothesis — not yet validated | Must have linked EXP |
| `[ASSUMPTION]` | Engineering assumption — may not be validated | Must note risk |

Never mix facts and assumptions in the same sentence without explicit labeling.

---

## 4. Required Content by Document Type

### Engineering Spec (AI-XXXX)

| Section | Required |
|---------|----------|
| Metadata | ✅ |
| Cross-References | ✅ |
| Overview | ✅ |
| Requirements (REQ-IDs) | ✅ |
| Engineering Decisions (EDR-IDs) | ✅ |
| Benchmarks / Evidence | ✅ |
| Configuration | ✅ |
| Changelog | ✅ |

### Experiment (EXP-XXXX)

| Section | Required |
|---------|----------|
| Metadata | ✅ |
| Cross-References | ✅ |
| Objective | ✅ |
| Hypothesis | ✅ |
| Variables | ✅ |
| Environment | ✅ |
| Procedure | ✅ |
| Expected Results | ✅ |
| Actual Results | ✅ |
| Analysis | ✅ |
| Conclusion | ✅ |
| Decision | ✅ |
| Changelog | ✅ |

### Benchmark TC (TC-XXXX)

| Section | Required |
|---------|----------|
| Metadata | ✅ |
| Question | ✅ |
| Expected Behaviour | ✅ |
| Evaluation Criteria | ✅ |
| Scoring | ✅ |
| Failure Condition | ✅ |
| Success Condition | ✅ |
| Difficulty | ✅ |
| Required Capability | ✅ |
| References | ✅ |

---

## 5. Writing Style

| Rule | Requirement |
|------|-------------|
| Language | English (technical) |
| Voice | Active voice preferred |
| Tense | Present tense for specs, past tense for completed experiments |
| Lists | Use tables when comparing; use bullet lists for sequential steps |
| Code | Always use fenced code blocks with language tag |
| Diagrams | Mermaid diagrams preferred; include text fallback |
| Length | Never truncate — completeness over brevity |

---

## 6. Versioning

See [AI-9004](AI-9004-Versioning-Policy.md) for full versioning policy.

Summary:
- `MAJOR.MINOR.PATCH` semantic versioning
- MAJOR: breaking change to configuration or behavior
- MINOR: new section or significant addition
- PATCH: corrections, clarifications, typos

---

## 7. Review and Approval

| Stage | Requirement |
|-------|-------------|
| Draft | Author self-review against this standard |
| Active | Reviewed for completeness, linked experiments/benchmarks |
| Deprecated | Note replacement document and reason |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial governance standard |
