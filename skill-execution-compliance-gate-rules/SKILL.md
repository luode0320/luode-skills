---
name: skill-execution-compliance-gate-rules
description: 只要本轮任务已命中其他 skill 且可能存在“只做了部分规则”的风险、多 skill 边界冲突、非预期工具/命令/API/模型/浏览器/安装执行失败需要联动 `execution-failure-learning-rules`、任一工具调用后最终回复需要给出可核验的 Skill 执行证据、或当前运行环境存在 goal/plan/task 等显式状态收口机制需要确认真实收口，最终回复前必须命中本 skill。负责检查已命中 skill 的执行完整性、`blocked/manual_handoff` 共享阻断契约的校验与唯一渲染边界、Skill 执行证据与运行时状态真收口。若存在原执行计划内未完成必需项或阻断级规则缺口，禁止给“已完成”结论；真实 `blocked/manual_handoff` 时只校验共享阻断契约与唯一渲染条件，不生成面向用户的阻断区块或解决计划。除此之外默认直接结束，不额外制造任何下一步区块、下一步建议、等待指令文案或“无需继续动作”占位。
---


# Skill 执行完整性闸门规则

只在“skill 已触发但执行闭环可能不完整”时使用这个 skill。
目标不是重复实现业务，而是在收口前确认所有已命中 skill 的当前阶段规则已经真实执行。

本 skill 与 `code-change-finalization-gate-rules` 保持独立：前者负责通用 Skill 执行完整性、失败学习联动、执行证据和运行时状态真收口；后者只负责代码/测试改动的专项最终闸门。

## Skill 作用与适用场景

- 对本轮实际命中的 skill 做末端合规检查，识别“已执行 / 可执行但未执行 / 当前阶段不适用”。
- 校验计划内必需项、真实阻断事实、工具执行证据和 goal/plan/task 等显式运行时状态是否真实收口。
- 真实 `blocked/manual_handoff` 时只校验共享阻断契约与唯一渲染条件，不生成用户可见阻断区块或解决计划。
- 最终总结、条件区块和后续内容全部交给 `reasoning-summary-structure-rules`；本 skill 只产出 PASS/FAIL、缺失项和结构化事实。

## 自动触发信号

- 已命中其他 skill 且存在只执行部分规则、多 skill 边界冲突或收口遗漏风险。
- 用户要求检查 Skill 是否完整执行。
- 本轮发生非预期工具、命令、API、模型、浏览器、安装器或生成器失败，或成功退出但产物不可信。
- 本轮发生工具调用，最终回复需要可核验的 Skill 执行证据。
- 当前运行环境存在显式状态收口机制，需要确认状态已经真实完成。

## 进入后先做什么

1. 列出本轮实际命中的 skill，不臆造未命中项。
2. 读取 `references/applicability-and-gap-check.md`，只核验当前阶段可执行规则。
3. 分类计划内必需缺口、真实阻断候选和不适用项；`limited/not_applicable` 不得升级为阻断。
4. 出现非预期执行失败时，核验 `execution-failure-learning-rules` 的分类、恢复、同输入复验和状态处理证据。
5. 核验本轮工具调用的 Skill 执行证据，以及 goal/plan/task 等显式状态的真实收口动作。
6. 输出 PASS/FAIL 与缺失事实；用户可见结构统一交给 `reasoning-summary-structure-rules`。

## 默认执行流程

1. 收集本轮编辑、命令、测试、日志、产物和运行时状态证据。
2. 逐 Skill 核对当前阶段规则，记录执行状态和证据定位。
3. 对非预期执行失败核验失败学习链；对代码/测试改动只检查是否已交给 `code-change-finalization-gate-rules`，不重复执行专项闸门。
4. 校验共享阻断事实的状态、阶段、依据、已尝试与停止条件、影响、恢复入口和去重关系。
5. 形成唯一合规结论：PASS，或 FAIL + 缺失字段/未完成动作。
6. 最终渲染前读取 `../reasoning-summary-structure-rules/references/conditional-sections-rules.md`；本 skill 不自行定义或输出后续内容、阻断区块和等待类文案。

## 阻断判定与处理

属于阻断级：

- 缺口会直接导致实现错误、测试结论失真、归档位置错误或当前阶段无法正确推进。
- 工具调用后的 Skill 执行证据缺失，且自动补救后仍不可核验。
- 显式运行时状态应收口但未执行真实状态动作。
- `blocked/manual_handoff` 的共享契约缺少必填事实或存在重复冲突记录。

属于非阻断级：

- 缺口不影响当前结论正确性，且不属于原执行计划当前阶段必需项。
- 非阻断缺口只作为结构化事实交给最终总结 owner；是否展示由其条件规则决定。

## 权责边界与不负责事项

- 只负责通用 Skill 执行完整性、失败联动、执行证据和运行时状态收口，不代替业务实现。
- 不重复代码专项的注释、测试目录、实现自审、真实运行验证、router 或用户手改保护检查。
- 不把历史遗留规则或当前阶段不适用项误报为未执行缺口。
- 不拥有最终输出模板、后续内容或任务阻断渲染权。

## 执行通过 / 驳回标准

- 通过：当前阶段所有已命中 Skill 均有执行状态和证据；失败学习、共享阻断契约、Skill 执行证据和运行时状态均按适用性完成核验。
- 驳回：存在可执行但未执行的必需规则、无法核验的工具结果、未真实收口的运行时状态，或共享阻断事实不完整/不唯一，却仍给出完成结论。
- 驳回：本 skill 自行渲染用户可见后续内容、阻断区块、解决计划或等待类占位文案。

## references 读取规则

- 默认先读 `references/applicability-and-gap-check.md`。
- 判断最终条件区块时只读 `../reasoning-summary-structure-rules/references/conditional-sections-rules.md`，不得维护第二份规则。

## 回到主流程的重启点

- FAIL 时先回到缺失规则的唯一 owner 或真实状态入口补齐，再重新执行本闸门。
- 无法在停止边界内补齐时，只提交结构化阻断事实给最终总结 owner。

## 输出要求（简化版）

- 只输出 `Skill 合规:PASS/FAIL`、缺失项和可核验执行证据。
- 最终总结结构、后续内容、阻断区块与无后续收口规则统一读取 `reasoning-summary-structure-rules`，本 skill 不复制。
