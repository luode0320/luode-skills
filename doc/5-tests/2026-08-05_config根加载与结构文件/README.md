---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-SOURCE-001"
doc_type: test
source_ids: ["REQ-PSR-CONFIG-SOURCE-001", "CYCLE-PSR-23"]
status: accepted
version: "v1.0"
current_slice: "T23-02"
updated_at: "2026-08-05"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# config 根加载与结构文件规则真实测试证据

结论：`config/load.<ext>` 与 `config/model.<ext>` 的 Catalog 契约、Schema 守卫、四语言 strict 正反向、init 边界与只读检查专项测试通过 `11/11`；影响：目录规则、Catalog、CLI 和配置 reference 的落点契约均有本地回归证据；范围：config 根源码文件查询、渲染、strict/adoption/legacy 边界和 init 行为；非范围：真实业务项目迁移、`common/util/`、外部服务和 Git 历史写入；变化：config/ 根直接源码文件仅放行 load/model 两个命名；完成标准：专项测试、四文件回归、文档 profile、编码检查和风格回归均有可核验证据；术语说明：`load.<ext>` 是配置加载与解析入口，`model.<ext>` 是配置结构定义文件；验证状态：专项测试 `11/11` 通过，package-structure-rules 四文件回归 `26/26` 通过，需求/实施/测试/风格 profile 通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联需求 | `REQ-PSR-CONFIG-SOURCE-001` |
| 关联周期 | `CYCLE-PSR-23` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行测试根 | `test/` |
| 证据目录 | `doc/5-tests/2026-08-05_config根加载与结构文件/` |

## 测试入口

```text
python -X utf8 -m unittest discover -s test/package-structure-rules -p configuration_layout_test.py -v
python -X utf8 -m unittest discover -s test/package-structure-rules -p '*_test.py' -v
```

## 覆盖范围

- backend/fullstack × loader/model 四个 pattern 条目的 query 唯一命中与 Schema 守卫。
- render 两棵树均暴露 `load.<ext>` 与 `model.<ext>` 占位契约。
- Go、Java、Node.js、Python 四语言 `config/load.<ext>` 与 `config/model.<ext>` strict 正向放行。
- 非 load/model 根文件、错误扩展名、`config/load/` 子目录、`config/foo/` 与 `config/loader/` 禁止路径失败关闭。
- 默认 init 与显式启用 pattern 均不创建 load/model 占位文件；check 前后 `directory_hash` 一致。
- 既有 yaml/embedded、common/util、entrypoint、project-layout 用例不回归。

## 证据文件

- `test/package-structure-rules/configuration_layout_test.py`：活动可执行测试。
- 本次运行结果：专项 `Ran 11 tests ... OK`；四文件回归 `Ran 26 tests ... OK`。

## 完成标准

- config 根 load/model 的 Catalog、Schema、渲染、四语言正反向、init 与只读边界均有断言。
- 本地专项测试、四文件回归、文档 profile、Skill 校验和 `git diff --check` 均可复验。
- 任一真实测试失败时保留未收口状态，不把静态阅读或构建结果替代为功能通过。

## 测试边界

- 仅使用本地 Python、仓库文件和 `tempfile.TemporaryDirectory`；不连接数据库、缓存、消息队列、HTTP/RPC 上游或真实业务项目。
- 图片资产决策：N/A + 原因：本轮没有界面或视觉产物 + 证据：测试只断言文本、路径和退出码。

## 追踪附录

| AC | TASK | TEST | 证据 |
|---|---|---|---|
| `AC-PSR-CONFIG-SOURCE-001` | `T23-01` | `TEST-PSR-CONFIG-SOURCE-001` | `EVD-T23-01-TEST` |
| `AC-PSR-CONFIG-SOURCE-002` | `T23-02` | `TEST-PSR-CONFIG-SOURCE-001` | `EVD-T23-02-TEST` |
| `AC-PSR-CONFIG-SOURCE-003` | `T23-02` | `TEST-PSR-CONFIG-SOURCE-001` | `EVD-T23-02-TEST` |
| `AC-PSR-CONFIG-SOURCE-004` | `T23-04` | `TEST-PSR-CONFIG-SOURCE-001` | `EVD-T23-04-GATE` |
