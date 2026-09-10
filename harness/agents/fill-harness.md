# Harness 填充总纲

## 目标

用 Agent 从真实来源提取规则，填充 Harness。

## 执行顺序

### 阶段 1：核心 6 个（必须）

1. 架构解析 Agent → rules/project-structure.md
2. 事故反推 Agent → rules/coding-standard.md
3. Review 提炼 Agent → rules/coding-standard.md
4. 代码考古 Agent → skills/coding/
5. 数据建模 Agent → wiki/
6. 门禁解析 Agent → scripts/、CI

### 阶段 2：扩展 5 个（可选）

7. 安全 Agent → rules/security-standard.md
8. 性能 Agent → rules/performance-standard.md
9. 重构 Agent → docs/anti-patterns.md
10. 依赖 Agent → rules/dependency-standard.md
11. 文档 Agent → docs/

### 阶段 3：编排

12. Orchestrator Agent 调度全部

## 每步之后

- 人工审核
- 合并到目标文件
- 更新检查脚本
- 更新测试
- 提交 PR

## 禁止

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main。
- 不允许无来源规则进入 Harness。
- 不允许不可验证规则进入 Harness。
- 不允许无测试 P0 规则进入 Harness。

## 参考

- `harness/agents/README.md`：Agent 索引
- `harness/agents/orchestrator.md`：编排
- `docs/fill-guide.md`：详细指南
