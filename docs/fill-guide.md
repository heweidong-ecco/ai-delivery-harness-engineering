# 填充指南

## 执行顺序

### 第一阶段：核心 6 个 Agent

1. 架构解析 Agent → rules/project-structure.md
2. 事故反推 Agent → rules/coding-standard.md
3. Review 提炼 Agent → rules/coding-standard.md
4. 代码考古 Agent → skills/coding/
5. 数据建模 Agent → wiki/
6. 门禁解析 Agent → scripts/、CI

### 第二阶段：扩展 5 个 Agent（可选）

7. 安全 Agent → rules/security-standard.md
8. 性能 Agent → rules/performance-standard.md
9. 重构 Agent → docs/anti-patterns.md
10. 依赖 Agent → rules/dependency-standard.md
11. 文档 Agent → docs/

### 第三阶段：编排

12. Orchestrator Agent → 调度全部

## 每步

1. 来源放入 harness/sources/
2. 跑对应 Agent
3. 人工审核
4. 合并回填
5. 更新检查脚本
6. 更新测试
7. 提交 PR

## 来源要求
...

## 三道防编造闸
...
