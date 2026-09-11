# 安全政策

## 报告漏洞

请勿公开 Issue 报告安全漏洞。  
请走 **GitHub 私密漏洞报告**（Private vulnerability reporting）：

<https://github.com/heweidong-ecco/ai-delivery-harness-engineering/security/advisories/new>

> 仓库管理员需在 **Settings → Code security** 中开启 *Private vulnerability reporting*
> 该入口才会生效。本仓**不使用公开邮箱**接收漏洞报告。

## 支持版本

| 版本  | 支持 |
| ----- | ---- |
| 0.1.x | 是   |

## 禁止

- 禁止提交密钥、Token、密码。
- 禁止提交真实用户数据。
- 禁止提交生产配置。
- 禁止在日志打印身份证、手机号、银行卡。
- 禁止裸 except 吞异常。

## 强制

- 密钥必须走环境变量或配置中心。
- 敏感日志必须脱敏。
- 外部调用必须设超时。
- 依赖必须定期扫描。

## 扫描

```bash
python scripts/check_secrets.py
bandit -r src
```

## 事件响应

- 发现漏洞立即停用受影响凭证。

- 轮换密钥。

- 修复并回归。

- 记录到 harness/iteration/patch-log.md。
