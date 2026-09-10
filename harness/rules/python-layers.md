# Python 分层架构

| 层 | 职责 | 允许依赖 | 禁止依赖 |
|---|---|---|---|
| api | 路由、请求校验、响应封装 | service | repository、adapter |
| service | 业务编排、事务边界 | domain、repository、adapter | api |
| domain | 领域模型、领域服务 | 无 | service、api、repository |
| repository | 数据访问 | domain | service、api |
| adapter | 外部服务适配 | domain | api、service |
| config | 配置 | 无 | 业务层 |

## 硬性约束

- `api` 不写业务逻辑。
- `service` 负责编排，不直接写 SQL。
- `domain` 不依赖 Web 框架和 ORM。
- `adapter` 必须设置超时、重试、降级。
- `repository` 不写业务判断。

# Python 分层架构（模板）

| 层         | 职责   | 允许依赖                    | 禁止依赖                 |
| ---------- | ------ | --------------------------- | ------------------------ |
| api        | <职责> | service                     | repository, adapter      |
| service    | <职责> | domain, repository, adapter | api                      |
| domain     | <职责> | 无                          | service, api, repository |
| repository | <职责> | domain                      | service, api             |
| adapter    | <职责> | domain                      | api, service             |

## 硬性约束

- api 不写业务逻辑。
- service 负责编排，不直接写 SQL。
- domain 不依赖 Web 框架和 ORM。
- adapter 必须设置超时、重试、降级。
- repository 不写业务判断。

## 填充指南

- 来源：架构文档、代码库
- 填充 Agent：架构解析 Agent