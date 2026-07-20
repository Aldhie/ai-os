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
| [AI-9004](AI-9004-Versioning-Policy.md) | Version scheme |
| [AI-9006](AI-9006-Repository-Structure.md) | Structure it operates on |
| [AI-9001](AI-9001-Documentation-Standard.md) | Document quality gate |

---

## 1. Release Types

| Type | Trigger | Scope |
|------|---------|-------|
| **Patch Release** | Config fixes, doc corrections | `configs/`, typo fixes |
| **Minor Release** | New experiments, new benchmarks | `docs/05_EXPERIMENTS/`, `benchmark/` |
| **Major Release** | Architecture changes, new documents | All `docs/00_ENGINEERING/` changes |
| **Emergency Fix** | Critical finding validation | Immediate push to `main` |

---

## 2. Release Checklist

### Pre-Release
```
[ ] All changed documents pass AI-9001 review checklist
[ ] No Draft documents cited as authoritative sources
[ ] Cross-references verified (no broken links)
[ ] Changelog updated in all modified documents
[ ] configs/ versions bumped if changed
[ ] REQ-INDEX updated if requirements changed
```

### Release
```
[ ] Commit message follows convention: type(scope): description
[ ] Push to main branch
[ ] Git tag created: repo-vX.Y.Z
[ ] AUDIT document updated with release date
```

### Post-Release
```
[ ] Brain Memory updated with key decisions (via MCP)
[ ] Any new open benchmarks logged in AI-0004
[ ] Any new open experiments logged in experiment index
```

---

## 3. Commit Message Convention

```
type(scope): description [version]
```

| Type | When |
|------|------|
| `feat` | New document or feature |
| `fix` | Correction to existing content |
| `refactor` | Structural reorganization |
| `docs` | Documentation-only change |
| `benchmark` | Benchmark test case changes |
| `config` | Configuration file changes |
| `exp` | Experiment document changes |
| `governance` | Governance document changes |

Examples:
```
feat(engineering): add AI-0007 agent workflow spec v1.0.0
fix(config): remove top_k and repetition_penalty from parameters.json v1.1.0
benchmark(reasoning): add TC-0001 through TC-0003 for reasoning category
refactor: upgrade repository to production architecture
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release process |
