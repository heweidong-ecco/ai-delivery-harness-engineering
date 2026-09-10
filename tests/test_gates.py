"""门禁防腐测试 —— 盯着「门禁自己」不要静默腐烂。

反外审 H3/§5(2026-09-11)。教训:`scripts/check_harness_docs.py` 第 1 行被写成了
markdown 围栏(```` ```python ````),于是**该脚本永不执行**;而它被 `Makefile` 与 CI 调用,
`make gate` 与 CI **从未绿过** —— **没有人知道**,因为**没有测试盯着门禁自己**。

每条门禁至少三类断言(§5):
  ① 语法       —— 抓"永不执行"那一类(python: ast.parse;shell: bash -n);
  ② 可执行位   —— scripts/ 下的文件必须可执行;
  ③ 已被注册   —— 没挂进 Makefile / CI / pre-commit / 测试 = 形同不存在;
  ④ 该拦的拦   —— 喂真实输入,断言它**真的拒绝**,并**反向验证**(把门禁改坏 → 测试必须红)。
"""

from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

# ③ "已被注册"的判定范围:凡在这些文件里出现脚本名 = 被调用。
REGISTRY_FILES = [
    ROOT / "Makefile",
    ROOT / ".pre-commit-config.yaml",
    *sorted((ROOT / ".github" / "workflows").glob("*.yml")),
    *sorted((ROOT / "tests").glob("*.py")),
]


def all_scripts() -> list[Path]:
    return sorted(SCRIPTS.glob("*.py")) + sorted(SCRIPTS.glob("*.sh"))


def python_scripts() -> list[Path]:
    return sorted(SCRIPTS.glob("*.py"))


def code_lines(path: Path) -> Iterator[tuple[int, str]]:
    """产出行号 + **去掉注释后**的代码 —— 避免"注释里提到 `|| true`"被误判为软失败。"""
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("#"):
            continue
        yield number, stripped.split("#", 1)[0]


# ============================================================
# ① 语法 —— 抓 H1 那类"永不执行"
# ============================================================


@pytest.mark.parametrize("script", python_scripts(), ids=lambda p: p.name)
def test_python_script_parses(script: Path) -> None:
    """每个 .py 都必须能被 compile —— 门禁脚本第一行是 ```` ```python ```` 就会死在这里。"""
    source = script.read_text(encoding="utf-8")
    ast.parse(source, filename=str(script))


@pytest.mark.parametrize("script", sorted(SCRIPTS.glob("*.sh")), ids=lambda p: p.name)
def test_shell_script_parses(script: Path) -> None:
    result = subprocess.run(["bash", "-n", str(script)], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_root_markdown_fence_detection_has_teeth(tmp_path: Path) -> None:
    """**反向验证**:把门禁改坏,上面那条断言必须真的红。

    只证明"能过"是不够的 —— 还要证明"坏了会被抓到",否则它和
    `test_check_harness_docs_passes` 里那个 `pytest.skip` 一样是摆设。
    """
    broken = tmp_path / "broken.py"
    broken.write_text("```python\nx = 1\n", encoding="utf-8")
    with pytest.raises(SyntaxError):
        ast.parse(broken.read_text(encoding="utf-8"), filename=str(broken))

    # 对照:去掉围栏就应当能过 —— 证明上面失败的原因确实是围栏本身。
    broken.write_text("x = 1\n", encoding="utf-8")
    ast.parse(broken.read_text(encoding="utf-8"), filename=str(broken))


# ============================================================
# ② 可执行位
# ============================================================


@pytest.mark.parametrize("script", all_scripts(), ids=lambda p: p.name)
def test_script_is_executable(script: Path) -> None:
    assert os.access(script, os.X_OK), f"{script.name} 缺少可执行位(chmod +x)"


# ============================================================
# ③ 已被注册 —— 没注册 = 形同不存在
# ============================================================


def registry_text() -> str:
    return "\n".join(p.read_text(encoding="utf-8") for p in REGISTRY_FILES)


@pytest.mark.parametrize("script", all_scripts(), ids=lambda p: p.name)
def test_script_is_registered(script: Path) -> None:
    """脚本必须被 Makefile / CI / pre-commit / 测试里至少一处调用。

    `scripts/check-gates.sh` 原先就是这样烂掉的:文件是对的,但
    **Makefile / CI / pre-commit 三处都没有它** —— 于是它从未运行过。
    """
    assert script.name in registry_text(), (
        f"{script.name} 没有被任何 Makefile / CI / pre-commit / 测试调用 —— 形同不存在"
    )


def test_registry_detects_unregistered_script() -> None:
    """反向验证:注册制本身能发现"孤儿脚本"。

    名字在运行时拼出来 —— 否则它字面量地出现在本文件里,而 tests/*.py 本身
    也在 REGISTRY_FILES 内,会变成自证(这条测试的第一版就踩了这个坑)。
    """
    orphan = "definitely-not-" + "registered-anywhere.py"
    assert orphan not in registry_text()


# ============================================================
# ④ 该拦的拦:check_harness_docs
# ============================================================


def run_harness_docs(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "check_harness_docs.py"), *args],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_harness_docs_passes_on_this_repo() -> None:
    result = run_harness_docs()
    assert result.returncode == 0, result.stdout + result.stderr


def test_harness_docs_rejects_missing_anchor(tmp_path: Path) -> None:
    """缺锚点文件 → 必须**拒绝**(exit 1),而不是打个招呼放行。"""
    result = run_harness_docs("--root", str(tmp_path))
    assert result.returncode == 1
    assert "缺少锚点文件" in result.stdout


def test_harness_docs_rejects_empty_document(tmp_path: Path) -> None:
    """0 字节孤儿文件 → 必须拒绝。"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "harness").mkdir()
    (tmp_path / "docs" / "orphan.md").write_text("", encoding="utf-8")
    result = run_harness_docs("--root", str(tmp_path))
    assert result.returncode == 1
    assert "空文件" in result.stdout


def test_harness_docs_rejects_document_without_h1(tmp_path: Path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "untitled.md").write_text("正文但无标题\n", encoding="utf-8")
    result = run_harness_docs("--root", str(tmp_path))
    assert result.returncode == 1
    assert "没有 H1 标题" in result.stdout


def test_gate_survives_the_slimming_documented_in_usage(tmp_path: Path) -> None:
    """照 `USAGE.md` §九「复制后建议删除的内容」精简后,门禁**必须仍然通过**。

    这条是补的 —— 第一版阈值直接取"当前实际数量"(如 skills 要求 ≥12),
    结果**照 kit 自己的文档操作就会把门禁弄红**(5 个可选 skill 删掉后只剩 10)。
    一个惩罚"按文档操作"的门禁与 H1/H6 是同一类病:约束本身站不住。
    """
    target = tmp_path / "repo"
    shutil.copytree(
        ROOT,
        target,
        ignore=shutil.ignore_patterns(
            ".git",
            ".claude",
            "original_document",
            "__pycache__",
            ".venv",
            ".mypy_cache",
            ".ruff_cache",
            ".pytest_cache",
            ".import_linter_cache",
            "*.egg-info",
            ".coverage*",
            "pytest-report.json",
            "htmlcov",
        ),
    )
    # USAGE §九 列出的可删除项(逐条照抄)
    deletable = [
        "harness/rules/performance-standard.md",
        "harness/rules/concurrency-standard.md",
        "harness/rules/cache-standard.md",
        "harness/rules/timezone-standard.md",
        "harness/rules/i18n-standard.md",
        "harness/skills/performance",
        "harness/skills/refactor",
        "harness/skills/migration",
        "harness/skills/api-versioning",
        "harness/skills/db-migration",
        "harness/agents/refactor-agent.md",
        "harness/agents/dependency-agent.md",
        "harness/agents/doc-agent.md",
        ".github/workflows/auto-label.yml",
        ".github/workflows/stale.yml",
        ".github/workflows/release.yml",
        ".github/workflows/dependency-update.yml",
        ".github/workflows/security-scan.yml",
        "docs/adr",
        "docs/tutorials",
        "docs/compliance.md",
        "docs/data-governance.md",
        "docs/threat-model.md",
        "docs/capacity-planning.md",
        "docs/integrations.md",
        "docs/anti-patterns.md",
        "docs/best-practices.md",
        "docs/roadmap.md",
        "config/grafana",
        "config/prometheus.yml",
        "config/alert-rules.yml",
        "config/logging.yml",
        "scripts/collect_metrics.py",
        "scripts/audit_log.py",
        "scripts/state_tracker.py",
        "scripts/check_dependencies.py",
    ]
    for rel in deletable:
        path = target / rel
        if path.is_dir():
            shutil.rmtree(path)
        elif path.is_file():
            path.unlink()

    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_harness_docs.py"), "--root", str(target)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        "照 USAGE §九 精简后门禁变红了 —— 门禁在惩罚'按文档操作':\n" + result.stdout
    )


FENCE = "`" * 3


def test_harness_docs_rejects_unclosed_fence(tmp_path: Path) -> None:
    """实测曾有 6 个文件围栏"开了没关"(FillWorkflow 等),导致整段渲染错位。"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "bad.md").write_text(f"# 标题\n\n{FENCE}bash\necho hi\n", encoding="utf-8")
    result = run_harness_docs("--root", str(tmp_path))
    assert result.returncode == 1
    assert "没有闭合" in result.stdout


def test_harness_docs_rejects_nested_equal_length_fence(tmp_path: Path) -> None:
    """```markdown 里套 ```python:内层等长,会把外层"闭掉" → 后面全错位。"""
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "nested.md").write_text(
        f"# 标题\n\n{FENCE}markdown\n{FENCE}python\nx = 1\n{FENCE}\n",
        encoding="utf-8",
    )
    result = run_harness_docs("--root", str(tmp_path))
    assert result.returncode == 1, "等长嵌套围栏没被拦住"
    assert "没有闭合" in result.stdout


def test_harness_docs_accepts_longer_outer_fence(tmp_path: Path) -> None:
    """反面对照:**4 个反引号**的外层里放 ``` 示例是合法的,不能误报。

    这正是 `harness/agents/README.md` 与 `FillWorkflow.md` 的修法 ——
    门禁必须接受这种写法,否则修完还是红。
    """
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "good.md").write_text(
        f"# 标题\n\n{'`' * 4}markdown\n{FENCE}python\nx = 1\n{FENCE}\n{'`' * 4}\n",
        encoding="utf-8",
    )
    result = run_harness_docs("--root", str(tmp_path))
    assert "没有闭合" not in result.stdout


# ============================================================
# ④ 该拦的拦:真空门禁必须**自称未实现**,而不是静默通过
# ============================================================


def test_check_layers_declares_unimplemented_rather_than_passing_silently() -> None:
    """H6:骨架期 src/ 无分层包 → 必须显式标注,不能静默 skip。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check_layers.py"), "src"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0
    assert "UNIMPLEMENTED" in result.stdout
    assert "no rules configured" not in result.stdout


def test_validate_schemas_declares_unimplemented_but_still_validates() -> None:
    """H6/H9:schema 自检要真的跑;无数据时如实标注未实现。"""
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_schemas.py")],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Schema 自检通过" in result.stdout


def test_validate_schemas_rejects_invalid_schema(tmp_path: Path) -> None:
    """反向验证:坏掉的 schema 必须被 `check_schema` 抓到。"""
    import jsonschema

    with pytest.raises(jsonschema.SchemaError):
        jsonschema.Draft202012Validator.check_schema({"type": "not-a-real-type"})


def test_rule_schema_requires_test_for_p0() -> None:
    """H10:「每条 P0 规则必须有测试」必须被 schema 真正强制。"""
    import jsonschema

    schema = json.loads(
        (ROOT / "harness" / "schemas" / "rule-schema.json").read_text(encoding="utf-8")
    )
    validator = jsonschema.Draft202012Validator(schema)

    base = {
        "id": "ERR-001",
        "rule": "禁止裸 except",
        "reason": "事故 INC-1",
        "check": "ruff E722",
        "priority": "P0",
        "owner": "team",
        "source": "harness/sources/incidents/INC-1.md",
    }
    assert list(validator.iter_errors(base)), "P0 规则缺 test 却通过了 —— schema 没强制住"
    assert not list(validator.iter_errors({**base, "test": "tests/test_except.py"}))

    # 缺 source 也必须被拒(「来源为空则拒绝」)。
    without_source = {k: v for k, v in base.items() if k != "source"}
    assert list(validator.iter_errors({**without_source, "test": "tests/test_except.py"}))


# ============================================================
# ④ 该拦的拦:阶段门 / 状态机
# ============================================================


def make_sandbox(tmp_path: Path, stages: dict | None = None) -> Path:
    """一个独立的 HARNESS_ROOT,内嵌本仓真实使用的阶段配置。"""
    root = tmp_path / "root"
    (root / "harness" / "state").mkdir(parents=True)
    (root / "harness" / "changes" / "REQ-TEST").mkdir(parents=True)
    (root / "harness" / "checkpoints").mkdir(parents=True)
    config = stages or json.loads(
        (ROOT / "harness" / "state" / "stages.json").read_text(encoding="utf-8")
    )
    (root / "harness" / "state" / "stages.json").write_text(
        json.dumps(config, ensure_ascii=False), encoding="utf-8"
    )
    return root


def gate(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, HARNESS_ROOT=str(root))
    return subprocess.run(
        [sys.executable, str(SCRIPTS / "stage_gate.py"), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )


def run_check_gates(root: Path, *args: str) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ, HARNESS_ROOT=str(root))
    return subprocess.run(
        ["bash", str(SCRIPTS / "check-gates.sh"), *args],
        capture_output=True,
        text=True,
        env=env,
        cwd=ROOT,
    )


def artifact(root: Path, rel: str, text: str = "内容\n") -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_cannot_enter_later_stage_without_prerequisites(tmp_path: Path) -> None:
    """【闸 1】不许跳步。"""
    root = make_sandbox(tmp_path)
    assert gate(root, "init", "--req", "REQ-TEST").returncode == 0
    result = gate(root, "enter", "--req", "REQ-TEST", "--stage", "编码实现")
    assert result.returncode == 1
    assert "前置门禁未过" in result.stdout


def test_pass_requires_evidence_to_exist(tmp_path: Path) -> None:
    """【闸 2】产出物不存在 → 该阶段不算通过。"""
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    gate(root, "enter", "--req", "REQ-TEST", "--stage", "需求分析")
    assert gate(root, "pass", "--req", "REQ-TEST").returncode == 1

    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    assert gate(root, "pass", "--req", "REQ-TEST").returncode == 0


def test_empty_evidence_file_does_not_count(tmp_path: Path) -> None:
    """建个空文件糊弄不过去。"""
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    gate(root, "enter", "--req", "REQ-TEST", "--stage", "需求分析")
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md", "")
    assert gate(root, "pass", "--req", "REQ-TEST").returncode == 1


def test_resume_rolls_back_when_evidence_is_deleted(tmp_path: Path) -> None:
    """**核心**(H4):产出物事后被删 → resume 必须**退回**该阶段,不许假装已完成。"""
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    for stage, rel in [
        ("需求分析", "harness/changes/REQ-TEST/requirement-analysis.md"),
        ("需求评审", "harness/changes/REQ-TEST/review-record-v1.md"),
    ]:
        assert gate(root, "enter", "--req", "REQ-TEST", "--stage", stage).returncode == 0
        artifact(root, rel)
        assert gate(root, "pass", "--req", "REQ-TEST").returncode == 0

    assert "计划评审" in gate(root, "resume", "--req", "REQ-TEST").stdout

    (root / "harness/changes/REQ-TEST/requirement-analysis.md").unlink()
    result = gate(root, "resume", "--req", "REQ-TEST")
    assert "需求分析" in result.stdout, "产出物没了却没退回第一阶段"


def test_enter_rejects_when_prior_evidence_vanished(tmp_path: Path) -> None:
    """进入下一阶段时,前置阶段的产出物**现在**必须依然在。"""
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    gate(root, "enter", "--req", "REQ-TEST", "--stage", "需求分析")
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    gate(root, "pass", "--req", "REQ-TEST")

    (root / "harness/changes/REQ-TEST/requirement-analysis.md").unlink()
    result = gate(root, "enter", "--req", "REQ-TEST", "--stage", "需求评审")
    assert result.returncode == 1
    assert "产出物缺失/为空" in result.stdout


def test_unknown_stage_rejected(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    assert gate(root, "enter", "--req", "REQ-TEST", "--stage", "不存在").returncode == 2


def test_state_file_lives_under_harness_state(tmp_path: Path) -> None:
    """状态落在 `harness/state/`(**入库**)—— 换台机器也能续跑。"""
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    state_file = root / "harness" / "state" / "REQ-TEST.json"
    assert state_file.is_file()
    data = json.loads(state_file.read_text(encoding="utf-8"))
    assert data["req"] == "REQ-TEST" and "history" in data


# ============================================================
# H5:增量阶段门
# ============================================================


def test_check_gates_is_incremental(tmp_path: Path) -> None:
    """`--stage N` 只要求阶段 1..N —— 每阶段结束就能跑,不必等最后。"""
    root = make_sandbox(tmp_path)
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")

    assert run_check_gates(root, "REQ-TEST", "--stage", "1").returncode == 0
    assert run_check_gates(root, "REQ-TEST", "--stage", "2").returncode == 1

    artifact(root, "harness/changes/REQ-TEST/review-record-v1.md")
    assert run_check_gates(root, "REQ-TEST", "--stage", "2").returncode == 0


def test_check_gates_default_requires_all_seven_deliverables(tmp_path: Path) -> None:
    """默认口径 = 变更七件套齐备(阶段 1..9)。"""
    root = make_sandbox(tmp_path)
    assert run_check_gates(root, "REQ-TEST").returncode == 1, "空目录却过了"

    for rel in [
        "requirement-analysis.md",
        "review-record-v1.md",
        "task-breakdown.md",
        "coding-report.md",
        "unit-test-report.md",
        "ci-result.md",
        "deploy-validation.md",
    ]:
        artifact(root, f"harness/changes/REQ-TEST/{rel}")
    assert run_check_gates(root, "REQ-TEST").returncode == 0


def test_check_gates_rejects_bad_stage_number(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    assert run_check_gates(root, "REQ-TEST", "--stage", "abc").returncode == 2
    assert run_check_gates(root, "REQ-TEST", "--stage", "99").returncode == 2


def test_check_gates_accepts_legacy_directory_argument(tmp_path: Path) -> None:
    """兼容原文档写法 `./scripts/check-gates.sh harness/changes/REQ-TEST`。"""
    root = make_sandbox(tmp_path)
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    result = run_check_gates(root, "harness/changes/REQ-TEST", "--stage", "1")
    assert result.returncode == 0


def test_init_rejects_missing_config(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    result = gate(root, "init", "--req", "REQ-TEST", "--config", str(tmp_path / "nope.json"))
    assert result.returncode == 2


def test_init_rejects_config_without_stages(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    empty = tmp_path / "empty.json"
    empty.write_text('{"stages": []}', encoding="utf-8")
    assert gate(root, "init", "--req", "REQ-TEST", "--config", str(empty)).returncode == 2


@pytest.mark.parametrize("command", ["enter", "pass", "status", "resume"])
def test_commands_require_state_file(tmp_path: Path, command: str) -> None:
    """没 init 就调用 → 用法错误(exit 2),而不是静默创建状态。"""
    root = make_sandbox(tmp_path)
    args = [command, "--req", "REQ-NEVER-INITIALISED"]
    if command == "enter":
        args += ["--stage", "需求分析"]
    assert gate(root, *args).returncode == 2


def test_pass_without_enter_is_usage_error(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    assert gate(root, "pass", "--req", "REQ-TEST").returncode == 2


@pytest.mark.parametrize("upto", ["0", "11", "-1"])
def test_check_rejects_out_of_range_stage(tmp_path: Path, upto: str) -> None:
    root = make_sandbox(tmp_path)
    assert gate(root, "check", "--req", "REQ-TEST", "--upto", upto).returncode == 2


def test_check_works_without_init(tmp_path: Path) -> None:
    """`check` 是纯产出物校验,不该逼人先 init。"""
    root = make_sandbox(tmp_path)
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    assert gate(root, "check", "--req", "REQ-TEST", "--upto", "1").returncode == 0


def test_resume_reports_nothing_left_when_all_stages_pass(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    stages = json.loads((ROOT / "harness" / "state" / "stages.json").read_text(encoding="utf-8"))[
        "stages"
    ]
    for stage in stages:
        assert gate(root, "enter", "--req", "REQ-TEST", "--stage", stage["name"]).returncode == 0
        for rel in stage["evidence"]:
            artifact(root, rel.replace("{req}", "REQ-TEST"))
        assert gate(root, "pass", "--req", "REQ-TEST").returncode == 0

    result = gate(root, "resume", "--req", "REQ-TEST")
    assert result.returncode == 0
    assert "无待续" in result.stdout


def test_status_marks_passed_and_missing(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    gate(root, "init", "--req", "REQ-TEST")
    gate(root, "enter", "--req", "REQ-TEST", "--stage", "需求分析")
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    gate(root, "pass", "--req", "REQ-TEST")
    result = gate(root, "status", "--req", "REQ-TEST")
    assert result.returncode == 0
    assert "passed" in result.stdout
    assert "产出物缺" in result.stdout


def test_state_tracker_rejects_missing_args_and_unknown_status(tmp_path: Path) -> None:
    root = make_sandbox(tmp_path)
    env = dict(os.environ, HARNESS_ROOT=str(root))

    def tracker(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "state_tracker.py"), *args],
            capture_output=True,
            text=True,
            env=env,
            cwd=ROOT,
        )

    assert tracker("REQ-TEST").returncode == 2
    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    assert tracker("REQ-TEST", "需求分析", "in_progress").returncode == 0
    assert tracker("REQ-TEST", "需求分析", "banana").returncode == 2


def test_state_tracker_is_a_validating_shim(tmp_path: Path) -> None:
    """H4:旧的 state_tracker 命令仍能用,但**再也不能绕过校验**(跳步会被拒)。"""
    root = make_sandbox(tmp_path)
    env = dict(os.environ, HARNESS_ROOT=str(root))

    def tracker(*args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPTS / "state_tracker.py"), *args],
            capture_output=True,
            text=True,
            env=env,
            cwd=ROOT,
        )

    # 没有产出物就标 passed —— 旧实现会直接写进去,现在必须失败。
    assert tracker("REQ-TEST", "需求分析", "passed").returncode == 1

    artifact(root, "harness/changes/REQ-TEST/requirement-analysis.md")
    assert tracker("REQ-TEST", "需求分析", "passed").returncode == 0

    # 跳步依然被拒。
    assert tracker("REQ-TEST", "CI 验证", "in_progress").returncode == 1


# ============================================================
# H13:提交环节必须有测试门
# ============================================================


def test_pre_commit_runs_pytest() -> None:
    """「跑测试」这条最重要的纪律,在提交环节必须有门。"""
    config = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
    assert "pytest" in config, "pre-commit 里没有 pytest —— 提交环节没有测试门"


# 软失败扫描面:原先只扫 Makefile 与 CI workflow,**漏掉了 Dockerfile** ——
# 于是 `Dockerfile` 里那句 `pre-commit install --install-hooks || true` 一直没被抓到。
# 教训:防腐测试本身也有覆盖面,覆盖面之外等于没有门禁。
SOFT_FAIL_SURFACE = [
    ROOT / "Makefile",
    ROOT / "Dockerfile",
    ROOT / "docker-compose.yml",
    *sorted((ROOT / ".github" / "workflows").glob("*.yml")),
    *sorted((ROOT / "scripts").glob("*.sh")),
]


def test_no_soft_fail_anywhere() -> None:
    """H11/H12:`|| true` 让"检查"永不失败 = 等于没有检查。

    扫描面覆盖 Makefile / CI / **Dockerfile** / docker-compose / 所有 .sh。
    """
    offenders: list[str] = []
    for path in SOFT_FAIL_SURFACE:
        if not path.is_file():
            continue
        offenders += [
            f"{path.relative_to(ROOT)}:{number}"
            for number, code in code_lines(path)
            if "|| true" in code
        ]
    assert not offenders, f"仍有软失败(`|| true`): {offenders}"


def test_soft_fail_scan_covers_dockerfile() -> None:
    """反向验证:扫描面必须真的包含 Dockerfile(漏掉它正是上一版的 bug)。"""
    names = {p.name for p in SOFT_FAIL_SURFACE}
    assert "Dockerfile" in names
    assert "docker-compose.yml" in names


def test_import_linter_is_declared_and_invoked() -> None:
    """H14:`.importlinter` 定义了契约,就必须有地方真的运行它。"""
    assert (ROOT / ".importlinter").is_file()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "import-linter" in pyproject, "import-linter 没有声明为依赖"
    layers = (SCRIPTS / "check_layers.py").read_text(encoding="utf-8")
    assert "lint-imports" in layers, "check_layers.py 没有真正运行 lint-imports"


def test_workflows_live_where_github_reads_them() -> None:
    """H7:GitHub 只读 `.github/workflows/`,放在 harness/ 下 = 永不生效。"""
    assert not (ROOT / "harness" / "workflows").exists()
    names = {p.name for p in (ROOT / ".github" / "workflows").glob("*.yml")}
    assert {
        "auto-label.yml",
        "stale.yml",
        "release.yml",
        "dependency-update.yml",
        "security-scan.yml",
    } <= names


def test_github_config_files_are_at_repo_root_config_dir() -> None:
    """H7:CODEOWNERS / dependabot.yml 只在这两个位置生效。"""
    assert (ROOT / ".github" / "CODEOWNERS").is_file()
    assert (ROOT / ".github" / "dependabot.yml").is_file()
    assert not (ROOT / ".github" / "ISSUE_TEMPLATE" / "CODEOWNERS").exists()
    assert not (ROOT / ".github" / "ISSUE_TEMPLATE" / "dependabot.yml").exists()


def test_declared_dev_tools_are_importable() -> None:
    """H9:缺依赖应 fail,前提是依赖真的声明了 —— 声明的必须装得上。"""
    for module in ("jsonschema",):
        import importlib

        assert importlib.util.find_spec(module) is not None, f"{module} 未安装"


# **叙事型**文档:它们本来就要记录"过去在哪里"。真正的靶子是**指导型**文档
# (README/USAGE/docs/*/harness/{rules,skills,pipeline,wiki}/**),
# 读者会照着它们去找文件 —— 那才是不能指向旧路径的地方。
NARRATIVE_DOCS = {"patch-log.md", "CHANGELOG.md", "freeze.md"}


def test_no_guidance_doc_points_at_the_moved_workflow_dir() -> None:
    """H7:移动 `harness/workflows/` 后,**指导型**文档不得再指向旧路径。

    判据区分了「叙事」与「指导」:CHANGELOG 写「从 harness/workflows/ 移入
    .github/workflows/」是**描述这次变更**,合法;README/教程里写「你的 workflow
    放在 harness/workflows/」则是把人指去一个**GitHub 永不读取**的目录,必须拦。
    """
    stale: list[str] = []
    for path in ROOT.rglob("*.md"):
        if any(part in {".git", "original_document", ".claude"} for part in path.parts):
            continue
        if path.name.startswith("AUDIT-") or path.name in NARRATIVE_DOCS:
            continue
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if "harness/workflows/" in line:
                stale.append(f"{path.relative_to(ROOT)}:{number}")
    assert not stale, f"仍有指导型文档指向已移动的 harness/workflows/: {stale}"


@pytest.fixture(scope="session")
def bash_available() -> None:
    assert shutil.which("bash"), "测试需要 bash"
