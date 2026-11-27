# Rework linkage in v0.3: method change, specified before re-running any results

Status: **specified on 27 November 2026, before applying it to any dataset.** This file is committed
ahead of the implementation and the re-runs, so the commit history shows the rules were fixed in advance
and not tuned to the results.

## Why

The field tests on ten public projects (examples/field-tests) showed that file-linked rework over-counts
in busy repositories:
- **Hub files.** Files most changes touch, such as `Cargo.toml`, `CHANGELOG.md` and shared test
  configuration, link unrelated changes to later fixes.
- **Broad fix detection.** Conventional-commit titles such as `fix(deps): bump x` and `chore: fix lint` are
  counted as fixes.

v0.3 tightens both. Reverts are unchanged.

## Rule 1: what counts as a fix

A later change counts as a fix when its subject matches the existing fix pattern (fix, bug, hotfix,
regression, revert, broke, rollback, patch, ...) **and none** of these maintenance patterns (case-insensitive):

- a conventional-commit type other than fix: `^\s*(chore|build|ci|docs?|style|tests?|refactor|perf|release|bump)\b`;
- a maintenance scope on any type: `^\s*\w+\((deps?|dependencies|ci|docs?|build|release|lint)\)`;
- version bumps and typos anywhere in the subject: `\bbump(s|ed)?\b`, `\btypos?\b`.

## Rule 2: which shared files link a change to a fix

A fix links to an earlier change only through a shared file that is **not a hub file**. A path is a hub
file when either:

1. It matches a hub pattern:
   - changelogs and release notes (`CHANGELOG*`, `CHANGES*`, `HISTORY*`, `NEWS*`, `RELEASE*` at any depth);
   - package manifests (`Cargo.toml`, `package.json`, `pyproject.toml`, `setup.py`, `setup.cfg`, `go.mod`,
     `Gemfile`, `*.gemspec`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `requirements*.txt`);
   - version files (`VERSION`, `version.py`, `_version.py`, `version.txt`);
   - CI configuration under `.github/`.
2. Or, in a history of at least 100 changes, more than **10%** of the changes in the analysed history
   touched it.

The frequency rule is computed from the changes the analysis is given. In a month-by-month replay, that
means only the history up to the replay date, so no later data leaks in.

Hub files still count toward change size, production and change cost. They are only ignored when
linking fixes to earlier changes.

## What stays the same

Everything else stays as it is:
- the 14-day window, the matured-only cohort, the size weight and the trend test;
- the late-rework window and the decision rules;
- reverts.

## Reproducibility

- The v0.2 rule remains available as `--rework-rule legacy`.
- Datasets record both fix flags: `fix` (v0.3 rule) and `fix_legacy` (v0.2 rule). Older datasets, which
  have only `fix`, are read as legacy.
- The article's worked example will be re-run with the v0.3 rule. Its v0.1.1 results stay reproducible
  from the v0.1.1 release and with `--rework-rule legacy`.

## How it will be checked

1. **All datasets:** re-run Homebrew and the ten field-test projects with both rules, and report
   before-and-after for every project, whichever way the numbers move.
2. **Precision:** draw a random sample of rework links per project under each rule, and hand-label each
   as a real fix of the earlier change or not.
