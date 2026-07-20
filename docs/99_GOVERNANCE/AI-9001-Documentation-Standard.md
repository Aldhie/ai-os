# AI-9001: Documentation Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9001 |
| **Title** | Documentation Engineering Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All documents in `Aldhie/ai-os` |
| **Cross-References** | [AI-9002](AI-9002-Benchmark-Standard.md) · [AI-9004](AI-9004-Versioning-Policy.md) · [AI-9006](AI-9006-Repository-Structure.md) · [AI-9008](AI-9008-Engineering-Decision-Record-Standard.md) |

---

## 1. Purpose

This standard defines the required structure, metadata, content quality, and lifecycle management for all documents in the `Aldhie/ai-os` engineering repository. Every document that fails to meet this standard is classified as a documentation debt item and must be remediated before the next release.

---

## 2. Document Taxonomy

| Prefix | Category | Location | Example |
|--------|----------|----------|---------|
| `AI-0xxx` | Engineering Specification | `docs/00_ENGINEERING/` | `AI-0001-Nemotron-Engineering-Spec.md` |
| `AI-9xxx` | Governance Standard | `docs/99_GOVERNANCE/` | `AI-9001-Documentation-Standard.md` |
| `EXP-xxxx` | Experiment Record | `docs/05_EXPERIMENTS/` | `EXP-0001-Temperature.md` |
| `REQ-AI-xxxx` | Requirement | `docs/00_ENGINEERING/REQ-INDEX.md` | `REQ-AI-0001` |
| `TC-xxxx` | Test Case | `benchmark/tests/` | `TC-0001.md` |
| `ADR-xxxx` | Architecture Decision Record | `docs/00_ENGINEERING/` | `AI-0006-Architecture-Decision-Record.md` |
| `AUDIT-yyyy-mm-dd` | Repository Audit | `docs/00_ENGINEERING/` | `AUDIT-2026-07-20.md` |

---

## 3. Required Document Header

Every document MUST begin with:

```markdown
# <DOCUMENT-ID>: <Title>

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | <ID> |
| **Title** | <Full title> |
| **Version** | <semver x.y.z> |
| **Status** | Draft | Review | Active | Deprecated |
| **Owner** | <GitHub username> |
| **Created** | <YYYY-MM-DD> |
| **Updated** | <YYYY-MM-DD> |
| **Scope** | <What this document covers> |
| **Cross-References** | <Links to related documents> |
```

---

## 4. Content Quality Rules

### 4.1 Fact vs Assumption Separation

| Classification | Marker | Requirement |
|---------------|--------|-------------|
| **Confirmed Fact** | ✅ | Must cite source (official docs, benchmark, experiment) |
| **Engineering Assumption** | ⚠️ `[ASSUMPTION]` | Must state basis and how to verify |
| **Hypothesis** | 🔬 `[HYPOTHESIS]` | Must describe test to confirm |
| **Unknown** | ❓ `[UNKNOWN]` | Must be linked to a benchmark item |

**STRICT RULE:** Facts and assumptions must NEVER be mixed in the same sentence without explicit labeling.

### 4.2 Claims Requiring Citations

All of the following require a citation:
- Performance numbers (tokens/sec, latency, quality scores)
- Parameter recommendations (temperature values, max_tokens ranges)
- Model capability claims (context length, supported features)
- Compatibility assertions (supported / unsupported)
- Security recommendations

### 4.3 Prohibited Patterns

```
❌ "The model performs well on reasoning tasks." (vague, uncited)
❌ "This should work." (assumption presented as fact)
❌ "TODO: fill in later" (placeholder in Active document)
❌ "See above" (broken reference)
❌ "As mentioned before" (forward/backward reference without link)
```

### 4.4 Required Patterns

```
✅ "temperature=1.0 per official NVIDIA NIM docs [Source: docs.api.nvidia.com/nim]"
✅ "[ASSUMPTION] top_p=0.95 produces good output diversity — verify via EXP-0002"
✅ "[HYPOTHESIS] medium_effort reduces token cost by ~40% — pending BM-11"
```

---

## 5. Document Lifecycle

```
Draft → Review → Active → Deprecated
  ↑         ↓
  └─────────┘ (rejected → revise)
```

| Status | Meaning | Action Required |
|--------|---------|----------------|
| **Draft** | Work in progress; may have incomplete sections | No blocking requirement |
| **Review** | Complete; awaiting engineering validation | All facts must be cited |
| **Active** | Validated and production-approved | Zero placeholders; all benchmarks resolved |
| **Deprecated** | Superseded by a newer document | Must link to successor document |

---

## 6. Section Requirements by Document Type

### Engineering Spec (AI-0xxx)
Required sections:
1. Metadata
2. Purpose
3. Scope
4. Requirements (with REQ-IDs)
5. Technical Detail
6. Configuration
7. Risk
8. Cross-References
9. Changelog

### Experiment (EXP-xxxx)
Required sections: see [AI-9002](AI-9002-Benchmark-Standard.md)

### Governance (AI-9xxx)
Required sections:
1. Metadata
2. Purpose
3. Rules/Standards
4. Enforcement
5. Exceptions
6. Changelog

---

## 7. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release — production architecture refactor |
