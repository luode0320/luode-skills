---
schema_version: 1
doc_id: "TEST-PSR-DOC-LAYOUT-001"
doc_type: test_record
source_ids: ["REQ-PSR-DOC-LAYOUT-001", "CYCLE-PSR-DOC-LAYOUT-16-001"]
status: passed
updated_at: "2026-08-02"
---

# 三类项目 doc 目录收敛测试记录

结论：目录专项测试验证了 fullstack、backend、frontend 三类项目的活动研发目录一致，独立前端不再生成根 `data/business`、`data/project`，历史 `doc/6-审查` 与 `doc/7-验收` 不进入初始化骨架。

## 测试范围

- 环境：本地 Windows Python、仓库内 Catalog、临时目录；不连接数据库、缓存、消息队列或外部服务。
- 可执行入口：`test/package-structure-rules/project_layout_contract_test.py`。
- 样本：三类项目各一个临时初始化根目录；Catalog JSON 兼容 YAML；人工目录树 Markdown。
- 非范围：真实业务项目迁移、历史目录删除、源码域 `src/modules/<domain>/data/`。

## 执行命令与断言

```bash
python -X utf8 -B test/package-structure-rules/project_layout_contract_test.py
```

通过条件：退出码为 `0`，共 `2` 项测试通过；每类项目包含 `doc/1-架构`、`doc/2-需求`、`doc/3-实施`、`doc/4-bugs`、`doc/5-tests`、`doc/6-review` 和 `doc/data/images`；不存在 `doc/6-审查`、`doc/7-验收`；frontend 不存在根 `data/business` 或 `data/project`。

失败预期：任一目录缺失、旧目录出现、前端根 data 出现、CLI 非零退出或人工树仍声明旧活动目录时，测试失败并停止收口。

## 结果

| 测试 | 结果 | 证据 |
|---|---|---|
| Catalog 与人工目录树一致 | 通过 | `project_layout_contract_test.py::test_catalog_and_layout_define_same_active_doc_tree` |
| 三类 init 输出一致 | 通过 | `project_layout_contract_test.py::test_init_creates_doc_tree_for_all_project_kinds` |

## 清理与回滚

测试使用 `tempfile.TemporaryDirectory`，结束后自动清理；仓库不保留临时 fixture。回滚仅撤销本轮未提交测试和规则增量，不删除任何真实项目目录。

## 证据索引

- `EVD-PSR-DOC-16-03`: 专项测试退出码 `0`、2/2 通过。
- `EVD-PSR-DOC-16-02`: Catalog skeleton 与人工目录树断言通过。
