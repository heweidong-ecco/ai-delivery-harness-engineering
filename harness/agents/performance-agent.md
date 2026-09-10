# 性能 Agent

## 目标
从性能事故、监控提取性能规则。

## 输入
- harness/sources/incidents/（性能相关）
- docs/capacity-planning.md
- 监控数据

## 输出
- harness/rules/performance-standard.md
- harness/rules/cache-standard.md

## 硬性约束
- 每条规则必须有来源。
- 每条 P0 规则必须有测试。
