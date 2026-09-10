"""脚本测试。"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

# ============================================================
# check_pytest_report
# ============================================================


def test_check_pytest_report_missing_file(tmp_path: Path) -> None:
    result = subprocess.run(
        [sys.executable, "scripts/check_pytest_report.py", str(tmp_path / "not-exist.json")],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_pytest_report_no_tests(tmp_path: Path) -> None:
    report = tmp_path / "report.json"
    report.write_text(json.dumps({"summary": {"total": 0, "passed": 0}}), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_pytest_report.py", str(report)],
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
        [sys.executable, "scripts/check_pytest_report.py", str(report)],
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
        [sys.executable, "scripts/check_pytest_report.py", str(report)],
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
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_python_rules_price_float(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("def f(price: float) -> None:\n    pass\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "PRICE-001" in result.stdout


def test_check_python_rules_http_timeout(tmp_path: Path) -> None:
    code = "import requests\n\ndef f() -> None:\n    requests.post('http://x')\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "HTTP-001" in result.stdout


def test_check_python_rules_bare_except(tmp_path: Path) -> None:
    code = "def f() -> None:\n    try:\n        pass\n    except:\n        pass\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "ERR-001" in result.stdout


def test_check_python_rules_print(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("print('hello')\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "LOG-001" in result.stdout


def test_check_python_rules_eval(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text("x = eval('1+1')\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_python_rules.py", str(tmp_path)],
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
        [sys.executable, "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_secrets_aws_key(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text(
        "key = 'AKIAIOSFODNN7EXAMPLE'\n",  # pragma: allowlist secret
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "AWS" in result.stdout


def test_check_secrets_private_key(tmp_path: Path) -> None:
    (tmp_path / "bad.py").write_text(
        "-----BEGIN RSA PRIVATE KEY-----\n",  # pragma: allowlist secret
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


def test_check_secrets_allowlist_marker_skips_that_line(tmp_path: Path) -> None:
    """行级豁免:`pragma: allowlist secret` 只放行**那一行**。

    本仓的测试必须包含假密钥才能验证扫描器可拦;没有行级豁免就只能整文件跳过,
    等于给该文件开永久盲区。这里同时验证"豁免是有边界的"。
    """
    (tmp_path / "ok.py").write_text(
        "key = 'AKIAIOSFODNN7EXAMPLE'  # pragma: allowlist secret\n", encoding="utf-8"
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, "带豁免标记的行仍被拦"


def test_check_secrets_allowlist_marker_does_not_leak_to_other_lines(tmp_path: Path) -> None:
    """**反向验证**:豁免只作用于标记所在行,同一文件里别的真密钥照样要拦。"""
    (tmp_path / "leak.py").write_text(
        "a = 'AKIAIOSFODNN7EXAMPLE'  # pragma: allowlist secret\nb = 'AKIAIOSFODNN7EXAMPLE'\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [sys.executable, "scripts/check_secrets.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "leak.py:2" in result.stdout


# ============================================================
# check_layers
# ============================================================


# 反外审 H6:这里原先有 `test_check_layers_no_rules`,断言的是
# `"no rules" in result.stdout` —— 即**把"规则列表为空、直接跳过"这个病态行为
# 当成了正确行为来锁死**。门禁空转被测试固化,是"软约束体制"最深的一层。
# 已删除;新行为(显式标注 UNIMPLEMENTED,而非静默跳过)由 test_gates.py 里的
# `test_check_layers_declares_unimplemented_rather_than_passing_silently` 覆盖。


# ============================================================
# check_complexity
# ============================================================


def test_check_complexity_ok(tmp_path: Path) -> None:
    (tmp_path / "ok.py").write_text("def f() -> int:\n    return 1\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_complexity_too_long(tmp_path: Path) -> None:
    lines = ["def f() -> None:"] + ["    x = 1"] * 60
    (tmp_path / "bad.py").write_text("\n".join(lines) + "\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_complexity.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0
    assert "CPLX-001" in result.stdout


def test_check_complexity_too_many_args(tmp_path: Path) -> None:
    args = ", ".join(f"a{i}: int" for i in range(10))
    (tmp_path / "bad.py").write_text(f"def f({args}) -> None:\n    pass\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_complexity.py", str(tmp_path)],
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
        [sys.executable, "scripts/check_complexity.py", str(tmp_path)],
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
        [sys.executable, "scripts/check_commit_msg.py", str(msg)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_commit_msg_invalid(tmp_path: Path) -> None:
    msg = tmp_path / "msg.txt"
    msg.write_text("bad message\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_commit_msg.py", str(msg)],
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
        [sys.executable, "scripts/check_commit_msg.py", str(msg)],
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
        [sys.executable, "scripts/check_i18n.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0


def test_check_i18n_naive_datetime(tmp_path: Path) -> None:
    code = "from datetime import datetime\nx = datetime.now()\n"
    (tmp_path / "bad.py").write_text(code, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "scripts/check_i18n.py", str(tmp_path)],
        capture_output=True,
        text=True,
    )
    assert result.returncode != 0


# ============================================================
# check_harness_docs / check-gates —— 见 tests/test_gates.py
# ============================================================
#
# 反外审 H3(2026-09-11):这里原先有 `test_check_harness_docs_passes`,
# 用的是 `pytest.skip(...)` 兜底 —— **门禁坏掉时,测试替它打掩护**,
# 而不是暴露它。这被外审称为"软约束体制的病理切片"。
#
# 两个测试**已删除并重写**到 `tests/test_gates.py`:
#   · 不再 skip —— 门禁坏了就是**测试红**;
#   · 补上"该拦的拦"(喂真实输入断言它真的拒绝)+ **反向验证**(把门禁改坏 → 测试必须红);
#   · 补上防腐断言(语法 / 可执行位 / 是否被 Makefile·CI·pre-commit 注册);
#   · 原先三个测试调用的是**不存在的** `scripts/check_gates.sh`(下划线),
#     真实文件是 `check-gates.sh`(连字符)—— 现已按新接口重写。
