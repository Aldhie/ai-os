# Context Compression Rules

> **Status**: RUNTIME | **Version**: 1.0.0

---

## Rule Set

### Rule 1: Conversation History Compression

```
Trigger: conversation > 5 turns
Action: Summarize turns 1 to (N-3) into a single block
Format:
  "[History Summary]: User is working on [X]. Key facts established:
   - [Fact 1]
   - [Fact 2]
   Current goal: [Y]"
Target: 200-400 tokens per compressed block
Preserve verbatim: last 3 turns always
```

### Rule 2: RAG Chunk Trimming

```
Trigger: RAG budget exceeded
Action: Trim each chunk to top-3 sentences by relevance
Method: Sentence-level semantic similarity to query
Fallback: First 3 sentences if similarity scoring unavailable
Minimum chunks retained: 2
```

### Rule 3: Memory Compression

```
Trigger: memory count > 3 or total memory tokens > 2000
Action: Exclude entries with similarity < 0.7
Action: For remaining entries, extract title + key facts only
Target: < 100 tokens per memory entry
```

### Rule 4: System Prompt Compression

```
Trigger: Only when total budget critically exceeded
Action: Load core identity only (500 tokens)
Skip: Extended mode behaviors, example responses
Note: This is last resort; avoid if possible
```

---

## Compression Priority (lowest priority compressed first)

```
1. Extended history (oldest first)
2. Extra RAG chunks (lowest relevance first)
3. Extra memory entries (lowest similarity first)
4. Planner verbose output (keep task list only)
5. Reflection (keep final assessment only)
6. Critic (keep verdict only)
```

---

*File: runtime/openwebui/token/compression_rules.md | Last updated: 2026-07-20*
