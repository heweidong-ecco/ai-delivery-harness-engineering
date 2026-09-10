# 来源池

用于存放填充 Harness 的真实输入源。

| 目录          | 用途             | 填充 Agent        |
| ------------- | ---------------- | ----------------- |
| incidents/    | 事故报告         | 事故反推 Agent    |
| reviews/      | Code Review 意见 | Review 提炼 Agent |
| architecture/ | 架构文档         | 架构解析 Agent    |
| ddl/          | 数据库 DDL       | 数据建模 Agent    |
| api/          | 接口文档         | 数据建模 Agent    |
| flows/        | 业务流程图       | 数据建模 Agent    |
| code/         | 代码库快照       | 代码考古 Agent    |

## 规则

- 所有资料必须脱敏。
- 禁止提交密钥、真实用户数据、生产配置。
- 每条规则必须有来源。
- 来源为空则拒绝进入 Harness。
