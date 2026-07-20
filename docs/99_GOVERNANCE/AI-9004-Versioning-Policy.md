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

## Cross-References

- [AI-9001 Documentation Standard](AI-9001-Documentation-Standard.md)
- [AI-9005 Release Process](AI-9005-Release-Process.md)
- [AI-9006 Repository Structure](AI-9006-Repository-Structure.md)

---

## 1. Purpose

Defines semantic versioning rules for all documents, configurations, prompts, and benchmarks in this repository. Consistent versioning enables engineering traceability and safe rollback.

---

## 2. Semantic Versioning Schema

All versioned artifacts follow `MAJOR.MINOR.PATCH`:

| Component | Increment When |
|-----------|---------------|
| `MAJOR` | Engineering decision changes; interface changes; incompatible structural change |
| `MINOR` | New sections, new evidence, new requirements added |
| `PATCH` | Typo fix, formatting, broken link repair, metadata update |

### 2.1 Examples

| Change | Before | After |
|--------|--------|-------|
| Discovered `top_k` is unsupported (breaking config change) | 0.1.0 | 1.0.0 |
| Added `medium_effort` profile section | 1.0.0 | 1.1.0 |
| Fixed typo in table | 1.1.0 | 1.1.1 |
| Changed recommended temperature from 0.6 to 1.0 | 1.1.1 | 2.0.0 |

---

## 3. Config File Versioning

All config files (`parameters.json`, `capabilities.json`, etc.) additionally carry:

```json
{
  "_metadata": {
    "version": "1.1.0",
    "status": "active",
    "previous_version": "1.0.0",
    "breaking_changes": ["removed top_k", "removed repetition_penalty"],
    "audit_reference": "AI-0003-Critical-Findings-Audit.md"
  }
}
```

---

## 4. Branch and Tag Strategy

| Branch | Purpose |
|--------|---------|
| `main` | Production-equivalent. All documents are `Active` or `Review`. |
| `draft/[topic]` | Work-in-progress documents. May contain `[ASSUMPTION]` tags. |
| `experiment/[id]` | Active experiment branches. Merged when EXP document completed. |

Tags:
```
v1.0.0          — Repository-level release
doc/AI-0001-v2  — Document-specific version tag
exp/EXP-0001    — Experiment execution snapshot
```

---

## 5. Deprecation Policy

1. No document is deleted. Documents are marked `Deprecated`.
2. Deprecated documents MUST contain a header pointing to the replacement:

```markdown
> ⚠️ DEPRECATED as of YYYY-MM-DD. Superseded by [AI-XXXX](link). This document is preserved for historical reference.
```

3. Config keys deprecated in config files MUST be moved to a `_deprecated` block, not deleted:

```json
{
  "_deprecated": {
    "top_k": { "removed_version": "1.1.0", "reason": "Not supported by NVIDIA NIM", "reference": "AI-0003-Critical-Findings-Audit.md" },
    "repetition_penalty": { "removed_version": "1.1.0", "reason": "Not supported by NVIDIA NIM", "reference": "AI-0003-Critical-Findings-Audit.md" }
  }
}
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
