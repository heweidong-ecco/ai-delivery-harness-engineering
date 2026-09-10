# 测试说明

## 目录

| 文件            | 用途         |
| --------------- | ------------ |
| conftest.py     | 公共 fixture |
| test_smoke.py   | 冒烟测试     |
| test_scripts.py | 脚本测试     |

## 运行

```bash
make test
```
## 覆盖率
要求 >= 80%。

## 新增测试
- 每个新脚本必须新增测试。

- 每个 P0 规则必须有测试。

- 测试必须可失败、可通过。

## Fixture
- project_root：项目根目录

- harness_root：harness 目录

- sample_req_dir：临时需求目录

