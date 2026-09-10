# 状态目录

## 用途

跟踪需求当前状态 —— 这是「十阶段不可跳过」**真正被执行**的地方。

> 反外审 H4:原先 `scripts/state_tracker.py` **只写不校验**(直接写 `stage`/`status`
> 再 append `history`),全仓没有任何代码读它 —— 于是「十阶段不可跳过」只是**口号**。
> 现在阶段迁移由 `scripts/stage_gate.py` 做**前置校验**:
> 进入某阶段前,所有更早的阶段必须 passed,**且它们的产出物现在依然存在**。

## 文件

| 文件 | 说明 |
| ---- | ---- |
| `harness/state/stages.json` | **阶段门配置**:十阶段 → 各自的产出物(单一来源) |
| `harness/state/<REQ>.json` | 该需求的阶段状态(**入库**,换台机器也能续跑) |

## 状态文件格式

```json
{
  "req": "REQ-0001",
  "stages": [{ "name": "需求分析", "evidence": ["harness/changes/{req}/requirement-analysis.md"] }],
  "current": "编码实现",
  "updated_at": "2026-09-11T00:00:00Z",
  "created_at": "2026-09-11T00:00:00Z",
  "history": [
    { "stage": "需求分析", "status": "passed", "at": "...", "passed_at": "..." }
  ]
}
```

`status` 取值:`in_progress`(已进入)、`passed`(产出物齐备,已通过)。

## 命令

```bash
python scripts/stage_gate.py init   --req REQ-0001
python scripts/stage_gate.py enter  --req REQ-0001 --stage 编码实现   # 校验前置才放行
python scripts/stage_gate.py pass   --req REQ-0001                    # 校验产出物才通过
python scripts/stage_gate.py status --req REQ-0001
python scripts/stage_gate.py resume --req REQ-0001                    # 从第一个断点继续
python scripts/stage_gate.py check  --req REQ-0001 --upto 4           # 只查产出物(增量门)
```

也可以走 Makefile:

```bash
make state ARGS='enter --req REQ-0001 --stage 编码实现'
make gates REQ=REQ-0001 STAGE=4        # 增量阶段门(等价于 check-gates.sh --stage 4)
```

## 关于 `state_tracker.py`

`scripts/state_tracker.py` **已弃用**,保留为兼容转发层 ——
仍可按 `python scripts/state_tracker.py <REQ> <stage> <status>` 调用,
但它不再自己写状态,而是转发到 `stage_gate.py`(因此**再也不能绕过校验**)。
新代码请直接用 `stage_gate.py`。
