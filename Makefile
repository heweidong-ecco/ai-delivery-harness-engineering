.PHONY: install lint format type test gate layers commit-msg hooks clean

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

gate: lint format type test layers
	python scripts/check_pytest_report.py pytest-report.json
	python scripts/check_python_rules.py src
	python scripts/check_harness_docs.py

commit-msg:
	python scripts/check_commit_msg.py .git/COMMIT_EDITMSG

hooks:
	bash scripts/install-hooks.sh

clean:
	rm -rf .pytest_cache .mypy_cache .ruff_cache htmlcov .coverage pytest-report.json