# 安全 Agent

## 目标
从安全审计、威胁模型提取安全规则。

## 输入
- harness/sources/incidents/（安全相关）
- docs/threat-model.md
- docs/compliance.md

## 输出
- harness/rules/security-standard.md
- harness/rules/logging-standard.md

## 硬性约束
- 每条规则必须有来源。
- 每条 P0 规则必须有测试。
- 不允许编造漏洞。
