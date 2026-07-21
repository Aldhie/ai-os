# Tool Orchestration
> **Role**: Intelligent runtime tool routing | **Version**: 1.0.0

---

## Why Tool Orchestration Exists

Every tool call costs latency and RPM quota. On NVIDIA NIM free tier (32 RPM), an uncontrolled tool chain of 5 tools per turn at 10 active users hits the limit immediately. This policy ensures tools are used only when necessary, batched efficiently, and never called redundantly.

---

## Tool Registry

### GitHub MCP

```yaml
purpose:    Access user's GitHub repositories, issues, PRs, code
trigger:    User refers to a specific repo, file, PR, issue, or commit
skip_when:
  - General coding question not about a specific repo
  - User has not mentioned any repo or GitHub context
  - Answer is derivable from model knowledge
latency:    +0.5-2s (varies by operation)
rpm_cost:   0 (does not call NIM; calls GitHub API directly)
max_calls:  3 per turn
batch:      true  # consolidate multiple repo reads into one response cycle
```

### Brain Memory (MCP)

```yaml
purpose:    Read and write user's persistent memory
trigger:    Loading: preference/history questions; Writing: new fact/decision established
skip_when:
  - Greeting or first turn
  - General knowledge question
  - No user-specific context needed
latency:    +0.3-0.8s
rpm_cost:   0 (does not call NIM)
max_calls:  2 per turn (1 read + 1 write)
batch:      false  # reads and writes are separate
```

### Web Search

```yaml
purpose:    Retrieve current, time-sensitive information
trigger:    User asks for news, current prices, latest releases, real-time facts
skip_when:
  - Question is answerable from model training or RAG
  - No time-sensitivity indicated
  - Token budget is at minimal tier
latency:    +1-3s
rpm_cost:   0 (does not call NIM; calls search API)
max_calls:  2 per turn
batch:      true  # multiple search queries batched if possible
```

### Knowledge (RAG)

```yaml
purpose:    Domain-specific knowledge base retrieval
trigger:    See knowledge/orchestration.md
skip_when:  See knowledge/orchestration.md
latency:    +0.5-1.5s (cached: +0ms)
rpm_cost:   0 (vector search; no NIM call)
max_calls:  1 per turn (retrieves top-K chunks in one call)
batch:      n/a
```

### Calculator

```yaml
purpose:    Precise arithmetic and unit conversions
trigger:    Multi-step calculation, currency conversion, financial model, statistics
skip_when:  Single-step arithmetic (model reasoning is sufficient)
latency:    +0.1s
rpm_cost:   0
max_calls:  1 per turn
```

### Future MCP Tools

```yaml
purpose:    Any new tool integrated via MCP protocol
trigger:    Tool-specific; document when adding
default:    Same budget and batching rules apply
rpm_cost:   0 unless tool requires a NIM call
registration_required: true  # must be registered in tool registry before use
```

---

## Tool Selection Algorithm

```python
def select_tools(request, task_class, context) -> list[Tool]:
    """
    Priority: use the minimum tools that produce a correct answer.
    """
    tools = []
    budget = TOOL_BUDGET[task_class]  # max tool calls from decision matrix
    
    # 1. GitHub: only if repo context is referenced
    if references_specific_repo(request):
        tools.append("github")
    
    # 2. Brain Memory: if personalization is relevant
    if needs_user_context(request, task_class):
        tools.append("brain_memory_read")
    
    # 3. Web Search: only if time-sensitive
    if is_time_sensitive(request) and not covered_by_rag(request):
        tools.append("web_search")
    
    # 4. Knowledge RAG: if domain-specific
    if needs_domain_knowledge(request):
        tools.append("knowledge_rag")
    
    # 5. Calculator: if precise arithmetic needed
    if needs_calculation(request):
        tools.append("calculator")
    
    # Enforce budget
    return tools[:budget]
```

---

## Batching Rule

```
CRITICAL: Batch ALL tool results before the final NIM call.

Wrong:
  1. Call GitHub → NIM call to process
  2. Call Memory → NIM call to process
  3. Final NIM response
  Total: 3 NIM calls = 3 RPM

Correct:
  1. Call GitHub + Call Memory (parallel, both non-NIM)
  2. Assemble all results
  3. ONE final NIM call with all context
  Total: 1 NIM call = 1 RPM
```

---

## Tool Failure Handling

| Tool | Failure Action |
|------|---------------|
| GitHub | Note: "Could not access repository" — continue with available info |
| Brain Memory | Skip memory context — continue without personalization |
| Web Search | Fall back to model knowledge — flag as potentially outdated |
| Knowledge RAG | Fall back to model knowledge — flag `[verify with docs]` |
| Calculator | Fall back to model arithmetic — flag `[verify calculation]` |

Never retry a failed tool more than once per turn.
Never silently swallow tool failures.

---

## RPM Impact Analysis

```
Scenario: Architecture design with 3 tools (GitHub + Memory + RAG)
  - GitHub call:    0 RPM (GitHub API)
  - Memory read:    0 RPM (Brain Memory API)
  - RAG retrieval:  0 RPM (vector DB)
  - Final NIM call: 1 RPM
  Total: 1 RPM per turn → SAFE at 32 RPM limit

Scenario: Tool chain that mistakenly calls NIM per tool
  - 3 tools × 1 NIM call each + 1 final = 4 RPM per turn
  - At 8 concurrent turns: 32 RPM = limit hit
  This is why batching is mandatory.
```

---

*File: runtime/openwebui/tools/orchestration.md | Last updated: 2026-07-21*
