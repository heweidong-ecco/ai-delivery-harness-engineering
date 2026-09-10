# 状态目录

## 用途

跟踪需求当前状态。

## 文件

`harness/state/<REQ>.json`

## 格式

```json
{
  "req": "REQ-0001",
  "stage": "coding",
  "status": "in_progress",
  "owner": "<待填>",
  "updated_at": "<待填>",
  "history": []
}
```

## 脚本
```bash
python scripts/state_tracker.py <REQ> <stage> <status>
```
