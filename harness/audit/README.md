# 审计目录

## 用途

记录关键决策和变更。

## 文件

`harness/audit/<date>-<event>.md`

## 事件类型

- 规则新增
- 规则修改
- Agent 执行
- 人工确认
- 升级上报
- 回滚

## 脚本

```bash
python scripts/audit_log.py <event> <detail>
