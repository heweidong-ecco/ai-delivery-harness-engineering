#!/usr/bin/env python3
"""state_tracker —— **已弃用**;保留为 `stage_gate` 的兼容转发层。

反外审 H4(2026-09-11):本脚本原先只做
`data["stage"] = stage; data["status"] = status; data["history"].append(...)`,
**没有任何前置校验**,且全仓没有任何代码读它 —— 于是
`docs/architecture.md:133`「十阶段不可跳过」只是**口号**,不是机制。
"建个空文件糊弄过去""直接跳到第 8 阶段"都拦不住。

现在真正的状态机是 `scripts/stage_gate.py`(进入阶段前校验前置阶段全部 passed
**且产出物现在依然存在**;`resume` 从第一个断点续跑)。
本文件只把**旧命令**翻译过去,不再自己写状态 —— 这样文档里已有的
`python scripts/state_tracker.py <REQ> <stage> <status>` 仍然可用,
但**再也不能绕过校验**。

旧 → 新 映射:
    state_tracker.py REQ-0001 coding in_progress  →  stage_gate.py enter --stage coding
    state_tracker.py REQ-0001 coding passed       →  stage_gate.py enter --stage coding && pass

退出码:同 stage_gate(0 成功;1 门禁未过;2 用法/配置错误)。
新代码请直接用:`python scripts/stage_gate.py --help`
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from types import ModuleType

_STAGE_GATE = Path(__file__).resolve().parent / "stage_gate.py"

PASSED_STATUSES = {"passed", "pass", "done", "success", "succeeded"}
ENTER_STATUSES = {"in_progress", "doing", "started", "active"}


def _load_stage_gate() -> ModuleType:
    spec = importlib.util.spec_from_file_location("_stage_gate", _STAGE_GATE)
    if spec is None or spec.loader is None:
        raise SystemExit(f"无法加载 {_STAGE_GATE}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run(gate: ModuleType, argv: list[str]) -> int:
    try:
        return gate.main(argv)
    except SystemExit as exc:  # stage_gate 用 SystemExit 表达错误码
        return int(exc.code or 0)


def main() -> int:
    if len(sys.argv) < 4:
        print("Usage: state_tracker.py <REQ> <stage> <status>")
        print(
            "  ⚠ 已弃用 —— 推荐直接用:"
            " python scripts/stage_gate.py enter --req <REQ> --stage <stage>"
        )
        return 2

    req, stage, status = sys.argv[1], sys.argv[2], sys.argv[3]
    print(
        f"⚠ state_tracker.py 已弃用(反外审 H4):转发到 stage_gate.py"
        f"(不再跳过前置校验)。新写法:"
        f" python scripts/stage_gate.py enter --req {req} --stage {stage}"
    )

    gate = _load_stage_gate()

    # 旧脚本会自动创建状态文件;这里保持同样的手感,先 init 一次(已存在则覆盖也无妨)。
    if not (Path(gate.ROOT) / "harness" / "state" / f"{req}.json").is_file():
        code = _run(gate, ["init", "--req", req])
        if code != 0:
            return code

    code = _run(gate, ["enter", "--req", req, "--stage", stage])
    if code != 0:
        return code

    if status in PASSED_STATUSES:
        return _run(gate, ["pass", "--req", req])

    if status not in ENTER_STATUSES:
        print(
            f"::error::未知状态 {status!r};可用:{sorted(ENTER_STATUSES | PASSED_STATUSES)}",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
