# 骨架架构

## 分层

```text
L0 目标与度量
L1 规则体系
L2 编排与角色
L3 知识与技能
L4 执行流水线
L5 质量门禁与回退
L6 变更与沉淀
L7 持续迭代
```

## 数据流
```text
来源 → Agent → 规则/技能/Wiki → 流水线 → 门禁 → 反馈
```

## 目录映射
层	目录
L1	harness/rules/
L2	harness/agent/
L3	harness/skills/、harness/wiki/
L4	harness/pipeline/
L5	scripts/、.github/workflows/
L6	harness/changes/
L7	harness/iteration/、harness/sources/