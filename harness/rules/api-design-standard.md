# API 设计规范

## 规则列表

| 规则 ID | 规则         | 检查     | 测试                     | 优先级 |
| ------- | ------------ | -------- | ------------------------ | ------ |
| API-001 | 必须版本化   | 自定义   | tests/test_version.py    | P0     |
| API-002 | 必须幂等     | 自定义   | tests/test_idempotent.py | P0     |
| API-003 | 必须分页     | 自定义   | tests/test_paging.py     | P1     |
| API-004 | 必须限流     | 配置检查 | -                        | P0     |
| API-005 | 必须鉴权     | 自定义   | tests/test_auth.py       | P0     |
| API-006 | 错误码规范   | 自定义   | tests/test_error.py      | P1     |
| API-007 | 字段命名规范 | 自定义   | -                        | P2     |

## 填充指南

- 来源：API 规范、事故
- 填充 Agent：事故反推 Agent
