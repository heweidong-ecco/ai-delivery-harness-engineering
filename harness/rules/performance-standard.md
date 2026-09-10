# 性能规范

## 规则列表

| 规则 ID  | 规则               | 检查   | 测试                    | 优先级 |
| -------- | ------------------ | ------ | ----------------------- | ------ |
| PERF-001 | 禁止 N+1 查询      | 自定义 | tests/test_n_plus_1.py  | P0     |
| PERF-002 | 关键查询必须有索引 | 自定义 | tests/test_index.py     | P0     |
| PERF-003 | 大循环禁止 IO      | 自定义 | tests/test_loop_io.py   | P1     |
| PERF-004 | 批量优先于单条     | 自定义 | tests/test_batch.py     | P1     |
| PERF-005 | 缓存必须设过期     | 自定义 | tests/test_cache_ttl.py | P1     |
| PERF-006 | 接口 P99 必须达标  | 监控   | -                       | P1     |

## 填充指南

- 来源：性能事故、监控
- 填充 Agent：事故反推 Agent、性能 Agent
