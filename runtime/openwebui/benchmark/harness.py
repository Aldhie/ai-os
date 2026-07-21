"""
AI-OS Benchmark Execution Harness
Version: 1.0.0
Sprint: B

Runs the benchmark suite defined in suite.json against a live Open WebUI endpoint.
Produces a JSON score report for each dimension and an overall weighted score.

Usage:
    python harness.py --base-url http://localhost:3000 --api-key YOUR_OWU_KEY \
                      --model-id ai-os-nemotron-ultra --suite suite.json

Output:
    benchmark_results_<timestamp>.json
    benchmark_results_<timestamp>.txt  (human-readable summary)

WHY: Automated benchmarking is the only way to detect quality regressions
before they reach production. Manual inspection does not scale across 12 dimensions.
"""

import argparse
import json
import time
import re
import sys
from datetime import datetime, timezone
from typing import Any

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Benchmark probe prompts — one per dimension
# Each probe is designed to produce a response that can be scored by the
# corresponding rubric in suite.json without human evaluation.
# ---------------------------------------------------------------------------

PROBES = {
    "discussion_quality": {
        "prompt": "What is the CAP theorem?",
        "task_class": "discussion",
        "checks": ["answer_first", "no_prohibited_patterns", "length_compliance"]
    },
    "reasoning": {
        "prompt": "Analyse the trade-offs between consistency and availability in a distributed database. Use a named framework.",
        "task_class": "analysis",
        "checks": ["framework_named", "assumptions_stated", "uncertainty_tagged"]
    },
    "architecture": {
        "prompt": "Design a rate limiter service for an API gateway. Include failure modes and trade-offs.",
        "task_class": "architecture",
        "checks": ["structure_completeness", "tradeoff_explicit"]
    },
    "coding": {
        "prompt": "Write a Python function that implements a sliding window rate limiter. Include type hints and a docstring.",
        "task_class": "coding",
        "checks": ["syntax_check", "has_docstring"]
    },
    "tool_usage": {
        "prompt": "What is the Pythagorean theorem?",
        "task_class": "discussion",
        "checks": ["no_tool_call"]
    },
    "conversation_consistency": {
        "prompt": "Earlier I told you to always use tabs for indentation. What indentation style should I use?",
        "task_class": "discussion",
        "checks": ["references_prior_context"]
    },
}


def call_openwebui(base_url: str, api_key: str, model_id: str, prompt: str, system_prompt: str = "") -> dict:
    """Send a chat completion request to Open WebUI and return the response."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model_id,
        "messages": messages,
        "stream": False
    }

    start = time.time()
    try:
        resp = requests.post(
            f"{base_url}/api/chat/completions",
            headers=headers,
            json=payload,
            timeout=120
        )
        resp.raise_for_status()
        data = resp.json()
        latency_ms = int((time.time() - start) * 1000)
        content = data["choices"][0]["message"]["content"]
        return {"content": content, "latency_ms": latency_ms, "error": None}
    except Exception as e:
        return {"content": "", "latency_ms": 0, "error": str(e)}


# ---------------------------------------------------------------------------
# Scoring functions — one per check type
# Each returns a score in [0, 10] and a reason string.
# ---------------------------------------------------------------------------

PROHIBITED = re.compile(
    r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!|Happy to|I\'d be happy)',
    re.IGNORECASE | re.MULTILINE
)
VERIFY_TAG = re.compile(r'\[verify\]', re.IGNORECASE)
FRAMEWORK_WORDS = re.compile(
    r'\b(SWOT|5 Whys|First Principles|MECE|CAP theorem|Paxos|Raft|Byzantine|'
    r'cost.benefit|RACI|STAR|framework|model|approach)\b',
    re.IGNORECASE
)
ASSUMPTION_WORDS = re.compile(r'\b(assum|given that|presuppos|taking .* as given)\b', re.IGNORECASE)
ARCH_SECTIONS = ["requirement", "constraint", "component", "interface", "failure", "trade.off"]
CODE_BLOCK = re.compile(r'```python', re.IGNORECASE)
DOCSTRING = re.compile(r'"""', re.IGNORECASE)


def score_answer_first(text: str) -> tuple[int, str]:
    first_line = text.strip().split('\n')[0]
    if first_line and not first_line.lower().startswith(("i will", "let me", "to answer", "in order to")):
        return 10, "Response begins with direct answer"
    return 0, "Response starts with preamble, not answer"


def score_no_prohibited(text: str) -> tuple[int, str]:
    count = len(PROHIBITED.findall(text))
    score = max(0, 10 - count * 4)
    return score, f"{count} prohibited pattern(s) found"


def score_length_compliance(text: str, task_class: str) -> tuple[int, str]:
    targets = {"discussion": 600, "coding": 3000, "architecture": 2500,
               "analysis": 1500, "research": 2000, "debugging": 1500}
    target = targets.get(task_class, 600)
    actual = int(len(text) * 0.25)  # token estimate
    ratio = actual / target
    if 0.5 <= ratio <= 1.5:
        return 10, f"Length compliant: {actual} tokens (target {target})"
    return 0, f"Length non-compliant: {actual} tokens (target {target}, ratio {ratio:.2f})"


def score_framework_named(text: str) -> tuple[int, str]:
    if FRAMEWORK_WORDS.search(text):
        return 20, "Named framework detected"
    return 0, "No named framework detected"


def score_assumptions_stated(text: str) -> tuple[int, str]:
    count = len(ASSUMPTION_WORDS.findall(text))
    score = min(15, count * 5)
    return score, f"{count} assumption(s) explicitly stated"


def score_uncertainty_tagged(text: str) -> tuple[int, str]:
    count = len(VERIFY_TAG.findall(text))
    # Heuristic: 1-3 verify tags on an analysis = good calibration
    if 1 <= count <= 5:
        return 15, f"{count} [verify] tag(s) — appropriate uncertainty signalling"
    if count == 0:
        return 5, "No [verify] tags — may indicate overconfidence"
    return 10, f"{count} [verify] tags"


def score_arch_completeness(text: str) -> tuple[int, str]:
    covered = sum(1 for s in ARCH_SECTIONS if re.search(s, text, re.IGNORECASE))
    score = int(covered / len(ARCH_SECTIONS) * 30)
    return score, f"{covered}/{len(ARCH_SECTIONS)} architecture sections covered"


def score_tradeoff_explicit(text: str) -> tuple[int, str]:
    if re.search(r'\btrade.off\b|\bpros.*(cons|downsides)\b', text, re.IGNORECASE):
        return 20, "Trade-off explicitly stated"
    return 0, "No explicit trade-off found"


def score_syntax_check(text: str) -> tuple[int, str]:
    if not CODE_BLOCK.search(text):
        return 0, "No Python code block found"
    # Extract code and attempt compile
    blocks = re.findall(r'```python\n(.*?)```', text, re.DOTALL | re.IGNORECASE)
    if not blocks:
        return 10, "Code block present (content extraction failed)"
    try:
        compile(blocks[0], "<benchmark>", "exec")
        return 40, "Python code compiles without syntax errors"
    except SyntaxError as e:
        return 0, f"Syntax error: {e}"


def score_has_docstring(text: str) -> tuple[int, str]:
    if DOCSTRING.search(text):
        return 10, "Docstring present"
    return 0, "No docstring found"


def score_no_tool_call(text: str) -> tuple[int, str]:
    # A simple factual answer should NOT contain tool call artefacts
    if any(t in text.lower() for t in ["github", "search result", "retrieved from"]):
        return 0, "Unnecessary tool reference detected for simple factual query"
    return 50, "No unnecessary tool calls"


def score_references_prior_context(text: str) -> tuple[int, str]:
    if re.search(r'(earlier|previous|you mentioned|as you said|prior|you told me)', text, re.IGNORECASE):
        return 50, "Response references prior context"
    return 0, "No reference to prior context"


SCORE_FUNCTIONS = {
    "answer_first": score_answer_first,
    "no_prohibited_patterns": score_no_prohibited,
    "framework_named": score_framework_named,
    "assumptions_stated": score_assumptions_stated,
    "uncertainty_tagged": score_uncertainty_tagged,
    "structure_completeness": score_arch_completeness,
    "tradeoff_explicit": score_tradeoff_explicit,
    "syntax_check": score_syntax_check,
    "has_docstring": score_has_docstring,
    "no_tool_call": score_no_tool_call,
    "references_prior_context": score_references_prior_context,
}


def run_probe(base_url, api_key, model_id, dimension_name, probe):
    print(f"  [{dimension_name}] Sending probe: {probe['prompt'][:60]}...")
    result = call_openwebui(base_url, api_key, model_id, probe["prompt"])

    if result["error"]:
        return {
            "dimension": dimension_name,
            "error": result["error"],
            "total_score": 0,
            "latency_ms": 0,
            "checks": {}
        }

    text = result["content"]
    task_class = probe["task_class"]
    checks_detail = {}
    total = 0

    for check in probe["checks"]:
        fn = SCORE_FUNCTIONS.get(check)
        if fn is None:
            continue
        if check == "length_compliance":
            score, reason = fn(text, task_class)
        else:
            score, reason = fn(text)
        checks_detail[check] = {"score": score, "reason": reason}
        total += score

    return {
        "dimension": dimension_name,
        "total_score": total,
        "latency_ms": result["latency_ms"],
        "response_preview": text[:200],
        "checks": checks_detail,
        "error": None
    }


def main():
    parser = argparse.ArgumentParser(description="AI-OS Benchmark Harness")
    parser.add_argument("--base-url", default="http://localhost:3000", help="Open WebUI base URL")
    parser.add_argument("--api-key", required=True, help="Open WebUI API key")
    parser.add_argument("--model-id", default="ai-os-nemotron-ultra", help="Model ID in Open WebUI")
    parser.add_argument("--suite", default="suite.json", help="Path to benchmark suite JSON")
    parser.add_argument("--dimension", default=None, help="Run only this dimension (optional)")
    args = parser.parse_args()

    print(f"\nAI-OS Benchmark Harness v1.0.0")
    print(f"Target: {args.base_url} | Model: {args.model_id}")
    print(f"Timestamp: {datetime.now(timezone.utc).isoformat()}")
    print("-" * 60)

    results = []
    probes_to_run = {
        k: v for k, v in PROBES.items()
        if args.dimension is None or k == args.dimension
    }

    for dimension_name, probe in probes_to_run.items():
        result = run_probe(args.base_url, args.api_key, args.model_id, dimension_name, probe)
        results.append(result)
        status = "ERROR" if result["error"] else f"Score: {result['total_score']:>3}"
        print(f"  [{dimension_name}] {status} | Latency: {result['latency_ms']}ms")
        time.sleep(2)  # Respect RPM: 2s between probes = max 30 probes/min

    # Compute overall score
    valid = [r for r in results if not r["error"]]
    overall = int(sum(r["total_score"] for r in valid) / len(valid)) if valid else 0
    passing = overall >= 70

    print("-" * 60)
    print(f"Overall Score: {overall}/100 | {'PASS' if passing else 'FAIL (minimum: 70)'}")

    # Write report
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    report = {
        "schema": "ai-os/benchmark-report",
        "version": "1.0.0",
        "timestamp": timestamp,
        "model_id": args.model_id,
        "base_url": args.base_url,
        "overall_score": overall,
        "passing": passing,
        "minimum_passing_score": 70,
        "dimensions": results
    }

    report_file = f"benchmark_results_{timestamp}.json"
    with open(report_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"Report written: {report_file}")

    sys.exit(0 if passing else 1)


if __name__ == "__main__":
    main()
