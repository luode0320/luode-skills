---
schema_version: 1
template_version: 1
doc_id: "STYLE-TEST-MOCK-20260802-01"
doc_type: style_regression
source_ids: ["REQ-TEST-LAYOUT-20260801"]
status: accepted
version: "v1.0"
current_slice: "TASK-TEST-MOCK-MIRROR-01"
updated_at: "2026-08-02 23:33:30"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review 风格回归：测试 mock 源码镜像规则

结论：本轮核对测试 Skill 对 mock、stub、fake、fixture、helper 的目录归位、命名和证据边界；影响：模拟程序与测试程序都能从根 `test/` 的源码镜像路径发现；范围：六个相关 Skill、路径映射、测试契约和字典索引；非范围：业务逻辑、真实项目迁移、历史 `doc/5-tests/` 可执行资产和 Git 历史；变化：源码专属模拟程序必须与对应测试使用同一源码相对路径，跨源码复用才进入 `test/shared/`；完成标准：`STYLE: PASS`；术语说明：无技术术语需要解释；验证状态：治理测试 `13/13`、根 Python 测试 `216/216`、六个 Skill 校验和字典生成均已通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-TEST-MOCK-MIRROR-01` |
| 关联真实测试 | `TEST-TEST-MOCK-MIRROR-001` |
| 检查时点 | 真实测试通过后 |

## 检查范围

- 检查 `artifact-storage-rules`、`test-strategy-rules`、`test-program-rules`、`functional-validation-rules`、`test-regression-rules`、`project-interface-release-execution-rules` 及其直接 references/agent 提示。
- 检查 `test/shared/layout_policy.py`、`test/test-asset-governance/asset_location_test.py` 的测试资产归位、源码路径镜像、错误目录拒绝和字典同步。
- 检查 UTF-8、Markdown 层级、命名、目录落点、尾随空白和历史 `doc/5-tests/` 只读边界。
- 范围外：不判断业务正确性、需求覆盖率、外部服务连通性或发布放行。

## 真实测试前置证据

- 治理测试：`python -X utf8 -B -m unittest discover -s test/test-asset-governance -p "*_test.py" -v`，13 项通过。
- 根测试：`python -X utf8 -B test/run_python_tests.py`，216 项通过。
- Skill 校验：六个相关 Skill 的 `quick_validate.py` 均通过；字典生成器已完成。

## 6-review 结论

- STYLE: PASS

## 检查清单

| 检查项 | 结果 | 证据 |
| --- | --- | --- |
| UTF-8、Markdown 结构、尾随空白 | PASS | `git diff --check` |
| 命名、路径镜像和测试资产归位 | PASS | `test_mock_stub_and_fake_mirror_source_path`、`test_simulation_outside_source_mirror_is_rejected` |
| 根 `test/` 与 `doc/5-tests/` 双根边界 | PASS | `test_active_rules_keep_test_code_and_evidence_separate`、`test_mock_policy_is_explicit_and_interface_rule_has_no_old_conflict` |
| Skill 结构与索引一致 | PASS | 六个 `quick_validate.py`、字典生成器 |

## 问题与修复

N/A + 原因 + 证据：本轮没有未修复的 `STYLE: FIX_REQUIRED` 项；扫描到的 `doc/5-tests/` 反例仅作为禁止示例保留，未改变规则语义。

图片资产决策：N/A + 原因 + 证据：本风格回归只检查文本、路径和测试资产，不需要图片资产。

## 执行附录

所有命令只读取本地工作树或临时目录；未连接数据库、缓存、消息队列、HTTP/RPC 上游；未迁移或改写历史 `doc/5-tests/` 可执行资产；未执行 Git 历史写入。

## 追踪附录

`TASK-TEST-MOCK-MIRROR-01` -> `test/shared/layout_policy.py` / `test/test-asset-governance/asset_location_test.py` -> `TEST-TEST-MOCK-MIRROR-001` -> `STYLE: PASS`。
