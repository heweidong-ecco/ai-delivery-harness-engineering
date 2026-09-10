# 时区规范

## 规则列表

| 规则 ID | 规则                | 检查   | 测试                  | 优先级 |
| ------- | ------------------- | ------ | --------------------- | ------ |
| TZ-001  | 存储必须 UTC        | 自定义 | tests/test_utc.py     | P0     |
| TZ-002  | 禁止 naive datetime | 自定义 | tests/test_naive.py   | P0     |
| TZ-003  | 展示必须带时区      | 自定义 | tests/test_display.py | P0     |
| TZ-004  | 跨时区必须转换      | 自定义 | tests/test_convert.py | P0     |

## 填充指南

- 来源：时区事故
- 填充 Agent：事故反推 Agent
