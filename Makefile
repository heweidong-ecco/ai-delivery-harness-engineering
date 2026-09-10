.PHONY: install lint format type test layers secrets schema complexity i18n deps metrics audit markdownlint yamllint gate commit-msg hooks clean

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

commit-msg:
	python scripts/check_commit_msg.py .git/COMMIT_EDITMSG

hooks:
	bash scripts/install-hooks.sh

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage pytest-report.json
