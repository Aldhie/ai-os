# AI-9005: Release Process

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9005 |
| **Title** | Release Process |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9004 — Versioning Policy](AI-9004-Versioning-Policy.md)
- [AI-9006 — Repository Structure](AI-9006-Repository-Structure.md)

---

## 1. Release Types

| Type | Trigger | Branch | Tag Format |
|------|---------|--------|------------|
| Configuration Release | Config files updated and validated | `main` | `cfg-v1.1.0` |
| Documentation Release | Major doc update or new spec | `main` | `docs-v1.x.0` |
| Benchmark Release | New benchmark results committed | `main` | `bench-v1.x.0` |
| Architecture Release | New ADR or major spec change | `main` | `arch-v1.x.0` |

---

## 2. Release Checklist

Before any release tag is created:

```
[ ] All documents in scope have Status: Active (not Draft)
[ ] All claims marked [HYPOTHESIS] have an assigned EXP-xxx
[ ] All items marked [UNKNOWN] have an assigned TC-xxx
[ ] No prohibited patterns (see AI-9001 §10)
[ ] CHANGELOG.md updated
[ ] Cross-references verified (no broken links)
[ ] Configuration files pass syntax validation
[ ] Benchmark results for changed configs are recorded
```

---

## 3. Hotfix Process

For critical fixes (incorrect engineering claim, broken config):

1. Create issue with label `critical-finding`
2. Fix directly on `main` with commit type `fix:`
3. Reference the finding ID in commit message: `fix(params): remove top_k — confirmed unsupported (AI-0003-Audit R-01)`
4. Update affected document version (PATCH bump)
5. Update Risk Register if finding was a known risk

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release process |
