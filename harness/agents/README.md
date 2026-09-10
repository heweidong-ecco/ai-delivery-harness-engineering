# 填充 Agent 索引

| Agent       | 文件                      | 输入                | 输出                  |
| ----------- | ------------------------- | ------------------- | --------------------- |
| 架构解析    | architecture-agent.md     | architecture/、src/ | extracted-rules.md    |
| 事故反推    | incident-agent.md         | incidents/          | extracted-rules.md    |
| Review 提炼 | review-agent.md           | reviews/            | extracted-rules.md    |
| 代码考古    | code-archaeology-agent.md | src/                | extracted-patterns.md |
| 数据建模    | data-modeling-agent.md    | ddl/、api/、flows/  | wiki/                 |
| 门禁解析    | gate-agent.md             | CI、Makefile        | extracted-gates.md    |
| 编排        | orchestrator.md           | 全部                | 调度                  |

## 执行顺序

1. 架构解析
2. 事故反推
3. Review 提炼
4. 代码考古
5. 数据建模
6. 门禁解析

## 硬性约束

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main。
- 不允许无来源规则进入 Harness。
- 每条规则必须有来源、检查、测试。