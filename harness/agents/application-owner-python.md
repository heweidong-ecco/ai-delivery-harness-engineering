# Application Owner - Python 扩展

## 工具链

| 用途     | 工具              | 命令                         |
| -------- | ----------------- | ---------------------------- |
| 依赖管理 | pip / uv / poetry | <待填>                       |
| Lint     | ruff              | `ruff check .`               |
| 格式化   | ruff format       | `ruff format --check .`      |
| 类型检查 | mypy              | `mypy src`                   |
| 测试     | pytest            | `pytest --json-report`       |
| 覆盖率   | pytest-cov        | `pytest --cov-fail-under=80` |
| 安全扫描 | bandit            | `bandit -r src`              |

## 编码阶段加载

- `harness/rules/python-coding-standard.md`
- `harness/rules/python-layers.md`
- `harness/skills/coding/SKILL.md`

## 评审阶段加载

- `harness/skills/expert-reviewer/SKILL.md`
- `harness/skills/expert-reviewer/checklists/python.md`

## 单测阶段加载

- `harness/skills/unit-test/SKILL.md`

## 门禁命令

```bash
make gate
```

等价于：

bash

ruff check .
ruff format --check .
mypy src
pytest --json-report --json-report-file=pytest-report.json
python scripts/check_pytest_report.py pytest-report.json
python scripts/check_python_rules.py src
python scripts/check_harness_docs.py

## 硬性约束

- 金额禁止 float。

- 外部调用必须有 timeout。

- 测试数必须大于 0。

- 覆盖率不低于 80%。

- CI 必须满足 Status=SUCCESS、TotalTest>0、Passed=Total。

- 禁止裸 except。

- 禁止 print。

- 配置禁止硬编码。

## 回退路径

| 失败              | 回退目标           |
| ----------------- | ------------------ |
| Ruff lint 失败    | 编码实现           |
| Ruff format 失败  | 编码实现           |
| Mypy 失败         | 编码实现           |
| Pytest 测试数为 0 | 单测编写           |
| Pytest 失败       | 单测编写或编码实现 |
| Python rules 违规 | 编码实现           |
| Harness docs 缺失 | 文档管理           |

---
