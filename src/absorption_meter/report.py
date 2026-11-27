"""Render an analysis as Markdown or JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from typing import List

from . import __version__
from .metrics import Analysis
from .pairs import DEBT, PairResult, Recommendation

_STATUS = {"debt-signal": "⚠️ debt signal", "no-signal": "✅ no signal", "insufficient-data": "… not enough data"}

_VERDICT = {
    "scale": "🟢 **Scale cautiously**",
    "hold": "🔴 **Hold**",
    "address": "🟡 **Address**",
    "insufficient-data": "⚪ **Not enough history**",
}


def _fmt(value) -> str:
    if value is None:
        return "–"
    if isinstance(value, float):
        return f"{value:.2f}" if abs(value) < 10 else f"{value:.0f}"
    return str(value)


def to_markdown(name: str, analysis: Analysis, pairs: List[PairResult], rec: Recommendation) -> str:
    out: List[str] = []
    out.append(f"# Absorption report: {name}")
    out.append("")
    out.append(
        f"{analysis.total_changes} mainline changes, {analysis.first} to {analysis.last}. "
        f"Rework window {analysis.rework_window_days} days ({analysis.rework_rule} rule). "
        f"Deployment frequency uses {'releases (tags)' if analysis.releases_used else 'merged changes'}. "
        f"Pull-request data: {'yes' if analysis.pr_data else 'no'}. "
        f"Team data: {'yes' if analysis.team_data else 'no'}."
    )
    out.append("")
    out.append("## Decision")
    out.append("")
    out.append(f"{_VERDICT[rec.verdict]}: {rec.reading}")
    out.append("")
    if rec.cautions:
        out.append("**Cautions: AR_repo may overstate absorption**")
        out.append("")
        for c in rec.cautions:
            out.append(f"- {c}")
        out.append("")
    if rec.actions:
        out.append("Suggested order: protect contracts and verify critical behavior first, and close telemetry "
                   "gaps that block diagnosis; move simplification earlier when change cost is the dominant "
                   "constraint. The order is a hypothesis, not a finding.")
        out.append("")
        for action in rec.actions:
            out.append(f"1. {action}")
        out.append("")
    out.append("## Paired metrics")
    out.append("")
    out.append("A DORA metric that improves or holds while its paired indicator worsens signals hidden delivery debt.")
    out.append("")
    out.append("| Pair | DORA metric (lags) | Indicator (leads) | Status | Reading |")
    out.append("|---|---|---|---|---|")
    for p in pairs:
        out.append(f"| {p.pair} | {p.dora} | {p.signal} | {_STATUS[p.status]} | {p.reading} |")
    out.append("")

    out.append("## Month by month")
    out.append("")
    cols = [("month", "Month"), ("changes", "Changes"), ("absorption_ratio", "AR_repo"), ("rework_rate", "Rework"),
            ("untested_share", "Untested"), ("late_rework_rate", "Late rework"),
            ("median_lines", "Median lines"), ("mean_dirs", "Areas/change"), ("revert_rate", "Reverts"),
            ("releases", "Releases"), ("recovery_hours", "Recovery h"), ("contract_drift", "Drift")]
    if analysis.pr_data:
        cols += [("median_lead_hours", "Lead h"), ("median_first_review_hours", "1st review h"),
                 ("review_comments_per_100_lines", "Comments/100 lines"), ("unreviewed_share", "Unreviewed"),
                 ("examined_absorption_ratio", "Examined AR")]
    if analysis.team_data:
        team = [("time_to_detect_hours", "Detect h"), ("telemetry_coverage", "Telemetry"),
                ("mutation_score", "Mutation"), ("critical_verified", "Critical verified"),
                ("escaped_defects", "Escaped defects"), ("days_to_first_defect", "Days to 1st defect")]
        cols += [(a, l) for a, l in team if any(getattr(r, a) is not None for r in analysis.months)]
    out.append("| " + " | ".join(label for _, label in cols) + " |")
    out.append("|" + "---|" * len(cols))
    for row in analysis.months:
        out.append("| " + " | ".join(_fmt(getattr(row, attr)) for attr, _ in cols) + " |")
    out.append("")

    drift = [e for e in analysis.drift_events if e.is_drift]
    if drift:
        out.append("## Contract drift")
        out.append("")
        for e in drift:
            when = datetime.fromtimestamp(e.timestamp, tz=timezone.utc).strftime("%Y-%m-%d")
            listed = "; ".join(str(b) for b in e.breaking[:5])
            more = f" (+{len(e.breaking) - 5} more)" if len(e.breaking) > 5 else ""
            out.append(f"- {when} `{e.sha[:8]}` `{e.path}`: version {e.old_version} → {e.new_version} "
                       f"({e.kind}): {listed}{more}")
        out.append("")

    out.append("## Reading this report")
    out.append("")
    out.append("AR_repo is the repository proxy for the absorption ratio: the size-weighted share of changes not "
               "reworked within the window. The full model's AR also requires a first-run CI pass, which version "
               "control does not record, so this tool reports AR_repo. Every measure is a proxy. Rework counts reverts and fix-like follow-ups to the same files; it "
               "misses silent fixes and can count unrelated fixes to busy files, so read trends, not levels: each "
               "measure is compared with this repository's own trailing baseline. The most recent "
               f"{analysis.rework_window_days} days are left out of rework because their window hasn't closed.")
    out.append("")
    out.append("Low rework can mean a change was solid, or that nobody looked closely and its defects surfaced "
               "later. Late rework (fixes "
               f"{analysis.rework_window_days + 1}-{analysis.late_window_days} days after merging, shown once that "
               "window has closed), examined absorption and unreviewed share (with --github), and escaped defects "
               "(team data) help tell the two apart; when they point the other way, the report lists cautions.")
    out.append("")
    out.append(f"_absorption-meter {__version__}_")
    return "\n".join(out) + "\n"


def to_json(name: str, analysis: Analysis, pairs: List[PairResult], rec: Recommendation) -> str:
    payload = {
        "tool": "absorption-meter",
        "version": __version__,
        "repository": name,
        # absorption_ratio below is AR_repo: the repository proxy, without the first-run CI term of the full AR.
        "absorption_ratio_kind": "AR_repo",
        "analysis": asdict(analysis),
        "decision": asdict(rec),
        "pairs": [asdict(p) for p in pairs],
    }
    for event in payload["analysis"]["drift_events"]:
        event["breaking"] = [f"{b['kind']} at {b['location']}" for b in event["breaking"]]
    return json.dumps(payload, indent=2, ensure_ascii=False) + "\n"
