# 填充指南

## 顺序

1. 架构解析 Agent → rules/project-structure.md
2. 事故反推 Agent → rules/coding-standard.md
3. Review 提炼 Agent → rules/coding-standard.md
4. 代码考古 Agent → skills/coding/
5. 数据建模 Agent → wiki/
6. 门禁解析 Agent → scripts/、CI

## 每步

1. 把来源放入 harness/sources/。
2. 跑对应 Agent。
3. 人工审核。
4. 合并到目标文件。
5. 更新检查脚本。
6. 更新测试。
7. 提交 PR。

## 来源要求

- 每条规则必须有来源。
- 来源为空则拒绝。
- 来源必须可查。

## 审核

- 真实性
- 可程序化
- 可测试
- 优先级
- Owner

## 禁止

- 无来源规则。
- 不可验证规则。
- 无测试 P0 规则。