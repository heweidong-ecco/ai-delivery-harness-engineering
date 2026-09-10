# 填充 Agent 索引

## 核心 Agent（6 个）

| Agent       | 文件                      | 输入                | 输出                  |
| ----------- | ------------------------- | ------------------- | --------------------- |
| 架构解析    | architecture-agent.md     | architecture/、src/ | extracted-rules.md    |
| 事故反推    | incident-agent.md         | incidents/          | extracted-rules.md    |
| Review 提炼 | review-agent.md           | reviews/            | extracted-rules.md    |
| 代码考古    | code-archaeology-agent.md | src/                | extracted-patterns.md |
| 数据建模    | data-modeling-agent.md    | ddl/、api/、flows/  | wiki/                 |
| 门禁解析    | gate-agent.md             | CI、Makefile        | extracted-gates.md    |

## 扩展 Agent（5 个）

| Agent | 文件                 | 输入           | 输出                    |
| ----- | -------------------- | -------------- | ----------------------- |
| 安全  | security-agent.md    | 安全审计       | security-standard.md    |
| 性能  | performance-agent.md | 性能事故       | performance-standard.md |
| 重构  | refactor-agent.md    | src/           | anti-patterns.md        |
| 依赖  | dependency-agent.md  | pyproject.toml | dependency-standard.md  |
| 文档  | doc-agent.md         | src/、changes/ | docs/                   |

## 编排 Agent（3 个）

| Agent             | 文件                 | 作用     |
| ----------------- | -------------------- | -------- |
| Orchestrator      | orchestrator.md      | 调度全部 |
| Fill Harness      | fill-harness.md      | 填充总纲 |
| Application Owner | application-owner.md | 需求编排 |

## 执行顺序

1. 核心 6 个（必须）
2. 扩展 5 个（可选）
3. Orchestrator 调度

## 硬性约束

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main。
- 不允许无来源规则进入 Harness。
- 每条规则必须有来源、检查、测试。
