"""pytest 公共 fixture。"""

from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest


# ============================================================
# 路径 fixture
# ============================================================


@pytest.fixture(scope="session")
def project_root() -> Path:
    """项目根目录。"""
    return Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def harness_root(project_root: Path) -> Path:
    """harness 目录。"""
    return project_root / "harness"


@pytest.fixture(scope="session")
def scripts_root(project_root: Path) -> Path:
    """scripts 目录。"""
    return project_root / "scripts"


@pytest.fixture(scope="session")
def docs_root(project_root: Path) -> Path:
    """docs 目录。"""
    return project_root / "docs"


# ============================================================
# 临时目录 fixture
# ============================================================


@pytest.fixture
def tmp_python_file(tmp_path: Path) -> Path:
    """空的 Python 文件。"""
    f = tmp_path / "sample.py"
    f.write_text("", encoding="utf-8")
    return f


@pytest.fixture
def sample_req_dir(tmp_path: Path) -> Iterator[Path]:
    """完整的临时需求目录。"""
    req_dir = tmp_path / "REQ-TEST"
    req_dir.mkdir()
    files = {
        "requirement-analysis.md": "# 需求分析\n\n## 背景\n\n## 目标\n",
        "task-breakdown.md": "# 任务拆分\n\n| 任务 | 层 | 负责人 |\n|---|---|---|\n",
        "coding-report.md": "# 编码报告\n\n## 改动文件\n",
        "unit-test-report.md": "# 单测报告\n\n## 覆盖接口\n",
        "ci-result.md": "# CI 结果\n\n- Status: SUCCESS\n- TotalTest: 1\n- Passed: 1\n",
        "deploy-validation.md": "# 部署验证\n\n## 环境参数确认\n",
    }
    for name, content in files.items():
        (req_dir / name).write_text(content, encoding="utf-8")
    yield req_dir


@pytest.fixture
def incomplete_req_dir(tmp_path: Path) -> Iterator[Path]:
    """不完整的临时需求目录。"""
    req_dir = tmp_path / "REQ-INCOMPLETE"
    req_dir.mkdir()
    (req_dir / "requirement-analysis.md").write_text("# 需求分析\n", encoding="utf-8")
    yield req_dir


# ============================================================
# pytest report fixture
# ============================================================


@pytest.fixture
def pytest_report_passed(tmp_path: Path) -> Path:
    """通过的 pytest 报告。"""
    f = tmp_path / "report-passed.json"
    f.write_text(
        json.dumps({"summary": {"total": 5, "passed": 5, "failed": 0, "error": 0}}),
        encoding="utf-8",
    )
    return f


@pytest.fixture
def pytest_report_failed(tmp_path: Path) -> Path:
    """失败的 pytest 报告。"""
    f = tmp_path / "report-failed.json"
    f.write_text(
        json.dumps({"summary": {"total": 5, "passed": 3, "failed": 2, "error": 0}}),
        encoding="utf-8",
    )
    return f


@pytest.fixture
def pytest_report_zero_tests(tmp_path: Path) -> Path:
    """测试数为 0 的报告。"""
    f = tmp_path / "report-zero.json"
    f.write_text(
        json.dumps({"summary": {"total": 0, "passed": 0, "failed": 0, "error": 0}}),
        encoding="utf-8",
    )
    return f


# ============================================================
# 代码样本 fixture
# ============================================================


@pytest.fixture
def sample_good_code() -> str:
    """符合规范的代码。"""
    return '''
from datetime import datetime, UTC

def get_price(order_id: int) -> int:
    """获取价格，单位分。"""
    return 9900

def call_api(url: str) -> None:
    """调用外部服务。"""
    import httpx
    httpx.post(url, timeout=3)
'''


@pytest.fixture
def sample_bad_code() -> str:
    """违反多条规则的代码。"""
    return '''
import requests

def get_price(price: float) -> None:
    print("debug")
    requests.post("http://x")
    try:
        eval("1+1")
    except:
        pass
'''


@pytest.fixture
def sample_code_file(tmp_path: Path, sample_bad_code: str) -> Path:
    """含违规代码的文件。"""
    f = tmp_path / "bad.py"
    f.write_text(sample_bad_code, encoding="utf-8")
    return f


# ============================================================
# Git fixture
# ============================================================


@pytest.fixture
def git_repo(tmp_path: Path) -> Iterator[Path]:
    """初始化一个临时 git 仓库。"""
    import subprocess

    subprocess.run(["git", "init", "-b", "main"], cwd=tmp_path, check=True, capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=tmp_path,
        check=True,
        capture_output=True,
    )
    yield tmp_path
