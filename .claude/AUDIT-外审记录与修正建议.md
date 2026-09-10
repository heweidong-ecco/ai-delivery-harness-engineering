# [已修] 外审记录 · 缺陷与修正建议(严格版)

> ## 状态:[已修] —— H1–H14 全部处理完毕(2026-09-11)
>
> - **处理结果**:见 `harness/iteration/patch-log.md` §四(逐条状态)、§五(已 Patch 清单)、§八(统计)。
> - **修正过程中另外发现 10 条同类缺陷(X1–X10)** —— 修完 H1–H14 后 `make gate` 仍然红才暴露出来,
>   说明本工单抓的是第一层,底下还压着同一类病。见 patch-log §四 4.1。
> - **结果**:`make gate` **首次全绿**(136 个测试通过,覆盖率 84%)。
>   此前它因 H1 / H2 / H3 / X1(ruff 的 T20)/ X2(覆盖率测不到东西)/ X3(套件收集失败)/ X4(密钥扫描拦自己)
>   而**从未绿过**。
> - **本文件自此转为历史记录**,不再作为待办工单;SessionStart 提示据此关闭。
> - 是否按新版本**重新冻结**骨架,由业务方决定(见 `docs/freeze.md`)。

---

> **以下为 2026-09-11 出具时的原始工单内容**,保留以便追溯。
> **本文件是修正工单。** 由外部项目 `agent-eval-gate`(2026-09-11)在通读本仓设计文档 + 实际落地机制后出具。
> **放置位置说明**:本仓 `docs/freeze.md` 规定「骨架不再新增文件」且冻结范围含 `docs/`,故本记录放在 **`.claude/`(不在冻结范围)**,不违反冻结规则。
> **阅读时机**:本仓 `.claude/settings.json` 已注册 SessionStart hook,启动会话时会**自动提示本文件**。

---

## 0. 一句话总评

> 本仓最重要的一句 —— `README.md:129`「**一切不可被机器验证的约束,在 Agent 执行中都是无效约束**」——
> **完全正确,而且本仓自身就是它的最大反例**:它把"代码级纪律"做成了硬的,
> 把"流程级纪律"留成了软的;更糟的是,**它那部分硬门当前是坏的**(见 H1/H2/H3),而**没人知道**。

设计哲学值得肯定(见 §4「本仓做得好、应保留」)。以下 §1–§3 是**必须修**、**应该修**、**建议修**。

---

## 1. 必须修(P0 —— 门禁体系当前实质失效)

### H1 ⛔ 门禁脚本因语法错误**永不执行**,导致 `make gate` 与 CI **从未绿过**

- **证据**:`scripts/check_harness_docs.py:1` 的内容是 ```` ```python ```` —— **一个 markdown 代码围栏被写进了 .py 文件第一行**。
  实测 `compile()` → `SyntaxError: invalid syntax`。
- **影响链**:该文件被 `Makefile:76` 与 `.github/workflows/harness-ci.yml:55` **同时调用** →
  **`make gate` 必红、CI 该 step 必红** → 而 `scripts/dev-setup.sh:27` 的 onboarding 第一步就是 `make gate` → **新项目第一步就撞墙**。
- **最小修复**:① 删掉第一行;② **补一条防腐测试**(见 §5 模板)——这类病**只有测试能防**。

### H2 ⛔ 即使修好 H1,`check_harness_docs.py` 仍会失败:REQUIRED 里 **6 个文件不存在**

- **证据**:`.github/CODEOWNERS`(`:40`)、`.github/dependabot.yml`(`:41`)、
  `harness/rules/logging-standard.md`(`:83`)、`harness/agent/application-owner.md`(`:148`)、
  `harness/agent/application-owner-python.md`(`:149`)、`scripts/check_gates.sh`(`:224`,实际文件是**连字符** `check-gates.sh`)。
- **最小修复**:逐条核对路径;并把"硬编码 184 个路径"改为**「按 glob 校验目录非空 + 校验必需 front-matter」** —— 274 行的路径清单维护不动,必然腐烂。

### H3 ⛔ 测试**给坏门禁兜底** —— "门禁坏了就跳过它"

- **证据**:`tests/test_scripts.py:316-326` 的 `test_check_harness_docs_passes` 用 `pytest.skip(...)` 兜底;
  `:334-357` 三个测试直接调用**不存在的** `scripts/check_gates.sh` → `FileNotFoundError` → 测试套件红。
- **影响**:这是"**软约束体制的病理切片**" —— 门禁坏掉后,**测试替它打了掩护**,而非暴露它。
- **最小修复**:删掉 skip;让"门禁坏了"= 测试**红**。门禁的测试必须断言"它真的会拦"(见 §5)。

---

## 2. 应该修(P1 —— 设计有、落地为零)

### H4 状态机**只写不校验**

- **证据**:`scripts/state_tracker.py:20-30` 只做 `data["stage"]=...` 并 append `history[]`;
  **全仓没有任何代码读这个文件**做前置校验;无 resume/回滚/超时。
- **影响**:`docs/architecture.md:133`「十阶段不可跳过」是**口号**,不是机制。
- **最小修复**:阶段迁移前校验「前置阶段全部 passed **且其产出物现在依然存在**」;
  `resume` 从**第一个断点**续跑。参考实现(可直接移植):`agent-eval-gate/tools/stage_gate.py`。

### H5 阶段门是"一次性查全部产出物",**且不在任何链路里**

- **证据**:`scripts/check-gates.sh:10-24` 一次性检查 6 个产出物;grep 全仓,**它未挂进 Makefile / CI / pre-commit 任何一处**。
- **影响**:**这正是"长任务中间全白费"的教科书案例** —— 门禁只可能在最后触发,中途断了则没有任何门触发过。
- **最小修复**:① 拆成 `check-gates.sh --stage <n>` **增量门**;② **每阶段结束立即跑**;③ 挂进 `Makefile` 与 CI。

### H6 空壳门禁(看起来有检查,实际没有)

- **证据**:`scripts/check_layers.py:6-10` 的 `RULES` 是**空列表**,`:35-37` 直接 `print("no rules configured, skipping")`;
  `scripts/validate_schemas.py:23-25` 在 `harness/schemas/data/` 不存在时直接 return(该目录**确实不存在**);
  `:5-9` jsonschema 未安装时 `exit(0)`。
- **影响**:**比没有更坏** —— 它会给出"这里检查过了"的虚假安全感。
- **最小修复**:要么真实现,要么**明确标注为"未实现"**(并在 `make gate` 输出里说明),不要静默通过。

### H7 设计稿放错目录 = **永不生效**

- **证据**:`harness/workflows/` 下 5 个 yml(`auto-label` / `stale` / `release` / `dependency-update` / `security-scan`)——
  GitHub **只读 `.github/workflows/`**;`.github/ISSUE_TEMPLATE/CODEOWNERS` 与
  `.github/ISSUE_TEMPLATE/dependabot.yml` 同样**放错**(应在 `.github/` 根)。
- **影响**:5 个 workflow + CODEOWNERS(而 `CONTRIBUTING.md:56` 的"至少一人审核"依赖它)+ 依赖更新 **全部不生效**。
- **最小修复**:移到正确目录。其中 `harness/workflows/release.yml:33-39` 有一段**真正的联动硬检查**(CHANGELOG 里 grep 版本号,缺则 exit 1)—— 思路对,**值得优先救活**。

---

## 3. 建议修(P2 —— 一致性 / 语义)

| # | 问题 | 证据 | 修复 |
|---|---|---|---|
| **H8** | **观测是纯装饰**:`config/{alert-rules,prometheus,logging,grafana}` **零消费者**;grafana panel 只有 title+type,**无 datasource 无 query**;`gate_pass_rate`/`coverage` 在 Prometheus 里不存在;**没有熔断、没有"触发即停"** | grep 全仓无 import;`src/__init__.py` 为空,无进程监听 8000 | 要么接线,要么在文档里**明确标为"未实现"** —— 否则读者会以为有观测 |
| **H9** | `validate_schemas.py:5-9`:jsonschema 未装时 `exit(0)` | 依赖未声明 | 缺依赖**应 fail**,不应 pass |
| **H10** | `harness/schemas/rule-schema.json:13` 的 `test` 字段**不在 required 里** | — | 自称「P0 规则必须有测试」实际没强制 → **关键字段一律进 required** |
| **H11** | `pip-audit --strict \|\| true`(CI,`:64`)与 `check_dependencies.py:11-14`(真 fail)**语义矛盾** | 同一检查 CI 软、脚本硬 | 统一为硬 |
| **H12** | `Makefile` 的 `markdownlint:68` / `yamllint:71` / `audit:65` 带 `\|\| true` | — | 去掉 `\|\| true`(否则"检查"永不失败) |
| **H13** | **pre-commit 里没有 pytest / 覆盖率** | `.pre-commit-config.yaml:5-66` | **"跑测试"这条最重要的纪律,在提交环节完全没有门** → 补本地测试门 |
| **H14** | `.importlinter` 定义了分层契约,**但全仓无任何地方运行 `import-linter`** | Makefile/CI/pre-commit 均无 | 加依赖 + target + CI step,或删掉该文件 |

---

## 4. 本仓做得好、应保留(不要因为上面而全盘否定)

| 亮点 | 位置 | 说明 |
|---|---|---|
| **设计哲学的那句话** | `README.md:129` | 本文全篇最有价值的一句,应置顶 |
| **`check_pytest_report.py`(27 行)** | `scripts/` | 堵三个作弊口:`total<=0` / 有 failed / `passed!=total`(skip、xfail 冒充通过)。**已被外部项目采纳**(见 §6) |
| **"三道防编造闸"的来源强制** | `README.md:726-731`、`FillWorkflow.md:1019-1044` | 产出物必须带 `source/check/test`;`source` 空则拒 —— **把"证明你做了功课"从请求变成强制** |
| **`harness/agents/gate-agent.md:17-20`** | — | 全仓**唯一一条自我否定的元规则**:「每条门禁必须可机器验证 / 自然语言描述不算门禁 / 必须给出具体命令」 |
| **`harness/rules/_template.md` 六件套 + `rule-schema.json`** | — | 「规则必须带检查脚本 + 测试文件」是**把软约束转硬的关键钩子**(可惜没接线,见 H6/H10) |
| **`harness/changes/_template/` 七件套** | — | 全仓唯一形成闭环的地方(产出物 → 阶段门),可惜没挂链路(见 H5) |
| **`harness-ci.yml:66-80` 的逐 commit 校验** | — | `for sha in $(git rev-list base..head)` 逐个校验提交信息,设计干净 |

---

## 5. 修正时请同时补上:**门禁防腐测试**(本仓最缺的一环)

**本仓的教训**:门禁脚本**会静默腐烂**(H1 就是活证),而腐烂后**无人知道**,因为**没有测试盯着门禁自己**。

每条门禁至少三类断言:

```python
# ① 语法(抓 H1 那类"永不执行")
subprocess.run(["sh", "-n", script])  # shell
ast.parse(open(script).read())  # python
# ② 可执行位 + ③ 已在 settings/Makefile/CI 里被调用(没注册 = 形同不存在)
# ④ 该拦的拦:喂真实输入,断言它真的拒绝 —— 并**反向验证**(把门禁改坏 → 测试必须红)
```

> **反向验证是关键**:只有"把门禁改坏,测试会红"才证明这条测试守得住 ——
> 否则它和 `test_check_harness_docs_passes` 的 `pytest.skip` 一样是摆设。

---

## 6. 参考:外部项目已按本仓思路落地的部分(可直接对照)

`agent-eval-gate`(出具备忘)在读完本仓后,已落地下列机制并**实测通过**:

| 机制 | 位置(该项目) | 实测 |
|---|---|---|
| 防假测试口径(采纳自本仓) | `tools/check_pytest_report.py` | 4 场景:真实报告过;报告缺失/`total=0`/skip 超基线 全拦 |
| 门禁防腐测试 | `tests/test_hooks.py`(40 条) | **反证**:注入语法错 → 测试红 |
| 真状态机(补 H4/H5) | `tools/stage_gate.py` | 9 条;**测试抓出"resume 会跳过被删产出物"的实现 bug** |
| 左移门(门禁提前到"动手那一刻") | `.claude/hooks/impl-guard.sh` | 4 方向 |
| skill 调用可机器校验(transcript → trace → commit-msg) | `.claude/hooks/skill-trace.sh` + `.githooks/commit-msg` | 退出码 1/0 双向 |

---

## 7. 修正优先级建议

1. **H1 → H3**(先把坏掉的门禁救活,并确保"再坏会被发现")—— 否则本仓一切"硬门"叙事都不成立
2. **H2**(路径清单)→ 顺手改成 glob + front-matter 校验
3. **H5 → H4**(把阶段门做成增量门 + 真状态机)—— 直击"长任务中间全白费"
4. **H6/H7/H9/H10/H11/H12/H13/H14**(一致性与语义)
5. **H8**(观测要么接线要么明确标未实现)

---

## 变更记录

- 2026-09-11 建立。出具方:`agent-eval-gate`(外部);依据:通读本仓
  `README.md` / `BluePrint.md` / `FillWorkflow.md` / `USAGE.md`
  \+ 实际落地文件(`.pre-commit-config.yaml` / `.github/` / `Makefile` /
  `scripts/` / `config/` / 各点文件)的逐一核对,所有结论均带 路径:行号 证据。
- 2026-09-11 标记 `[已修]`(H1–H14 处理完毕;另有 X1–X10)。
