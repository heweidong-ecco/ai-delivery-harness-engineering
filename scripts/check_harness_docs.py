"""检查 Harness 文档完整性。

反外审 H2(2026-09-11):原实现硬编码 181 条路径,实测其中 6 条指向不存在的文件;
又因脚本自身第 1 行是 markdown 围栏(H1)而**从未执行**,故无人发现。
「274 行的路径清单维护不动,必然腐烂」—— 改为三层校验:

  ① ANCHORS   少量真正稳定的锚点文件(入口 / 配置 / CI),逐条必须存在;
  ② DIRECTORY 受治理目录必须存在且【非空】(按 glob 计数,不再逐文件列举);
  ③ SHAPE     受治理文档必须非空且以 H1 开头(抓 0 字节孤儿文件)。

关于工单建议的「必需 front-matter」:本仓**不存在 front-matter 约定**
(全仓仅 `.github/ISSUE_TEMPLATE/*.md` 以 `---` 开头),模板一律是
`# 标题` + `## 基本信息` + 表格。故这里校验本仓**实际**的约定(非空 + H1),
而不引入一个全仓都不存在的新约定。

用法:
    python scripts/check_harness_docs.py [--root <dir>]
退出码:0 = 通过;1 = 有缺陷;2 = 根目录不存在。
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# 代码围栏:3 个及以上反引号(```` 用于包住内含 ``` 的示例)。
FENCE_RE = re.compile(r"^(`{3,})(.*)$")

# ① 锚点文件:只有当「入口 / 配置 / 自动化」本身丢失时才应该失败。
ANCHORS = [
    # 根目录入口与项目配置
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "Makefile",
    "pyproject.toml",
    "Dockerfile",
    "docker-compose.yml",
    ".pre-commit-config.yaml",
    ".importlinter",
    # 自动化:CI 与 GitHub 集成
    ".github/workflows/harness-ci.yml",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",
    ".github/labeler.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    # harness 的契约与规则入口(schema 是「软约束转硬」的钩子)
    "harness/schemas/rule-schema.json",
    "harness/schemas/skill-schema.json",
    "harness/changes/_template/README.md",
    "harness/rules/_template.md",
    # 本门禁自身 + 状态机(最容易被改坏的三个脚本)
    "scripts/check_harness_docs.py",
    "scripts/check_pytest_report.py",
    "scripts/check-gates.sh",
    "tests/conftest.py",
]

# ② 受治理目录:(目录, glob, 最少文件数, 该目录是什么)
DIRECTORIES: list[tuple[str, str, int, str]] = [
    ("docs", "*.md", 15, "设计文档"),
    ("docs/adr", "*.md", 2, "ADR"),
    ("docs/tutorials", "*.md", 3, "教程"),
    ("harness/rules", "*.md", 15, "规则"),
    ("harness/agents", "*.md", 12, "Agent 角色"),
    ("harness/skills", "*/SKILL.md", 12, "Skill"),
    ("harness/templates", "*.md", 4, "模板"),
    ("harness/changes/_template", "*.md", 7, "变更七件套"),
    ("harness/pipeline", "*.md", 5, "流水线"),
    ("harness/metrics", "*.md", 4, "度量"),
    ("harness/iteration", "*.md", 2, "迭代"),
    ("harness/wiki", "*.md", 5, "知识库"),
    ("harness/sources", "README.md", 1, "来源池入口"),
    ("config", "*.yml", 3, "可观测性配置"),
    (".github/workflows", "*.yml", 6, "CI / 自动化 workflow"),
    (".github/ISSUE_TEMPLATE", "*.md", 2, "Issue 模板"),
    ("scripts", "*.py", 10, "检查脚本"),
    ("scripts", "*.sh", 3, "Shell 脚本"),
    ("tests", "*.py", 2, "测试"),
]

# ③ 形状校验的根:这些目录/根下的 .md 必须非空且以 H1 开头。
SHAPE_GLOBS = ["*.md", "docs/**/*.md", "harness/**/*.md"]

# 标题允许前导 banner,但不应离题太远。
H1_SEARCH_LINES = 10

PLACEHOLDER_SKIP = {
    "harness/rules/_template.md",
    "harness/skills/_template/SKILL.md",
    "harness/changes/_template/README.md",
}


def check_anchors(root: Path) -> list[str]:
    return [f"缺少锚点文件: {p}" for p in ANCHORS if not (root / p).is_file()]


def check_directories(root: Path) -> list[str]:
    errors: list[str] = []
    for rel, pattern, minimum, what in DIRECTORIES:
        directory = root / rel
        if not directory.is_dir():
            errors.append(f"缺少目录: {rel}({what})")
            continue
        found = len(list(directory.glob(pattern)))
        if found < minimum:
            errors.append(
                f"{rel} 下匹配 {pattern!r} 的文件只有 {found} 个,少于要求的 {minimum} 个({what})"
            )
    return errors


def check_shape(root: Path) -> list[str]:
    """受治理文档必须非空、且前若干行内出现 H1 标题(抓 0 字节孤儿 / 无标题文件)。

    允许标题前有少量导语 —— `README.md` 就是「7 行引用块 banner + 第 8 行 H1」。
    """
    errors: list[str] = []
    seen: set[Path] = set()
    for pattern in SHAPE_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            rel = path.relative_to(root)
            if path.stat().st_size == 0:
                errors.append(f"{rel}: 空文件(0 字节)")
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            head = text.splitlines()[:H1_SEARCH_LINES]
            if not any(ln.startswith("# ") for ln in head):
                errors.append(f"{rel}: 前 {H1_SEARCH_LINES} 行内没有 H1 标题")
    return errors


def check_fences(root: Path) -> list[str]:
    """代码围栏必须**配平**:每个 ``` 开块都有对应的闭块。

    反外审补充修正(2026-09-11)。实测发现 **6 个**文件的围栏数是奇数 —— 也就是
    「开了没关」:`FillWorkflow.md`(多一个收尾围栏)、`harness/agents/README.md`、
    `harness/audit/README.md`、`harness/changes/README.md`、
    `harness/checkpoints/README.md`、`docs/tutorials/first-requirement.md`。
    其中 `FillWorkflow.md` 与 `harness/agents/README.md` 还是
    `````markdown`` 里套 ```python`` 的写法 —— 围栏等长,内层直接把外层"闭掉",
    于是**后面整段内容渲染错位**。这和 H1(门禁脚本第一行是 markdown 围栏)是
    同一类病:**结构坏了,但没有任何机器在看它**。

    判定按 CommonMark 的语义:
      · 「等长或更长」且**带语言标记**的围栏出现在块内 → 这是"块内又开块",
        内层会直接把外层"闭掉"(例如 ```markdown 里写 ```python),后续内容全部错位;
      · 「等长或更长」且**裸**围栏 → 正常闭块;
      · **更短**的围栏 → 字面内容(合法)。所以正确写法是**外层用 4 个反引号**
        ````,里面就能安全地放 ``` 示例 —— 门禁必须接受这种写法。
    """
    errors: list[str] = []
    seen: set[Path] = set()
    for pattern in SHAPE_GLOBS:
        for path in sorted(root.glob(pattern)):
            if path in seen or not path.is_file():
                continue
            seen.add(path)
            rel = path.relative_to(root)
            open_len = 0
            opened_at = 0
            for number, line in enumerate(
                path.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                match = FENCE_RE.match(line)
                if match is None:
                    continue
                run, info = len(match.group(1)), match.group(2).strip()
                if open_len == 0:
                    open_len, opened_at = run, number
                    continue
                if run < open_len:
                    continue  # 比外层短 —— 字面内容,合法
                if info == "":
                    open_len = 0  # 正常闭块
                    continue
                errors.append(
                    f"{rel}:{number}: 在代码块内又开了新块(外层第 {opened_at} 行)"
                    f' —— 内层会把外层"闭掉",后面内容全部错位;'
                    f"若要在示例里展示 ``` 围栏,请把**外层**改成 4 个反引号 ````"
                )
                open_len = 0  # 容错:按"开了新的"继续扫描,尽量多报
                opened_at = number
            if open_len:
                errors.append(
                    f"{rel}: 第 {opened_at} 行的代码围栏没有闭合"
                    f"(若示例里含 ``` 围栏,请把外层改成 4 个反引号 ````)"
                )
    return errors


def check_placeholders(root: Path) -> list[str]:
    """核心文档不应有未填占位符(模板除外)。仅告警,不判失败。"""
    warnings: list[str] = []
    for rel in SHAPE_GLOBS:
        for path in sorted(root.glob(rel)):
            if not path.is_file():
                continue
            rel_str = str(path.relative_to(root))
            if rel_str in PLACEHOLDER_SKIP:
                continue
            content = path.read_text(encoding="utf-8", errors="replace")
            if "<待填>" in content and "填充指南" not in content:
                warnings.append(f"{rel_str}: 有未填占位符但无填充指南")
    return warnings


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="check_harness_docs")
    parser.add_argument("--root", default=".", help="仓库根目录(默认当前目录)")
    args = parser.parse_args(argv)

    root = Path(args.root).resolve()
    if not root.is_dir():
        print(f"::error::根目录不存在: {root}")
        return 2

    errors = check_anchors(root) + check_directories(root) + check_shape(root) + check_fences(root)
    if errors:
        print(f"Harness docs check FAILED ({len(errors)} 项):")
        for err in errors:
            print(f"  - {err}")
        return 1

    warnings = check_placeholders(root)
    for warning in warnings:
        print(f"  ⚠ {warning}")

    total_files = sum(len(list((root / d).glob(p))) for d, p, _, _ in DIRECTORIES)
    print(
        f"Harness docs check passed "
        f"({len(ANCHORS)} 个锚点, {len(DIRECTORIES)} 个目录规则, {total_files} 个受治理文件)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
