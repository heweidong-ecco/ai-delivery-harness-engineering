#!/usr/bin/env bash
set -euo pipefail

PYTHON="${PYTHON:-python3.11}"

echo "==> Creating venv"
"$PYTHON" -m venv .venv

echo "==> Activating venv"
# shellcheck disable=SC1091
source .venv/bin/activate

echo "==> Upgrading pip"
pip install --upgrade pip

echo "==> Installing dev deps"
pip install -e ".[dev]"

echo "==> Installing hooks"
pre-commit install
pre-commit install --hook-type commit-msg

echo "==> Configuring git message template"
git config commit.template .gitmessage

echo "==> Running gate"
make gate

echo "==> Done"
