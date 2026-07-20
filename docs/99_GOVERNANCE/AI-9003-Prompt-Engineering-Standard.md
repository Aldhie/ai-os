# AI-9003: Prompt Engineering Standard

---

## Metadata

| Field | Value |
|-------|-------|
| **Document ID** | AI-9003 |
| **Title** | Prompt Engineering Standard for Nemotron Ultra 550B |
| **Version** | 1.0.0 |
| **Status** | Active |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Scope** | All system prompts and prompt templates in `Aldhie/ai-os` |
| **Cross-References** | [AI-0001](../00_ENGINEERING/AI-0001-Nemotron-Engineering-Spec.md) · [AI-0002](../00_ENGINEERING/AI-0002-NVIDIA-NIM-API.md) · [EXP-0004](../05_EXPERIMENTS/EXP-0004-SystemPrompt.md) · [AI-9002](AI-9002-Benchmark-Standard.md) |

---

## 1. Purpose

Prompts are engineering artifacts, not natural language text. Every system prompt deployed in production must be version-controlled, tested, and documented with the same rigor as code. This standard defines the rules for authoring, versioning, and validating prompts for NVIDIA Nemotron Ultra 550B.

---

## 2. Nemotron Ultra 550B Prompt Architecture

### 2.1 Reasoning Mode Control (Source: Official NVIDIA Docs)

| Method | Syntax | Scope | Via OW UI |
|--------|--------|-------|-----------|
| System prompt ON | `/think` in system prompt | Session-wide | ✅ |
| System prompt OFF | `/nothink` in system prompt | Session-wide | ✅ |
| `extra_body` ON | `chat_template_kwargs.enable_thinking: true` | Per-request | ❌ (Pipeline needed) |
| `extra_body` OFF | `chat_template_kwargs.enable_thinking: false` | Per-request | ❌ (Pipeline needed) |
| `medium_effort` | `chat_template_kwargs.medium_effort: true` | Per-request | ❌ (Pipeline needed) |
| `reasoning_budget` | `reasoning_budget: N` | Per-request | ❌ (Pipeline needed) |

**[CONFIRMED]** Source: `docs.api.nvidia.com/nim/reference/nvidia-nemotron-3-ultra-550b-a55b`

### 2.2 Thinking Tag Behavior (Confirmed)

When reasoning is ON, the model wraps its reasoning trace in:
```
<think>
...reasoning trace...
</think>
<actual response>
```

Open WebUI filters `<think>` tags by default (configurable). Engineers must verify OW version behavior.

---

## 3. System Prompt Templates

### 3.1 General Assistant
```
/nothink
You are a knowledgeable, helpful assistant.
Respond clearly, concisely, and accurately.
Cite sources when making factual claims.
```

### 3.2 Deep Reasoning Agent
```
/think
You are an expert analytical reasoner.
For every problem: decompose, reason step by step, verify your logic.
Present your final answer clearly after thinking.
```

### 3.3 Code Agent
```
/think
You are a senior software engineer and principal architect.
Approach every coding task with:
1. Requirements analysis
2. Design before implementation
3. Clean, production-ready code
4. Test coverage consideration
5. Security and performance review
```

### 3.4 Medium Effort (via Pipeline — requires `extra_body`)
```
/think
You are a balanced analytical assistant.
Think efficiently — use reasoning when needed, but avoid over-elaborating simple topics.
```
Note: This profile requires Pipeline injection of `medium_effort: true`. System prompt alone does not activate medium_effort mode.

### 3.5 RAG / Knowledge Base Agent
```
/nothink
You are a precise knowledge retrieval assistant.
Answer ONLY from provided context.
If the answer is not in the context, state: "This information is not in the provided documents."
Do not infer or speculate beyond the context.
Cite the document source for every claim.
```

---

## 4. Prompt Quality Rules

### 4.1 Required Elements
- Reasoning mode declaration (`/think` or `/nothink`) as FIRST line
- Role definition in second line
- Behavioral constraints
- Output format specification (if structured output needed)

### 4.2 Prohibited Patterns
```
❌ Missing /think or /nothink (reasoning mode undefined → unpredictable behavior)
❌ Contradictory instructions ("Be brief" + "Provide comprehensive analysis")
❌ Undefined terms ("good response", "appropriate answer")
❌ No output format for structured tasks (JSON, tables, code)
❌ Prompts longer than 500 tokens for system prompt (wastes context budget)
```

### 4.3 Token Budget Guidelines

| Budget Component | Recommended Tokens | Source |
|-----------------|-------------------|--------|
| System prompt | ≤ 500 | [ASSUMPTION — pending EXP-0004] |
| Conversation history | ≤ 8,192 | configs/openwebui/parameters.json |
| RAG context | ≤ 4,096 | configs/openwebui/parameters.json |
| Output reservation | ≤ 4,096 | configs/openwebui/parameters.json |
| **Total** | **≤ 16,884** | Well within 256K default context |

---

## 5. Prompt Versioning

Every system prompt file in `prompts/` must include a version header:
```markdown
---
prompt_id: PROMPT-xxxx
version: x.y.z
agent_profile: general | reasoning | code | rag | medium_effort
thinking_mode: on | off | medium_effort
max_tokens_system: <number>
tested_with: nvidia/nemotron-3-ultra-550b-a55b
test_reference: EXP-xxxx
---
```

---

## 6. Changelog

| Version | Date | Author | Changes |
|---------|------|--------|--------|
| 1.0.0 | 2026-07-20 | Aldhie | Initial release |
