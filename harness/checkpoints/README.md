# 检查点目录

## 用途

记录五个人工确认点(`HC-1` ~ `HC-5`,时机与确认内容见
`harness/pipeline/human-checkpoints.md`)。

## 文件

`harness/checkpoints/<REQ>-HC<N>.md`

## 模板

从 `_template.md` 复制:

```bash
cp harness/checkpoints/_template.md harness/checkpoints/REQ-XXXX-HC5.md
```

> 空跑-1 修正:此前**没有这份模板** —— `harness/changes/_template/` 只给变更七件套,
> 而 `stages.json` 却要求阶段 10 产出 `harness/checkpoints/<REQ>-HC5.md`。
> 照文档执行的 Agent 会走完阶段 1–9 后,在**最后一阶段**卡在一个**从未被告知要产出**
> 的文件上(实测:`stage_gate.py pass` 报"产出物缺失/为空")。

## 格式

```markdown
# REQ-XXXX HC-N

- 确认人：
- 时间：
- 内容：
- 结论：
```

## ⚠ 当前只有 HC-5 被机器校验

| 确认点 | 时机 | 是否被阶段门校验 |
| ------ | ---- | ---------------- |
| HC-1 | 需求评审后 | ❌ **无机制** |
| HC-2 | 计划评审后 | ❌ **无机制** |
| HC-3 | 编码评审后 | ❌ **无机制** |
| HC-4 | 部署前 | ❌ **无机制** |
| HC-5 | 用户确认阶段 | ✅ 阶段 10 的产出物(`harness/state/stages.json`) |

`human-checkpoints.md` 写着"未确认不得进入下一阶段(**阻塞**)",但上述 4 个确认点
目前**完全是文字约定,没有任何机制拦它** —— 这与本仓修过的 H4/H5 是同一类问题
(写下来的约束没有机制)。记为已知缺口,**尚未上机制**(空跑-3,见
`harness/pilot/findings.md`)。

要让它们上机制,需要先定清楚**每个确认点各自产出什么证据**,再写进
`harness/state/stages.json` 对应阶段的 `evidence`。
