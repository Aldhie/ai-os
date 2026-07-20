# Reasoning Budget Specification

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Thinking Token Budget by Task

```yaml
reasoning_budgets:

  # Task: Budget Tokens | Rationale
  greeting:           0       # No reasoning needed
  simple_fact:        0       # Direct retrieval
  simple_question:    0       # Pattern match
  casual_chat:        1000    # Light coherence check
  recommendation:     2000    # Simple comparison
  explanation:        4000    # Structure + accuracy
  business_analysis:  8000    # Framework application
  market_strategy:    10000   # Multi-variable reasoning
  negotiation:        8000    # BATNA + strategy
  architecture:       16000   # Design + trade-offs
  system_design:      16000   # NFRs + components
  code_generation:    8000    # Logic + correctness
  debugging:          10000   # Hypothesis + trace
  code_review:        10000   # Correctness + security
  security_analysis:  14000   # Attack surface + mitigations
  mathematical_proof: 20000   # Step-by-step verification
  research_synthesis: 12000   # Source integration
  planning:           10000   # Dependency + sequencing
  creative_writing:   4000    # Structure + voice
  hospitality:        6000    # Empathy + resolution logic
```

---

## Free Tier Token Conservation

At standard usage (15 conversations/day, 7.5 turns avg = ~112 requests/day):

```
If avg thinking budget = 5,000 tokens
→ 112 × 5,000 = 560,000 thinking tokens/day
→ Plus ~112 × 1,000 output tokens = 112,000 output tokens
→ Total ~672,000 tokens/day = comfortably within estimates

If batch analysis adds 20 extra requests @ 12,000 each:
→ +240,000 tokens → watch RPM (40/min limit)
```

**Rule**: Use the MINIMUM budget that achieves the required quality. Never use MAXIMUM by default.

---

*File: runtime/openwebui/reasoning/reasoning_budget.md | Last updated: 2026-07-20*
