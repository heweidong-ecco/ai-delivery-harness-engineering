# 骨架冻结说明

## 冻结版本

v0.1.0-skeleton

## 冻结日期

2026-XX-XX

## 冻结范围

- harness/
- scripts/
- tests/
- docs/
- .github/

## 冻结后规则

1. 骨架不再新增文件。
2. 所有改动通过填充层进行。
3. 每次填充必须走 PR。
4. 每次 Patch 必须记录。

## 下一步

- 引入项目
- 跑 6 个核心 Agent
- 空跑 REQ-0000
- 试点

---

## 🔓 解冻记录

**解冻日期**:2026-09-11

**解冻原因**:外部项目 `agent-eval-gate` 对本仓出具了一份**外审缺陷工单**
(`.claude/AUDIT-外审记录与修正建议.md`);其中 **P0 三条表明当前门禁体系实质失效** ——
尤其 `scripts/check_harness_docs.py:1` 的 SyntaxError,使 `make gate` 与 CI **从未绿过**。
修正涉及 `scripts/` / `tests/` / `docs/` / `.github/`,均落在原冻结范围内,故**解冻**。

**解冻范围**:上表「冻结范围」所列**全部目录**(`harness/` `scripts/` `tests/` `docs/` `.github/`)。

**原「冻结后规则」的处理**:

| 原规则 | 解冻后的处理 |
|---|---|
| 1. 骨架不再新增文件 | **暂停执行** —— 外审修正需要新增/改动文件(如防腐测试、真状态机) |
| 2. 所有改动通过填充层进行 | **暂停执行** |
| 3. 每次填充必须走 PR | **以「最小留痕」替代** —— 本机无 `gh` CLI,无法创建 PR;改为在提交信息内写明变更与依据(与 Kit 的 KD-3「无 gh 最小留痕」一致) |
| 4. 每次 Patch 必须记录 | **继续执行** —— 登记在 `harness/iteration/patch-log.md` §四「待 Patch 清单」 |

**关联记录**:`harness/iteration/patch-log.md` §四(H1–H14 待 Patch 清单)、
`.claude/AUDIT-外审记录与修正建议.md`(完整工单:证据 + 影响 + 最小修复 + 优先级)。

**重新冻结条件**:外审工单 H1–H14 全部处理完毕后,由业务方决定是否按新的骨架版本重新冻结。

---

## ⚠ 工作方式变更记录:本仓修正**不走 PR**(2026-09-11)

**变更内容**:对本仓库(`ai-delivery-harness-engineering`)的修正,
**不需要走 PR,直接 `commit` + `push` 到 `main`**。

**变更原因**:业主明确指示(2026-09-11)。本机无 `gh` CLI,且当前为单人多机的
骨架维护阶段,PR 流程在此场景下是纯开销。这与上文解冻记录里
「每次填充必须走 PR → 以『最小留痕』替代」是同一取向的延续。

**留痕替代方案**:
1. 提交信息按 `scripts/check_commit_msg.py` 的规范(`<type>: <subject>`),
   并在正文写明**变更依据**(外审工单编号 H1–H14、patch-log 条目等);
2. 每条修正登记在 `harness/iteration/patch-log.md` §五「已 Patch 清单」;
3. 重要变更同步 `CHANGELOG.md`。

**⚠ 与仓库自身规则的冲突(已知并被显式覆盖)**:本仓**自己写着**「必须走 PR」——
`README.md` Q7「Agent 能直接改 main 吗?**不能。必须走 PR**」、
`harness/iteration/patch-log.md` §七「**禁止 Agent 直接改 main**」、
`harness/agents/README.md` §八「直接改 main」列为禁止项。

业主是所有者和最终决策人,此覆盖**有效**;但记录在此,以免日后读仓库规则的人
以为这些条文仍然生效。**若本仓要作为"方法论范本"对外发布**(USAGE 的方式 A),
这条偏离必须先解决 —— 因为范本自身违反自己的规则,是最坏的反例。

**恢复条件**:重新冻结、或对外发布范本之前,应恢复「走 PR」并要求至少一人审核
(`CONTRIBUTING.md` §PR 规范)。

