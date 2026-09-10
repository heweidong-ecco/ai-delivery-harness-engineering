# 十阶段流水线

| 阶段 | 触发 | Skill | 产出 | 门禁 | 回退 | 人工确认 |
|---|---|---|---|---|---|---|
| 需求分析 | 新需求 | request-analysis | 需求分析文档 | 边界清晰 | - | 需求待决议确认 |
| 需求评审 | 分析完成 | expert-reviewer | 评审记录 | 意见完整 | 需求分析 | 需求待决议确认 |
| 计划评审 | 拆分完成 | expert-reviewer | 计划评审 | 可执行 | 任务拆解 | 计划评审后确认 |
| 编码实现 | 计划确认 | coding | 代码、报告 | 编译通过 | 编码实现 | - |
| 编码评审 | 编码完成 | expert-reviewer | 评审记录 | 问题分级 | 编码实现 | 编码评审后确认 |
| 单测编写 | 编码通过 | unit-test | 单测、报告 | 用例>0 | 单测编写 | - |
| 单测评审 | 单测完成 | expert-reviewer | 评审记录 | 断言完整 | 单测编写 | - |
| CI 验证 | 单测通过 | ci-validation | CI 结果 | Status=SUCCESS, TotalTest>0, Passed=Total | 单测编写 | - |
| 部署验证 | CI 通过 | deploy-validation | 部署报告 | 参数正确 | 参数确认 | 部署环境参数确认 |
| 用户确认 | 部署通过 | doc-management | 交付确认 | 用户通过 | 需求分析 | 最终交付确认 |
