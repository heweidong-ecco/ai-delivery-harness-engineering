# 国际化规范

## 规则列表

| 规则 ID  | 规则                    | 检查   | 测试                   | 优先级 |
| -------- | ----------------------- | ------ | ---------------------- | ------ |
| I18N-001 | 主链路改动必须同步 i18n | 自定义 | tests/test_i18n.py     | P0     |
| I18N-002 | 禁止硬编码文案          | 自定义 | tests/test_hardcode.py | P0     |
| I18N-003 | 时区必须处理            | 自定义 | tests/test_tz.py       | P0     |
| I18N-004 | 货币必须处理            | 自定义 | tests/test_currency.py | P0     |
| I18N-005 | 语言必须回退            | 自定义 | tests/test_fallback.py | P1     |

## 填充指南

- 来源：国际化事故
- 填充 Agent：事故反推 Agent
