# Harness 填充编排

## 执行顺序

1. 架构解析 Agent → rules/project-structure.md
2. 事故反推 Agent → rules/coding-standard.md
3. Review 提炼 Agent → rules/coding-standard.md
4. 代码考古 Agent → skills/coding/
5. 数据建模 Agent → wiki/
6. 门禁解析 Agent → scripts/、CI

## 每步之后

- 人工审核
- 合并到目标文件
- 更新检查脚本
- 更新测试
- 提交

## 禁止

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main 分支。
- 不允许无来源规则进入 Harness。