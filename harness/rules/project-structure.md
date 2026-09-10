# 工程结构规则

## 模块清单

| 模块 | 职责 | 允许依赖 | 禁止依赖 |
|---|---|---|---|
| api | 对外接口 | service | dao、外部实现 |
| service | 业务编排 | domain、adapter | controller |
| domain | 领域模型与领域服务 | 无 | service、adapter |
| adapter | 外部服务适配 | domain | controller |
| dao | 数据访问 | domain | service |

## 分层架构

Controller -> Service -> Domain -> Adapter -> DAO

## 硬性约束

- Controller 不写业务逻辑。
- Service 负责流程编排。
- Domain 不依赖外部框架。
- Adapter 必须设置超时和降级。
- DAO 不写业务判断。

# 工程结构规则（模板）

## 模块清单

| 模块     | 职责   | 允许依赖 | 禁止依赖 |
| -------- | ------ | -------- | -------- |
| <模块名> | <职责> | <允许>   | <禁止>   |

## 分层架构

<填写分层，例如：api -> service -> domain -> repository -> adapter>

## 硬性约束

- <约束 1>
- <约束 2>

## 填充指南

- 来源：架构文档、模块清单、包结构
- 填充 Agent：架构解析 Agent
- 检查脚本：scripts/check_layers.py（待实现）