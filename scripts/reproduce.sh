#!/usr/bin/env bash
# Regenerate every committed output from the committed datasets. No network, no repository clones.
# After running, `git status` should show no changes: if it does, the outputs are not reproducible.
set -euo pipefail
cd "$(dirname "$0")/.."
AM="${AM:-absorption-meter}"
PY="${PY:-python}"

# Demo: a synthetic team (deterministic generator).
$PY examples/demo/make_demo.py
$AM analyze --input examples/demo/changes.jsonl --team-metrics examples/demo/team.csv -o examples/demo/report.md
$AM analyze --input examples/demo/changes.jsonl --team-metrics examples/demo/team.csv --format json -o examples/demo/report.json

# Worked example: Homebrew/brew mainline, Jul 2024 - Oct 2026 (dataset pinned to a commit).
$AM analyze --input examples/homebrew/changes.jsonl -o examples/homebrew/report.md
$AM analyze --input examples/homebrew/changes.jsonl --format json -o examples/homebrew/report.json
$PY scripts/rule_timeline.py examples/homebrew/changes.jsonl examples/homebrew --from 2025-01

# Paper figures.
$PY scripts/simulate_model.py paper/model.dat
$PY scripts/paper_data.py
echo "Done. Check with: git status --short"
