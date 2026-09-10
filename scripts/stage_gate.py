#!/usr/bin/env python3
"""stage_gate —— 阶段硬门 + 检查点(治"长任务中间全白费")。

反外审 H4/H5(2026-09-11,业务方批准)。原实现的两个病:

  · `scripts/state_tracker.py` **只写不校验** —— 直接 `data["stage"]=...` 再 append
    `history[]`,全仓没有任何代码读它;`docs/architecture.md:133`「十阶段不可跳过」
    因此只是**口号**,不是机制。
  · `scripts/check-gates.sh` **一次性检查全部产出物**,而且**不在任何链路里**
    (Makefile / CI / pre-commit 都没挂)→ 门禁只可能压在"最后一次提交",
    长任务中途断了/做错了 = **前面全白费,且没有任何门触发过**。

本工具把"阶段门"做成**真状态机**:
  · 每个阶段有 **evidence(产出物)** —— 必须真实存在且**非空**;
  · **迁移前必须校验**:所有前置阶段都 passed,且它们的 evidence **现在依然在**;
  · **不满足就拒绝进入下一阶段**(exit 1);
  · `resume` 告诉你"从第一个断点继续" → 中断后可续跑,不必重来;
  · `check` 只做产出物存在性校验(供 `check-gates.sh --stage N` 增量门使用)。

状态文件:`harness/state/<req>.json`(**入库** —— 换台机器也能续跑)。
阶段配置:`harness/state/stages.json`(十阶段,见 `harness/pipeline/stages.md`)。

用法:
    stage_gate.py init   --req <id> [--config <stages.json>]
    stage_gate.py enter  --req <id> --stage <name>     # 校验前置 → 进入该阶段(in_progress)
    stage_gate.py pass   --req <id>                    # 校验本阶段 evidence 存在 → 标记 passed
    stage_gate.py status --req <id>
    stage_gate.py resume --req <id>                    # 从哪继续
    stage_gate.py check  --req <id> [--upto <n>]       # 只校验产出物(不碰状态)

退出码:0 成功;1 门禁未过;2 用法/配置错误。
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(os.environ.get("HARNESS_ROOT") or Path(__file__).resolve().parents[1])
STATE_DIR = ROOT / "harness" / "state"
DEFAULT_CONFIG = STATE_DIR / "stages.json"


def _now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())


def _state_path(req: str) -> Path:
    return STATE_DIR / f"{req}.json"


def _resolve(rel: str, req: str) -> Path:
    """把配置里的相对路径(可含 {req})解析为绝对路径。"""
    return ROOT / rel.replace("{req}", req)


def _load(req: str) -> dict:
    path = _state_path(req)
    if not path.is_file():
        print(f"::error::状态文件不存在: {path}(先跑 init)")
        sys.exit(2)
    return json.loads(path.read_text(encoding="utf-8"))


def _save(req: str, state: dict) -> None:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state["updated_at"] = _now()
    _state_path(req).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def _stage_cfg(state: dict, name: str) -> dict | None:
    for stage in state["stages"]:
        if stage["name"] == name:
            return stage
    return None


def _missing_evidence(state: dict, stage: dict) -> list[str]:
    """产出物必须**存在且非空** —— 光"建了个空文件"不算交付。"""
    missing: list[str] = []
    for rel in stage.get("evidence", []):
        path = _resolve(rel, state["req"])
        if not path.is_file() or path.stat().st_size == 0:
            missing.append(rel.replace("{req}", state["req"]))
    return missing


def _passed(state: dict, name: str) -> bool:
    return any(h["stage"] == name and h["status"] == "passed" for h in state["history"])


# ── 命令 ────────────────────────────────────────────────────────────────────


def cmd_init(args: argparse.Namespace) -> int:
    config = Path(args.config) if args.config else DEFAULT_CONFIG
    if not config.is_file():
        print(f"::error::阶段配置不存在: {config}")
        return 2
    cfg = json.loads(config.read_text(encoding="utf-8"))
    if not cfg.get("stages"):
        print("::error::config 里没有 stages")
        return 2
    state = {
        "req": args.req,
        "stages": cfg["stages"],
        "current": None,
        "history": [],
        "created_at": _now(),
    }
    _save(args.req, state)
    print(f"✅ 已初始化 {args.req}:{len(state['stages'])} 个阶段 → {_state_path(args.req)}")
    return 0


def cmd_enter(args: argparse.Namespace) -> int:
    state = _load(args.req)
    names = [s["name"] for s in state["stages"]]
    if args.stage not in names:
        print(f"::error::未知阶段 {args.stage!r};可选 {names}")
        return 2
    index = names.index(args.stage)

    # 【核心】前置校验:所有更早的阶段必须 passed,且其 evidence **现在依然在**
    bad: list[str] = []
    for prev in names[:index]:
        if not _passed(state, prev):
            bad.append(f"阶段 {prev} 未通过")
            continue
        missing = _missing_evidence(state, _stage_cfg(state, prev))
        if missing:
            bad.append(f"阶段 {prev} 的产出物缺失/为空: {missing}")

    if bad:
        print(f"::error::不能进入阶段 {args.stage} —— 前置门禁未过:")
        for item in bad:
            print(f"::error::  - {item}")
        print(
            "::error::(阶段门必须在前一阶段【产出物真实存在】之后才放行;"
            "这正是『中间全白费』的第一个闸)"
        )
        return 1

    state["current"] = args.stage
    state["history"].append({"stage": args.stage, "status": "in_progress", "at": _now()})
    _save(args.req, state)
    print(f"✅ 已进入阶段 {args.stage}(前置 {index} 个阶段均已通过)")
    return 0


def cmd_pass(args: argparse.Namespace) -> int:
    state = _load(args.req)
    if not state.get("current"):
        print("::error::还没有进入任何阶段(先 enter)")
        return 2
    current = _stage_cfg(state, state["current"])
    missing = _missing_evidence(state, current)
    if missing:
        print(f"::error::阶段 {state['current']} 的产出物缺失/为空: {missing}")
        print("::error::产出物不存在 = 这一阶段没真正完成 → 不算通过")
        return 1
    for entry in reversed(state["history"]):
        if entry["stage"] == state["current"] and entry["status"] == "in_progress":
            entry["status"] = "passed"
            entry["passed_at"] = _now()
            break
    _save(args.req, state)
    print(f"✅ 阶段 {state['current']} 已通过(产出物齐备)")
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    state = _load(args.req)
    print(f"  req: {args.req} | current: {state.get('current')}")
    for stage in state["stages"]:
        status = "-"
        for entry in state["history"]:
            if entry["stage"] == stage["name"]:
                status = entry["status"]
        mark = {"passed": "✅", "in_progress": "▶", "-": "⬜"}.get(status, "?")
        missing = _missing_evidence(state, stage)
        note = f"  (产出物缺: {missing})" if missing else ""
        print(f"  {mark} {stage['name']:<12} {status}{note}")
    return 0


def cmd_resume(args: argparse.Namespace) -> int:
    """断点续跑:从**第一个「未通过 或 产出物已缺失」的阶段**继续。

    ⚠️ 必须**顺序走到第一个断点就停**,而不是取"最高的已通过阶段" ——
    否则某阶段的产出物事后被删/被改坏时,会**跳过它继续往前**(假装已完成)。
    这是参考实现的第一版真 bug,由其测试
    `test_removing_evidence_rolls_resume_back` 抓出。
    """
    state = _load(args.req)
    names = [s["name"] for s in state["stages"]]
    next_index = len(names)
    for index, name in enumerate(names):
        if not (_passed(state, name) and not _missing_evidence(state, _stage_cfg(state, name))):
            next_index = index
            break
    if next_index >= len(names):
        print(f"✅ {args.req}:所有阶段已通过且产出物齐备,无待续")
        return 0
    nxt = names[next_index]
    done = names[next_index - 1] if next_index > 0 else "(无)"
    print(f"▶ {args.req}:从阶段 {nxt} 继续(最后有效通过的阶段:{done})")
    print(f"  下一步:stage_gate.py enter --req {args.req} --stage {nxt}")
    return 0


def _load_for_check(req: str) -> dict:
    """`check` 不要求先 init —— 有状态文件就用它,否则直接用阶段配置。"""
    path = _state_path(req)
    if path.is_file():
        return json.loads(path.read_text(encoding="utf-8"))
    cfg = json.loads(DEFAULT_CONFIG.read_text(encoding="utf-8"))
    return {"req": req, "stages": cfg["stages"], "history": []}


def cmd_check(args: argparse.Namespace) -> int:
    """只校验产出物是否存在且非空 —— 供 `check-gates.sh --stage N` 增量门使用。"""
    state = _load_for_check(args.req)
    names = [s["name"] for s in state["stages"]]
    upto = args.upto if args.upto is not None else len(names)
    if upto < 1 or upto > len(names):
        print(f"::error::--upto 必须在 1..{len(names)} 之间,收到 {upto}")
        return 2

    missing: list[tuple[str, str]] = []
    for name in names[:upto]:
        for rel in _missing_evidence(state, _stage_cfg(state, name)):
            missing.append((name, rel))

    if missing:
        print(f"::error::{args.req} 阶段门未过(检查到阶段 {upto} {names[upto - 1]}):")
        for stage_name, rel in missing:
            print(f"::error::  - [{stage_name}] 缺失/为空: {rel}")
        return 1

    print(f"✅ 阶段门通过:{args.req}(阶段 1..{upto} 产出物齐备)")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="stage_gate")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init")
    p.add_argument("--req", required=True)
    p.add_argument("--config")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("enter")
    p.add_argument("--req", required=True)
    p.add_argument("--stage", required=True)
    p.set_defaults(func=cmd_enter)

    p = sub.add_parser("pass")
    p.add_argument("--req", required=True)
    p.set_defaults(func=cmd_pass)

    p = sub.add_parser("status")
    p.add_argument("--req", required=True)
    p.set_defaults(func=cmd_status)

    p = sub.add_parser("resume")
    p.add_argument("--req", required=True)
    p.set_defaults(func=cmd_resume)

    p = sub.add_parser("check")
    p.add_argument("--req", required=True)
    p.add_argument("--upto", type=int, default=None, help="只检查阶段 1..N(默认全部)")
    p.set_defaults(func=cmd_check)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
