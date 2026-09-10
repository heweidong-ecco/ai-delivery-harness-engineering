# CI 结果

## 基本信息

| 字段     | 内容       |
| -------- | ---------- |
| 需求编号 | REQ-XXXX   |
| 流水线   | Harness CI |
| 运行 ID  | <待填>     |
| 日期     | <待填>     |

## 门禁结果

| 门禁          | 命令                     | 结果        | 说明 |
| ------------- | ------------------------ | ----------- | ---- |
| Ruff lint     | `ruff check .`           | <通过/失败> |      |
| Ruff format   | `ruff format --check .`  | <通过/失败> |      |
| Mypy          | `mypy src`               | <通过/失败> |      |
| Pytest        | `pytest --json-report`   | <通过/失败> |      |
| Pytest report | `check_pytest_report.py` | <通过/失败> |      |
| Python rules  | `check_python_rules.py`  | <通过/失败> |      |
| Harness docs  | `check_harness_docs.py`  | <通过/失败> |      |

## 可程序化验证条件

- Status = SUCCESS
- TotalTest > 0
- Passed = Total

## 结论

- [ ] CI 通过
- [ ] CI 失败，需回退

## 失败回退

- 若测试数为 0：回退单测编写
- 若编译错误：回退编码实现
- 若规则违规：回退编码实现

## 备注

<待填>
