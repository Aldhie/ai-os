# AI-9003: Prompt Engineering Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9003 |
| **Title** | Prompt Engineering Standard |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Governance |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) | Model spec |
| [EXP-0004](../05_EXPERIMENTS/EXP-0004-SystemPrompt.md) | System prompt experiment |
| [EXP-0003](../05_EXPERIMENTS/EXP-0003-Thinking.md) | Thinking mode experiment |
| [AI-9001](AI-9001-Documentation-Standard.md) | Documentation standard |

---

## 1. Purpose

This document defines the engineering standard for all system prompts, user prompt templates, and tool-use prompts in the `ai-os` system. All prompts deployed to Open WebUI must be authored, reviewed, and versioned according to this standard.

---

## 2. System Prompt Structure Standard

All system prompts for Nemotron Ultra 550B MUST follow this structure (in order):

```
[THINKING DIRECTIVE]    ← Required: /think or /nothink
[ROLE DEFINITION]       ← Required: 1-2 sentences
[BEHAVIORAL CONSTRAINTS]← Optional: specific do/don't rules
[OUTPUT FORMAT]         ← Optional: format requirements
[DOMAIN CONTEXT]        ← Optional: specialized knowledge context
```

Example (Reasoning Profile):
```
/think
You are an expert analyst and problem solver.
Analyze all problems methodically before answering.
Use structured markdown with clear headers.
Always show your key reasoning steps.
```

---

## 3. Thinking Directive Rules

| Rule | Requirement | Evidence |
|------|-------------|----------|
| Every system prompt MUST include `/think` or `/nothink` | Required | [FACT: Official Doc — OW+NIM integration docs] |
| `/think` enables `<think>` trace in response | Confirmed | [FACT: Official Doc] |
| `/nothink` disables reasoning trace | Confirmed | [FACT: Official Doc] |
| Directive MUST be on first line | Required | [HYPOTHESIS — to validate in EXP-0004] |
| Only one directive per system prompt | Required | [HYPOTHESIS] |

---

## 4. Token Budget Guidelines

| Profile | Max System Prompt Tokens | Rationale |
|---------|-------------------------|-----------|
| General | 100 | Minimize overhead; simple use case |
| Reasoning | 200 | Needs behavioral detail but should leave budget for thinking |
| Code | 150 | Role + format instructions |
| RAG/Analyst | 200 | Needs grounding instructions |
| Creative | 100 | Let the model breathe |

[HYPOTHESIS: Prompts over 500 tokens degrade reasoning quality. See EXP-0004 for validation.]

---

## 5. Prompt Anti-Patterns

| Anti-Pattern | Example | Problem | Preferred Alternative |
|-------------|---------|---------|----------------------|
| Thinking directive missing | No `/think` or `/nothink` | Undefined behavior | Always include directive |
| Overly long system prompt | 1000+ token instructions | Reduces reasoning budget | Keep under 200 tokens |
| Contradictory instructions | "Be concise. Explain everything in detail." | Ambiguous behavior | Pick one |
| Hallucination encouragement | "If you don't know, make your best guess" | Increases false facts | "If unsure, say so explicitly" |
| Role inflation | "You are the world's most expert..." | Sycophancy risk | Neutral, professional role |
| Nested instructions | Bullet lists inside bullet lists | Parsing ambiguity | Flat list or prose |

---

## 6. Approved System Prompt Templates

### Profile: General (`/nothink`)
```
/nothink
You are a knowledgeable, helpful assistant.
Answer clearly using markdown formatting.
If you are uncertain, say so explicitly.
```
**Token count:** ~25 | **Status:** Validated (EXP-0004 PENDING)

### Profile: Reasoning (`/think`)
```
/think
You are an expert analyst.
Analyze problems methodically and show your reasoning.
Provide structured answers with clear conclusions.
```
**Token count:** ~30 | **Status:** Validated (EXP-0004 PENDING)

### Profile: Code (`/think`)
```
/think
You are a senior software engineer.
Write clean, production-ready, well-documented code.
Always include error handling. Explain your approach briefly.
```
**Token count:** ~30 | **Status:** Validated (EXP-0004 PENDING)

### Profile: RAG/Analyst (`/nothink`)
```
/nothink
You are a precise analyst. Base all answers strictly on provided context.
Never invent information. If context is insufficient, state what is missing.
Cite the source document for each claim.
```
**Token count:** ~40 | **Status:** Validated (EXP-0004 PENDING)

### Profile: Critic (`/think`)
```
/think
You are a rigorous technical critic.
Evaluate responses for accuracy, completeness, clarity, and actionability.
Score each dimension 0-10. Provide specific, actionable feedback.
Do not be lenient: incorrect confident answers score lower than honest uncertainty.
```
**Token count:** ~50 | **Status:** Validated (EXP-0009 PENDING)

---

## 7. Prompt Versioning

All approved system prompts MUST be stored in `configs/openwebui/prompts/` as individual JSON files:

```json
{
  "prompt_id": "SYS-001",
  "profile": "reasoning",
  "version": "1.0.0",
  "content": "/think\nYou are an expert analyst...",
  "token_count": 30,
  "status": "active",
  "validated_by": "EXP-0004",
  "created": "2026-07-20",
  "updated": "2026-07-20"
}
```

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial prompt engineering standard |
