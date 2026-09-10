# Orchestrator Agent

## 目标

编排全部填充 Agent 按顺序执行，从来源池提取规则，填充 Harness。

## 输入

- `harness/sources/` 下所有来源
- `src/` 代码库
- CI 配置、Makefile、pyproject.toml

## 输出

- 每个 Agent 的输出文件
- 审核清单
- PR 描述

## 执行阶段

### 阶段 1：核心 6 个（必须）

| Agent       | 状态   | 分支                   | PR  | 审核 | 合并 |
| ----------- | ------ | ---------------------- | --- | ---- | ---- |
| 架构解析    | 待开始 | agent/architecture     |     |      |      |
| 事故反推    | 待开始 | agent/incident         |     |      |      |
| Review 提炼 | 待开始 | agent/review           |     |      |      |
| 代码考古    | 待开始 | agent/code-archaeology |     |      |      |
| 数据建模    | 待开始 | agent/data-modeling    |     |      |      |
| 门禁解析    | 待开始 | agent/gate             |     |      |      |

### 阶段 2：扩展 5 个（可选）

| Agent | 状态   | 分支              | PR  | 审核 | 合并 |
| ----- | ------ | ----------------- | --- | ---- | ---- |
| 安全  | 待开始 | agent/security    |     |      |      |
| 性能  | 待开始 | agent/performance |     |      |      |
| 重构  | 待开始 | agent/refactor    |     |      |      |
| 依赖  | 待开始 | agent/dependency  |     |      |      |
| 文档  | 待开始 | agent/doc         |     |      |      |

## 步骤

```text
1. 检查来源完整性
   ├── sources/architecture/ 非空
   ├── sources/incidents/ 非空
   ├── sources/reviews/ 非空
   ├── sources/ddl/ 非空
   ├── sources/api/ 非空
   └── sources/flows/ 非空
2. 按顺序触发阶段 1 的 Agent
3. 每个 Agent 独立分支、独立 PR
4. 人工审核
5. 合并
6. 阶段 1 完成后，可选阶段 2
7. 全部完成后，跑 make gate
8. 记录到 patch-log.md
```

## 来源完整性检查

| 来源          | 必需   | 检查        |
| ------------- | ------ | ----------- |
| incidents/    | 是     | 至少 1 份   |
| reviews/      | 是     | 至少 10 份  |
| architecture/ | 是     | 至少 1 份   |
| ddl/          | 视项目 | 有则用      |
| api/          | 视项目 | 有则用      |
| flows/        | 视项目 | 有则用      |
| code/         | 否     | 直接用 src/ |

来源为空则拒绝启动。

## 硬性约束

- 不允许跳过阶段 1 任何 Agent。
- 不允许跳过人工审核。
- 每个 Agent 独立分支、独立 PR。
- 来源为空则拒绝。
- 阶段 2 可跳过，但阶段 1 必须完成。
- Agent 输出必须可追溯。
- 合并前必须跑 `make gate`。

## 失败处理

| 失败             | 处理             |
| ---------------- | ---------------- |
| 来源不完整       | 停止，请求补充   |
| Agent 输出无来源 | 拒绝，打回重做   |
| 检查脚本跑不通   | 拒绝，打回重做   |
| P0 规则无测试    | 拒绝，打回重做   |
| 人工审核不通过   | 打回 Agent 重做  |
| CI 失败          | 回退，修复后重提 |

## 输出报告
