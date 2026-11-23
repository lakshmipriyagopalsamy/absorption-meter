# CATS and change absorption capacity

**AI raised how fast your team can produce change. Did it raise how fast your system can absorb it?**

This repository holds an open framework, a tool and a research paper about one idea. When production
outruns absorption, the gap builds up as **delivery debt**. DORA metrics measure the pipeline, so they
can stay green while the debt grows. Practitioners have started calling the constraint *absorption
capacity*. This work makes it measurable, shows where the debt hides, and says what to do about it.

| | What | Where |
|---|---|---|
| 📄 | **Paper:** *When AI Outpaces Absorption: A Capacity Model and the CATS Controls for Delivery Debt* | [`paper/`](paper/) ([PDF](paper/main.pdf)) |
| 📘 | **Playbook:** the framework in practice: the matrix, paired metrics, decision rules, a two-week start, a self-check | [`docs/PLAYBOOK.md`](docs/PLAYBOOK.md) |
| 🛠️ | **Tool:** `absorption-meter`, a CLI and GitHub Action that computes the paired metrics and flags contract drift | [`src/absorption_meter/`](src/absorption_meter/) |

## The framework in 30 seconds

- **P** (production): changes merged, weighted by size. **A** (absorption): the part not reverted, hotfixed
  or reworked within 14 days. **AR = A / P**.
- Delivery debt hides in five places: **contracts, verification, observability, coupling, decisions**.
- **CATS** raises absorption: **C**ontracts, **A**utomated verification, **T**elemetry,
  **S**implification. Human decision ownership is the governance layer beneath all four.
- **Paired metrics.** Read each lagging DORA metric next to a leading indicator:

  | DORA metric | Paired indicator |
  |---|---|
  | Deployment frequency | Rework rate |
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
and any contract drift. Options:

| Option | Adds |
|---|---|
| `--github OWNER/REPO` | Lead time, decision latency and review depth from pull requests (uses `GITHUB_TOKEN`) |
| `--team-metrics team.csv` | Telemetry coverage, time to detect, recovery, deployments, from your own systems ([template](docs/team-metrics-template.csv)) |
| `--format json` | Machine-readable output |
| `--fail-on-signal` | Exit status 2 on a debt signal or a Hold, for CI gates |
| `--recent 3 --baseline 6 --k 1` | Window sizes and sensitivity of the baseline comparison |

`absorption-meter contracts path/to/repo` lists every OpenAPI or JSON Schema change that broke
compatibility without a version bump.

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
python scripts/simulate_model.py paper/model.dat   # data for the paper's Figure 2
cd paper && tectonic main.tex                      # or pdflatex + bibtex
```

## Citing

See [`CITATION.cff`](CITATION.cff). The ideas were first presented in *The AI Velocity Paradox*
(October 2026) and at Raptors Conference 2026.

## License

Code: [MIT](LICENSE). Paper and documentation (`paper/`, `docs/`): [CC BY 4.0](LICENSE-docs.md).
