# AI-0006 — Architecture Decision Record

| Field | Value |
|-------|-------|
| **Title** | Architecture Decision Record (ADR) Log |
| **Purpose** | Record all significant architectural decisions with context, options considered, and rationale |
| **Scope** | All major design decisions for AI OS |
| **Version** | 0.1.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Dependencies** | All AI-XXXX documents |
| **References** | [ADR GitHub](https://adr.github.io/), [Michael Nygard ADR](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) |

---

## ADR Template

```
### ADR-XXXX — Title
- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Deprecated | Superseded by ADR-XXXX
- **Context:** Why this decision was needed
- **Options Considered:** What alternatives were evaluated
- **Decision:** What was chosen
- **Rationale:** Why this option was chosen
- **Consequences:** What changes as a result
```

---

## ADR-0001 — Use NVIDIA NIM Cloud API Instead of Self-Hosted

- **Date:** 2026-07-20
- **Status:** Accepted
- **Context:** Nemotron Ultra requires significant GPU resources (multiple A100/H100 GPUs). Self-hosting is cost-prohibitive for individual use.
- **Options Considered:**
  - Self-hosted via NVIDIA NIM container
  - NVIDIA Cloud NIM API (managed)
  - Other cloud providers (Together AI, Groq, Fireworks)
- **Decision:** Use NVIDIA Cloud NIM API
- **Rationale:** Managed service eliminates infrastructure overhead. Free tier available. Best performance guarantee for NVIDIA's own model.
- **Consequences:** Subject to rate limits. Internet dependency. Must implement graceful degradation.

---

## ADR-0002 — Use Open WebUI as Frontend

- **Date:** 2026-07-20
- **Status:** Accepted
- **Context:** Need a capable, self-hostable frontend that supports system prompts, tools, RAG, and OpenAI-compatible APIs.
- **Options Considered:**
  - Build custom UI
  - Open WebUI
  - LibreChat
  - AnythingLLM
- **Decision:** Use Open WebUI
- **Rationale:** Active development, OpenAI-compatible, strong RAG and tool support, large community, easy Docker deployment.
- **Consequences:** Tied to Open WebUI's feature roadmap. Must monitor breaking changes on upgrades.

---

## ADR-0003 — Engineering Documentation Repository (No Source Code)

- **Date:** 2026-07-20
- **Status:** Accepted
- **Context:** The AI OS primarily consists of prompts, configurations, and policies — not traditional source code.
- **Options Considered:**
  - Mix documentation and code in one repo
  - Separate repos for docs and config
  - Single documentation-only repo
- **Decision:** Single repository for all engineering documentation, prompts, configs, and datasets
- **Rationale:** Easier to maintain a single source of truth. Versioning aligned with AI OS releases.
- **Consequences:** Large repository over time. Must use good folder structure and naming conventions.

---

## ADR-0004 — Semantic Versioning for Repository

- **Date:** 2026-07-20
- **Status:** Accepted
- **Context:** Need clear versioning strategy that reflects breaking vs. non-breaking changes.
- **Decision:** Use Semantic Versioning (semver.org)
- **Rationale:** Industry standard, widely understood, compatible with automated tooling.
- **Consequences:** Must tag releases in GitHub. Must maintain CHANGELOG.

---

## TODO

- [ ] Add ADR for memory/knowledge policy decisions
- [ ] Add ADR for dataset strategy
- [ ] Add ADR for fine-tuning approach
- [ ] Add ADR for evaluation framework
