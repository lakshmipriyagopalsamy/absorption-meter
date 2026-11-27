"""v0.2.0: telling 'absorbed' apart from 'unexamined' — late rework, examined absorption, unreviewed share,
escaped defects. None of these may change a verdict on their own except through R3/R6."""

from datetime import datetime, timezone

from absorption_meter.github import earliest_merge, reviewed_map
from absorption_meter.gitlog import Change, FileChange
from absorption_meter.metrics import Analysis, MonthStats, load_team_metrics, monthly
from absorption_meter.pairs import DOWN, FLAT, SCALE, Trend, cautions, lagged_trend, recommend

DAY = 86400
T0 = int(datetime(2025, 1, 6, 12, tzinfo=timezone.utc).timestamp())


def ch(i, when, subject="change", path=None):
    return Change(f"{i:040x}", when, [], "", subject, "", [FileChange(path or f"f{i}.py", 10, 0)])


def test_late_rework_counts_fixes_after_the_window_only_once_matured():
    base, early_base = ch(1, T0, path="a.py"), ch(2, T0, path="b.py")
    late_fix = ch(3, T0 + 30 * DAY, "fix: late", path="a.py")      # day 30: beyond W=14, within 90
    early_fix = ch(4, T0 + 3 * DAY, "fix: early", path="b.py")     # day 3: ordinary rework
    history = [base, early_base, early_fix, late_fix]
    matured = monthly(history, as_of=T0 + 120 * DAY)
    jan = matured.months[0]
    # Of January's three changes, only `base` was reworked late (b.py was reworked early, the fix itself wasn't).
    assert jan.late_rework_rate == round(1 / 3, 4)
    assert jan.absorption_ratio < 1.0                                # the early fix still counts as rework
    assert monthly(history, as_of=T0 + 60 * DAY).months[0].late_rework_rate is None   # 90-day window still open


def test_examined_absorption_needs_a_review_and_covered_months():
    history = [ch(i, T0 + 31 * DAY + i * DAY) for i in range(4)]   # February
    reviewed = {history[0].sha: True, history[1].sha: True, history[2].sha: False}   # history[3]: no PR
    a = monthly(history, as_of=T0 + 120 * DAY, reviewed=reviewed)
    feb = a.months[0]
    assert feb.absorption_ratio == 1.0 and feb.examined_absorption_ratio == 0.5
    # PR data starting mid-February: February is only partly covered, so no examined value.
    partial = monthly(history, as_of=T0 + 120 * DAY, reviewed=reviewed, reviewed_from=T0 + 40 * DAY)
    assert partial.months[0].examined_absorption_ratio is None


def test_reviewed_map_and_earliest_merge():
    prs = [{"merge_commit_sha": "a" * 40, "review_rounds": 2, "merged_at": "2025-03-04T10:00:00Z"},
           {"merge_commit_sha": "b" * 40, "review_rounds": 0, "merged_at": "2025-02-01T10:00:00Z"},
           {"merge_commit_sha": None, "review_rounds": 1, "merged_at": "2025-01-01T10:00:00Z"}]
    assert reviewed_map(prs) == {"a" * 40: True, "b" * 40: False}
    assert earliest_merge(prs) == int(datetime(2025, 1, 1, 10, tzinfo=timezone.utc).timestamp())


def rows(n=9, **series):
    out = []
    for i in range(n):
        m = MonthStats(month=f"2025-{i + 1:02d}", changes=20, production=20.0, absorption_ratio=0.9,
                       rework_rate=0.1, mean_dirs=1.0, median_lines=10.0)
        for k, vals in series.items():
            setattr(m, k, vals[i])
        out.append(m)
    return out


def analysis(r, pr=False):
    return Analysis(r, sum(m.changes for m in r), r[0].month, r[-1].month, 14, False, [], pr)


def test_unexamined_absorption_cautions_without_changing_the_verdict():
    r = rows(examined_absorption_ratio=[0.85] * 6 + [0.55] * 3)
    rec = recommend(analysis(r, pr=True))
    assert rec.verdict == SCALE and rec.rules == ["R0"]               # verdict unchanged
    assert any("unexamined" in c for c in rec.cautions)


def test_rising_unreviewed_share_fires_r6():
    r = rows(unreviewed_share=[0.05] * 6 + [0.40] * 3)
    rec = recommend(analysis(r, pr=True))
    assert "R6" in rec.rules and any("without review" in c for c in rec.cautions)


def test_late_rework_trend_uses_latest_matured_months():
    r = rows(12, late_rework_rate=[0.02] * 6 + [0.10] * 3 + [None] * 3)
    assert lagged_trend(r, "late_rework_rate", abs_min=0.02).direction == "up"
    rec = recommend(analysis(r))
    assert rec.verdict == SCALE and any("Late rework" in c for c in rec.cautions)


def test_escaped_defects_from_team_data_fire_r3(tmp_path):
    r = rows()
    a = analysis(r)
    csv = tmp_path / "team.csv"
    csv.write_text("month,escaped_defects,days_to_first_defect\n" +
                   "".join(f"2025-{i + 1:02d},{1 if i < 6 else 6},{30 if i < 6 else 9}\n" for i in range(9)))
    load_team_metrics(a, str(csv))
    assert a.months[0].escaped_defects_per_100 == 5.0
    rec = recommend(a)
    assert "R3" in rec.rules
    assert any("Escaped defects" in c for c in rec.cautions) and any("sooner" in c for c in rec.cautions)


def test_large_gap_between_ar_and_examined_ar_is_flagged():
    t = {"examined_absorption_ratio": Trend(FLAT, 0.5, 0.5), "unreviewed_share": Trend("n/a", None, None),
         "late_rework_rate": Trend("n/a", None, None), "escaped_defects_per_100": Trend("n/a", None, None),
         "days_to_first_defect": Trend("n/a", None, None)}
    out = cautions(analysis(rows()), t, Trend(FLAT, 0.9, 0.9))
    assert out and "never reviewed" in out[0]
