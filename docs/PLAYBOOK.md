# The CATS playbook: measure absorption, not just speed

A practical guide for engineering teams using AI to write code. It explains the framework, how to measure
it with or without the `absorption-meter` tool, and what to do when a signal fires.

An accompanying research article is in preparation.

## 1. The idea in one paragraph

AI raises how fast a team can **produce** change. It doesn't raise how fast the system can **absorb**
change: verify it, integrate it, observe it, and decide on it without breaking. When production outruns
absorption, the gap builds up as **delivery debt**. DORA metrics measure the pipeline, so they can stay
green while the debt grows. CATS (Contracts, Automated verification, Telemetry, Simplification) is how
you raise absorption capacity. Paired metrics are how you see the gap before it shows up as incidents.

**Delivery debt is not the same as technical debt.** Technical debt (Cunningham's metaphor) is
shortcuts in code or design that speed delivery now and make later change costlier until they are
repaid; it lives in the codebase. Delivery debt is change shipped faster than the delivery system could
absorb it: verify, integrate, observe and decide on it. It can settle as technical debt (weak tests,
growing coupling) but also outside the code (missing telemetry, decisions nobody owns). D measures its
observable consequences, unabsorbed change, not the amount of technical debt in the code.

## 2. Three numbers

Measure over a rolling window, monthly by default:

| Symbol | Name | Definition |
|---|---|---|
| **P** | Production | Changes merged, weighted by size. `absorption-meter` uses log(1 + lines changed), so one huge change can't dominate |
| **A** | Absorption | The part of P that was absorbed safely: not reverted, hotfixed or reworked within *W* days (default 14) |
| **AR** | Absorption ratio | A / P, between 0 and 1. Without first-run CI data, the tool reports the repository proxy **AR_repo** (no verification term) |

Accumulated delivery debt is the running total of change taken in but not absorbed: **D = Σ (P − A)**.
It records cumulative unabsorbed change and never decreases. Track remediation separately: work that
addresses previously unabsorbed change, such as contract repair, test improvements and refactoring.
Remediation may improve later absorption, but it is not subtracted from D.

AR is a proxy: it estimates the share of delivered change absorbed **without observable short-term
corrective work**. It is not a direct measure of correctness, reliability or quality.

Watch AR's **trend** against your own history. A falling AR while P rises is the clearest single sign
that you are taking on change faster than you can absorb it.

**A steady AR is not the same as a safe one.** Low rework can mean a change was solid, or that nobody
looked closely and its defects surfaced weeks later, in production or on field devices, outside the
rework window. Check three things beside AR: how much absorbed change was actually **reviewed**, whether
fixes are arriving **late** (15–90 days after a change), and whether **escaped defects** are rising. The
tool reports all three and lists cautions when they disagree with AR.

## 3. Where delivery debt hides

| Debt | How it shows up with AI | CATS control | Leading indicator | Paired DORA metric |
|---|---|---|---|---|
| **Contract** | Schemas or field meanings change silently; interfaces assumed, never declared | **C**: versioned schemas, consumer-driven contract tests | Contract drift: breaking schema changes without a version bump, per 100 changes | Change failure rate |
| **Verification** | Tests mirror the implementation: green, but behavior unchecked | **A**: acceptance tests from the spec, property and mutation tests | Verification effectiveness: mutation score on critical behavior, or critical requirements with automated tests. Proxy: code changes without test changes. Outcome: rework rate | Deployment frequency |
| **Observability** | New code paths ship without instrumentation; failures found late | **T**: SLOs, instrumentation as part of done | Telemetry coverage; time to detect | Recovery time |
| **Coupling** | Each change touches more of the system | **S**: simplification budget, deletion, module boundaries | Change cost: areas and lines per change | Lead time |
| **Decision** | Rubber-stamp reviews, undocumented hotfixes, no clear owner | **Governance** (below) | Decision latency; review depth relative to PR size; share of PRs merged without review | Lead time |

**Governance is the layer under all four controls, not a fifth letter.** Someone named owns intent,
domain behavior, the definition of done, and every high-risk call. CATS makes those decisions cheaper and
better informed, but it can't make them for you.

## 4. Paired metrics

DORA metrics primarily describe delivery outcomes. The paired indicators are meant to give earlier
signals about the controls that sustain those outcomes (whether they lead in practice is what the
propositions test):

| DORA metric (outcome) | Paired indicator (earlier signal) |
|---|---|
| Deployment frequency | Verification effectiveness: mutation score on critical behavior, or the share of critical requirements with automated verification. The share of code changes merged without test changes is a supporting proxy: some valid changes need no new tests, and new tests need not be good ones. Rework rate, itself a DORA metric, corroborates |
| Lead time | Decision latency, and change cost |
| Change failure rate | Contract drift |
| Recovery time | Telemetry coverage, and time to detect |

**The signature of hidden delivery debt:** the DORA metric improves or holds steady while its paired
indicator gets worse. "Deployments up, rework up" means you are busier, not faster.

## 5. Decision rules

Check every window. Compare each measure with **your own trailing baseline**: the last 3 months against
the 6 before them, by default. A move counts when it exceeds one standard deviation of the baseline and a
minimum practical size. These are starting heuristics, not validated thresholds: calibrate them against
your history. Change size, rework and latency are skewed, so if a few outlier months dominate, use the
median and median absolute deviation instead (`--robust`). There are no universal thresholds, because
teams differ too much.

| Rule | When | Do |
|---|---|---|
| **R0 · Scale cautiously** | AR steady or rising, no indicator fired | Conditions support cautiously expanding AI-assisted delivery, while monitoring the paired indicators. A steady AR is not proof of safety |
| **R1 · Hold** | P rising while AR falls | Pause expansion; use the diagnostic matrix (section 3) to identify the control requiring investment |
| **R2** | Contract drift rising | Invest in **C** first |
| **R3** | Verification weakening, rework rising, or escaped defects rising, and contract drift flat | Invest in **A** |
| **R4** | Time to detect or recover rising, or telemetry coverage falling | Invest in **T** |
| **R5** | Change cost rising | Invest in **S**: a simplification budget, sized to the share of code AI writes |
| **R6** | Decision latency rising, review depth falling as PRs grow, or more PRs merged without review | Cap PR size; require review and decision records for high-risk changes |

**When several fire,** prioritize contract integrity and verification of critical behavior, and close
telemetry gaps that prevent diagnosis. The default order is C → A → T → S: contracts define what to
verify, verification defines what to observe, and simplification lowers the cost of all three. Move
simplification earlier when coupling or change cost is the dominant constraint. Address decision debt
(R6) in parallel, because governance sits underneath everything. *The order is a hypothesis.* It hasn't
been tested yet; tell us if your experience differs.

## 6. Measuring it

### With `absorption-meter`

Requires Python 3.9 or later.

```bash
pip install git+https://github.com/lakshmipriyagopalsamy/absorption-meter
absorption-meter analyze path/to/repo --since 2025-01-01
```

The tool reads only the git history on your machine; nothing is uploaded. It needs **at least nine
months of history** (a six-month baseline plus a three-month recent window); with less, the report says
*Not enough history*.

To see a full report before using your own data, clone the repository and run it on the synthetic demo
team, where every signal fires:

```bash
absorption-meter analyze --input examples/demo/changes.jsonl --team-metrics examples/demo/team.csv
```

To see why a healthy-looking AR isn't enough, run the second demo, a small team whose AR stays near
0.89 while reviews thin out and field defects rise. AR alone says *Scale cautiously*; with the review and
defect data the verdict is *Address*, with cautions:

```bash
absorption-meter analyze --input examples/unexamined/changes.jsonl --late-window 14      # AR alone
absorption-meter analyze --input examples/unexamined/changes.jsonl \
  --prs examples/unexamined/prs.json --team-metrics examples/unexamined/team.csv          # with review and defect data
```

The tool reads mainline history and gives you P, A and AR_repo by month, rework, change cost, revert and
patch-release rates, and contract drift for OpenAPI and JSON Schema files (a partial compatibility check; see the README's scope section). Add:

- `--github OWNER/REPO` for lead time, decision latency and review depth from pull requests (set
  `GITHUB_TOKEN`);
- `--team-metrics team.csv` for what git can't see: telemetry coverage, time to detect, recovery time,
  deployments and change failure rate from your own systems. Template:
  [`team-metrics-template.csv`](team-metrics-template.csv);
- `--fail-on-signal` to fail a CI job on a debt signal or a Hold verdict.

As a GitHub Action, with `fetch-depth: 0` so the whole history is available:

```yaml
- uses: actions/checkout@v4
  with: { fetch-depth: 0 }
- uses: lakshmipriyagopalsamy/absorption-meter@v0.2.1
  with: { github-prs: "true" }
```

### Using the tool on your team

**Who and how often.** An engineering manager or platform lead runs it on one repository, once a month,
and reviews the result with the team. Compare each repository only with its own history, never with
another team's numbers.

**Reading the report**, top to bottom:

1. **Decision.** 🟢 *Scale cautiously* (R0): absorption is holding and no indicator has moved.
   🔴 *Hold* (R1): production is rising while AR_repo falls, so pause expanding AI use. 🟡 *Address*:
   an indicator has moved; the rule that fired (R2–R6) names the CATS control to strengthen first.
   ⚪ *Not enough history*: fewer than nine months.
   **Cautions**, when listed, say AR_repo may overstate absorption: absorbed change that wasn't
   reviewed, fixes arriving late, or escaped defects rising. They don't change the verdict, but treat a
   healthy-looking AR with suspicion until you've checked them.
2. **Paired metrics.** Each DORA metric beside its earlier signal. ⚠️ *debt signal* means the DORA metric
   held or improved while its indicator worsened.
3. **Month by month.** Changes, AR_repo, rework, late rework, untested share, change size and modules
   touched; with pull-request data, also unreviewed share and examined AR; with team data, escaped
   defects. Read the trend, not a single month.
4. **Contract drift.** Schema changes that broke compatibility without a version bump, with what broke.

**Acting on it.** Pick the one control the rules point to, set a target for its indicator, name an
owner, and run the tool again next month (section 7 has the 30-day path).

**Other useful options.**

| Option | Use |
|---|---|
| `--format json -o report.json` | Feed a dashboard or keep a monthly record |
| `--as-of YYYY-MM-DD` | Analysis date. Changes whose 14-day window hasn't closed by then are left out (default: today) |
| `--robust` | Median-based baseline, steadier when one unusual month would skew the comparison |
| `--prs prs.json` | Pull-request data saved as JSON (the records `--github` reads), analyzed offline |
| `--late-window 90` | Late rework: fixes after the 14-day window but within this many days |

**Sharing results without sharing code.** `export` writes a dataset with change sizes, file paths, fix
and revert markers and release tags, and **no names, e-mail addresses, commit messages or code**:

```bash
absorption-meter export path/to/repo -o our-team.jsonl
absorption-meter analyze --input our-team.jsonl      # anyone can reproduce the report from it
```

Use it to share a history with a researcher or another team. File paths are included, so check them
before sharing outside your company. Or share only the report.

### Without the tool

You can measure every number by hand, monthly, in a spreadsheet:

1. **P:** merged PRs (or deployments).
2. **Verification:** of last month's code changes, how many were merged without any test change?
3. **Rework:** of last month's merged PRs, how many were reverted, hotfixed, or had a fix to the same
   files within 14 days? A ≈ P × (1 − rework share).
4. **Contract drift:** how many API or event schema changes broke compatibility without a version bump?
5. **Change cost:** median lines changed, and top-level modules touched, per PR.
6. **Decision latency:** median hours from PR opened to first review. Also count the PRs merged with no
   review from anyone but the author.
7. **Telemetry coverage:** of last month's changes, how many shipped with the logs, metrics or traces
   needed to see them fail?
8. **Late and escaped defects:** how many fixes landed 15–90 days after the change they repaired, and
   how many defects reached production or the field?

## 7. Getting started

### Measure first: a 30-day path

**Week 1: baseline.** Compute P, A and AR for the past six months from merge history. Choose W (start
with 14 days). Look at the trend, not the level.
**Week 2: indicators.** Add rework rate and contract drift; add decision latency if you have review data.
**Week 3: rules.** Run R0–R6 against the baseline. Agree as a team which row of the matrix the signals
point to.
**Week 4: one control.** Pick the first control the rules point to, set a target for its indicator, and
name an owner. Run the loop again next window.

### Fix first: a two-week start

If you already know where it hurts, start fixing while you measure.

**Week 1: baseline and boundaries**
- Record rework rate and review queue time for the last three months.
- Pick the two or three boundaries that break most often. Write each one down as a contract: schema,
  field meanings, owner.
- Gate CI on schema validation for those boundaries.

**Week 2: verification, telemetry, one simplification**
- Write an invariant test suite for the rules people know but the code doesn't show. People name the
  invariants; AI can help cover them.
- Add drift alerts and a feature flag and rollback template for risky changes.
- Remove one hidden dependency as part of a feature you're already building.

**Four weeks later:** run the measures again and compare with the baseline.

## 8. Self-check (draft, not yet validated)

Answer yes or no for one service or team. Each "no" points to a control. A validated version of this
check is planned; until then, treat it as a conversation starter, not a score.

**Contracts**
- [ ] Every external interface (API, event, file format) has a machine-readable schema in the repo.
- [ ] Each schema has a version, and breaking changes require a major-version bump.
- [ ] CI fails on breaking schema changes.
- [ ] Field meanings and owners are written down, not only in people's heads.

**Automated verification**
- [ ] Domain rules (invariants) have tests written from the spec, not from the implementation.
- [ ] Some critical areas use property-based or mutation testing.
- [ ] AI-generated tests are reviewed for what they assert, not only for passing.
- [ ] Security and schema checks run in CI on every change.

**Telemetry**
- [ ] "Done" includes the instrumentation needed to see the change fail.
- [ ] Services have SLOs, with alerts tied to them.
- [ ] Risky changes ship behind a flag, with a rollback someone can run alone at night.
- [ ] You know your time to detect, not just your time to recover.

**Simplification**
- [ ] The team has an explicit budget for removing coupling and dead code.
- [ ] You track files or modules touched per change.
- [ ] Module boundaries are enforced (for example, by dependency rules in CI).

**Governance**
- [ ] Every high-risk change has a named human owner who makes the call.
- [ ] PR size is capped, or large PRs need an explicit reason.
- [ ] Significant decisions leave a decision record.

## 9. Operational definitions

Exactly what `absorption-meter` computes. Defaults are in brackets; all are configurable.

| Measure | Operational definition | Unit |
|---|---|---|
| Change | One commit on the branch's first-parent history: a merge, a squash-merged PR or a direct commit. A merge counts once, diffed against its first parent. Lockfiles, vendored, built and binary files are dropped; changes left empty, and dependency-bot changes, are excluded | – |
| Size weight *s(c)* | ln(1 + lines added + lines deleted) | – |
| Matured change | A change whose rework window [*W* = 14 days] has fully elapsed by the analysis date (today by default; `--as-of` or `--until` set it, and a dataset uses the date it was read). Only matured changes enter P, A, AR and rework | – |
| P (production) | Σ *s(c)* over the month's matured changes | size-weighted changes / month |
| Reworked | Within *W* days of merge, a later change reverts it (`This reverts commit <sha>`), or a later change whose message matches *fix, bug, hotfix, regression, revert, rollback, broke, patch* touches at least one of the same files | yes / no |
| Rework rate | Reworked matured changes ÷ matured changes (a count, not size-weighted). A DORA outcome, used here to corroborate | share |
| Verification proxy (repository) | Share of the month's code changes merged without touching any test file. Test files follow common conventions (`test/`, `tests/`, `spec/`, `__tests__/`, `test_*.py`, `*_test.go`, `*.test.ts`, `*_spec.rb`, `*Test.java` …); changes touching only documentation or configuration are left out. Observable at merge; no window | share (lower is better) |
| Verification effectiveness (team, primary) | Team-reported mutation score on critical behavior (`mutation_score`), or the share of critical requirements with automated verification (`critical_verified`), in the team CSV. Either replaces the repository proxy when present; mutation score is preferred if both are given | 0–1 (higher is better) |
| A (absorption) | Σ *s(c)* over matured changes not reworked. The full model also requires a first-run CI pass; without CI data the tool computes the repository proxy, **AR_repo** | size-weighted changes / month |
| AR | A ÷ P. The tool reports **AR_repo**, A without the first-run CI term, because version control does not record CI results | 0–1 |
| Late rework | Of the changes whose late window [90 days] has closed, the share reworked after *W* days but within the late window (same rule as rework). Catches defects that surface weeks later but are fixed in the repository | share |
| Examined absorption | With pull-request data: size-weighted share of matured changes that were absorbed **and** reviewed by someone other than the author. Changes without a pull request count as unexamined; months before the pull-request data begins are left blank. AR_repo minus this is unexamined absorption | 0–1 |
| Unreviewed share | With pull-request data: share of the month's merged pull requests with no review from anyone but the author. A rising share fires R6 | share |
| Escaped defects (team) | Defects found after release, in production or the field (`escaped_defects` in the team CSV), per 100 changes; `days_to_first_defect` is the median days from release to the first. Rising escaped defects, or a falling time to first defect, fire R3 | per 100 changes; days |
| Cautions | Signs that AR_repo may overstate absorption: examined absorption falling or far below AR_repo, unreviewed share rising, late rework rising, escaped defects rising. Listed under the decision; they never change the verdict on their own | – |
| D (delivery debt) | Running total of P − A: change shipped but not absorbed. Records debt incurred and never decreases; remediation is tracked separately. Not a measure of technical debt in the code | size-weighted changes |
| Contract drift | A change to an OpenAPI/Swagger or JSON Schema file that breaks compatibility while its version (`info.version`, `version` or `$id`) is unchanged. A version change that keeps the major number is also counted. *Breaking:* a removed path, operation or 2xx response; a removed response property, or one no longer required; a newly required request parameter or property; a changed type; an enum value removed from a request. Moved or deleted files are not counted | events per 100 changes / month |
| Change cost | Median lines changed per change, and mean number of top-level directories touched per change | lines; directories |
| Deployment frequency | Semantic-version release tags per month (when there are at least 6 in the period); otherwise merged changes per month | per month |
| Change failure rate | Share of releases followed within 7 days by a patch release of the same major.minor; without releases, the share of changes later reverted | share |
| Recovery time | Median hours from a failed release to its patch release, or team-reported | hours |
| Lead time | Median hours from PR opened to merged (GitHub API) | hours |
| Decision latency | Median hours from PR opened to the first review submitted by someone other than the author (GitHub API; bot-authored PRs excluded) | hours |
| Review depth | Review comments per 100 changed lines, over the month's merged PRs | comments / 100 lines |
| Telemetry coverage | Team-reported: the share of the month's changes that shipped with the logs, metrics or traces needed to detect their failure. Decide the checklist as a team, for example as a PR-template checkbox | share |
| Time to detect | Team-reported: median hours from a failure starting to its detection | hours |
| Trend | Mean of the last [3] months against the previous [6]. A move counts when the difference exceeds both [1] × the baseline spread (standard deviation, or 1.4826 × MAD with `--robust`) and a practical minimum: 2 points for rework and AR, 5 for patch-release rate and telemetry coverage, 1 for revert rate, 0.5 per 100 for drift, 20% for recovery and detection times, 10% otherwise | up / down / flat |

## 10. Help build an open benchmark

Teams can share anonymized monthly results so everyone can compare against a baseline that isn't their
own. Run `absorption-meter analyze --format json`, remove anything identifying, and share the `months`
and `pairs` sections. A submission process will be announced in this repository. Never share data your
employer hasn't approved for release.
