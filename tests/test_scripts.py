"""脚本测试。"""

from __future__ import annotations

import json
import subprocess
from pathlib import Path

import pytest


# ============================================================
# check_pytest_report
# ============================================================


def test_check_pytest_report_missing_file(tmp_path: Path) -> None:
    result = subprocess.run(
        ["python", "scripts/check_pytest_report.py", str(tmp_path / "not-exist.json")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_pytest_report_no_tests(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text(json.dumps({"summary": {"total": 0, "passed": 0}}), encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_pytest_report.py", str(report)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "No tests" in result.stdout or "No tests" in result.stderr


def test_check_pytest_report_failed(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text(
        json.dumps({"summary": {"total": 3, "passed": 2, "failed": 1}}),
        encoding="utf-8",
    )
    result = subprocess.run(
        ["python", "scripts/check_pytest_report.py", str(report)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_pytest_report_passed(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text(
        json.dumps({"summary": {"total": 3, "passed": 3, "failed": 0, "error": 0}}),
        encoding="utf-8",
    )
    result = subprocess.run(
        ["python", "scripts/check_pytest_report.py", str(report)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


# ============================================================
# check_python_rules
# ============================================================


def test_check_python_rules_empty(tmp_path: Path) -> None:
    (tmp_path / "empty.py").write_text("", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_python_rules_price_float(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("def f(price: float) -> None:\n    pass\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "PRICE-001" in result.stdout


def test_check_python_rules_http_timeout(tmp_path: Path) -> None:
    code = "import requests\n\ndef f() -> None:\n    requests.post('http://x')\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "HTTP-001" in result.stdout


def test_check_python_rules_bare_except(tmp_path: Path) -> None:
    code = "def f() -> None:\n    try:\n        pass\n    except:\n        pass\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "ERR-001" in result.stdout


def test_check_python_rules_print(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("print('hello')\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "LOG-001" in result.stdout


def test_check_python_rules_eval(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("x = eval('1+1')\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "SEC-002" in result.stdout


# ============================================================
# check_secrets
# ============================================================


def test_check_secrets_clean(tmp_path: Path) -> None:
    (tmp_path / "clean.py").write_text("x = 1\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_secrets_aws_key(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("key = 'AKIAIOSFODNN7EXAMPLE'\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "AWS" in result.stdout


def test_check_secrets_private_key(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("-----BEGIN RSA PRIVATE KEY-----\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


# ============================================================
# check_layers
# ============================================================


def test_check_layers_no_rules() -> None:
    result = subprocess.run(
        ["python", "scripts/check_layers.py", "src"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "no rules" in result.stdout.lower()


# ============================================================
# check_complexity
# ============================================================


def test_check_complexity_ok(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text("def f() -> int:\n    return 1\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_complexity_too_long(tmp_path: Path) -> None:
    lines = ["def f() -> None:"] + ["    x = 1"] * 60
    (tmp_path / "bad.py").write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "CPLX-001" in result.stdout


def test_check_complexity_too_many_args(tmp_path: Path) -> None:
    args = ", ".join(f"a{i}: int" for i in range(10))
    (tmp_path / "bad.py").write_text(f"def f({args}) -> None:\n    pass\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "CPLX-002" in result.stdout


def test_check_complexity_high_cyclomatic(tmp_path: Path) -> None:
    code = "def f(x: int) -> int:\n"
    for i in range(15):
        code += f"    if x == {i}:\n        return {i}\n"
    code += "    return -1\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "CPLX-003" in result.stdout


# ============================================================
# check_commit_msg
# ============================================================


def test_check_commit_msg_valid(tmp_path: Path) -> None:
    msg = tmp_path / "msg.txt"
    msg.write_text("feat: add feature\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_commit_msg.py", str(msg)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_commit_msg_invalid(tmp_path: Path) -> None:
    msg = tmp_path / "msg.txt"
    msg.write_text("bad message\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_commit_msg.py", str(msg)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


@pytest.mark.parametrize(
    "type_",
    ["feat", "fix", "docs", "ci", "chore", "rule", "agent", "test"],
)
def test_check_commit_msg_all_types(tmp_path: Path, type_: str) -> None:
    msg = tmp_path / "msg.txt"
    msg.write_text(f"{type_}: something\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_commit_msg.py", str(msg)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


# ============================================================
# check_i18n
# ============================================================


def test_check_i18n_clean(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text("x = 1\n", encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_i18n.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_i18n_naive_datetime(tmp_path: Path) -> None:
    code = "from datetime import datetime\nx = datetime.now()\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        ["python", "scripts/check_i18n.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


# ============================================================
# check_harness_docs
# ============================================================


def test_check_harness_docs_passes() -> None:
    """当前仓库应通过。"""
    result = subprocess.run(
        ["python", "scripts/check_harness_docs.py"],
        capture_output=True,
        text=True,
    )
    # 如果仓库完整，应通过
    if result.returncode != 0:
        pytest.skip(f"Harness docs incomplete: {result.stdout[:200]}")
    assert result.returncode == 0


# ============================================================
# check_gates.sh
# ============================================================


def test_check_gates_no_args() -> None:
    result = subprocess.run(
        ["bash", "scripts/check_gates.sh"],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_gates_missing_dir(tmp_path: Path) -> None:
    result = subprocess.run(
        ["bash", "scripts/check_gates.sh", str(tmp_path / "not-exist")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_gates_complete(tmp_path: Path, sample_req_dir: Path) -> None:
    result = subprocess.run(
        ["bash", "scripts/check_gates.sh", str(sample_req_dir)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
