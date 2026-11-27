"""Collect one field-test project from a local clone (run once; the outputs are committed).

Writes examples/field-tests/<name>/changes.jsonl.gz (the absorption-meter dataset, July 2024 to October 2026,
no names, e-mails or messages) and markers.json (when AI-instruction files were first added, and the share
of commits with a visible AI co-author or agent signature, before and after that date). Everything else
is regenerated from these by scripts/reproduce.sh, offline.

Usage: python scripts/collect_field_test.py NAME OWNER/REPO PATH_TO_CLONE [--markers-only]
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys

SINCE, UNTIL = "2024-07-01", "2026-11-01"
FILES = ("AGENTS.md", "CLAUDE.md", ".github/copilot-instructions.md", ".cursorrules", "GEMINI.md", ".cursor")
SIGNAL = re.compile(r"co-authored-by:[^\n]*(copilot|claude|cursor|gemini|codex|devin|aider)|generated with \[?claude|"
                    r"copilot-swe-agent|\(cursor\)|codex", re.IGNORECASE)


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env={**os.environ, "TZ": "UTC"}).stdout


def main(name: str, owner_repo: str, clone: str) -> None:
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out = os.path.join(root, "examples", "field-tests", name)
    os.makedirs(out, exist_ok=True)
    head = git(clone, "rev-parse", "HEAD").strip()
    if "--markers-only" not in sys.argv:
        subprocess.run(["absorption-meter", "export", clone, "--since", SINCE, "--until", UNTIL, "--as-of", UNTIL,
                        "--source", f"https://github.com/{owner_repo}", "-o", os.path.join(out, "changes.jsonl.gz")],
                       check=True)

    first_added = {}
    for f in FILES:
        dates = git(clone, "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", f).split()
        if dates:
            first_added[f] = dates[-1]
    marker = min(first_added.values()) if first_added else None

    # Filter dates here, not with git's --since/--until: those stop early when commit dates are out of
    # order, which made the counts vary between runs. Committer dates in UTC, matching the dataset.
    raw = git(clone, "log", "--first-parent", "--format=%x1e%cd%x1f%B", "--date=format-local:%Y-%m-%d")
    before = after = before_ai = after_ai = 0
    for rec in raw.split("\x1e"):
        if not rec.strip():
            continue
        date, _, body = rec.partition("\x1f")
        if not (SINCE <= date < UNTIL):
            continue
        is_ai = bool(SIGNAL.search(body))
        if marker and date >= marker:
            after += 1; after_ai += is_ai
        else:
            before += 1; before_ai += is_ai
    markers = {
        "repository": f"https://github.com/{owner_repo}",
        "commit": head,
        "window": [SINCE, UNTIL],
        "ai_instruction_files_first_added": first_added,
        "adoption_marker": marker,
        "mainline_commits_before_marker": before,
        "mainline_commits_after_marker": after,
        "ai_signed_share_before": round(before_ai / before, 4) if before else None,
        "ai_signed_share_after": round(after_ai / after, 4) if after else None,
        "note": "AI-instruction files mark project-level adoption, not how much code AI wrote. AI signatures "
                "(co-author trailers, agent names) undercount AI use.",
    }
    with open(os.path.join(out, "markers.json"), "w") as fh:
        json.dump(markers, fh, indent=1)
        fh.write("\n")
    print(f"{name}: commit {head[:12]}, marker {marker}")


if __name__ == "__main__":
    main(*[a for a in sys.argv[1:] if a != "--markers-only"][:3])
