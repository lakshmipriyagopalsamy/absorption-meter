"""Edge cases behind the paper's central measurements: merge counting, window boundaries, reverts,
inactivity, missing data and empty input."""

from datetime import datetime, timezone

from conftest import day

from absorption_meter.gitlog import Change, FileChange, read_changes
from absorption_meter.metrics import monthly, rework_flags

DAY = 86400


def test_merged_branch_counts_once_with_first_parent_diff(repo):
    repo.commit({"app/base.py": "base\n"}, "initial", day(2025, 1, 1))
    repo.checkout("feature", create=True)
    repo.commit({"app/a.py": "a\n" * 10}, "feature part 1", day(2025, 1, 2))
    repo.commit({"app/b.py": "b\n" * 5}, "feature part 2", day(2025, 1, 3))
    repo.checkout("main")
    repo.commit({"docs/note.md": "n\n" * 3}, "mainline change before the merge", day(2025, 1, 4))
    merge = repo.merge("feature", "Merge feature", day(2025, 1, 5))

    changes = read_changes(repo.path)
    shas = [c.sha for c in changes]
    assert len(shas) == len(set(shas)) == 3          # initial, mainline change, merge: no per-parent duplicates
    assert all(c.subject != "feature part 1" for c in changes)   # branch commits are not mainline changes
    m = next(c for c in changes if c.sha == merge)
    # Diff against the first parent: exactly the feature's files, not the mainline change made meanwhile.
    assert sorted((f.path, f.added) for f in m.files) == [("app/a.py", 10), ("app/b.py", 5)]


def _c(i, when, subject="change", path=None, body="", added=10):
    return Change(f"{i:040x}", when, [], "", subject, body, [FileChange(path or f"f{i}.py", added, 0)])


T0 = int(datetime(2025, 3, 3, 12, tzinfo=timezone.utc).timestamp())


def test_fix_exactly_at_window_boundary_counts_and_one_second_later_does_not():
    base = _c(1, T0, path="x.py")
    on_edge = rework_flags([base, _c(2, T0 + 14 * DAY, "fix: edge", path="x.py")], 14)
    past = rework_flags([base, _c(2, T0 + 14 * DAY + 1, "fix: late", path="x.py")], 14)
    assert on_edge[base.sha] is True and past[base.sha] is False


def test_revert_and_multiple_fixes_flag_once():
    base = _c(1, T0, path="x.py")
    revert = _c(2, T0 + DAY, f'Revert "change"', path="x.py", body=f"This reverts commit {base.sha}.")
    fixes = [_c(3 + k, T0 + (2 + k) * DAY, "fix: again", path="x.py") for k in range(3)]
    flags = rework_flags([base, revert, *fixes], 14)
    assert flags[base.sha] is True
    a = monthly([base, revert, *fixes], as_of=T0 + 60 * DAY)
    assert a.months[0].rework_rate is not None and a.months[0].rework_rate <= 1.0


def test_fix_to_other_files_is_not_rework():
    base = _c(1, T0, path="x.py")
    assert rework_flags([base, _c(2, T0 + DAY, "fix: unrelated", path="y.py")], 14)[base.sha] is False


def test_zero_line_change_has_zero_weight_but_is_counted():
    a = monthly([_c(1, T0, added=0), _c(2, T0 + DAY)], as_of=T0 + 60 * DAY)
    month = a.months[0]
    assert month.changes == 2 and month.production > 0


def test_inactive_repository_matures_recent_changes_at_analysis_date():
    history = [_c(i, T0 + i * DAY) for i in range(5)]
    by_last_commit = monthly(history, as_of=history[-1].timestamp)
    much_later = monthly(history, as_of=history[-1].timestamp + 60 * DAY)
    # Anchored to the newest commit, none of these changes has matured; at a later analysis date all have.
    assert by_last_commit.months[0].absorption_ratio is None
    assert much_later.months[0].absorption_ratio == 1.0


def test_no_tags_and_no_team_metrics_leave_those_measures_empty():
    a = monthly([_c(i, T0 + i * DAY) for i in range(5)], as_of=T0 + 60 * DAY)
    m = a.months[0]
    assert m.releases in (0, None) and m.telemetry_coverage is None and m.mutation_score is None


def test_empty_input_gives_empty_analysis():
    a = monthly([])
    assert a.months == [] and a.total_changes == 0
