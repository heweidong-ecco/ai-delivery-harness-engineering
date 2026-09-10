# 填充指南

## 目标

用 Agent 从真实来源提取规则，填充 Harness。

核心公式：

```text
真实来源 + 结构化 Prompt + 六件套输出 + 人工审核 + 可执行检查 = 厚实规则
```

---

## 一、执行阶段

### 阶段 1：核心 6 个 Agent（必须）

| 顺序 | Agent       | 输入                | 输出                       |
| ---- | ----------- | ------------------- | -------------------------- |
| 1    | 架构解析    | architecture/、src/ | rules/project-structure.md |
| 2    | 事故反推    | incidents/          | rules/coding-standard.md   |
| 3    | Review 提炼 | reviews/            | rules/coding-standard.md   |
| 4    | 代码考古    | src/                | skills/coding/             |
| 5    | 数据建模    | ddl/、api/、flows/  | wiki/                      |
| 6    | 门禁解析    | CI、Makefile        | scripts/、CI               |

### 阶段 2：扩展 5 个 Agent（可选）

| 顺序 | Agent | 输入               | 输出                          |
| ---- | ----- | ------------------ | ----------------------------- |
| 7    | 安全  | 安全审计、威胁模型 | rules/security-standard.md    |
| 8    | 性能  | 性能事故、监控     | rules/performance-standard.md |
| 9    | 重构  | src/、反模式       | docs/anti-patterns.md         |
| 10   | 依赖  | pyproject.toml     | rules/dependency-standard.md  |
| 11   | 文档  | src/、changes/     | docs/                         |

### 阶段 3：编排

| Agent        | 作用           |
| ------------ | -------------- |
| Orchestrator | 调度全部 Agent |
| Fill Harness | 填充总纲       |

---

## 二、每步流程

```text
1. 来源放入 harness/sources/<type>/
2. 跑对应 Agent
3. Agent 输出到 harness/sources/<type>/extracted-*.md
4. 人工审核
5. 合并到目标文件
6. 更新检查脚本
7. 更新测试
8. 提交 PR
```

---

## 三、来源要求

| 来源        | 目录              | 脱敏 |
| ----------- | ----------------- | ---- |
| 事故报告    | incidents/        | 必须 |
| Review 意见 | reviews/          | 必须 |
| 架构文档    | architecture/     | 必须 |
| DDL         | ddl/              | 必须 |
| 接口文档    | api/              | 必须 |
| 流程图      | flows/            | 必须 |
| 代码库      | code/ 或直接 src/ | 必须 |

### 硬性约束

- 每条规则必须有来源。
- 来源为空则拒绝。
- 来源必须可查。
- 来源必须脱敏。

---

## 四、三道防编造闸

### 闸 1：来源强制

```text
每条规则必须有 source 字段。
source 为空 → 直接拒绝。
source 查不到 → 直接拒绝。
```

### 闸 2：可执行强制

```text
每条规则必须有检查命令。
检查命令跑不通 → 直接拒绝。
检查命令跑通但拦不住反例 → 直接拒绝。
```

### 闸 3：测试强制

```text
每条 P0 规则必须有测试。
测试必须能失败。
测试必须能通过。
```

---

## 五、人工审核清单

- [ ] 每条规则有来源
- [ ] 来源可查
- [ ] 反例能跑出问题
- [ ] 正例能通过检查
- [ ] 检查脚本能拦
- [ ] 测试能失败也能通过
- [ ] 优先级合理
- [ ] Owner 明确

---

## 六、每个 Agent 的独立操作

### Agent 1：架构解析

```bash
git checkout -b agent/architecture
# 放入 sources/architecture/
# 跑 Agent
# 输出 sources/architecture/extracted-rules.md
# 人工审核
# 合并到 rules/project-structure.md
git commit -m "agent: extract architecture rules"
git push -u origin agent/architecture
gh pr create --title "Agent: Architecture" --body "架构解析"
```

### Agent 2：事故反推

```bash
git checkout -b agent/incident
# 放入 sources/incidents/
# 跑 Agent
# 输出 sources/incidents/extracted-rules.md
# 人工审核
# 合并到 rules/coding-standard.md
git commit -m "agent: extract incident rules"
git push -u origin agent/incident
gh pr create --title "Agent: Incident" --body "事故反推"
```

### Agent 3：Review 提炼

```bash
git checkout -b agent/review
# 放入 sources/reviews/
# 跑 Agent
# 输出 sources/reviews/extracted-rules.md
# 人工审核
# 合并到 rules/coding-standard.md
git commit -m "agent: extract review rules"
git push -u origin agent/review
gh pr create --title "Agent: Review" --body "Review 提炼"
```

### Agent 4：代码考古

```bash
git checkout -b agent/code-archaeology
# 指向 src/
# 跑 Agent
# 输出 sources/code/extracted-patterns.md
# 人工审核
# 合并到 skills/coding/
git commit -m "agent: extract code patterns"
git push -u origin agent/code-archaeology
gh pr create --title "Agent: Code Archaeology" --body "代码考古"
```

### Agent 5：数据建模

```bash
git checkout -b agent/data-modeling
# 放入 sources/ddl/、api/、flows/
# 跑 Agent
# 输出 wiki/data-model.md、wiki/business-flows.md
# 人工审核
git commit -m "agent: extract data model and flows"
git push -u origin agent/data-modeling
gh pr create --title "Agent: Data Modeling" --body "数据建模"
```

### Agent 6：门禁解析

```bash
git checkout -b agent/gate
# 读 CI、Makefile、pyproject.toml
# 跑 Agent
# 输出 sources/architecture/extracted-gates.md
# 人工审核
# 合并到 scripts/、CI
git commit -m "agent: extract gates"
git push -u origin agent/gate
gh pr create --title "Agent: Gate" --body "门禁解析"
```

---

## 七、禁止事项

- 不允许跳过人工审核。
- 不允许 Agent 直接改 main。
- 不允许无来源规则进入 Harness。
- 不允许不可验证规则进入 Harness。
- 不允许无测试 P0 规则进入 Harness。
- 不允许编造事故、PR、模块、字段。
- 不允许提交密钥、真实数据、生产配置。

---

## 八、完成后验证

```bash
# 1. 跑门禁
make gate

# 2. 检查文档完整性
python scripts/check_harness_docs.py

# 3. 检查规则来源
grep -r "source:" harness/rules/ | wc -l

# 4. 检查规则检查脚本
grep -r "check:" harness/rules/ | wc -l

# 5. 检查规则测试
grep -r "test:" harness/rules/ | wc -l
```

---

## 九、填充完成标准

| 维度              | 标准       |
| ----------------- | ---------- |
| 规则条数          | >= 30      |
| 规则来源覆盖率    | 100%       |
| 规则可程序化率    | 100%       |
| P0 规则测试覆盖率 | 100%       |
| Wiki 完整度       | >= 80%     |
| Agent 输出已审核  | 100%       |
| 无待填占位符      | 核心文件 0 |

---
