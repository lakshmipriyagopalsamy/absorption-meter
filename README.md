# CATS and change absorption capacity

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.24521870.svg)](https://doi.org/10.5281/zenodo.24521870)

**AI raised how fast your team can produce change. Did it raise how fast your system can absorb it?**

Created and maintained by **Lakshmi Priya Gopalsamy** ([ORCID 0009-0002-3628-2540](https://orcid.org/0009-0002-3628-2540)).
The change absorption model, the CATS framework and the measurement methodology are the author's
research; `absorption-meter` is their reference implementation.

> **Status.** A research framework with a reference implementation. The measures are practical
> proxies, and the decision thresholds are starting points to tune to your team's own history.

This repository holds an open framework and a tool built around one idea. When production
outruns absorption, the gap builds up as **delivery debt**. DORA metrics measure the pipeline, so they
can stay green while the debt grows. Practitioners have started calling the constraint *absorption
capacity*. This work makes it measurable, shows where the debt hides, and says what to do about it.

Delivery debt is broader than technical debt: technical debt is shortcuts in the code or design;
delivery debt is change shipped faster than the team could verify, integrate, observe and decide on it.
It can settle in the code (weak tests, coupling) or outside it (missing telemetry, unowned decisions).

| | What | Where |
|---|---|---|
| 📘 | **Playbook:** the framework in practice: the matrix, paired metrics, decision rules, a two-week start, a self-check | [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) |
| 🛠️ | **Tool:** `absorption-meter`, a CLI and GitHub Action that computes the paired metrics and flags contract drift | [`src/absorption_meter/`](src/absorption_meter/) |

## The framework in 30 seconds

- **P** (production): changes merged, weighted by size. **A** (absorption): the part not reverted, hotfixed
  or reworked within 14 days. **AR = A / P**. The full model also requires a first-run CI pass; git history
  doesn't record CI, so the tool reports the repository proxy **AR_repo**.
- Delivery debt hides in five places: **contracts, verification, observability, coupling, decisions**.
- **CATS** raises absorption: **C**ontracts, **A**utomated verification, **T**elemetry,
  **S**implification. Human decision ownership is the governance layer beneath all four.
- **Paired metrics.** Read each DORA outcome metric next to an earlier signal from the controls:

  | DORA metric | Paired indicator |
  |---|---|
  | Deployment frequency | Verification effectiveness: mutation score or critical requirements verified (code changes without test changes as proxy; rework rate corroborates) |
  | Lead time | Decision latency; change cost |
  | Change failure rate | Contract drift |
  | Recovery time | Telemetry coverage; time to detect |

  A DORA metric that improves or holds while its indicator worsens is the signature of hidden debt.
- **Decision rules R0–R6** say when to scale AI use, when to hold, and which control to invest in first,
  judged against your team's own baseline.

## Quick start

```bash
pip install git+https://github.com/lakshmipriyagopalsamy/absorption-meter
absorption-meter analyze path/to/repo --since 2025-01-01
```

The report opens with a decision (Scale, Hold or Address), then the four pairs, a month-by-month table
and any contract drift.

Try it without a repository, on the bundled demo team:

```bash
absorption-meter analyze --input examples/demo/changes.jsonl --team-metrics examples/demo/team.csv
```

Options:

| Option | Adds |
|---|---|
| `--github OWNER/REPO` | Lead time, decision latency and review depth from pull requests (uses `GITHUB_TOKEN`) |
| `--team-metrics team.csv` | Telemetry coverage, time to detect, recovery, deployments, from your own systems ([template](docs/team-metrics-template.csv)) |
| `--format json` | Machine-readable output |
| `--fail-on-signal` | Exit status 2 on a debt signal or a Hold, for CI gates |
| `--recent 3 --baseline 6 --k 1` | Window sizes and sensitivity of the baseline comparison |
| `--robust` | Median and MAD baseline instead of mean and standard deviation (resists outlier months) |
| `--prs prs.json` | Pull-request data saved as JSON (the records `--github` reads), analyzed offline |
| `--late-window 90` | Days for late rework: fixes after the 14-day window but within this many days |
| `--input data.jsonl` | Analyze an exported dataset instead of a repository |
| `--as-of YYYY-MM-DD` | Analysis date: changes whose 14-day window hasn't closed by then are left out of P and A (default: today, or `--until`; a dataset uses the date it was read) |

`absorption-meter contracts path/to/repo` lists OpenAPI or JSON Schema changes that broke
compatibility without a version bump. This is a partial compatibility check, not full contract
validation (see [Scope and limitations](#scope-and-limitations)). `absorption-meter export path/to/repo -o data.jsonl` writes a
shareable dataset that holds no names, e-mail addresses or commit messages.

## Reproducibility

[`examples/`](examples/) holds a synthetic demo team, where every signal fires, and a worked example on
the public history of Homebrew/brew, with the decision rules replayed month by month.

| | |
|---|---|
| Homebrew source | [Homebrew/brew](https://github.com/Homebrew/brew) mainline, pinned to commit `3e47189a707c739ee1278a28a3b845f5834574e6` (BSD-2-Clause) |
| Dataset | `examples/homebrew/changes.jsonl`, made with `absorption-meter export path/to/brew --since 2024-07-01 --until 2026-11-01` (4,176 changes; no names, e-mails or messages) |
| Window and dates | Calendar months; rework window *W* = 14 days; only changes whose window has closed by the analysis date enter P and A; baseline: last 3 months against the previous 6 |
| Replay | `scripts/rule_timeline.py` re-runs the rules as of the end of each month using only history up to then (`timeline.csv`, `rule_timeline.md`; `robust/` uses the median/MAD baseline) |
| Demo | `examples/demo/make_demo.py`, deterministic (seed 20260101) |
| Regenerate everything | `scripts/reproduce.sh`, with no network access and no clones |
| Check | `git status --short` should show no changes afterwards; CI runs the script and fails on any difference |
| Outputs | `examples/*/report.md` and `report.json`, `examples/homebrew/{monthly,timeline}.csv`, `rule_timeline.md`, `robust/`, `figures/*.dat` |
| Environment | Python 3.9 or later (CI: 3.9, 3.12, 3.13), PyYAML; `pip install -e .` |
| Tests | `pytest`: includes merge counting, window boundaries, the matured-cohort replay, and checks that every worked-example number follows from the committed outputs |
| Performance | Linear in history length: about 2 s for 100,000 changes ([benchmark](docs/BENCHMARK.md)) |

### GitHub Action

```yaml
on:
  schedule: [{ cron: "0 6 1 * *" }]   # monthly
  workflow_dispatch:
jobs:
  absorption:
    runs-on: ubuntu-latest
    permissions: { contents: read, pull-requests: read }
    steps:
      - uses: actions/checkout@v4
        with: { fetch-depth: 0 }
      - uses: lakshmipriyagopalsamy/absorption-meter@v0.2.1
        with: { github-prs: "true" }
```

The report appears in the job summary. For production workflows, pin the action to the release's
full commit SHA instead of the tag (`uses: lakshmipriyagopalsamy/absorption-meter@<sha>  # v0.2.1`).

## Scope and limitations

The tool measures what version control and optional team data can show. It does not run mutation
tests, instrument services or judge whether a human decision was a good one.

| CATS part | What `absorption-meter` does | Coverage |
|---|---|---|
| Contracts | Detects selected breaking changes in OpenAPI 3, Swagger 2 and JSON Schema files: removed paths, operations, 2xx responses or properties; newly required inputs; type changes; removed request enum values. External `$ref` targets, constraint changes (`pattern`, `minLength` …), `oneOf`/`anyOf`/`allOf`, AsyncAPI, protobuf and GraphQL are not analyzed | Partial |
| Automated verification | Share of code changes merged without test changes (a proxy); accepts team-reported mutation score or critical-requirements coverage | Partial |
| Telemetry | Accepts team-reported telemetry coverage, time to detect and recovery time | Partial (team data) |
| Simplification | Change cost: lines and top-level modules touched per change | Proxy |
| Ownership and decisions | Pull-request decision latency, review depth, unreviewed share and examined absorption (with `--github`); decision rules R0–R6 | Partial |

### What the measures can and can't tell you

Every measure is a proxy. Rework is detected from reverts and fix-like follow-up changes to the same
files: it misses silent fixes and can count unrelated fixes to busy files. Compare a repository with its
own history, never with another team's numbers. Operational definitions of every measure are in the [playbook](docs/PLAYBOOK.md#9-operational-definitions).

**Absorbed or unexamined?** Low rework can mean a change was solid, or that nobody looked closely and its
defects surfaced later, in production or on field devices, outside the git window. Since v0.2.0 the
report separates the two:
- **Late rework:** fixes 15–90 days after merging (`--late-window`), over changes whose window has closed;
- **Examined absorption** and **unreviewed share** (with `--github` or `--prs`): how much absorbed change was
  actually reviewed by someone other than its author. A rising unreviewed share also fires R6;
- **Escaped defects** and **days to first defect** (team data): failures git never sees. Rising escaped
  defects fire R3.

When these point the other way from AR_repo, the report lists **cautions** under the decision. Cautions
qualify the verdict; they never change it on their own.

See it in one command, with no GitHub token: the `examples/unexamined/` team keeps AR_repo near 0.89, so AR
alone says *Scale cautiously*, while its review and defect data turn the verdict to *Address* with five
cautions:

```bash
absorption-meter analyze --input examples/unexamined/changes.jsonl \
  --prs examples/unexamined/prs.json --team-metrics examples/unexamined/team.csv
```

## Development

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
scripts/reproduce.sh                               # regenerate all example outputs and figure data
```

## Citing

Cite the software as: Gopalsamy, L. P. *absorption-meter* (software). Zenodo.
[doi:10.5281/zenodo.24521870](https://doi.org/10.5281/zenodo.24521870) (all versions; v0.1.1 is
[10.5281/zenodo.24521871](https://doi.org/10.5281/zenodo.24521871)). See also [`CITATION.cff`](CITATION.cff).
The worked example in the accompanying article was produced with v0.1.1; later versions reproduce the
same numbers, and `tests/test_paper_numbers.py` checks this on every change. The ideas were first presented in *The AI Velocity Paradox*
(October 2026) and at Raptors Conference 2026. An accompanying article is in preparation.

## License

Code: [MIT](LICENSE). Documentation (`docs/`): [CC BY 4.0](LICENSE-docs.md).
