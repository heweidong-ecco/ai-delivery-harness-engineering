# 命名约定

## 一、文件命名

| 类型     | 规范                          | 示例                      |
| -------- | ----------------------------- | ------------------------- |
| 规则     | `<domain>-<type>.md`          | python-coding-standard.md |
| 技能     | `SKILL.md` 或 `<name>-sop.md` | SKILL.md                  |
| 需求目录 | `REQ-XXXX`                    | REQ-0001                  |
| 热修目录 | `HOTFIX-XXXX`                 | HOTFIX-0001               |
| 发布目录 | `RELEASE-XXXX`                | RELEASE-0001              |
| 事故     | `INC-YYYY-MMDD`               | INC-2024-0312             |
| Agent    | `<name>-agent.md`             | incident-agent.md         |
| 模板     | `<name>.md`                   | incident.md               |
| 脚本     | `<action>_<target>.py`        | check_secrets.py          |
| 测试     | `test_<module>_<behavior>.py` | test_amount_float.py      |

## 二、分支命名

| 类型  | 规范             | 示例                |
| ----- | ---------------- | ------------------- |
| 功能  | `feature/<name>` | feature/req-0001    |
| 修复  | `fix/<name>`     | fix/payment-timeout |
| 文档  | `docs/<name>`    | docs/readme-full    |
| Agent | `agent/<name>`   | agent/incident      |
| 规则  | `rule/<id>`      | rule/pay-001        |
| 热修  | `hotfix/<name>`  | hotfix/pay-timeout  |

## 三、提交命名

```text
<type>: <subject>
```

| type  | 用途   |
| ----- | ------ |
| feat  | 新功能 |
| fix   | 修复   |
| docs  | 文档   |
| ci    | CI     |
| chore | 杂项   |
| rule  | 规则   |
| agent | Agent  |
| test  | 测试   |

**示例**：

```text
rule: add PAY-001 from INC-2024-0421
docs: update fill guide
ci: add secret scan
```

## 四、规则 ID 命名

`<DOMAIN>-<NNN>`

| 域     | 前缀  | 示例      |
| ------ | ----- | --------- |
| 支付   | PAY   | PAY-001   |
| 安全   | SEC   | SEC-001   |
| 异常   | ERR   | ERR-001   |
| 日志   | LOG   | LOG-001   |
| 可观测 | OBS   | OBS-001   |
| 性能   | PERF  | PERF-001  |
| 数据库 | DB    | DB-001    |
| API    | API   | API-001   |
| 并发   | CONC  | CONC-001  |
| 缓存   | CACHE | CACHE-001 |
| 幂等   | IDEM  | IDEM-001  |
| 时区   | TZ    | TZ-001    |
| 依赖   | DEP   | DEP-001   |
| 测试   | TEST  | TEST-001  |
| 国际化 | I18N  | I18N-001  |
| 价格   | PRICE | PRICE-001 |
| HTTP   | HTTP  | HTTP-001  |
| 配置   | CFG   | CFG-001   |

## 五、Python 代码命名

### 变量

- 小写 + 下划线
- `user_id`、`order_amount_cents`

### 函数

- 小写 + 下划线
- 动词开头
- `get_user`、`create_order`、`calc_discount`

### 类

- 大驼峰
- `OrderService`、`PaymentAdapter`

### 常量

- 大写 + 下划线
- `MAX_RETRY`、`DEFAULT_TIMEOUT`

### 模块

- 小写 + 下划线
- `order_service.py`、`payment_adapter.py`

### 包

- 小写
- `api`、`service`、`domain`

### 私有

- 前缀下划线
- `_internal_method`、`_cache`

### 测试

- `test_<module>_<behavior>.py`
- `test_<function>_<case>()`

## 六、字段命名

### 价格

- `*_cents`
- 类型 `int`
- 单位分

### 时间

- `*_at`
- 类型 `datetime`
- 时区 UTC

### 布尔

- `is_*`、`has_*`、`can_*`
- `is_active`、`has_permission`

### ID

- `*_id`
- 类型 `int` 或 `str`

### 数量

- `*_count`
- 类型 `int`

## 七、数据库命名

| 对象     | 规范                    | 示例                |
| -------- | ----------------------- | ------------------- |
| 表       | 小写 + 下划线 + 复数    | orders、users       |
| 字段     | 小写 + 下划线           | user_id、created_at |
| 索引     | `idx_<table>_<column>`  | idx_orders_user_id  |
| 唯一索引 | `uniq_<table>_<column>` | uniq_users_email    |
| 外键     | `fk_<table>_<ref>`      | fk_orders_user_id   |

## 八、API 命名

| 类型     | 规范          | 示例                |
| -------- | ------------- | ------------------- |
| 路径     | 小写 + 连字符 | /api/v1/user-orders |
| 参数     | 小写 + 下划线 | user_id             |
| 响应字段 | 小写 + 下划线 | order_amount_cents  |
| 错误码   | 大写 + 下划线 | INVALID_PARAM       |

## 九、环境变量命名

- 大写 + 下划线
- `DATABASE_URL`、`REDIS_HOST`

## 十、配置项命名

- 小写 + 点号
- `app.name`、`db.host`

## 十一、日志字段命名

- 小写 + 下划线
- `trace_id`、`user_id`、`order_id`

## 十二、监控指标命名

- `<domain>_<metric>_<unit>`
- `order_create_count`、`payment_latency_ms`

## 十三、文档命名

| 类型 | 规范                  | 示例                   |
| ---- | --------------------- | ---------------------- |
| 指南 | `<topic>-guide.md`    | fill-guide.md          |
| 说明 | `<topic>.md`          | architecture.md        |
| 模板 | `<name>-template.md`  | adr-template.md        |
| ADR  | `ADR-XXXX-<title>.md` | ADR-0001-use-python.md |
| 教程 | `first-<topic>.md`    | first-rule.md          |

## 十四、禁止

- 禁止拼音命名
- 禁止单字母变量（循环除外）
- 禁止无意义缩写
- 禁止中英文混用
- 禁止类型后缀（如 `str_name`）
- 禁止数字开头
- 禁止关键字
