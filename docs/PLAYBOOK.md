# The CATS playbook: measure absorption, not just speed

A practical guide for engineering teams using AI to write code. It explains the framework, how to measure
it with or without the `absorption-meter` tool, and what to do when a signal fires.

The research paper behind it is [`paper/main.pdf`](../paper/main.pdf).

## 1. The idea in one paragraph

AI raises how fast a team can **produce** change. It doesn't raise how fast the system can **absorb**
change: verify it, integrate it, observe it, and decide on it without breaking. When production outruns
absorption, the gap builds up as **delivery debt**. DORA metrics measure the pipeline, so they can stay
green while the debt grows. CATS (Contracts, Automated verification, Telemetry, Simplification) is how
you raise absorption capacity. Paired metrics are how you see the gap before it shows up as incidents.

## 2. Three numbers

Measure over a rolling window, monthly by default:

| Symbol | Name | Definition |
|---|---|---|
| **P** | Production | Changes merged, weighted by size. `absorption-meter` uses log(1 + lines changed), so one huge change can't dominate |
| **A** | Absorption | The part of P that was absorbed safely: not reverted, hotfixed or reworked within *W* days (default 14) |
| **AR** | Absorption ratio | A / P, between 0 and 1 |

Delivery debt is a level that rises with the unabsorbed part of production and falls as you repay it:
**D(t) = D(t−1) + (P − A) − R**, where R is the work spent repaying it.

Watch AR's **trend** against your own history. A falling AR while P rises is the clearest single sign
that you are taking on change faster than you can absorb it.

## 3. Where delivery debt hides

| Debt | How it shows up with AI | CATS control | Leading indicator | Paired DORA metric |
|---|---|---|---|---|
| **Contract** | Schemas or field meanings change silently; interfaces assumed, never declared | **C**: versioned schemas, consumer-driven contract tests | Contract drift: breaking schema changes without a version bump, per 100 changes | Change failure rate |
| **Verification** | Tests mirror the implementation: green, but behavior unchecked | **A**: acceptance tests from the spec, property and mutation tests | Rework rate | Deployment frequency |
| **Observability** | New code paths ship without instrumentation; failures found late | **T**: SLOs, instrumentation as part of done | Telemetry coverage; time to detect | Recovery time |
| **Coupling** | Each change touches more of the system | **S**: simplification budget, deletion, module boundaries | Change cost: areas and lines per change | Lead time |
| **Decision** | Rubber-stamp reviews, undocumented hotfixes, no clear owner | **Governance** (below) | Decision latency; review depth relative to PR size | Lead time |

**Governance is the layer under all four controls, not a fifth letter.** Someone named owns intent,
domain behavior, the definition of done, and every high-risk call. CATS makes those decisions cheaper and
better informed, but it can't make them for you.

## 4. Paired metrics

Each DORA metric lags. Read it next to the indicator that leads it:

| DORA metric (lags) | Paired indicator (leads) |
|---|---|
| Deployment frequency | Rework rate |
| Lead time | Decision latency, and change cost |
| Change failure rate | Contract drift |
| Recovery time | Telemetry coverage, and time to detect |

**The signature of hidden delivery debt:** the DORA metric improves or holds steady while its paired
indicator gets worse. "Deployments up, rework up" means you are busier, not faster.

## 5. Decision rules

Check every window. Compare each measure with **your own trailing baseline**: the last 3 months against
the 6 before them, by default. A move counts when it exceeds one standard deviation of the baseline and a
minimum practical size. There are no universal thresholds, because teams differ too much.

| Rule | When | Do |
|---|---|---|
| **R0 · Scale** | AR steady or rising, no indicator fired | Safe to expand AI use |
| **R1 · Hold** | P rising while AR falls | Stop expanding AI throughput; use the table in section 3 to find which indicator moved |
| **R2** | Contract drift rising | Invest in **C** first |
| **R3** | Rework rising, contract drift flat | Invest in **A** |
| **R4** | Time to detect or recover rising, or telemetry coverage falling | Invest in **T** |
| **R5** | Change cost rising | Invest in **S**: a simplification budget, sized to the share of code AI writes |
| **R6** | Decision latency rising, or review depth falling as PRs grow | Cap PR size; require decision records for high-risk changes |

**When several fire, work in the order C → A → T → S.** Contracts define what to verify, verification
defines what to observe, and simplification lowers the cost of all three. R6 runs alongside, because
governance sits underneath everything. *This order is a hypothesis.* It hasn't been tested yet; tell us
if your experience differs.

## 6. Measuring it

### With `absorption-meter`

```bash
pip install absorption-meter        # or: pip install git+https://github.com/<owner>/<repo>
absorption-meter analyze path/to/repo --since 2025-01-01
```

The tool reads mainline history and gives you P, A and AR by month, rework, change cost, revert and
patch-release rates, and contract drift for OpenAPI and JSON Schema files. Add:

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
- uses: <owner>/<repo>@v0.1.0
  with: { github-prs: "true" }
```

### Without the tool

You can measure every number by hand, monthly, in a spreadsheet:

1. **P:** merged PRs (or deployments).
2. **Rework:** of last month's merged PRs, how many were reverted, hotfixed, or had a fix to the same
   files within 14 days? A ≈ P × (1 − rework share).
3. **Contract drift:** how many API or event schema changes broke compatibility without a version bump?
4. **Change cost:** median files or modules touched per PR.
5. **Decision latency:** median hours from PR opened to first review.
6. **Telemetry coverage:** of last month's changes, how many shipped with the logs, metrics or traces
   needed to see them fail?

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

## 9. Help build an open benchmark

Teams can share anonymized monthly results so everyone can compare against a baseline that isn't their
own. Run `absorption-meter analyze --format json`, remove anything identifying, and share the `months`
and `pairs` sections. A submission process will be announced in this repository. Never share data your
employer hasn't approved for release.
