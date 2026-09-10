# 变更模板

每个需求复制本目录到 `harness/changes/REQ-XXXX/`。

## 必须文件

- requirement-analysis.md
- task-breakdown.md
- coding-report.md
- review-record-v1.md
- unit-test-report.md
- ci-result.md
- deploy-validation.md

## 评审版本

- v1、v2、v3 递增
- 旧版本不删

## 检查

```bash
# 增量门:每完成一个阶段就查一次,不必等最后
./scripts/check-gates.sh harness/changes/REQ-XXXX --stage 4

# 默认 = 阶段 1..9,即上面「必须文件」七件套齐备
./scripts/check-gates.sh harness/changes/REQ-XXXX
```

> 反外审 H5:阶段门原先**一次性查全部产出物**,且**不在 Makefile / CI / pre-commit
> 任何链路里** —— 于是它只可能压在"最后一次提交",长任务中途断了 = 前面全白费。
> 现在支持 `--stage <n>` 增量,并列出了 `make gates` 与 CI。
> 原实现还**漏检 `review-record-v1.md`** —— 现已与上面的「必须文件」对齐。