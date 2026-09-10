# Pytest 单测 SOP

## 原则

改动驱动测试：改了哪个接口，就测哪个接口。

## 要求

- 使用 pytest。
- 优先使用线上真实请求的脱敏出入参。
- 覆盖正常、异常、边界。
- 测试数必须大于 0。
- 通过率必须 100%。
- 覆盖率不低于 80%。

## 命令

```bash
pytest --json-report --json-report-file=pytest-report.json
python scripts/check_pytest_report.py pytest-report.json
```
