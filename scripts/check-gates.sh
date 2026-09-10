#!/usr/bin/env bash
set -euo pipefail

REQ_DIR="${1:-}"
if [ -z "$REQ_DIR" ]; then
  echo "Usage: $0 harness/changes/REQ-XXXX"
  exit 1
fi

required=(
  "requirement-analysis.md"
  "task-breakdown.md"
  "coding-report.md"
  "unit-test-report.md"
  "ci-result.md"
  "deploy-validation.md"
)

for f in "${required[@]}"; do
  if [ ! -f "$REQ_DIR/$f" ]; then
    echo "Missing: $REQ_DIR/$f"
    exit 1
  fi
done

echo "Gate check passed for $REQ_DIR"
