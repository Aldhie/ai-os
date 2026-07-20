# AI-9004: Versioning Policy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9004 |
| **Title** | Versioning Policy |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9001](AI-9001-Documentation-Standard.md) | Documentation standard |
| [AI-9005](AI-9005-Release-Process.md) | Release process |
| [AI-9006](AI-9006-Repository-Structure.md) | Repository structure |

---

## 1. Purpose

This document defines versioning rules for all artifacts in the `ai-os` repository: documents, configurations, system prompts, benchmark suites, and experiments.

---

## 2. Semantic Versioning (Documents)

All documents follow `MAJOR.MINOR.PATCH`:

| Increment | Trigger | Example |
|-----------|---------|--------|
| **MAJOR** | Breaking change to configuration, behavior, or interface | Parameter removed, thinking mode default changed |
| **MINOR** | New section added, new requirement added, new EDR added | New benchmark category, new compatibility row |
| **PATCH** | Correction, clarification, typo fix, link update | Fixed broken link, corrected spec value |

---

## 3. Configuration Versioning

Configuration files in `configs/` follow a separate version tracked in a `metadata` block inside each config:

```json
{
  "metadata": {
    "version": "1.2.0",
    "created": "2026-07-20",
    "updated": "2026-07-20",
    "owner": "Aldhie",
    "changelog": [
      {"version": "1.2.0", "date": "2026-07-20", "change": "Updated temperature to 1.0 per EXP-0001 results"}
    ]
  }
}
```

---

## 4. Experiment Versioning

Experiments follow a lifecycle, not semantic versioning:

| Status | Meaning |
|--------|---------|
| `Pending Execution` | Designed, not run |
| `In Progress` | Currently being run |
| `Completed` | Results recorded, analysis done |
| `Superseded` | Replaced by newer experiment |
| `Archived` | No longer relevant |

Experiment designs may be revised (MINOR/PATCH changes to the design document) before execution. After execution, only the Results and Analysis sections may be updated. Conclusions and Decisions are immutable once written.

---

## 5. Benchmark TC Versioning

Benchmark TCs are versioned independently. Results are IMMUTABLE once recorded.

| Version Change | Trigger |
|---------------|--------|
| PATCH | Clarification to question wording that does not change difficulty |
| MINOR | New evaluation criterion added |
| MAJOR | Question changed materially — previous results are no longer comparable |

When a TC increments MAJOR, all previous results are archived (not deleted) and labeled with the old version.

---

## 6. Repository Release Versioning

The repository itself is versioned via Git tags:

```
v0.1.0   Initial structure
v0.2.0   First benchmark suite
v0.3.0   First experiment results
v1.0.0   Production-ready: all TCs pass, all critical experiments complete
```

See [AI-9005](AI-9005-Release-Process.md) for release criteria.

---

## 7. Changelog Rules

Every document MUST include a Changelog table as its LAST section:

```markdown
## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | YYYY-MM-DD | [author] | [description] |
```

Changelogs are append-only. Never delete changelog entries.

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial versioning policy |
