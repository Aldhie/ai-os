# Knowledge Orchestration
> **Role**: Complete runtime knowledge (RAG) behaviour | **Version**: 1.0.0

---

## Why Knowledge Orchestration Exists

Retrieving knowledge costs tokens and latency. Retrieving irrelevant knowledge pollutes context and degrades answer quality. This policy defines exactly when to retrieve, how much to retrieve, how to rank it, and when to skip it entirely.

---

## Knowledge Priority Order

When multiple sources could answer a question:

```
1. Explicitly uploaded documents (user's own files) — highest authority
2. Domain knowledge collections (project-specific RAG) — high authority
3. General knowledge collections — medium authority
4. Model training knowledge — baseline (no retrieval needed)
5. Web search — only for time-sensitive facts not in collections
```

---

## Knowledge Ranking

Chunks are ranked by:
1. Semantic similarity to query (weight: 0.60)
2. Recency of the source document (weight: 0.20)
3. Source authority tier (weight: 0.20)

Minimum score to include: **0.65**

---

## Freshness Policy

```yaml
freshness_sensitive_topics:
  - API versions and endpoints
  - Software library releases
  - Pricing information
  - Regulatory and compliance requirements
  - Security vulnerability databases
  - Company-specific policies

freshness_action:
  - Flag retrieved content: "[may be outdated: verify against current {source}]"
  - If source date > 6 months: always flag
  - If source date > 12 months: flag + recommend web search
```

---

## Chunk Strategy

```yaml
chunk_size:           600 tokens   # optimal balance of context + relevance
top_k_standard:       5            # standard budget tier
top_k_deep:           8            # deep/research budget tier
top_k_minimal:        2            # tight budget situations
overlap:              50 tokens    # prevents context loss at chunk boundaries
deduplication:        true         # remove near-duplicate chunks (similarity > 0.95)
```

---

## Retrieval Budget

| Budget Tier | Max Chunks | Max Tokens | Use When |
|------------|-----------|------------|----------|
| Minimal | 2 | 1,200 | Simple question, low budget |
| Standard | 5 | 4,000 | Most tasks |
| Deep | 8 | 6,000 | Research, architecture |
| Maximum | 10 | 8,000 | Document analysis (explicit) |

---

## Citation Policy

- **Always cite** when answer is grounded in retrieved chunks: `[Source: {collection}, chunk {N}]`
- **Flag low confidence**: for chunks with score 0.65–0.74: `[verify: low confidence retrieval]`
- **Never cite** when using model knowledge alone — instead: `[model knowledge; verify with current docs]`
- **Never fabricate** source names or document titles

---

## Fallback Behaviour

```
Scenario 1: No relevant chunks found (all scores < 0.65)
  → Proceed with model reasoning
  → Add: [model knowledge; no relevant documentation found]

Scenario 2: Chunks contradict each other
  → Present both positions
  → Indicate which source is more authoritative or recent
  → Let user decide

Scenario 3: RAG service unavailable
  → Continue with model reasoning
  → Add: [knowledge base unavailable; answer from model training only]
  → Do not fail the request

Scenario 4: Knowledge clearly outdated
  → Answer with the retrieved content
  → Add: [source dated {date}; verify for current status]
```

---

## When to Skip RAG

```
Skip RAG if:
  ✗ Greeting or simple acknowledgment
  ✗ General concept question answerable from model training ("What is TCP/IP?")
  ✗ Pure reasoning task ("Which of these two options is logically consistent?")
  ✗ Creative writing task
  ✗ Token budget is at minimal tier and question is not domain-specific
  ✗ No relevant knowledge collection exists for the topic
```

## When RAG is Mandatory

```
Mandatory RAG if:
  ✓ User says "check the docs", "according to the spec", "in our knowledge base"
  ✓ Question involves a specific library version or API
  ✓ Question involves company-specific or project-specific information
  ✓ Previous answer was challenged and knowledge may resolve the dispute
```

---

## Cache vs. Live Retrieval

| Condition | Use Cache | Use Live |
|-----------|-----------|----------|
| Same query within 15 minutes | Yes | No |
| New session, same topic | Yes (5min TTL) | No |
| User says "get the latest" | No | Yes |
| Source marked as freshness-sensitive | No | Yes |
| Query hash unchanged | Yes | No |

---

## When Web Search Overrides RAG

```
Use web search instead of RAG when:
  ✓ Query is explicitly time-sensitive (news, prices, recent events)
  ✓ User asks for "current", "latest", "today", "now"
  ✓ Topic is not covered by any knowledge collection
  ✓ RAG returned no relevant results for a time-sensitive topic

Do NOT use web search:
  ✗ For questions well-covered by knowledge collections
  ✗ For general concepts that do not change
  ✗ When RPM budget is constrained (web search = additional NIM call overhead)
```

---

*File: runtime/openwebui/knowledge/orchestration.md | Last updated: 2026-07-21*
