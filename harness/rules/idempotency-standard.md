# 幂等规范

## 规则列表

| 规则 ID  | 规则           | 检查   | 测试                     | 优先级 |
| -------- | -------------- | ------ | ------------------------ | ------ |
| IDEM-001 | 写接口必须幂等 | 自定义 | tests/test_idempotent.py | P0     |
| IDEM-002 | 必须用幂等键   | 自定义 | tests/test_key.py        | P0     |
| IDEM-003 | 重试必须安全   | 自定义 | tests/test_retry.py      | P0     |
| IDEM-004 | 消息必须去重   | 自定义 | tests/test_msg.py        | P0     |

## 填充指南

- 来源：重复执行事故
- 填充 Agent：事故反推 Agent
