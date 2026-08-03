---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-002"
doc_type: "test"
source_ids: ["REQ-PSR-CONFIG-ENV-002", "CYCLE-PSR-20-001"]
status: accepted
version: "v1.0"
current_slice: "T20-01..02"
updated_at: "2026-08-03"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 代码位置目录规则 V2：embedded 配置文件名格式后置 真实测试记录

结论：本次两轮真实测试全部通过，格式后置的新命名被放行、旧命名与重复格式名被失败关闭，且跨周期回归未受影响。影响：确认目录检查工具对内嵌配置文件名的判定方向已完整反转，规则文档、目录清单与工具三处口径一致。范围：目录检查工具的查询与渲染子命令、配置布局行为回归文件、目录规则全量回归。非范围：真实业务项目的文件迁移、外部 YAML 命名、秘密原值检测算法和任何写入版本历史的动作。变化：反向用例从"拒绝格式后置"改为"拒绝缺少格式后置与重复格式名"两类，正向用例改为格式后置命名。完成标准：查询与渲染断言成立、配置布局回归七项全绿、全量回归十六项全绿、反向用例检查前后目录摘要一致。术语说明：`失败关闭` 指检查发现问题时直接判定不通过而不是只提醒；`目录摘要` 指对目标目录全部路径和内容算出的指纹，用来证明检查过程没有改动任何文件。验证状态：全部通过，无阻断项。

## 文档信息

| 项目 | 内容 |
|---|---|
| 所属需求 | `REQ-PSR-CONFIG-ENV-002` |
| 所属周期 | `CYCLE-PSR-20-001` |
| 覆盖任务 | `T20-01`、`T20-02` |
| 测试 ID | `TEST-PSR-CONFIG-002-A`、`TEST-PSR-CONFIG-002-B` |
| 执行时间 | 2026-08-03 17:48:21 起 |
| 执行环境 | 本地 Windows + Git Bash + 本地 Python，无外部服务连接 |
| 本地环境边界 | 本次测试不连接任何数据库、缓存、消息队列或 HTTP 上游，全部样本由测试用例在临时目录内构造 |

## 通过标准

| 判定项 | 通过标准 | 实际结果 |
|---|---|---|
| 内嵌配置查询 | 两类后端项目均返回 `config_<env>_yaml.go` 作为 Go 文件名模式，退出码为零 | 通过 |
| 外部 YAML 未漂移 | 外部 YAML 文件名模式仍为 `config_<env>.yaml|config_<env>.yml` | 通过 |
| 目录树渲染 | 输出同时含 `config_<env>_yaml.<ext>` 与未改动的 `config_<env>.yaml` | 通过 |
| 配置布局行为回归 | 七个用例全部通过 | 通过，7 tests OK |
| 目录规则全量回归 | 十六个用例全部通过 | 通过，16 tests OK |
| 只读性 | 反向用例在检查前后目录摘要一致 | 通过，由回归用例内置断言判定 |

## 清理与阻断

| 项目 | 内容 |
|---|---|
| 清理 | 无需清理。回归用例使用临时目录，退出时由测试框架自动删除；查询与渲染子命令只读，不产生文件 |
| 阻断项 | 无 |
| 环境阻断 | N/A + 原因：本次测试不需要数据库、缓存或外部服务 + 证据：全部样本由测试用例在临时目录内构造 |
| 提交状态 | 停在已改动未提交状态，本轮未获提交授权 |

## 图片资产决策

图片资产决策：N/A + 原因：本次真实测试只产生命令行文本输出，不包含界面、截图或视觉验收对象 + 证据：`doc/data/images/` 下无本任务图片引用。

## 执行附录

### TEST-PSR-CONFIG-002-A：查询与渲染（对应 `T20-01`，证据 `EVD-T20-01-TEST`）

内嵌配置查询，两类后端项目各一次：

```bash
cd /d/luode/luode-skills && python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind backend --artifact config --category embedded
```

```bash
cd /d/luode/luode-skills && python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind fullstack --artifact config --category embedded
```

实际输出关键行：

```text
--- backend ---
  "ok": true,
    "canonical_path": "config/embedded",
    "file_name_pattern": "config_<env>_yaml.go（Go）；其他语言仅检查原有扩展名",
    "go_file_name_pattern": "config_<env>_yaml.go",
exit=0
--- fullstack ---
  "ok": true,
    "canonical_path": "backend/config/embedded",
    "file_name_pattern": "config_<env>_yaml.go（Go）；其他语言仅检查原有扩展名",
    "go_file_name_pattern": "config_<env>_yaml.go",
exit=0
```

目录树渲染与外部 YAML 未漂移核对：

```bash
cd /d/luode/luode-skills && python -X utf8 package-structure-rules/scripts/placement_catalog.py render --project-kind backend
```

```bash
cd /d/luode/luode-skills && python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind backend --artifact config --category yaml
```

实际输出关键行：

```text
19:├── config/                                  # [必需·提交] 唯一配置根
21:│   │   └── config_<env>.yaml                 # [条件·提交] 兼容 `.yml`；标准环境为 local、test、prod
23:│       └── config_<env>_yaml.<ext>           # [条件·提交] Go 使用 config_<env>_yaml.go；格式名后置规避 Go 测试文件命名；允许源码私密配置，源码优先且默认不依赖环境变量
render_exit=0
--- yaml 条目未漂移 ---
    "file_name_pattern": "config_<env>.yaml|config_<env>.yml",
```

### TEST-PSR-CONFIG-002-B：行为回归（对应 `T20-02`，证据 `EVD-T20-02-TEST`）

配置布局行为回归：

```bash
cd /d/luode/luode-skills && python -X utf8 test/package-structure-rules/configuration_layout_test.py -v
```

实际输出尾部：

```text
test_catalog_query_and_schema_expose_environment_contract ... ok
test_embedded_secret_boundary_is_distinct_from_yaml_boundary ... ok
test_init_creates_directories_without_dynamic_environment_files ... ok
test_policies_preserve_failure_semantics_and_hash ... ok
test_render_contains_environment_examples ... ok
test_strict_accepts_split_and_unpaired_environment_files ... ok
test_strict_rejects_invalid_names_locations_and_nesting ... ok

----------------------------------------------------------------------
Ran 7 tests in 5.860s

OK
```

目录规则全量回归，确认跨周期无回归：

```bash
cd /d/luode/luode-skills && python -X utf8 -m unittest discover -s test/package-structure-rules -p "*_test.py"
```

实际输出：

```text
................
----------------------------------------------------------------------
Ran 16 tests in 11.893s

OK
```

### 样本与断言对照

| 样本 | 类型 | 期望 | 判定用例 |
|---|---|---|---|
| `config/embedded/config_local_yaml.go` | 正向 | 严格检查放行 | `test_strict_accepts_split_and_unpaired_environment_files` |
| `backend/config/embedded/config_dev_yaml.go` | 正向 | 严格检查放行 | 同上 |
| `config/embedded/config_local.java` | 正向 | 放行，锚定文件名契约只对 Go 强制 | 同上 |
| `config/embedded/config_test.go` | 反向 | 失败关闭，错误含 `Go embedded` | `test_strict_rejects_invalid_names_locations_and_nesting` |
| `config/embedded/config_test_yaml_yaml.go` | 反向 | 失败关闭，错误含 `Go embedded` | 同上 |
| `config/embedded/nested/config_local_yaml.go` | 反向 | 失败关闭，错误含 `直接位于`，证明失败原因是层级而非文件名 | 同上 |
| `config/yaml/config_prod.yaml` | 正向 | 放行，外部 YAML 命名未受本次改动影响 | 同上正向用例 |

### 文档门禁

```bash
cd /d/luode/luode-skills && python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc "doc/2-需求/2026-08-03_代码位置目录规则V2_embedded配置文件名格式后置.md" --root "D:\luode\luode-skills" --strict
```

```bash
cd /d/luode/luode-skills && python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc "doc/3-实施/2026-08-03_代码位置目录规则V2_实施周期20_embedded配置文件名格式后置.md" --root "D:\luode\luode-skills" --strict
```

两条均返回 `PASS` 且错误列表为空。
