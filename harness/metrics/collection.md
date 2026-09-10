# 度量采集

## 采集方式

| 指标       | 采集方式       | 频率 |
| ---------- | -------------- | ---- |
| AI 代码率  | Git 提交统计   | 每日 |
| 返工轮次   | PR Review 记录 | 每周 |
| 门禁通过率 | CI 结果        | 实时 |
| 覆盖率     | pytest-cov     | 每次 |
| 规则条数   | 文件统计       | 每周 |
| 来源覆盖率 | 脚本检查       | 每周 |

## 脚本

```bash
python scripts/collect_metrics.py
```

## 存储

harness/metrics/data/

## 展示

harness/metrics/dashboard.md
