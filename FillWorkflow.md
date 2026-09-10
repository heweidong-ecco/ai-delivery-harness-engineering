# 填充工作流

> 本文档说明如何把真实项目信息填充到 Harness 骨架中。
>
> 骨架是容器，填充是内容。没有填充，骨架就是空壳。

---

## 目录

- [一、填充总览](#一填充总览)
- [二、前置准备](#二前置准备)
- [三、来源池建立](#三来源池建立)
- [四、核心 6 个 Agent](#四核心-6-个-agent)
- [五、扩展 5 个 Agent](#五扩展-5-个-agent)
- [六、编排流程](#六编排流程)
- [七、人工审核](#七人工审核)
- [八、合并回填](#八合并回填)
- [九、空跑验证](#九空跑验证)
- [十、试点](#十试点)
- [十一、度量](#十一度量)
- [十二、迭代](#十二迭代)
- [十三、完整工作流图](#十三完整工作流图)
- [十四、时间估算](#十四时间估算)
- [十五、常见问题](#十五常见问题)

---

## 一、填充总览

### 填充公式

```text
真实来源 + 结构化 Prompt + 六件套输出 + 人工审核 + 可执行检查 = 厚实规则
```

### 填充阶段

```text
阶段 1：来源池建立
    ↓
阶段 2：核心 6 个 Agent（必须）
    ↓
阶段 3：扩展 5 个 Agent（可选）
    ↓
阶段 4：人工审核
    ↓
阶段 5：合并回填
    ↓
阶段 6：空跑验证
    ↓
阶段 7：试点
    ↓
阶段 8：度量
    ↓
阶段 9：迭代
```

### 填充产出

| 产出              | 目标     |
| ----------------- | -------- |
| 规则              | >= 30 条 |
| 规则来源覆盖率    | 100%     |
| 规则可程序化率    | 100%     |
| P0 规则测试覆盖率 | 100%     |
| Wiki 完整度       | >= 80%   |
| 门禁可运行        | 是       |

---

## 二、前置准备

### 2.1 环境

```bash
cd your-project-harness
bash scripts/dev-setup.sh
make gate
```

确保门禁通过。

### 2.2 确定填充范围

| 项            | 说明          |
| ------------- | ------------- |
| 填充哪些规则  | 至少核心 5 份 |
| 填充哪些技能  | 至少核心 9 个 |
| 填充哪些 Wiki | 至少核心 3 份 |
| 跑哪些 Agent  | 至少核心 6 个 |

### 2.3 确定来源

| 来源        | 必需   | 位置                            |
| ----------- | ------ | ------------------------------- |
| 事故报告    | 是     | `harness/sources/incidents/`    |
| Code Review | 是     | `harness/sources/reviews/`      |
| 架构文档    | 是     | `harness/sources/architecture/` |
| DDL         | 视项目 | `harness/sources/ddl/`          |
| 接口文档    | 视项目 | `harness/sources/api/`          |
| 业务流程图  | 视项目 | `harness/sources/flows/`        |
| 代码库      | 是     | `src/`                          |

### 2.4 脱敏

**所有来源必须脱敏**：

```bash
# 手机号
sed -E 's/1[3-9][0-9]{9}/138****1234/g' source.md

# 身份证
sed -E 's/[0-9]{17}[0-9Xx]/110101********1234/g' source.md

# 银行卡
sed -E 's/[0-9]{16,19}/****1234/g' source.md

# 邮箱
sed -E 's/([a-zA-Z])[a-zA-Z0-9._%+-]*@/\\1***@/g' source.md

# 密钥
# 手动删除或替换为 <REDACTED>
```

### 2.5 检查清单

- [ ] 环境装好
- [ ] 门禁通过
- [ ] 来源已脱敏
- [ ] 填充范围确定
- [ ] 团队知会

---

## 三、来源池建立

### 3.1 目录结构

```text
harness/sources/
├── README.md
├── incidents/           # 事故报告
├── reviews/             # Code Review 意见
├── architecture/        # 架构文档
├── ddl/                 # 数据库 DDL
├── api/                 # 接口文档
├── flows/               # 业务流程图
└── code/                # 代码库快照（可选）
```

### 3.2 事故报告

**来源**：

- Jira 导出；
- Confluence 导出；
- 事故工单；
- 复盘文档。

**命名**：

```text
harness/sources/incidents/INC-YYYY-MMDD.md
```

**格式**：

```markdown
# INC-YYYY-MMDD

## 基本信息

| 字段     | 内容          |
| -------- | ------------- |
| 编号     | INC-YYYY-MMDD |
| 日期     |               |
| 模块     |               |
| 严重级别 | P0/P1/P2      |
| 影响     |               |
| 损失     |               |

## 时间线

| 时间 | 事件 |
| ---- | ---- |
|      |      |

## 现象

## 根因

## 修复

## 回滚

## 复盘

## 可转规则

| 规则 | 检查 | 测试 | 状态 |
| ---- | ---- | ---- | ---- |
```

**最少数量**：5 份。

### 3.3 Review 意见

**来源**：

- GitHub PR；
- GitLab MR；
- Bitbucket PR；
- Code Review 工具。

**导出命令**：

```bash
# GitHub
gh pr list --state merged --limit 200 --json number,title > pr-list.json

# 逐个导出
gh pr view <number> --comments > harness/sources/reviews/PR-<number>.md
```

**格式**：

```markdown
# PR-<number>

## 标题

## Review 意见

| 评论人 | 意见 | 文件 | 行号 |
| ------ | ---- | ---- | ---- |
|        |      |      |      |

## 结论

- [ ] 通过
- [ ] 有条件通过
- [ ] 不通过
```

**最少数量**：20 份。

### 3.4 架构文档

**来源**：

- Wiki；
- Confluence；
- 架构图；
- 模块清单；
- 包结构。

**格式**：

```markdown
# 架构文档

## 模块清单

| 模块 | 职责 | 允许依赖 | 禁止依赖 |
| ---- | ---- | -------- | -------- |

## 分层架构

## 关键设计

## 扩展点
```

**最少数量**：1 份。

### 3.5 DDL

**来源**：

- 数据库导出；
- ER 图；
- 数据字典。

**命令**：

```bash
# MySQL
mysqldump --no-data your_db > harness/sources/ddl/schema.sql

# PostgreSQL
pg_dump --schema-only your_db > harness/sources/ddl/schema.sql
```

### 3.6 接口文档

**来源**：

- Swagger；
- OpenAPI；
- Postman；
- 接口文档。

**命令**：

```bash
# 从 Swagger 导出
curl http://your-service/v3/api-docs > harness/sources/api/openapi.json
```

### 3.7 业务流程图

**来源**：

- 流程图工具；
- 文档；
- 人工整理。

**格式**：

```markdown
# 流程名

- 触发：
- 主链路：
- 国际化链路：
- 异常与降级：
- 相关表：
- 相关接口：
- 历史事故：
```

### 3.8 来源池 README

`harness/sources/README.md`：

```markdown
# 来源池

## 目录

| 目录          | 用途        | 填充 Agent        |
| ------------- | ----------- | ----------------- |
| incidents/    | 事故报告    | 事故反推 Agent    |
| reviews/      | Code Review | Review 提炼 Agent |
| architecture/ | 架构文档    | 架构解析 Agent    |
| ddl/          | 数据库 DDL  | 数据建模 Agent    |
| api/          | 接口文档    | 数据建模 Agent    |
| flows/        | 业务流程图  | 数据建模 Agent    |
| code/         | 代码库快照  | 代码考古 Agent    |

## 规则

- 所有资料必须脱敏。
- 禁止提交密钥、真实用户数据、生产配置。
- 每条规则必须有来源。
- 来源为空则拒绝进入 Harness。
```

### 3.9 来源完整性检查

```bash
# 检查来源
ls harness/sources/incidents/ | wc -l
ls harness/sources/reviews/ | wc -l
ls harness/sources/architecture/ | wc -l

# 期望
# incidents >= 5
# reviews >= 20
# architecture >= 1
```

**来源不足则停止，先补充。**

---

## 四、核心 6 个 Agent

### Agent 1：架构解析

#### 目标

从代码库或架构文档提取分层规则。

#### 输入

- `harness/sources/architecture/`
- `src/`

#### 步骤

```bash
git checkout -b agent/architecture
```

**Prompt**：

```text
你是 Harness 架构解析 Agent。

## 任务
阅读 harness/sources/architecture/ 和 src/ 目录下的代码结构，
推断项目的分层架构和依赖方向。

## 步骤
1. 扫描 src/ 下所有包和模块。
2. 统计每个模块被谁 import。
3. 推断分层：api / service / domain / repository / adapter。
4. 找出违反分层方向的 import。
5. 生成分层规则。

## 输出
### 1. 模块清单
| 模块 | 职责 | 被谁依赖 | 依赖谁 |

### 2. 分层结论

### 3. 违规清单
| 文件 | 行号 | 违规 import | 违反规则 |

### 4. 建议规则
按六件套输出。

## 硬性约束
- 不允许编造模块。
- 不允许编造违规。
- 每条规则必须有来源。
- 缺失信息写"待补充"。
```

**输出路径**：

```text
harness/sources/architecture/extracted-rules.md
```

**回填目标**：

```text
harness/rules/project-structure.md
harness/rules/python-layers.md
scripts/check_layers.py
```

**提交**：

```bash
git add harness/sources/architecture/extracted-rules.md
git commit -m "agent: extract architecture rules"
git push -u origin agent/architecture
gh pr create --title "Agent: Architecture" --body "架构解析"
```

#### 审核清单

- [ ] 模块清单与实际一致
- [ ] 分层结论合理
- [ ] 违规清单可查
- [ ] 每条规则有来源
- [ ] 缺失信息写"待补充"

---

### Agent 2：事故反推

#### 目标

从事故报告提取硬约束规则。

#### 输入

- `harness/sources/incidents/`

#### 步骤

```bash
git checkout -b agent/incident
```

**Prompt**：

```text
你是 Harness 事故反推 Agent。

## 任务
阅读 harness/sources/incidents/ 下所有事故报告，
为每条事故提取可转化为 Harness 规则的候选规则。

## 对每条事故，回答
1. 这条事故能不能用一条规则拦住？
2. 这条规则能不能程序化验证？
3. 这条规则属于哪个文件？
4. 这条规则的反例是什么？
5. 这条规则的正例是什么？
6. 这条规则应该配什么测试？

## 输出格式
按六件套输出：
- 规则 ID: <模块>-<序号>
- 规则
- 原因（事故编号、日期、现象、根因、损失）
- 反例
- 正例
- 检查
- 测试
- 优先级
- Owner
- 来源

## 硬性约束
- 不允许编造事故。
- 不允许写没有事故支撑的规则。
- 如果一条事故无法转成规则，明确写"无法转化"并说明原因。
- 如果一条事故能转成多条规则，拆开写。
```

**输出路径**：

```text
harness/sources/incidents/extracted-rules.md
```

**回填目标**：

```text
harness/rules/coding-standard.md
harness/rules/security-standard.md
harness/rules/error-handling.md
harness/rules/logging-standard.md
harness/rules/observability-standard.md
scripts/check_python_rules.py
tests/
```

**提交**：

```bash
git add harness/sources/incidents/extracted-rules.md
git commit -m "agent: extract incident rules"
git push -u origin agent/incident
gh pr create --title "Agent: Incident" --body "事故反推"
```

#### 输出示例

````markdown
## 规则 ID: PAY-001

### 规则
支付回调必须设置超时，超时后必须标记 pending 并异步补偿。

### 原因
INC-2024-0421，2024-04-21，支付回调堆积 3 小时，
根因是 service 直接调 HTTP 未设 timeout，
影响 1.2 万笔订单，损失约 8 万。

### 反例
```python
requests.post(url, json=payload)
```

### 正例
```python
try:
    requests.post(url, json=payload, timeout=3)
except requests.Timeout:
    order.mark_pending()
    raise
```

### 检查
scripts/check_python_rules.py HTTP-001

### 测试
tests/payment/test_callback.py::test_timeout_marks_pending

### 优先级
P0

### Owner
支付组

### 来源
harness/sources/incidents/INC-2024-0421.md
````

#### 审核清单

- [ ] 每条规则有事故编号
- [ ] 事故编号可查
- [ ] 反例和正例能跑通
- [ ] 检查脚本能实现
- [ ] 测试能写出来
- [ ] 优先级合理

---

### Agent 3：Review 提炼

#### 目标

从 Code Review 意见提取重复规则。

#### 输入

- `harness/sources/reviews/`

#### 步骤

```bash
git checkout -b agent/review
```

**Prompt**：

```text
你是 Harness Review 提炼 Agent。

## 任务
阅读 harness/sources/reviews/ 下所有 Code Review 意见，
提取重复出现的、可规则化的意见。

## 对每条意见，回答
1. 这条意见是否重复出现 3 次以上？
2. 是否可写成规则？
3. 是否可程序化验证？
4. 属于哪个文件？

## 输出格式
| 规则 ID | 规则 | 出现次数 | 来源 PR | 可程序化 | 目标文件 | 优先级 |

## 对重复 3 次以上的意见，展开六件套：
规则、原因、反例、正例、检查、测试。

## 硬性约束
- 只提取重复出现的意见。
- 只出现 1 次的写进"观察池"，不写成规则。
- 不允许编造 PR。
- 每条规则必须列出至少 3 个来源 PR。
```

**输出路径**：

```text
harness/sources/reviews/extracted-rules.md
harness/sources/reviews/observation-pool.md
```

**回填目标**：

```text
harness/rules/coding-standard.md
harness/rules/testing-standard.md
harness/rules/database-standard.md
harness/rules/api-design-standard.md
```

#### 输出示例

```markdown
| 规则 ID  | 规则                          | 出现次数 | 来源 PR        | 可程序化 | 目标文件                  | 优先级 |
| -------- | ----------------------------- | -------- | -------------- | -------- | ------------------------- | ------ |
| API-001  | api 层禁止直接访问 repository | 12       | #101,#108,#115 | 是       | python-layers.md          | P0     |
| LOG-001  | 禁止 print，必须用 logging    | 8        | #98,#120,#133  | 是       | python-coding-standard.md | P1     |
| TEST-001 | 新增接口必须新增测试          | 15       | #90,#99,#110   | 是       | dev-process.md            | P0     |
| CFG-001  | 配置禁止硬编码                | 6        | #88,#105,#121  | 是       | python-coding-standard.md | P0     |
```

#### 审核清单

- [ ] 出现次数统计准确
- [ ] 来源 PR 可查
- [ ] 规则可程序化
- [ ] 没有把一次性意见写成规则

---

### Agent 4：代码考古

#### 目标

从代码库提取每层最佳实践和反例。

#### 输入

- `src/`

#### 步骤

```bash
git checkout -b agent/code-archaeology
```

**Prompt**：

```text
你是 Harness 代码考古 Agent。

## 任务
在 src/ 中找出每个分层的最佳实践和反例。

## 步骤
1. 找出每层最规范的 3 个文件。
2. 找出每层最不规范的 3 个文件。
3. 提取模板。
4. 提取反例。

## 输出
### 每层最佳实践
文件、理由、模板

### 每层反例
文件、理由、问题

### 建议规则

## 硬性约束
- 不允许编造文件。
- 每条模板必须有来源文件。
- 每条反例必须有来源文件。
```

**输出路径**：

```text
harness/sources/code/extracted-patterns.md
```

**回填目标**：

```text
harness/skills/coding/SKILL.md
harness/rules/coding-standard.md
```

#### 输出示例

````markdown
## Service 层最佳实践
文件：src/service/order_service.py
理由：事务边界清晰，adapter 调用带 timeout，异常不吞。

模板：
```python
class OrderService:
    def __init__(self, repo: OrderRepository, pay: PaymentAdapter) -> None:
        self._repo = repo
        self._pay = pay

    def create(self, cmd: CreateOrderCommand) -> Order:
        order = Order.create(cmd)
        self._repo.save(order)
        try:
            self._pay.charge(order.id, order.amount_cents, timeout=3)
        except PaymentTimeout:
            order.mark_pending()
            self._repo.save(order)
            raise
        return order
```

## Service 层反例
文件：src/service/legacy_pay.py
理由：直接 import requests，无 timeout，吞异常。
````

---

### Agent 5：数据建模

#### 目标

从 DDL 和接口文档生成 Wiki。

#### 输入

- `harness/sources/ddl/`
- `harness/sources/api/`
- `harness/sources/flows/`

#### 步骤

```bash
git checkout -b agent/data-modeling
```

**Prompt**：

```text
你是 Harness 数据建模 Agent。

## 任务
1. 读 DDL，生成 wiki/data-model.md。
2. 读 OpenAPI，生成 wiki/business-flows.md。
3. 读业务流程图，补充流程说明。

## data-model.md 格式
| 表名 | 说明 | 关键字段 | 关联表 | 注意事项 |

## business-flows.md 格式
## 流程名
- 触发：
- 主链路：
- 国际化链路：
- 异常与降级：
- 相关表：
- 相关接口：
- 历史事故：

## 硬性约束
- 不允许编造字段。
- 不允许编造流程。
- 缺失信息写"待补充"。
```

**输出路径**：

```text
harness/wiki/data-model.md
harness/wiki/business-flows.md
harness/wiki/glossary.md
```

---

### Agent 6：门禁解析

#### 目标

从 CI 配置生成可程序化门禁。

#### 输入

- `.github/workflows/`
- `Makefile`
- `pyproject.toml`

#### 步骤

```bash
git checkout -b agent/gate
```

**Prompt**：

```text
你是 Harness 门禁解析 Agent。

## 任务
读现有 CI 配置和 Makefile，
生成可程序化验证的门禁清单。

## 输出
| 门禁 | 命令 | 通过条件 | 失败回退 | 对应规则 |

## 硬性约束
- 每条门禁必须可机器验证。
- 自然语言描述不算门禁。
- 必须给出具体命令。
```

**输出路径**：

```text
harness/sources/architecture/extracted-gates.md
```

**回填目标**：

```text
scripts/
.github/workflows/harness-ci.yml
Makefile
```

#### 输出示例

```markdown
| 门禁     | 命令                                  | 通过条件  | 失败回退 | 对应规则  |
| -------- | ------------------------------------- | --------- | -------- | --------- |
| 类型检查 | mypy src                              | exit 0    | 回退编码 | TYPE-001  |
| 金额检查 | python scripts/check_python_rules.py  | 无输出    | 回退编码 | PRICE-001 |
| 测试数   | python scripts/check_pytest_report.py | total > 0 | 回退单测 | TEST-001  |
| 覆盖率   | pytest --cov-fail-under=80            | exit 0    | 回退单测 | TEST-002  |
```

---

## 五、扩展 5 个 Agent

### Agent 7：安全

**目标**：从安全审计、威胁模型提取安全规则。

**输入**：安全审计报告、`docs/threat-model.md`、`docs/compliance.md`

**输出**：`harness/rules/security-standard.md`

### Agent 8：性能

**目标**：从性能事故、监控提取性能规则。

**输入**：性能事故、`docs/capacity-planning.md`、监控数据

**输出**：`harness/rules/performance-standard.md`、`harness/rules/cache-standard.md`

### Agent 9：重构

**目标**：识别反模式，生成重构规则。

**输入**：`src/`、`docs/anti-patterns.md`

**输出**：反模式清单、重构建议、规则

### Agent 10：依赖

**目标**：从依赖问题提取规则。

**输入**：`pyproject.toml`、`pip-audit` 输出

**输出**：`harness/rules/dependency-standard.md`

### Agent 11：文档

**目标**：从代码和需求生成文档。

**输入**：`src/`、`harness/changes/`

**输出**：`docs/`、`harness/wiki/`

---

## 六、编排流程

### 6.1 Orchestrator 角色

`harness/agents/orchestrator.md` 定义编排逻辑。

### 6.2 执行阶段

```text
阶段 1：核心 6 个（必须）
  ├── Agent 1：架构解析
  ├── Agent 2：事故反推
  ├── Agent 3：Review 提炼
  ├── Agent 4：代码考古
  ├── Agent 5：数据建模
  └── Agent 6：门禁解析

阶段 2：扩展 5 个（可选）
  ├── Agent 7：安全
  ├── Agent 8：性能
  ├── Agent 9：重构
  ├── Agent 10：依赖
  └── Agent 11：文档
```

### 6.3 每个 Agent 独立操作

```bash
# 1. 建分支
git checkout main
git pull
git checkout -b agent/<name>

# 2. 放入来源
# （已在来源池中）

# 3. 跑 Agent
# （按 Prompt 执行）

# 4. 人工审核
# （按审核清单）

# 5. 合并回填
# 追加到目标文件

# 6. 更新检查脚本
# 更新 scripts/

# 7. 更新测试
# 更新 tests/

# 8. 提交
git add .
git commit -m "agent: <name>"
git push -u origin agent/<name>
gh pr create --title "Agent: <name>" --body "<说明>"

# 9. CI 通过后合并
```

### 6.4 状态跟踪

`harness/agents/orchestrator.md` 中的状态表：

| Agent    | 状态 | 分支 | PR  | 审核 | 合并 |
| -------- | ---- | ---- | --- | ---- | ---- |
| 架构解析 |      |      |     |      |      |
| 事故反推 |      |      |     |      |      |
| ...      |      |      |     |      |      |

---

## 七、人工审核

### 7.1 审核清单

- [ ] 每条规则有来源
- [ ] 来源可查
- [ ] 反例能跑出问题
- [ ] 正例能通过检查
- [ ] 检查脚本能拦
- [ ] 测试能失败也能通过
- [ ] 优先级合理
- [ ] Owner 明确

### 7.2 三道防编造闸

#### 闸 1：来源强制

```text
每条规则必须有 source 字段。
source 为空 → 直接拒绝。
source 查不到 → 直接拒绝。
```

#### 闸 2：可执行强制

```text
每条规则必须有检查命令。
检查命令跑不通 → 直接拒绝。
检查命令跑通但拦不住反例 → 直接拒绝。
```

#### 闸 3：测试强制

```text
每条 P0 规则必须有测试。
测试必须能失败。
测试必须能通过。
```

### 7.3 审核记录

`harness/audit/<date>-<event>.md`：

```markdown
# <event>

- 时间：
- 来源：
- 审核人：
- 结论：
- 备注：
```

---

## 八、合并回填

### 8.1 追加规则

```bash
# 追加到规则文件
cat extracted-rule.md >> harness/rules/coding-standard.md
```

### 8.2 更新检查脚本

```python
# scripts/check_python_rules.py
RULES = [
    ("PRICE-001", rule_price_no_float),
    ("HTTP-001", rule_http_timeout),
    ("PAY-001", rule_payment_timeout),  # 新增
    # ...
]
```

### 8.3 更新测试

```python
# tests/test_python_rules.py
def test_rule_pay_001():
    code = "requests.post(url, json=payload)"
    errors = check_rule(code, "PAY-001")
    assert errors
```

### 8.4 更新 CHANGELOG

```markdown
## [Unreleased]

### Added
- PAY-001：支付回调必须设置 timeout（来源：INC-2024-0421）
- API-001：api 层禁止直接访问 repository（来源：PR #101,#108,#115）
```

### 8.5 提交

```bash
git add .
git commit -m "rule: add PAY-001 from INC-2024-0421"
git push
```

---

## 九、空跑验证

### 9.1 目标

用真实需求之前，先空跑一次，发现体系缺陷。

### 9.2 步骤

```bash
git checkout -b pilot/req-0000
mkdir -p harness/changes/REQ-0000
cp harness/changes/_template/*.md harness/changes/REQ-0000/
```

### 9.3 走完整十阶段

按 `harness/pipeline/stages.md` 走。

### 9.4 记录缺陷

`harness/pilot/findings.md`：

```markdown
# 空跑发现

| 缺陷              | 原因           | 修复             | 状态 |
| ----------------- | -------------- | ---------------- | ---- |
| CI 忽略测试数为 0 | 门禁不完整     | 增加 TotalTest>0 | 待修 |
| 评审报告不生成    | 模板未强制     | 强制生成         | 待修 |
| 摘要重复行        | Agent 追加倾向 | 模板去重         | 待修 |
| 部署参数推测      | 无人工确认     | 增加确认点       | 待修 |
```

### 9.5 常见 4 个缺陷

1. CI 门禁只检查状态码，忽略测试用例数为 0；
2. 简单需求下评审报告不生成文件；
3. 摘要文件因 Agent 的追加倾向出现重复行；
4. 部署参数被 Agent 错误推测。

### 9.6 Patch

每个缺陷 Patch 回 Harness：

```bash
# 修 CI
vim scripts/check_pytest_report.py

# 修模板
vim harness/changes/_template/review-record-v1.md

# 修流程
vim harness/pipeline/stages.md

# 提交
git add .
git commit -m "fix: patch harness from pilot REQ-0000"
git push
```

### 9.7 验收

- [ ] 走完十阶段
- [ ] 记录 >= 4 个缺陷
- [ ] 每个缺陷已 Patch
- [ ] `make gate` 通过

---

## 十、试点

### 10.1 目标

用一个真实需求走完整流程。

### 10.2 选需求

| 标准     | 说明             |
| -------- | ---------------- |
| 真实     | 不是编造的       |
| 简单     | 不要一上来就复杂 |
| 完整     | 有需求、有验收   |
| 有主链路 | 不要纯配置       |

### 10.3 步骤

```bash
git checkout -b feature/req-0001
mkdir -p harness/changes/REQ-0001
cp harness/changes/_template/*.md harness/changes/REQ-0001/
```

按十阶段走：

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

### 10.4 记录

每个阶段产出写入 `harness/changes/REQ-0001/`。

### 10.5 度量

`harness/metrics/data/metrics-YYYYMMDD.json`：

```json
{
  "collected_at": "2024-XX-XXT00:00:00Z",
  "req": "REQ-0001",
  "rework_rounds": 1,
  "review_rounds": 1,
  "gate_pass_rate": 1.0,
  "coverage": 0.85,
  "ai_code_rate": 0.9
}
```

### 10.6 复盘

`harness/iteration/retrospective.md`：

```markdown
# 复盘 REQ-0001

## 做得好的

## 做得不好的

## 改进

## Patch

## 下一步
```

### 10.7 验收

- [ ] 1 个真实需求完成
- [ ] 度量数据积累
- [ ] Patch 记录 >= 5 条
- [ ] `make gate` 通过

---

## 十一、度量

### 11.1 核心指标

| 指标       | 目标  |
| ---------- | ----- |
| AI 代码率  | 90%   |
| 返工轮次   | <=1   |
| 门禁通过率 | 100%  |
| 覆盖率     | >=80% |

### 11.2 采集

```bash
make metrics
```

或：

```bash
python scripts/collect_metrics.py
```

### 11.3 存储

`harness/metrics/data/metrics-YYYYMMDD.json`

### 11.4 看板

`harness/metrics/dashboard.md`

### 11.5 频率

- 实时：门禁通过率、覆盖率；
- 每日：AI 代码率；
- 每周：返工轮次、评审轮次；
- 每月：规则条数、来源覆盖率。

---

## 十二、迭代

### 12.1 Patch 流程

```text
1. 发现问题
2. 记录到 patch-log.md
3. 写规则
4. 写检查脚本
5. 写测试
6. 提交 PR
7. 审核
8. 合并
```

### 12.2 Patch 优先级

| 优先级 | 条件     | 时限    |
| ------ | -------- | ------- |
| P0     | 阻塞上线 | 24 小时 |
| P1     | 本轮修完 | 本周    |
| P2     | 后续优化 | 本月    |

### 12.3 Patch 记录

`harness/iteration/patch-log.md`：

| 日期 | 来源 | 问题 | Patch | 目标文件 | 提交 | 审核人 |
| ---- | ---- | ---- | ----- | -------- | ---- | ------ |

### 12.4 复盘

- 月度复盘：`harness/iteration/retrospective-YYYY-MM.md`
- 季度复盘：团队

### 12.5 规则

- 每次实战问题必须 Patch。
- Patch 必须可程序化验证。
- Patch 必须更新测试。
- Patch 必须提交 PR。
- Patch 必须有人审核。
- Patch 必须有来源。

---

## 十三、完整工作流图

```text
┌──────────────────────────────────────────────┐
│  阶段 0：前置准备                            │
│  ├── 环境装好                                │
│  ├── 门禁通过                                │
│  └── 来源脱敏                                │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 1：来源池建立                          │
│  ├── incidents/                              │
│  ├── reviews/                                │
│  ├── architecture/                           │
│  ├── ddl/                                    │
│  ├── api/                                    │
│  └── flows/                                  │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 2：核心 6 个 Agent                     │
│  ├── Agent 1：架构解析                       │
│  ├── Agent 2：事故反推                       │
│  ├── Agent 3：Review 提炼                    │
│  ├── Agent 4：代码考古                       │
│  ├── Agent 5：数据建模                       │
│  └── Agent 6：门禁解析                       │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 3：扩展 5 个 Agent（可选）             │
│  ├── Agent 7：安全                           │
│  ├── Agent 8：性能                           │
│  ├── Agent 9：重构                           │
│  ├── Agent 10：依赖                          │
│  └── Agent 11：文档                          │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 4：人工审核                            │
│  ├── 来源强制                                │
│  ├── 可执行强制                              │
│  └── 测试强制                                │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 5：合并回填                            │
│  ├── rules/                                  │
│  ├── skills/                                 │
│  ├── wiki/                                   │
│  ├── scripts/                                │
│  ├── tests/                                  │
│  └── CHANGELOG                               │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 6：空跑验证 REQ-0000                   │
│  ├── 走十阶段                                │
│  ├── 记录缺陷                                │
│  └── Patch                                   │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 7：试点 REQ-0001                       │
│  ├── 走十阶段                                │
│  ├── 度量                                    │
│  └── 复盘                                    │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 8：度量                                │
│  ├── AI 代码率                               │
│  ├── 返工轮次                                │
│  ├── 门禁通过率                              │
│  └── 覆盖率                                  │
└──────────────────────────────────────────────┘
                    ↓
┌──────────────────────────────────────────────┐
│  阶段 9：迭代                                │
│  ├── Patch                                   │
│  ├── 复盘                                    │
│  └── 持续优化                                │
└──────────────────────────────────────────────┘
```

---

## 十四、时间估算

| 阶段            | 时间           | 产出       |
| --------------- | -------------- | ---------- |
| 0. 前置准备     | 1 天           | 环境就绪   |
| 1. 来源池       | 2-3 天         | 来源齐全   |
| 2. 核心 6 Agent | 5-7 天         | 规则 >= 30 |
| 3. 扩展 5 Agent | 3-5 天（可选） | 规则扩展   |
| 4. 人工审核     | 2 天           | 审核通过   |
| 5. 合并回填     | 1-2 天         | 合并完成   |
| 6. 空跑         | 3-5 天         | 缺陷修复   |
| 7. 试点         | 1-2 周         | 需求完成   |
| 8. 度量         | 持续           | 数据积累   |
| 9. 迭代         | 持续           | 持续优化   |
| **总计**        | **约 4-6 周**  | **可上线** |

> 阿里团队经验：一周搭建，两周试点，一个月见效。

---

## 十五、常见问题

### Q1：来源不足怎么办？

**A**：先补充。没有来源，Agent 就编。三道闸会拒绝。

### Q2：Agent 输出有编造怎么办？

**A**：打回重做。来源强制、可执行强制、测试强制三道闸会拦。

### Q3：规则太多怎么办？

**A**：按 P0/P1/P2 分级。

### Q4：规则太少怎么办？

**A**：继续填充。至少 30 条。

### Q5：空跑发现缺陷怎么办？

**A**：立即 Patch 回 Harness。每个缺陷对应一条规则。

### Q6：试点需求太复杂怎么办？

**A**：换简单的。先易后难。

### Q7：度量数据不达标怎么办？

**A**：复盘。找出根因，Patch。

### Q8：什么时候算完成？

**A**：

- 规则 >= 30；
- 来源覆盖率 100%；
- 可程序化率 100%；
- P0 测试覆盖率 100%；
- 空跑通过；
- 试点通过。

### Q9：能跳过空跑吗？

**A**：不建议。空跑是发现体系缺陷的最好时机。

### Q10：能跳过扩展 Agent 吗？

**A**：可以。核心 6 个必须，扩展 5 个可选。

---

## 十六、一句话总结

**填充公式：真实来源 + 结构化 Prompt + 六件套输出 + 人工审核 + 可执行检查 = 厚实规则。**

**没有来源，Agent 就编。没有审核，规则就假。没有检查，规则就空。没有测试，规则就死。**

---
## 总结

| 文档              | 作用           | 面向                 |
| ----------------- | -------------- | -------------------- |
| `USAGE.md`        | 怎么用这个 kit | 使用者、复制者       |
| `FillWorkflow.md` | 怎么填充内容   | 填充者、Agent 操作者 |
| `BluePrint.md`    | 蓝图           | 核心内容总设计文档   |

**三份文档覆盖**：

- 从拿到 kit 到复制出去；
- 从复制出去到改完；
- 从改完到验证；
- 从验证到填充；
- 从填充到空跑；
- 从空跑到试点；
- 从试点到度量；
- 从度量到迭代。

**骨架 + 使用指南 + 填充工作流 = 完整 kit。**
