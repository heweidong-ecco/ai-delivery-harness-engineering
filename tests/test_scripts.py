import ast
import subprocess
from pathlib import Path

import pytest


def test_check_pytest_report_missing_file() -> None:
    result = subprocess.run(
        ["python", "scripts/check_pytest_report.py", "not-exist.json"],
        capture_output=True,
    )
    assert result.returncode != 0


def test_check_harness_docs() -> None:
    result = subprocess.run(
        ["python", "scripts/check_harness_docs.py"],
        capture_output=True,
    )
    assert result.returncode == 0


def test_check_layers_no_rules() -> None:
    result = subprocess.run(
        ["python", "scripts/check_layers.py", "src"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "no rules" in result.stdout.lower()


def test_check_python_rules_smoke() -> None:
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", "src"],
        capture_output=True,
    )
    assert result.returncode == 0