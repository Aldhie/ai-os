# Tool Budget

> **Version**: 1.0.0
> **Spec Ref**: AI-0005-FreeTier-Strategy.md

---

## Daily Tool Budget (NVIDIA Free Tier)

Total API budget: 1,000 requests/day, 40 RPM

| Budget Allocation | Requests/Day | Percentage |
|-------------------|-------------|------------|
| Direct responses (no tool) | 600 | 60% |
| Tool-assisted responses | 200 | 20% |
| Memory operations | 100 | 10% |
| Knowledge operations | 50 | 5% |
| Background/system | 50 | 5% |
| **Total** | **1,000** | **100%** |

---

## Per-Session Tool Budget

| Profile | Max Tool Calls/Session |
|---------|-----------------------|
| discussion | 3 |
| coding | 5 |
| architecture | 10 |
| creative | 2 |
| analysis | 6 |

---

## Budget Enforcement

1. Track tool calls per session (session counter)
2. When session limit is reached, disable auto-invoke
3. User can still manually request a tool call (explicit override)
4. Log all tool calls for daily budget tracking
5. At 80% of daily budget: warn user and reduce non-essential tool calls
6. At 95% of daily budget: lock all RPM-costly tools
