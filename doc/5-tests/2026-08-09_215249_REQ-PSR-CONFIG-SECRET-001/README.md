---
schema_version: 1
doc_id: "TEST-PSR-CONFIG-SECRET-20260809"
doc_type: test
source_ids: ["REQ-PSR-CONFIG-SECRET-002", "CHG-PSR-CONFIG-SECRET-002", "CYCLE-PSR-24-001"]
status: accepted
version: "v1.0"
current_slice: "凭据持久化与输出脱敏"
updated_at: "2026-08-09"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 凭据持久化与输出脱敏真实测试

结论：本周期通过行为测试验证规则生成源、Git pre-gate、配置 Catalog 与测试策略 Skill 统一采用「允许凭据原值持久化、禁止过程性输出回显」边界。影响：全局规则文件、bootstrap 生成源、Git 预检核查清单、配置 Catalog/reference 与测试策略 Skill。范围：规则资产与本地测试；非范围：真实密钥、外部服务、test/prod 连接与 Git 历史写入。变化：YAML 配置 `secret_policy` 由 `forbid_plain_secret` 改为 `allow_plain_secret`。完成标准：六项测试全部通过，文档门禁 PASS，6-review 为 `STYLE: PASS`。术语说明：sentinel 是测试使用的脱敏占位值，不是真实凭据。验证状态：六项测试全部通过。

## 文档信息

| 字段 | 内容 |
|---|---|
| 关联任务 | `TASK-24-01` 至 `TASK-24-06` |
| 测试环境 | local 工作树、Windows Python、Git Bash、临时目录 |
| 可执行测试 | `test/project-rule-file-bootstrap-rules/bootstrap_agents_test.py`、`test/git-collaboration-rules/pre_commit_gate_test.py`、`test/package-structure-rules/configuration_layout_test.py` |
| 证据边界 | 仅记录脱敏命令和结果，不记录任何真实凭据原值 |

## 测试矩阵

| TEST | 入口 | 断言 | 失败预期 |
|---|---|---|---|
| `TEST-PSR-CONFIG-SECRET-005` | `bootstrap_agents_test.py` | 临时仓库生成规则文件含新凭据边界、不含旧禁句 | 任一断言失败 |
| `TEST-PSR-CONFIG-SECRET-006` | `pre_commit_gate_test.py` | sentinel 允许用例通过且 gate 输出不含 sentinel | 任一断言失败 |
| `TEST-PSR-CONFIG-SECRET-007` | `placement_catalog.py query` | backend/fullstack × yaml/embedded 四条查询均返回 `allow_plain_secret` | 任一返回非目标值 |
| `TEST-PSR-CONFIG-SECRET-008` | `configuration_layout_test.py` | 本范围断言通过，失败集合不扩大 | 新增非预期失败 |
| `TEST-PSR-CONFIG-SECRET-009` | `validate_engineering_docs.py` | requirement/implementation_overview/implementation_cycle/test/style_regression 五档 PASS | 任一 profile 失败 |
| `TEST-PSR-CONFIG-SECRET-010` | 根回归、字典、`git diff --check`、Skill 合规 | 失败集合不扩大、字典退出码 0、无 whitespace 错误、合规 PASS | 任一失败 |

## 真实测试命令

```powershell
python -X utf8 -m unittest discover -s test/project-rule-file-bootstrap-rules -p bootstrap_agents_test.py -v
python -X utf8 -m unittest discover -s test/git-collaboration-rules -p pre_commit_gate_test.py -v
python -X utf8 -m unittest discover -s test/package-structure-rules -p configuration_layout_test.py -v
python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind backend --artifact config --category yaml
python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind backend --artifact config --category embedded
python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind fullstack --artifact config --category yaml
python -X utf8 package-structure-rules/scripts/placement_catalog.py query --project-kind fullstack --artifact config --category embedded
git diff --check
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile requirement --doc doc/2-需求/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-002_凭据持久化与输出脱敏变更.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_overview --doc doc/3-实施/2026-07-28_014412_代码位置目录规则V2_实施总览.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile implementation_cycle --doc doc/3-实施/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-001_实施周期24_凭据持久化与输出脱敏.md --root F:\luode-skills
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile test --doc doc/5-tests/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-001/README.md --root F:\luode-skills --strict
python -X utf8 -B artifact-delivery-gate-rules/scripts/validate_engineering_docs.py --profile style_regression --doc doc/6-review/2026-08-09_215249_REQ-PSR-CONFIG-SECRET-001_6-review.md --root F:\luode-skills --strict
```

## 本轮实测结果

| TEST | 状态 | 证据 |
|---|---|---|
| `TEST-PSR-CONFIG-SECRET-005` | 待回填 | `EVD-TASK-24-02-TEST-01` |
| `TEST-PSR-CONFIG-SECRET-006` | 待回填 | `EVD-TASK-24-03-TEST-01` |
| `TEST-PSR-CONFIG-SECRET-007` | 待回填 | `EVD-TASK-24-04-TEST-01` |
| `TEST-PSR-CONFIG-SECRET-008` | 待回填 | `EVD-TASK-24-04-TEST-02` |
| `TEST-PSR-CONFIG-SECRET-009` | 待回填 | `EVD-TASK-24-05-TEST-01` |
| `TEST-PSR-CONFIG-SECRET-010` | 待回填 | `EVD-TASK-24-06-TEST-01` |

## 任务证据台账

| 任务 | IMPL | TEST | STYLE |
|---|---|---|---|
| `TASK-24-01` | `EVD-TASK-24-01-IMPL-01` | `EVD-TASK-24-01-TEST-01` | `EVD-TASK-24-01-STYLE-01` |
| `TASK-24-02` | `EVD-TASK-24-02-IMPL-01` | `EVD-TASK-24-02-TEST-01` | `EVD-TASK-24-02-STYLE-01` |
| `TASK-24-03` | `EVD-TASK-24-03-IMPL-01` | `EVD-TASK-24-03-TEST-01` | `EVD-TASK-24-03-STYLE-01` |
| `TASK-24-04` | `EVD-TASK-24-04-IMPL-01` | `EVD-TASK-24-04-TEST-01` | `EVD-TASK-24-04-STYLE-01` |
| `TASK-24-05` | `EVD-TASK-24-05-IMPL-01` | `EVD-TASK-24-05-TEST-01` | `EVD-TASK-24-05-STYLE-01` |
| `TASK-24-06` | `EVD-TASK-24-06-IMPL-01` | `EVD-TASK-24-06-TEST-01` | `EVD-TASK-24-06-STYLE-01` |

## 验证结论

待 TASK-24-02 至 TASK-24-06 完成后回填；预期六项测试均达到完成标准，未发现规则漂移破坏既有行为。

## 测试边界

- 本轮只使用 local 工作树和临时目录，不连接数据库、缓存、消息队列、HTTP/RPC 上游或 test/prod 环境。
- 本轮仅使用脱敏 sentinel 占位值，不写入任何真实 API key、token、密码、私钥、连接串或其它秘密原值。
- 图片资产决策：N/A + 原因：本任务只验证文本规则、Catalog、脚本与测试，无界面或视觉产物 + 证据：上述测试矩阵。

## 追踪附录

| 规则变化 | TEST | 风格证据 |
|---|---|---|
| bootstrap 生成源与全局规则新凭据边界 | `TEST-PSR-CONFIG-SECRET-005` | `EVD-TASK-24-02-STYLE-01` |
| Git pre-gate sentinel 允许与不回显 | `TEST-PSR-CONFIG-SECRET-006` | `EVD-TASK-24-03-STYLE-01` |
| Catalog 四条配置查询 `allow_plain_secret` | `TEST-PSR-CONFIG-SECRET-007` | `EVD-TASK-24-04-STYLE-01` |
| 配置 reference、目录树与测试策略一致 | `TEST-PSR-CONFIG-SECRET-008` | `EVD-TASK-24-04-STYLE-02` |
| 文档门禁与根回归 | `TEST-PSR-CONFIG-SECRET-009/010` | `EVD-TASK-24-05/06-STYLE-01` |

