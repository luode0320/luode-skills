---
schema_version: 1
doc_id: "TEST-PSR-TEST-ROOT-20260802"
doc_type: test
source_ids: ["REQ-PSR-TEST-ROOT-001", "CYCLE-PSR-TEST-ROOT-18-001"]
status: accepted
version: "v1.0"
current_slice: "TASK-18-04"
updated_at: "2026-08-02 23:50:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 三类项目根 test 目录统一真实测试

结论：本轮验证三类项目都把活动测试代码统一放在项目根 `test/`，并由 Catalog、目录树、查询、渲染和初始化共同表达；影响：测试程序、mock、fixture、helper 与测试说明拥有清晰的双根边界；范围：根 `test/` 目录事实、Catalog 条目、初始化骨架和既有入口/配置回归；非范围：真实业务项目迁移、CLI/Schema 重构、外部服务连接和 Git 历史写入；变化：fullstack、backend、frontend 均新增根 `test/`，`doc/5-tests/` 继续只保存说明与证据；完成标准：专项测试、全量根测试、适用文档 profile、Skill 校验和差异检查全部通过；术语说明：根 `test/` 是活动测试代码唯一入口，`doc/5-tests/` 是测试说明与证据入口；验证状态：专项测试 `4/4`、入口回归 `5/5`、配置回归 `7/7`、根 Python 测试 `212/212`、文档 profile、Skill 校验和差异检查均已通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联需求 | `REQ-PSR-TEST-ROOT-001` |
| 关联周期 | `CYCLE-18` |
| 测试环境 | local 工作树、Windows Python、临时目录 |
| 可执行代码根 | `test/` |
| 证据根 | 当前目录的 `evidence/` 与 `artifacts/` |

## 测试矩阵

| TEST | 入口 | 完成条件 | 样本/断言 | 失败预期 | 清理 |
| --- | --- | --- | --- | --- | --- |
| `TEST-PSR-TEST-ROOT-001` | `test/package-structure-rules/project_layout_contract_test.py` | `AC-PSR-TEST-ROOT-001` | 三类 Catalog、人工树和 skeleton 均包含根 `test/` | 任一目录事实缺失即失败 | `TemporaryDirectory` 自动清理 |
| `TEST-PSR-TEST-ROOT-002` | 同上 | `AC-PSR-TEST-ROOT-002` | 三类 query 唯一返回 `artifact_kind=test` 与 `canonical_path=test` | 返回 0 条或多条即失败 | 无外部状态 |
| `TEST-PSR-TEST-ROOT-003` | 同上 | `AC-PSR-TEST-ROOT-003` | 三类 render 输出根 `test/`，不出现竞争测试根 | 输出漂移即失败 | 无外部状态 |
| `TEST-PSR-TEST-ROOT-004` | 同上 | `AC-PSR-TEST-ROOT-004` | 三类 init 创建 `test/`，不创建测试文件或嵌套测试根 | 骨架或边界不符即失败 | `TemporaryDirectory` 自动清理 |
| `TEST-PSR-TEST-ROOT-005` | `entrypoint_layout_test.py`、`configuration_layout_test.py` | 前序周期不回归 | CYCLE-15 入口与 CYCLE-17 配置规则继续通过 | 任一既有专项失败即停止 | `-B` 不产生字节码 |
| `TEST-PSR-TEST-ROOT-006` | `test/run_python_tests.py` | 根测试入口完整通过 | 只发现根 `test/` 下的活动测试 | 发现历史 `doc/5-tests` 可执行资产即失败 | Python 临时缓存清理 |

## 完成标准

- `TEST-PSR-TEST-ROOT-001..004` 的专项断言通过，三类 Catalog、人工树、render 和 init 对根 `test/` 给出一致结论。
- `TEST-PSR-TEST-ROOT-005..006`、`test` profile、Skill 校验和 `git diff --check` 均已通过，本轮测试说明标记为 `accepted`。
- 任何 profile、专项测试或全量入口失败，都保留 `in_progress` 并停止 6-review 放行。

## 真实测试命令

```powershell
python -X utf8 -B test/package-structure-rules/project_layout_contract_test.py
python -X utf8 -B .system/skill-creator/scripts/quick_validate.py package-structure-rules
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-02_235000_三类项目根test目录统一/README.md --root F:\luode-skills --strict
python -X utf8 -B test/run_python_tests.py
git diff --check
```

## 测试边界

- 只使用本地规则仓库文件、Python 标准库和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或任何非 local 环境。
- 不修改历史 `doc/5-tests/` 可执行资产，不在测试说明目录新增可执行程序、mock、fixture 或 helper。
- `6-review` 只判断格式、写法、位置、注释、可读性和目录归位，不替代目录契约测试、需求覆盖或发布放行。
- 图片资产决策：N/A + 原因：本轮只验证文本规则、目录和 CLI 行为，没有视觉产物 + 证据：测试矩阵与命令均为文本/路径断言。

## 当前实测结果

| TEST | 状态 | 证据 |
| --- | --- | --- |
| `TEST-PSR-TEST-ROOT-001..004` | `4/4` 通过 | `EVD-TASK-18-02-TEST` |
| `TEST-PSR-TEST-ROOT-005` | `12/12` 通过：入口 `5/5`、配置 `7/7` | `EVD-TASK-18-04-TEST` |
| `TEST-PSR-TEST-ROOT-006` | `212/212` 通过 | `EVD-TASK-18-04-TEST` |

## 执行附录

本轮脱敏日志、报告和非可执行产物仅允许写入当前目录的 `evidence/` 或 `artifacts/`；不得在此目录新增 Python、Go、PowerShell、JavaScript 或其他可执行文件。

## 追踪附录

| AC | TASK | TEST | 证据 |
| --- | --- | --- | --- |
| `AC-PSR-TEST-ROOT-001` | `TASK-18-02` | `TEST-PSR-TEST-ROOT-001` | `EVD-TASK-18-02-TEST` |
| `AC-PSR-TEST-ROOT-002` | `TASK-18-02` | `TEST-PSR-TEST-ROOT-002` | `EVD-TASK-18-02-TEST` |
| `AC-PSR-TEST-ROOT-003` | `TASK-18-02` | `TEST-PSR-TEST-ROOT-003` | `EVD-TASK-18-02-TEST` |
| `AC-PSR-TEST-ROOT-004` | `TASK-18-03..04` | `TEST-PSR-TEST-ROOT-004..006` | `EVD-TASK-18-03-TEST`、`EVD-TASK-18-04-TEST` |
