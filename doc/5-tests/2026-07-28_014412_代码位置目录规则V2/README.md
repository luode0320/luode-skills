---
schema_version: 1
doc_id: "TEST-PSR-V2-001"
doc_type: "test"
source_ids: ["REQ-PSR-V2-001", "REQ-PSR-UTILS-001", "REQ-PSR-SOURCE-UTIL-002", "REQ-PSR-CLI-003", "REQ-PSR-BUSINESS-RPC-004", "REQ-PSR-ADOPT-001"]
status: "accepted"
version: "v1.2"
current_slice: "TASK-09-03 渐进采用本地行为验证"
updated_at: "2026-07-29 00:25:50"
template_version: 1
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
review_acceptance_gates:
  - stage: functional_validation
    applicability: applicable
    reason: 目录规则的公开行为必须通过真实 CLI 与临时样本验证。
    basis: AC-PSR-UTILS-001 至 AC-PSR-UTILS-005、AC-PSR-RPC-001 至 AC-PSR-RPC-003、AC-PSR-ADOPT-001 至 AC-PSR-ADOPT-003。
    required_by_source: true
    required_now: true
    completed_validation: ["TEST-PSR-UTILS-001", "TEST-PSR-RPC-001", "TEST-PSR-RPC-002", "TEST-PSR-RPC-003", "TEST-PSR-ADOPT-001"]
    substitute_validation: []
    manual_follow_up: "N/A；原因：本地单元测试已直接执行 CLI、隔离检查与 CodeGraph 行为；证据：31 项 unittest 结果。"
    pass_standard: 31 项测试全部通过，且 strict/adoption 检查前后 fixture 哈希一致。
  - stage: browser_integration
    applicability: not_applicable
    reason: 本测试没有浏览器页面或前端联调入口。
    basis: BOUND-PSR-003。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
  - stage: third_party
    applicability: not_applicable
    reason: 本测试只使用本地 Python 和临时目录。
    basis: BOUND-PSR-003。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# 代码位置目录规则 V2 测试

结论：本地行为测试验证了根 `utils/`、源码根 `util/`、业务域 `rpc/` 与旧项目渐进采用的不同边界。影响：目录生成和只读检查可在不修改用户文件的前提下拒绝违规位置，旧项目可登记相符目录和冻结快照而不继续扩张遗留结构。范围：查询、渲染、初始化、严格检查、兼容告警、渐进采用、无写入验证、普通 YAML 清单、JSON 响应和 CodeGraph 导入审查。非范围：数据库、缓存、消息队列、第三方 API、浏览器页面和业务项目迁移。变化：新增 `adoption` 清单、已采纳目录、遗留快照、普通 YAML 与未登记源码的正反向断言。完成标准：31 项自动化断言全部通过且 fixture 哈希不变。术语说明：fixture 是测试创建的临时目录样本，哈希用于确认检查未改写样本。验证状态：本地 Python 测试与 CodeGraph 证据已执行通过。图片资产决策：N/A。原因：目录和 CLI 行为没有视觉验收对象。证据：所有结果由退出码、标准输出和文件哈希判断。

## 文档信息

| 项目 | 内容 |
|---|---|
| 测试任务 | `TEST-PSR-UTILS-001`、`TEST-PSR-RPC-001`、`TEST-PSR-RPC-002`、`TEST-PSR-RPC-003`、`TEST-PSR-ADOPT-001`。 |
| 真实测试资产 | `package-structure-rules/test_catalog_schema.py`、`test_query_render.py`、`test_init_check.py`、`test_business_rpc.py`、`test_adoption_check.py` 与 `fixtures/micro-business-rpc/`。 |
| 执行环境 | 本机 Windows Python 3.14（含 PyYAML）、临时 fixture、`F:\luode-skills` 规则仓库。 |
| 外部连接 | N/A；原因：测试不读取外部配置且不发起网络连接；证据：测试仅调用本地 CLI。 |

## 测试范围与样本

| 分类 | 样本 | 预期结果 |
|---|---|---|
| 正向路径 | `utils/time/format.<ext>`、`utils/cron/scheduler.<ext>`、`utils/json/codec.<ext>`、`utils/log/logger.<ext>`、`utils/discovery/polaris/`、`utils/discovery/nacos/`。 | strict 通过或查询返回唯一位置。 |
| 四语言路径 | Go `internal/util/`、Java `src/main/java/<base-package>/util/`、Node.js `src/util/`、Python `src/<package>/util/`。 | `source-util --language` 返回一个规范路径。 |
| 负向根文件 | `utils/<file>.<ext>`。 | strict 返回退出码 2。 |
| 负向旧路径 | 根 `util/...`。 | strict 返回退出码 2，legacy 只警告。 |
| 负向嵌套 | `<source-root>/util/<child>/<file>.<ext>`。 | strict 返回退出码 2。 |
| RPC 目录与初始化 | `business/<domain>/rpc/<operation>.<ext>`。 | Catalog 唯一返回，显式启用才创建且不允许子目录。 |
| RPC 导入边界 | `orders` 导入 `users/rpc`；`users/service`、`users/entity`、`users/util`。 | 合规样本通过；三类私有层样本在确定性检查和 CodeGraph 审查中失败。 |
| RPC 统一响应 | 成功、非法 JSON、校验失败、业务失败。 | 都可解析为 `code`、`status`、`message`、`data`。 |
| 渐进采用正向 | 已登记 `util/legacy.go`、`utils/discovery/polaris/`、`database/repository/`；改名后根级 `crontask/` 与业务域内部 `business/<domain>/crontask/`。 | adoption 通过且检查前后哈希相同。 |
| 渐进采用负向 | 遗留根新增源码或目录、未登记 `service/` 源码、项目或语言不符、重复/嵌套/越界/禁止清单路径。 | adoption 返回退出码 2 和稳定原因。 |

## 测试命令与断言

```powershell
python -m unittest discover -s doc/5-tests/2026-07-28_014412_代码位置目录规则V2/package-structure-rules -p "test_*.py"
python package-structure-rules/scripts/placement_catalog.py query --artifact utils --category discovery --technology polaris
python package-structure-rules/scripts/placement_catalog.py query --artifact source-util --language go
python package-structure-rules/scripts/placement_catalog.py query --artifact business-rpc
python micro-business-architecture-rules/scripts/micro_business.py check --root doc/5-tests/2026-07-28_014412_代码位置目录规则V2/package-structure-rules/fixtures/micro-business-rpc/good
python package-structure-rules/scripts/placement_catalog.py check --root <fixture-root> --project-kind backend --language go --policy strict
python package-structure-rules/scripts/placement_catalog.py check --root <legacy-fixture-root> --project-kind backend --language go --policy adoption --adoption-manifest doc/1-架构/3-目录规则收敛清单.yaml
```

| 断言 ID | 断言 | 失败预期 | 实际结果 |
|---|---|---|---|
| `AC-PSR-UTILS-001` | 根 `utils/` 直接文件必须被 strict 拒绝。 | 退出码 2 并定位文件。 | 通过。 |
| `AC-PSR-UTILS-002` | 四语言源码根 `util/` 直接代码文件可通过，子目录必须失败。 | 子目录退出码 2。 | 通过。 |
| `AC-PSR-UTILS-003` | `utils` 和 `source-util` 查询唯一，旧 artifact 失败关闭。 | 旧 artifact 返回错误。 | 通过。 |
| `AC-PSR-UTILS-004` | 后端 strict 缺少语言上下文必须失败。 | 参数错误退出码 2。 | 通过。 |
| `AC-PSR-UTILS-005` | strict 与 legacy 不改写 fixture。 | 检查前后哈希不同即失败。 | 通过。 |
| `AC-PSR-RPC-001` | Catalog 查询和渲染唯一展示业务域 `rpc/`，init 仅显式启用时创建。 | query、render 与 init fixture。 | 通过。 |
| `AC-PSR-RPC-002` | 仅精确目标域 `rpc/` 导入通过，私有层导入失败。 | 三个负向 Go fixture 与 CodeGraph 导入节点。 | 通过。 |
| `AC-PSR-RPC-003` | 四种 RPC 结果都可解析为统一响应字段。 | JSON 响应 fixture。 | 通过。 |
| `AC-PSR-ADOPT-001` | 已采纳 V2 目录和登记遗留快照可原地通过。 | Catalog ID 与目录快照 fixture。 | 通过。 |
| `AC-PSR-ADOPT-004` | `corntask` 拼写修正为 `crontask` 后，根级与业务域内部该目录仍被 adoption 接受。 | 根级 `crontask/` 与 `business/<domain>/crontask/` fixture。 | 通过。 |
| `AC-PSR-ADOPT-002` | 遗留根新增源码文件、目录和未登记源码必须失败。 | `util/new.go`、`util/new/`、`service/order.go` fixture。 | 通过。 |
| `AC-PSR-ADOPT-003` | 清单缺失、项目/语言不符、重复、嵌套、越界和禁止路径必须失败且不写入。 | 普通 YAML 正向 fixture、多个无效 YAML fixture 与哈希。 | 通过。 |

## 验证结论

本轮执行 31 项 `unittest`，结果为 `OK`。根 `utils/time/`、`utils/cron/`、`utils/json/`、`utils/log/` 和 `utils/discovery/{polaris,nacos}/` 的正向工具包样本、四语言源码根 `util/` 样本、普通 YAML 收敛清单、`orders -> users/rpc` 合规样本、改名后根级与业务域内部 `crontask/` 样本，以及已采纳目录与遗留快照均通过检查；三个私有层跨域导入、遗留新增源码/目录和无效收敛清单均得到可定位失败。严格检查、兼容检查与 adoption 检查均未改变 fixture 的目录树或文件哈希；CodeGraph 已在测试中同步索引并定位每个导入节点。

## 完成标准

1. 所有 31 项本地单元测试返回成功。
2. CLI 查询能返回四语言源码根 `util/` 和两个服务发现工具包的唯一路径。
3. strict 拒绝根 `utils/` 直接文件、旧根 `util/`、源码根 `util/` 子目录与业务域 `rpc/` 子目录。
4. 检查前后哈希相同，证明 `check` 只读。
5. `micro_business.py check` 与 CodeGraph 同时证明调用方不导入目标域私有层。
6. adoption 只放行人工登记的已采纳路径和遗留快照，拒绝新增遗留源码、目录和无效清单。

## 范围外说明

N/A；原因：本测试不验证真实数据库迁移、SDK 网络调用或浏览器体验。证据：计划范围 `BOUND-PSR-003` 限制为本地 Python、临时 fixture 和规则仓库。

## 执行附录

失败时先保留 CLI 输出和 fixture 哈希，再修复 Catalog、Schema 或 CLI 的唯一 Owner；禁止通过移动或改写 fixture 掩盖失败。测试结束后临时目录由测试框架自行清理。

## 追踪附录

| 上游需求 | 验收 | 测试文件 | 证据 |
|---|---|---|---|
| `REQ-PSR-UTILS-001` | `AC-PSR-UTILS-001` | `test_init_check.py` | 根工具目录文件负向断言。 |
| `REQ-PSR-SOURCE-UTIL-002` | `AC-PSR-UTILS-002` | `test_query_render.py`、`test_init_check.py` | 四语言扁平源码根工具断言。 |
| `REQ-PSR-CLI-003`、`RULE-PSR-STRICT-004` | `AC-PSR-UTILS-003` 至 `AC-PSR-UTILS-005` | 三个测试文件 | query、render、init、check 与哈希断言。 |
| `REQ-PSR-BUSINESS-RPC-004`、`RULE-PSR-RPC-005` | `AC-PSR-RPC-001`、`AC-PSR-RPC-002` | `test_business_rpc.py`、`fixtures/micro-business-rpc/` | Catalog、初始化、确定性隔离检查与 CodeGraph 导入节点断言。 |
| `RULE-PSR-RPC-006` | `AC-PSR-RPC-003` | `test_business_rpc.py` | 成功和三类失败的 JSON `Response` 断言。 |
| `REQ-PSR-ADOPT-001`、`RULE-PSR-ADOPT-001` | `AC-PSR-ADOPT-001` 至 `AC-PSR-ADOPT-003` | `test_adoption_check.py` | 已采纳目录、遗留快照、无效清单与无写入断言。 |
