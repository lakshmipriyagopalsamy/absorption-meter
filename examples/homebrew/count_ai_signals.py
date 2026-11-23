"""Count visible AI-assistance signals per month in a Homebrew/brew checkout.

Signals: commits whose message carries an AI co-author or "generated with" line,
or whose author is a coding-agent bot; and the dates AI instruction files were
first added. Counts only; no names are written.

Usage: python examples/homebrew/count_ai_signals.py PATH_TO_BREW COMMIT
"""

from __future__ import annotations

import re
import subprocess
import sys
from collections import Counter

SIGNAL = re.compile(r"co-authored-by:\s*(github\s*)?(copilot|claude|cursor)|generated with \[?claude|copilot-swe-agent",
                    re.IGNORECASE)
FILES = ("CLAUDE.md", "AGENTS.md", ".github/copilot-instructions.md", ".cursor")


def git(repo: str, *args: str) -> str:
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True,
                          encoding="utf-8", errors="replace").stdout


def main(repo: str, commit: str) -> None:
    raw = git(repo, "log", commit, "--since=2024-07-01", "--until=2026-11-01",
              "--format=%x1e%ad%x1f%an%x1f%B", "--date=format:%Y-%m")
    total, marked = Counter(), Counter()
    for rec in raw.split("\x1e"):
        if not rec.strip():
            continue
        month, author, body = (rec.split("\x1f") + ["", ""])[:3]
        total[month] += 1
        if SIGNAL.search(body) or SIGNAL.search(author):
            marked[month] += 1
    with open("examples/homebrew/ai_signals.csv", "w") as fh:
        fh.write("month,commits,ai_marked_commits\n")
        for month in sorted(total):
            fh.write(f"{month},{total[month]},{marked[month]}\n")
    with open("examples/homebrew/ai_files.csv", "w") as fh:
        fh.write("file,first_added\n")
        for f in FILES:
            dates = git(repo, "log", commit, "--diff-filter=A", "--format=%ad", "--date=short", "--", f).split()
            fh.write(f"{f},{dates[-1] if dates else ''}\n")
    print("wrote examples/homebrew/ai_signals.csv and ai_files.csv")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
