"""
AI-OS Benchmark Runner
Version: 1.0.0
Responsibility: Execute benchmark fixtures against the AI-OS runtime and
                produce a scored report per dimension defined in suite.json.
Rationale: Benchmarks are only meaningful if they are executable. This
           runner loads fixtures from benchmark/fixtures/, sends them to
           the Open WebUI API (or directly to NIM), and scores each response
           against the rubric in suite.json. Results are written to
           benchmark/results/ as JSON and Markdown.
Usage:
  python runner.py --host http://localhost:3000 --api-key $OPENWEBUI_API_KEY
  python runner.py --nim-direct --api-key $NVIDIA_API_KEY
  python runner.py --dry-run   # validate fixtures without API calls
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import requests
except ImportError:
    print("[ERROR] 'requests' library not found. Install with: pip install requests")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
ROOT = Path(__file__).parent
SUITE_FILE = ROOT / "suite.json"
FIXTURES_DIR = ROOT / "fixtures"
RESULTS_DIR = ROOT / "results"


# ---------------------------------------------------------------------------
# API Client
# ---------------------------------------------------------------------------
class NIMClient:
    """Thin OpenAI-compatible client for NIM or Open WebUI."""

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.model = model
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json',
        })

    def chat(self, messages: list[dict], params: dict) -> dict:
        payload = {
            'model': self.model,
            'messages': messages,
            **params,
        }
        t0 = time.perf_counter()
        resp = self.session.post(
            f'{self.base_url}/chat/completions',
            json=payload,
            timeout=120,
        )
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        resp.raise_for_status()
        data = resp.json()
        content = data['choices'][0]['message']['content']
        tokens_in = data.get('usage', {}).get('prompt_tokens', 0)
        tokens_out = data.get('usage', {}).get('completion_tokens', 0)
        return {
            'content': content,
            'tokens_in': tokens_in,
            'tokens_out': tokens_out,
            'latency_ms': elapsed_ms,
        }


# ---------------------------------------------------------------------------
# Scorer
# ---------------------------------------------------------------------------
class BenchmarkScorer:
    """Score a single response against a metric definition."""

    def score_metric(self, metric: dict, response: str, context: dict) -> float:
        mid = metric['id']

        # --- Discussion Quality ---
        if mid == 'DQ-01':  # Answer-first rate
            fillers = ['great question', 'certainly', 'of course', 'absolutely', 'sure']
            first_50 = response[:200].lower()
            for f in fillers:
                if first_50.startswith(f):
                    return 0.0
            return float(metric['score_pass'])

        if mid == 'DQ-02':  # Prohibited pattern absence
            fillers = re.findall(
                r'\b(great question|certainly!|of course|absolutely|sure thing|definitely)\b',
                response, re.IGNORECASE
            )
            count = len(fillers)
            return round(10.0 * max(0.0, 1.0 - count / 3.0), 2)

        if mid == 'DQ-03':  # Length compliance
            target = context.get('length_target', 500)
            actual = len(response) // 4
            ratio = actual / target if target else 1.0
            return 10.0 if 0.5 <= ratio <= 1.5 else 0.0

        # --- Reasoning ---
        if mid == 'RS-01':  # Framework application
            frameworks = ['first principles', 'trade-off', 'pros and cons', 'requirements',
                          'constraints', 'because', 'therefore', 'given that']
            for f in frameworks:
                if f.lower() in response.lower():
                    return 20.0
            return 0.0

        if mid == 'RS-02':  # Assumption surfacing
            assumptions = re.findall(
                r'\b(assum|presuppos|given that|assuming|if we assume)',
                response, re.IGNORECASE
            )
            return min(len(assumptions) * 5.0, 15.0)

        if mid == 'RS-03':  # Uncertainty calibration
            verify_tags = re.findall(r'\[verify\]', response, re.IGNORECASE)
            uncertain_markers = re.findall(
                r'\b(may|might|could|approximately|roughly|unclear|uncertain)\b',
                response, re.IGNORECASE
            )
            if not uncertain_markers:
                return 15.0  # No uncertain claims = no verify tags needed
            ratio = min(len(verify_tags) / len(uncertain_markers), 1.0)
            return round(15.0 * ratio, 2)

        # --- Architecture ---
        if mid == 'AR-01':  # Structure completeness
            sections = ['requirement', 'constraint', 'component', 'interface', 'failure', 'trade']
            covered = sum(1 for s in sections if s in response.lower())
            return round(covered / 6.0 * 30.0, 2)

        if mid == 'AR-02':  # Trade-off explicitness
            return 20.0 if re.search(r'trade.off|versus|vs\.|on the other hand', response, re.IGNORECASE) else 0.0

        # --- Coding ---
        if mid == 'CD-01':  # Syntax correctness (heuristic: check for code fence)
            return 40.0 if re.search(r'```[a-z]', response) else 20.0

        if mid == 'CD-02':  # Test coverage present
            return 10.0 if re.search(r'\btest|assert|pytest|unittest\b', response, re.IGNORECASE) else 0.0

        # --- Memory ---
        if mid == 'ME-01':  # Relevant memory loaded (context check)
            return context.get('memory_score', 25.0)

        if mid == 'ME-02':  # No stale memory
            return context.get('memory_fresh_score', 25.0)

        # --- Knowledge ---
        if mid == 'KN-01':  # Citation rate
            return 50.0 if re.search(r'\[Source:', response) else 0.0

        # --- Planner ---
        if mid == 'PL-01':  # Planner activation accuracy
            return context.get('planner_score', 50.0)

        # --- Reflection ---
        if mid == 'RF-01':
            return context.get('reflection_score', 50.0)

        # --- Critic ---
        if mid == 'CR-01':
            return context.get('critic_score', 50.0)

        # --- Tool Usage ---
        if mid == 'TU-01':  # Minimum tools principle
            unnecessary = context.get('unnecessary_tool_calls', 0)
            return max(0.0, 50.0 - unnecessary * 10.0)

        if mid == 'TU-02':  # Batching compliance
            return context.get('batching_score', 50.0)

        # --- Conversation Consistency ---
        if mid == 'CC-01':
            contradiction_rate = context.get('contradiction_rate', 0.0)
            return round(50.0 * (1.0 - contradiction_rate), 2)

        # --- Long Context ---
        if mid == 'LC-01':
            return context.get('compression_score', 25.0)

        if mid == 'LC-02':
            return context.get('budget_compliance_score', 25.0)

        return 0.0


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------
class BenchmarkRunner:
    def __init__(self, client: NIMClient | None, dry_run: bool = False):
        self.client = client
        self.dry_run = dry_run
        self.scorer = BenchmarkScorer()
        self.suite = json.loads(SUITE_FILE.read_text())
        RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    def load_fixtures(self) -> list[dict]:
        fixtures = []
        if not FIXTURES_DIR.exists():
            print(f"[WARN] Fixtures directory not found: {FIXTURES_DIR}")
            return []
        for f in sorted(FIXTURES_DIR.glob('*.json')):
            fixtures.append(json.loads(f.read_text()))
        return fixtures

    def run_fixture(self, fixture: dict) -> dict:
        """Run a single fixture and return scored result."""
        fid = fixture['id']
        task_class = fixture.get('task_class', 'conversational')
        messages = fixture.get('messages', [])
        params = fixture.get('params', {})
        context = fixture.get('scoring_context', {})
        context['length_target'] = fixture.get('length_target', 500)

        print(f"  [{fid}] {task_class}: {fixture.get('description', '')[:60]}")

        if self.dry_run:
            response_text = f"[DRY RUN] fixture={fid}"
            latency_ms = 0
            tokens_in, tokens_out = 0, 0
        else:
            try:
                result = self.client.chat(messages, params)
                response_text = result['content']
                latency_ms = result['latency_ms']
                tokens_in = result['tokens_in']
                tokens_out = result['tokens_out']
            except Exception as e:
                print(f"  [ERROR] {fid}: {e}")
                response_text = ""
                latency_ms = -1
                tokens_in = tokens_out = 0

        # Score each metric for this fixture
        dimension = fixture.get('dimension')
        dim_config = self.suite['dimensions'].get(dimension, {})
        metrics = dim_config.get('metrics', [])
        metric_scores = {}
        total = 0.0
        for metric in metrics:
            s = self.scorer.score_metric(metric, response_text, context)
            metric_scores[metric['id']] = s
            total += s

        return {
            'fixture_id': fid,
            'dimension': dimension,
            'task_class': task_class,
            'metric_scores': metric_scores,
            'dimension_raw_score': round(total, 2),
            'latency_ms': latency_ms,
            'tokens_in': tokens_in,
            'tokens_out': tokens_out,
        }

    def run_all(self) -> dict:
        fixtures = self.load_fixtures()
        print(f"\n[AI-OS Benchmark] Running {len(fixtures)} fixture(s)...\n")

        raw_results: list[dict] = []
        for fixture in fixtures:
            result = self.run_fixture(fixture)
            raw_results.append(result)

        # Aggregate scores per dimension
        dim_scores: dict[str, list[float]] = {}
        for r in raw_results:
            dim = r['dimension']
            if dim:
                dim_scores.setdefault(dim, []).append(r['dimension_raw_score'])

        # Compute weighted total
        dimensions_config = self.suite['dimensions']
        weighted_total = 0.0
        dimension_summary = {}
        for dim_id, scores in dim_scores.items():
            avg = sum(scores) / len(scores)
            max_s = dimensions_config.get(dim_id, {}).get('max_score', 50)
            normalised = round((avg / max_s) * 100, 1) if max_s else 0.0
            weight = dimensions_config.get(dim_id, {}).get('weight', 0.0)
            weighted_total += normalised * weight
            dimension_summary[dim_id] = {
                'average_raw': round(avg, 2),
                'max_possible': max_s,
                'normalised_score': normalised,
                'weight': weight,
                'fixture_count': len(scores),
            }

        passing = self.suite['scoring']['minimum_passing_score']
        final_score = round(weighted_total, 1)
        passed = final_score >= passing

        report = {
            'schema': 'ai-os/benchmark-result',
            'version': '1.0.0',
            'generated': datetime.now(timezone.utc).isoformat(),
            'dry_run': self.dry_run,
            'total_fixtures': len(fixtures),
            'final_score': final_score,
            'minimum_passing': passing,
            'passed': passed,
            'dimension_summary': dimension_summary,
            'raw_results': raw_results,
        }
        return report

    def save_report(self, report: dict) -> Path:
        ts = datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')
        out_json = RESULTS_DIR / f"run_{ts}.json"
        out_md = RESULTS_DIR / f"run_{ts}.md"
        out_json.write_text(json.dumps(report, indent=2))
        md = self._render_markdown(report)
        out_md.write_text(md)
        return out_json

    def _render_markdown(self, report: dict) -> str:
        lines = [
            "# AI-OS Benchmark Report",
            f"",
            f"**Generated**: {report['generated']}",
            f"**Dry Run**: {report['dry_run']}",
            f"**Fixtures**: {report['total_fixtures']}",
            f"",
            f"## Final Score: {report['final_score']} / 100",
            f"**Status**: {'✅ PASSED' if report['passed'] else '❌ FAILED'} "
            f"(minimum: {report['minimum_passing']})",
            f"",
            "## Dimension Scores",
            "",
            "| Dimension | Normalised | Weight | Raw Avg / Max | Fixtures |",
            "|-----------|-----------|--------|--------------|----------|",
        ]
        for dim_id, d in report['dimension_summary'].items():
            status = '✅' if d['normalised_score'] >= 50 else '⚠️'
            lines.append(
                f"| {status} {dim_id} | {d['normalised_score']}% | "
                f"{d['weight']} | {d['average_raw']}/{d['max_possible']} | {d['fixture_count']} |"
            )
        lines += ["", "## Raw Results", ""]
        for r in report['raw_results']:
            lines.append(
                f"- **{r['fixture_id']}** ({r['task_class']}) | "
                f"score={r['dimension_raw_score']} | "
                f"{r['latency_ms']}ms | {r['tokens_out']} out-tokens"
            )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description='AI-OS Benchmark Runner')
    parser.add_argument('--host', default='http://localhost:3000', help='Open WebUI base URL')
    parser.add_argument('--nim-direct', action='store_true',
                        help='Connect directly to NVIDIA NIM instead of Open WebUI')
    parser.add_argument('--model', default='nvidia/nemotron-3-ultra-550b-a55b')
    parser.add_argument('--api-key', default=os.environ.get('NVIDIA_API_KEY', ''),
                        help='API key (or set NVIDIA_API_KEY env var)')
    parser.add_argument('--dry-run', action='store_true',
                        help='Validate fixtures without making API calls')
    args = parser.parse_args()

    if args.nim_direct:
        base_url = 'https://integrate.api.nvidia.com/v1'
    else:
        base_url = args.host + '/api'

    if not args.dry_run and not args.api_key:
        print('[ERROR] --api-key or NVIDIA_API_KEY env var required.')
        sys.exit(1)

    client = None if args.dry_run else NIMClient(base_url, args.api_key, args.model)
    runner = BenchmarkRunner(client=client, dry_run=args.dry_run)

    report = runner.run_all()
    out_path = runner.save_report(report)

    print(f"\n{'=' * 60}")
    print(f"FINAL SCORE : {report['final_score']} / 100")
    print(f"STATUS      : {'PASSED ✅' if report['passed'] else 'FAILED ❌'}")
    print(f"REPORT      : {out_path}")
    print(f"{'=' * 60}\n")

    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
