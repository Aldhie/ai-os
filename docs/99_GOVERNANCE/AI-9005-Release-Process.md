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

## Cross-References

- [AI-9004 Versioning Policy](AI-9004-Versioning-Policy.md)
- [AI-9006 Repository Structure](AI-9006-Repository-Structure.md)
- [AI-9002 Benchmark Standard](AI-9002-Benchmark-Standard.md)

---

## 1. Purpose

Defines the process for releasing new versions of engineering configurations, prompts, and benchmark frameworks into the `main` branch.

---

## 2. Release Checklist

Before any commit to `main` that changes `Active` engineering documents or config files:

### 2.1 Pre-Release

- [ ] All changed documents have updated version numbers
- [ ] All changed documents have updated changelog entries
- [ ] All `[ASSUMPTION]` tags are still valid or escalated to benchmark items
- [ ] No `TODO` without linked benchmark or experiment
- [ ] All new facts cite official documentation or experiment ID
- [ ] Cross-references verified — no broken links
- [ ] Config files pass JSON validation
- [ ] Any removed config keys are in `_deprecated` block

### 2.2 Benchmark Gate

For any change affecting model parameters or system prompts:

- [ ] Minimum 1 benchmark test case re-run with new config
- [ ] Result documented in relevant EXP-xxxx document
- [ ] Score >= 3.0/5.0 or explicit exception documented

### 2.3 Commit Message Format

```
<type>(<scope>): <summary>

[optional body]

[optional footer]
```

Types:
- `feat` — new capability or document
- `fix` — correction of error or broken reference
- `refactor` — restructuring without behavior change
- `docs` — documentation update
- `benchmark` — benchmark result recorded
- `experiment` — experiment result recorded
- `config` — configuration change
- `governance` — governance document update

Examples:
```
docs(AI-0001): add reasoning_budget section — validated against NIM docs
config(parameters): remove top_k and repetition_penalty — not supported by NIM [AI-0003-Audit]
benchmark(TC-0001): record initial temperature experiment result — score 4/5
```

---

## 3. Repository Release Tags

Repository-level releases are tagged when:
- A complete audit cycle is completed
- A major configuration version is deployed
- A full experiment cycle (EXP-0001 through EXP-0010) is completed

```bash
git tag -a v1.0.0 -m "Production architecture — complete engineering docs, governance, benchmarks"
git push origin v1.0.0
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
