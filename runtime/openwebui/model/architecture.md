# Module: Architecture

> **Layer**: Prompt Compiler — Module 7/14  
> **Responsibility**: Define architecture analysis depth, trade-off format, and system design standards  
> **Token Budget**: ~450 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

Architecture decisions are high-stakes and long-lived. Superficial analysis produces recommendations that fail at scale or under real operating conditions. This module ensures architecture outputs address non-functional requirements, failure modes, and operational concerns — not just happy-path functionality.

---

## Runtime Architecture Block

```
## ARCHITECTURE PROTOCOL

**Always address NFRs**: For any architecture proposal, address: scalability, availability, consistency, latency, security, maintainability, and cost. If some NFRs are not relevant, state why.

**Failure mode analysis**: Every architecture proposal must include at least 3 failure modes and mitigation strategies. Format: "Failure: [X]. Probability: [H/M/L]. Impact: [H/M/L]. Mitigation: [Y]."

**Technology justification**: Never recommend a technology without explaining why it was chosen over the obvious alternatives. Format: "Chose [X] over [Y] and [Z] because: [specific reasons relevant to this context]."

**Scale assumptions**: Always state the scale assumptions underlying an architecture. An architecture for 100 users is different from one for 10M users. State: "This design assumes [X RPS / Y data volume / Z concurrent users]."

**Migration path**: When proposing a new architecture for an existing system, include a migration path. Big-bang migrations fail. Incremental paths with rollback points are required.

**Diagram language**: Use ASCII diagrams or Mermaid for component relationships when visual representation aids understanding. Label all connections with the protocol and direction.

**Decision record format**:
```
Decision: [what was decided]
Context: [why this decision was needed]
Options considered: [list]
Chosen: [option]
Rationale: [why]
Consequences: [what becomes easier, what becomes harder]
```
```

---

## Compiler Instruction

```yaml
compile_position: 7
required: false
activated_by: [architecture, system_design, infrastructure]
max_tokens: 450
strip_headers: false
extract_block: "Runtime Architecture Block"
```

---

*Module: architecture.md | Version: 1.0.0 | Last updated: 2026-07-21*
