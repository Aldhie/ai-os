# EXP-0004: System Prompt Engineering for Nemotron Ultra 550B

---

## Metadata

| Field | Value |
|-------|-------|
| **Experiment ID** | EXP-0004 |
| **Title** | System Prompt Engineering |
| **Version** | 0.1.0 |
| **Status** | Pending Execution |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |
| **Category** | Experiment — Prompt Engineering |

## Cross-References

| Document | Relationship |
|----------|--------------|
| [AI-9003](../99_GOVERNANCE/AI-9003-Prompt-Engineering-Standard.md) | Prompt engineering standard |
| [EXP-0003](EXP-0003-Thinking.md) | Thinking mode control |
| [AI-0003](../00_ENGINEERING/AI-0003-OpenWebUI-Compatibility.md) | System prompt compatibility |
| [REQ-INDEX](../00_ENGINEERING/REQ-INDEX.md) | REQ-AI-0006 |

---

## 1. Objective

Determine the optimal system prompt structure for Nemotron Ultra 550B across five agent profiles: **general**, **reasoning**, **code**, **creative**, and **RAG/analyst**. Validate the 500-token budget hypothesis and identify anti-patterns.

---

## 2. Background

System prompts for Nemotron Ultra 550B have a unique constraint: the thinking mode directive (`/think` or `/nothink`) MUST be present. Without it, the model defaults to an unspecified mode. [FACT: Official Doc — system prompt directives are the primary Open WebUI control mechanism]

The optimal structure and length of system prompts beyond the thinking directive is unknown. [ASSUMPTION]

---

## 3. Hypothesis

**H1:** System prompts over 500 tokens reduce effective reasoning budget, degrading output quality on complex tasks. [HYPOTHESIS]

**H2:** Role + Thinking Directive + Constraints + Output Format is the optimal system prompt structure. [HYPOTHESIS]

**H3:** Explicit output format instructions in the system prompt ("respond in JSON", "use markdown headers") improve formatting consistency by >80%. [HYPOTHESIS]

---

## 4. Variables

### Independent Variables
| Variable | Values |
|----------|--------|
| Prompt length | 50, 100, 200, 500, 1000 tokens |
| Prompt structure | Role-only / Role+Directives / Role+Directives+Format / Full |
| Output format instruction | None / Markdown / JSON / Plain |

---

## 5. Profiles to Design

### Profile: General
```
/nothink
You are a knowledgeable assistant. Answer clearly and directly.
Use markdown formatting. Cite sources when available.
```

### Profile: Reasoning
```
/think
You are an expert analyst. Analyze problems methodically.
Show your reasoning. Provide structured conclusions.
Use markdown with headers.
```

### Profile: Code
```
/think
You are a senior software engineer.
Write clean, documented, production-ready code.
Always include error handling. Explain your approach.
Output code blocks with language specification.
```

### Profile: Creative
```
/nothink
You are a creative writer. Generate original, engaging content.
Prioritize quality and creativity over speed.
```

### Profile: RAG/Analyst
```
/nothink
You are a precise analyst. Base all answers strictly on provided context.
If context is insufficient, state explicitly what is missing.
Never invent information. Cite the source document for each claim.
```

---

## 6. Actual Results

> **Status: PENDING EXECUTION**

---

## 7. Conclusion

> **PENDING**

---

## Changelog

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1.0 | 2026-07-20 | Aldhie | Initial experiment design including profile templates |
