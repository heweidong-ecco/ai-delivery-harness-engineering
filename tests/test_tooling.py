"""辅助脚本测试 —— audit_log / collect_metrics。

反外审附加:tests/README.md 写着「每个新脚本必须新增测试」,但这两个脚本
原先**一条测试都没有**(覆盖率 0%),属于"写了但没人验证过"。
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"


def run(script: str, *args: str, cwd: Path) -> subprocess.CompletedProcess[str]:
    """这两个脚本按**相对路径**写产物,故必须在临时目录里跑,避免污染本仓。"""
    return subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
    )


# ============================================================
# audit_log
# ============================================================


def test_audit_log_writes_record(tmp_path: Path) -> None:
    result = run("audit_log.py", "规则新增", "新增 ERR-006", cwd=tmp_path)
    assert result.returncode == 0

    written = list((tmp_path / "harness" / "audit").glob("*.md"))
    assert len(written) == 1
    content = written[0].read_text(encoding="utf-8")
    assert "规则新增" in content
    assert "新增 ERR-006" in content


def test_audit_log_requires_two_arguments(tmp_path: Path) -> None:
    assert run("audit_log.py", "只有一个参数", cwd=tmp_path).returncode == 1


# ============================================================
# check_dependencies
# ============================================================


def stub_pip_audit(bin_dir: Path, exit_code: int, output: str = "") -> dict[str, str]:
    """放一个假的 pip-audit 到 PATH 最前面,用来验证**退出码语义**。"""
    bin_dir.mkdir(parents=True, exist_ok=True)
    stub = bin_dir / "pip-audit"
    stub.write_text(f"#!/usr/bin/env bash\necho '{output}'\nexit {exit_code}\n", encoding="utf-8")
    stub.chmod(0o755)
    return dict(os.environ, PATH=f"{bin_dir}{os.pathsep}{os.environ['PATH']}")


def test_check_dependencies_fails_when_audit_fails(tmp_path: Path) -> None:
    """H11:CI 与脚本必须同一口径 —— 审计失败 = 门禁失败(不许 `|| true` 吞掉)。"""
    env = stub_pip_audit(tmp_path / "bin", 1, "vulnerability found")
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_dependencies.py")],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )
    assert result.returncode == 1
    assert "vulnerability found" in result.stdout


def test_check_dependencies_passes_when_audit_passes(tmp_path: Path) -> None:
    env = stub_pip_audit(tmp_path / "bin", 0)
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_dependencies.py")],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )
    assert result.returncode == 0
    assert "passed" in result.stdout.lower()


# ============================================================
# collect_metrics
# ============================================================


def test_collect_metrics_writes_counts(tmp_path: Path) -> None:
    result = run("collect_metrics.py", cwd=tmp_path)
    assert result.returncode == 0

    written = list((tmp_path / "harness" / "metrics" / "data").glob("metrics-*.json"))
    assert len(written) == 1
    data = json.loads(written[0].read_text(encoding="utf-8"))
    for key in ("collected_at", "rule_commits", "agent_commits", "docs_commits", "fix_commits"):
        assert key in data
        assert isinstance(data[key], (int, str))


def test_collect_metrics_counts_matching_commits(git_repo: Path) -> None:
    """在真实 git 仓库里,'rule:' 前缀的提交要真的被数到。"""
    for message in ("rule: add ERR-006", "rule: add SEC-007", "docs: update readme"):
        subprocess.run(
            ["git", "commit", "--allow-empty", "-m", message],
            cwd=git_repo,
            check=True,
            capture_output=True,
        )

    assert run("collect_metrics.py", cwd=git_repo).returncode == 0

    written = list((git_repo / "harness" / "metrics" / "data").glob("metrics-*.json"))
    data = json.loads(written[0].read_text(encoding="utf-8"))
    assert data["rule_commits"] == 2
    assert data["docs_commits"] == 1
    assert data["fix_commits"] == 0
