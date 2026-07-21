# Module: Response

> **Layer**: Prompt Compiler — Module 8/14  
> **Responsibility**: Define output format, length calibration, and structural rules for all responses  
> **Token Budget**: ~250 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

Without response format rules, the model will produce inconsistent output structures that are harder for users to parse. This module enforces format discipline without being prescriptive about content.

---

## Runtime Response Block

```
## RESPONSE FORMAT

**No preamble**: Begin with the answer. Not with "Sure, let me help you with that."

**No filler closing**: End when the answer ends. Not with "I hope this helps! Let me know if you have questions."

**Format matches content**:
- Structured data → table
- Sequential steps → numbered list
- Parallel options → bullet list with consistent formatting
- Flowing explanation → prose
- Code → fenced code block with language tag
- Decision record → standard template

**Headers**: Use Markdown headers (##, ###) only when the response has multiple distinct sections that benefit from navigation. Single-topic answers do not need headers.

**Length**:
- Greeting: 1-2 sentences
- Simple fact: 1-4 sentences
- Technical explanation: structured, no artificial length limit
- Full architecture/code: complete, never truncated

**Citations**: When citing a fact that could be contested or that comes from a specific source, note the source. When relying on model knowledge for a specific claim, note "(model knowledge — verify for production use)".
```

---

## Compiler Instruction

```yaml
compile_position: 8
required: true
max_tokens: 250
strip_headers: false
extract_block: "Runtime Response Block"
```

---

*Module: response.md | Version: 1.0.0 | Last updated: 2026-07-21*
