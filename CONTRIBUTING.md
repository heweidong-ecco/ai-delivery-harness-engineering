# 贡献指南

## 分支规范

| 分支           | 用途       |
| -------------- | ---------- |
| main           | 稳定分支   |
| feature/<name> | 功能开发   |
| agent/<name>   | Agent 填充 |
| fix/<name>     | 修复       |
| docs/<name>    | 文档       |

## 提交规范

格式：

```text
<type>: <subject>

<body>

<footer>
type：

- feat：新功能
    
- fix：修复
    
- docs：文档
    
- ci：CI
    
- chore：杂项
    
- rule：规则
    
- agent：Agent
    
- test：测试
    

示例：

rule: add PAY-001 from INC-2024-0421
支付回调必须设置 timeout，超时后标记 pending。
Source: harness/sources/incidents/INC-2024-0421.md
```

## PR 规范

1. 从 main 切分支。
    
2. 每个 PR 只做一件事。
    
3. PR 描述用模板。
    
4. CI 必须通过。
    
5. 至少一人审核。
    
6. 规则类 PR 必须附来源。
    

## 规则贡献

每条规则必须包含六件套：

1. 规则
    
2. 原因
    
3. 反例
    
4. 正例
    
5. 检查
    
6. 测试
    

来源为空则拒绝。

## Agent 贡献

每个 Agent 必须：

1. 有独立 Prompt 文件。
    
2. 有输入目录约定。
    
3. 有输出格式。
    
4. 有硬性约束。
    
5. 有示例输出。
    

## 禁止

- 禁止提交密钥、真实数据、生产配置。
    
- 禁止无来源规则。
    
- 禁止跳过 CI。
    
- 禁止 Agent 直接改 main。