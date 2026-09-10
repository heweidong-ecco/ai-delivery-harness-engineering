# Application Owner - Python 扩展

## 工具链

- 依赖管理：pip / uv / poetry，按项目实际。
- Lint：ruff。
- 格式化：ruff format。
- 类型检查：mypy。
- 测试：pytest + pytest-cov + pytest-json-report。
- 安全扫描：bandit。

## 编码阶段加载

- `harness/rules/python-coding-standard.md`
- `harness/rules/python-layers.md`
- `harness/skills/coding/python-layers.md`

## 评审阶段加载

- `harness/skills/expert-reviewer/checklists/python.md`

## 单测阶段加载

- `harness/skills/unit-test/pytest-sop.md`

## 门禁命令

```bash
make gate

## 硬性约束

- 金额禁止 float。
- 外部调用必须有 timeout。
- 测试数必须大于 0。
- 覆盖率不低于 80%。
- CI 必须满足 Status=SUCCESS、TotalTest>0、Passed=Total。
