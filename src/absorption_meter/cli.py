"""Command line: ``absorption-meter analyze`` and ``absorption-meter contracts``."""

from __future__ import annotations

import argparse
import os
import sys
from typing import List, Optional

from . import __version__
from .contracts import scan_drift
from .gitlog import read_changes, read_tags
from .metrics import drop_incomplete_last_month, load_team_metrics, monthly
from .pairs import DEBT, HOLD, Settings, evaluate, recommend
from .report import to_json, to_markdown


def _common(p: argparse.ArgumentParser) -> None:
    p.add_argument("path", nargs="?", default=".", help="path to a git repository (default: .)")
    p.add_argument("--branch", default="HEAD", help="branch or ref to read (default: HEAD)")
    p.add_argument("--since", help="only changes after this date, e.g. 2024-01-01")
    p.add_argument("--until", help="only changes before this date")
    p.add_argument("--include-bots", action="store_true", help="keep dependency-bot changes")
    p.add_argument("--as-of", help="analysis date, YYYY-MM-DD: changes whose rework window has not closed "
                   "by then are left out (default: today, or --until if given; for a dataset, the date it "
                   "was read)")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="absorption-meter",
        description="Paired delivery metrics: see when change production outruns absorption capacity.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command", required=True)

    a = sub.add_parser("analyze", help="paired metrics and monthly table")
    _common(a)
    a.add_argument("--rework-window", type=int, default=14, help="days after a change to look for rework (default 14)")
    a.add_argument("--late-window", type=int, default=90,
                   help="days for late rework: fixes after the rework window but within this many days (default 90)")
    a.add_argument("--recent", type=int, default=3, help="months in the recent window (default 3)")
    a.add_argument("--baseline", type=int, default=6, help="months in the trailing baseline (default 6)")
    a.add_argument("--k", type=float, default=1.0, help="baseline spreads a move must exceed (default 1)")
    a.add_argument("--robust", action="store_true",
                   help="use the baseline median and MAD instead of mean and standard deviation (resists outliers)")
    a.add_argument("--input", metavar="JSONL", help="analyze an exported dataset instead of a repository")
    a.add_argument("--team-metrics", metavar="CSV", help="team-reported monthly measures: month, recovery_hours, "
                   "time_to_detect_hours, telemetry_coverage, mutation_score, critical_verified, escaped_defects, "
                   "days_to_first_defect, change_failure_rate, deployments")
    a.add_argument("--no-contracts", action="store_true", help="skip the contract-drift scan")
    a.add_argument("--github", metavar="OWNER/REPO", help="add pull-request measures from the GitHub API")
    a.add_argument("--max-prs", type=int, default=300, help="most PRs to read from GitHub (default 300)")
    a.add_argument("--prs", metavar="JSON", help="pull-request data saved as JSON (the records --github reads), "
                   "instead of calling the GitHub API")
    a.add_argument("--format", choices=("markdown", "json"), default="markdown")
    a.add_argument("--output", "-o", help="write the report to this file instead of stdout")
    a.add_argument("--keep-current-month", action="store_true", help="keep the unfinished current month")
    a.add_argument("--fail-on-signal", action="store_true",
                   help="exit with status 2 if any pair signals debt or the decision is hold")

    e = sub.add_parser("export", help="write the history as a portable dataset (no names, e-mails or messages)")
    _common(e)
    e.add_argument("--output", "-o", required=True, help="dataset file to write (JSON lines)")
    e.add_argument("--source", default="", help="description of the source, e.g. a public repository URL")
    e.add_argument("--no-contracts", action="store_true", help="skip the contract-drift scan")

    c = sub.add_parser("contracts", help="list contract changes that broke compatibility")
    _common(c)
    c.add_argument("--all", action="store_true", help="also list breaking changes that bumped the major version")
    return parser


def _write(text: str, output: Optional[str]) -> None:
    if output:
        with open(output, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary and output != summary and os.environ.get("ABSORPTION_METER_SUMMARY") == "1":
        with open(summary, "a", encoding="utf-8") as fh:
            fh.write(text)


def _stamp(day: str) -> int:
    from datetime import datetime, timezone

    return int(datetime.strptime(day, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())


def _within(ts: int, since: Optional[str], until: Optional[str]) -> bool:
    return (not since or ts >= _stamp(since)) and (not until or ts < _stamp(until))


def _as_of(args, dataset_meta: Optional[dict] = None) -> Optional[int]:
    """The analysis date: --as-of, else --until, else the dataset's read date, else now (live repository).

    Older datasets that record no read date fall back to the newest change (None), which is conservative.
    """
    if getattr(args, "as_of", None):
        return _stamp(args.as_of)
    if args.until:
        return _stamp(args.until)
    if dataset_meta is not None:
        return dataset_meta.get("as_of")
    import time

    return int(time.time())


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)

    if args.command == "analyze" and args.input:
        from .dataset import load

        meta, changes, tags, drift = load(args.input)
        changes = [c for c in changes if _within(c.timestamp, args.since, args.until)]
        drift = [d for d in drift if _within(d.timestamp, args.since, args.until)]
        name = meta.get("source") or os.path.basename(args.input)
        return _analyze(args, name, changes, tags, drift, _as_of(args, meta))

    repo = os.path.abspath(args.path)
    name = os.path.basename(repo.rstrip(os.sep))
    changes = read_changes(repo, args.branch, args.since, args.until, include_bots=args.include_bots)
    # git applies --since/--until in local time; trim to exact UTC days so results don't depend on time zone.
    changes = [c for c in changes if _within(c.timestamp, args.since, args.until)]

    if args.command == "export":
        from .dataset import save
        from .gitlog import _git

        drift = [] if args.no_contracts else scan_drift(repo, changes)
        commit = _git(repo, ["rev-parse", args.branch]).strip()
        save(args.output, changes, read_tags(repo), drift, args.source or name, commit, _as_of(args))
        print(f"wrote {len(changes)} changes and {len(drift)} drift events to {args.output} (commit {commit[:12]})")
        return 0

    if args.command == "contracts":
        events = scan_drift(repo, changes)
        shown = [e for e in events if args.all or e.is_drift]
        if not shown:
            print("No contract drift found.")
        for e in shown:
            print(f"{e.sha[:8]}  {e.path}  {e.old_version} -> {e.new_version}  [{e.kind}]")
            for b in e.breaking:
                print(f"    {b}")
        return 0

    drift = [] if args.no_contracts else scan_drift(repo, changes)
    return _analyze(args, name, changes, read_tags(repo), drift, _as_of(args))


def _analyze(args, name, changes, tags, drift, as_of: Optional[int] = None) -> int:
    prs, reviewed, reviewed_from = None, None, None
    if args.prs or args.github:
        from .github import earliest_merge, fetch_merged_prs, reviewed_map

        if args.prs:
            import json

            with open(args.prs, encoding="utf-8") as fh:
                prs = json.load(fh)
        else:
            prs = fetch_merged_prs(args.github, args.since, args.max_prs)
        reviewed, reviewed_from = reviewed_map(prs), earliest_merge(prs)
    analysis = monthly(changes, tags, drift, args.rework_window, as_of=as_of, late_window_days=args.late_window,
                       reviewed=reviewed, reviewed_from=reviewed_from)
    if not args.keep_current_month:
        analysis = drop_incomplete_last_month(analysis)
    if prs is not None:
        from .github import merge_into, pr_monthly

        merge_into(analysis, pr_monthly(prs))
        name = args.github or name
    if args.team_metrics:
        load_team_metrics(analysis, args.team_metrics)
    settings = Settings(recent=args.recent, baseline=args.baseline, k=args.k, robust=args.robust)
    pairs = evaluate(analysis, settings)
    rec = recommend(analysis, settings)

    render = to_json if args.format == "json" else to_markdown
    _write(render(name, analysis, pairs, rec), args.output)
    if args.fail_on_signal and (rec.verdict == HOLD or any(p.status == DEBT for p in pairs)):
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
