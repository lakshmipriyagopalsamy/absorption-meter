"""Read a repository's mainline history as a list of changes.

A *change* is one commit on the first-parent history of a branch: a merge commit,
a squash-merged pull request, or a direct commit. For merge commits the diff is
taken against the first parent, so a merged pull request counts once, with its
full size.
"""

from __future__ import annotations

import re
import subprocess
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Iterable, List, Optional, Sequence, Tuple

_REC = "\x1e"
_FLD = "\x1f"
_END = "\x1d"

# Files that change mechanically and would distort change size.
DEFAULT_EXCLUDES: Tuple[str, ...] = (
    r"(^|/)(package-lock\.json|npm-shrinkwrap\.json|yarn\.lock|pnpm-lock\.yaml|poetry\.lock|"
    r"Pipfile\.lock|uv\.lock|Cargo\.lock|go\.sum|composer\.lock|Gemfile\.lock|packages\.lock\.json)$",
    r"(^|/)(vendor|node_modules|dist|build|third_party)/",
    r"\.min\.(js|css)$",
    r"(^|/)__snapshots__/",
    r"\.snap$",
    r"\.(png|jpe?g|gif|svg|ico|pdf|woff2?|ttf|eot|zip|gz|jar)$",
)

_BOT = re.compile(r"(\[bot\]|dependabot|renovate|github-actions|greenkeeper)", re.IGNORECASE)
_REVERTS = re.compile(r"This reverts commit ([0-9a-f]{7,40})", re.IGNORECASE)


@dataclass
class FileChange:
    path: str
    added: int
    deleted: int

    @property
    def lines(self) -> int:
        return self.added + self.deleted


@dataclass
class Change:
    sha: str
    timestamp: int
    parents: List[str]
    author_email: str
    subject: str
    body: str = ""
    files: List[FileChange] = field(default_factory=list)

    @property
    def lines(self) -> int:
        return sum(f.lines for f in self.files)

    @property
    def paths(self) -> List[str]:
        return [f.path for f in self.files]

    @property
    def top_dirs(self) -> set:
        """Top-level directories touched; files at the root count as '.'."""
        return {p.split("/", 1)[0] if "/" in p else "." for p in self.paths}

    @property
    def is_merge(self) -> bool:
        return len(self.parents) > 1

    @property
    def is_bot(self) -> bool:
        return bool(_BOT.search(self.author_email)) or bool(_BOT.search(self.subject))

    @property
    def month(self) -> str:
        return month_of(self.timestamp)

    @property
    def reverted_sha(self) -> Optional[str]:
        m = _REVERTS.search(self.body) or _REVERTS.search(self.subject)
        return m.group(1).lower() if m else None


def month_of(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).strftime("%Y-%m")


def _git(repo: str, args: Sequence[str]) -> str:
    result = subprocess.run(
        ["git", "-C", repo, *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    return result.stdout


def _excluded(path: str, patterns: Iterable[re.Pattern]) -> bool:
    return any(p.search(path) for p in patterns)


def read_changes(
    repo: str,
    branch: str = "HEAD",
    since: Optional[str] = None,
    until: Optional[str] = None,
    excludes: Sequence[str] = DEFAULT_EXCLUDES,
    include_bots: bool = False,
) -> List[Change]:
    """Return the first-parent changes of ``branch``, oldest first.

    Excluded files are dropped from each change. Changes left with no files
    (for example lockfile-only updates) and, unless ``include_bots``, changes by
    dependency bots are dropped entirely.
    """
    fmt = f"{_REC}%H{_FLD}%at{_FLD}%P{_FLD}%ae{_FLD}%s{_FLD}%b{_END}"
    args = ["log", "--first-parent", "-m", "--numstat", "--no-renames", f"--format={fmt}"]
    if since:
        args.append(f"--since={since}")
    if until:
        args.append(f"--until={until}")
    args.append(branch)
    raw = _git(repo, args)

    patterns = [re.compile(p) for p in excludes]
    changes: List[Change] = []
    for record in raw.split(_REC):
        if not record.strip():
            continue
        header, _, numstat = record.partition(_END)
        parts = header.split(_FLD)
        if len(parts) < 6:
            continue
        sha, ts, parents, email, subject = parts[:5]
        body = _FLD.join(parts[5:])
        files: List[FileChange] = []
        for line in numstat.strip().splitlines():
            cols = line.split("\t")
            if len(cols) != 3:
                continue
            added, deleted, path = cols
            if _excluded(path, patterns):
                continue
            files.append(
                FileChange(path, int(added) if added.isdigit() else 0, int(deleted) if deleted.isdigit() else 0)
            )
        change = Change(sha, int(ts), parents.split(), email, subject, body.strip(), files)
        if not files:
            continue
        if change.is_bot and not include_bots:
            continue
        changes.append(change)
    changes.sort(key=lambda c: c.timestamp)
    return changes


def read_tags(repo: str) -> List[Tuple[int, str]]:
    """Return ``(timestamp, tag)`` pairs for every tag, oldest first."""
    raw = _git(repo, ["for-each-ref", "--format=%(creatordate:unix)\t%(refname:short)", "refs/tags"])
    tags = []
    for line in raw.splitlines():
        ts, _, name = line.partition("\t")
        if ts.strip().isdigit():
            tags.append((int(ts), name.strip()))
    tags.sort()
    return tags


def show_file(repo: str, sha: str, path: str) -> Optional[str]:
    """Return a file's content at a commit, or None if it doesn't exist there."""
    try:
        return _git(repo, ["show", f"{sha}:{path}"])
    except subprocess.CalledProcessError:
        return None


def list_files(repo: str, sha: str) -> List[str]:
    return _git(repo, ["ls-tree", "-r", "--name-only", sha]).splitlines()
