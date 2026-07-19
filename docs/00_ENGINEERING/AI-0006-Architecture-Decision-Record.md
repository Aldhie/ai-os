# AI-0006 — Architecture Decision Record (ADR)

| Field | Value |
|-------|-------|
| **Title** | Architecture Decision Record |
| **Purpose** | Track all major architectural decisions for AI-OS |
| **Scope** | Model selection, infrastructure, frameworks, integrations |
| **Version** | 0.1.0 |
| **Status** | Active |
| **Owner** | Aldhie / Global Telko Informatika |
| **Created** | 2026-07-19 |
| **Dependencies** | All AI-00xx engineering docs |
| **References** | https://adr.github.io |

---

## ADR Format

Each decision follows this template:

```
### ADR-XXXX: Title
- **Date**: YYYY-MM-DD
- **Status**: Proposed | Accepted | Deprecated | Superseded
- **Context**: Why this decision was needed
- **Decision**: What was decided
- **Consequences**: Impact and trade-offs
```

---

## ADR-0001: Use NVIDIA Nemotron 3 Ultra 550B as Core Model

- **Date**: 2026-07-19
- **Status**: Accepted
- **Context**: Need a high-capability LLM for complex reasoning, code generation, and instruction following. Must be accessible via API without self-hosting 550B parameters.
- **Decision**: Use NVIDIA Nemotron 3 Ultra 550B via NVIDIA Cloud NIM API.
- **Consequences**: Dependent on NVIDIA NIM availability and pricing. Free tier limits must be managed carefully. Benefits from NVIDIA's TensorRT-LLM optimized inference.

---

## ADR-0002: Use Open WebUI as Frontend

- **Date**: 2026-07-19
- **Status**: Accepted
- **Context**: Need a production-ready chat UI that supports OpenAI-compatible APIs, system prompts, RAG, and tool use without building from scratch.
- **Decision**: Use Open WebUI (self-hosted Docker) as the primary user interface.
- **Consequences**: Inherits Open WebUI's release cycle. Custom features require fork or plugin development. Provides immediate RAG, voice, and multi-model support out of the box.

---

## ADR-0003: Documentation-Only Repository

- **Date**: 2026-07-19
- **Status**: Accepted
- **Context**: AI-OS engineering involves extensive prompt design, configuration tuning, benchmarking, and dataset curation — none of which are traditional source code.
- **Decision**: This repository contains only documentation, configuration, prompts, and datasets. No application source code.
- **Consequences**: Clear separation of concerns. Engineers can iterate on AI behavior independently of application deployment.

---

## TODO

- [ ] ADR-0004: Decide on embedding model for RAG
- [ ] ADR-0005: Decide on vector database (pgvector vs Qdrant vs Chroma)
- [ ] ADR-0006: Decide on fine-tuning approach (LoRA vs full fine-tune)
- [ ] ADR-0007: Decide on evaluation automation framework
