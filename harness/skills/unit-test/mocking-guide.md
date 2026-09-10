# Mock 指南

## 原则

- 只 mock 边界，不 mock 业务。
- 外部服务必须 mock。
- 数据库优先用真实测试库。

## Mock 对象

| 对象      | 是否 mock | 工具                   |
| --------- | --------- | ---------------------- |
| 外部 HTTP | 是        | responses / httpx mock |
| 数据库    | 优先真实  | testcontainers         |
| 消息队列  | 是        | 内存实现               |
| 时间      | 是        | freezegun              |
| 随机      | 是        | 固定种子               |

## 禁止

- 禁止 mock 被测对象自身。
- 禁止 mock 过度导致测试无意义。
- 禁止 mock 真实生产服务。
