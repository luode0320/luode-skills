---
schema_version: "1.0"
doc_id: "TEST-DOC-20260712-061500-C05"
doc_type: "test_record"
template_version: "v1.0-extreme"
source_ids:
  - "REQ-DOC-20260712-033322"
  - "DOC-IMPL-CYCLE-05-20260712-061500"
status: "accepted"
version: "v1.0"
current_slice: "C05"
updated_at: "2026-07-12"
---

# 周期 05 全局同步与最终验收验证

## 目标与边界

验证存储路径、交付闸门、仓库入口、Skill 字典、项目四件套、固定 Obsidian vault、五类文档 profile 和周期 05 Mermaid 真解析。脚本只读取 local 仓库和固定 vault，临时 SVG 写入系统临时目录后自动清理；不连接数据库、消息队列、HTTP/RPC 或 test/prod 环境。

## 真实入口

```powershell
python -X utf8 doc/5-tests/2026-07-12_061500/artifact_delivery_gate_rules/test_cycle05_global_sync.py
python -X utf8 -m unittest artifact-delivery-gate-rules/tests/test_validate_engineering_docs.py -v
python -X utf8 doc/5-tests/2026-07-12_042832/需求与验收Skill极致完整性行为测试/test_extreme_requirements.py
python -X utf8 doc/5-tests/2026-07-12_042731/implementation_planning_cycle03/test_cycle03_contract.py
python -X utf8 doc/5-tests/2026-07-12_045805/artifact_delivery_gate_rules/test_cycle04_gate_and_mermaid.py
```

## 覆盖矩阵

| ID | 覆盖 | 正例与断言 | 失败/阻断标准 |
| --- | --- | --- | --- |
| `EVD-T05-01-TEST-01` | 存储与入口同步 | path-map、仓库规则、owner Skill 和 profile 关键入口存在且语义一致 | 根目录、owner 或 gate 冲突即 BLOCKED |
| `EVD-T05-02-TEST-01` | 字典与项目四件套 | 字典源/产物存在；current、memory、history 职责和 UTF-8/大小约束通过 | 生成失败、职责串位、敏感扫描命中即 BLOCKED |
| `EVD-T05-02-TEST-02` | Obsidian 固定 vault | `version`、`vaults verbose`、`search`、`read` 成功，既有沉淀笔记内容可定位；本测试只读，不重复追加 | CLI 不可用或 vault 不一致即 BLOCKED，不使用文件系统 fallback |
| `EVD-T05-03-TEST-01` | 全量 profile | 需求、验收、总表、总览和周期 01-05 全部 `valid: true` | 任一结构/ID/链接/图形失败即 BLOCKED |
| `EVD-T05-03-TEST-02` | Mermaid 真解析 | 周期 05 生成至少 2 个非空 SVG，周期 04 全量图继续 PASS | npx 非零、离线包缺失或 SVG 为空即 BLOCKED |
| `EVD-T05-03-TEST-03` | 规则回归 | 校验器单测、周期 02/03/04 行为测试和四个 Skill quick validator 全部通过 | 任一退出码非零即 BLOCKED |

## 实际结果

`python -X utf8 doc/5-tests/2026-07-12_061500/artifact_delivery_gate_rules/test_cycle05_global_sync.py`：6 tests OK，退出码 `0`；9 份当前文档 profile、最终验收输入一致性、入口同步、项目记忆/字典、敏感 diff 扫描、固定 vault CLI 读回和周期 05 Mermaid 真解析均通过。周期 04 Mermaid CLI 回归仍为 6 份文档、12 个非空 SVG。Obsidian 既有沉淀笔记通过 `obsidian vault=知识库 read` 读回并确认“周期 05 收口”段落存在；本测试不重复写入 vault。

## 清理与回滚

测试不写业务数据；Mermaid 临时目录由 `TemporaryDirectory` 自动清理。若入口、字典、CLI、profile 或 Mermaid 失败，保留终端输出和文件指纹，只撤销周期 05 新增测试资产，不改动周期 01-04 已验收规则资产。

## 当前状态

周期 05 任务按 `T05-01 -> T05-02 -> T05-03` 顺序执行；每个任务均需实现/落盘、真实测试、审查和验收四类证据，收口后才允许最终放行。
