> **项目蓝图**：见 [BluePrint.md](./BluePrint.md)
> **使用指南**：见 [USAGE.md](./USAGE.md)
> **填充工作流**：见 [FillWorkflow.md](./FillWorkflow.md)
> **状态**：v0.1.0-skeleton **已于 2026-09-11 解冻**，用于修正外审缺陷 H1–H14（见 `docs/freeze.md`）。
> 骨架 100% 完成，填充 0%，试点 0%。
> 下一步：修完 H1–H14 → 由业务方决定是否重新冻结 → 引入项目 → 跑 6 个核心 Agent → 空跑 REQ-0000。
>
# AI Delivery Harness Engineering

> AI 代码上线 Harness 体系：用外部约束与反馈系统，让 AI 生成的代码真正可上线。

[![CI](https://github.com/<org>/<repo>/actions/workflows/harness-ci.yml/badge.svg)](https://github.com/<org>/<repo>/actions/workflows/harness-ci.yml)
[![License](https://img.shields.io/badge/license-MIT-blue)](./LICENSE)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
![Status](https://img.shields.io/badge/status-skeleton--unfrozen-orange)

---

## 目录

- [一、这是什么](#一这是什么)
- [二、为什么需要它](#二为什么需要它)
- [三、核心理念](#三核心理念)
- [四、它解决什么问题](#四它解决什么问题)
- [五、整体架构](#五整体架构)
- [六、目录结构](#六目录结构)
- [七、核心组件详解](#七核心组件详解)
- [八、十阶段开发流水线](#八十阶段开发流水线)
- [九、快速开始](#九快速开始)
- [十、完整使用方法](#十完整使用方法)
- [十一、填充指南](#十一填充指南)
- [十二、CI 与门禁](#十二ci-与门禁)
- [十三、度量指标](#十三度量指标)
- [十四、关键经验](#十四关键经验)
- [十五、常见问题](#十五常见问题)
- [十六、贡献指南](#十六贡献指南)
- [十七、版本与路线图](#十七版本与路线图)
- [十八、许可证](#十八许可证)

---

## 一、这是什么

**AI Delivery Harness Engineering** 是一套**不依赖具体项目**的 AI 代码交付骨架。

它的目标只有一个：

> **让 AI 写出来的代码，不只是"语法正确"，而是经过需求分析、评审、单测、CI、部署验证后，真正可上线。**

它不换更强的模型，不依赖某个特定框架，而是搭建一套**外部的约束与反馈系统**：

- **规则**：把资深开发者脑子里的隐性规矩写下来；
- **技能**：把每个阶段的最佳实践变成 SOP；
- **知识库**：把业务上下文按需喂给 Agent；
- **变更管理**：全流程留痕；
- **Agent 角色**：编排、执行、评审分离；
- **十阶段流水线**：从需求到交付的完整闭环；
- **质量门禁**：可程序化验证；
- **回退路径**：出问题精确路由到该修的环节；
- **人工确认点**：关键决策权始终在人手里。

---

## 二、为什么需要它

### 现状

你可能已经在用 AI 写代码，体感确实快了。但在真实企业级项目里：

- 十几万行代码；
- RPC 框架；
- 流程引擎；
- 配置中心；
- 分布式缓存；
- 全套中间件。

你大概率遇到过：

- AI 生成代码语法完美、风格统一；
- 但业务逻辑有微妙错误；
- 编译没问题，运行却错漏百出。

### 典型错误

- 价格字段用 `Double` 而不是 `Long`，单位搞错；
- 改了主链路，漏了国际化链路同步修改；
- 调用外部服务，没设超时和降级；
- 事务边界混乱；
- 配置硬编码；
- 缓存未设 TTL。

### 为什么

这些错误**不是模型不够聪明**，而是：

> **模型不知道你项目里那些从未被写下来的规矩。**

这些规矩以前靠：

- 口头传承；
- Code Review；
- 事故复盘；
- 老人带新人。

现在需要让 Agent 也知道。

### 结果

阿里团队在一个存量项目上，用一周时间搭了一套 Harness 体系：

- 项目维度 AI 代码率：**24.86% → 90.54%**
- 个人维度 AI 代码率：**14.24% → 87.85%**
- 返工轮次：**3-5 轮 → 通常 1 轮**

他们没有换更强的模型，只是搭了一套外部约束和反馈系统。

---

## 三、核心理念

### 理念一：工程化消除错误

每次发现 Agent 犯错，不是加一句"请注意不要犯这个错"，而是：

> **把约束变成文件、规则、自动化检查，让它成为系统的一部分。**

### 理念二：可程序化验证

> **一切不可被机器验证的约束，在 Agent 执行中都是无效约束。**

例如：

- ❌ "检查 CI 是否通过" → Agent 可能认为状态 Success 即通过，忽略测试数为 0；
- ✅ "Status=SUCCESS 且 TotalTest>0 且 Passed=Total" → 彻底消除歧义。

### 理念三：执行与评判分离

> **做事的 Agent 和评判的 Agent 必须分开。**

评审 Agent 不需要更聪明，它只需要用一套**不同视角的检查清单**来审视产出物。

### 理念四：上下文刚好够用

> **让 Agent 在任何时刻都拥有刚好够用的上下文，不多不少。**

分三层加载：

1. **会话长驻**：Agent 定义 + 规则文件；
2. **阶段触发**：进入某阶段才加载对应 Skill；
3. **按需查询**：Wiki 不主动加载，Agent 自主查阅。

### 理念五：流程一致性优先于效率

> **小改动大事故的案例不胜枚举。**

一个只涉及两个文件、六行代码的小需求，依然走完整十阶段流程。当需求足够简单时，每个阶段执行时间自然缩短，但流程一致性保证不会因为"这次改动很小"就跳过关键环节。

### 理念六：规范是活文档

> **规范的每一行都对应一个历史失败案例。**

每次实战发现新问题，立即 Patch 到 Harness。当你觉得某条规则多余或啰嗦时，往往是它背后有一个真实踩过的坑。

---

## 四、它解决什么问题

### 四类典型失败模式

| 失败模式           | 表现                            | 根因         |
| ------------------ | ------------------------------- | ------------ |
| **试图一步到位**   | 上下文占用超 40% 后质量快速衰退 | 缺乏阶段切分 |
| **过早宣布胜利**   | 完成部分工作就说"编码完成"      | 缺乏验收门禁 |
| **没做端到端验证** | 部署后才发现关键路径不通        | 缺乏 CI 验证 |
| **冷启动问题**     | 每次会话重新理解项目            | 缺乏知识沉淀 |

### 共同根源

> **Agent 缺乏外部的结构化约束和反馈机制。**

Anthropic 在工程博客里说得很直白：

> **Agent 无法准确评估自身产出的质量。你不能指望 Agent 自己审查自己。**

---

## 五、整体架构

### 分层架构

```text
L0 目标与度量层
  ├── AI 代码率
  ├── 返工轮次
  ├── 人工确认轮次
  └── 质量门禁通过率

L1 治理与规则层
  ├── 工程结构规则
  ├── 开发流程规范
  ├── 项目编码规范
  ├── Python 编码规范
  ├── Python 分层规范
  ├── 安全规范
  ├── 异常处理规范
  ├── 日志规范
  ├── 可观测性规范
  ├── 性能规范
  ├── 数据库规范
  ├── API 设计规范
  ├── 并发规范
  ├── 缓存规范
  ├── 幂等规范
  ├── 时区规范
  ├── 依赖规范
  ├── 测试规范
  └── 国际化规范

L2 编排与角色层
  ├── Application Owner Agent
  ├── 编码 Agent
  ├── 评审 Agent
  └── 人工决策者

L3 知识与技能层
  ├── 9 个核心 Skill
  ├── 扩展 Skill
  ├── Wiki 知识库
  └── 分层上下文加载

L4 执行流水线层
  ├── 需求分析 → 需求评审 → 计划评审
  ├── 编码实现 → 编码评审
  ├── 单测编写 → 单测评审
  └── CI 验证 → 部署验证 → 用户确认

L5 质量门禁与回退层
  ├── 可程序化验证
  ├── 评审循环上限
  ├── 精确回退路径
  └── 人工升级机制

L6 变更与知识沉淀层
  ├── 需求独立目录
  ├── 全流程留痕
  ├── 评审版本递增
  └── 活的项目开发手册

L7 持续迭代层
  ├── 空跑验证
  ├── 实战问题 Patch
  └── 规范持续迭代
```

### 数据流

```text
真实输入源（事故/Review/架构/DDL/代码库）
        ↓
   填充 Agent
        ↓
  规则 / 技能 / Wiki
        ↓
   十阶段流水线
        ↓
    质量门禁
        ↓
   反馈与 Patch
        ↓
   回到规则 / 技能 / Wiki
```

---

## 六、目录结构

```text
ai-delivery-harness-engineering/
│
├── README.md                              # 本文件
├── LICENSE                                # MIT 许可证
├── CONTRIBUTING.md                        # 贡献指南
├── CHANGELOG.md                           # 变更记录
├── SECURITY.md                            # 安全政策
├── Dockerfile                             # 容器化
├── docker-compose.yml                     # 本地编排
├── pyproject.toml                         # Python 项目配置
├── Makefile                               # 常用命令
├── requirements.txt                       # 兼容旧工具
├── requirements-dev.txt                   # 兼容旧工具
│
├── .pre-commit-config.yaml                # Pre-commit 钩子
├── .gitignore                             # Git 忽略
├── .gitattributes                         # Git 属性
├── .editorconfig                          # 编辑器配置
├── .env.example                           # 环境变量示例
├── .env.ci                                # CI 环境变量
├── .env.test                              # 测试环境变量
├── .gitmessage                            # 提交模板
├── .yamllint.yml                          # YAML 校验
├── .markdownlint.yml                      # Markdown 校验
├── .coveragerc                            # 覆盖率配置
├── .bandit                                # 安全扫描配置
├── .importlinter                          # 分层依赖校验
├── .dockerignore                          # 容器忽略
│
├── .github/
│   ├── workflows/
│   │   ├── harness-ci.yml                 # 主 CI 工作流
│   │   ├── auto-label.yml                 # 自动标签
│   │   ├── stale.yml                      # 过期 Issue
│   │   ├── release.yml                    # 发布
│   │   ├── dependency-update.yml          # 依赖更新
│   │   └── security-scan.yml              # 安全扫描
│   ├── PULL_REQUEST_TEMPLATE.md           # PR 模板
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md                  # Bug 模板
│   │   ├── feature_request.md             # 需求模板
│   │   └── config.yml                     # Issue 配置
│   ├── labeler.yml                        # 标签规则
│   ├── CODEOWNERS                         # 代码所有者
│   └── dependabot.yml                     # 依赖更新
│
├── .vscode/
│   ├── settings.json                      # VSCode 配置
│   └── extensions.json                    # 推荐扩展
│
├── config/                                # 观测配置(示例,**均未接线** —— 见各文件头部说明)
│   ├── prometheus.yml                     # Prometheus 示例
│   ├── alert-rules.yml                    # 告警规则示例(指标名尚未产出)
│   ├── logging.yml                        # 日志配置示例(暂无消费者)
│   └── grafana/
│       └── dashboard.json                 # Grafana 面板示例(无 datasource/query)
│
├── docs/
│   ├── quickstart.md                      # 快速开始
│   ├── fill-guide.md                      # 填充指南
│   ├── faq.md                             # FAQ
│   ├── architecture.md                    # 骨架架构
│   ├── freeze.md                          # 冻结 / 解冻记录
│   ├── naming-conventions.md              # 命名约定
│   ├── versioning.md                      # 版本策略
│   ├── anti-patterns.md                   # 反模式
│   ├── best-practices.md                  # 最佳实践
│   ├── glossary.md                        # 术语表
│   ├── roadmap.md                         # 路线图
│   ├── integrations.md                    # 集成说明
│   ├── compliance.md                      # 合规说明
│   ├── data-governance.md                 # 数据治理
│   ├── threat-model.md                    # 威胁模型
│   ├── capacity-planning.md               # 容量规划
│   ├── adr/
│   │   ├── README.md                      # ADR 索引
│   │   └── template.md                    # ADR 模板
│   └── tutorials/
│       ├── first-rule.md                  # 第一条规则
│       ├── first-agent.md                 # 第一个 Agent
│       └── first-requirement.md           # 第一个需求
│
├── harness/
│   │
│   ├── rules/                             # 规则体系
│   │   ├── project-structure.md           # 工程结构
│   │   ├── dev-process.md                 # 开发流程
│   │   ├── coding-standard.md             # 编码规范
│   │   ├── python-coding-standard.md      # Python 编码规范
│   │   ├── python-layers.md               # Python 分层
│   │   ├── security-standard.md           # 安全规范
│   │   ├── error-handling.md              # 异常处理
│   │   ├── logging-standard.md            # 日志规范
│   │   ├── observability-standard.md      # 可观测性
│   │   ├── performance-standard.md        # 性能规范
│   │   ├── database-standard.md           # 数据库规范
│   │   ├── api-design-standard.md         # API 设计规范
│   │   ├── concurrency-standard.md        # 并发规范
│   │   ├── cache-standard.md              # 缓存规范
│   │   ├── idempotency-standard.md        # 幂等规范
│   │   ├── timezone-standard.md           # 时区规范
│   │   ├── dependency-standard.md         # 依赖规范
│   │   ├── testing-standard.md            # 测试规范
│   │   ├── i18n-standard.md               # 国际化规范
│   │   └── _template.md                   # 规则模板
│   │
│   ├── skills/                            # 技能体系
│   │   ├── _template/
│   │   │   └── SKILL.md
│   │   ├── coding/
│   │   │   └── SKILL.md                   # 编码技能
│   │   ├── expert-reviewer/
│   │   │   ├── SKILL.md                   # 评审技能
│   │   │   └── checklists/
│   │   │       └── python.md              # Python 评审清单
│   │   ├── unit-test/
│   │   │   ├── SKILL.md                   # 单测技能
│   │   │   ├── test-data-guide.md         # 测试数据指南
│   │   │   └── mocking-guide.md           # Mock 指南
│   │   ├── request-analysis/
│   │   │   └── SKILL.md                   # 需求分析
│   │   ├── task-breakdown/
│   │   │   └── SKILL.md                   # 任务拆分
│   │   ├── ci-validation/
│   │   │   └── SKILL.md                   # CI 验证
│   │   ├── deploy-validation/
│   │   │   ├── SKILL.md                   # 部署验证
│   │   │   └── rollback-sop.md            # 回滚 SOP
│   │   ├── doc-management/
│   │   │   └── SKILL.md                   # 文档管理
│   │   ├── knowledge-qa/
│   │   │   └── SKILL.md                   # 知识问答
│   │   ├── performance/
│   │   │   └── profiling.md               # 性能剖析
│   │   ├── security/
│   │   │   └── audit.md                   # 安全审计
│   │   ├── refactor/
│   │   │   └── SKILL.md                   # 重构
│   │   ├── migration/
│   │   │   └── SKILL.md                   # 迁移
│   │   ├── api-versioning/
│   │   │   └── SKILL.md                   # API 版本
│   │   └── db-migration/
│   │       └── SKILL.md                   # 数据库迁移
│   │
│   ├── wiki/                              # 知识库
│   │   ├── README.md                      # Wiki 索引
│   │   ├── glossary.md                    # 术语
│   │   ├── data-model.md                  # 数据模型
│   │   ├── business-flows.md              # 业务流程
│   │   ├── monitoring.md                  # 监控指标
│   │   ├── rollback-playbook.md           # 回滚手册
│   │   ├── onboarding.md                  # 新人上手
│   │   └── faq.md                         # 业务 FAQ
│   │
│   ├── templates/                         # 通用模板
│   │   ├── incident.md                    # 事故
│   │   ├── postmortem.md                  # 复盘
│   │   ├── design-doc.md                  # 设计文档
│   │   ├── rfc.md                         # RFC
│   │   └── runbook.md                     # Runbook
│   │
│   ├── changes/                           # 变更管理
│   │   ├── README.md                      # 变更索引
│   │   └── _template/
│   │       ├── README.md                  # 模板说明
│   │       ├── requirement-analysis.md    # 需求分析
│   │       ├── task-breakdown.md          # 任务拆分
│   │       ├── coding-report.md           # 编码报告
│   │       ├── review-record-v1.md        # 评审记录
│   │       ├── unit-test-report.md        # 单测报告
│   │       ├── ci-result.md               # CI 结果
│   │       └── deploy-validation.md       # 部署验证
│   │
│   ├── pipeline/                          # 流水线
│   │   ├── stages.md                      # 十阶段
│   │   ├── human-checkpoints.md           # 五个人工确认点
│   │   ├── escalation.md                  # 升级上报
│   │   ├── hotfix-process.md              # 热修
│   │   ├── release-process.md             # 发布
│   │   └── rollback-process.md            # 回滚
│   │
│   ├── metrics/                           # 度量
│   │   ├── metrics.md                     # 指标
│   │   ├── dashboard.md                   # 看板
│   │   ├── collection.md                  # 采集
│   │   ├── badges.md                      # 徽章
│   │   └── sla.md                         # SLA
│   │
│   ├── iteration/                         # 迭代
│   │   ├── README.md                      # Patch 说明
│   │   ├── patch-log.md                   # Patch 记录
│   │   └── retrospective.md               # 复盘
│   │
│   ├── sources/                           # 来源池
│   │   ├── README.md                      # 来源说明
│   │   ├── incidents/                     # 事故
│   │   ├── reviews/                       # Review
│   │   ├── architecture/                  # 架构
│   │   ├── ddl/                           # DDL
│   │   ├── api/                           # 接口
│   │   ├── flows/                         # 流程
│   │   └── code/                          # 代码
│   │
│   ├── agents/                            # Agent 角色(定义 + 填充,同一目录)
│   │   ├── README.md                      # Agent 索引
│   │   ├── orchestrator.md                # 编排
│   │   ├── fill-harness.md                # 填充总纲
│   │   ├── orchestrator-report.md         # 编排报告
│   │   ├── application-owner.md           # 编排主角色
│   │   ├── application-owner-python.md    # Python 扩展
│   │   ├── architecture-agent.md          # 架构解析
│   │   ├── incident-agent.md              # 事故反推
│   │   ├── review-agent.md                # Review 提炼
│   │   ├── code-archaeology-agent.md      # 代码考古
│   │   ├── data-modeling-agent.md         # 数据建模
│   │   ├── gate-agent.md                  # 门禁解析
│   │   ├── security-agent.md              # 安全
│   │   ├── performance-agent.md           # 性能
│   │   ├── refactor-agent.md              # 重构
│   │   ├── dependency-agent.md            # 依赖
│   │   └── doc-agent.md                   # 文档
│   │
│   ├── glossary/                          # 领域术语索引
│   │   └── README.md
│   │
│   ├── pilot/                             # 空跑与试点
│   │   ├── runbook.md                     # 空跑手册
│   │   └── findings.md                    # 空跑发现
│   │
│   ├── state/                             # 需求状态
│   │   ├── README.md
│   │   └── stages.json                    # 十阶段门配置(阶段 → 产出物)
│   │
│   ├── audit/                             # 审计
│   │   └── README.md
│   │
│   ├── checkpoints/                       # 确认点
│   │   └── README.md
│   │
│   └── schemas/                           # Schema
│       ├── rule-schema.json
│       ├── skill-schema.json
│       └── data/                          # 数据文件(填充时创建;不存在时门禁会显式标注未实现)
│
├── scripts/                               # 检查脚本
│   ├── check_pytest_report.py             # 测试报告检查
│   ├── check_python_rules.py              # Python 规则检查
│   ├── check_harness_docs.py              # Harness 文件检查
│   ├── check_layers.py                    # 分层检查
│   ├── check_commit_msg.py                # 提交信息检查
│   ├── check_secrets.py                   # 密钥扫描
│   ├── check_complexity.py                # 复杂度检查
│   ├── check_dependencies.py              # 依赖检查
│   ├── check_i18n.py                      # 国际化检查
│   ├── collect_metrics.py                 # 度量采集
│   ├── audit_log.py                       # 审计记录
│   ├── state_tracker.py                   # 状态跟踪(已弃用,转发到 stage_gate)
│   ├── stage_gate.py                      # 阶段状态机(前置校验 + resume)
│   ├── validate_schemas.py                # Schema 校验
│   ├── check-gates.sh                     # 阶段产出物门(增量 --stage)
│   ├── install-hooks.sh                   # 安装钩子
│   └── dev-setup.sh                       # 开发环境
│
├── src/                                   # 业务代码（待填）
│   └── __init__.py
│
└── tests/                                 # 测试
    ├── README.md                          # 测试说明
    ├── conftest.py                        # 公共 fixture
    ├── test_smoke.py                      # 冒烟测试
    └── test_scripts.py                    # 脚本测试
```

---

## 七、核心组件详解

### 1. 规则体系（`harness/rules/`）

**作用**：告诉 Agent 什么是"标准"，是不随需求变化的稳定约束。

**特点**：

- 不在代码里，但所有资深开发者都知道；
- 以前靠口头传承，现在写成文件；
- 每条规则背后都有一个真实踩过的坑。

**规则六件套**：

| 字段 | 说明                   |
| ---- | ---------------------- |
| 规则 | 一句话描述             |
| 原因 | 来源事故/Review/文档   |
| 反例 | 错误代码               |
| 正例 | 正确代码               |
| 检查 | 可执行脚本或 lint 规则 |
| 测试 | 可失败、可通过的测试   |

### 2. 技能体系（`harness/skills/`）

**作用**：把每个阶段的最佳实践变成结构化 SOP。

**核心 Skill**：

| Skill             | 作用                   |
| ----------------- | ---------------------- |
| Coding            | 按分层规范一层一层实现 |
| Expert Reviewer   | 独立评审计划与执行     |
| UnitTest          | 改动驱动测试           |
| Request Analysis  | 需求分析               |
| Task Breakdown    | 任务拆分               |
| CI Validation     | CI 验证                |
| Deploy Validation | 部署验证               |
| Doc Management    | 文档管理               |
| Knowledge QA      | 知识问答               |

**评审 Skill 的关键设计**：

每条评审意见必须包含：

- 问题描述
- 修改建议
- 优先级分级（P0/P1/P2）

### 3. 知识库（`harness/wiki/`）

**作用**：Agent 理解业务上下文的素材。

**特点**：

- **不主动全量加载**；
- Agent 根据任务需要自主查阅；
- 核心是"按需获取"。

**内容**：

- 领域术语
- 数据模型
- 核心业务流程
- 监控指标
- 回滚手册
- 新人上手
- 业务 FAQ

### 4. 变更管理（`harness/changes/`）

**作用**：每个需求独立目录，全流程留痕。

**目录结构**：

```text
harness/changes/REQ-XXXX/
├── requirement-analysis.md
├── task-breakdown.md
├── coding-report.md
├── review-record-v1.md
├── review-record-v2.md     # 版本递增
├── unit-test-report.md
├── ci-result.md
└── deploy-validation.md
```

**特点**：

- 评审文件用版本递增；
- 旧版本永远不删；
- 全流程可追溯。

### 5. Agent 角色（`harness/agents/`）

> 角色定义（`application-owner*.md`）与填充 Agent（`*-agent.md`、`orchestrator.md`、
> `fill-harness.md`，共 14 个）**同在一个目录**；索引见 `harness/agents/README.md`。

**Application Owner**：整套体系的编排中枢，约 400 行，包含 5 个模块：

| 模块               | 内容                                                                 |
| ------------------ | -------------------------------------------------------------------- |
| 角色和项目背景     | 20-30 行，刚好够用的项目视野                                         |
| 配置中枢索引       | Rules、Skills、Wiki、MCP 的路径、职责、触发场景                      |
| 七项核心职责       | 需求理解、任务拆解、任务分发、任务验收、质量把关、文档管理、知识问答 |
| 工作流程调度指令   | 十阶段完整调度逻辑                                                   |
| 沟通原则和硬性约束 | 必须做/禁止做两张清单                                                |

### 6. 流水线（`harness/pipeline/`）

**十阶段**：

1. 需求分析
2. 需求评审
3. 计划评审
4. 编码实现
5. 编码评审
6. 单测编写
7. 单测评审
8. CI 验证
9. 部署验证
10. 用户确认

**每阶段三要素**：

- 触发条件
- Skill 加载
- 质量门禁

**回退路径**：

| 失败              | 回退目标 |
| ----------------- | -------- |
| CI 失败但测试为 0 | 单测编写 |
| 编译错误          | 编码实现 |
| 需求不符          | 需求分析 |
| 评审超限          | 升级人工 |

**评审循环上限**：

- 需求评审：最多 3 轮
- 编码评审：最多 2 轮
- 单测评审：最多 2 轮

### 7. 质量门禁（`scripts/` + CI）

**可程序化验证条件**：

| 门禁        | 命令                     | 通过条件                        |
| ----------- | ------------------------ | ------------------------------- |
| Lint        | `ruff check .`           | exit 0                          |
| Format      | `ruff format --check .`  | exit 0                          |
| Type        | `mypy src`               | exit 0                          |
| Test        | `pytest --json-report`   | exit 0                          |
| Test Report | `check_pytest_report.py` | `TotalTest>0` 且 `Passed=Total` |
| Rules       | `check_python_rules.py`  | 无输出                          |
| Layers      | `check_layers.py`        | 无输出                          |
| Secrets     | `check_secrets.py`       | 无输出                          |
| Complexity  | `check_complexity.py`    | 无输出                          |
| i18n        | `check_i18n.py`          | 无输出                          |
| Docs        | `check_harness_docs.py`  | 无缺失                          |
| Schema      | `validate_schemas.py`    | 无错误                          |
| Bandit      | `bandit -r src -q`       | exit 0                          |

### 8. 填充 Agent（`harness/agents/`）

**作用**：从真实来源提取规则，填充 Harness。

| Agent            | 输入                | 输出       |
| ---------------- | ------------------- | ---------- |
| Orchestrator     | 全部                | 调度       |
| Architecture     | architecture/、src/ | 分层规则   |
| Incident         | incidents/          | 硬约束规则 |
| Review           | reviews/            | 编码规范   |
| Code Archaeology | src/                | 模板与反例 |
| Data Modeling    | ddl/、api/、flows/  | Wiki       |
| Gate             | CI、Makefile        | 门禁清单   |
| Security         | 安全审计            | 安全规则   |
| Performance      | 性能事故            | 性能规则   |
| Refactor         | src/                | 重构规则   |
| Dependency       | pyproject.toml      | 依赖规则   |
| Doc              | src/、changes/      | 文档       |

**三道防编造闸**：

1. **来源强制**：每条规则必须有来源，来源为空则拒绝；
2. **可执行强制**：每条规则必须有检查命令，跑不通则拒绝；
3. **测试强制**：每条 P0 规则必须有测试，测试必须能失败也能通过。

---

## 八、十阶段开发流水线

| 阶段         | 触发     | Skill             | 产出         | 门禁                                      | 回退     | 人工确认         |
| ------------ | -------- | ----------------- | ------------ | ----------------------------------------- | -------- | ---------------- |
| 1. 需求分析  | 新需求   | request-analysis  | 需求分析文档 | 边界清晰                                  | -        | 需求待决议确认   |
| 2. 需求评审  | 分析完成 | expert-reviewer   | 评审记录     | 意见完整                                  | 需求分析 | 需求待决议确认   |
| 3. 计划评审  | 拆分完成 | expert-reviewer   | 计划评审     | 可执行                                    | 任务拆解 | 计划评审后确认   |
| 4. 编码实现  | 计划确认 | coding            | 代码、报告   | 编译通过                                  | 编码实现 | -                |
| 5. 编码评审  | 编码完成 | expert-reviewer   | 评审记录     | 问题分级                                  | 编码实现 | 编码评审后确认   |
| 6. 单测编写  | 编码通过 | unit-test         | 单测、报告   | 用例>0                                    | 单测编写 | -                |
| 7. 单测评审  | 单测完成 | expert-reviewer   | 评审记录     | 断言完整                                  | 单测编写 | -                |
| 8. CI 验证   | 单测通过 | ci-validation     | CI 结果      | Status=SUCCESS, TotalTest>0, Passed=Total | 单测编写 | -                |
| 9. 部署验证  | CI 通过  | deploy-validation | 部署报告     | 参数正确                                  | 参数确认 | 部署环境参数确认 |
| 10. 用户确认 | 部署通过 | doc-management    | 交付确认     | 用户通过                                  | 需求分析 | 最终交付确认     |

### 五个人工确认点

| 编号 | 名称             | 时机         | 决策内容           |
| ---- | ---------------- | ------------ | ------------------ |
| HC-1 | 需求待决议确认   | 需求评审后   | 边界、验收、优先级 |
| HC-2 | 计划评审后确认   | 计划评审后   | 任务、依赖、风险   |
| HC-3 | 编码评审后确认   | 编码评审后   | 代码质量、业务逻辑 |
| HC-4 | 部署环境参数确认 | 部署前       | 环境、配置、参数   |
| HC-5 | 最终交付确认     | 用户确认阶段 | 是否满足需求       |

---

## 九、快速开始

### 前置条件

- Python 3.11+
- Git
- Make
- （可选）Docker

### 安装

```bash
# 1. 克隆
git clone <repo-url>
cd ai-delivery-harness-engineering

# 2. 一键初始化（推荐）
bash scripts/dev-setup.sh

# 或手动
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install --upgrade pip
pip install -e ".[dev]"

# 3. 安装钩子
pre-commit install
pre-commit install --hook-type commit-msg
git config commit.template .gitmessage
```

### 跑门禁

```bash
make gate
```

等价于：

```bash
ruff check .
ruff format --check .
mypy src
pytest --json-report --json-report-file=pytest-report.json
python scripts/check_pytest_report.py pytest-report.json
python scripts/check_python_rules.py src
python scripts/check_layers.py src
python scripts/check_complexity.py src
python scripts/check_i18n.py src
python scripts/check_secrets.py .
python scripts/check_harness_docs.py
python scripts/validate_schemas.py
```

### Docker 运行

```bash
docker compose up harness
```

---

## 十、完整使用方法

### 场景一：作为独立范本使用

你想把这套 Harness 作为团队的方法论范本。

**步骤**：

1. Fork 或克隆本仓库；
2. 阅读 `docs/architecture.md` 理解整体架构；
3. 阅读 `harness/pipeline/stages.md` 理解十阶段流水线；
4. 阅读 `harness/agents/application-owner.md` 理解编排逻辑；
5. 按 `docs/fill-guide.md` 用 Agent 填充具体项目内容；
6. 团队按十阶段流水线执行。

### 场景二：引入到已有 Python 项目

**步骤**：

```bash
# 1. 在已有项目中
cd your-existing-project

# 2. 把 harness 目录复制过去
cp -r /path/to/ai-delivery-harness-engineering/harness ./harness
cp -r /path/to/ai-delivery-harness-engineering/scripts ./scripts
cp /path/to/ai-delivery-harness-engineering/.pre-commit-config.yaml .
cp /path/to/ai-delivery-harness-engineering/Makefile .

# 3. 合并 pyproject.toml 的 dev 依赖

# 4. 安装
pip install -e ".[dev]"
pre-commit install

# 5. 跑门禁
make gate
```

**注意**：如果已有 CI，把 `.github/workflows/harness-ci.yml` 合并到现有 CI。

### 场景三：填充 Harness

**步骤**：

```bash
# 1. 建来源池
mkdir -p harness/sources/{incidents,reviews,architecture,ddl,api,flows,code}

# 2. 放入真实资料（全部脱敏）
# - 事故报告 → incidents/
# - Review 意见 → reviews/
# - 架构文档 → architecture/
# - DDL → ddl/
# - 接口文档 → api/
# - 流程图 → flows/
# - 代码库 → 直接指向 src/

# 3. 按顺序跑 Agent（每个独立分支 + PR）
# Agent 1：架构解析
# Agent 2：事故反推
# Agent 3：Review 提炼
# Agent 4：代码考古
# Agent 5：数据建模
# Agent 6：门禁解析

# 4. 每个 Agent 输出人工审核
# 5. 合并回填
# 6. 更新检查脚本和测试
# 7. 提交
```

### 场景四：执行一个需求

**步骤**：

```bash
# 1. 创建分支
git checkout -b feature/req-0001

# 2. 创建需求目录
mkdir -p harness/changes/REQ-0001
cp harness/changes/_template/*.md harness/changes/REQ-0001/

# 3. 填写需求分析
vim harness/changes/REQ-0001/requirement-analysis.md

# 4. 需求评审
# 加载 Expert Reviewer，评审，最多 3 轮
# HC-1 人工确认

# 5. 任务拆分
vim harness/changes/REQ-0001/task-breakdown.md

# 6. 计划评审
# 加载 Expert Reviewer，评审，最多 3 轮
# HC-2 人工确认

# 7. 编码实现
# 加载 Coding Skill，按分层规范实现

# 8. 编码评审
# 加载 Expert Reviewer，评审，最多 2 轮
# HC-3 人工确认

# 9. 单测编写
# 加载 UnitTest Skill，改动驱动测试

# 10. 单测评审
# 加载 Expert Reviewer，评审，最多 2 轮

# 11. CI 验证
make gate

# 12. 部署验证
# HC-4 环境参数确认
# 部署后验证关键路径

# 13. 用户确认
# HC-5 最终交付确认

# 14. 提交
git add harness/changes/REQ-0001
git commit -m "docs: add req-0001"
git push -u origin feature/req-0001
gh pr create --title "REQ-0001" --body "按 Harness 十阶段流程执行"
```

### 场景五：空跑验证

**目标**：用真实需求之前，先空跑一次，发现体系缺陷。

```bash
# 1. 建空跑需求
mkdir -p harness/changes/REQ-0000
cp harness/changes/_template/*.md harness/changes/REQ-0000/

# 2. 走完整十阶段
# 3. 记录每个阶段的缺陷

# 4. 空跑常见缺陷
# - CI 门禁只检查状态码，忽略测试数为 0
# - 简单需求下评审报告不生成文件
# - 摘要文件出现重复行
# - 部署参数被 Agent 错误推测

# 5. 记录到 harness/pilot/findings.md
# 6. 每个缺陷 Patch 回 Harness
```

### 场景六：热修

```bash
git checkout -b hotfix/fix-payment-timeout
# 最小改动
# 必须新增测试
# 必须新增事故规则
# 双人 Review
# CI 通过
# 部署验证
# 记录到 harness/changes/HOTFIX-XXXX/
```

### 场景七：发布

```bash
# 发布前检查
- [ ] 所有需求 CI 通过
- [ ] 所有人工确认点完成
- [ ] 回归测试通过
- [ ] 监控就绪
- [ ] 回滚方案就绪

# 打 tag
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0

# 部署 staging → 验证 → 部署 prod → 监控
```

### 场景八：回滚

```bash
# 触发
# - 关键路径不通
# - 监控异常
# - 数据异常

# 步骤
# 1. 决策人确认
# 2. 执行回滚命令
# 3. 验证主链路
# 4. 验证国际化链路
# 5. 验证数据一致性
# 6. 监控观察
# 7. 记录到 patch-log.md
# 8. 复盘
```

---

## 十一、填充指南

### 填充公式

```text
真实来源 + 结构化 Prompt + 六件套输出 + 人工审核 + 可执行检查 = 厚实规则
```

### 六个核心填充 Agent

#### Agent 1：架构解析

**输入**：

- `harness/sources/architecture/`
- `src/`

**步骤**：

1. 扫描 `src/` 下所有包和模块；
2. 统计每个模块被谁 import；
3. 推断分层；
4. 找出违反分层方向的 import；
5. 生成分层规则。

**输出**：`harness/sources/architecture/extracted-rules.md`

#### Agent 2：事故反推

**输入**：`harness/sources/incidents/`

**对每条事故回答**：

1. 能不能用一条规则拦住？
2. 能不能程序化验证？
3. 属于哪个文件？
4. 反例是什么？
5. 正例是什么？
6. 配什么测试？

**输出**：六件套规则 → `harness/sources/incidents/extracted-rules.md`

#### Agent 3：Review 提炼

**输入**：`harness/sources/reviews/`

**输出**：

- 重复 3 次以上：六件套规则；
- 只出现 1 次：观察池。

#### Agent 4：代码考古

**输入**：`src/`

**输出**：

- 每层最佳实践 3 个；
- 每层反例 3 个；
- 模板与规则。

#### Agent 5：数据建模

**输入**：`ddl/`、`api/`、`flows/`

**输出**：

- `wiki/data-model.md`
- `wiki/business-flows.md`

#### Agent 6：门禁解析

**输入**：CI 配置、`Makefile`

**输出**：可程序化门禁清单。

### 三道防编造闸

1. **来源强制**：来源为空 → 拒绝；
2. **可执行强制**：检查命令跑不通 → 拒绝；
3. **测试强制**：P0 规则无测试 → 拒绝。

### 人工审核清单

- [ ] 每条规则有来源；
- [ ] 来源可查；
- [ ] 反例能跑出问题；
- [ ] 正例能通过检查；
- [ ] 检查脚本能拦；
- [ ] 测试能失败也能通过；
- [ ] 优先级合理；
- [ ] Owner 明确。

---

## 十二、CI 与门禁

### 主 CI 工作流

`.github/workflows/harness-ci.yml`：

1. Ruff lint；
2. Ruff format；
3. Mypy；
4. Pytest；
5. Test report 检查；
6. Python 规则检查；
7. 分层检查；
8. 复杂度检查；
9. i18n 检查；
10. 密钥扫描；
11. Harness 文件检查；
12. Schema 校验；
13. Bandit；
14. pip-audit。

### 提交信息检查

`.github/workflows/harness-ci.yml` 第二个 job：

```bash
for sha in $(git rev-list "$base..$head"); do
  git log -1 --format=%s "$sha" > /tmp/msg.txt
  python scripts/check_commit_msg.py /tmp/msg.txt
done
```

### 提交信息格式

```text
<type>: <subject>
```

**type**：

- `feat`：新功能
- `fix`：修复
- `docs`：文档
- `ci`：CI
- `chore`：杂项
- `rule`：规则
- `agent`：Agent
- `test`：测试

**示例**：

```text
rule: add PAY-001 from INC-2024-0421

支付回调必须设置 timeout，超时后标记 pending。

Source: harness/sources/incidents/INC-2024-0421.md
```

---

## 十三、度量指标

### 核心指标

| 指标               | 目标  |
| ------------------ | ----- |
| 项目维度 AI 代码率 | 90%   |
| 个人维度 AI 代码率 | 85%   |
| 返工轮次           | <=1   |
| 人工确认轮次       | 1     |
| 质量门禁通过率     | 100%  |
| 测试覆盖率         | >=80% |

### 质量指标

| 指标               | 目标 |
| ------------------ | ---- |
| 金额 float 违规    | 0    |
| 外部调用无 timeout | 0    |
| 裸 except          | 0    |
| print 残留         | 0    |
| 硬编码配置         | 0    |
| 无测试接口         | 0    |

### 流程指标

| 指标             | 目标     |
| ---------------- | -------- |
| 需求评审轮次     | <=3      |
| 编码评审轮次     | <=2      |
| 单测评审轮次     | <=2      |
| 评审升级人工次数 | 越少越好 |

### 知识沉淀指标

| 指标           | 目标     |
| -------------- | -------- |
| 规则条数       | 持续增长 |
| 规则来源覆盖率 | 100%     |
| 规则可程序化率 | 100%     |
| 规则测试覆盖率 | 100%     |

### 度量频率

- 每周：AI 代码率、返工轮次、门禁通过率；
- 每月：规则条数、来源覆盖率、知识沉淀；
- 每季度：整体复盘。

---

## 十四、关键经验

### 经验一：真实需求使用前，先空跑全流程

团队在空跑中发现 4 个缺陷：

1. CI 门禁只检查状态码，忽略测试用例数为 0 的异常；
2. 简单需求下评审报告不生成文件；
3. 摘要文件因 Agent 的追加倾向出现重复行；
4. 部署参数被 Agent 错误推测。

这些问题如果在真实需求中才暴露，每一个都会导致严重返工。

### 经验二：质量文件必须可程序化验证

OpenAI 百万行代码项目的核心经验：

> **如果一个约束不能被机械化执行，Agent 就会偏离。**

"检查 CI 是否通过"这种自然语言描述不够。Agent 可能认为状态 Success 即通过，却忽略测试用例数为 0。

改成三个可程序化验证的条件：

- `Status = SUCCESS`
- `TotalTest > 0`
- `Passed = Total`

问题彻底消除。

> **一切不可被机器验证的约束，在 Agent 执行中都是无效约束。**

### 经验三：流程一致性优先于流程效率

一个仅涉及两个文件、六行代码的小需求，依然走完整十阶段流程，一轮评审即通过。

好的流程不应该给简单任务增加显著负担。当需求足够简单时，每个阶段执行时间自然缩短，但流程一致性保证不会因为"这次改动很小"就跳过关键环节。

> **在企業級系統中，小改動大事故的案例不勝枚舉。**

### 经验四：规范是活文档，需要持续迭代

每次实战发现新问题，都立即 Patch 到 Harness。

> **规范的每一行都对应一个历史失败案例。**

当你觉得某条规则多余或啰嗦时，往往是它背后有一个真实踩过的坑。

### 经验五：执行与评判必须分离

评审 Agent 不需要更聪明，它只需要用一套不同于编码 Agent 的检查视角来审视产出物。

实践中，评审 Agent 曾：

- 发现编码 Agent 遗漏的渠道判断逻辑，一个潜在线上故障；
- 检测到 Agent 试图跳过评审阶段，并强制回退。

---

## 十五、常见问题

### Q1：为什么骨架这么"薄"？

**A**：骨架是脚手架，厚度来自项目实战。一条厚规则长这样：

```text
价格字段必须用 Long，单位分。
原因：2024-03 订单模块用 Double 计算优惠，
      0.1 + 0.2 = 0.30000000000000004，
      对账差异 37 万，事故编号 INC-2024-0312。
反例：OrderService.calcDiscount()
正例：PriceUtil.add()
检查：scripts/check_python_rules.py 第 42 行
测试：tests/pricing/test_discount.py::test_float_precision
```

没有历史，规则就是空的。

### Q2：规则从哪来？

**A**：事故报告、Code Review、架构文档、DDL、接口文档、代码库、CI 配置、线上监控。

### Q3：Agent 会编吗？

**A**：会。所以有三道闸：来源强制、可执行强制、测试强制。

### Q4：没有事故怎么办？

**A**：从 Review 和架构反推。Code Review 意见重复 3 次以上即可写成规则。

### Q5：规则太多怎么办？

**A**：按 P0/P1/P2 分级。P0 是硬约束（阻塞上线），P1 是本轮修完，P2 是后续优化。

### Q6：CI 必须通过吗？

**A**：是。CI 不通过不能合并。

### Q7：Agent 能直接改 main 吗？

**A**：不能。必须走 PR。

### Q8：怎么开始？

**A**：

1. 跑 `bash scripts/dev-setup.sh`；
2. 阅读 `docs/quickstart.md`；
3. 阅读 `docs/fill-guide.md`；
4. 按顺序跑 6 个填充 Agent；
5. 空跑 REQ-0000；
6. 执行第一个真实需求。

### Q9：骨架和项目怎么结合？

**A**：见 `docs/fill-guide.md`。核心是把真实来源放进 `harness/sources/`，用 Agent 提取规则，人工审核后回填。

### Q10：能用于非 Python 项目吗？

**A**：可以，但需要替换 Python 相关规则、脚本和 CI。骨架结构本身与语言无关。

---

## 十六、贡献指南

见 `CONTRIBUTING.md`。

### 分支规范

| 分支           | 用途       |
| -------------- | ---------- |
| main           | 稳定分支   |
| feature/<name> | 功能开发   |
| agent/<name>   | Agent 填充 |
| fix/<name>     | 修复       |
| docs/<name>    | 文档       |
| rule/<id>      | 规则       |
| hotfix/<name>  | 热修       |

### 提交规范

```text
<type>: <subject>

<body>

<footer>
```

### 规则贡献

每条规则必须包含六件套：

1. 规则
2. 原因
3. 反例
4. 正例
5. 检查
6. 测试

来源为空则拒绝。

### 禁止

- 禁止提交密钥、真实数据、生产配置；
- 禁止无来源规则；
- 禁止跳过 CI；
- 禁止 Agent 直接改 main。

---

## 十七、版本与路线图

### 当前版本

**v0.1.0-skeleton**：骨架冻结版

- 170+ 文件；
- 覆盖规则、技能、知识库、变更、Agent、流水线、门禁、度量、迭代；
- CI 可运行；
- 可用 Agent 填充。

### 路线图

#### 阶段 0：骨架（已完成）

- [x] 目录结构
- [x] 规则模板
- [x] 技能模板
- [x] Agent 定义
- [x] CI 骨架
- [x] 文档

#### 阶段 1：填充（进行中）

- [ ] 架构解析
- [ ] 事故反推
- [ ] Review 提炼
- [ ] 代码考古
- [ ] 数据建模
- [ ] 门禁解析

#### 阶段 2：试点

- [ ] 空跑 REQ-0000
- [ ] 修复缺陷
- [ ] 真实需求试点
- [ ] 度量采集

#### 阶段 3：推广

- [ ] 多需求常态化
- [ ] 多团队使用
- [ ] 度量看板
- [ ] 复盘

#### 阶段 4：优化

- [ ] 规则持续 Patch
- [ ] Agent 持续优化
- [ ] 流程持续优化
- [ ] 知识持续沉淀

#### 阶段 5：扩展

- [ ] 多项目支持
- [ ] 多语言支持
- [ ] 多 Agent 协作
- [ ] 自动化升级

### 版本策略

- **MAJOR**：不兼容变更
- **MINOR**：新增功能
- **PATCH**：修复

---

## 十八、许可证

MIT，见 [LICENSE](./LICENSE)。

---

## 附录：快速导航

| 我想...        | 去看                                 |
| -------------- | ------------------------------------ |
| 快速上手       | `docs/quickstart.md`                 |
| 填充 Harness   | `docs/fill-guide.md`                 |
| 理解架构       | `docs/architecture.md`               |
| 看十阶段       | `harness/pipeline/stages.md`         |
| 看 Agent 定义  | `harness/agents/application-owner.md` |
| 写第一条规则   | `harness/rules/_template.md`         |
| 写第一个 Skill | `harness/skills/_template/SKILL.md`  |
| 跑 Agent 填充  | `harness/agents/README.md`           |
| 看反模式       | `docs/anti-patterns.md`              |
| 看最佳实践     | `docs/best-practices.md`             |
| 看术语         | `docs/glossary.md`                   |
| 提 Issue       | `.github/ISSUE_TEMPLATE/`            |
| 提 PR          | `.github/PULL_REQUEST_TEMPLATE.md`   |

---

> **Harness 的价值不在于让 Agent 变得更聪明，而在于让 Agent 的错误变得可控、可发现、可修复。**
>
> **这和传统软件质量保障思路一脉相承：我们不指望程序员写出零缺陷代码，而是通过 Code Review、Unit Testing、CI/CD 来确保缺陷被层层拦截。Harness 做的事情本质上完全一样，只不过拦截对象从程序员变成了 Agent。**
