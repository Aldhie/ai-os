# Module: Thinking Policy
> **Module ID**: M-THINKING | **Version**: 2.0.0 | **Responsibility**: Control when and how deep extended reasoning is activated for Nemotron Ultra via NIM API
> **Why this module exists**: Nemotron Ultra's reasoning budget is a billable, latency-incurring resource. Activating it for greetings or factual lookups wastes tokens and burns Free Tier RPM quota. This module enforces deterministic budget allocation per task class.

---

## NIM API Thinking Parameters

Nemotron Ultra on NVIDIA Cloud NIM exposes reasoning via:
```json
{
  "extra_body": {
    "chat_template_kwargs": { "enable_thinking": true },
    "reasoning_budget": <tokens>
  }
}
```

When `enable_thinking: false` (or omitted), the model responds without extended chain-of-thought. When enabled, the model silently reasons up to `reasoning_budget` tokens before generating the visible response. Thinking tokens do NOT appear in the output — they consume input quota only.

---

## Task Classification → Thinking Budget

| Task Class | Enable Thinking | Reasoning Budget | Rationale |
|---|---|---|---|
| greeting / acknowledgement | false | 0 | Zero reasoning value. Wastes latency and RPM. |
| simple factual lookup | false | 0 | Single-hop retrieval. No reasoning chain needed. |
| clarification request | false | 0 | Response depends on user input, not reasoning. |
| explanation (concept) | false | 0 | Declarative output. No multi-step derivation. |
| comparison / trade-off | true | 4,096 | Requires weighing multiple attributes. |
| code generation (< 100 LOC) | true | 4,096 | Prevents logic errors in implementation. |
| debugging / root cause | true | 8,192 | Hypothesis tree often spans 5–8 branches. |
| architecture design | true | 16,384 | Component interactions, failure modes, evolution paths all require deep chain. |
| mathematical / formal reasoning | true | 20,000 | Proof-level derivation or formal verification. |
| research synthesis | true | 12,288 | Cross-source synthesis and contradiction resolution. |
| security analysis | true | 16,384 | Adversarial path enumeration requires exhaustive reasoning. |
| business strategy | true | 8,192 | Risk/trade-off matrix requires structured exploration. |
| long-context continuation (> 20 turns) | true | 8,192 | Consistency enforcement across extended conversation state. |

---

## Budget Enforcement Rules

1. **Default OFF**: `enable_thinking` is `false` unless task class explicitly requires it.
2. **Budget cap**: No request shall set `reasoning_budget` above 20,000 tokens on Free Tier.
3. **Context-aware reduction**: If the conversation history already contains resolved reasoning for the same sub-problem, reduce budget by 50%.
4. **RPM guard**: If the runtime has consumed ≥ 28 requests in the current minute, downgrade all thinking budgets by one tier (e.g., 16,384 → 8,192) until the minute resets.
5. **Streaming**: Thinking always runs with `stream: true` to maintain responsiveness under shared infrastructure latency.

---

## Failure Strategy

- If NIM returns a timeout with thinking enabled: retry once with `reasoning_budget` halved.
- If retry also times out: disable thinking, respond from model knowledge, append `[thinking disabled — NIM timeout; verify critical claims]`.
- Never fail silently on thinking budget errors.
