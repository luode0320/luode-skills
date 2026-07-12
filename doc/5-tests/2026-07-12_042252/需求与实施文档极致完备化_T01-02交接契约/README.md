---
schema_version: 1
doc_id: "TEST-DOC-20260712-042252-T01-02"
doc_type: test_record
source_ids:
  - "REQ-DOC-20260712-033322"
  - "T01-02"
status: accepted
version: "v1.0"
current_slice: "C01"
updated_at: "2026-07-12"
---

# T01-02 交接契约与质量 profile 测试记录

## 测试目的

验证 `T01-02` 的公共交接契约、五类文档 profile、正例文档和关键负例能够在 local 只读条件下稳定判定。该测试不修改生产代码、Skill 资产、需求/实施文档或外部环境。

## 测试资产入口

| 资产 | 路径 | 说明 |
| --- | --- | --- |
| 主测试脚本 | `doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/test_handoff_contract.py` | 控制台过程日志、正例/负例断言和最终退出码 |
| fixture 目录 | `doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/fixtures/` | 缺章节、占位词、N/A 无证据和 N/A 有证据样本 |
| 被测契约 | `artifact-delivery-gate-rules/references/document-handoff-contract.md` | MUST、追踪、图形、低推理演练和放行顺序 |
| 被测 profile | `artifact-delivery-gate-rules/references/document-quality-profiles.yaml` | requirement、acceptance、implementation_master、implementation_overview、implementation_cycle |
| 被测校验器 | `artifact-delivery-gate-rules/scripts/validate_engineering_docs.py` | UTF-8、元数据、章节、ID、链接、占位词、N/A、图形与表格门禁 |

## 执行前置条件

- Windows 本地 Python 3 与 PyYAML 可用。
- 工作目录为仓库根目录 `C:\Users\luode\.codex\skills`。
- 仅读取仓库中的 Markdown、YAML 和 Python 文件；不读取或写入 `test`、`staging`、`prod`、`production` 配置。
- 不连接数据库、缓存、消息队列、HTTP/RPC 上游或外部模型；测试脚本只在内存中执行断言。
- 目标时间戳目录为当前测试轮 `2026-07-12_042252`，不复用历史测试目录。

## 运行命令

```powershell
python -X utf8 doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/test_handoff_contract.py
```

脚本必须输出 `开始`、每个关键 `步骤`、失败时的 `失败点` 和最终 `结束` 日志；退出码 `0` 表示通过，退出码 `1` 表示任一断言失败。

## 覆盖矩阵

| 场景 ID | 覆盖内容 | 样本/入口 | 通过标准 |
| --- | --- | --- | --- |
| `TEST-T01-02-POS-001` | 五类 profile 正例 | 当前需求、验收、全量顺序、实施总览、周期 01 文档 | 每个 profile 的 `validate_document` 返回 `valid: true` |
| `TEST-T01-02-CONTRACT-001` | 契约关键条款 | `document-handoff-contract.md` | MUST、条件必填、N/A、双向追踪、100%覆盖、Mermaid 真解析、普通模型演练条款均存在 |
| `TEST-T01-02-PROFILE-001` | profile 字段矩阵 | `document-quality-profiles.yaml` | 五类 profile 均有章节、ID、图形、表格和必需短语配置 |
| `TEST-T01-02-NEG-001` | 缺章节 | `fixtures/acceptance_missing_section.md` | 返回 `valid: false`，包含缺少“验收场景”错误 |
| `TEST-T01-02-NEG-002` | 占位词 | `fixtures/requirement_placeholder.md` | 返回 `valid: false`，包含 placeholder/vague 错误 |
| `TEST-T01-02-NEG-003` | N/A 无原因/证据 | `fixtures/implementation_cycle_na_without_reason.md` | 返回 `valid: false`，包含 `N/A requires reason/evidence` |
| `TEST-T01-02-POS-002` | N/A 有原因/证据 | `fixtures/na_with_reason.md` | `check_na_reasons` 不产生错误 |

## 测试步骤与实际结论

1. 加载 profile YAML 和校验器模块，显式 UTF-8 读取所有输入。
2. 检查交接契约关键条款与五类 profile 字段集合。
3. 运行五类目标文档 profile 正例。
4. 运行缺章节、占位词、N/A 无证据三个负例，确认均被阻断。
5. 运行 N/A 有原因与证据正例，确认不误报。
6. 汇总控制台退出码和失败点；任一步骤失败即结束并返回非零。

## 证据 ID 映射

| 证据 ID | 证据类型 | 磁盘落点/命令 | 当前结论 |
| --- | --- | --- | --- |
| `EVD-T01-02-IMPL-01` | 测试资产实现 | 本 README、`test_handoff_contract.py` 与 `fixtures/` | 已落盘；仅覆盖 T01-02 测试写集 |
| `EVD-T01-02-TEST-01` | 真实测试 | `python -X utf8 doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/test_handoff_contract.py` | 退出码 `0`；五类正例 PASS、三个负例 BLOCKED、N/A 正例 PASS |
| `EVD-T01-02-REVIEW-01` | 实现审查 | N/A；原因与证据：本写集只负责测试资产，独立审查由父 agent 按 `doc/6-审查/` 归档 | 待父 agent 审查 |
| `EVD-T01-02-ACCEPT-01` | 任务验收 | N/A；原因与证据：任务验收需结合审查和周期收口，不由测试脚本单独放行 | 待父 agent 验收 |

## 验收与失败标准

- 通过：命令退出码为 `0`，五类 profile 正例全部 PASS，契约/profile 条款全部 PASS，三个负例全部 BLOCKED，N/A 合规正例 PASS，并输出完整过程日志。
- 失败：任一正例被拒绝、任一负例放行、N/A 有证据被误报、关键条款缺失、输入非 UTF-8、脚本异常退出或输出缺少开始/步骤/结束/失败点信息。
- 本测试不宣称 Mermaid CLI 真解析或低推理模型演练已完成；这些属于契约要求的后续独立证据，若执行需单独归档并回写实施周期。

## 验证结论

| 字段 | 实际结果 |
| --- | --- |
| 执行时间 | 2026-07-12 04:29:13 +08:00 |
| 执行人 | Codex 子 agent `cycle01_audit` |
| 执行环境 | Windows local；只读仓库文件；未连接外部服务 |
| 执行命令 | `python -X utf8 doc/5-tests/2026-07-12_042252/artifact-delivery-gate-rules/test_handoff_contract.py` |
| 退出码 | `0` |
| 实际结论 | `PASS`：五类 profile、契约关键条款、三个负例和 N/A 合规正例均符合预期 |
| 过程证据 | 控制台输出包含 `开始`、逐项 `步骤` 和 `结束: PASS`，失败时脚本会输出 `失败点` 并返回非零 |

本记录只证明本脚本覆盖的静态正反验证；不将 Mermaid CLI 真解析、低推理模型演练或全量双向追踪扫描冒充已完成。

## 未覆盖项与后续边界

- 未连接任何外部服务，未修改数据。
- 未执行 Mermaid CLI 真解析、低推理模型零决策演练、跨文档双向覆盖率扫描或重复/孤立 ID 全量扫描；这些不属于本脚本的静态正反验证范围。
- 本测试只覆盖 T01-02 契约/profile 资产，不替代 T01-01 任务审查、C01-CLOSE 周期验收或最终验收。
