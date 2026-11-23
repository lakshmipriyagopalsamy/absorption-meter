"""Golden tests: the committed example reports must be exactly reproducible from the committed datasets,
and the dataset format must give the same analysis as reading the repository directly."""

import json
import os

import pytest
from conftest import day

from absorption_meter.cli import main
from absorption_meter.dataset import load
from absorption_meter.metrics import MonthStats
from absorption_meter.pairs import Settings, trend

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "examples")

CASES = [
    ("demo", ["--team-metrics", os.path.join(EX, "demo", "team.csv")]),
    ("homebrew", []),
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
