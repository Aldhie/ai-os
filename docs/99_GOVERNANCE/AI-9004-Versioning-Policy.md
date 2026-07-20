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
| **Last Updated** | 2026-07-20 |
| **Category** | Governance |

---

## Cross References

- [AI-9005 — Release Process](AI-9005-Release-Process.md)
- [AI-9006 — Repository Structure](AI-9006-Repository-Structure.md)

---

## 1. Semantic Versioning (SemVer)

All documents, configurations, and prompts use [SemVer 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH
```

| Change Type | Version Bump | Example Trigger |
|-------------|-------------|-----------------|
| Breaking change, structural rewrite | MAJOR | Removing a section, changing document scope |
| New content, new section, new finding | MINOR | Adding benchmark results, new risk items |
| Typo, formatting, link fix | PATCH | Correcting URL, fixing table alignment |

---

## 2. Git Commit Message Convention

Format: `<type>(<scope>): <description>`

| Type | When to Use |
|------|-------------|
| `feat` | New document, new feature, new benchmark |
| `fix` | Correcting incorrect engineering claim |
| `refactor` | Restructuring without content change |
| `docs` | Documentation improvement |
| `benchmark` | Adding or updating benchmark results |
| `experiment` | Adding or updating experiment records |
| `config` | Configuration file changes |
| `prompt` | Prompt file changes |
| `chore` | Maintenance (dependency updates, CI) |

**Examples:**
```
feat(AI-0003): add function calling compatibility matrix
fix(configs): remove top_k parameter — not supported by NIM (AI-0003-Audit)
benchmark(TC-NIM-001): record initial tool calling round-trip results
experiment(EXP-0001): complete temperature sweep results
```

---

## 3. Configuration File Versioning

All configuration files must include a `_metadata` block:

```json
{
  "_metadata": {
    "version": "1.1.0",
    "status": "active",
    "audit": "AI-0003-Audit v1.0 — 2026-07-20",
    "description": "Description of this config",
    "last_updated": "2026-07-20",
    "owner": "Aldhie",
    "changelog": [
      {"version": "1.1.0", "date": "2026-07-20", "changes": "Removed top_k, repetition_penalty. Fixed temperature to 1.0."}
    ]
  }
}
```

---

## 4. Document ID Assignment

| Range | Series | Purpose |
|-------|--------|---------|
| AI-0001 – AI-0099 | Engineering Specs | Architecture, model, API, compatibility |
| AI-0100 – AI-0199 | Configuration Docs | Runtime config documentation |
| AI-0200 – AI-0299 | Runbooks | Operational procedures |
| EXP-0001 – EXP-0099 | Experiments | Empirical investigation records |
| TC-xxxx | Test Cases | Benchmark test cases (by category) |
| ADR-0001 – ADR-0099 | Architecture Decisions | One per major decision |
| REQ-AI-0001 – REQ-AI-9999 | Requirements | System requirements with traceability |
| AI-9001 – AI-9099 | Governance | Standards and policies |

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial versioning policy |
