---
schema_version: 1
doc_id: "TEST-DOC-20260712-042832-C02"
doc_type: "test_record"
source_ids:
  - "REQ-DOC-20260712-033322"
  - "DOC-IMPL-CYCLE-02-20260712-042832"
status: "accepted"
version: "v1.0"
current_slice: "C02"
updated_at: "2026-07-12"
---

# 周期 02 需求与验收 Skill 极致完整性行为测试

## 测试目的

验证六个需求/验收 Skill 的模板、硬闸门和默认提示是否冻结了普通模型执行所需的字段、稳定 ID、图形、二值验收、阻断、清理、回滚和双向追踪。本测试只读取 local 工作区文件，不连接数据库、缓存、消息队列、HTTP/RPC 上游或任何 test/prod 环境。

## 测试入口与样本

| 资产 | 路径 | 用途 |
| --- | --- | --- |
| 主脚本 | `doc/5-tests/2026-07-12_042832/需求与验收Skill极致完整性行为测试/test_extreme_requirements.py` | 四个任务正反行为断言 |
| T02-01 | `requirement-intake-rules/references/requirement-structure-template.md`、`agents/openai.yaml` | 来源/决策/REQ/RULE/图形/追踪字段 |
| T02-02 | `requirement-gap-rules/SKILL.md`、`references/missing-info-checklist.md`、`agents/openai.yaml` | GAP 分级、授权和 blocked |
| T02-03 | boundary/splitting/change 三组 Skill 资产 | BOUND/SLICE/CHG 唯一归属与回开 |
| T02-04 | `acceptance-criteria-rules/references/acceptance-template.md`、`agents/openai.yaml` | AC 二值化、路径覆盖和证据 |

## 执行前置条件

- Windows local Python 3 可执行，工作目录为 `C:\Users\luode\.codex\skills`。
- 使用显式 UTF-8 读取；脚本只在内存中构造缺字段负例，不写入仓库。
- 不使用 test/staging/pre/release/prod/production 配置，不连接外部服务。
- 六个 Skill 的 quick validator 在脚本之后逐个执行。

## 运行命令

```powershell
python -X utf8 doc/5-tests/2026-07-12_042832/需求与验收Skill极致完整性行为测试/test_extreme_requirements.py --case all
```

单任务复验：

```powershell
python -X utf8 doc/5-tests/2026-07-12_042832/需求与验收Skill极致完整性行为测试/test_extreme_requirements.py --case T02-01
```

## 覆盖矩阵

| 测试 ID | 覆盖内容 | 正例断言 | 负例断言 |
| --- | --- | --- | --- |
| `TEST-C02-01` | 需求入口完整模板 | SRC/DEC/REQ/RULE/AC、N/A、unresolved、flowchart、sequenceDiagram、blocked 均存在 | 移除来源字段后必须识别缺失 |
| `TEST-C02-02` | 缺口与决策阻断 | GAP、P0/P1/P2、授权/有效期/复核、清理/回滚存在 | 移除 GAP 字段后必须识别缺失 |
| `TEST-C02-03` | 边界/切片/变更传播 | BOUND/SLICE/CHG、范围、文件符号、DAG、原值新值、回开存在 | 移除 BOUND 字段后必须识别缺失 |
| `TEST-C02-04` | 二值 AC 与追踪 | AC/REQ、PASS/FAIL、local、失败预期、清理/回滚、图形存在 | 移除 AC 字段后必须识别缺失 |

脚本将“缺少任一关键字段”作为稳定负向断言；这模拟普通模型拿到不完整文档时必须阻断，而不是自行补决策。

## 证据登记

| 证据 ID | 类型 | 命令/落点 | 结论 |
| --- | --- | --- | --- |
| `EVD-T02-01-IMPL-01` | 实现 | T02-01 两个 Skill 资产 diff | 已落盘 |
| `EVD-T02-02-IMPL-01` | 实现 | T02-02 三个 Skill 资产 diff | 已落盘 |
| `EVD-T02-03-IMPL-01` | 实现 | T02-03 六个 Skill 资产 diff | 已落盘 |
| `EVD-T02-04-IMPL-01` | 实现 | T02-04 两个 Skill 资产 diff | 已落盘 |
| `EVD-C02-TEST-01` | 真实测试 | `python -X utf8 .../test_extreme_requirements.py --case all` | PASS；T02-01 至 T02-04 正例通过，缺字段负例按预期阻断 |
| `EVD-C02-TEST-02` | Skill 校验 | 六个 `quick_validate.py` 命令 | PASS；六个 Skill 全部 `Skill is valid!` |
| `EVD-C02-TEST-03` | 编码/写集检查 | `Get-Content -Encoding UTF8`、`git diff --check`、Skill 目录 diff/stat | PASS；UTF-8 可回读、无空白错误；仅周期 02 授权写集由本 agent 修改 |
| `EVD-C02-REVIEW-01` | 实现审查 | 周期 02 实现审查文档 | PASS；`EVD-C02-REVIEW-01` |
| `EVD-C02-ACCEPT-01` | 任务验收 | 周期 02 C02-CLOSE 验收证据 | PASS；`EVD-C02-CLOSE-ACCEPT-01` |

## 通过、失败、清理与回滚

- 通过：四个 case 正例均 PASS，缺字段负例均被脚本识别，六个 Skill quick validator 均 PASS，UTF-8 回读和 `git diff --check` PASS。
- 失败：任一正例缺字段、负例未识别、脚本非零异常、quick validator 失败、编码乱码或写集越界；必须停止当前任务并保留输出。
- 清理：脚本不创建持久化 fixture，不写数据库，不写外部服务；无需数据清理。
- 回滚：只撤销本周期新增的 Skill 条款、default prompt、周期文档和测试目录；不删除周期 01 或父任务已有证据。

## 当前验证结论

| 项目 | 状态 |
| --- | --- |
| 测试脚本 | 已落盘并执行 PASS（`EVD-C02-TEST-01`） |
| 四个任务真实行为测试 | PASS；正反断言均符合预期（`EVD-C02-TEST-01`） |
| 六个 Skill quick validator | PASS；六个 Skill 全部通过（`EVD-C02-TEST-02`） |
| UTF-8 与写集边界 | PASS；回读、diff 检查无错误（`EVD-C02-TEST-03`） |
| 周期 02 审查与验收 | PASS；`EVD-C02-REVIEW-01`、`EVD-C02-CLOSE-ACCEPT-01` |

本 README 不宣称尚未执行的命令已通过；所有结果必须在命令真实退出后回填对应证据行。
