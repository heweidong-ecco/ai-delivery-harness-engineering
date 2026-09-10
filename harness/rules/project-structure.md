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
