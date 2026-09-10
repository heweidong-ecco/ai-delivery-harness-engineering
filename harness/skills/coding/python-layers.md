# Python 分层编码 Skill

## 加载时机
编码实现阶段。

## 顺序

1. 写 domain 模型。
2. 写 repository 接口与实现。
3. 写 adapter，必须带 timeout/retry/降级。
4. 写 service，编排业务。
5. 写 api，只做参数校验和响应。
6. 写测试。
7. 更新文档。

## 禁止

- 在 api 中直接访问数据库。
- 在 service 中拼接 SQL。
- 使用 float 表示金额。
- 外部调用不设置 timeout。
