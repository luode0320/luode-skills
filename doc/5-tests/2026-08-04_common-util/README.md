---
schema_version: 1
doc_id: "TEST-PSR-COMMON-UTIL-001"
doc_type: test
source_ids: ["REQ-PSR-COMMON-UTIL-001", "CYCLE-PSR-22-001"]
status: accepted
version: "v1.0"
current_slice: "T22-02"
updated_at: "2026-08-04"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# `common/util` 目录规则真实测试证据

结论：独立后端 `common/util` 专项行为测试通过 `5/5`；影响：目录规则、Catalog、CLI 和相邻 Skill 的落点契约均有本地回归证据；范围：`common/util` 查询、渲染、初始化和 strict/adoption 边界；非范围：真实业务项目迁移、外部服务和 Git 历史写入；变化：新增独立后端关联工具的扁平目录行为测试；完成标准：专项测试、文档 profile、编码检查和风格回归均有可核验证据；术语说明：`common/util` 是独立后端项目关联工具的扁平目录，`utils/<package>/` 是可独立复制的工具包目录；验证状态：专项测试 `5/5` 通过，package-structure-rules 四个活动测试文件共 `22/22` 通过，需求/实施/测试/风格 profile 通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联需求 | `REQ-PSR-COMMON-UTIL-001` |
| 关联周期 | `CYCLE-PSR-22-001` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行测试根 | `test/` |
| 证据目录 | `doc/5-tests/2026-08-04_common-util/` |

## 测试入口

```text
python -X utf8 -m unittest discover -s test/package-structure-rules -p backend_common_util_layout_test.py -v
```

## 覆盖范围

- Catalog 唯一 `backend.common.util` 与 `source-util` 兼容查询别名。
- `query`、`render`、`init` 的 `common/util` 路径行为。
- Go、Java、Node.js、Python 当前语言直接文件放行。
- 错误扩展、子目录、根 `utils` 直接文件、源码根旧 `util` 和非 backend 根 `common/util` 失败关闭。
- adoption legacy 快照允许维护既有旧源码文件且不自动搬移。

## 证据文件

- `backend_common_util_layout_test.py`：活动可执行测试。
- 本次运行结果：`Ran 5 tests ... OK`。

## 完成标准

- `common/util` 的正向路径、错误扩展、子目录、旧源码根、根 `utils` 和非 backend 边界均有断言。
- 本地专项测试、package-structure-rules 活动回归、文档 profile、Skill 校验和 `git diff --check` 均可复验。
- 任一真实测试失败时保留未收口状态，不把静态阅读或构建结果替代为功能通过。

## 测试边界

- 仅使用本地 Python、仓库文件和 `tempfile.TemporaryDirectory`；不连接数据库、缓存、消息队列、HTTP/RPC 上游或真实业务项目。
- 图片资产决策：N/A + 原因：本轮没有界面或视觉产物 + 证据：测试只断言文本、路径和退出码。

## 追踪附录

| AC | TASK | TEST | 证据 |
|---|---|---|---|
| `AC-PSR-COMMON-UTIL-001` | `T22-02` | `TEST-PSR-COMMON-UTIL-001` | `EVD-T22-02-TEST` |
| `AC-PSR-COMMON-UTIL-002` | `T22-02` | `TEST-PSR-COMMON-UTIL-001` | `EVD-T22-02-TEST` |
| `AC-PSR-COMMON-UTIL-003` | `T22-02` | `TEST-PSR-COMMON-UTIL-001` | `EVD-T22-02-TEST` |
| `AC-PSR-COMMON-UTIL-004` | `T22-03` | `TEST-PSR-COMMON-UTIL-001` | `EVD-T22-03-TEST` |
