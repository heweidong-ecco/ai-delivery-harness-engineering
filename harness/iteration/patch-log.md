# Harness Patch 记录

## 一、说明

每次实战发现新问题，立即 Patch 到 Harness。

> **规范的每一行都对应一个历史失败案例。**

当你觉得某条规则多余或啰嗦时，往往是它背后有一个真实踩过的坑。

---

## 二、Patch 流程

```text
1. 发现问题
   ├── 空跑发现
   ├── 实战发现
   ├── 事故复盘
   └── Review 意见

2. 记录到 patch-log.md
   ├── 日期
   ├── 来源
   ├── 问题
   └── 优先级

3. 写规则
   ├── 规则 ID
   ├── 原因
   ├── 反例
   ├── 正例
   └── 来源

4. 写检查脚本
   ├── 脚本路径
   ├── 规则 ID
   └── 可程序化验证

5. 写测试
   ├── 测试文件
   ├── 能失败
   └── 能通过

6. 提交 PR
   ├── 分支：rule/<id>
   ├── 提交信息：rule: add <ID>
   └── PR 描述：附来源

7. 审核
   ├── 来源真实性
   ├── 可程序化
   ├── 可测试
   ├── 优先级
   └── Owner

8. 合并
   ├── CI 通过
   ├── 人工审核通过
   └── 合并到 main
```

---

## 三、Patch 记录表

| 日期   | 来源               | 问题   | Patch        | 目标文件 | 提交     | 审核人 |
| ------ | ------------------ | ------ | ------------ | -------- | -------- | ------ |
| <日期> | <事故/Review/空跑> | <问题> | <Patch 内容> | <文件>   | <commit> | <待填> |

### 示例

| 日期       | 来源          | 问题                            | Patch                          | 目标文件                        | 提交   | 审核人 |
| ---------- | ------------- | ------------------------------- | ------------------------------ | ------------------------------- | ------ | ------ |
| 2024-XX-XX | 空跑 REQ-0000 | CI 只检查状态码，忽略测试数为 0 | 增加 TotalTest>0、Passed=Total | scripts/check_pytest_report.py  | abc123 | <待填> |
| 2024-XX-XX | INC-2024-0312 | 价格用 float 导致对账差异       | 增加 PRICE-001                 | rules/python-coding-standard.md | def456 | <待填> |
| 2024-XX-XX | PR #101       | api 层直接访问 repository       | 增加 LAYER-001                 | rules/python-layers.md          | ghi789 | <待填> |

---

## 四、待 Patch 清单

> **2026-09-11 外审录入**:来源 = 外部项目 `agent-eval-gate` 通读本仓设计文档 + 逐个核对实际落地文件后出具。
> **完整工单(含证据:行号、影响、最小修复)见 `.claude/AUDIT-外审记录与修正建议.md`**;
> 本表只登记条目,细节以该工单为准。所有条目均**尚未处理**。

| 问题 | 来源 | 优先级 | 状态 | 负责人 |
| ---- | ---- | ------ | ---- | ------ |
| **H1** `scripts/check_harness_docs.py:1` 是 markdown 围栏(```` ```python ````)→ SyntaxError → **该脚本永不执行**;而它被 `Makefile:76` 与 `harness-ci.yml:55` 调用 → **`make gate` 与 CI 从未绿过** | 外审 | **P0** | 待处理 | <待填> |
| **H2** 同文件 REQUIRED 清单含 6 个不存在的路径(`.github/CODEOWNERS:40`、`.github/dependabot.yml:41`、`harness/rules/logging-standard.md:83`、`harness/agent/application-owner.md:148`、`harness/agent/application-owner-python.md:149`、`scripts/check_gates.sh:224` ← 实际是连字符) | 外审 | **P0** | 待处理 | <待填> |
| **H3** `tests/test_scripts.py:316-326` 用 `pytest.skip` 给坏门禁兜底(「门禁坏了就跳过它」);`:334-357` 调用不存在的脚本 → 套件红 | 外审 | **P0** | 待处理 | <待填> |
| **H4** 状态机**只写不校验**:`scripts/state_tracker.py:20-30` 只 append history,全仓无消费者 → 「十阶段不可跳过」是口号 | 外审 | **P1** | 待处理 | <待填> |
| **H5** 阶段门 `check-gates.sh:10-24` 是**一次性查全部产出物**,且**未挂 Makefile/CI/pre-commit 任何一处** → 「长任务中间全白费」 | 外审 | **P1** | 待处理 | <待填> |
| **H6** 空壳门禁:`check_layers.py:6-10` RULES 为空;`validate_schemas.py` 校验目录不存在 + jsonschema 未声明 → 永远空转(**比没有更坏**) | 外审 | **P1** | 待处理 | <待填> |
| **H7** 设计稿放错目录 = 永不生效:`harness/workflows/*.yml`(5 个)、`.github/ISSUE_TEMPLATE/{CODEOWNERS,dependabot.yml}` | 外审 | **P1** | 待处理 | <待填> |
| **H8** 观测纯装饰:`config/` 零消费者、grafana panel 无 datasource/query、指标名不存在、**无熔断无停** | 外审 | **P2** | 待处理 | <待填> |
| **H9** `validate_schemas.py:5-9` jsonschema 未装时 `exit(0)`(缺依赖应 fail) | 外审 | **P2** | 待处理 | <待填> |
| **H10** `rule-schema.json:13` 的 `test` 不在 required → 「P0 必须有测试」未强制 | 外审 | **P2** | 待处理 | <待填> |
| **H11** `pip-audit --strict \|\| true`(CI)与 `check_dependencies.py`(真 fail)语义矛盾 | 外审 | **P2** | 待处理 | <待填> |
| **H12** `Makefile:65,68,71` 的 audit/markdownlint/yamllint 带 `\|\| true` → 永不失败 | 外审 | **P2** | 待处理 | <待填> |
| **H13** **pre-commit 里没有 pytest / 覆盖率** → 「跑测试」这条最重要的纪律在提交环节没有门 | 外审 | **P2** | 待处理 | <待填> |
| **H14** `.importlinter` 定义分层契约但全仓无任何地方运行 `import-linter` | 外审 | **P2** | 待处理 | <待填> |

**建议处理顺序**(工单 §7):`H1→H3`(先把坏门禁救活,并保证**再坏会被发现**)→ `H2` → `H5→H4`(增量阶段门 + 真状态机)→ 其余 → `H8`。

**修完一条请更新状态**;全部修完在 `.claude/AUDIT-外审记录与修正建议.md` 头部加 `[已修]`(SessionStart 提示会自动关闭)。

---

## 五、已 Patch 清单

| 问题   | 来源   | Patch   | 日期   | 提交     |
| ------ | ------ | ------- | ------ | -------- |
| <问题> | <来源> | <Patch> | <日期> | <commit> |

---

## 六、Patch 优先级

| 优先级 | 条件     | 处理时限  |
| ------ | -------- | --------- |
| P0     | 阻塞上线 | 24 小时内 |
| P1     | 本轮修完 | 本周内    |
| P2     | 后续优化 | 本月内    |

---

## 七、Patch 规则

### 必须

- 每次实战问题必须 Patch。
- Patch 必须可程序化验证。
- Patch 必须更新测试。
- Patch 必须提交 PR。
- Patch 必须有人审核。
- Patch 必须有来源。
- Patch 必须更新 CHANGELOG。

### 禁止

- 禁止无来源 Patch。
- 禁止不可验证 Patch。
- 禁止无测试 P0 Patch。
- 禁止跳过 CI。
- 禁止 Agent 直接改 main。

---

## 八、Patch 统计

| 月份    | P0  | P1  | P2  | 合计 |
| ------- | --- | --- | --- | ---- |
| 2024-01 | 0   | 0   | 0   | 0    |
| 2024-02 | 0   | 0   | 0   | 0    |

### 趋势

```text
P0  →  递减
P1  →  递减
P2  →  稳定
总  →  递减（Harness 成熟）
```

---

## 九、复盘

### 月度复盘

| 月份    | 新增规则 | 修改规则 | 废弃规则 | 事故数 | 返工轮次 |
| ------- | -------- | -------- | -------- | ------ | -------- |
| 2024-01 | 0        | 0        | 0        | 0      | 0        |

### 复盘要点

1. 哪些规则拦住了事故？
2. 哪些事故没被规则拦住？
3. 哪些规则冗余？
4. 哪些规则需要细化？
5. Agent 表现如何？

---

## 十、填充指南

- 来源：实战问题、事故、Review、空跑
- 填充 Agent：事故反推 Agent、Review 提炼 Agent
- 审核要点：
  - 来源是否真实
  - Patch 是否可程序化
  - 测试是否可跑
  - 优先级是否合理
  - Owner 是否明确
