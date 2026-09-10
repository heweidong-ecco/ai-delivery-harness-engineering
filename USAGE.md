# 骨架使用指南

> 本文档说明如何把本仓库当作 kit 使用：复制、改名、填充、上线。
>
> 如果你只是阅读，先看 `README.md`。如果你要动手用，看本文档。

---

## 目录

- [一、这个 kit 是什么](#一这个-kit-是什么)
- [二、这个 kit 能做什么](#二这个-kit-能做什么)
- [三、这个 kit 不能做什么](#三这个-kit-不能做什么)
- [四、三种使用方式](#四三种使用方式)
- [五、复制前准备](#五复制前准备)
- [六、复制步骤](#六复制步骤)
- [七、复制后必须修改的内容](#七复制后必须修改的内容)
- [八、复制后建议保留的内容](#八复制后建议保留的内容)
- [九、复制后建议删除的内容](#九复制后建议删除的内容)
- [十、环境准备](#十环境准备)
- [十一、首次验证](#十一首次验证)
- [十二、常见场景](#十二常见场景)
- [十三、目录速查](#十三目录速查)
- [十四、FAQ](#十四faq)
- [十五、下一步](#十五下一步)

---

## 一、这个 kit 是什么

这是一个**不依赖具体项目的 AI 代码交付骨架**。

它提供：

- 目录结构；
- 规则模板；
- 技能模板；
- 知识库模板；
- 变更管理模板；
- Agent 角色定义；
- 十阶段流水线；
- 质量门禁脚本；
- CI 配置；
- 填充 Agent（14 个）；
- 度量与迭代机制。

它**不是一个可以直接跑业务的项目**，而是一个**容器**：你把项目信息、事故、Review、架构、DDL 灌进去，它就能约束 AI 生成可上线的代码。

---

## 二、这个 kit 能做什么

| 能力             | 说明                               |
| ---------------- | ---------------------------------- |
| 约束 AI 编码     | 通过规则 + 技能 + 门禁             |
| 让 AI 代码可上线 | 通过十阶段流水线                   |
| 防止 AI 编造     | 通过来源强制、可执行强制、测试强制 |
| 让错误可控       | 通过可程序化验证 + 回退路径        |
| 让决策可控       | 通过五个人工确认点                 |
| 让知识沉淀       | 通过变更目录 + Patch 记录          |
| 让规则变厚       | 通过 14 个填充 Agent               |
| 让度量可见       | 通过度量指标 + 看板                |

---

## 三、这个 kit 不能做什么

| 不能做         | 说明                        |
| -------------- | --------------------------- |
| 替代模型能力   | 它不换模型，只加约束        |
| 自动懂你的业务 | 需要你提供真实来源          |
| 无来源生成规则 | 三道闸会拒绝                |
| 保证零缺陷     | 它保证缺陷被拦截            |
| 跨语言开箱即用 | 默认 Python，其他语言需替换 |
| 替代人工决策   | 五个人工确认点必须人工      |

---

## 四、三种使用方式

### 方式 A：Fork 后作为独立范本

**适用**：你想把骨架作为团队方法论范本，不绑定具体项目。

```bash
# 1. Fork 本仓库
# 2. 克隆到本地
git clone <your-fork>
cd <your-fork>

# 3. 修改 README、LICENSE、CODEOWNERS
# 4. 保留全部内容
# 5. 作为范本维护
```

**适合**：架构组、流程组、平台组。

### 方式 B：复制到已有项目

**适用**：你有一个已有 Python 项目，想引入 Harness。

```bash
# 1. 在已有项目中
cd your-existing-project

# 2. 复制核心目录
cp -r /path/to/kit/harness ./harness
cp -r /path/to/kit/scripts ./scripts
cp -r /path/to/kit/tests ./tests  # 可选，如已有测试则合并
cp -r /path/to/kit/docs ./docs    # 可选
cp -r /path/to/kit/config ./config
cp -r /path/to/kit/.github ./.github  # 合并，不覆盖

# 3. 复制根文件
cp /path/to/kit/.pre-commit-config.yaml .
cp /path/to/kit/.coveragerc .
cp /path/to/kit/.bandit .
cp /path/to/kit/.importlinter .
cp /path/to/kit/Makefile .         # 合并
cp /path/to/kit/pyproject.toml .   # 合并

# 4. 合并依赖
# 把 [project.optional-dependencies].dev 合并到你的 pyproject.toml

# 5. 安装
bash scripts/dev-setup.sh

# 6. 跑门禁
make gate
```

**注意**：不要覆盖已有 `Makefile`、`pyproject.toml`、`.github/`，要合并。

### 方式 C：复制出去作为独立仓库

**适用**：你想把骨架复制成一个新仓库，专门用于某个项目。

```bash
# 1. 复制
cp -r /path/to/kit ./my-project-harness
cd my-project-harness

# 2. 重新初始化 git
rm -rf .git
git init -b main

# 3. 创建新 GitHub 仓库
gh repo create my-project-harness \
  --private \
  --description "My project Harness" \
  --source=. \
  --remote=origin

# 4. 改 README、LICENSE、CODEOWNERS
# 5. 提交
git add .
git commit -m "chore: init harness from kit"
git push -u origin main
```

**适合**：一个项目一个 Harness 仓库，独立演进。

---

## 五、复制前准备

### 必须准备

| 项               | 说明                        |
| ---------------- | --------------------------- |
| Python 3.11+     | 运行环境                    |
| Git              | 版本控制                    |
| Make             | 命令执行                    |
| GitHub 账号      | 托管                        |
| 项目架构图       | 填充 `project-structure.md` |
| 事故报告         | 填充 `coding-standard.md`   |
| Code Review 意见 | 填充 `coding-standard.md`   |
| 编码规范         | 填充 `coding-standard.md`   |
| 分层规范         | 填充 `python-layers.md`     |
| CI/CD 配置       | 填充 `dev-process.md`       |

### 建议准备

| 项           | 说明                        |
| ------------ | --------------------------- |
| DDL          | 填充 `data-model.md`        |
| 接口文档     | 填充 `business-flows.md`    |
| 业务流程图   | 填充 `business-flows.md`    |
| 监控配置     | 填充 `monitoring.md`        |
| 运维手册     | 填充 `rollback-playbook.md` |
| 脱敏线上请求 | 用于单测                    |

### 脱敏要求

**所有来源必须脱敏**：

- 手机号：保留前 3 后 4；
- 身份证：保留前 6 后 4；
- 银行卡：保留后 4；
- 邮箱：保留首字母 + 域名；
- 姓名：保留姓；
- 密钥：删除或替换。

---

## 六、复制步骤

### 步骤 1：选择使用方式

- A：Fork；
- B：复制到已有项目；
- C：复制出去独立仓库。

### 步骤 2：复制核心目录

```bash
# 最小集合
cp -r kit/harness ./
cp -r kit/scripts ./
cp kit/.pre-commit-config.yaml .
cp kit/.coveragerc .
cp kit/.bandit .
cp kit/.importlinter .
cp kit/Makefile .
cp kit/pyproject.toml .
cp kit/.gitignore .
cp kit/.gitattributes .
cp kit/.editorconfig .
cp kit/.yamllint.yml .
cp kit/.markdownlint.yml .
cp kit/.gitmessage .
cp kit/.dockerignore .
cp kit/Dockerfile .
cp kit/docker-compose.yml .
cp kit/CONTRIBUTING.md .
cp kit/SECURITY.md .
cp kit/CHANGELOG.md .
```

### 步骤 3：合并而非覆盖

```bash
# 已有项目时，不要覆盖
# 而是手动合并：
# - Makefile：保留你的 target，加入 gate、lint、test
# - pyproject.toml：保留你的依赖，加入 dev 依赖
# - .github/workflows/：保留你的 workflow，加入 harness-ci.yml
```

### 步骤 4：改根文件

- `README.md`：改成你的项目
- `LICENSE`：改成你的
- `CODEOWNERS`：改成你的团队
- `CODEOWNERS`：`@your-team` 替换

### 步骤 5：初始化

```bash
bash scripts/dev-setup.sh
make gate
```

---

## 七、复制后必须修改的内容

### 7.1 根目录

| 文件                                        | 修改内容                 |
| ------------------------------------------- | ------------------------ |
| `README.md`                                 | 项目名、描述、徽章、链接 |
| `LICENSE`                                   | 版权人、年份             |
| `CONTRIBUTING.md`                           | 团队信息、联系方式       |
| `SECURITY.md`                               | 安全邮箱                 |
| `CODEOWNERS`                                | `@your-team` 替换        |
| `.github/ISSUE_TEMPLATE/config.yml`         | 讨论链接                 |
| `.github/ISSUE_TEMPLATE/bug_report.md`      | 项目名                   |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 项目名                   |
| `.env.example`                              | 你的环境变量             |

### 7.2 `harness/rules/`

| 文件                        | 修改内容             |
| --------------------------- | -------------------- |
| `project-structure.md`      | 你的模块、分层、依赖 |
| `dev-process.md`            | 你的流程、CI 命令    |
| `coding-standard.md`        | 你的编码规范         |
| `python-coding-standard.md` | 你的 Python 规范     |
| `python-layers.md`          | 你的分层             |
| `security-standard.md`      | 你的安全规范         |
| 其他规则                    | 按需修改             |

### 7.3 `harness/skills/`

| 文件                                   | 修改内容     |
| -------------------------------------- | ------------ |
| `coding/SKILL.md`                      | 你的分层模板 |
| `expert-reviewer/checklists/python.md` | 你的检查清单 |
| `unit-test/SKILL.md`                   | 你的测试框架 |
| 其他 Skill                             | 按需修改     |

### 7.4 `harness/wiki/`

| 文件                   | 修改内容 |
| ---------------------- | -------- |
| `glossary.md`          | 你的术语 |
| `data-model.md`        | 你的表   |
| `business-flows.md`    | 你的流程 |
| `monitoring.md`        | 你的监控 |
| `rollback-playbook.md` | 你的回滚 |

### 7.5 `harness/agent/`

| 文件                          | 修改内容               |
| ----------------------------- | ---------------------- |
| `application-owner.md`        | 项目背景、技术栈、架构 |
| `application-owner-python.md` | 你的工具链             |

### 7.6 `harness/pipeline/`

| 文件                   | 修改内容     |
| ---------------------- | ------------ |
| `stages.md`            | 你的阶段细节 |
| `human-checkpoints.md` | 你的确认人   |
| `escalation.md`        | 你的升级路径 |
| `hotfix-process.md`    | 你的热修流程 |
| `release-process.md`   | 你的发布流程 |
| `rollback-process.md`  | 你的回滚命令 |

### 7.7 `scripts/`

| 文件                    | 修改内容     |
| ----------------------- | ------------ |
| `check_layers.py`       | 你的分层规则 |
| `check_python_rules.py` | 你的规则     |
| `check_secrets.py`      | 你的密钥模式 |
| `check_complexity.py`   | 你的阈值     |

### 7.8 `.github/workflows/`

| 文件             | 修改内容               |
| ---------------- | ---------------------- |
| `harness-ci.yml` | 你的 Python 版本、命令 |

### 7.9 `config/`

| 文件                     | 修改内容     |
| ------------------------ | ------------ |
| `prometheus.yml`         | 你的监控地址 |
| `alert-rules.yml`        | 你的告警规则 |
| `logging.yml`            | 你的日志格式 |
| `grafana/dashboard.json` | 你的面板     |

---

## 八、复制后建议保留的内容

| 目录/文件                                  | 原因            |
| ------------------------------------------ | --------------- |
| `harness/agents/`                          | 填充 Agent 通用 |
| `harness/sources/`                         | 来源池通用      |
| `harness/templates/`                       | 通用模板        |
| `harness/changes/_template/`               | 通用模板        |
| `harness/metrics/`                         | 度量框架通用    |
| `harness/iteration/`                       | 迭代框架通用    |
| `harness/state/`、`audit/`、`checkpoints/` | 通用机制        |
| `harness/schemas/`                         | Schema 通用     |
| `docs/`（大部分）                          | 通用文档        |
| `.vscode/`                                 | 通用配置        |
| `tests/conftest.py`                        | 通用 fixture    |

---

## 九、复制后建议删除的内容

只想保留核心，可删除：

```text
# 可选扩展规则
harness/rules/performance-standard.md
harness/rules/concurrency-standard.md
harness/rules/cache-standard.md
harness/rules/timezone-standard.md
harness/rules/i18n-standard.md

# 可选扩展技能
harness/skills/performance/
harness/skills/refactor/
harness/skills/migration/
harness/skills/api-versioning/
harness/skills/db-migration/

# 可选扩展 Agent
harness/agents/refactor-agent.md
harness/agents/dependency-agent.md
harness/agents/doc-agent.md

# 可选工作流
harness/workflows/auto-label.yml
harness/workflows/stale.yml
harness/workflows/release.yml
harness/workflows/dependency-update.yml

# 可选文档
docs/adr/
docs/tutorials/
docs/compliance.md
docs/data-governance.md
docs/threat-model.md
docs/capacity-planning.md
docs/integrations.md
docs/anti-patterns.md
docs/best-practices.md
docs/roadmap.md

# 可选配置
config/grafana/
config/prometheus.yml
config/alert-rules.yml
config/logging.yml

# 可选脚本
scripts/collect_metrics.py
scripts/audit_log.py
scripts/state_tracker.py
scripts/check_dependencies.py
```

**删除后记得同步更新**：

- `scripts/check_harness_docs.py` 的 `REQUIRED` 列表；
- `Makefile` 的 target；
- `.github/workflows/harness-ci.yml` 的 steps。

---

## 十、环境准备

### 安装

```bash
# 一键
bash scripts/dev-setup.sh

# 或手动
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type commit-msg
git config commit.template .gitmessage
```

### 验证

```bash
make gate
```

期望输出：

```text
Ruff lint passed
Ruff format passed
Mypy passed
Pytest passed
Pytest gate passed: total=N, passed=N
Python harness rules passed
Harness docs check passed
```

### Docker

```bash
docker compose up harness
```

---

## 十一、首次验证

### 验证 1：门禁能跑

```bash
make gate
```

### 验证 2：CI 能跑

```bash
git checkout -b test/ci-check
git commit --allow-empty -m "ci: test"
git push -u origin test/ci-check
gh pr create --title "CI Test" --body "验证 CI"
```

### 验证 3：提交信息检查

```bash
git commit --allow-empty -m "bad message"
# 应该被拒绝
```

### 验证 4：门禁能拦

```bash
# 故意写一段违规代码
cat > src/bad.py <<'EOF'
import requests

def f(price: float) -> None:
    print("debug")
    requests.post("http://x")
EOF

python scripts/check_python_rules.py src
# 应输出 PRICE-001、HTTP-001、LOG-001
```

### 验证 5：空跑

```bash
mkdir -p harness/changes/REQ-0000
cp harness/changes/_template/*.md harness/changes/REQ-0000/
./scripts/check-gates.sh harness/changes/REQ-0000
```

---

## 十二、常见场景

### 场景 1：给新项目接入

见 [方式 B](#方式-b复制到已有项目)。

### 场景 2：给团队做范本

见 [方式 A](#方式-afork-后作为独立范本)。

### 场景 3：跑第一个需求

```bash
git checkout -b feature/req-0001
mkdir -p harness/changes/REQ-0001
cp harness/changes/_template/*.md harness/changes/REQ-0001/
# 按十阶段走
```

### 场景 4：填充规则

见 `docs/fill-workflow.md`。

### 场景 5：空跑

```bash
mkdir -p harness/changes/REQ-0000
# 走完整流程
# 记录到 harness/pilot/findings.md
```

### 场景 6：热修

```bash
git checkout -b hotfix/fix-xxx
# 最小改动
# 必须新增测试
# 必须新增规则
```

### 场景 7：发布

```bash
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### 场景 8：回滚

见 `harness/pipeline/rollback-process.md`。

---

## 十三、目录速查

| 我想...       | 去看                                 |
| ------------- | ------------------------------------ |
| 理解架构      | `docs/architecture.md`               |
| 填充 Harness  | `docs/fill-workflow.md`              |
| 看十阶段      | `harness/pipeline/stages.md`         |
| 看 Agent 定义 | `harness/agent/application-owner.md` |
| 写规则        | `harness/rules/_template.md`         |
| 写 Skill      | `harness/skills/_template/SKILL.md`  |
| 跑 Agent      | `harness/agents/README.md`           |
| 看反模式      | `docs/anti-patterns.md`              |
| 看最佳实践    | `docs/best-practices.md`             |
| 看 FAQ        | `docs/faq.md`                        |
| 看度量        | `harness/metrics/metrics.md`         |
| 看 Patch      | `harness/iteration/patch-log.md`     |

---

## 十四、FAQ

### Q1：必须用 Python 吗？

默认 Python。其他语言需要：

- 替换 `python-coding-standard.md`；
- 替换 `python-layers.md`；
- 替换 `scripts/check_*.py`；
- 替换 `.github/workflows/harness-ci.yml`。

骨架结构本身与语言无关。

### Q2：可以只用一部分吗？

可以。最小集合：

```text
harness/rules/
harness/skills/
harness/changes/_template/
harness/agent/
scripts/
.github/workflows/harness-ci.yml
pyproject.toml
Makefile
```

### Q3：必须走完整十阶段吗？

是。小改动大事故的案例不胜枚举。流程一致性优先于效率。

### Q4：可以跳过评审吗？

不可以。评审与编码分离是核心设计。

### Q5：可以跳过人工确认吗？

不可以。五个确认点必须人工。

### Q6：Agent 会编吗？

会。所以有三道闸：来源强制、可执行强制、测试强制。

### Q7：怎么开始填充？

见 `docs/fill-workflow.md`。

### Q8：多久能见效？

按阿里团队经验：一周搭建，两周试点，一个月见效。

### Q9：AI 代码率能到多少？

项目维度 90%+，个人维度 85%+。

### Q10：返工轮次能降到多少？

从 3-5 轮降到通常 1 轮。

---

## 十五、下一步

1. 复制骨架到目标位置；
2. 按 [七、复制后必须修改的内容](#七复制后必须修改的内容) 改；
3. 按 [十、环境准备](#十环境准备) 装；
4. 按 [十一、首次验证](#十一首次验证) 验证；
5. 按 `docs/fill-workflow.md` 填充；
6. 空跑 REQ-0000；
7. 试点 REQ-0001；
8. 度量；
9. 迭代。

---

> **这个 kit 的价值不在于它本身，而在于你往里填的东西。**
>
> **它是容器，不是内容。它是脚手架，不是建筑。**
>
> **你填一条真实事故，它就厚一分。你填一条真实 Review，它就准一分。**

---

## 十六、总结

| 文档                    | 作用           | 面向                 |
| ----------------------- | -------------- | -------------------- |
| `USAGE.md`              | 怎么用这个 kit | 使用者、复制者       |
| `FillWorkflow.md`       | 怎么填充内容   | 填充者、Agent 操作者 |
| `BluePrint.md`          | 蓝图         | 核心内容总设计文档 |
**两份文档覆盖**：

- 从拿到 kit 到复制出去；
- 从复制出去到改完；
- 从改完到验证；
- 从验证到填充；
- 从填充到空跑；
- 从空跑到试点；
- 从试点到度量；
- 从度量到迭代。

**骨架 + 使用指南 + 填充工作流 = 完整 kit。**
