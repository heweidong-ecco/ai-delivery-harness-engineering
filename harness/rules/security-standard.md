# 安全规范

## 规则列表

| 规则 ID | 规则               | 检查                          | 测试                  | 优先级 |
| ------- | ------------------ | ----------------------------- | --------------------- | ------ |
| SEC-001 | 禁止提交密钥       | scripts/check_secrets.py      | tests/test_secrets.py | P0     |
| SEC-002 | 敏感日志必须脱敏   | ruff 自定义                   | tests/test_logging.py | P0     |
| SEC-003 | 外部调用必须 HTTPS | scripts/check_python_rules.py | tests/test_http.py    | P0     |
| SEC-004 | SQL 必须参数化     | bandit                        | tests/test_sql.py     | P0     |
| SEC-005 | 禁止 eval/exec     | bandit                        | tests/test_eval.py    | P0     |
| SEC-006 | 依赖必须扫描       | pip-audit                     | CI                    | P1     |

## 填充指南

- 来源：安全审计、事故
- 填充 Agent：事故反推 Agent