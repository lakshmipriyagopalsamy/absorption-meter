"""Golden tests: the committed example reports must be exactly reproducible from the committed datasets,
and the dataset format must give the same analysis as reading the repository directly."""

import json
import math
import os

import pytest
from conftest import day

from absorption_meter.cli import main
from absorption_meter.dataset import load
from absorption_meter.metrics import MonthStats
from absorption_meter.pairs import Settings, trend

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")

U = os.path.join(EX, "unexamined")
CASES = [
    ("demo", ["--team-metrics", os.path.join(EX, "demo", "team.csv")]),
    ("homebrew", []),
    ("unexamined", ["--prs", os.path.join(U, "prs.json"), "--team-metrics", os.path.join(U, "team.csv")]),
]


@pytest.mark.parametrize("name,extra", CASES)
@pytest.mark.parametrize("fmt,filename", [("markdown", "report.md"), ("json", "report.json")])
def test_example_report_is_reproducible(tmp_path, name, extra, fmt, filename):
    out = tmp_path / filename
    main(["analyze", "--input", os.path.join(EX, name, "changes.jsonl"), *extra, "--format", fmt, "-o", str(out)])
    with open(os.path.join(EX, name, filename), encoding="utf-8") as fh:
        expected = fh.read()
    assert out.read_text(encoding="utf-8") == expected


def test_demo_shows_every_signal():
    with open(os.path.join(EX, "demo", "report.json")) as fh:
        report = json.load(fh)
    assert report["decision"]["verdict"] == "hold"
    assert {p["status"] for p in report["pairs"]} == {"debt-signal"}


def test_dataset_round_trip_matches_repository(repo, tmp_path):
    n = 0
    for month in range(1, 11):
        for k in range(3 if month < 8 else 8):
            n += 1
            repo.commit({f"src/m{n}.py": "x\n" * (5 if month < 8 else 40), f"web/v{n}.js": "y\n"},
                        f"feature {n}", day(2025, month, 2 + k * 3))
            if month >= 8 and k % 2 == 0:
                repo.commit({f"src/m{n}.py": "fixed\n"}, f"fix: {n}", day(2025, month, 3 + k * 3))
    repo.tag("v1.0.0", day(2025, 3, 1))
    data = tmp_path / "changes.jsonl"
    main(["export", repo.path, "-o", str(data)])
    direct, via = tmp_path / "direct.json", tmp_path / "via.json"
    main(["analyze", repo.path, "--format", "json", "-o", str(direct), "--keep-current-month"])
    main(["analyze", "--input", str(data), "--format", "json", "-o", str(via), "--keep-current-month"])
    a, b = json.loads(direct.read_text()), json.loads(via.read_text())
    a.pop("repository"), b.pop("repository")
    assert a == b

    meta, changes, tags, _ = load(str(data))
    text = data.read_text()
    assert "test@example.com" not in text and "feature 1" not in text   # no e-mails, no messages
    assert meta["commit"] and len(changes) == a["analysis"]["total_changes"]


def test_robust_baseline_ignores_one_outlier_month():
    values = [10, 10, 10, 10, 10, 60, 13, 13, 13]   # one spike in the baseline
    rows = [MonthStats(month=f"2025-{i + 1:02d}", changes=v) for i, v in enumerate(values)]
    assert trend(rows, "changes").direction == "flat"                       # the spike inflates the SD
    assert trend(rows, "changes", Settings(robust=True)).direction == "up"  # median/MAD is not fooled


def test_replay_uses_only_matured_changes():
    """An as-of analysis must not change when later history is added (no future leakage), and changes
    whose rework window hasn't closed by the cut-off must be left out of P and A."""
    from datetime import datetime, timezone

    from absorption_meter.gitlog import Change, FileChange
    from absorption_meter.metrics import monthly

    def ts(m, d):
        return int(datetime(2025, m, d, 12, tzinfo=timezone.utc).timestamp())

    def change(i, when, subject="change", path=None):
        return Change(f"{i:040x}", when, [], "", subject, "", [FileChange(path or f"f{i}.py", 10, 0)])

    history = [change(i, ts(m, d)) for i, (m, d) in enumerate([(1, 5), (1, 20), (2, 3), (2, 10), (3, 2), (3, 28)])]
    cut = ts(4, 1)
    # A fix to the 28 March change, made after the cut-off: it must not count as of March.
    future = history + [change(99, ts(4, 3), "fix: regression", path="f5.py")]

    as_of = monthly([c for c in history if c.timestamp < cut], as_of=cut)
    with_future = monthly([c for c in future if c.timestamp < cut], as_of=cut)
    assert as_of == with_future

    march = as_of.months[-1]
    # 28 March's window runs to 11 April, past the 1 April replay date: excluded. 2 March has matured.
    assert march.changes == 2 and march.absorption_ratio == 1.0
    assert march.production == round(math.log1p(10), 3)


def test_unexamined_demo_ar_alone_says_scale_but_review_and_defect_data_say_address(tmp_path):
    """The LinkedIn question in one dataset: low rework, but because nobody looked, not because it was solid."""
    ar_only, full = tmp_path / "ar.json", tmp_path / "full.json"
    data = os.path.join(U, "changes.jsonl")
    main(["analyze", "--input", data, "--late-window", "14", "--format", "json", "-o", str(ar_only)])
    main(["analyze", "--input", data, "--prs", os.path.join(U, "prs.json"), "--team-metrics",
          os.path.join(U, "team.csv"), "--format", "json", "-o", str(full)])
    a, f = json.loads(ar_only.read_text())["decision"], json.loads(full.read_text())["decision"]
    assert a["verdict"] == "scale" and a["cautions"] == []
    assert f["verdict"] == "address" and {"R3", "R6"} <= set(f["rules"])
    assert any("unexamined" in c for c in f["cautions"]) and any("Escaped defects" in c for c in f["cautions"])
    with open(os.path.join(U, "report_ar_only.md"), encoding="utf-8") as fh:
        assert "Scale cautiously" in fh.read()


def test_gzip_dataset_round_trip(tmp_path):
    from absorption_meter.dataset import load, save

    meta, changes, tags, drift = load(os.path.join(EX, "demo", "changes.jsonl"))
    gz = tmp_path / "d.jsonl.gz"
    save(str(gz), changes, tags, drift, meta["source"], meta["commit"])
    first = gz.read_bytes()
    save(str(gz), changes, tags, drift, meta["source"], meta["commit"])
    assert gz.read_bytes() == first                       # byte-identical: safe to commit and regenerate
    _, again, _, _ = load(str(gz))
    assert [c.sha for c in again] == [c.sha for c in changes]
