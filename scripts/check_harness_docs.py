```python
"""检查 Harness 文档完整性。"""

from pathlib import Path

REQUIRED = [
    # 根目录
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SECURITY.md",
    "Dockerfile",
    "docker-compose.yml",
    "pyproject.toml",
    "Makefile",
    "requirements.txt",
    "requirements-dev.txt",
    ".pre-commit-config.yaml",
    ".gitignore",
    ".gitattributes",
    ".editorconfig",
    ".env.example",
    ".env.ci",
    ".env.test",
    ".gitmessage",
    ".yamllint.yml",
    ".markdownlint.yml",
    ".coveragerc",
    ".bandit",
    ".importlinter",
    ".dockerignore",

    # .github
    ".github/workflows/harness-ci.yml",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
    ".github/ISSUE_TEMPLATE/config.yml",
    ".github/CODEOWNERS",
    ".github/dependabot.yml",

    # .vscode
    ".vscode/settings.json",
    ".vscode/extensions.json",

    # config
    "config/prometheus.yml",
    "config/alert-rules.yml",
    "config/logging.yml",
    "config/grafana/dashboard.json",

    # docs
    "docs/quickstart.md",
    "docs/fill-guide.md",
    "docs/faq.md",
    "docs/architecture.md",
    "docs/naming-conventions.md",
    "docs/versioning.md",
    "docs/anti-patterns.md",
    "docs/best-practices.md",
    "docs/glossary.md",
    "docs/roadmap.md",
    "docs/integrations.md",
    "docs/compliance.md",
    "docs/data-governance.md",
    "docs/threat-model.md",
    "docs/capacity-planning.md",
    "docs/adr/README.md",
    "docs/adr/template.md",
    "docs/tutorials/first-rule.md",
    "docs/tutorials/first-agent.md",
    "docs/tutorials/first-requirement.md",

    # harness/rules
    "harness/rules/project-structure.md",
    "harness/rules/dev-process.md",
    "harness/rules/coding-standard.md",
    "harness/rules/python-coding-standard.md",
    "harness/rules/python-layers.md",
    "harness/rules/security-standard.md",
    "harness/rules/error-handling.md",
    "harness/rules/logging-standard.md",
    "harness/rules/observability-standard.md",
    "harness/rules/performance-standard.md",
    "harness/rules/database-standard.md",
    "harness/rules/api-design-standard.md",
    "harness/rules/concurrency-standard.md",
    "harness/rules/cache-standard.md",
    "harness/rules/idempotency-standard.md",
    "harness/rules/timezone-standard.md",
    "harness/rules/dependency-standard.md",
    "harness/rules/testing-standard.md",
    "harness/rules/i18n-standard.md",
    "harness/rules/_template.md",

    # harness/skills
    "harness/skills/_template/SKILL.md",
    "harness/skills/coding/SKILL.md",
    "harness/skills/expert-reviewer/SKILL.md",
    "harness/skills/expert-reviewer/checklists/python.md",
    "harness/skills/unit-test/SKILL.md",
    "harness/skills/unit-test/test-data-guide.md",
    "harness/skills/unit-test/mocking-guide.md",
    "harness/skills/request-analysis/SKILL.md",
    "harness/skills/task-breakdown/SKILL.md",
    "harness/skills/ci-validation/SKILL.md",
    "harness/skills/deploy-validation/SKILL.md",
    "harness/skills/deploy-validation/rollback-sop.md",
    "harness/skills/doc-management/SKILL.md",
    "harness/skills/knowledge-qa/SKILL.md",
    "harness/skills/performance/profiling.md",
    "harness/skills/security/audit.md",
    "harness/skills/refactor/SKILL.md",
    "harness/skills/migration/SKILL.md",
    "harness/skills/api-versioning/SKILL.md",
    "harness/skills/db-migration/SKILL.md",

    # harness/wiki
    "harness/wiki/README.md",
    "harness/wiki/glossary.md",
    "harness/wiki/data-model.md",
    "harness/wiki/business-flows.md",
    "harness/wiki/monitoring.md",
    "harness/wiki/rollback-playbook.md",
    "harness/wiki/onboarding.md",
    "harness/wiki/faq.md",

    # harness/templates
    "harness/templates/incident.md",
    "harness/templates/postmortem.md",
    "harness/templates/design-doc.md",
    "harness/templates/rfc.md",
    "harness/templates/runbook.md",

    # harness/changes
    "harness/changes/README.md",
    "harness/changes/_template/README.md",
    "harness/changes/_template/requirement-analysis.md",
    "harness/changes/_template/task-breakdown.md",
    "harness/changes/_template/coding-report.md",
    "harness/changes/_template/review-record-v1.md",
    "harness/changes/_template/unit-test-report.md",
    "harness/changes/_template/ci-result.md",
    "harness/changes/_template/deploy-validation.md",

    # harness/agent
    "harness/agent/application-owner.md",
    "harness/agent/application-owner-python.md",

    # harness/pipeline
    "harness/pipeline/stages.md",
    "harness/pipeline/human-checkpoints.md",
    "harness/pipeline/escalation.md",
    "harness/pipeline/hotfix-process.md",
    "harness/pipeline/release-process.md",
    "harness/pipeline/rollback-process.md",

    # harness/metrics
    "harness/metrics/metrics.md",
    "harness/metrics/dashboard.md",
    "harness/metrics/collection.md",
    "harness/metrics/badges.md",
    "harness/metrics/sla.md",

    # harness/iteration
    "harness/iteration/README.md",
    "harness/iteration/patch-log.md",
    "harness/iteration/retrospective.md",

    # harness/sources
    "harness/sources/README.md",

    # harness/agents
    "harness/agents/README.md",
    "harness/agents/orchestrator.md",
    "harness/agents/fill-harness.md",
    "harness/agents/architecture-agent.md",
    "harness/agents/incident-agent.md",
    "harness/agents/review-agent.md",
    "harness/agents/code-archaeology-agent.md",
    "harness/agents/data-modeling-agent.md",
    "harness/agents/gate-agent.md",
    "harness/agents/security-agent.md",
    "harness/agents/performance-agent.md",
    "harness/agents/refactor-agent.md",
    "harness/agents/dependency-agent.md",
    "harness/agents/doc-agent.md",

    # harness/workflows
    "harness/workflows/auto-label.yml",
    "harness/workflows/stale.yml",
    "harness/workflows/release.yml",
    "harness/workflows/dependency-update.yml",
    "harness/workflows/security-scan.yml",

    # harness/state
    "harness/state/README.md",

    # harness/audit
    "harness/audit/README.md",

    # harness/checkpoints
    "harness/checkpoints/README.md",

    # harness/schemas
    "harness/schemas/rule-schema.json",
    "harness/schemas/skill-schema.json",

    # scripts
    "scripts/check_pytest_report.py",
    "scripts/check_python_rules.py",
    "scripts/check_harness_docs.py",
    "scripts/check_layers.py",
    "scripts/check_commit_msg.py",
    "scripts/check_secrets.py",
    "scripts/check_complexity.py",
    "scripts/check_dependencies.py",
    "scripts/check_i18n.py",
    "scripts/collect_metrics.py",
    "scripts/audit_log.py",
    "scripts/state_tracker.py",
    "scripts/validate_schemas.py",
    "scripts/check_gates.sh",
    "scripts/install-hooks.sh",
    "scripts/dev-setup.sh",

    # tests
    "tests/README.md",
    "tests/conftest.py",
    "tests/test_smoke.py",
    "tests/test_scripts.py",
]

PLACEHOLDER_SKIP = {
    "harness/rules/_template.md",
    "harness/skills/_template/SKILL.md",
    "harness/changes/_template/README.md",
}


def check_missing() -> list[str]:
    return [p for p in REQUIRED if not Path(p).exists()]


def check_placeholders() -> list[str]:
    """核心文件不应有未填占位符（模板除外）。"""
    errors: list[str] = []
    for path_str in REQUIRED:
        if path_str in PLACEHOLDER_SKIP:
            continue
        path = Path(path_str)
        if not path.exists() or path.suffix != ".md":
            continue
        content = path.read_text(encoding="utf-8")
        if "<待填>" in content and "填充指南" not in content:
            errors.append(f"{path_str}: 有未填占位符但无填充指南")
    return errors


def main() -> None:
    missing = check_missing()
    if missing:
        raise SystemExit("Missing harness docs:\n" + "\n".join(missing))

    placeholders = check_placeholders()
    if placeholders:
        print("Placeholder warnings:\n" + "\n".join(placeholders))

    print(f"Harness docs check passed ({len(REQUIRED)} files)")


if __name__ == "__main__":
    main()
