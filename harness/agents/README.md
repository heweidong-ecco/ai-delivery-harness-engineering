# 填充 Agent 索引

## 一、核心 Agent（6 个，必须）

| Agent       | 文件                      | 输入                | 输出                  | 分支                   |
| ----------- | ------------------------- | ------------------- | --------------------- | ---------------------- |
| 架构解析    | architecture-agent.md     | architecture/、src/ | extracted-rules.md    | agent/architecture     |
| 事故反推    | incident-agent.md         | incidents/          | extracted-rules.md    | agent/incident         |
| Review 提炼 | review-agent.md           | reviews/            | extracted-rules.md    | agent/review           |
| 代码考古    | code-archaeology-agent.md | src/                | extracted-patterns.md | agent/code-archaeology |
| 数据建模    | data-modeling-agent.md    | ddl/、api/、flows/  | wiki/                 | agent/data-modeling    |
| 门禁解析    | gate-agent.md             | CI、Makefile        | extracted-gates.md    | agent/gate             |

## 二、扩展 Agent（5 个，可选）

| Agent | 文件                 | 输入               | 输出                    | 分支              |
| ----- | -------------------- | ------------------ | ----------------------- | ----------------- |
| 安全  | security-agent.md    | 安全审计、威胁模型 | security-standard.md    | agent/security    |
| 性能  | performance-agent.md | 性能事故、监控     | performance-standard.md | agent/performance |
| 重构  | refactor-agent.md    | src/、反模式       | anti-patterns.md        | agent/refactor    |
| 依赖  | dependency-agent.md  | pyproject.toml     | dependency-standard.md  | agent/dependency  |
| 文档  | doc-agent.md         | src/、changes/     | docs/                   | agent/doc         |

## 三、编排 Agent（3 个）

| Agent             | 文件                          | 作用           |
| ----------------- | ----------------------------- | -------------- |
| Orchestrator      | orchestrator.md               | 调度全部 Agent |
| Fill Harness      | fill-harness.md               | 填充总纲       |
| Application Owner | ../agent/application-owner.md | 需求编排       |

## 四、执行顺序

```text
阶段 1（必须）：架构 → 事故 → Review → 代码考古 → 数据建模 → 门禁
阶段 2（可选）：安全 → 性能 → 重构 → 依赖 → 文档
阶段 3（编排）：Orchestrator 调度全部
```

## 五、每个 Agent 的硬性约束

- 不允许编造来源。
- 每条规则必须有来源。
- 每条规则必须可程序化验证。
- 每条 P0 规则必须有测试。
- 不允许跳过人工审核。
- 不允许 Agent 直接改 main。
- 每个 Agent 独立分支、独立 PR。
- 缺失信息写"待补充"，不编造。

## 六、Agent 输出通用格式

```markdown
## 规则 ID: <DOMAIN>-<NNN>

### 规则
<一句话>

### 原因
<来源：事故编号/PR 编号/文档路径>

### 反例
```python
<错误代码>
```

### 正例
```python
<正确代码>
```

### 检查
<脚本路径>

### 测试
<测试路径>

### 优先级
P0/P1/P2

### Owner
<待填>

### 来源
<来源路径>

## 七、人工审核要点

- 来源真实性
- 反例可运行
- 正例可运行
- 检查可执行
- 测试可跑
- 优先级合理
- Owner 明确

## 八、禁止事项

- 无来源规则
- 不可验证规则
- 无测试 P0 规则
- 编造事故
- 编造 PR
- 提交密钥
- 提交真实数据
- 跳过人工审核
- 直接改 main
