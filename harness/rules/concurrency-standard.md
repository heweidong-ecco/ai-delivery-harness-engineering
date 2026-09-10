# 并发规范

## 规则列表

| 规则 ID  | 规则             | 检查   | 测试                  | 优先级 |
| -------- | ---------------- | ------ | --------------------- | ------ |
| CONC-001 | 共享状态必须加锁 | 自定义 | tests/test_lock.py    | P0     |
| CONC-002 | 禁止在锁内 IO    | 自定义 | tests/test_lock_io.py | P0     |
| CONC-003 | 线程池必须限大小 | 自定义 | tests/test_pool.py    | P0     |
| CONC-004 | 异步必须处理异常 | 自定义 | tests/test_async.py   | P0     |
| CONC-005 | 禁止 sleep 轮询  | 自定义 | tests/test_sleep.py   | P1     |

## 填充指南

- 来源：并发事故
- 填充 Agent：事故反推 Agent
