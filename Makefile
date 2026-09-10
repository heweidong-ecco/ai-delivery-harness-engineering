.PHONY: help install lint format type test layers secrets schema complexity i18n deps metrics audit markdownlint yamllint gate check all commit-msg hooks clean

help:
	@echo "Available targets:"
	@echo "  install      安装依赖"
	@echo "  lint         Ruff lint"
	@echo "  format       Ruff format 检查"
	@echo "  type         Mypy 类型检查"
	@echo "  test         Pytest"
	@echo "  layers       分层检查"
	@echo "  secrets      密钥扫描"
	@echo "  schema       Schema 校验"
	@echo "  complexity   复杂度检查"
	@echo "  i18n         国际化检查"
	@echo "  deps         依赖审计"
	@echo "  metrics      度量采集"
	@echo "  audit        审计记录"
	@echo "  markdownlint Markdown 检查"
	@echo "  yamllint     YAML 检查"
	@echo "  gate         完整门禁"
	@echo "  check        gate 别名"
	@echo "  all          安装 + gate"
	@echo "  commit-msg   提交信息检查"
	@echo "  hooks        安装钩子"
	@echo "  clean        清理"

install:
	pip install -e ".[dev]"

lint:
	ruff check .

format:
	ruff format --check .

type:
	mypy src

test:
	pytest --json-report --json-report-file=pytest-report.json

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

audit:
	@echo "Usage: make audit EVENT='...' DETAIL='...'"
	@[ -n "$(EVENT)" ] && python scripts/audit_log.py "$(EVENT)" "$(DETAIL)" || true

markdownlint:
	markdownlint "**/*.md" --ignore node_modules || true

yamllint:
	yamllint . || true

gate: lint format type test layers secrets schema complexity i18n
	python scripts/check_pytest_report.py pytest-report.json
	python scripts/check_python_rules.py src
	python scripts/check_harness_docs.py

check: gate

all: install gate

commit-msg:
	python scripts/check_commit_msg.py .git/COMMIT_EDITMSG

hooks:
	bash scripts/install-hooks.sh

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage pytest-report.json
	rm -rf harness/metrics/data/*.json
