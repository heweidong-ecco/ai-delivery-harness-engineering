# 变更索引

## 说明

每个需求一个独立目录：`harness/changes/REQ-XXXX/`。

## 目录模板

从 `harness/changes/_template/` 复制。

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
./scripts/check-gates.sh harness/changes/REQ-XXXX
```
