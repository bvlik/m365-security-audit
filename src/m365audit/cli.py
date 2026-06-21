"""Command-line entrypoint: python -m m365audit"""
from __future__ import annotations

import argparse
import sys

from .checks import ALL_CHECKS
from .config import Settings
from .graph import GraphClient, GraphError
from .models import CheckResult, Severity
from . import report


def run(formats: list[str]) -> int:
    settings = Settings.from_env()
    client = GraphClient(settings)

    results: list[CheckResult] = []
    for check in ALL_CHECKS:
        try:
            findings = check.run(client, settings)
            results.append(CheckResult(check.id, check.title, findings))
        except GraphError as exc:
            results.append(CheckResult(check.id, check.title, [], error=str(exc)))

    if "console" in formats:
        report.to_console(results)
    if "json" in formats:
        report.to_json(results)
        print("Wrote report.json")

    # Exit non-zero if any High+ finding (useful in CI).
    worst = max(
        (f.severity for r in results for f in r.findings),
        default=Severity.INFO,
    )
    return 1 if worst >= Severity.HIGH else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="m365audit", description="Read-only M365 security audit")
    parser.add_argument(
        "--format",
        default="console",
        help="comma-separated: console,json (default: console)",
    )
    args = parser.parse_args(argv)
    return run([f.strip() for f in args.format.split(",") if f.strip()])


if __name__ == "__main__":
    sys.exit(main())
