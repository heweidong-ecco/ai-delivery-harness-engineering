# REQ-XXXX HC-N

> 人工确认点记录模板。复制为 `harness/checkpoints/<REQ>-HC<N>.md` 后填写。
> 五个确认点的时机与确认内容见 `harness/pipeline/human-checkpoints.md`。

- 确认人：
- 时间：
- 内容：
- 结论：

## 说明

- **确认人必须是人**,不得由 Agent 代填(`human-checkpoints.md` 硬性约束)。
- `HC-N` 中 N 取 1–5;当前**只有 HC-5(最终交付确认)被阶段门校验**
  (`harness/state/stages.json` 里阶段 10 的产出物)。HC-1 ~ HC-4 尚无机制,
  属已知缺口 —— 见 `harness/pilot/findings.md` 空跑-3。
- 空跑-1 修正:此前**没有这份模板**,导致照文档执行的 Agent 走完阶段 1–9 后,
  会在阶段 10 卡在一个从未被告知要产出的文件上。现已补上并在
  `harness/changes/README.md` 的产出物清单里注明。
