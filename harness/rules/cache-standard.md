# 缓存规范

## 规则列表

| 规则 ID   | 规则          | 检查   | 测试                      | 优先级 |
| --------- | ------------- | ------ | ------------------------- | ------ |
| CACHE-001 | 必须设 TTL    | 自定义 | tests/test_ttl.py         | P0     |
| CACHE-002 | 必须处理穿透  | 自定义 | tests/test_penetration.py | P0     |
| CACHE-003 | 必须处理雪崩  | 自定义 | tests/test_avalanche.py   | P0     |
| CACHE-004 | 必须处理击穿  | 自定义 | tests/test_breakdown.py   | P0     |
| CACHE-005 | 缓存 key 规范 | 自定义 | -                         | P1     |

## 填充指南

- 来源：缓存事故
- 填充 Agent：事故反推 Agent
