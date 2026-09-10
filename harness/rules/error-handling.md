# 异常处理规范

## 规则列表

| 规则 ID | 规则                 | 检查      | 测试                  | 优先级 |
| ------- | -------------------- | --------- | --------------------- | ------ |
| ERR-001 | 禁止裸 except        | ruff E722 | tests/test_except.py  | P0     |
| ERR-002 | 异常必须带上下文     | 自定义    | tests/test_context.py | P0     |
| ERR-003 | 外部异常必须转换     | 自定义    | tests/test_convert.py | P0     |
| ERR-004 | 禁止吞异常           | 自定义    | tests/test_swallow.py | P0     |
| ERR-005 | 业务异常必须有错误码 | 自定义    | tests/test_code.py    | P0     |

## 填充指南

- 来源：事故、Review
- 填充 Agent：事故反推 Agent
