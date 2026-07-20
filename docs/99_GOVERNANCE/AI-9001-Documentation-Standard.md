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
| **Applies To** | All documents in `Aldhie/ai-os` |

## Cross-References

- [AI-9002 Benchmark Standard](AI-9002-Benchmark-Standard.md)
- [AI-9003 Prompt Engineering Standard](AI-9003-Prompt-Engineering-Standard.md)
- [AI-9004 Versioning Policy](AI-9004-Versioning-Policy.md)
- [AI-9006 Repository Structure](AI-9006-Repository-Structure.md)
- [AI-9008 EDR Standard](AI-9008-Engineering-Decision-Record-Standard.md)

---

## 1. Purpose

This document defines mandatory structure, metadata, content quality, and maintenance standards for every document in the `Aldhie/ai-os` repository. Compliance is required before any document reaches `Active` status.

---

## 2. Document Classification

| Class | Prefix | Location | Example |
|-------|--------|----------|---------|
| Engineering Spec | `AI-0xxx` | `docs/00_ENGINEERING/` | AI-0001 |
| Experiment | `EXP-0xxx` | `docs/05_EXPERIMENTS/` | EXP-0001 |
| Configuration | `CFG-0xxx` | `docs/10_CONFIGURATION/` | CFG-0001 |
| Runtime | `RUN-0xxx` | `docs/20_RUNTIME/` | RUN-0001 |
| Dataset | `DS-0xxx` | `docs/30_DATASET/` | DS-0001 |
| Fine-Tune | `FT-0xxx` | `docs/40_FINETUNE/` | FT-0001 |
| Testing | `TST-0xxx` | `docs/90_TESTING/` | TST-0001 |
| Governance | `AI-9xxx` | `docs/99_GOVERNANCE/` | AI-9001 |
| Requirement | `REQ-xxx` | `docs/00_ENGINEERING/REQ-INDEX.md` | REQ-AI-0001 |
| Audit | `AUDIT-YYYY-MM-DD` | `docs/00_ENGINEERING/` | AUDIT-2026-07-20 |

---

## 3. Mandatory Document Structure

Every document MUST contain these sections in this order:

### 3.1 Metadata Block

```markdown
## Metadata

| Field | Value |
|-------|-------|
| Document ID | |
| Title | |
| Version | |
| Status | Draft / Review / Active / Deprecated |
| Owner | |
| Created | YYYY-MM-DD |
| Updated | YYYY-MM-DD |
| Scope | |
```

### 3.2 Cross-References Block

Immediately after Metadata. Must list all directly related documents with relative links.

```markdown
## Cross-References
- [AI-0001 Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [REQ-AI-0001](../00_ENGINEERING/REQ-INDEX.md#req-ai-0001)
```

### 3.3 Purpose / Scope

What this document covers. What it does NOT cover. Who should read it.

### 3.4 Body Sections

Domain-specific content per document class.

### 3.5 Changelog

Every document MUST have a changelog at the bottom:

```markdown
## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | name | Initial release |
```

---

## 4. Content Quality Rules

### 4.1 Fact vs Assumption

Every engineering claim MUST be tagged:

| Tag | Meaning | Example |
|-----|---------|------|
| `[FACT]` | Verified from official docs or experiment | `[FACT] temperature range is 0.0–2.0 per NVIDIA API ref` |
| `[HYPOTHESIS]` | Engineering inference, not yet tested | `[HYPOTHESIS] medium_effort reduces tokens by ~40%` |
| `[BENCHMARK-REQUIRED]` | Needs empirical test | `[BENCHMARK-REQUIRED] parallel tool call success rate` |
| `[ASSUMPTION]` | Temporary placeholder pending verification | `[ASSUMPTION] Cloud NIM uses vLLM backend` |

**Rule:** No assumption may exist in an `Active` document for more than 14 days without either promotion to `[FACT]` or escalation to a benchmark item.

### 4.2 Reference Requirements

Every `[FACT]` must cite one of:
- Official vendor documentation URL
- Experiment document (EXP-xxxx) with result
- Benchmark test case (TC-xxxx) with score
- Peer-reviewed source

### 4.3 Tables

- Every comparison MUST be in a table, not prose.
- Tables must have a caption above them: `**Table N — Description**`.
- Maximum 8 columns per table. Split wider tables.

### 4.4 Code Blocks

- Every code block must specify language: ` ```python `, ` ```json `, ` ```bash `
- Every code block must have a comment or caption explaining what it does.
- No code block may contain placeholder values like `YOUR_KEY_HERE` without a comment explaining the substitution.

### 4.5 Prohibited Content

- No placeholder sections with only `TODO` text.
- No `coming soon` or `to be determined` without a linked issue or benchmark.
- No statements like "may work" or "might support" without tagging as `[HYPOTHESIS]`.

---

## 5. Status Lifecycle

```
Draft → Review → Active → Deprecated
           ↓
        Rejected
```

| Status | Meaning | Who Can Set |
|--------|---------|-------------|
| Draft | Work in progress | Author |
| Review | Ready for review | Author |
| Active | Approved and correct | Owner |
| Deprecated | Superseded or obsolete | Owner |
| Rejected | Failed review | Reviewer |

**Rule:** Only `Active` documents are authoritative. `Draft` documents may contain unverified claims tagged `[ASSUMPTION]`.

---

## 6. Versioning

See [AI-9004 Versioning Policy](AI-9004-Versioning-Policy.md) for full semver rules.

Brief summary:
- `MAJOR` — breaking change to documented interface or incompatible change to engineering decision
- `MINOR` — additive content, new sections, new evidence
- `PATCH` — typo, formatting, link fix

---

## 7. Prohibited Actions

The following actions are **explicitly prohibited** on any document:

1. Replacing detailed tables with prose summaries
2. Removing changelog entries
3. Removing cross-references without updating all pointing documents
4. Shortening benchmark evidence sections
5. Promoting `[ASSUMPTION]` to `[FACT]` without citation
6. Merging two documents without creating a redirect entry in both originals
7. Deleting requirements without a deprecation notice in REQ-INDEX.md

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — full documentation standard |
