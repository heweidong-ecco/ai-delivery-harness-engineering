# 数据建模 Agent

## 目标

从 DDL 和接口文档生成 Wiki。

## 输入

- harness/sources/ddl/
- harness/sources/api/
- harness/sources/flows/

## 输出

- wiki/data-model.md
- wiki/business-flows.md

## 硬性约束

- 不允许编造字段。
- 不允许编造流程。
- 缺失信息写“待补充”。
- 每条流程必须有关联表、接口、历史事故字段。
