# 发布流程

## 发布前

- [ ] 所有需求 CI 通过
- [ ] 所有人工确认点完成
- [ ] 回归测试通过
- [ ] 监控就绪
- [ ] 回滚方案就绪
- [ ] 发布说明就绪

## 发布中

1. 冻结 main。
2. 打 tag。
3. 部署 staging。
4. 验证 staging。
5. 部署 prod。
6. 监控观察。

## 发布后

- [ ] 关键路径验证
- [ ] 监控无异常
- [ ] 用户确认
- [ ] 解冻 main

## 回滚

见 `rollback-process.md`。

## 记录

写入 `harness/changes/RELEASE-XXXX/`。
