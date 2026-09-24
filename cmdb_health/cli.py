"""Command-line entry point: python -m cmdb_health.cli --cis data/cis.json --rels data/rels.json"""
from __future__ import annotations

import argparse
import csv
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from .analyzer import analyze


def load_records(path: Path) -> list[dict]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8") as fh:
            return list(csv.DictReader(fh))
    data = json.loads(path.read_text(encoding="utf-8"))
    # Accept raw Table API payloads ({"result": [...]}) or plain lists.
    return data["result"] if isinstance(data, dict) and "result" in data else data


def render_markdown(summary: dict, findings: list) -> str:
    lines = [
        "# CMDB Health Report",
        "",
        f"Generated: {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}  ",
        f"CIs evaluated: **{summary['total_cis']}**",
        "",
        "| KPI | Score |",
        "|---|---|",
        f"| Completeness | {summary['completeness']}% |",
        f"| Correctness | {summary['correctness']}% |",
        f"| Compliance | {summary['compliance']}% |",
        "",
        "## Findings by rule",
        "",
        "| Rule | Count |",
        "|---|---|",
    ]
    lines += [f"| {rule} | {count} |" for rule, count in summary["findings_by_rule"].items()]
    lines += ["", "## Remediation queue", "", "| CI | KPI | Rule | Detail |", "|---|---|---|---|"]
    lines += [f"| {f.ci_name} | {f.kpi} | {f.rule} | {f.detail} |" for f in findings]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Score CMDB health from an export.")
    parser.add_argument("--cis", type=Path, required=True, help="CI export (.json or .csv)")
    parser.add_argument("--rels", type=Path, required=True, help="cmdb_rel_ci export (.json or .csv)")
    parser.add_argument("--stale-days", type=int, default=30)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    parser.add_argument("--out", type=Path, help="Write report to file instead of stdout")
    parser.add_argument("--min-score", type=float, default=0.0,
                        help="Exit non-zero if any KPI falls below this (useful in pipelines)")
    parser.add_argument("-v", "--verbose", action="store_true")
    args = parser.parse_args(argv)

    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s")
    try:
        report = analyze(load_records(args.cis), load_records(args.rels),
                         stale_after_days=args.stale_days)
    except (FileNotFoundError, json.JSONDecodeError, KeyError) as exc:
        logging.error("Could not load input: %s", exc)
        return 2

    summary = report.summary()
    if args.format == "json":
        output = json.dumps({"summary": summary,
                             "findings": [f.__dict__ for f in report.findings]}, indent=2)
    else:
        output = render_markdown(summary, report.findings)

    if args.out:
        args.out.write_text(output, encoding="utf-8")
        logging.info("Report written to %s", args.out)
    else:
        sys.stdout.write(output)

    worst = min(summary["completeness"], summary["correctness"], summary["compliance"])
    return 1 if worst < args.min_score else 0


if __name__ == "__main__":
    raise SystemExit(main())
