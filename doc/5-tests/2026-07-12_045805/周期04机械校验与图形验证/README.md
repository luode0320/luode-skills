---
schema_version: "1.0"
doc_id: "TEST-DOC-20260712-045805-C04"
doc_type: "test_record"
template_version: "v1.0-extreme"
source_ids:
  - "REQ-DOC-20260712-033322"
  - "DOC-IMPL-CYCLE-04-20260712-045805"
status: "accepted"
version: "v1.0"
current_slice: "C04"
updated_at: "2026-07-12"
---

# 周期 04 机械校验与 Mermaid 真解析验证

## 目标与边界

验证严格追踪链、五类 profile、负向 fixture 和 Mermaid CLI 真解析。脚本只读取 local 仓库与本机 npm 缓存，不连接数据库、消息队列、HTTP/RPC 或 test/prod 环境；临时 SVG 写入系统临时目录，测试结束自动清理。

## 真实入口

```powershell
python -X utf8 doc/5-tests/2026-07-12_045805/artifact_delivery_gate_rules/test_cycle04_gate_and_mermaid.py
python -X utf8 -m unittest artifact-delivery-gate-rules/tests/test_validate_engineering_docs.py -v
```

测试脚本通过 `npx --offline --yes @mermaid-js/mermaid-cli` 对六份当前文档真解析，要求退出码为 `0`、每份至少生成一个非空 SVG，总数不少于 8；无法找到 `npx`、离线包缺失或任一图解析失败均为 `BLOCKED`。

## 覆盖矩阵

| ID | 覆盖 | 正例 | 负例/断言 |
| --- | --- | --- | --- |
| `EVD-T04-01-TEST-01` | 严格追踪 fixture | `REQ -> AC -> CYCLE -> TASK -> TEST -> EVIDENCE` 完整链通过 | 缺 REVIEW 证据被拒绝 |
| `EVD-T04-01-TEST-02` | 六份当前文档 profile | requirement/acceptance/overview/cycle 全部 `valid: true` | 任一 profile 失败即阻断 |
| `EVD-T04-02-TEST-01` | Mermaid CLI 真解析 | 6 份文档生成 12 个非空 SVG | 无 npx、CLI 非零或无 SVG 即 BLOCKED |
| `EVD-T04-02-TEST-02` | Mermaid 静态负例 | `broken_mermaid.md` 被 delimiter 检查拒绝 | 不允许截图替代源码/解析 |

## 实际结果

`python -X utf8 artifact_delivery_gate_rules/test_cycle04_gate_and_mermaid.py`：3 tests OK，退出码 `0`；strict、六份 profile 和 Mermaid CLI 真解析全部通过。

## 清理与回滚

测试不写业务数据；临时目录由 `TemporaryDirectory` 自动清理。若 CLI 或追踪校验失败，保留终端输出和失败文档指纹，只回滚周期 04 新增校验/测试资产，不改动周期 01-03 已验收文档。

## 当前状态

本 README 记录测试入口和验收标准；实际 PASS/FAIL 必须以脚本真实退出码和产物清单回填，不以计划文字代替证据。
