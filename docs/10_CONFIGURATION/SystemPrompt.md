# System Prompt Specification

| Field | Value |
|---|---|
| **Title** | AI-OS System Prompt Specification |
| **Version** | 0.1.0 |
| **Status** | Draft |
| **Owner** | Aldhie |
| **Created** | 2026-07-20 |
| **Updated** | 2026-07-20 |

---

## Purpose

Specifies the structure, content, and versioning policy for the AI-OS system prompt. The system prompt is the primary mechanism for defining the AI's identity, behavior, constraints, and capabilities.

---

## Scope

- Applies to all interactions via Open WebUI with Nemotron Ultra 550B
- Version-controlled alongside model configuration
- Changes require regression testing before deployment

---

## System Prompt Structure

The system prompt is organized into sections using XML-style delimiters:

```xml
<identity>
  Who the AI is.
</identity>

<capabilities>
  What the AI can do.
</capabilities>

<constraints>
  What the AI must never do.
</constraints>

<tone>
  How the AI communicates.
</tone>

<memory>
  Memory rules (see MemoryPolicy.md).
</memory>

<tools>
  Tool usage rules (see ToolPolicy.md).
</tools>

<knowledge>
  Knowledge and RAG rules (see KnowledgePolicy.md).
</knowledge>
```

---

## Current System Prompt

See: `prompts/nemotron-ultra/system.txt`

---

## Versioning Policy

- System prompt version follows the repository version.
- Any change that alters behavior must increment at minimum PATCH version.
- Any change that alters identity or constraints must increment MINOR version.
- Prompt history is preserved via git commits.

---

## Token Budget

- Target: ≤2,000 tokens
- Hard limit: 4,000 tokens
- Measure with: `scripts/count_tokens.py` (TBD)

---

## Testing Requirements

Before merging system prompt changes:

1. Run regression suite: `docs/90_TESTING/Regression.md`
2. Verify persona consistency: `docs/10_CONFIGURATION/Persona.md`
3. Verify constraint enforcement: adversarial test cases
4. Token count within budget

---

## Dependencies

- `prompts/nemotron-ultra/system.txt`
- `docs/10_CONFIGURATION/Persona.md`
- `docs/10_CONFIGURATION/MemoryPolicy.md`
- `docs/10_CONFIGURATION/ToolPolicy.md`
- `docs/10_CONFIGURATION/KnowledgePolicy.md`

---

## References

- [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [OpenAI Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)

---

## TODO

- [ ] Write system prompt v1 in `prompts/nemotron-ultra/system.txt`
- [ ] Build token counter script
- [ ] Define regression test cases for system prompt
- [ ] Create A/B test framework for prompt variants
- [ ] Document prompt change review process
