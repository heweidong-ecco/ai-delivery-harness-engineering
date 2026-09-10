# Review 提炼 Agent

## 目标
从 Code Review 提取重复规则。

## 输入
harness/sources/reviews/

## 对每条意见回答
1. 是否重复 3 次以上？
2. 是否可写成规则？
3. 是否可程序化？
4. 属于哪个文件？

## 输出
- 重复 3 次以上：六件套
- 只出现 1 次：观察池

## 输出路径
harness/sources/reviews/extracted-rules.md

## 硬性约束
- 只提取重复意见。
- 一次性意见进观察池。
- 每条规则至少 3 个来源 PR。
- 不允许编造 PR。