"""The indexed rework detector must agree exactly with the straightforward pairwise definition."""

import random

from absorption_meter.gitlog import Change, FileChange
from absorption_meter.metrics import FIX_PATTERN, rework_flags

DAY = 86400


def reference(changes, window_days=14, rule="legacy"):
    from absorption_meter.metrics import hub_paths, is_fix

    ordered = sorted(changes, key=lambda c: c.timestamp)
    hubs = hub_paths(ordered) if rule == "strict" else set()
    flags = {}
    for i, change in enumerate(ordered):
        reworked = False
        for later in ordered[i + 1:]:
            if later.timestamp - change.timestamp > window_days * DAY:
                break
            r = later.reverted_sha
            if r and (change.sha.startswith(r) or r.startswith(change.sha[:7])):
                reworked = True
                break
            if is_fix(later, rule) and (set(change.paths) - hubs) & (set(later.paths) - hubs):
                reworked = True
                break
        flags[change.sha] = reworked
    return flags


def test_indexed_detector_matches_reference_on_random_histories():
    rng = random.Random(7)
    for _ in range(30):
        changes, t = [], 1_700_000_000
        for i in range(300):
            t += rng.randint(0, 2 * DAY)
            sha = f"{rng.getrandbits(160):040x}"
            subject = rng.choice(["feature", "fix: bug", "refactor", "hotfix crash", "docs", "fix(deps): bump x",
                                  "chore: fix lint"])
            body = ""
            if changes and rng.random() < 0.05:
                body = f"This reverts commit {rng.choice(changes).sha}."
            files = [FileChange(rng.choice([f"m{rng.randint(1, 25)}.py", "Cargo.toml", "CHANGELOG.md"]), rng.randint(0, 50), 0)
                     for _ in range(rng.randint(1, 3))]
            changes.append(Change(sha, t, [], "", subject, body, files))
        for rule in ("legacy", "strict"):
            assert rework_flags(changes, rule=rule) == reference(changes, rule=rule)
