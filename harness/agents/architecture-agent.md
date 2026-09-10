# 架构解析 Agent

## 目标
从代码库或架构文档提取分层规则。

## 输入
- harness/sources/architecture/
- src/

## 步骤
1. 扫描 src/ 下所有包和模块。
2. 统计每个模块被谁 import。
3. 推断分层：api / service / domain / repository / adapter。
4. 找出违反分层方向的 import。
5. 生成分层规则。

## 输出
- 模块清单
- 分层结论
- 违规清单
- 建议规则（六件套）

## 输出路径
harness/sources/architecture/extracted-rules.md

## 硬性约束
- 不允许编造模块。
- 不允许编造违规。
- 每条规则必须有来源。
- 缺失信息写“待补充”。