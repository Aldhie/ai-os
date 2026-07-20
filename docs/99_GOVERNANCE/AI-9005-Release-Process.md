# AI-9005: Release Process

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9005 |
| **Title** | Engineering Repository Release Process |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | Release lifecycle for `Aldhie/ai-os` |
| **Cross-References** | [AI-9004](AI-9004-Versioning-Policy.md) · [AI-9006](AI-9006-Repository-Structure.md) |

---

## 1. Purpose

Defines what constitutes a release, what quality gates must pass before a release, and how releases are named and tagged.

---

## 2. Release Types

| Type | Trigger | Tag Format | Example |
|------|---------|------------|---------|
| **Major** | Architecture change, new model, schema change | `v{MAJOR}.0.0` | `v2.0.0` |
| **Minor** | New document, new config, new experiment | `v{MAJOR}.{MINOR}.0` | `v1.3.0` |
| **Patch** | Bug fix, broken link, typo correction | `v{MAJOR}.{MINOR}.{PATCH}` | `v1.2.1` |
| **Milestone** | Major phase completion | `milestone/{name}` | `milestone/production-arch` |

---

## 3. Quality Gates (pre-release checklist)

### Gate 1 — Documentation
- [ ] All `Active` documents have zero `TODO:` placeholders
- [ ] All `Active` documents have complete Changelog
- [ ] All cross-references resolve (no broken links)
- [ ] All facts are cited; all assumptions are labeled `[ASSUMPTION]`

### Gate 2 — Configuration
- [ ] `parameters.json` version incremented if changed
- [ ] `capabilities.json` version incremented if changed
- [ ] No unsupported parameters present (R-01, R-02 resolved)
- [ ] All environment variables documented in `configs/README.md`

### Gate 3 — Benchmarks
- [ ] All `[UNKNOWN]` items have a linked `BM-xx` or `TC-xxxx`
- [ ] All completed benchmarks have actual results (not pending)
- [ ] No `Need Benchmark` items in Critical priority without mitigation

### Gate 4 — Security
- [ ] No API keys in any committed file
- [ ] Secret scanning run on all staged files
- [ ] API keys stored in env vars, not hardcoded

---

## 4. Release Tagging

```bash
# Create annotated tag
git tag -a v1.0.0 -m "Release v1.0.0 — Production Architecture"
git push origin v1.0.0
```

---

## 5. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
