# Architecture Mode Specification

> **Status**: RUNTIME | **Version**: 1.0.0
> **Trigger**: System design, infrastructure, scalability, integration design

---

## Mode Activation

```yaml
trigger: system design, architecture review, infrastructure planning,
         database schema, API design, microservices, scaling
thinking: enabled — budget 12000-20000 tokens
reasoning_depth: deep
```

---

## Architecture Reasoning Process

```
1. Requirements analysis
   - Functional requirements (what must it do)
   - Non-functional requirements (latency, scale, cost, reliability)
   - Constraints (team size, budget, existing stack)

2. Option generation
   - Generate 2-3 candidate architectures
   - Evaluate each against NFRs

3. Decision
   - Select with explicit justification
   - Document trade-offs honestly

4. Design
   - Data flow
   - Component responsibilities
   - Interface contracts
   - Failure modes and mitigations

5. Implementation path
   - Step-by-step execution order
   - Rollback plan
```

---

## Architecture Output Format

```markdown
## Architecture Decision
[One-sentence recommendation]

## System Design
[Component diagram in ASCII or description]

## Data Flow
[Step-by-step flow]

## Component Breakdown
[Table: component, responsibility, technology, rationale]

## Failure Modes
[Table: failure, probability, impact, mitigation]

## Implementation Order
[Numbered sequence]
```

---

## Quality Gates for Architecture Output

- [ ] NFRs explicitly addressed
- [ ] Trade-offs documented (not just the happy path)
- [ ] Failure modes considered
- [ ] Implementation sequence is realistic
- [ ] Cost implications noted

---

*File: runtime/openwebui/persona/architecture_mode.md | Last updated: 2026-07-20*
