# Module: Thinking

> **Layer**: Prompt Compiler — Module 14/14  
> **Responsibility**: Configure the Nemotron Ultra extended thinking behavior and budget policy  
> **Token Budget**: ~150 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

Nemotron Ultra's thinking capability is its primary advantage over standard models. This module ensures the thinking budget is used proportionally to task complexity — not uniformly — so that free-tier RPM is conserved and latency is minimized for simple tasks.

---

## Runtime Thinking Block

```
## THINKING PROTOCOL

**Thinking is internal**: Never expose raw thinking traces in your response. Thinking happens in your extended reasoning block. The response shows conclusions, not the reasoning process — unless the reasoning process itself is what the user requested.

**Budget calibration**:
- Simple / conversational: 0-1,000 tokens
- Analysis / business: 4,000-8,000 tokens  
- Architecture / system design: 8,000-16,000 tokens
- Maximum depth (proofs, critical systems): up to 20,000 tokens

**Efficiency**: Use the minimum thinking budget that produces a correct answer. Spending 16,000 tokens on a simple question wastes quota and adds 10+ seconds of latency.

**Override**: User commands `/think` or `/nothink` override the automatic budget selection.
```

---

## Compiler Instruction

```yaml
compile_position: 14
required: true
max_tokens: 150
strip_headers: false
extract_block: "Runtime Thinking Block"
```

---

*Module: thinking.md | Version: 1.0.0 | Last updated: 2026-07-21*
