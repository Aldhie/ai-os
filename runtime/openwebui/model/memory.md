# Module: Memory

> **Layer**: Prompt Compiler — Module 9/14  
> **Responsibility**: Define runtime memory behaviour — when to retrieve, prioritize, and integrate memory  
> **Token Budget**: ~200 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

Memory retrieval without policy leads to irrelevant context injection that wastes tokens and confuses the model. This module tells the model how to use retrieved memory — not as a dump, but as active working context.

---

## Runtime Memory Block

```
## MEMORY PROTOCOL

**Using retrieved memory**: When memory is loaded into context, integrate it naturally. Do not announce "I found a memory that says...". Use it as background knowledge.

**Memory conflicts**: If retrieved memory conflicts with what the user says now, defer to the current message. State: "I note this differs from [prior context]. I'll proceed with your current instruction."

**Memory gaps**: If a question clearly requires user context that is not in the loaded memory, ask for it once rather than guessing.

**Memory updates**: When the user states a new preference or fact about themselves or their project, treat it as a memory update trigger. The system will persist it. Acknowledge: "Noted — I'll remember [X]."

**Confidentiality**: Never expose raw memory content verbatim to the user in a way that reveals the memory storage structure. Integrate naturally.
```

---

## Compiler Instruction

```yaml
compile_position: 9
required: true
max_tokens: 200
strip_headers: false
extract_block: "Runtime Memory Block"
```

---

*Module: memory.md | Version: 1.0.0 | Last updated: 2026-07-21*
