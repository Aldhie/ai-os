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
| [AI-9001](AI-9001-Documentation-Standard.md) | Depends on version scheme |
| [AI-9005](AI-9005-Release-Process.md) | Implements version bump process |

---

## 1. Semantic Versioning for Engineering Documents

All documents and configuration files use **Semantic Versioning (SemVer)**:

```
MAJOR.MINOR.PATCH
```

| Component | Increment When |
|-----------|----------------|
| `MAJOR` | Breaking change to engineering claims, structure, or decisions |
| `MINOR` | New content added, existing content expanded |
| `PATCH` | Corrections, typo fixes, clarifications without new information |

---

## 2. Version States

| Version Range | State | Meaning |
|---------------|-------|---------|
| `0.x.y` | Draft | Content not yet validated |
| `1.0.0` | Stable | First validated production version |
| `≥ 1.0.0` | Production | Can be cited in other documents |
| `DEPRECATED` | Legacy | Superseded; do not use for new work |

**Rule:** Documents in state `0.x.y` MUST NOT be cited as authoritative sources in other documents.

---

## 3. Version Bump Protocol

### MAJOR bump triggers:
- An existing engineering claim is proven wrong by benchmark or experiment
- Document structure is significantly reorganized
- A critical finding invalidates a previous decision

### MINOR bump triggers:
- New section added
- New benchmark results added
- New experiments added
- Existing content expanded with new evidence

### PATCH bump triggers:
- Typo or grammar correction
- Metadata update (date, owner)
- Cross-reference link updated

---

## 4. Configuration File Versioning

All JSON/YAML configuration files MUST include:

```json
{
 "_metadata": {
 "version": "X.Y.Z",
 "status": "draft | active | deprecated",
 "last_updated": "YYYY-MM-DD",
 "owner": "[username]",
 "changelog": [
 {"version": "1.0.0", "date": "YYYY-MM-DD", "changes": "[description]"}
 ]
 }
}
```

---

## 5. Git Tag Convention

```
repo-vX.Y.Z — Full repository milestone release
doc/AI-XXXX-vX.Y.Z — Individual document version tag
benchmark/CATEGORY-vX.Y.Z — Benchmark suite version tag
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial versioning policy |
