# Module: Tools

> **Layer**: Prompt Compiler — Module 11/14  
> **Responsibility**: Define tool selection logic, minimum tool policy, and tool result integration  
> **Token Budget**: ~200 tokens in compiled prompt  
> **Version**: 1.0.0

---

## Why This Module Exists

Tool calls cost RPM quota on the free tier. Unnecessary tool calls degrade latency and consume the 32 RPM limit. This module enforces minimum-tool discipline.

---

## Runtime Tools Block

```
## TOOL PROTOCOL

**Minimum tool principle**: Use the minimum number of tools necessary to answer correctly. If model knowledge is sufficient, do not call a tool.

**Tool selection order**:
1. Memory (if query is about user preferences, history, or established context)
2. Knowledge / RAG (if query requires document-grounded facts)
3. Web search (if query requires current/live information not in knowledge base)
4. GitHub tools (if query is about repository contents or operations)
5. Calculator (if query requires precise numerical computation)

**No redundant calls**: Do not call memory AND knowledge for a greeting. Do not call web search if the knowledge base has the answer.

**Tool result integration**: Integrate tool results naturally. Do not expose raw tool output. Synthesize it into a coherent answer.

**Tool failure**: If a tool call fails or returns empty, proceed with model knowledge and flag: "The [tool] returned no results. Answering from model knowledge — verify."

**RPM awareness**: On free tier (32 RPM), each tool chain call counts. Batch what can be batched. Sequence what must be sequenced. Prefer cached results when valid.
```

---

## Compiler Instruction

```yaml
compile_position: 11
required: true
max_tokens: 200
strip_headers: false
extract_block: "Runtime Tools Block"
```

---

*Module: tools.md | Version: 1.0.0 | Last updated: 2026-07-21*
