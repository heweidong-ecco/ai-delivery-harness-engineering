# 用 Agent 填充 Harness 具体内容的完整方法论

核心原则先说清楚：

> **Agent 不是“创造”规则，而是“提取 + 结构化 + 验证”真实资料。**  
> 你给它真实输入源，它输出结构化规则；你不给输入源，它就开始编。

所以填充的关键不是 Agent 多聪明，而是**你喂什么、怎么喂、怎么验收**。

---

## 1. 整体流程

```text
真实输入源
  ├── 事故报告
  ├── Code Review 意见
  ├── 架构文档
  ├── DDL / 接口文档
  ├── CI 配置
  ├── 代码库
  └── 线上监控
        ↓
  Agent 提取阶段
  ├── 抽取候选规则
  ├── 去重合并
  ├── 分类归档
  └── 生成六件套
        ↓
  人工审核阶段
  ├── 真实性校验
  ├── 可程序化校验
  ├── 优先级排序
  └── Owner 确认
        ↓
  回填 Harness
  ├── rules/
  ├── skills/
  ├── wiki/
  ├── scripts/
  └── tests/
        ↓
  CI 验证
  ├── lint
  ├── 规则检查
  └── 测试
```

---

## 2. 五种输入源对应五种 Agent 角色

| 输入源         | Agent 角色        | 产出               | 目标文件                   |
| -------------- | ----------------- | ------------------ | -------------------------- |
| 事故报告       | 事故反推 Agent    | 硬约束规则         | rules/coding-standard.md   |
| Code Review    | Review 提炼 Agent | 编码规范           | rules/coding-standard.md   |
| 架构文档       | 架构解析 Agent    | 分层规则           | rules/project-structure.md |
| DDL / 接口文档 | 数据建模 Agent    | 数据模型、业务流程 | wiki/                      |
| 代码库         | 代码考古 Agent    | 模板、反例、正例   | skills/coding/             |
| CI 配置        | 门禁解析 Agent    | 门禁脚本           | scripts/、CI               |

---

## 3. 事故反推 Agent：最厚实的来源

### 输入

```text
你项目过去 6-12 个月的事故报告、复盘文档、故障工单。
格式不限：Markdown、Word、Confluence 导出、Jira 导出都行。
```

### 输入目录约定

```bash
mkdir -p harness/sources/incidents
# 把事故报告放进去
harness/sources/incidents/INC-2024-0312.md
harness/sources/incidents/INC-2024-0421.md
...
```

### Agent Prompt 模板

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
按以下模板输出，每条规则一个块：

---
## 规则 ID: <模块>-<序号>
### 规则
<一句话规则>
### 原因
<事故编号、日期、现象、根因、损失>
### 反例
```python
<反例代码>
```
### 正例
```python
<正例代码>
### 检查
<脚本路径或 lint 规则>
### 测试
<测试文件路径>
### 优先级
<P0/P1/P2>
### Owner
<待填>
---

## 硬性约束
- 不允许编造事故。
- 不允许写没有事故支撑的规则。
- 如果一条事故无法转成规则，明确写“无法转化”并说明原因。
- 如果一条事故能转成多条规则，拆开写。
```

### 输出示例

```markdown
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
scripts/check_python_rules.py（已实现 HTTP timeout 检查）
### 测试
tests/payment/test_callback.py::test_timeout_marks_pending
### 优先级
P0
### Owner
待填

### 人工审核清单

- [ ] 每条规则都有事故编号
- [ ] 事故编号能在事故库里查到
- [ ] 反例和正例能跑通
- [ ] 检查脚本能实现
- [ ] 测试能写出来
- [ ] 优先级合理

### 回填动作

```bash
# Agent 输出到
harness/sources/incidents/extracted-rules.md

# 人工审核后合并到
harness/rules/coding-standard.md

# 检查脚本更新
scripts/check_python_rules.py

# 测试更新
tests/
```

---

## 4. Code Review 提炼 Agent：高频规则来源

### 输入

```bash
mkdir -p harness/sources/reviews
# 从 GitHub PR 导出 Review 意见
gh pr list --state merged --limit 200 --json number,title
# 逐个导出
gh pr view <number> --comments > harness/sources/reviews/PR-<number>.md
```

### Agent Prompt 模板

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
| ------- | ---- | -------- | ------- | -------- | -------- | ------ |

## 对重复 3 次以上的意见，展开六件套：
规则、原因、反例、正例、检查、测试。

## 硬性约束
- 只提取重复出现的意见。
- 只出现 1 次的写进“观察池”，不写成规则。
- 不允许编造 PR。
- 每条规则必须列出至少 3 个来源 PR。
```

### 输出示例

```markdown
| 规则 ID  | 规则                          | 出现次数 | 来源 PR           | 可程序化 | 目标文件                  | 优先级 |
| -------- | ----------------------------- | -------- | ----------------- | -------- | ------------------------- | ------ |
| API-001  | api 层禁止直接访问 repository | 12       | #101,#108,#115... | 是       | python-layers.md          | P0     |
| LOG-001  | 禁止 print，必须用 logging    | 8        | #98,#120,#133...  | 是       | python-coding-standard.md | P1     |
| TEST-001 | 新增接口必须新增测试          | 15       | #90,#99,#110...   | 是       | dev-process.md            | P0     |
| CFG-001  | 配置禁止硬编码                | 6        | #88,#105,#121...  | 是       | python-coding-standard.md | P0     |
```

### 人工审核

- [ ] 出现次数统计准确
- [ ] 来源 PR 可查
- [ ] 规则可程序化
- [ ] 没有把一次性意见写成规则

---

## 5. 架构解析 Agent：分层规则来源

### 输入

```bash
mkdir -p harness/sources/architecture
# 放入
harness/sources/architecture/module-list.md
harness/sources/architecture/package-structure.md
harness/sources/architecture/dependency-graph.png
```

### 更直接的方式：让 Agent 读代码库

```text
你是 Harness 架构解析 Agent。

## 任务
阅读 src/ 目录下的代码结构，
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
```

### 输出示例

```markdown
## 违规清单
| 文件               | 行号 | 违规 import                                | 违反规则                    |
| ------------------ | ---- | ------------------------------------------ | --------------------------- |
| src/api/order.py   | 12   | from src.repository.order import OrderRepo | api 不得直接依赖 repository |
| src/domain/user.py | 8    | from sqlalchemy import Column              | domain 不得依赖 ORM         |
| src/service/pay.py | 30   | import requests                            | service 不得直接 HTTP       |

## 建议规则
## 规则 ID: LAYER-001
### 规则
api 层禁止直接 import repository。
### 原因
架构评审 2024-06，api 直接访问 DB 导致事务边界混乱。
### 检查
scripts/check_layers.py
### 测试
tests/architecture/test_layers.py
```

### 检查脚本自动生成

Agent 可以顺带生成：

```python
# scripts/check_layers.py
import ast
from pathlib import Path

RULES = [
    ("src/api", "src.repository", "api 不得直接依赖 repository"),
    ("src/domain", "sqlalchemy", "domain 不得依赖 ORM"),
    ("src/service", "requests", "service 不得直接 HTTP"),
]

def check_imports(root: Path) -> list[str]:
    errors = []
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for prefix, banned, msg in RULES:
                        if str(path).startswith(prefix) and alias.name.startswith(banned):
                            errors.append(f"{path}:{node.lineno} {msg}")
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    for prefix, banned, msg in RULES:
                        if str(path).startswith(prefix) and node.module.startswith(banned):
                            errors.append(f"{path}:{node.lineno} {msg}")
    return errors
```

---

## 6. 数据建模 Agent：Wiki 来源

### 输入

```bash
harness/sources/ddl/schema.sql
harness/sources/api/openapi.yaml
harness/sources/flows/order-flow.md
```

### Agent Prompt

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
- 缺失信息写“待补充”。
```

---

## 7. 代码考古 Agent：模板与反例来源

### Prompt

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
### 每层模板
### 每层反例
### 建议规则
```

### 输出示例

```markdown
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
```

---

## 8. 门禁解析 Agent：CI 来源

### Prompt

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

### 输出示例

```markdown
| 门禁     | 命令                                  | 通过条件  | 失败回退 | 对应规则  |
| -------- | ------------------------------------- | --------- | -------- | --------- |
| 类型检查 | mypy src                              | exit 0    | 回退编码 | TYPE-001  |
| 金额检查 | python scripts/check_python_rules.py  | 无输出    | 回退编码 | PRICE-001 |
| 测试数   | python scripts/check_pytest_report.py | total > 0 | 回退单测 | TEST-001  |
| 覆盖率   | pytest --cov-fail-under=80            | exit 0    | 回退单测 | TEST-002  |
```

---

## 9. 编排：让 Agent 按顺序跑

创建编排脚本：

```bash
mkdir -p harness/agents
cat > harness/agents/fill-harness.md <<'EOF'
# Harness 填充编排

## 执行顺序

1. 架构解析 Agent → rules/project-structure.md
2. 事故反推 Agent → rules/coding-standard.md
3. Review 提炼 Agent → rules/coding-standard.md
4. 代码考古 Agent → skills/coding/
5. 数据建模 Agent → wiki/
6. 门禁解析 Agent → scripts/、CI

## 每步之后

- 人工审核
- 合并到目标文件
- 更新检查脚本
- 更新测试
- 提交

## 禁止

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main 分支。
- 不允许无来源规则进入 Harness。
EOF
```

每个 Agent 一个分支：

```bash
git checkout -b agent/incident-extraction
# 跑事故反推 Agent
git add harness/sources/incidents/extracted-rules.md
git commit -m "agent: extract rules from incidents"
gh pr create --title "Agent: Incident Rule Extraction"
```

---

## 10. 人工审核是必须的

Agent 填充的最大风险是**编造**。审核清单：

| 检查项     | 通过标准                     |
| ---------- | ---------------------------- |
| 来源真实性 | 每条规则能追溯到事故/PR/文档 |
| 反例可运行 | 反例代码能跑出问题           |
| 正例可运行 | 正例代码能通过检查           |
| 检查可执行 | 脚本能跑，能拦               |
| 测试可跑   | 测试能跑，能失败             |
| 优先级合理 | P0 是硬约束，P2 是建议       |
| Owner 明确 | 每条规则有人负责             |

审核不通过 → 打回 Agent 重做。

---

## 11. 防止 Agent 编造的三道闸

### 闸一：来源强制

```text
每条规则必须有来源字段。
来源为空 → 直接拒绝。
来源查不到 → 直接拒绝。
```

### 闸二：可执行强制

```text
每条规则必须有检查命令。
检查命令跑不通 → 直接拒绝。
检查命令跑通但拦不住反例 → 直接拒绝。
```

### 闸三：测试强制

```text
每条 P0 规则必须有测试。
测试必须能失败。
测试必须能通过。
```

---

## 12. 完整示例：从事故到规则

### 输入

```markdown
# INC-2024-0421

日期：2024-04-21
模块：支付
现象：支付回调堆积 3 小时
根因：service 直接调 HTTP，未设 timeout
影响：1.2 万笔订单，损失约 8 万
修复：加 timeout，加 pending 补偿
```

### Agent 输出

```markdown
## 规则 ID: PAY-001
### 规则
支付回调必须设 timeout，超时后标记 pending 并异步补偿。
### 原因
INC-2024-0421，2024-04-21，支付回调堆积 3 小时，
根因 service 直接调 HTTP 未设 timeout，
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
scripts/check_python_rules.py
### 测试
tests/payment/test_callback.py::test_timeout_marks_pending
### 优先级
P0
### Owner
支付组

### 回填

```bash
# 1. 追加到规则文件
cat extracted-rule.md >> harness/rules/coding-standard.md

# 2. 更新检查脚本
# scripts/check_python_rules.py 已支持 HTTP timeout 检查

# 3. 新增测试
cat > tests/payment/test_callback.py <<'EOF'
def test_timeout_marks_pending(mock_http_timeout, order):
    with pytest.raises(requests.Timeout):
        service.charge(order.id, order.amount_cents)
    assert order.status == "pending"
EOF

# 4. 提交
git add .
git commit -m "rule: add PAY-001 from INC-2024-0421"
git push
```

---

## 13. 你要做的具体动作

### 动作 1：建来源池

```bash
mkdir -p harness/sources/{incidents,reviews,architecture,ddl,api,flows,code}
```

### 动作 2：导入真实资料

| 来源   | 命令                                            |
| ------ | ----------------------------------------------- |
| 事故   | 从 Jira/Confluence 导出到 incidents/            |
| Review | `gh pr view <n> --comments > reviews/PR-<n>.md` |
| 架构   | 从 Wiki 导出到 architecture/                    |
| DDL    | 从数据库导出到 ddl/                             |
| 接口   | 从 Swagger 导出到 api/                          |
| 流程   | 从文档导出到 flows/                             |
| 代码   | 直接指向 src/                                   |

### 动作 3：跑 Agent

按顺序：

```text
1. 架构解析 Agent
2. 事故反推 Agent
3. Review 提炼 Agent
4. 代码考古 Agent
5. 数据建模 Agent
6. 门禁解析 Agent
```

每个 Agent 一个分支，一个 PR。

### 动作 4：人工审核

每个 PR 用审核清单过一遍。

### 动作 5：合并回填

审核通过后合并到 main。

### 动作 6：CI 验证

```bash
make gate
```

---

## 14. 一句话总结

**Agent 填充 Harness 的公式：**

```text
真实来源 + 结构化 Prompt + 六件套输出 + 人工审核 + 可执行检查 = 厚实规则


没有来源，Agent 就编。  
没有审核，规则就假。  
没有检查，规则就空。  
没有测试，规则就死。
```

---

下一步给我以下任意一项，写出对应 Agent 的完整 Prompt 和示例输出：

1. 你项目的一个真实事故报告；
2. 你项目的 10 条真实 Review 意见；
3. 你项目的目录结构；
4. 你项目的 DDL；
5. 你项目的 CI 配置。