# 数据库规范

## 规则列表

| 规则 ID | 规则               | 检查   | 测试                    | 优先级 |
| ------- | ------------------ | ------ | ----------------------- | ------ |
| DB-001  | 禁止 SELECT *      | 自定义 | tests/test_select.py    | P1     |
| DB-002  | 必须使用参数化查询 | bandit | tests/test_sql.py       | P0     |
| DB-003  | 大事务必须拆分     | 自定义 | tests/test_tx.py        | P0     |
| DB-004  | 迁移必须可回滚     | 自定义 | tests/test_migration.py | P0     |
| DB-005  | 索引命名规范       | 自定义 | -                       | P2     |
| DB-006  | 禁止在循环中查询   | 自定义 | tests/test_loop.py      | P0     |

## 填充指南

- 来源：DBA 规范、事故
- 填充 Agent：事故反推 Agent
