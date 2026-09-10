# 测试规范

## 规则列表

| 规则 ID  | 规则               | 检查                | 测试                   | 优先级 |
| -------- | ------------------ | ------------------- | ---------------------- | ------ |
| TEST-001 | 新增接口必须有测试 | 自定义              | tests/test_coverage.py | P0     |
| TEST-002 | 测试数必须 > 0     | check_pytest_report | CI                     | P0     |
| TEST-003 | 覆盖率 >= 80%      | pytest-cov          | CI                     | P0     |
| TEST-004 | 测试必须独立       | 自定义              | -                      | P1     |
| TEST-005 | 禁止 sleep 测试    | 自定义              | -                      | P1     |
| TEST-006 | 测试数据必须脱敏   | check_secrets       | CI                     | P0     |

## 填充指南

- 来源：测试事故
- 填充 Agent：事故反推 Agent
