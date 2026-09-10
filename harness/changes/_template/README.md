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
./scripts/check-gates.sh harness/changes/REQ-XXXX
```