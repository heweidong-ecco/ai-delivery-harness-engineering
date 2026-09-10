# Task Breakdown Skill

## 目标

把需求拆成可执行任务。

## 触发条件

需求分析完成。

## 输入

requirement-analysis.md

## 步骤

1. 按分层拆任务。
2. 标依赖。
3. 标产出。
4. 标负责人。
5. 标预估。
6. 找关键路径。

## 输出

harness/changes/REQ-XXXX/task-breakdown.md

## 质量门禁

- 每个任务有层
- 每个任务有产出
- 依赖无环
- 关键路径明确
- 风险已标

## 失败回退

- 依赖有环：重新拆
- 任务过大：继续拆
