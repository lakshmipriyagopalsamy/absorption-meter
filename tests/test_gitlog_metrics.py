from conftest import day

from absorption_meter.gitlog import read_changes, read_tags
from absorption_meter.metrics import monthly, release_failures, rework_flags


def test_excludes_lockfiles_and_bots(repo):
    repo.commit({"src/app.py": "a\n"}, "add app", day(2025, 1, 2))
    repo.commit({"package-lock.json": "{}\n"}, "bump lockfile", day(2025, 1, 3))
    repo.commit({"src/app.py": "a\nb\n"}, "Bump x from 1 to 2", day(2025, 1, 4), author="49699333+dependabot[bot]@users.noreply.github.com")
    repo.commit({"src/app.py": "a\nb\nc\n", "docs/x.md": "x\n"}, "feature", day(2025, 1, 5))
    changes = read_changes(repo.path)
    assert [c.subject for c in changes] == ["add app", "feature"]
    assert changes[-1].top_dirs == {"src", "docs"}
    assert changes[-1].lines == 2


def test_merge_counts_full_branch_diff(repo):
    repo.commit({"a.txt": "1\n"}, "base", day(2025, 1, 1))
    repo._git("checkout", "-q", "-b", "feature")
    repo.commit({"src/a.py": "x\n"}, "f1", day(2025, 1, 2))
    repo.commit({"src/b.py": "y\n"}, "f2", day(2025, 1, 3))
    repo._git("checkout", "-q", "main")
    stamp = "2025-01-04T12:00:00+0000"
    repo._git("merge", "-q", "--no-ff", "feature", "-m", "Merge feature",
              env={"GIT_AUTHOR_DATE": stamp, "GIT_COMMITTER_DATE": stamp})
    changes = read_changes(repo.path)
    assert [c.subject for c in changes] == ["base", "Merge feature"]
    assert changes[-1].is_merge
    assert sorted(changes[-1].paths) == ["src/a.py", "src/b.py"]


def test_rework_by_fix_and_revert(repo):
    a = repo.commit({"src/a.py": "1\n"}, "feature a", day(2025, 2, 1))
    b = repo.commit({"src/b.py": "1\n"}, "feature b", day(2025, 2, 2))
    c = repo.commit({"src/c.py": "1\n"}, "feature c", day(2025, 2, 3))
    repo.commit({"src/a.py": "2\n"}, "fix: null check in a", day(2025, 2, 5))
    repo._git("revert", "--no-edit", b, env={"GIT_AUTHOR_DATE": "2025-02-06T12:00:00+0000",
                                             "GIT_COMMITTER_DATE": "2025-02-06T12:00:00+0000"})
    repo.commit({"src/c.py": "2\n"}, "fix c much later", day(2025, 3, 20))
    flags = rework_flags(read_changes(repo.path), window_days=14)
    assert flags[a] and flags[b]
    assert not flags[c]


def test_release_failures_and_monthly(repo):
    repo.commit({"src/a.py": "1\n"}, "one", day(2025, 1, 10))
    repo.tag("v1.0.0", day(2025, 1, 10))
    repo.commit({"src/a.py": "2\n"}, "fix: hot", day(2025, 1, 12))
    repo.tag("v1.0.1", day(2025, 1, 12))
    repo.commit({"src/b.py": "1\n"}, "two", day(2025, 3, 1))
    repo.tag("v1.1.0", day(2025, 3, 1))
    tags = read_tags(repo.path)
    assert [(f, h) for _, f, h in release_failures(tags)] == [(True, 48.0), (False, None), (False, None)]

    analysis = monthly(read_changes(repo.path), tags, rework_window_days=14, min_releases=1)
    assert [r.month for r in analysis.months] == ["2025-01", "2025-02", "2025-03"]
    jan = analysis.months[0]
    assert jan.changes == 2 and jan.releases == 2 and jan.patch_release_rate == 0.5
    assert jan.rework_rate == 0.5  # "one" was fixed within the window
    assert jan.recovery_hours == 48.0
    assert 0 < jan.absorption_ratio < 1
    assert analysis.months[1].changes == 0
    # March's only change is inside the censored tail.
    assert analysis.months[2].rework_rate is None
