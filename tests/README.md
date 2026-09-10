# 测试说明

## 目录

| 文件            | 用途                                             |
| --------------- | ------------------------------------------------ |
| conftest.py     | 公共 fixture                                     |
| test_smoke.py   | 冒烟测试                                         |
| test_scripts.py | 各检查脚本的行为测试                             |
| test_gates.py   | **门禁防腐测试** —— 盯住"门禁自己"不要静默腐烂 |
| test_tooling.py | 辅助脚本(audit_log / collect_metrics / 依赖审计) |

## 运行

```bash
make test
```

## 覆盖率

要求 >= 80%(阈值由 `make coverage` 执行;骨架期 `src/` 无代码时会**显式标注未实现**)。

本仓脚本几乎全部以 subprocess 驱动,普通进程内覆盖率看不见它们 ——
`conftest.py` 里的 `_subprocess_coverage` 启用了 coverage 的跨进程采集,
所以覆盖率是**真实**数字(此前实测为 0.00% 的假数字)。

## 新增测试

- 每个新脚本必须新增测试。
- 每个 P0 规则必须有测试。
- 测试必须可失败、可通过。
- **门禁必须有防腐测试**:语法 / 可执行位 / 是否被 Makefile·CI·pre-commit 注册 /
  该拦必拦,并做**反向验证**(把门禁改坏 → 测试必须红)。见 `test_gates.py`。

## Fixture

- `project_root`：项目根目录
- `git_repo`：临时 git 仓库

> 需要新夹具时**随用随加**,不要预先囤积 —— 本文件曾介绍过若干"无人使用"的夹具,
> 它们会让读者以为有约定在被守着,实际没有。
