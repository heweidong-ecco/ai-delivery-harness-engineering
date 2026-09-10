# 日志规范

## 规则列表

| 规则 ID | 规则                     | 检查                          | 测试                                                    | 优先级 |
| ------- | ------------------------ | ----------------------------- | ------------------------------------------------------- | ------ |
| LOG-001 | 禁止 `print`，统一用 `logging` | `scripts/check_python_rules.py` | `tests/test_scripts.py::test_check_python_rules_print` | P1     |

> 本文件是**骨架**,目前只有 LOG-001 —— 因为它是本仓**已经实现且有测试**的那一条
> (`scripts/check_python_rules.py` 的 `rule_no_print`,`tests/test_scripts.py:116` 覆盖)。
> 其余日志规则**必须从真实来源填充**(事故 / Review / 日志规范文档),
> 不得凭空编写 —— 见 `harness/rules/_template.md` 的六件套与三道防编造闸。

## 可程序化验证

- `scripts/check_python_rules.py src`：命中 `print` 即报 `LOG-001`。

## 填充指南

- 来源：日志事故、Code Review 意见、现有日志规范文档
- 填充 Agent：事故反推 Agent、Review 提炼 Agent
- 每条规则必须有来源，来源为空则拒绝
- 每条 P0 规则必须有测试

## 与其他规则的边界

- **可观测性**(埋点 / 打点 / 异常计数 / 告警)→ `observability-standard.md`(OBS-*)
- **异常处理**(不吞异常、异常带上下文)→ `error-handling.md`(ERR-*)
- 本文件只负责**日志本身**:级别、格式、脱敏、禁止 `print` 等。
