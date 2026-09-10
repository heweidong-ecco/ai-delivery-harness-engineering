# CI Validation Skill

## 目标

验证 CI 结果满足门禁。

## 触发条件

单测评审通过。

## 输入

CI 输出、pytest-report.json

## 步骤

1. 检查 Status=SUCCESS。
2. 检查 TotalTest>0。
3. 检查 Passed=Total。
4. 检查覆盖率。
5. 检查规则脚本。

## 输出

harness/changes/REQ-XXXX/ci-result.md

## 质量门禁

- Status=SUCCESS
- TotalTest>0
- Passed=Total
- 覆盖率>=80%
- 规则脚本通过

## 失败回退

- 测试数为 0：回退单测编写
- 编译错误：回退编码实现
- 规则违规：回退编码实现
