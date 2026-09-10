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
| **H1** `scripts/check_harness_docs.py:1` 是 markdown 围栏(```` ```python ````)→ SyntaxError → **该脚本永不执行**;而它被 `Makefile:76` 与 `harness-ci.yml:55` 调用 → **`make gate` 与 CI 从未绿过** | 外审 | **P0** | ✅ 已修 | Claude Code |
| **H2** 同文件 REQUIRED 清单含 6 个不存在的路径(`.github/CODEOWNERS:40`、`.github/dependabot.yml:41`、`harness/rules/logging-standard.md:83`、`harness/agent/application-owner.md:148`、`harness/agent/application-owner-python.md:149`、`scripts/check_gates.sh:224` ← 实际是连字符) | 外审 | **P0** | ✅ 已修 | Claude Code |
| **H3** `tests/test_scripts.py:316-326` 用 `pytest.skip` 给坏门禁兜底(「门禁坏了就跳过它」);`:334-357` 调用不存在的脚本 → 套件红 | 外审 | **P0** | ✅ 已修 | Claude Code |
| **H4** 状态机**只写不校验**:`scripts/state_tracker.py:20-30` 只 append history,全仓无消费者 → 「十阶段不可跳过」是口号 | 外审 | **P1** | ✅ 已修 | Claude Code |
| **H5** 阶段门 `check-gates.sh:10-24` 是**一次性查全部产出物**,且**未挂 Makefile/CI/pre-commit 任何一处** → 「长任务中间全白费」 | 外审 | **P1** | ✅ 已修 | Claude Code |
| **H6** 空壳门禁:`check_layers.py:6-10` RULES 为空;`validate_schemas.py` 校验目录不存在 + jsonschema 未声明 → 永远空转(**比没有更坏**) | 外审 | **P1** | ✅ 已修 | Claude Code |
| **H7** 设计稿放错目录 = 永不生效:`harness/workflows/*.yml`(5 个)、`.github/ISSUE_TEMPLATE/{CODEOWNERS,dependabot.yml}` | 外审 | **P1** | ✅ 已修 | Claude Code |
| **H8** 观测纯装饰:`config/` 零消费者、grafana panel 无 datasource/query、指标名不存在、**无熔断无停** | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H9** `validate_schemas.py:5-9` jsonschema 未装时 `exit(0)`(缺依赖应 fail) | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H10** `rule-schema.json:13` 的 `test` 不在 required → 「P0 必须有测试」未强制 | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H11** `pip-audit --strict \|\| true`(CI)与 `check_dependencies.py`(真 fail)语义矛盾 | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H12** `Makefile:65,68,71` 的 audit/markdownlint/yamllint 带 `\|\| true` → 永不失败 | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H13** **pre-commit 里没有 pytest / 覆盖率** → 「跑测试」这条最重要的纪律在提交环节没有门 | 外审 | **P2** | ✅ 已修 | Claude Code |
| **H14** `.importlinter` 定义分层契约但全仓无任何地方运行 `import-linter` | 外审 | **P2** | ✅ 已修 | Claude Code |

**处理顺序**(工单 §7):`H1→H3` → `H2` → `H5→H4` → 其余 → `H8`。**H1–H14 全部处理完毕**,详见 §五「已 Patch 清单」。

### 4.1 修正过程中**另外发现**的缺陷(外审工单未列,一并修掉)

> 这些是"修完 H1–H14 后 `make gate` 仍然红"才暴露出来的 —— 说明外审抓的是**第一层**,
> 底下还压着**同类**的病。记录在此,以避免"修完清单就以为好了"。

| 编号 | 问题 | 证据 | 状态 |
| ---- | ---- | ---- | ---- |
| **X1** | **ruff 从第一步就红**:`select` 含 `T20`(禁 print),而 `scripts/` 全是 CLI,实测 72 条 `print` → **`make gate` 与 CI 的 lint 步从未绿过** | `pyproject.toml` `[tool.ruff.lint]` | ✅ 已修(按目录放行 `scripts/*`、`tests/*`) |
| **X2** | **覆盖率门禁测不到任何东西**:`source = src`(骨架期为空)+ 测试全部用 subprocess 驱动 → 实测 **741 条语句 0.00%**,`--cov-fail-under=80` 永远失败 | `.coveragerc`、`tests/conftest.py` | ✅ 已修(启用 subprocess 覆盖率,实测 84%) |
| **X3** | **测试套件根本收集不起来**:`tests/conftest.py` 的 fixture 名为 `pytest_report_*`,pytest 把 conftest 里所有 `pytest_*` 函数当 **hook** 注册 → `PluginValidationError` | `tests/conftest.py` | ✅ 已修(改名 `passed_report` 等) |
| **X4** | **密钥扫描拦自己的测试夹具**:`check_secrets.py` 无行级豁免,只能整文件跳过 → 给测试文件开永久盲区 | `scripts/check_secrets.py` | ✅ 已修(加 `pragma: allowlist secret`) |
| **X5** | **文档树与实际不符**:README 把 `harness/agent/`(单数)与 `harness/agents/`(复数)写成**两个目录**(实际只有一个);漏 `glossary/`、`pilot/`、`docs/freeze.md` | `README.md` §六 | ✅ 已修 |
| **X6** | **6 个文件代码围栏"开了没关"**,其中 2 个是 ` ```markdown ` 里套 ` ```python ` → 内层把外层闭掉,后面整段渲染错位 | `FillWorkflow.md`、`harness/agents/README.md`、`harness/audit/README.md`、`harness/changes/README.md`、`harness/checkpoints/README.md`、`docs/tutorials/first-requirement.md` | ✅ 已修 + **已加门禁** |
| **X7** | **`docs/fill-workflow.md` 不存在**(4 处引用);`harness/agent/` 单数引用 8 处;`harness/agents/README.md:30` 指向 `../agent/` | USAGE/README/BluePrint/architecture.md | ✅ 已修 |
| **X8** | **`logging-standard.md` 被 6 处引用但不存在**(骨架承诺 20 份规则、实交 19 份);`python-coding-standard.md` 是**两份文档拼接**(正文 + 重复的"（模板）"副本) | CHANGELOG 等 | ✅ 已修 |
| **X9** | **README 冻结状态过期**:banner 仍写"已冻结",而 `docs/freeze.md` 已记录 2026-09-11 解冻;文档尾部还残留**元文本**(教人复制本 README、含 `gh pr create`) | `README.md`、`FillWorkflow.md` | ✅ 已修 |
| **X10** | **`harness/agents/1.md`** 是 0 字节孤儿文件(全仓无引用) | — | ✅ 已删(经业主确认) |

**建议处理顺序**(工单 §7):`H1→H3`(先把坏门禁救活,并保证**再坏会被发现**)→ `H2` → `H5→H4`(增量阶段门 + 真状态机)→ 其余 → `H8`。

**修完一条请更新状态**;全部修完在 `.claude/AUDIT-外审记录与修正建议.md` 头部加 `[已修]`(SessionStart 提示会自动关闭)。

---

## 五、已 Patch 清单

| 问题 | 来源 | Patch | 日期 | 提交 |
| ---- | ---- | ----- | ---- | ---- |
| **H1** 门禁脚本首行是 markdown 围栏 → 永不执行 | 外审 | 删围栏;补套件级防腐测试(`tests/test_gates.py`:语法 / 可执行位 / 已注册 / 该拦必拦 + 反向验证) | 2026-09-11 | 本次提交 |
| **H2** 硬编码 181 条路径(6 条不存在) | 外审 | `check_harness_docs.py` 改「锚点文件 + 目录 glob + 文档形状 + 围栏配平」四层,并加 `--root` 便于测试 | 2026-09-11 | 本次提交 |
| **H3** 测试用 `pytest.skip` 给坏门禁兜底 | 外审 | 删 skip;重写为断言"它真的会拦";修正 `check_gates.sh` 下划线 → `check-gates.sh` | 2026-09-11 | 本次提交 |
| **H4** 状态机只写不校验 | 外审 | 新增 `scripts/stage_gate.py`(前置阶段 passed + 产出物**现在依然存在** 才放行;`resume` 从第一个断点续跑);`state_tracker.py` 降级为校验型转发层 | 2026-09-11 | 本次提交 |
| **H5** 阶段门一次性、且不在任何链路里 | 外审 | `check-gates.sh` 改增量门 `--stage N`,清单与 `harness/state/stages.json` **单一来源**(顺带修掉漏检 `review-record-v1.md`);挂进 `make gates` 与 CI | 2026-09-11 | 本次提交 |
| **H6** 空壳门禁(空规则 / 目录不存在) | 外审 | `check_layers.py` 改为读 `.importlinter` 并委托 `lint-imports`;`validate_schemas.py` 改真做 schema 自检;**空转时显式标注 `[UNIMPLEMENTED]`**,不静默通过 | 2026-09-11 | 本次提交 |
| **H7** 设计稿放错目录 | 外审 | 5 个 workflow 移入 `.github/workflows/`;`CODEOWNERS`、`dependabot.yml` 移入 `.github/`(并修 `CODEOWNERS` 里 `/harness/agent/` 死路径) | 2026-09-11 | 本次提交 |
| **H8** 观测纯装饰 | 外审 | `config/` 在 `docs` 与 `README` 中**显式标注为"示例 / 未接线"**,不再让读者以为有观测 | 2026-09-11 | 本次提交 |
| **H9** jsonschema 未装时 `exit(0)` | 外审 | 缺依赖改为 **fail**(并把它与 `import-linter`、`pip-audit` 一起**声明进 dev 依赖**) | 2026-09-11 | 本次提交 |
| **H10** `test` 不在 required | 外审 | 按本仓 doctrine 精确编码:**仅 P0 强制带 `test`**(条件 schema);`source` 进 required | 2026-09-11 | 本次提交 |
| **H11** CI 软、脚本硬 | 外审 | CI 改 `pip-audit --strict`(硬);`dependency-update.yml` 删冗余软审计 | 2026-09-11 | 本次提交 |
| **H12** Makefile `\|\| true` | 外审 | 去掉 audit/markdownlint/yamllint 的软失败;markdownlint/yamllint 复用 pre-commit 里已固定版本的 linter | 2026-09-11 | 本次提交 |
| **H13** pre-commit 无测试门 | 外审 | 加 `pytest` 本地钩子 | 2026-09-11 | 本次提交 |
| **H14** `.importlinter` 无人运行 | 外审 | `import-linter` 进 dev 依赖;由 `check_layers.py` 真正调用(`make layers` / CI 已覆盖) | 2026-09-11 | 本次提交 |
| **X1** ruff 的 `T20` 让 lint 从未绿过 | 修正中发现 | 按目录放行(`scripts/*`、`tests/*` 是 CLI/测试,`T20` 的靶子是 `src/`) | 2026-09-11 | 本次提交 |
| **X2** 覆盖率门禁测不到任何东西(0.00%) | 修正中发现 | 启用 subprocess 覆盖率(`COVERAGE_PROCESS_START` + sitecustomize);阈值移到 `make coverage` 并在骨架期显式标注未实现。实测 84% | 2026-09-11 | 本次提交 |
| **X3** conftest 的 `pytest_*` fixture 让套件收集失败 | 修正中发现 | fixture 改名 | 2026-09-11 | 本次提交 |
| **X4** 密钥扫描拦自己的测试夹具 | 修正中发现 | 加行级豁免 `pragma: allowlist secret`(+ 反向验证测试:豁免不得泄漏到同文件其它行) | 2026-09-11 | 本次提交 |
| **X5–X9** 文档层:目录树与实际不符、6 处围栏不配平、死路径、元文本、冻结状态过期 | 修正中发现 | 逐条修正;并**把"围栏配平 / 嵌套"加进门禁**,防止复发 | 2026-09-11 | 本次提交 |
| **X8** `logging-standard.md` 缺失 | 修正中发现 | 按同级骨架补上(只写**已实现**的 LOG-001,不编造来源) | 2026-09-11 | 本次提交 |
| **X10** `harness/agents/1.md` 0 字节孤儿 | 修正中发现 | 删除(经业主确认) | 2026-09-11 | 本次提交 |

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
| 2026-09 | 3   | 4   | 7   | 14   |

> 2026-09 的 14 条全部来自**外审工单**(`.claude/AUDIT-外审记录与修正建议.md`);
> 另有 **10 条**是修正过程中暴露的同类缺陷(X1–X10,见 §四 4.1),不计入上表。
>
> **这一栏本身就是本仓最该记住的一课**:P0 三条(H1/H2/H3)意味着
> **门禁体系实质失效而无人知晓** —— 不是"规则不够",而是**没有机器在看规则自己**。

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
| 2026-09 | 1        | 0        | 0        | 0      | 1        |

> 2026-09「新增规则」= `harness/rules/logging-standard.md`(补上骨架承诺却未交付的那一份)。

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
