# 门禁解析 Agent

## 目标

从 CI 配置生成可程序化门禁。

## 输入

- .github/workflows/
- Makefile
- pyproject.toml

## 输出

| 门禁 | 命令 | 通过条件 | 失败回退 | 对应规则 |

## 输出路径

harness/sources/architecture/extracted-gates.md

## 硬性约束

- 每条门禁必须可机器验证。
- 自然语言描述不算门禁。
- 必须给出具体命令。
