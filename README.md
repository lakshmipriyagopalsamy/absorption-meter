# CATS and change absorption capacity

**AI raised how fast your team can produce change. Did it raise how fast your system can absorb it?**

This repository holds an open framework, a tool and a research paper about one idea. When production
outruns absorption, the gap builds up as **delivery debt**. DORA metrics measure the pipeline, so they
can stay green while the debt grows. Practitioners have started calling the constraint *absorption
capacity*. This work makes it measurable, shows where the debt hides, and says what to do about it.

| | What | Where |
|---|---|---|
| 📄 | **Paper:** *When AI Outpaces Absorption: Measuring Delivery Debt and Repaying It with CATS* | [`paper/`](paper/) ([PDF](paper/main.pdf)) |
| 📘 | **Playbook:** the framework in practice: the matrix, paired metrics, decision rules, a two-week start, a self-check | [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) |
| 🛠️ | **Tool:** `absorption-meter`, a CLI and GitHub Action that computes the paired metrics and flags contract drift | [`src/absorption_meter/`](src/absorption_meter/) |

## The framework in 30 seconds

- **P** (production): changes merged, weighted by size. **A** (absorption): the part not reverted, hotfixed
  or reworked within 14 days. **AR = A / P**.
- Delivery debt hides in five places: **contracts, verification, observability, coupling, decisions**.
- **CATS** raises absorption: **C**ontracts, **A**utomated verification, **T**elemetry,
  **S**implification. Human decision ownership is the governance layer beneath all four.
- **Paired metrics.** Read each DORA outcome metric next to an earlier signal from the controls:

  | DORA metric | Paired indicator |
  |---|---|
  | Deployment frequency | Verification effectiveness (rework rate corroborates) |
  | Lead time | Decision latency; change cost |
  | Change failure rate | Contract drift |
  | Recovery time | Telemetry coverage; time to detect |

  A DORA metric that improves or holds while its indicator worsens is the signature of hidden debt.
- **Decision rules R0–R6** say when to scale AI use, when to hold, and which control to invest in first,
  judged against your team's own baseline.

## Quick start

```bash
pip install git+https://github.com/<owner>/<repo>
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
| `--input data.jsonl` | Analyze an exported dataset instead of a repository |

`absorption-meter contracts path/to/repo` lists every OpenAPI or JSON Schema change that broke
compatibility without a version bump. `absorption-meter export path/to/repo -o data.jsonl` writes a
shareable dataset that holds no names, e-mail addresses or commit messages.

## Demo data and a reproducible worked example

[`examples/`](examples/) holds a synthetic demo team, where every signal fires, and a worked example on
the public history of Homebrew/brew (July 2024 to October 2026), with the decision rules replayed month
by month. `scripts/reproduce.sh` regenerates every committed report, table and paper figure from the
committed datasets, with no network access; CI runs it and fails if anything changes.

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
      - uses: <owner>/<repo>@v0.1.0
        with: { github-prs: "true" }
```

The report appears in the job summary.

## What the measures can and can't tell you

Every measure is a proxy. Rework is detected from reverts and fix-like follow-up changes to the same
files: it misses silent fixes and can count unrelated fixes to busy files. Compare a repository with its
own history, never with another team's numbers. Details are in the paper, Sections III and VIII.

## Development

```bash
python -m venv .venv && .venv/bin/pip install -e ".[dev]"
.venv/bin/pytest
scripts/reproduce.sh                               # regenerate all example outputs and figure data
cd paper && tectonic main.tex                      # or pdflatex + bibtex
```

## Citing

See [`CITATION.cff`](CITATION.cff). The ideas were first presented in *The AI Velocity Paradox*
(October 2026) and at Raptors Conference 2026.

## License

Code: [MIT](LICENSE). Paper and documentation (`paper/`, `docs/`): [CC BY 4.0](LICENSE-docs.md).
