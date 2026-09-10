# Changelog

所有重要变更记录在此文件。

格式基于 [Keep a Changelog](https://keepachangelog.com/)。
版本遵循 [Semantic Versioning](https://semver.org/)。

## [Unreleased]

> **2026-09-11 外审修正**:外部项目 `agent-eval-gate` 出具缺陷工单
> (`.claude/AUDIT-外审记录与修正建议.md`),其中 **P0 三条表明门禁体系实质失效** ——
> 详见 `harness/iteration/patch-log.md` §四 / §五。
> 修正期间另发现 10 条同类缺陷(X1–X10),一并修掉。

### Added

> **2026-09-11 第二轮清理**:第一轮修完 H1–H14 后复查全仓,又发现并修掉 8 条
> 同类缺陷(X11–X18,见 `harness/iteration/patch-log.md` §四 4.1)。

- `harness/rules/logging-standard.md` —— 补上骨架承诺却未交付的那一份规则文件(骨架承诺 20 份、实交 19 份)
- `scripts/stage_gate.py` —— **真状态机**:进入阶段前校验前置阶段 passed **且产出物现在依然存在**;`resume` 从第一个断点续跑
- `harness/state/stages.json` —— 十阶段门配置(阶段 → 产出物),是 `stage_gate.py` 与 `check-gates.sh` 的**单一来源**
- `tests/test_gates.py` —— **门禁防腐测试**:语法 / 可执行位 / 是否被注册 / 该拦必拦 + **反向验证**
- `tests/test_tooling.py` —— `audit_log` / `collect_metrics` / `check_dependencies` 的测试(原先一条都没有)
- `make` 目标:`setup` / `coverage` / `gates` / `state`;`markdownlint` / `yamllint` 改为复用 pre-commit 里已固定版本的 linter
- pre-commit 增加 `pytest` 钩子(H13:提交环节原先没有测试门)
- `check_secrets.py` 支持**行级豁免** `pragma: allowlist secret`(原先只能整文件跳过 = 永久盲区)
- `check_harness_docs.py` 新增**代码围栏配平 / 嵌套**校验(实测曾有 6 个文件"开了没关")

### Changed

- `scripts/check_harness_docs.py`:**删掉硬编码 181 条路径**(实测 6 条不存在),改为「锚点文件 + 目录 glob + 文档形状 + 围栏配平」四层,并支持 `--root` 以便测试(H2)
- `scripts/check-gates.sh`:**一次性检查 → 增量门** `--stage N`,且挂进 `make gates` 与 CI;顺带修掉原先**漏检 `review-record-v1.md`** 的缺口(H5)
- `scripts/state_tracker.py`:降级为**校验型转发层**(不再自己写状态,无法再绕过前置校验)(H4)
- `scripts/check_layers.py`:改为读 `.importlinter` 并委托 `lint-imports`;空转时**显式标注 `[UNIMPLEMENTED]`**,不再静默跳过(H6/H14)
- `scripts/validate_schemas.py`:改做**真的** schema 自检;缺 `jsonschema` 时 **fail** 而非 `exit(0)`(H6/H9)
- `harness/schemas/rule-schema.json`:`source` 进 required;**仅 P0** 强制带 `test`(按本仓 doctrine 精确编码)(H10)
- 5 个 workflow 从 `harness/workflows/` 移入 `.github/workflows/`;`CODEOWNERS`、`dependabot.yml` 移入 `.github/`(H7)
- `config/` 四份配置**显式标注为「示例、未接线」**,并写明要生效还缺什么(H8)
- `ruff` 的 `T20` 按目录放行(`scripts/*`、`tests/*` 是 CLI 与测试);启用 **subprocess 覆盖率**(原先 741 条语句实测 0.00% —— 门禁测不到任何东西)
- 文档层:修正 `docs/fill-workflow.md` 死引用、`harness/agent/`(单数)残留 8 处、
  README 目录树与实际不符(把 `agent/` 与 `agents/` 写成了两个目录)、
  去掉两份文档尾部的元文本、README 冻结状态改为与 `docs/freeze.md` 一致
- markdownlint 首次真正跑通(此前**从未运行过**),309 条问题已清零;`make gate` 与
  CI 自此**包含** `markdownlint` / `yamllint`(此前两个 target 存在却不在任何链路里)
- `.vscode/` 改为**随仓库交付**(原先被 `.gitignore` 忽略,而 README/USAGE 都承诺交付它)
- `stages.md` 删掉与上文重复且永远空着的「每阶段三要素」表;`changes/README.md` 与
  `state/README.md` 补上两套状态词表的粒度对照(需求级 / 阶段级)
- `tests/conftest.py` 删掉 13 个无人使用的 fixture(其中 `harness_root` /
  `sample_req_dir` 等还被 `tests/README.md` 当作"可用 fixture"介绍)
- `BluePrint.md` §2 加"蓝图≠已交付骨架"的对照说明(蓝图是原始设计,骨架更大)
- 人工确认记录的路径统一为 `harness/checkpoints/<REQ>-HC<N>.md`
  (原先 `human-checkpoints.md` 与 `checkpoints/README.md` 说法矛盾)

### Fixed

- `scripts/check_harness_docs.py:1` 是 markdown 围栏 → SyntaxError → **该脚本永不执行**,而它被 `make gate` 与 CI 调用(H1,P0)
- `tests/test_scripts.py` 用 `pytest.skip` 给坏门禁兜底(「门禁坏了就跳过它」)—— 已删,改为断言"它真的会拦"(H3,P0)
- `tests/conftest.py` 的 `pytest_report_*` fixture 名为 `pytest_*`,被 pytest 当 hook 注册 → `PluginValidationError`,**测试套件连收集都跑不起来**(X3)
- `check_secrets.py` 拦自己的测试夹具 → 加行级豁免(X4)
- `python-coding-standard.md` 是**两份文档拼接**(正文 + 重复的"（模板）"副本) → 去重(X8)
- `.gitignore` 补上 `.coverage` / `__pycache__` / `*.egg-info` / `pytest-report.json` 等构建产物(原先 `git status` 里一直挂着)

### Removed

- `harness/agents/1.md`(0 字节孤儿文件,全仓无引用;经业主确认删除)
- CI 与 Makefile 里的 `|| true` 软失败(H11/H12);`harness/workflows/dependency-update.yml` 里冗余的软审计

### 结果

- `make gate` **首次全绿**(136 个测试通过,覆盖率 84%)—— 此前因 H1/H2/H3/X1/X2/X3/X4 从未绿过

---

## [0.1.0-skeleton] - 2026-09-10

### Added

#### 核心骨架

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

#### 文档

- README 完整版
- CONTRIBUTING
- SECURITY
- CHANGELOG
- docs/（20 份）
- ADR（README + template）
- 教程（3 份）

#### CI

- harness-ci.yml
- commit-message 检查
- security-scan.yml

#### 工程配置

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

## [0.0.1] - 2026-09-10

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
