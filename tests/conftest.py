"""pytest 公共 fixture。"""

from __future__ import annotations

import json
import os
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
# subprocess 覆盖率
# ============================================================


@pytest.fixture(scope="session", autouse=True)
def _subprocess_coverage(tmp_path_factory: pytest.TempPathFactory, project_root: Path) -> None:
    """让 tests 里以 **subprocess** 方式运行的脚本也计入覆盖率。

    本仓的脚本几乎全部靠 `subprocess.run([sys.executable, "scripts/..."])` 驱动,
    子进程是另一个解释器 —— 进程内覆盖率**看不见**它们。不处理这一点,
    `.coveragerc` 里的 `fail_under` 就永远指向一个 0.00% 的假数字
    (实测:741 条语句、0% 覆盖),覆盖率门禁形同虚设。

    做法是 coverage 支持的进程启动机制:往 PYTHONPATH 放一个 `sitecustomize.py`,
    它调用 `coverage.process_startup()`;子进程据此把覆盖率写进
    `.coverage.*` 并行数据文件,由 pytest-cov 在收尾时合并。
    """
    boot = tmp_path_factory.mktemp("covboot")
    (boot / "sitecustomize.py").write_text(
        "try:\n"
        "    import coverage\n"
        "\n"
        "    coverage.process_startup()\n"
        "except Exception:  # coverage 不可用时静默降级,不影响被测脚本\n"
        "    pass\n",
        encoding="utf-8",
    )
    # 子进程用的配置必须把 `source` 写成**绝对路径** —— 子进程的 cwd 不一定是
    # 仓库根(有些测试刻意在 tmp_path 里跑,避免往本仓写产物);
    # 而 .coveragerc 里的 `source = src, scripts` 是相对路径,在 tmp_path 下根本
    # 解析不到,表现为"脚本明明测过却是 0%"。
    child_rc = boot / "coveragerc"
    child_rc.write_text(
        "[run]\n"
        "branch = True\n"
        "parallel = True\n"
        f"source =\n    {project_root / 'src'}\n    {project_root / 'scripts'}\n"
        "omit =\n    */tests/*\n    */__init__.py\n"
        "[report]\n"
        "exclude_lines =\n"
        "    pragma: no cover\n"
        "    if __name__ == .__main__.:\n",
        encoding="utf-8",
    )
    os.environ["COVERAGE_PROCESS_START"] = str(child_rc)
    # 同上:并行数据文件默认落在子进程的 cwd,固定为绝对路径才收得回来。
    os.environ["COVERAGE_FILE"] = str(project_root / ".coverage")
    existing = os.environ.get("PYTHONPATH", "")
    os.environ["PYTHONPATH"] = f"{boot}{os.pathsep}{existing}" if existing else str(boot)


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
def sample_req_dir(tmp_path: Path, project_root: Path) -> Iterator[Path]:
    """完整的临时需求目录。

    直接**复制真实的变更模板**(`harness/changes/_template/`)并替换 REQ 占位符 ——
    而不是手写一份"看起来像"的内容。原先手写的版本与真实模板并不一致
    (例如 `ci-result.md` 被写成 `- Status: SUCCESS` 列表,而真实模板写的是
    `## 可程序化验证条件` 段落),这种 fixture 会让测试对着一个假契约变绿。
    """
    req_dir = tmp_path / "REQ-TEST"
    req_dir.mkdir()
    for template in sorted((project_root / "harness" / "changes" / "_template").glob("*.md")):
        if template.name == "README.md":
            continue
        (req_dir / template.name).write_text(
            template.read_text(encoding="utf-8").replace("REQ-XXXX", "REQ-TEST"),
            encoding="utf-8",
        )
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


# 注:fixture 名**不能**以 `pytest_` 开头 —— pytest 会把 conftest 里所有
# `pytest_*` 函数当作 hook 注册,名字对不上就 PluginValidationError(整个套件
# 连收集都跑不起来)。原先这三个叫 `pytest_report_*`,正是这个坑。
@pytest.fixture
def passed_report(tmp_path: Path) -> Path:
    """通过的 pytest 报告。"""
    f = tmp_path / "report-passed.json"
    f.write_text(
        json.dumps({"summary": {"total": 5, "passed": 5, "failed": 0, "error": 0}}),
        encoding="utf-8",
    )
    return f


@pytest.fixture
def failed_report(tmp_path: Path) -> Path:
    """失败的 pytest 报告。"""
    f = tmp_path / "report-failed.json"
    f.write_text(
        json.dumps({"summary": {"total": 5, "passed": 3, "failed": 2, "error": 0}}),
        encoding="utf-8",
    )
    return f


@pytest.fixture
def zero_test_report(tmp_path: Path) -> Path:
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
    return """
import requests

def get_price(price: float) -> None:
    print("debug")
    requests.post("http://x")
    try:
        eval("1+1")
    except:
        pass
"""


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
