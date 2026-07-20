# AI-9004: Versioning Policy

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9004 |
| **Title** | Repository Versioning and Changelog Policy |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All versioned artifacts in `Aldhie/ai-os` |
| **Cross-References** | [AI-9001](AI-9001-Documentation-Standard.md) · [AI-9005](AI-9005-Release-Process.md) · [AI-9006](AI-9006-Repository-Structure.md) |

---

## 1. Purpose

All engineering artifacts — documents, configurations, prompts, benchmark results — must follow a consistent versioning scheme to enable traceability, rollback, and release management.

---

## 2. Semantic Versioning

All artifacts use `MAJOR.MINOR.PATCH` versioning:

| Increment | When to Use | Example |
|-----------|-------------|---------|
| **MAJOR** | Breaking change to document scope, config schema, or API contract | `1.0.0 → 2.0.0` |
| **MINOR** | New section, new requirement, new benchmark, new finding | `1.0.0 → 1.1.0` |
| **PATCH** | Typo fix, wording improvement, cross-reference correction | `1.0.0 → 1.0.1` |

---

## 3. Git Commit Convention

All commits MUST follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]

[optional footer]
```

| Type | When to Use |
|------|-------------|
| `feat` | New document, new config, new experiment |
| `fix` | Correcting an error in existing document |
| `refactor` | Restructuring without content loss |
| `docs` | Documentation improvement |
| `test` | Adding benchmark or test case |
| `chore` | Maintenance, dependency updates |
| `audit` | Repository audit result |

Examples:
```
feat(AI-0003): add compatibility matrix for Open WebUI × NIM
fix(parameters): remove unsupported top_k and repetition_penalty
refactor: upgrade AI Engineering Repository to production architecture
audit: 2026-07-20 full repository quality audit
```

---

## 4. Document Changelog Format

Every document MUST end with a Changelog table:

```markdown
## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | YYYY-MM-DD | username | Description of changes |
```

---

## 5. Configuration File Versioning

All JSON/YAML config files must include:
```json
{
  "_metadata": {
    "version": "1.1.0",
    "updated": "2026-07-20",
    "changelog": [
      {"version": "1.1.0", "date": "2026-07-20", "changes": "Remove top_k, repetition_penalty"}
    ]
  }
}
```

---

## 6. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
