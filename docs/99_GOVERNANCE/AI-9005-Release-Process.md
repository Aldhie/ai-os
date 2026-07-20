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
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9004](AI-9004-Versioning-Policy.md) | Versioning rules |
| [AI-9006](AI-9006-Repository-Structure.md) | Structure |
| [AI-9002](AI-9002-Benchmark-Standard.md) | Benchmark requirements |

---

## 1. Purpose

This document defines the criteria, process, and gate controls for releasing a new version of the `ai-os` repository.

---

## 2. Release Levels

| Release | Criteria |
|---------|----------|
| **PATCH** (0.0.x) | Documentation corrections, link fixes, result updates |
| **MINOR** (0.x.0) | New benchmark TCs, new experiments, new governance docs, config updates |
| **MAJOR** (x.0.0) | Production-ready milestone: see Section 3 |

---

## 3. Production Release Criteria (v1.0.0)

The repository is considered production-ready when ALL of the following are complete:

| Criterion | Status |
|-----------|---------|
| All critical experiments (EXP-0001 through EXP-0010) completed | PENDING |
| All benchmark TCs pass (≥70/100) | PENDING |
| AI-0001 through AI-0005 fully validated (no unresolved hypotheses) | PENDING |
| configs/openwebui/parameters.json validated by benchmarks | PENDING |
| No open HIGH priority issues in GitHub Issues | PENDING |
| All cross-references in all documents are valid (no broken links) | PENDING |
| Documentation standard (AI-9001) compliance checked for all docs | PENDING |

---

## 4. Release Process Steps

```
1. Create release branch: release/vX.Y.Z
2. Run full benchmark suite
3. Verify all cross-references
4. Update CHANGELOG.md with all changes
5. Update version field in all modified documents
6. Tag release: git tag vX.Y.Z
7. Push tag to main
8. Create GitHub Release with release notes
```

---

## 5. Hotfix Process

For critical fixes to `main` outside the normal release cycle:

```
1. Create branch: hotfix/description
2. Apply fix
3. Verify benchmark TCs for affected area
4. Fast-merge to main with commit message: hotfix: [description]
5. Increment PATCH version
```

---

## 6. Breaking Changes

A change is considered breaking if it:
- Changes default parameter values
- Changes system prompt directive behavior
- Changes benchmark scoring criteria
- Renames document IDs or requirement IDs

Breaking changes require:
- EDR in AI-0006
- MAJOR version increment
- Migration notes in CHANGELOG

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release process |
