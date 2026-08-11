---
name: project-interface-release-execution-rules
description: 当需要做上线前项目级全接口测试、消费者视角的 HTTP/SSE/原生 WebSocket/Socket.IO 外部整体性测试、替代人工接口回归验证或生成发布门禁结论时触发。负责在接口基线就绪后执行接口与 verified 消费者场景、确定性断言、受控 local 探针、清理、双轨对账和硬切门禁；是统一执行内核 `scripts/release_test_engine/` 的唯一行为 owner。可执行测试脚本、mock、stub、fake、fixture、helper 和数据构造统一归入根 `test/`，源码关联资产按被测源码路径镜像；`doc/5-tests/` 仅保存扁平中文主报告 md，机器产物落在 `test/release-artifacts/YYYY-MM-DD_HHmmss_release-interface-test/`，禁止用候选场景、fixture 结果或非 local 配置伪造通过。
---

# 项目上线接口测试执行与放行规则

只在“接口基线已就绪，需要执行接口级或消费者场景级真实测试，并输出上线放行结论”时使用这个 skill。
如果接口基线尚未扫描或需要刷新，先转交 `project-interface-baseline-rules`；如果是任务级功能验证或改动影响面回归，分别转交 `functional-validation-rules`、`test-regression-rules`；如果是测试文档组织或目录结构，转交 `test-strategy-rules 的 test-asset-governance 条件路由`。

本 skill 与 `project-interface-baseline-rules` 是同源拆分：对方负责接口、事件、消费者和来源事实，本 skill 负责测试怎么跑、结果是否正确、清理是否完成以及能否上线。统一执行内核 `scripts/release_test_engine/`、隔离依赖清单 `scripts/requirements.in` / `requirements.lock` 和兼容入口 `scripts/generate_release_test_plan.py` 都由本 skill 独占行为；基线 owner 只维护事实资产，不持有执行或门禁代码。

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
- 输出标准化的测试报告，明确给出是否允许上线的结论，作为 `delivery-summary-rules` 的输入之一。
- 测试代码与可执行测试资产必须遵循测试域双根规则：可执行测试脚本、mock、stub、fake、fixture、helper 和数据构造统一落在根 `test/`；源码关联资产按被测源码目录镜像，跨源码复用资产才进入 `test/shared/`。`doc/5-tests/` 只保留一份扁平中文主报告 md，结论与摘要内联在正文；响应样本、报告、日志、对账结果等会被后续命令回读的机器产物落在 `test/release-artifacts/YYYY-MM-DD_HHmmss_release-interface-test/`。
## 自动触发信号
- 上线前需要做全项目接口回归验证。
- 需要替代人工做接口测试和响应判断。
- 需要输出上线接口测试准入结论。
- 项目迭代后需要验证所有核心接口是否正常。
- 用户明确要求做“项目级接口测试”“上线前全接口测试”“接口测试门禁”。
- 需要从前端、SDK 或其它系统消费者视角验证 HTTP/SSE/WebSocket/Socket.IO 跨接口、跨步骤或跨协议结果一致性。
- 需要运行 `external-doctor/generate/validate/verify/run/migrate`，或比较 `legacy/shadow/scenario` 发布门禁。

## 条件路由：shared-evidence-and-specialized-contracts

本路由统一承接参数来源与复用、脚本工具箱、接口执行、响应判定、报告、门禁和归档契约；项目接口基线仍由 `project-interface-baseline-rules` 单独负责。

命中后先读取 [shared-evidence-and-specialized-contracts](references/shared-evidence-and-specialized-contracts.md)，该文件承接本 owner 的阶段流程、边界、暂停条件、通过标准和归档契约；本入口只负责自动触发、主路由和职责裁决。

## 条件路由：external-consumer-scenario-release-gate

当目标不是逐接口烟测，而是验证前端、SDK 或其它系统通过公开 HTTP/SSE/原生 WebSocket/Socket.IO 能否取得正确且相互一致的数据时，进入本路由。候选场景只能由事实资产生成并经过确定性验证后晋级 verified；真实运行必须使用 local 配置、隔离工具环境、声明式动作、外部结果优先 oracle 和失败后清理。P0/P1 目录全集任一 FAIL/BLOCKED/PENDING、来源漂移、覆盖缺口或清理失败都禁止自动放行。

命中后依次读取 [场景契约](references/external-scenario-contract.md)、[真实执行与双轨门禁](references/external-scenario-execution-gate.md) 和 [兼容迁移与工具环境](references/external-scenario-migration.md)。接口与消费者事实仍由 `project-interface-baseline-rules` 维护；本路由不新增第二执行 owner，不扩展 gRPC、MQ、性能、压力、安全扫描或浏览器 UI。

## references 读取规则
- 筛选测试范围时读 `references/test-selection-policy.md`。
- 判定接口响应时读 `references/agent-response-judgement.md`。
- 输出报告时读 `references/report-format.md`。
- 输出门禁结论时读 `references/execution-gate.md`。
- 确认和现有测试 skill 集成关系时读 `references/existing-test-skill-integration.md`。
- 明确应产出的测试资产时读 `references/output-artifacts.md`。
- 构造测试请求参数时读 `references/test-data-construction-rules.md`。
- 调用或新增测试工具脚本前读 `references/reusable-script-toolbox.md`。
- 构造或验证 `external-scenario/1.0` 场景时读 `references/external-scenario-contract.md`。
- 执行 HTTP/SSE/WebSocket/Socket.IO、生成场景报告或计算 shadow/scenario 门禁时读 `references/external-scenario-execution-gate.md`。
- 使用旧 CLI/旧结果迁移、隔离虚拟环境或 doctor 时读 `references/external-scenario-migration.md`。
