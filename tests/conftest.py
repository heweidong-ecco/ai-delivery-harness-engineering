"""pytest 公共 fixture。

> 精简说明(2026-09-11):这里原先有 15 个 fixture,**13 个无人使用** ——
> 包括 `harness_root` / `scripts_root` / `docs_root` / `tmp_python_file` /
> `sample_req_dir` / `incomplete_req_dir` / `passed_report` / `failed_report` /
> `zero_test_report` / `sample_good_code` / `sample_bad_code` / `sample_code_file`。
> 死 fixture 会让读者以为"这些约定有人在守",实际没有 —— 已删除。
> 需要新夹具时**随用随加**,不要预先囤积。
"""

from __future__ import annotations

import os
from collections.abc import Iterator
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def project_root() -> Path:
    """项目根目录。"""
    return Path(__file__).resolve().parent.parent


# ============================================================
# subprocess 覆盖率
# ============================================================


@pytest.fixture(scope="session", autouse=True)
def _subprocess_coverage(tmp_path_factory: pytest.TempPathFactory, project_root: Path) -> None:
    """让 tests 里以 **subprocess** 方式运行的脚本也计入覆盖率。

    本仓的脚本几乎全部靠 `subprocess.run([sys.executable, "scripts/..."])` 驱动,
    子进程是另一个解释器 —— 进程内覆盖率**看不见**它们。不处理这一点,
    `.coveragerc` 里的阈值就永远指向一个 0.00% 的假数字
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
