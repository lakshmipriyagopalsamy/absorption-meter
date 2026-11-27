"""Every Homebrew number and verdict quoted in the article's worked example must follow from the committed
outputs, which scripts/reproduce.sh regenerates from the pinned dataset. The numbers are checked always;
the manuscript's wording is checked only where a local copy of the manuscript (paper/main.tex) exists,
since the manuscript is not part of the public repository."""

import csv
import json
import os
import re
from statistics import mean

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HB = os.path.join(ROOT, "examples", "homebrew")


def table(*parts):
    with open(os.path.join(HB, *parts), newline="") as fh:
        return list(csv.DictReader(fh))


MONTHLY = {r["month"]: r for r in table("monthly.csv")}
REPLAY = {r["as_of"]: r for r in table("timeline.csv")}
ROBUST = {r["as_of"]: r for r in table("robust", "timeline.csv")}
MANUSCRIPT = os.path.join(ROOT, "paper", "main.tex")
PAPER = None
if os.path.exists(MANUSCRIPT):
    with open(MANUSCRIPT, encoding="utf-8") as fh:
        PAPER = re.sub(r"\s+", " ", fh.read())

BASELINE = [f"2025-0{i}" for i in range(1, 7)]
MAY_JUL = ["2026-05", "2026-06", "2026-07"]


def col(months, name):
    return [float(MONTHLY[m][name]) for m in months]


def says(text):
    if PAPER is not None:
        assert text in PAPER, f"manuscript no longer says: {text!r}"


def test_scope():
    with open(os.path.join(HB, "report.json")) as fh:
        total = json.load(fh)["analysis"]["total_changes"]
    assert total == 4176 and min(MONTHLY) == "2024-07" and max(MONTHLY) == "2026-10"
    says("July 2024 to October 2026: 4,176 changes")


def test_adoption_markers():
    first = {r["file"]: r["first_added"] for r in table("ai_files.csv")}
    assert first[".github/copilot-instructions.md"] == "2025-07-24"
    assert sorted(v[:7] for f, v in first.items() if f != ".github/copilot-instructions.md") == \
        ["2025-09", "2025-10", "2026-02"]
    says("added on 24 July 2025, and other AI-tool instructions followed in September and October 2025 and February 2026")
    signals = [r for r in table("ai_signals.csv") if r["month"] >= "2025-08"]
    share = sum(int(r["ai_marked_commits"]) for r in signals) / sum(int(r["commits"]) for r in signals)
    assert round(100 * share, 1) == 2.7
    says("2.7\\% of commits from August 2025 onward")


def test_baseline_and_first_hold():
    base_p = mean(col(BASELINE, "production"))
    assert round(base_p) == 285 and round(mean(col(BASELINE, "absorption_ratio")), 2) == 0.80
    says("$P$ averaged 285 a month and $\\AR_{\\text{repo}}$ 0.80")
    aug_p, aug_ar = col(["2025-08"], "production")[0], col(["2025-08"], "absorption_ratio")[0]
    assert 1.9 <= aug_p / base_p < 2.0 and round(aug_ar, 2) == 0.63              # "nearly doubled"
    assert REPLAY["2025-08"]["verdict"] == "hold" and REPLAY["2025-08"]["rules"] == "R1 R3 R5"
    assert REPLAY["2025-10"]["verdict"] == "hold"
    holds_2025 = [m for m, r in REPLAY.items() if m.startswith("2025") and r["verdict"] == "hold"]
    assert holds_2025 == ["2025-08", "2025-10"]
    says("fell to 0.63, and the rules returned \\emph{hold} (R1), with rework (R3) and change cost (R5) rising; "
         "they returned hold again in October")


def test_recovery_and_scale():
    months = ["2025-11", "2025-12", "2026-01"]
    assert round(mean(col(months, "absorption_ratio")), 2) == 0.88
    assert all(REPLAY[m]["verdict"] == "scale" for m in months)
    says("recovered to 0.88 between November 2025 and January 2026, and the rules returned \\emph{scale}")


def test_change_cost_then_second_hold():
    r5 = [m for m, r in REPLAY.items() if m >= "2026-01" and "R5" in r["rules"].split()]
    assert r5[0] == "2026-02" and r5 == sorted(m for m in REPLAY if m >= "2026-02")   # fires from February on
    assert MONTHLY["2025-11"]["median_lines"] == "13.0" and round(mean(col(MAY_JUL, "median_lines"))) == 50
    says("R5 fired from February, as median change size grew from 13 lines in November 2025 to about 50 in May to July 2026")
    ratio = mean(col(MAY_JUL, "production")) / mean(col(BASELINE, "production"))
    assert round(ratio) == 4
    assert round(mean(col(MAY_JUL, "absorption_ratio")), 2) == 0.58
    assert round(mean(col(MAY_JUL, "rework_rate")), 2) == 0.36
    assert [m for m, r in REPLAY.items() if m >= "2026-01" and r["verdict"] == "hold"] == MAY_JUL
    says("about four times its 2025 baseline while $\\AR_{\\text{repo}}$ averaged 0.58 and rework 0.36")


def test_robust_baseline_holds_only_may_to_august_2026():
    assert [m for m, r in ROBUST.items() if r["verdict"] == "hold"] == MAY_JUL + ["2026-08"]
    says("return hold only in May to August 2026")


def test_figure_data_matches_outputs():
    with open(os.path.join(ROOT, "figures", "homebrew.dat")) as fh:
        rows = [line.split() for line in fh.read().splitlines()[1:]]
    for _, month, p, ar, hold in rows:
        assert abs(float(p) - float(MONTHLY[month]["production"])) < 0.051
        assert abs(float(ar) - float(MONTHLY[month]["absorption_ratio"])) < 1e-4
        assert (hold == "1") == (REPLAY.get(month, {}).get("verdict") == "hold")


def test_field_test_sentence_matches_the_summary():
    """Section VII's one-sentence summary of the ten field tests must match examples/field-tests/summary.csv."""
    with open(os.path.join(ROOT, "examples", "field-tests", "summary.csv"), newline="") as fh:
        rows = list(csv.DictReader(fh))
    ai = [r for r in rows if r["marker"]]
    assert len(ai) == 8 and len(rows) - len(ai) == 2
    grew = sum(float(r["median_lines_after"]) > float(r["median_lines_before"]) for r in ai)
    fell = sum(float(r["AR_after"]) < float(r["AR_before"]) - 0.02 for r in ai)
    fired_without_ai = all(int(r["hold_months_after"]) + int(r["address_months_after"]) > 0
                           for r in rows if not r["marker"])
    assert (grew, fell, fired_without_ai) == (7, 3, True)
    says("eight further public projects that adopted AI tooling, and two that did not")
    says("change size grew after adoption in seven of the eight, but $\\AR_{\\text{repo}}$ fell in only three, "
         "and the rules also fired on projects without AI")
    # "Rising change cost was the most consistent signal": R5 is the most frequent rule (or tied) in 7 of 8.
    def top_rules(r):
        counts = {k: int(v) for k, v in (x.split("×") for x in r["top_rules_after"].split())}
        best = max(counts.values())
        return {k for k, v in counts.items() if v == best}
    assert sum("R5" in top_rules(r) for r in ai) == 7
    says("rising change cost was the most consistent signal")
