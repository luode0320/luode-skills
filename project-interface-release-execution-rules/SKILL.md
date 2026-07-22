---
name: project-interface-release-execution-rules
description: 当需要做上线前项目级全接口测试、替代人工接口回归验证、生成上线接口测试门禁结论时触发。负责在接口基线（由 `project-interface-baseline-rules` 维护）就绪后，筛选本次必测接口范围、按依赖图构造请求参数并执行接口验证、由 agent 判定接口级结果、输出标准化报告与上线放行结论；是统一执行内核 `scripts/release_test_engine/` 的唯一行为 owner，所有测试资产强制落地到 `doc/5-tests/` 对应时间戳根目录，请求参数和简要响应必须是 JSON 字符串，禁止接口明细输出为 Markdown 表格。
---

# 项目上线接口测试执行与放行规则

只在“接口基线已就绪、需要执行测试、判定接口响应、输出上线放行结论”时使用这个 skill。
如果接口基线尚未扫描或需要刷新，先转交 `project-interface-baseline-rules`；如果是任务级功能验证或改动影响面回归，分别转交 `functional-validation-rules`、`test-regression-rules`；如果是测试文档组织或目录结构，转交 `test-strategy-rules 的 test-asset-governance 条件路由`、`test-strategy-rules 的 test-asset-governance 条件路由`。

本 skill 与 `project-interface-baseline-rules` 是同源拆分：对方负责“接口事实是什么”，本 skill 负责“测试怎么跑、结果是否通过、能不能上线”。统一执行内核 `scripts/release_test_engine/`（含 `runner.py`、`report.py`、`gate.py`、`judge.py`、`resolver.py`、`safety.py`、`auth.py`、`events.py`、`cli.py`、`model.py`、`storage.py`、`discovery.py`、`schema_registry.py`、`topology.py`、`graph.py`、`migrate_baseline.py`、`parameter_store.py`、`dependency_diagnostics.py` 及 9 个 `adapters/*` 协议适配器）和兼容入口 `scripts/generate_release_test_plan.py` 已物理迁移至 `project-interface-release-execution-rules/scripts/`，本 skill 是其唯一行为 owner 并负责运行时回写基线资产文件；`project-interface-baseline-rules` 只读取回写结果，不持有该内核代码。

## 测试隔离红线（强制，和现有测试域规则一致）
- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 接口测试必须基于真实业务实现和测试资产完成，禁止通过向生产代码注入测试专用能力来“制造通过”结果。
- 一旦发现生产代码测试污染，测试结论直接无效并阻断，先回退污染改动再重测。
- 当前仓库上线前接口测试也属于**本地自动化测试**：只能使用 `local` 环境信息执行，不得改动 `test` 配置文件，不得连接 `test` / `prod` / `staging` 环境数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务。
## Skill 作用与适用场景
- 作为上线前的项目级接口质量门禁，统一规划全项目接口测试范围、选择必测接口、执行验证、输出可决策的结论。
- 依赖 `project-interface-baseline-rules` 提供的最新接口基线和依赖图，不重复做基线扫描。
- 优先复用 `project-interface-release-execution-rules/scripts/` 的通用脚本工具箱；已有能力能覆盖时不得每轮重复生成同类脚本。
- 自动由 agent 判定接口响应是否符合预期，替代人工逐一查看响应结果。
- 输出标准化的测试报告，明确给出是否允许上线的结论，作为 `final-acceptance-rules` 的输入之一。
- 强制所有测试资产落地到 `doc/5-tests/` 下的时间戳根目录，遵循现有测试域的归档规则。
## 自动触发信号
- 上线前需要做全项目接口回归验证。
- 需要替代人工做接口测试和响应判断。
- 需要输出上线接口测试准入结论。
- 项目迭代后需要验证所有核心接口是否正常。
- 用户明确要求做“项目级接口测试”“上线前全接口测试”“接口测试门禁”。

## 条件路由：shared-evidence-and-specialized-contracts

本路由统一承接参数来源与复用、脚本工具箱、接口执行、响应判定、报告、门禁和归档契约；项目接口基线仍由 `project-interface-baseline-rules` 单独负责。

命中后先读取 [shared-evidence-and-specialized-contracts](references/shared-evidence-and-specialized-contracts.md)，该文件承接本 owner 的阶段流程、边界、暂停条件、通过标准和归档契约；本入口只负责自动触发、主路由和职责裁决。

## references 读取规则
- 筛选测试范围时读 `references/test-selection-policy.md`。
- 判定接口响应时读 `references/agent-response-judgement.md`。
- 输出报告时读 `references/report-format.md`。
- 输出门禁结论时读 `references/execution-gate.md`。
- 确认和现有测试 skill 集成关系时读 `references/existing-test-skill-integration.md`。
- 明确应产出的测试资产时读 `references/output-artifacts.md`。
- 构造测试请求参数时读 `references/test-data-construction-rules.md`。
- 调用或新增测试工具脚本前读 `references/reusable-script-toolbox.md`。
