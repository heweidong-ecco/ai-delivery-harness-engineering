# Changelog

所有重要变更记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/)。
版本遵循 [Semantic Versioning](https://semver.org/)。

## [Unreleased]

### Added

- 无

### Changed

- 无

### Fixed

- 无

### Removed

- 无

---

## [0.1.0-skeleton] - 2024-XX-XX

### Added

**核心骨架**

- 完整目录结构
- 规则体系（20 份）
  - project-structure
  - dev-process
  - coding-standard
  - python-coding-standard
  - python-layers
  - security-standard
  - error-handling
  - logging-standard
  - observability-standard
  - performance-standard
  - database-standard
  - api-design-standard
  - concurrency-standard
  - cache-standard
  - idempotency-standard
  - timezone-standard
  - dependency-standard
  - testing-standard
  - i18n-standard
  - _template
- 技能体系（20 个）
  - _template
  - coding
  - expert-reviewer（+ python 清单）
  - unit-test（+ 测试数据 + Mock）
  - request-analysis
  - task-breakdown
  - ci-validation
  - deploy-validation（+ 回滚 SOP）
  - doc-management
  - knowledge-qa
  - performance/profiling
  - security/audit
  - refactor
  - migration
  - api-versioning
  - db-migration
- 知识库（8 份）
  - README、glossary、data-model、business-flows
  - monitoring、rollback-playbook、onboarding、faq
- 变更管理（9 份）
  - README + 8 份模板
- Agent 角色（2 个）
  - application-owner
  - application-owner-python
- 流水线（6 份）
  - stages、human-checkpoints、escalation
  - hotfix-process、release-process、rollback-process
- 度量（5 份）
  - metrics、dashboard、collection、badges、sla
- 迭代（3 份）
  - README、patch-log、retrospective
- 来源池（8 个目录）
- 填充 Agent（14 个）
  - 核心 6：architecture、incident、review、code-archaeology、data-modeling、gate
  - 扩展 5：security、performance、refactor、dependency、doc
  - 编排 3：orchestrator、fill-harness、README
- 辅助工作流（5 个）
- Schema（2 个）
- 脚本（16 个）
- 测试（4 个）
- 模板（5 个）
- 状态、审计、检查点目录

**文档**

- README 完整版
- CONTRIBUTING
- SECURITY
- CHANGELOG
- docs/（20 份）
- ADR（README + template）
- 教程（3 份）

**CI**

- harness-ci.yml
- commit-message 检查
- security-scan.yml

**工程配置**

- Dockerfile
- docker-compose.yml
- pyproject.toml
- Makefile
- pre-commit
- .coveragerc、.bandit、.importlinter
- .yamllint.yml、.markdownlint.yml
- .gitattributes、.gitmessage
- .editorconfig
- .env.example、.env.ci、.env.test

### Changed

- 无

### Fixed

- 无

### Removed

- 无

---

## [0.0.1] - 2024-XX-XX

### Added

- 初始化仓库
- 基础目录结构
- 基础 CI

---

## 版本说明

| 版本 | 含义       |
| ---- | ---------- |
| 0.x  | 骨架阶段   |
| 1.x  | 稳定规则   |
| 2.x  | 多项目支持 |
