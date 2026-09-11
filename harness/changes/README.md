# 变更索引

## 说明

每个需求一个独立目录:`harness/changes/REQ-XXXX/`。

## 目录模板

从 `harness/changes/_template/` 复制:

```bash
mkdir -p harness/changes/REQ-XXXX
cp harness/changes/_template/*.md harness/changes/REQ-XXXX/
```

> `_template/` 里**只有交付物本身**,所以 `cp *.md` 就是把七件套原样搬过去,
> 不会带进任何与需求无关的文件。
>
> (空跑-2 修正:此前模板目录里另有一份模板说明 `README.md`,`*.md` 会把它一并
> 复制进每个需求目录,成为噪音。现已把该说明并入本文件。)

### 必须文件

| 文件 | 对应阶段 |
| ---- | -------- |
| `requirement-analysis.md` | 1 需求分析 |
| `review-record-v1.md` | 2 需求评审 |
| `task-breakdown.md` | 3 计划评审 |
| `coding-report.md` | 4 编码实现 / 5 编码评审 |
| `unit-test-report.md` | 6 单测编写 / 7 单测评审 |
| `ci-result.md` | 8 CI 验证 |
| `deploy-validation.md` | 9 部署验证 |

### 阶段 10 的额外产出物

阶段 10「用户确认」的产出物**不在本目录**,而在 `harness/checkpoints/`:

```text
harness/checkpoints/<REQ>-HC5.md
```

模板见 `harness/checkpoints/_template.md`。**七件套齐备 ≠ 走完十阶段** ——
少了 HC-5 检查点记录,阶段 10 不会通过(实测:`stage_gate.py pass` 会报产出物缺失)。

### 评审版本

- v1、v2、v3 递增
- 旧版本不删

## 索引

| 需求编号 | 名称   | 状态   | 负责人   | 创建日期 | 链接                    |
| -------- | ------ | ------ | -------- | -------- | ----------------------- |
| REQ-0001 | <名称> | 待开始 | <负责人> | <日期>   | [REQ-0001](./REQ-0001/) |

## 状态定义(**需求级**)

> ⚠ 本仓有**两套**状态词表,粒度不同 —— 别混用:
>
> | | 需求级(**本表**) | 阶段级 |
> | --- | --- | --- |
> | 位置 | 上面「索引」表的状态列(给人看) | `harness/state/<REQ>.json` |
> | 词表 | 待开始 / 进行中 / 评审中 / CI 中 / 部署中 / 已完成 / 已回滚 | `in_progress` / `passed` |
> | 读写者 | 人(手工维护索引) | `scripts/stage_gate.py`(**机器**) |
>
> 两者的对应关系(需求级状态由阶段级状态**派生**,不反向约束):
>
> | 需求级 | 阶段级判据 |
> | --- | --- |
> | 待开始 | 没有任何阶段的 `passed` |
> | 进行中 / 评审中 | `current` 指向某阶段且为 `in_progress` |
> | CI 中 / 部署中 | `current` 为「CI 验证」/「部署验证」 |
> | 已完成 | 十阶段全部 `passed`(含 HC-5 交付确认) |
> | 已回滚 | 见 `harness/pipeline/rollback-process.md` |
>
> 十阶段名见 `harness/pipeline/stages.md`(权威),机器可读版本见 `harness/state/stages.json`。

- 待开始
- 进行中
- 评审中
- CI 中
- 部署中
- 已完成
- 已回滚

## 检查

```bash
# 增量门:每完成一个阶段就查一次,不必等最后
./scripts/check-gates.sh harness/changes/REQ-XXXX --stage 4

# 默认 = 阶段 1..9,即上面「必须文件」七件套齐备
./scripts/check-gates.sh harness/changes/REQ-XXXX

# 走完十阶段(含阶段 10 的 HC-5 检查点)
./scripts/check-gates.sh harness/changes/REQ-XXXX --stage 10
```

> 反外审 H5:阶段门原先**一次性查全部产出物**,且**不在 Makefile / CI / pre-commit
> 任何链路里** —— 于是它只可能压在"最后一次提交",长任务中途断了 = 前面全白费。
> 现在支持 `--stage <n>` 增量,并已挂进 `make gates` 与 CI。
> 原实现还**漏检 `review-record-v1.md`** —— 现已与上面的「必须文件」对齐。
