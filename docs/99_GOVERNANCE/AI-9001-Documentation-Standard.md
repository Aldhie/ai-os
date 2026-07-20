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
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9002 — Benchmark Standard](AI-9002-Benchmark-Standard.md)
- [AI-9004 — Versioning Policy](AI-9004-Versioning-Policy.md)
- [AI-9006 — Repository Structure](AI-9006-Repository-Structure.md)
- [AI-9008 — Engineering Decision Record Standard](AI-9008-Engineering-Decision-Record-Standard.md)

---

## 1. Purpose

This document defines the mandatory standards for all documentation in the `Aldhie/ai-os` repository. Every document must satisfy these standards before being committed to `main`. The goal is to produce documentation of equivalent quality to an NVIDIA or Anthropic internal engineering specification — fully traceable, benchmark-driven, and free of placeholder content.

---

## 2. Document Classification

Every document must declare one of the following types in its metadata:

| Type | Prefix | Purpose |
|------|--------|---------|
| Engineering Specification | `AI-0xxx` | Architecture, model, API, compatibility specs |
| Configuration Reference | `CFG-xxx` | Runtime configurations, parameter files |
| Experiment Record | `EXP-xxx` | Hypotheses, procedures, results, conclusions |
| Benchmark Test Case | `TC-xxx` | Individual benchmark questions and criteria |
| Governance | `AI-9xxx` | Standards, policies, processes |
| Architecture Decision Record | `ADR-xxx` | Engineering decisions with rationale |

---

## 3. Mandatory Document Structure

Every document in this repository MUST contain:

### 3.1 Metadata Block

```markdown
## Metadata

| Field | Value |
|-------|-------|
| Document ID | [ID] |
| Title | [Title] |
| Version | [SemVer] |
| Status | Draft | Review | Active | Deprecated |
| Owner | [GitHub username] |
| Created | [ISO 8601 date] |
| Last Updated | [ISO 8601 date] |
| Category | [Classification] |
```

### 3.2 Cross References Block

Every document must link to every related document. No orphan documents permitted.

```markdown
## Cross References

- [AI-0001 — Nemotron Engineering Spec](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md)
- [EXP-0001 — Temperature Experiment](../05_EXPERIMENTS/EXP-0001-Temperature.md)
```

### 3.3 Purpose Section

Explain WHY this document exists. One to three paragraphs. No placeholder text.

### 3.4 Changelog

```markdown
## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
```

---

## 4. Fact vs Assumption Rule

This is the most critical rule in the repository.

**Every engineering claim must be classified:**

| Classification | Marker | Requirement |
|---------------|--------|-------------|
| **Confirmed Fact** | ✅ | Must cite official docs, benchmark, or experiment |
| **Validated Assumption** | ⚠️ `[HYPOTHESIS]` | Must state basis; must have an experiment planned |
| **Known Gap** | ❓ `[UNKNOWN]` | Must have a benchmark test case assigned |
| **Refuted** | ❌ `[REFUTED]` | Must explain what was found instead |

**Forbidden patterns:**
- Stating assumptions as facts without marking them
- Writing "probably", "likely", "should" without a hypothesis marker
- Copying documentation without citing source URL and access date

---

## 5. Evidence Hierarchy

Evidence quality must be declared for every technical claim:

| Level | Type | Weight |
|-------|------|--------|
| L1 | Official vendor documentation (URL + date) | Highest |
| L2 | Reproducible experiment result (EXP-xxx) | High |
| L3 | Benchmark test result (TC-xxx) | High |
| L4 | Published research paper (DOI) | Medium |
| L5 | Community consensus / engineering folklore | Low (must be marked `[HYPOTHESIS]`) |

---

## 6. Terminology Standardization

Use these exact terms throughout the repository:

| Standard Term | Do Not Use |
|---------------|------------|
| NVIDIA Cloud NIM | NIM Cloud, cloud NIM |
| Open WebUI | OpenWebUI, OWU |
| Nemotron Ultra 550B | Ultra 550B, Nemotron Ultra |
| `chat_template_kwargs` | extra_body kwargs, thinking kwargs |
| `/think` token | enable_thinking, thinking prompt |
| `reasoning_budget` | thinking budget, token budget |
| Pipeline (Open WebUI) | plugin, extension, filter |

---

## 7. Table Quality Standard

All tables must:
- Have a header with a meaningful title
- Have all columns aligned
- Never contain empty cells — use `N/A`, `TBD (→ TC-xxx)`, or `[UNKNOWN]`
- Never contain merged cells in Markdown

---

## 8. Code Block Standard

All code blocks must:
- Declare their language: ` ```python`, ` ```json`, ` ```bash`
- Include a comment explaining WHY when non-obvious
- Never contain placeholder values like `YOUR_API_KEY`, `<VALUE>` in production configs

---

## 9. Document Lifecycle

```
Draft → Review → Active → Deprecated
```

| Status | Meaning |
|--------|---------|
| Draft | Work in progress; not authoritative |
| Review | Complete; awaiting engineering review |
| Active | Authoritative; production reference |
| Deprecated | Superseded; link to replacement |

---

## 10. Prohibited Patterns

The following patterns are BANNED from this repository:

- `TODO: add content here`
- `[placeholder]`
- `TBD` without an assigned tracking ID (EXP-xxx or TC-xxx)
- Duplicate sections within a document
- Sections with less than two sentences of substance
- Claims about NVIDIA NIM behavior without L1 or L2 evidence

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — production documentation standard for ai-os |
