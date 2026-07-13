---
schema_version: 1
template_version: 1
doc_id: CYCLEDOC-OBS-01-20260713
doc_type: implementation_cycle
source_ids:
  - IMPLDOC-OBS-20260713
  - ACCDOC-OBS-20260713
status: confirmed
version: 1.0
complexity: L2
baseline_commit: unknown
current_slice: TASK-OBS-04
updated_at: 2026-07-13 17:17:55
---

# CYCLE-OBS-01 跨宿主 CLI 桥接

图片资产决策：N/A + 原因：任务依赖与验证分支均由 Mermaid 和矩阵表达 + 证据：TASK-OBS-01 至 TASK-OBS-04。

## 当前代码/文档基线

| 基线 | 事实 |
| --- | --- |
| 文档 | `REQDOC-OBS-20260713`、`ACCDOC-OBS-20260713`、`IMPLDOC-OBS-20260713` 已冻结 |
| 运行 | Windows Obsidian CLI 是唯一目标宿主；WSL 当前不能依赖原生 `obsidian` |
| 安全 | 固定 root 为 `D:\obsidian_data`；所有 vault 操作 CLI-only；local 环境 |
| 图片资产决策 | N/A + 原因：本周期仅 bridge、脚本、测试与 Markdown，流程以 Mermaid 表达 + 证据：AC-OBS-001~006 |

## 周期内最小任务执行顺序

图形目的：固定“当前任务独立闭环后才可继续”的顺序。关联 ID：CYCLE-OBS-01、TASK-OBS-01、TASK-OBS-04。

```mermaid
flowchart LR
  T1[TASK-OBS-01 文档] --> V1[validator + review + accept]
  V1 --> T2[TASK-OBS-02 Python bridge]
  T2 --> V2[unit + review + accept]
  V2 --> T3[TASK-OBS-03 PS adapter]
  T3 --> V3[contract + review + accept]
  V3 --> T4[TASK-OBS-04 双端 smoke]
  T4 --> C[周期收口]
```

## 当前周期目标、边界与进入条件

目标是建立可独立测试的 Windows/WSL transport；进入条件是需求、验收、唯一 vault 根与 local 安全边界均已冻结。边界是不迁移 `distill_vault.py`、SKILL.md 或 references，直到 TASK-OBS-04 通过。

## 进入条件与收口条件

收口要求 Windows/WSL doctor 和 smoke 全部 `verified=true`，且 selector、interop、路径与 readback 的异常路径均有稳定测试证据。

## 最小任务闭环

| TASK | 文件/符号 | 实现 | 真实测试 | 审查/验收证据 | 停止条件 | 回滚 |
| --- | --- | --- | --- | --- | --- | --- |
| TASK-OBS-01 | 4 份研发文档 | 落盘 SRC/DEC/REQ/AC/CYCLE/TASK/TEST 追踪 | 四个 profile validator | EVD-TASK-OBS-01-IMPL/TEST/REVIEW/ACCEPT | validator、图或 ID 失败 | ROLLBACK-OBS-001：仅撤回本轮文档 |
| TASK-OBS-02 | `scripts/obsidian_cli_bridge.py`、ASCII test/fixture | host、path、temp JSON、project identity | native/UNC/WSL、Unicode、traversal 单元测试 | EVD-TASK-OBS-02-* | identity 不一致、日志泄漏 | ROLLBACK-OBS-002：删除新 bridge，不写 vault |
| TASK-OBS-03 | `scripts/obsidian_cli_windows.ps1`、contract fake CLI | startup、selector、allowlist、readback | success/timeout/zero/multi vault 契约 | EVD-TASK-OBS-03-* | 需直写 vault 或杀进程 | ROLLBACK-OBS-003：删除 adapter |
| TASK-OBS-04 | current test README、fixture/证据 | Windows/WSL smoke 流程 | create/read/append/read | EVD-TASK-OBS-04-* | interop/selector/readback 失败 | ROLLBACK-OBS-004：覆盖 smoke 为 fixture |

## 当前周期验证矩阵

| TEST | 输入样本 | 命令/动作 | 断言与清理 |
| --- | --- | --- | --- |
| TEST-OBS-001 | Windows fixed vault | doctor | 唯一 selector；无写入 |
| TEST-OBS-002/005 | UNC 与 Linux 同项目 | project-context | 同一 `wsl://` ID；删除临时 JSON |
| TEST-OBS-003/004/013 | WSL interop、中文 smoke | doctor/create/read/append | transport 与双端正文一致；覆盖 fixture |
| TEST-OBS-006/011 | app unavailable、vault list fixture | adapter fake CLI | 一次启动、稳定错误；不杀进程 |
| TEST-OBS-008/010/015 | traversal、10KB Unicode、敏感正文 | bridge unit test | CLI 未调用或完整 readback；日志无正文 |

## 真实测试与断言

每个命令只使用 local 环境；断言以 JSON `ok/code/transport/verified`、读回文本和临时文件清理结果为准。build 或静态阅读不替代上述真实测试。

## 周期阻断、停止与回滚

若自动启动一次后应用仍不可达、selector 非唯一、interop 不可用、path 越界执行 CLI 或 readback 不一致，立即停止当前 TASK，按 ROLLBACK-OBS-001 至 004 清理新增资产或 smoke fixture，不进入 CYCLE-OBS-02。

## 周期完成条件与最大推进边界

| 类型 | 条件 |
| --- | --- |
| 完成条件 | TASK-OBS-01 至 TASK-OBS-04 各自完成实现、真实测试、审查、验收；Windows/WSL doctor 与 smoke 均通过 |
| 停止条件 | AC-OBS-003、AC-OBS-004 或 AC-OBS-005 的失败标准命中 |
| 最大推进边界 | CYCLE-OBS-01 未收口前不迁移 `distill_vault.py`、SKILL.md 或 references；不连接非 local 环境 |
| 回滚 | ROLLBACK-OBS-001 至 ROLLBACK-OBS-004 均只触及当前需求新增资产，不删除用户笔记 |

## 自审结论

TASK-OBS-02 至 TASK-OBS-03 已完成实现、离线真实测试与实现自审：bridge 单测 `16/16 PASS`、adapter 契约测试 `17/17 PASS`、Python 编译和 PowerShell parser PASS。TASK-OBS-03 已补齐 adapter 直调 `limit=1..100` 防线、query/limit argv 完整性断言，以及预检/写命令语义错误与 `Error:` 正文的分域处理。TASK-OBS-04 已完成 Windows/WSL doctor、Windows create/read、WSL read/append、Windows readback 和中性 fixture 覆盖，所有成功响应均为 `verified=true`。

AC-OBS-003 已取得实机证据：用户关闭 Obsidian 后，Windows `doctor` 自动隐藏启动一次并在第 3 次探测返回 `started_app=true`、`ok=true`、`verified=true`。该路径未杀死任何用户既有进程，符合 DEC-OBS-003。

公开检索入口已完成实机复验：修复 PowerShell 参数数组拆分后，Windows `search`、Windows `search-context` 与 WSL `search` 均返回 `ok=true`、`verified=true`。TASK-OBS-04 已完成，CYCLE-OBS-01 已收口，允许按计划进入 CYCLE-OBS-02。

## 追踪矩阵

| CYCLE | TASK | AC | TEST | ROLLBACK | EVIDENCE |
| --- | --- | --- | --- | --- | --- |
| CYCLE-OBS-01 | TASK-OBS-01 | AC-OBS-001~006 | profile validators | ROLLBACK-OBS-001 | EVD-TASK-OBS-01-IMPL/TEST/REVIEW/ACCEPT |
| CYCLE-OBS-01 | TASK-OBS-02 | AC-OBS-002/005/006 | TEST-OBS-002/005/008/009/010 | ROLLBACK-OBS-002 | EVD-TASK-OBS-02-IMPL/TEST/REVIEW/ACCEPT |
| CYCLE-OBS-01 | TASK-OBS-03 | AC-OBS-001/003/004/005 | TEST-OBS-001/006/011/012 | ROLLBACK-OBS-003 | EVD-TASK-OBS-03-IMPL/TEST/REVIEW/ACCEPT |
| CYCLE-OBS-01 | TASK-OBS-04 | AC-OBS-001~005 | TEST-OBS-003/004/013 | ROLLBACK-OBS-004 | EVD-TASK-OBS-04-IMPL/TEST/REVIEW/ACCEPT |

## 执行证据更新

| EVIDENCE | 结论 | 说明 |
| --- | --- | --- |
| EVD-TASK-OBS-02-TEST | PASS | `test_obsidian_cli_bridge.py` 16/16；覆盖 WSL 三路径、结构化失败码和 path 原始空白。 |
| EVD-TASK-OBS-03-TEST | PASS | `test_obsidian_cli_contract.py` 17/17；覆盖固定根、重复 vault、10KB 中文、长 stdout、read/search 正文与预检/写命令 `Error:` 边界、vault listing 语义错误、`limit=1..100`、search argv 与 readback。 |
| EVD-TASK-OBS-04-WINDOWS | PASS | 官方 Windows CLI doctor/create/read/append/read 均 `ok=true`、`verified=true`，最终 smoke note 为中性 fixture。 |
| EVD-TASK-OBS-04-WSL | PASS | WSL interop doctor/read/append 均 `ok=true`、`transport=wsl-powershell-interop`。 |
| EVD-TASK-OBS-04-AUTOSTART | PASS | 用户关闭 Obsidian 后，Windows `doctor` 返回 `started_app=true`、`attempts=3`、`ok=true`、`verified=true`。 |
| EVD-TASK-OBS-04-SEARCH | PASS | 修复 `query=`/`limit=` 参数拆分后，Windows search/search-context 与 WSL search 均 `ok=true`、`verified=true`。 |
