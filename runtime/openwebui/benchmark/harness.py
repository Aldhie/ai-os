#!/usr/bin/env python3
"""
AI-OS Benchmark Execution Harness
Version: 2.0.0
Sprint: C

Runs the benchmark suite defined in suite.json against a live Open WebUI endpoint.
All test cases, weights, and expected scores are driven by suite.json — not hardcoded.

Key improvements over v1.0:
  - Suite-driven: loads all domains/cases from suite.json
  - Normalized scoring: all dimension scores in [0.0, 1.0]
  - Retry logic: up to 3 attempts per case with exponential backoff
  - Multi-turn context injection: [INJECT ...] prompts build real conversation history
  - Per-case minimum score validation against suite.json expected_score_min
  - Language detection: validates response language matches case.language
  - Weighted overall score: weights per domain configurable via suite.json _domain_weights
  - Exit code 0 = PASS (overall >= _passing_threshold), 1 = FAIL

Usage:
    python harness.py --base-url http://localhost:3000 --api-key YOUR_OWU_KEY \
                      --model-id ai-os-nemotron-ultra --suite suite.json

    # Run single domain:
    python harness.py ... --domain coding

    # Run single case:
    python harness.py ... --case code-001

Output:
    benchmark_results_<timestamp>.json
    benchmark_results_<timestamp>.txt  (human-readable summary)

WHY: Automated benchmarking is the only way to detect quality regressions
before they reach production. Manual inspection does not scale across 9 domains x 3 cases.
"""

import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from typing import Any

try:
    import requests
except ImportError:
    print("ERROR: requests library required. Install with: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

MAX_RETRIES = 3
RETRY_BASE_DELAY = 4  # seconds; doubles each retry
PROBE_DELAY = 2        # seconds between probes (RPM guard)

# Default domain weights when not specified in suite.json
DEFAULT_DOMAIN_WEIGHTS: dict[str, float] = {
    "discussion":     0.08,
    "coding":         0.16,
    "architecture":   0.14,
    "debugging":      0.14,
    "analysis":       0.12,
    "research":       0.10,
    "memory":         0.10,
    "tool_efficiency": 0.08,
    "long_context":   0.08,
}


# ---------------------------------------------------------------------------
# Regex patterns for automated scoring
# ---------------------------------------------------------------------------

PROHIBITED = re.compile(
    r'^(Great!|Sure!|Absolutely!|Of course!|Certainly!|Happy to|I\'d be happy|'
    r'Of course,|Sure,|Certainly,)',
    re.IGNORECASE | re.MULTILINE
)
VERIFY_TAG      = re.compile(r'\[verify\]', re.IGNORECASE)
FRAMEWORK_WORDS = re.compile(
    r'\b(SWOT|5 Whys|First Principles|MECE|CAP theorem|Paxos|Raft|Byzantine|'
    r'CQRS|Event Sourcing|Saga|Two-Phase Commit|Vector Clock|'
    r'cost.benefit|RACI|STAR|framework|model|approach)\b',
    re.IGNORECASE
)
ASSUMPTION_WORDS = re.compile(
    r'\b(assum|given that|presuppos|taking .* as given|assuming)\b',
    re.IGNORECASE
)
CODE_BLOCK   = re.compile(r'```(?:python|py)\s', re.IGNORECASE)
DOCSTRING    = re.compile(r'"""')
TYPE_HINTS   = re.compile(r'->\s*\w+|:\s*(?:str|int|float|bool|list|dict|tuple|Optional|Union|List|Dict)\b')
CONFLICT_WORDS = re.compile(
    r'\b(contradict|conflict|inconsisten|earlier|previous|turn \d|at turn)\b',
    re.IGNORECASE
)
# Indonesian language signal words
ID_SIGNAL = re.compile(
    r'\b(adalah|untuk|dengan|yang|dalam|ini|itu|dapat|akan|atau|juga|lebih|'
    r'namun|karena|ketika|seperti|antara|sebagai|bisa|sudah|saat|pada|dari)\b',
    re.IGNORECASE
)
ARCH_SECTIONS = [
    "requirement", "constraint", "component", "interface", "failure", "trade.?off"
]


# ---------------------------------------------------------------------------
# Context injection: parse [INJECT ...] markers and build message history
# ---------------------------------------------------------------------------

INJECT_PATTERN = re.compile(r'^\[INJECT (.+?)\]\s*', re.DOTALL)


def build_messages(prompt: str, system_prompt: str = "") -> list[dict]:
    """
    Parse [INJECT context description] prefix and construct a realistic
    multi-turn message list so the model sees injected context naturally.

    Examples handled:
      [INJECT prior session context: user prefers PostgreSQL over MongoDB]
      [INJECT conflicting context: user said X in turn 3, now says Y]
      [INJECT 15-turn conversation] At turn 3 we decided ...
    """
    messages: list[dict] = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})

    m = INJECT_PATTERN.match(prompt)
    if m:
        inject_desc = m.group(1).strip()
        actual_question = prompt[m.end():].strip()

        # Build synthetic prior context as an assistant turn so the model
        # can reference it naturally.
        synthetic_context = (
            f"[Context from prior session/turns: {inject_desc}]\n\n"
            "The following conversation continues from this point."
        )
        messages.append({"role": "user",      "content": "[BEGIN INJECTED CONTEXT]"})
        messages.append({"role": "assistant", "content": synthetic_context})
        messages.append({"role": "user",      "content": actual_question})
    else:
        messages.append({"role": "user", "content": prompt})

    return messages


# ---------------------------------------------------------------------------
# Open WebUI API client with retry logic
# ---------------------------------------------------------------------------

def call_openwebui(
    base_url: str,
    api_key: str,
    model_id: str,
    prompt: str,
    system_prompt: str = "",
    temperature: float = 0.7,
) -> dict:
    """Send a chat completion request to Open WebUI with exponential-backoff retry."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type":  "application/json",
    }
    messages = build_messages(prompt, system_prompt)
    payload = {
        "model":       model_id,
        "messages":    messages,
        "stream":      False,
        "temperature": temperature,
    }

    last_error: str | None = None
    for attempt in range(1, MAX_RETRIES + 1):
        start = time.time()
        try:
            resp = requests.post(
                f"{base_url}/api/chat/completions",
                headers=headers,
                json=payload,
                timeout=120,
            )
            resp.raise_for_status()
            data = resp.json()
            latency_ms = int((time.time() - start) * 1000)
            content = data["choices"][0]["message"]["content"]
            return {"content": content, "latency_ms": latency_ms, "error": None, "attempts": attempt}
        except Exception as e:
            last_error = str(e)
            if attempt < MAX_RETRIES:
                delay = RETRY_BASE_DELAY * (2 ** (attempt - 1))
                print(f"    Retry {attempt}/{MAX_RETRIES - 1} after {delay}s: {last_error[:80]}")
                time.sleep(delay)

    return {"content": "", "latency_ms": 0, "error": last_error, "attempts": MAX_RETRIES}


# ---------------------------------------------------------------------------
# Individual check scorers — all return (score: float [0.0-1.0], reason: str)
# ---------------------------------------------------------------------------

def check_no_preamble(text: str) -> tuple[float, str]:
    """Response must open with direct answer, not a filler phrase."""
    if PROHIBITED.match(text.strip()):
        return 0.0, "Starts with prohibited preamble"
    first = text.strip().split('\n')[0].lower()
    if first.startswith(("i will", "let me", "to answer", "in order to")):
        return 0.3, "Starts with vague opening (not filler, but not direct)"
    return 1.0, "Response opens directly"


def check_length(text: str, target_tokens: int) -> tuple[float, str]:
    """Token estimate = len(text) * 0.25. Optimal window: 50%-150% of target."""
    estimated = max(1, int(len(text) * 0.25))
    ratio = estimated / max(1, target_tokens)
    if 0.5 <= ratio <= 1.5:
        return 1.0, f"Length OK: ~{estimated} tok (target {target_tokens})"
    if ratio < 0.5:
        score = ratio / 0.5  # linear ramp from 0 at ratio=0 to 1.0 at ratio=0.5
        return round(score, 2), f"Too short: ~{estimated} tok (target {target_tokens}, ratio {ratio:.2f})"
    # ratio > 1.5
    score = max(0.0, 1.0 - (ratio - 1.5) / 1.5)
    return round(score, 2), f"Too long: ~{estimated} tok (target {target_tokens}, ratio {ratio:.2f})"


def check_code_quality(text: str) -> tuple[float, str]:
    """Code block present, compiles, has docstring and type hints."""
    if not CODE_BLOCK.search(text):
        return 0.0, "No Python code block found"

    score = 0.4  # code block present
    notes = ["code block present"]

    blocks = re.findall(r'```(?:python|py)\s(.*?)```', text, re.DOTALL | re.IGNORECASE)
    if blocks:
        try:
            compile(blocks[0], "<benchmark>", "exec")
            score += 0.3
            notes.append("compiles")
        except SyntaxError as e:
            notes.append(f"syntax error: {e}")

    if DOCSTRING.search(text):
        score += 0.15
        notes.append("docstring present")

    if TYPE_HINTS.search(text):
        score += 0.15
        notes.append("type hints present")

    return round(min(1.0, score), 2), ", ".join(notes)


def check_arch_completeness(text: str) -> tuple[float, str]:
    """Architecture response covers required sections."""
    covered = [s for s in ARCH_SECTIONS if re.search(s, text, re.IGNORECASE)]
    score = len(covered) / len(ARCH_SECTIONS)
    return round(score, 2), f"{len(covered)}/{len(ARCH_SECTIONS)} arch sections: {covered}"


def check_tradeoff_explicit(text: str) -> tuple[float, str]:
    """Must name at least one explicit trade-off."""
    if re.search(r'\btrade.?off\b|\bpros.{0,20}cons\b|\badvantage.{0,20}disadvantage\b', text, re.IGNORECASE):
        return 1.0, "Explicit trade-off found"
    return 0.0, "No explicit trade-off"


def check_reasoning_depth(text: str) -> tuple[float, str]:
    """Heuristic: framework named + assumptions stated + uncertainty tagged."""
    score = 0.0
    notes = []
    if FRAMEWORK_WORDS.search(text):
        score += 0.4
        notes.append("framework named")
    n_assumptions = len(ASSUMPTION_WORDS.findall(text))
    if n_assumptions >= 1:
        assumption_score = min(0.35, n_assumptions * 0.12)
        score += assumption_score
        notes.append(f"{n_assumptions} assumption(s)")
    n_verify = len(VERIFY_TAG.findall(text))
    if 1 <= n_verify <= 5:
        score += 0.25
        notes.append(f"{n_verify} [verify] tag(s)")
    elif n_verify == 0:
        notes.append("no [verify] tags")
    return round(min(1.0, score), 2), ", ".join(notes) if notes else "no depth signals"


def check_hallucination_control(text: str) -> tuple[float, str]:
    """Proxy: no prohibited preamble, appropriate hedge phrases present."""
    hedge = re.compile(
        r'\b(typically|generally|often|may|might|could|depends on|in most cases|'
        r'usually|can vary|verify|check|consult)\b',
        re.IGNORECASE
    )
    n_preamble = len(PROHIBITED.findall(text))
    n_hedges    = len(hedge.findall(text))
    score = 1.0
    if n_preamble > 0:
        score -= 0.3
    if n_hedges < 1:
        score -= 0.15  # no epistemic humility at all is a mild risk signal
    return round(max(0.0, score), 2), f"{n_preamble} preambles, {n_hedges} hedges"


def check_language_match(text: str, expected_lang: str) -> tuple[float, str]:
    """If case requires Indonesian (id), response must contain Indonesian words."""
    if expected_lang == "id":
        matches = len(ID_SIGNAL.findall(text))
        if matches >= 5:
            return 1.0, f"Indonesian confirmed ({matches} signal words)"
        return round(matches / 5, 2), f"Weak Indonesian ({matches}/5 signal words)"
    return 1.0, "Language check skipped (en)"  # English detection not strict


def check_conflict_surfacing(text: str) -> tuple[float, str]:
    """Memory/long-context: must detect and surface contradictions."""
    if CONFLICT_WORDS.search(text):
        return 1.0, "Contradiction/context reference detected"
    return 0.0, "No conflict reference found"


def check_tool_efficiency(text: str) -> tuple[float, str]:
    """Tool calls must not appear for trivial factual questions."""
    tool_artefacts = re.compile(
        r'<tool_call|<function_call|\btool_use\b|"name":\s*"\w+"|'
        r'"function":|retrieved from|search result',
        re.IGNORECASE
    )
    if tool_artefacts.search(text):
        return 0.0, "Unexpected tool call artefact in response"
    return 1.0, "No unnecessary tool calls"


# ---------------------------------------------------------------------------
# Dimension scorer — maps suite.json dimensions to check functions
# ---------------------------------------------------------------------------

def score_case(text: str, case: dict, domain_meta: dict) -> dict[str, dict]:
    """
    Score a single response against all dimensions that appear in
    case["expected_score_min"].

    Returns a dict: {dimension: {"score": float, "reason": str, "min": float, "pass": bool}}
    """
    target_tokens: int = domain_meta.get("target_length_tokens", 600)
    expected_lang: str = case.get("language", "en")
    dimensions_min: dict = case.get("expected_score_min", {})

    results: dict[str, dict] = {}

    for dim in dimensions_min:
        min_score = dimensions_min[dim]

        if dim == "correctness":
            # Heuristic proxy: no preamble + language match + not empty
            s1, r1 = check_no_preamble(text)
            s2, r2 = check_language_match(text, expected_lang)
            score = round((s1 * 0.4 + s2 * 0.6), 2) if text else 0.0
            reason = f"preamble: {r1} | lang: {r2}"

        elif dim == "reasoning_depth":
            score, reason = check_reasoning_depth(text)

        elif dim == "format_compliance":
            expected_fmt = case.get("expected_format", "prose")
            score, reason = _check_format(text, expected_fmt)

        elif dim == "length_compliance":
            score, reason = check_length(text, target_tokens)

        elif dim == "tool_efficiency":
            score, reason = check_tool_efficiency(text)

        elif dim == "hallucination_control":
            score, reason = check_hallucination_control(text)

        else:
            score, reason = 0.5, f"No scorer for dimension '{dim}' — partial credit"

        results[dim] = {
            "score":  score,
            "reason": reason,
            "min":    min_score,
            "pass":   score >= min_score,
        }

    return results


def _check_format(text: str, expected_fmt: str) -> tuple[float, str]:
    """Light format compliance check."""
    fmt = expected_fmt.lower()
    has_code    = bool(CODE_BLOCK.search(text))
    has_headers = bool(re.search(r'^#{1,3} ', text, re.MULTILINE))
    has_numbered = bool(re.search(r'^\d+\.\s', text, re.MULTILINE))
    has_table   = bool(re.search(r'^\|.+\|', text, re.MULTILINE))

    if "code_block" in fmt:
        return (1.0, "code block present") if has_code else (0.0, "missing code block")
    if "numbered_list" in fmt:
        return (1.0, "numbered list present") if has_numbered else (0.3, "no numbered list")
    if "headers" in fmt:
        return (1.0, "headers present") if has_headers else (0.4, "no markdown headers")
    if "table" in fmt:
        if has_table:
            return 1.0, "table present"
        if has_headers or has_numbered:
            return 0.7, "structured prose (no table, but headers/list present)"
        return 0.4, "unstructured prose for table-expected response"
    # prose / any format
    return 1.0, "prose accepted"


# ---------------------------------------------------------------------------
# Domain-level runner
# ---------------------------------------------------------------------------

def run_case(
    base_url: str,
    api_key: str,
    model_id: str,
    case: dict,
    domain_meta: dict,
) -> dict:
    """Run a single test case and return its full result dict."""
    case_id   = case["id"]
    prompt    = case["prompt"]
    temp      = domain_meta.get("temperature", 0.7)

    print(f"    [{case_id}] {prompt[:70].replace(chr(10), ' ')}...")

    api_result = call_openwebui(
        base_url, api_key, model_id, prompt, temperature=temp
    )

    if api_result["error"]:
        return {
            "case_id":     case_id,
            "error":       api_result["error"],
            "attempts":    api_result["attempts"],
            "latency_ms":  0,
            "dimensions":  {},
            "case_pass":   False,
            "agg_score":   0.0,
        }

    text       = api_result["content"]
    dim_scores = score_case(text, case, domain_meta)
    agg        = _aggregate(dim_scores)
    case_pass  = all(v["pass"] for v in dim_scores.values())

    return {
        "case_id":          case_id,
        "error":            None,
        "attempts":         api_result["attempts"],
        "latency_ms":       api_result["latency_ms"],
        "response_preview": text[:300],
        "dimensions":       dim_scores,
        "agg_score":        agg,
        "case_pass":        case_pass,
    }


def _aggregate(dim_scores: dict) -> float:
    """Mean of all dimension scores."""
    if not dim_scores:
        return 0.0
    return round(sum(v["score"] for v in dim_scores.values()) / len(dim_scores), 4)


def run_domain(
    base_url: str,
    api_key: str,
    model_id: str,
    domain_name: str,
    domain_data: dict,
    case_filter: str | None = None,
) -> dict:
    """Run all cases in a domain and return domain result."""
    domain_meta = {
        k: v for k, v in domain_data.items() if k != "cases"
    }
    cases_run = []

    for case in domain_data.get("cases", []):
        if case_filter and case["id"] != case_filter:
            continue
        result = run_case(base_url, api_key, model_id, case, domain_meta)
        cases_run.append(result)
        status = "FAIL" if result["error"] else ("PASS" if result["case_pass"] else "FAIL")
        score_str = f"{result['agg_score']:.3f}" if not result["error"] else "ERR"
        print(f"      → {result['case_id']} [{status}] agg={score_str} | {result['latency_ms']}ms")
        time.sleep(PROBE_DELAY)

    valid = [r for r in cases_run if not r["error"]]
    domain_score = round(sum(r["agg_score"] for r in valid) / len(valid), 4) if valid else 0.0
    domain_pass  = all(r["case_pass"] for r in valid) and len(valid) == len(cases_run)

    return {
        "domain":       domain_name,
        "domain_score": domain_score,
        "domain_pass":  domain_pass,
        "cases":        cases_run,
    }


# ---------------------------------------------------------------------------
# Overall weighted score
# ---------------------------------------------------------------------------

def compute_overall(
    domain_results: list[dict],
    weights: dict[str, float],
    passing_threshold: float,
) -> dict:
    """Weighted mean of domain scores."""
    total_weight  = 0.0
    weighted_sum  = 0.0

    for dr in domain_results:
        w = weights.get(dr["domain"], 1.0 / max(len(domain_results), 1))
        weighted_sum  += dr["domain_score"] * w
        total_weight  += w

    overall = round(weighted_sum / total_weight, 4) if total_weight else 0.0
    return {
        "overall_score":     overall,
        "passing":           overall >= passing_threshold,
        "passing_threshold": passing_threshold,
    }


# ---------------------------------------------------------------------------
# Report writer
# ---------------------------------------------------------------------------

def write_report(report: dict, timestamp: str) -> None:
    json_file = f"benchmark_results_{timestamp}.json"
    txt_file  = f"benchmark_results_{timestamp}.txt"

    with open(json_file, "w") as f:
        json.dump(report, f, indent=2)
    print(f"\nJSON report: {json_file}")

    lines = [
        f"AI-OS Benchmark Report — {timestamp}",
        f"Model: {report['model_id']}  |  Suite: {report['suite_version']}  |  Sprint: {report['suite_sprint']}",
        "=" * 70,
    ]
    for dr in report["domains"]:
        status = "PASS" if dr["domain_pass"] else "FAIL"
        lines.append(f"  {dr['domain']:<20} {dr['domain_score']:.3f}  [{status}]")
        for cr in dr["cases"]:
            c_status = "PASS" if cr.get("case_pass") else "FAIL"
            err_str  = f"  ERROR: {cr['error']}" if cr.get("error") else ""
            lines.append(f"    {cr['case_id']:<12} agg={cr.get('agg_score', 0.0):.3f}  [{c_status}]{err_str}")
            for dim, dv in cr.get("dimensions", {}).items():
                d_status = "ok" if dv["pass"] else "FAIL"
                lines.append(f"      {dim:<25} {dv['score']:.3f} >= {dv['min']:.2f}  [{d_status}]  {dv['reason'][:60]}")
    lines += [
        "=" * 70,
        f"Overall: {report['overall_score']:.3f}  |"
        f" {'PASS' if report['passing'] else 'FAIL (min ' + str(report['passing_threshold']) + ')'}",
    ]

    with open(txt_file, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"TXT report:  {txt_file}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="AI-OS Benchmark Harness v2.0")
    parser.add_argument("--base-url",  default="http://localhost:3000", help="Open WebUI base URL")
    parser.add_argument("--api-key",   required=True,                   help="Open WebUI API key")
    parser.add_argument("--model-id",  default="ai-os-nemotron-ultra",  help="Model ID in Open WebUI")
    parser.add_argument("--suite",     default="suite.json",            help="Path to benchmark suite JSON")
    parser.add_argument("--domain",    default=None,                    help="Run only this domain")
    parser.add_argument("--case",      default=None,                    help="Run only this case ID")
    args = parser.parse_args()

    # Load suite
    try:
        with open(args.suite) as f:
            suite = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: suite file not found: {args.suite}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: invalid JSON in {args.suite}: {e}")
        sys.exit(1)

    passing_threshold: float = suite.get("_passing_threshold", 0.75)
    suite_weights: dict      = suite.get("_domain_weights", DEFAULT_DOMAIN_WEIGHTS)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    print(f"\nAI-OS Benchmark Harness v2.0.0")
    print(f"Target  : {args.base_url}")
    print(f"Model   : {args.model_id}")
    print(f"Suite   : {args.suite} (v{suite.get('_version', '?')}, sprint {suite.get('_sprint', '?')})")
    print(f"Time    : {datetime.now(timezone.utc).isoformat()}")
    print("-" * 70)

    domain_results: list[dict] = []

    for domain_name, domain_data in suite.get("domains", {}).items():
        if args.domain and domain_name != args.domain:
            continue
        print(f"\n[{domain_name}] {domain_data.get('description', '')}")
        dr = run_domain(
            args.base_url, args.api_key, args.model_id,
            domain_name, domain_data,
            case_filter=args.case,
        )
        domain_results.append(dr)
        print(f"  Domain score: {dr['domain_score']:.3f} | {'PASS' if dr['domain_pass'] else 'FAIL'}")

    if not domain_results:
        print("ERROR: No domains matched filters.")
        sys.exit(1)

    overall = compute_overall(domain_results, suite_weights, passing_threshold)

    print("\n" + "=" * 70)
    for dr in domain_results:
        print(f"  {dr['domain']:<20} {dr['domain_score']:.3f}  [{'PASS' if dr['domain_pass'] else 'FAIL'}]")
    print("=" * 70)
    print(
        f"Overall: {overall['overall_score']:.3f}  |  "
        f"{'PASS' if overall['passing'] else 'FAIL (min ' + str(passing_threshold) + ')'}"
    )

    # Write report
    report = {
        "schema":            "ai-os/benchmark-report",
        "version":           "2.0.0",
        "timestamp":         timestamp,
        "model_id":          args.model_id,
        "base_url":          args.base_url,
        "suite_version":     suite.get("_version", "?"),
        "suite_sprint":      suite.get("_sprint", "?"),
        "overall_score":     overall["overall_score"],
        "passing":           overall["passing"],
        "passing_threshold": passing_threshold,
        "domain_weights":    suite_weights,
        "domains":           domain_results,
    }
    write_report(report, timestamp)

    sys.exit(0 if overall["passing"] else 1)


if __name__ == "__main__":
    main()
