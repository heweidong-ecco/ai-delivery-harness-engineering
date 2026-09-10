# AI Delivery Harness Engineering

AI 代码上线 Harness 体系：规则、技能、知识库、变更管理、Agent 角色、十阶段流水线与质量门禁，让 AI 生成代码质量可控、可发现、可修复。

不依赖具体项目的 Harness 骨架。  
用于后续按项目填充规则、技能、知识库和 Agent。

## 核心目标

- 项目维度 AI 代码率： 90.%
- 个人维度 AI 代码率： 90%
- 返工轮次：3-5 轮 → 通常 1 轮
- 质量可控前提下的高 AI 代码率

## 骨架仓库目标

- 不含具体项目信息
- 所有规则、技能、知识库、Agent 定义均为模板
- 每个文件有明确占位符和填充指南
- CI 和门禁可运行，但不依赖业务代码
- 后续用 Agent 按来源池填充

## 目录

- `harness/rules/`：工程结构、开发流程、编码规范
- `harness/skills/`：9 个 Skill
- `harness/wiki/`：领域术语、数据模型、业务流程
- `harness/changes/`：需求变更全流程留痕
- `harness/agent/`：Application Owner 角色定义
- `harness/pipeline/`：十阶段流水线与门禁
- `harness/metrics/`：度量指标
- `harness/iteration/`：持续 Patch 记录
- `scripts/`：门禁检查脚本
- `.github/workflows/`：CI 工作流

ai-delivery-harness-engineering/
├── README.md
├── pyproject.toml
├── Makefile
├── .pre-commit-config.yaml
├── .gitignore
├── .github/
│   └── workflows/
│       └── harness-ci.yml
├── harness/
│   ├── rules/
│   │   ├── project-structure.md
│   │   ├── dev-process.md
│   │   ├── coding-standard.md
│   │   ├── python-coding-standard.md
│   │   └── python-layers.md
│   ├── skills/
│   │   ├── coding/
│   │   │   └── SKILL.md
│   │   ├── expert-reviewer/
│   │   │   ├── SKILL.md
│   │   │   └── checklists/
│   │   │       └── python.md
│   │   ├── unit-test/
│   │   │   └── SKILL.md
│   │   ├── request-analysis/
│   │   │   └── SKILL.md
│   │   ├── task-breakdown/
│   │   │   └── SKILL.md
│   │   ├── ci-validation/
│   │   │   └── SKILL.md
│   │   ├── deploy-validation/
│   │   │   └── SKILL.md
│   │   ├── doc-management/
│   │   │   └── SKILL.md
│   │   └── knowledge-qa/
│   │       └── SKILL.md
│   ├── wiki/
│   │   ├── glossary.md
│   │   ├── data-model.md
│   │   └── business-flows.md
│   ├── changes/
│   │   └── _template/
│   │       ├── requirement-analysis.md
│   │       ├── task-breakdown.md
│   │       ├── coding-report.md
│   │       ├── review-record-v1.md
│   │       ├── unit-test-report.md
│   │       ├── ci-result.md
│   │       └── deploy-validation.md
│   ├── agent/
│   │   ├── application-owner.md
│   │   └── application-owner-python.md
│   ├── pipeline/
│   │   └── stages.md
│   ├── metrics/
│   │   └── metrics.md
│   ├── iteration/
│   │   └── patch-log.md
│   ├── sources/
│   │   ├── incidents/
│   │   │   └── .gitkeep
│   │   ├── reviews/
│   │   │   └── .gitkeep
│   │   ├── architecture/
│   │   │   └── .gitkeep
│   │   ├── ddl/
│   │   │   └── .gitkeep
│   │   ├── api/
│   │   │   └── .gitkeep
│   │   ├── flows/
│   │   │   └── .gitkeep
│   │   └── code/
│   │       └── .gitkeep
│   └── agents/
│       └── fill-harness.md
├── scripts/
│   ├── check_pytest_report.py
│   ├── check_python_rules.py
│   ├── check_harness_docs.py
│   └── check_gates.sh
└── tests/
    └── test_smoke.py


## 填充方式

见 `harness/agents/fill-harness.md`。