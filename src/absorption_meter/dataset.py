"""A portable, privacy-preserving dataset format for change histories.

``absorption-meter export`` writes a repository's mainline history as JSON lines;
``absorption-meter analyze --input`` reads it back. Anyone can then reproduce a
report without access to the repository, and a team can share its history
without sharing its code.

The format keeps only what the measures need. It stores no author names,
e-mail addresses or commit messages: a change's message is reduced to two
facts, whether it looks like a fix and which commit (if any) it reverts.

Lines, in order:

* one ``meta`` record: format version, source description, pinned commit, tags;
* one ``change`` record per mainline change, oldest first;
* one ``drift`` record per breaking contract change found at export time.
"""

from __future__ import annotations

import json
from typing import IO, Iterable, List, Optional, Sequence, Tuple

from . import __version__
from .contracts import Breaking, DriftEvent
from .gitlog import Change, FileChange
from .metrics import is_fix

FORMAT = "absorption-meter/changes@1"


def _change_record(c: Change) -> dict:
    return {
        "type": "change",
        "sha": c.sha,
        "t": c.timestamp,
        "parents": c.parents,
        "fix": is_fix(c, "strict"),
        "fix_legacy": is_fix(c, "legacy"),
        "reverts": c.reverted_sha,
        "files": [[f.path, f.added, f.deleted] for f in c.files],
    }


def write_dataset(
    out: IO[str],
    changes: Sequence[Change],
    tags: Sequence[Tuple[int, str]] = (),
    drift_events: Sequence[DriftEvent] = (),
    source: str = "",
    commit: str = "",
    as_of: Optional[int] = None,
) -> None:
    meta = {"type": "meta", "format": FORMAT, "tool": f"absorption-meter {__version__}",
            "source": source, "commit": commit, "tags": [[ts, name] for ts, name in tags]}
    if as_of is not None:
        meta["as_of"] = as_of   # the date the history was read: the default analysis date for this dataset
    out.write(json.dumps(meta, separators=(",", ":")) + "\n")
    for c in changes:
        out.write(json.dumps(_change_record(c), separators=(",", ":")) + "\n")
    for e in drift_events:
        out.write(json.dumps({
            "type": "drift", "sha": e.sha, "t": e.timestamp, "path": e.path,
            "old_version": e.old_version, "new_version": e.new_version,
            "breaking": [[b.kind, b.location] for b in e.breaking],
        }, separators=(",", ":")) + "\n")


def read_dataset(lines: Iterable[str]) -> Tuple[dict, List[Change], List[Tuple[int, str]], List[DriftEvent]]:
    meta: dict = {}
    changes: List[Change] = []
    drift: List[DriftEvent] = []
    for raw in lines:
        raw = raw.strip()
        if not raw:
            continue
        rec = json.loads(raw)
        kind = rec.get("type")
        if kind == "meta":
            if rec.get("format") != FORMAT:
                raise ValueError(f"unsupported dataset format: {rec.get('format')!r}")
            meta = rec
        elif kind == "change":
            # The message is not stored: rebuild one that the fix and revert rules read the same way.
            subject = "fix" if rec.get("fix") else "change"
            body = f"This reverts commit {rec['reverts']}." if rec.get("reverts") else ""
            files = [FileChange(p, int(a), int(d)) for p, a, d in rec.get("files", [])]
            legacy = rec.get("fix_legacy")
            changes.append(Change(rec["sha"], int(rec["t"]), list(rec.get("parents", [])), "", subject, body, files,
                                  fix_strict=bool(rec["fix"]) if legacy is not None else None,
                                  fix_legacy=bool(legacy) if legacy is not None else bool(rec.get("fix"))))
        elif kind == "drift":
            drift.append(DriftEvent(rec["sha"], int(rec["t"]), rec["path"], rec.get("old_version"),
                                    rec.get("new_version"), [Breaking(k, loc) for k, loc in rec.get("breaking", [])]))
    if not meta:
        raise ValueError("missing meta record: not an absorption-meter dataset")
    changes.sort(key=lambda c: c.timestamp)
    tags = [(int(ts), name) for ts, name in meta.get("tags", [])]
    return meta, changes, tags, drift


def _open(path: str, mode: str):
    """Open a dataset file; paths ending in .gz are gzip-compressed (written reproducibly, with no timestamp)."""
    if path.endswith(".gz"):
        import gzip
        import io

        if "w" in mode:
            return io.TextIOWrapper(gzip.GzipFile(path, "wb", mtime=0), encoding="utf-8")
        return gzip.open(path, "rt", encoding="utf-8")
    return open(path, mode.replace("t", ""), encoding="utf-8")


def load(path: str):
    with _open(path, "rt") as fh:
        return read_dataset(fh)


def save(path: str, changes, tags=(), drift_events=(), source: str = "", commit: str = "",
         as_of: Optional[int] = None) -> None:
    with _open(path, "wt") as fh:
        write_dataset(fh, changes, tags, drift_events, source, commit, as_of)
