# Summary and Compression Policy

> **Status**: RUNTIME | **Version**: 1.0.0

---

## When to Generate a Summary

Summaries are only generated when:
1. A conversation exceeds 10 turns (compress older history)
2. A multi-document RAG request requires synthesis
3. User explicitly requests a summary

Summaries are NEVER generated:
- At the end of a regular response ("In summary...")
- As an opener ("Based on what you said...")
- To pad length

---

## History Summary Format

```
[SESSION SUMMARY - Turns 1-{N}]
Context: {one sentence about what this session is about}
Established facts:
- {fact 1}
- {fact 2}
User preferences revealed:
- {preference 1}
Current state: {what we are working on now}
```

Target: 200-300 tokens. Hard limit: 500 tokens.

---

## Document Synthesis Summary Format

```
[SOURCE SYNTHESIS]
Documents analyzed: {N}
Key consensus points:
- {point}
Conflicting information:
- {conflict and resolution}
Knowledge gaps:
- {gap}
```

---

*File: runtime/openwebui/token/summary_policy.md | Last updated: 2026-07-20*
