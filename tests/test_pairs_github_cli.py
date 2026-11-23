import json

from conftest import day

from absorption_meter.cli import main
from absorption_meter.github import fetch_merged_prs, merge_into, pr_monthly
from absorption_meter.metrics import Analysis, MonthStats, load_team_metrics
from absorption_meter.pairs import ADDRESS, DEBT, HOLD, INSUFFICIENT, OK, SCALE, evaluate, recommend, trend


def rows(changes, rework, dirs, lines=None):
    lines = lines or [10.0] * len(changes)
    out = []
    for i, (c, r, d, l) in enumerate(zip(changes, rework, dirs, lines)):
        out.append(MonthStats(month=f"2025-{i + 1:02d}", changes=c, rework_rate=r, mean_dirs=d, median_lines=l,
                              revert_rate=0.0, production=float(c), absorption_ratio=round(1 - r, 4),
                              untested_share=r))   # verification weakens alongside rework in these fixtures
    return out


def analysis(months, pr_data=False):
    return Analysis(months, sum(m.changes for m in months), months[0].month, months[-1].month, 14, False, [], pr_data)


def by_name(results):
    return {r.pair.split(" ↔")[0]: r for r in results}


QUIET, BURST = [10, 11, 10, 9, 10, 11], [20, 22, 24]


def test_trend_uses_trailing_baseline_and_sd():
    r = rows(QUIET + BURST, [0.1] * 9, [1.0] * 9)
    assert trend(r, "changes").direction == "up"
    assert trend(r, "rework_rate", abs_min=0.02).direction == "flat"
    assert trend(r[:8], "changes").direction == "n/a"
    # A noisy baseline raises the bar: the same recent mean no longer counts.
    noisy = rows([2, 18, 3, 19, 2, 18, 13, 13, 13], [0.1] * 9, [1.0] * 9)
    assert trend(noisy, "changes").direction == "flat"


def test_busier_not_faster_holds():
    r = rows(QUIET + BURST, [0.10] * 6 + [0.18, 0.20, 0.22], [1.2] * 6 + [1.8, 1.9, 2.0])
    a = analysis(r)
    result = by_name(evaluate(a))
    assert result["Deployment frequency"].status == DEBT
    assert result["Lead time"].status == DEBT and result["Lead time"].debt_type == "coupling"
    assert result["Change failure rate"].status == OK
    assert result["Recovery time"].status == INSUFFICIENT
    rec = recommend(a)
    assert rec.verdict == HOLD and rec.rules == ["R1", "R3", "R5"]
    assert rec.actions[0].startswith("R3")


def test_healthy_speed_up_scales():
    r = rows(QUIET + BURST, [0.10] * 9, [1.2] * 9)
    a = analysis(r)
    assert all(p.status != DEBT for p in evaluate(a))
    rec = recommend(a)
    assert rec.verdict == SCALE and rec.rules == ["R0"]


def test_contract_drift_comes_first_and_masks_r3():
    r = rows([10] * 9, [0.10] * 6 + [0.2] * 3, [1.0] * 9)
    for m in r[-3:]:
        m.contract_drift, m.contract_drift_per_100 = 1, 10.0
    for m in r[:6]:
        m.contract_drift_per_100 = 0.0
    a = analysis(r)
    assert by_name(evaluate(a))["Change failure rate"].status == DEBT
    rec = recommend(a)
    assert rec.verdict == ADDRESS
    assert rec.rules == ["R2"]  # rework is explained by drift, so R3 doesn't fire


def test_decision_debt_and_observability_from_team_data():
    r = rows([10] * 9, [0.1] * 9, [1.0] * 9)
    for m, lead, wait, cov in zip(r, [40] * 6 + [20] * 3, [4] * 6 + [9] * 3, [0.9] * 6 + [0.6] * 3):
        m.median_lead_hours, m.median_first_review_hours, m.telemetry_coverage = lead, wait, cov
    a = analysis(r, pr_data=True)
    result = by_name(evaluate(a))
    assert result["Lead time"].status == DEBT and result["Lead time"].debt_type == "decision"
    assert result["Recovery time"].status == DEBT
    assert recommend(a).rules == ["R4", "R6"]


def test_team_metrics_csv(tmp_path):
    a = analysis(rows([10] * 2, [0.1] * 2, [1.0] * 2))
    csv_path = tmp_path / "team.csv"
    csv_path.write_text("month,telemetry_coverage,time_to_detect_hours,deployments\n2025-02,0.75,3.5,12\n2030-01,1,1,1\n")
    load_team_metrics(a, str(csv_path))
    feb = a.months[1]
    assert (feb.telemetry_coverage, feb.time_to_detect_hours, feb.releases) == (0.75, 3.5, 12)
    assert a.team_data and a.releases_used


def test_github_fetch_and_monthly():
    pages = {
        "pulls?state=closed": [
            {"number": 2, "created_at": "2025-02-03T00:00:00Z", "merged_at": "2025-02-04T00:00:00Z", "user": {"login": "alice"}},
            {"number": 3, "created_at": "2025-02-02T00:00:00Z", "merged_at": None, "user": {"login": "bob"}},
            {"number": 4, "created_at": "2025-02-01T00:00:00Z", "merged_at": "2025-02-01T06:00:00Z", "user": {"login": "renovate[bot]"}},
            {"number": 1, "created_at": "2025-02-01T00:00:00Z", "merged_at": "2025-02-01T10:00:00Z", "user": {"login": "carol"}},
        ],
        "pulls/2/reviews": [{"user": {"login": "alice"}, "submitted_at": "2025-02-03T01:00:00Z"},
                            {"user": {"login": "dan"}, "submitted_at": "2025-02-03T06:00:00Z"}],
        "pulls/1/reviews": [],
        "pulls/2": {"additions": 150, "deletions": 50, "review_comments": 4},
        "pulls/1": {"additions": 10, "deletions": 0, "review_comments": 0},
    }

    def fetch(url):
        if "page=2" in url:
            return []
        for key in sorted(pages, key=len, reverse=True):
            if key in url:
                return pages[key]
        raise AssertionError(url)

    prs = fetch_merged_prs("o/r", fetch=fetch)
    assert [p["number"] for p in prs] == [2, 1]
    assert prs[0]["first_review_at"] == "2025-02-03T06:00:00Z" and prs[0]["review_rounds"] == 1
    month = pr_monthly(prs)["2025-02"]
    assert month["prs"] == 2
    assert month["median_lead_hours"] == 17.0
    assert month["median_first_review_hours"] == 6.0
    assert month["unreviewed_share"] == 0.5
    assert month["review_comments_per_100_lines"] == round(100 * 4 / 210, 3)

    a = analysis(rows([1], [0.0], [1.0]))
    a.months[0].month = "2025-02"
    merge_into(a, pr_monthly(prs))
    assert a.pr_data and a.months[0].prs == 2


def test_cli_end_to_end(repo, tmp_path, capsys):
    # Nine quiet months, then a burst of larger, cross-cutting changes with fixes.
    n = 0
    for month in range(1, 10):
        for k in range(4):
            n += 1
            repo.commit({f"src/m{n}.py": "x\n", f"tests/test_m{n}.py": "t\n"}, f"feature {n}",
                        day(2025, month, 2 + k * 5))
    for month in range(10, 13):
        for k in range(10):
            n += 1
            files = {f"src/m{n}.py": "x\n" * 30, f"api/h{n}.py": "y\n", f"web/v{n}.js": "z\n"}
            sha_day = 1 + k * 2
            repo.commit(files, f"feature {n}", day(2025, month, sha_day))
            if k % 2 == 0:
                repo.commit({f"src/m{n}.py": "fixed\n"}, f"fix: regression in {n}", day(2025, month, sha_day + 1))

    out = tmp_path / "report.json"
    code = main(["analyze", repo.path, "--format", "json", "--output", str(out), "--keep-current-month",
                 "--fail-on-signal"])
    data = json.loads(out.read_text())
    statuses = {p["pair"].split(" ↔")[0]: p["status"] for p in data["pairs"]}
    assert statuses["Deployment frequency"] == DEBT
    assert statuses["Lead time"] == DEBT
    assert data["decision"]["verdict"] == HOLD
    assert code == 2

    assert main(["analyze", repo.path, "--keep-current-month"]) == 0
    md = capsys.readouterr().out
    assert "## Decision" in md and "## Paired metrics" in md and "Hold" in md
