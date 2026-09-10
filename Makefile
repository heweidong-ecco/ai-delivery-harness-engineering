.PHONY: help install setup lint format type test coverage layers secrets schema complexity i18n deps metrics audit markdownlint yamllint gate check gates state commit-msg hooks clean

help:
	@echo "Available targets:"
	@echo "  install      安装依赖"
	@echo "  setup        一键开发环境(venv + 依赖 + 钩子 + 首次 gate)"
	@echo "  lint         Ruff lint"
	@echo "  format       Ruff format 检查"
	@echo "  type         Mypy 类型检查"
	@echo "  test         Pytest"
	@echo "  coverage     覆盖率门禁(>=80%;骨架期显式标注未实现)"
	@echo "  layers       分层检查(读 .importlinter,委托 lint-imports)"
	@echo "  secrets      密钥扫描"
	@echo "  schema       Schema 校验"
	@echo "  complexity   复杂度检查"
	@echo "  i18n         国际化检查"
	@echo "  deps         依赖审计"
	@echo "  metrics      度量采集"
	@echo "  audit        审计记录(make audit EVENT='...' DETAIL='...')"
	@echo "  markdownlint Markdown 检查"
	@echo "  yamllint     YAML 检查"
	@echo "  gate         完整门禁"
	@echo "  gates        阶段产出物门(make gates REQ=REQ-0001 [STAGE=4])"
	@echo "  state        阶段状态机(make state ARGS='enter --req REQ-0001 --stage 需求分析')"
	@echo "  check        gate 别名"
	@echo "  all          安装 + gate"
	@echo "  commit-msg   提交信息检查"
	@echo "  hooks        安装钩子"
	@echo "  clean        清理"

install:
	pip install -e ".[dev]"

setup:
	bash scripts/dev-setup.sh

lint:
	ruff check .

format:
	ruff format --check .

type:
	mypy src

test:
	pytest --json-report --json-report-file=pytest-report.json

# 覆盖率阈值(>=80%)在此执行,而**不**放在 .coveragerc 的 fail_under 或
# pyproject 的 --cov-fail-under 里:骨架期 src/ 尚无代码,那两个位置会直接
# 让 pytest 以 0.00% 失败(一个测不到东西的假数字),而这里可以如实说明。
coverage:
	@if find src -name '*.py' -size +0 -print -quit 2>/dev/null | grep -q .; then \
		coverage report --fail-under=80; \
	else \
		echo "⚠ [UNIMPLEMENTED] src/ 尚无代码 —— 覆盖率门禁(>=80%)将在填充后自动生效"; \
		echo "  (harness 自身代码的覆盖率仍会照常测量:coverage report 可查看 scripts/)"; \
	fi

layers:
	python scripts/check_layers.py src

secrets:
	python scripts/check_secrets.py .

schema:
	python scripts/validate_schemas.py

complexity:
	python scripts/check_complexity.py src

i18n:
	python scripts/check_i18n.py src

deps:
	python scripts/check_dependencies.py

metrics:
	python scripts/collect_metrics.py

# 反外审 H12:原先带 `|| true`,于是"检查"永不失败 —— 等于没有检查。
audit:
	@[ -n "$(EVENT)" ] || { echo "Usage: make audit EVENT='...' DETAIL='...'"; exit 1; }
	python scripts/audit_log.py "$(EVENT)" "$(DETAIL)"

# 复用 .pre-commit-config.yaml 里**已固定版本**的 linter,避免版本漂移;
# 同样去掉 `|| true`(H12)。
markdownlint:
	pre-commit run markdownlint --all-files

yamllint:
	pre-commit run yamllint --all-files

gate: lint format type test coverage layers secrets schema complexity i18n
	python scripts/check_pytest_report.py pytest-report.json
	python scripts/check_python_rules.py src
	python scripts/check_harness_docs.py

# 反外审 H5:阶段门原先**不在任何链路里**。现在有独立入口,且支持增量(--stage)。
gates:
	@[ -n "$(REQ)" ] || { echo "Usage: make gates REQ=REQ-0001 [STAGE=4]"; exit 1; }
	bash scripts/check-gates.sh "$(REQ)" $(if $(STAGE),--stage $(STAGE),)

# 反外审 H4:真状态机(进入阶段前校验前置阶段 + 产出物依然存在)。
state:
	python scripts/stage_gate.py $(ARGS)

check: gate

all: install gate

commit-msg:
	python scripts/check_commit_msg.py .git/COMMIT_EDITMSG

hooks:
	bash scripts/install-hooks.sh

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage pytest-report.json
	rm -rf harness/metrics/data/*.json
