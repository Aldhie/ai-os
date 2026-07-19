# Runtime Reflection

---

## Metadata

| Field | Value |
|-------|-------|
| **Document** | Reflection.md |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

This document defines the Reflection component of the AI OS runtime. Reflection enables the AI to evaluate its own outputs for quality, accuracy, and completeness before delivering the final response.

---

## Scope

- Reflection design and principles
- Reflection trigger conditions
- Self-evaluation criteria
- Memory extraction from reflection

---

## Dependencies

- `docs/20_RUNTIME/Workflow.md` — when reflection occurs in the flow
- `docs/20_RUNTIME/Critic.md` — critic evaluation complements reflection
- `prompts/nemotron-ultra/reflection.txt` — reflection prompt

---

## References

- [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.17651)
- [Reflexion: Language Agents with Verbal Reinforcement](https://arxiv.org/abs/2303.11366)

---

## Reflection Design

After generating a candidate response, the assistant applies a **self-evaluation loop**:

```
Candidate Response
    ↓
[CHECK] Does it answer the question?
[CHECK] Is it factually accurate?
[CHECK] Is it complete?
[CHECK] Is it clear and well-structured?
[CHECK] Does it respect all constraints?
    ↓
Pass? → Deliver Response
Fail? → Revise and re-evaluate
```

---

## Self-Evaluation Criteria

| Criterion | Check |
|-----------|-------|
| Relevance | Does the response directly address the user's request? |
| Accuracy | Are all facts correct and well-supported? |
| Completeness | Are all parts of the request addressed? |
| Clarity | Is the response easy to understand? |
| Safety | Is the response free from harmful content? |
| Format | Is the formatting appropriate for the context? |

---

## Memory Extraction

During reflection, the assistant may identify facts worth storing in memory:

- New user preferences revealed during conversation
- Important facts the user shared
- Corrections to previously stored information

---

## TODO

- [ ] Write reflection prompt v0.1.0
- [ ] Define maximum reflection iterations
- [ ] Measure quality improvement from reflection vs. direct response
- [ ] Implement reflection as optional per-request toggle
- [ ] Log reflection outcomes for analysis
