# Field tests: ten public projects before and after AI adoption

The Homebrew worked example is one project. These field tests apply the same method to ten more public
repositories:
- **eight that adopted AI tooling,** each with a dated AI-instruction file (`CLAUDE.md`, `AGENTS.md`, Copilot
  or Cursor instructions);
- **two with no such file,** as a reference.

The same window is used for all: July 2024 to October 2026, monthly, *W* = 14 days. The month-by-month replay uses only the
history available at each point.

**Read this as descriptive evidence, not proof of cause.**
- Projects differ in size, domain and maturity.
- An instructions file marks project-level adoption, not how much code AI wrote.
- Visible AI signatures in commit messages undercount AI use.

## Projects

| Project | Language | Pinned commit | First AI-instruction file | AI-signed commits after the marker |
|---|---|---|---|---|
| [zed](https://github.com/zed-industries/zed) | Rust | `da3a2740330a` | CLAUDE.md, .cursorrules, 2025-04-17 | 2% |
| [excalidraw](https://github.com/excalidraw/excalidraw) | TypeScript | `f4e5226a3d84` | CLAUDE.md, Copilot instructions, 2025-05-25 | 4% |
| [prefect](https://github.com/prefecthq/prefect) | Python | `5f7d879aa163` | AGENTS.md, 2025-06-16 | 53% |
| [sentry-python](https://github.com/getsentry/sentry-python) | Python | `566beb013a98` | .cursor, 2025-06-24 | 5% |
| [langchain](https://github.com/langchain-ai/langchain) | Python | `30c4e38d71c2` | Copilot instructions, 2025-07-21 | 2% |
| [biome](https://github.com/biomejs/biome) | Rust | `f50b26295e4e` | CLAUDE.md, 2025-07-31 | 4% |
| [deno](https://github.com/denoland/deno) | Rust | `ddbb5004864c` | CLAUDE.md, 2025-11-06 | 15% |
| [ruff](https://github.com/astral-sh/ruff) | Rust | `ee3883e05955` | CLAUDE.md, 2026-01-04 | 3% |
| [fastapi](https://github.com/fastapi/fastapi) | Python | `05e6df7e906c` | none (reference) | – |
| [poetry](https://github.com/python-poetry/poetry) | Python | `3cc663a73852` | none (reference) | – |

Results are in [`summary.md`](summary.md) (also [`summary.csv`](summary.csv)). Each project folder has:
- `report.md` and `report.json`: the report as of October 2026;
- `rule_timeline.md` and `timeline.csv`: the replay;
- `monthly.csv`: monthly measures;
- `markers.json`: adoption dates and AI-signature shares;
- `changes.jsonl.gz`: the dataset, with no names, e-mails or messages.

## What the field tests show

1. **Change size grew after adoption in seven of eight AI-marker projects.**
   - Median lines per change, six months before the marker against afterwards: biome 58 → 115, zed 31 → 59, sentry-python 25 → 51,
     langchain 10 → 25, deno 63 → 96, excalidraw 39 → 58, ruff 74 → 83.
   - The exception is prefect, 78 → 68.
   - Of the two references, fastapi's changes got smaller (78 → 42) and poetry's grew modestly (24 → 31).
   - Change cost (R5) is the most frequent rule, or tied for most frequent, in seven of the eight
     AI-marker projects. This matches the Homebrew example and published evidence that complexity rises after AI-editor adoption.
2. **AR_repo fell after adoption in three projects** (sentry-python 0.86 → 0.64, langchain 0.78 → 0.64,
   excalidraw 0.66 → 0.55). It held or rose in the other five.
   - Production more than doubled at sentry-python (+191%) and deno (+108%).
   - Deno and sentry-python (4 months each), biome (2) and excalidraw (1) returned **hold** in the replay.
3. **The rules are not an AI detector.** The two reference projects also return hold and address
   verdicts: fastapi's rework rose from 1% to 10% with no AI marker. The framework measures absorption,
   whatever drives it.
4. **Prefect is the clearest AI-adoption case.** 53% of its commits after the marker carry an AI
   co-author signature, yet its AR_repo rose (0.78 → 0.84) and its replay returned **scale** most often.
   - Its production fell 53% over the same period. That may reflect changes in the repository's structure
     as much as AI use.
   - Heavy AI use with a healthy AR_repo is exactly the case v0.2's review and late-defect measures exist
     to examine further.

## Limitation found, and the fix in v0.3

The first run, with the v0.2 rework rule, showed that file-linked rework over-counts in busy repositories,
for two reasons:
- **Hub files:** files most changes touch link unrelated changes to later fixes. Examples are deno's
  `tests/node_compat/config.jsonc` (493 links) and `Cargo.toml` (263), biome's `CHANGELOG.md` (121), and
  zed's `crates/editor/src/editor.rs` (376).
- **Conventional-commit titles:** titles such as `fix(deps): bump x` count as fixes.

v0.3 tightens the rule. It ignores maintenance titles and links fixes only through non-hub files. The rule
was specified in [docs/METHOD-v0.3.md](../../docs/METHOD-v0.3.md) and committed before it was applied to
any data. All numbers above use it.

[`../rule_comparison.md`](../rule_comparison.md) compares the two rules on every dataset:
- **Busy projects:** AR_repo rises markedly (biome 0.44 → 0.64, langchain 0.56 → 0.69, excalidraw
  0.44 → 0.57, deno 0.30 → 0.40).
- **Homebrew worked example:** it barely moves (0.75 → 0.77), and its replay verdicts are unchanged.
- **Zed and ruff:** levels stay low (0.37, 0.53). Their remaining links run through large core files touched
  by fewer than 10% of changes, which only line-level linkage, tracing the exact lines a fix changes, would
  resolve.

**Compare AR_repo trends within a project, not levels across projects.** The v0.2 rule remains available as
`--rework-rule legacy`.

## Reproduce

Everything except the datasets and markers is regenerated offline by `scripts/reproduce.sh`; CI fails if
anything changes. The datasets were collected once from clones at the pinned commits with
`scripts/collect_field_test.py NAME OWNER/REPO PATH`. Projects are credited under their own licences;
only aggregate change metadata is stored.
