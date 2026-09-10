# Python 编码规范

## 强制规则

- 所有函数必须写类型注解。
- 金额字段必须使用 `Decimal` 或整数“分”，禁止 `float`。
- 外部 HTTP/RPC 调用必须设置 `timeout`，并配置重试和降级。
- 禁止裸 `except:`，必须捕获具体异常。
- 禁止使用 `print`，统一使用 `logging`。
- 配置必须通过 `pydantic-settings` 或环境变量读取，禁止硬编码。
- 主链路修改必须同步检查国际化链路。
- 新增接口必须新增 pytest 测试。
- 禁止提交密钥、真实用户数据、生产配置。

## 可程序化验证

- `ruff check`：风格、导入、异常、print。
- `mypy`：类型注解完整性。
- `scripts/check_python_rules.py`：金额 float、HTTP timeout。
- `pytest --cov`：覆盖率不低于 80%。
- `pytest --json-report`：测试数 > 0，失败数 = 0，通过数 = 总数。

# Python 编码规范（模板）

## 强制规则

- 所有函数必须写类型注解。
- 金额字段必须使用 `Decimal` 或整数“分”，禁止 `float`。
- 外部 HTTP/RPC 调用必须设置 `timeout`，并配置重试和降级。
- 禁止裸 `except:`。
- 禁止使用 `print`，统一使用 `logging`。
- 配置必须通过环境变量或配置中心读取。
- 禁止提交密钥、真实用户数据、生产配置。

## 可程序化验证

- `ruff check`
- `mypy src`
- `scripts/check_python_rules.py`
- `pytest --cov-fail-under=80`

## 填充指南

- 来源：现有编码规范、历史 Review
- 填充 Agent：Review 提炼 Agent