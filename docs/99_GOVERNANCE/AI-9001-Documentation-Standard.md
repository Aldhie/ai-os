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
| [AI-9002](AI-9002-Benchmark-Standard.md) | Benchmark documentation format |
| [AI-9003](AI-9003-Prompt-Engineering-Standard.md) | Prompt doc format |
| [AI-9004](AI-9004-Versioning-Policy.md) | Version scheme |
| [AI-9006](AI-9006-Repository-Structure.md) | Folder structure |
| [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) | ADR format |

---

## 1. Purpose

This standard defines the mandatory structure, quality criteria, and lifecycle rules for all documents in the `Aldhie/ai-os` repository. Every document that does not conform to this standard is classified as **DRAFT** regardless of its declared status.

**Engineering Principle:** Documentation is code. It must be versioned, reviewed, and maintained with the same discipline as source code.

---

## 2. Document Categories

| Category | ID Prefix | Location | Description |
|----------|-----------|----------|-------------|
| Engineering Spec | `AI-00xx` | `docs/00_ENGINEERING/` | Architecture, API, compatibility, strategy |
| Experiment | `EXP-00xx` | `docs/05_EXPERIMENTS/` | Empirical investigation results |
| Configuration | `CFG-00xx` | `docs/10_CONFIGURATION/` | Runtime configuration documentation |
| Runtime | `RUN-00xx` | `docs/20_RUNTIME/` | Operational procedures |
| Dataset | `DS-00xx` | `docs/30_DATASET/` | Dataset definitions and schemas |
| Fine-tune | `FT-00xx` | `docs/40_FINETUNE/` | Fine-tuning specifications |
| Testing | `TST-00xx` | `docs/90_TESTING/` | Test plans and results |
| Governance | `AI-90xx` | `docs/99_GOVERNANCE/` | Standards, policies, processes |
| Benchmark | `BM-00xx` | `benchmark/` | Benchmark test cases |
| Requirement | `REQ-AI-00xx` | `docs/00_ENGINEERING/REQ-INDEX.md` | Requirement traceability |

---

## 3. Mandatory Document Header

Every document MUST begin with a metadata table:

```markdown
# [DOCUMENT-ID]: [Title]

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | [ID] |
| **Title** | [Full title] |
| **Version** | [semver: X.Y.Z] |
| **Status** | [Draft / Active / Deprecated / Archived] |
| **Owner** | [GitHub username] |
| **Created** | [YYYY-MM-DD] |
| **Updated** | [YYYY-MM-DD] |
| **Category** | [Category from §2] |
```

Optional fields (required for Engineering Specs):

```markdown
| **Reviewed By** | [username or team] |
| **Source** | [URL to official doc if applicable] |
| **Evidence Level** | [Official Doc / Benchmark / Experiment / Hypothesis] |
```

---

## 4. Cross-Reference Requirements

Every Engineering Spec (`AI-00xx`) MUST include a Cross-References table:

```markdown
## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-XXXX](path) | [depends-on / implements / tested-by / supersedes] |
```

Relationship vocabulary:
- `depends-on` — this document requires the referenced document
- `implements` — this document puts the referenced spec into practice
- `tested-by` — the referenced benchmark or experiment validates this document
- `supersedes` — this document replaces the referenced document
- `extends` — this document adds to the referenced document

---

## 5. Evidence Classification

Every engineering claim in any document MUST be tagged with one of:

| Tag | Meaning | When to use |
|-----|---------|-------------|
| `[FACT: Official Doc]` | Directly sourced from official documentation | Verified API behavior, official specs |
| `[FACT: Benchmark]` | Measured empirically in this repository | Benchmark results from `benchmark/` |
| `[FACT: Experiment]` | Validated via controlled experiment | Results from `docs/05_EXPERIMENTS/` |
| `[HYPOTHESIS]` | Engineering assumption not yet validated | Reasonable but unverified claims |
| `[ASSUMPTION]` | Known gap; requires future validation | Documented unknowns |

**Rule:** `[HYPOTHESIS]` and `[ASSUMPTION]` tags MUST be accompanied by:
1. The specific validation method
2. The benchmark or experiment ID that will validate it
3. The target date or milestone for validation

---

## 6. Version Scheme

Follows [AI-9004 Versioning Policy](AI-9004-Versioning-Policy.md).

| Version | Meaning |
|---------|---------|
| `0.x.0` | Draft — not validated |
| `1.0.0` | First stable validated version |
| `1.x.0` | Minor updates, backwards compatible |
| `x.0.0` | Major revision, breaking change to claims or structure |

**Rule:** A document cannot reach `1.0.0` without at least one `[FACT]` citation per major claim.

---

## 7. Status Lifecycle

```
Draft → Review → Active → Deprecated → Archived
                    ↕
                 Updated
```

| Status | Meaning | Can be cited? |
|--------|---------|---------------|
| `Draft` | Work in progress | No (internal use only) |
| `Review` | Under engineering review | Provisional |
| `Active` | Validated and production-ready | Yes |
| `Deprecated` | Superseded by newer document | Cite with warning |
| `Archived` | Historical record only | No |

---

## 8. Changelog Requirement

Every document at version `≥ 1.0.0` MUST contain a Changelog section:

```markdown
## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [username] | Initial stable release |
```

---

## 9. Forbidden Practices

| Practice | Why Forbidden |
|----------|---------------|
| `TODO: Fill this in later` | Creates permanent technical debt |
| Claims without evidence tag | Cannot verify engineering decisions |
| Mixing facts and assumptions | Creates false confidence |
| Shortening existing content without versioning | Destroys engineering history |
| Removing cross-references | Breaks traceability |
| Placeholder sections | Degrades repository quality |
| Vague recommendations without rationale | Not actionable |

---

## 10. Review Checklist

Before any document is promoted from `Draft` to `Active`:

```
[ ] Metadata table complete
[ ] All claims have evidence tags
[ ] Cross-references table populated
[ ] No TODO items remaining
[ ] No placeholder sections
[ ] Changelog updated
[ ] Version ≥ 1.0.0
[ ] At least one FACT citation
[ ] Linked from parent document or index
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial governance standard |
