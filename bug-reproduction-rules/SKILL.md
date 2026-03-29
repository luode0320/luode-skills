---
name: bug-reproduction-rules
description: 当问题需要构造步骤、确定触发条件、判断是否稳定发生、确认出现频率或复现环境时触发。负责输出复现路径、稳定性判断、符合 `artifact-storage-rules` 约定的 Bug 根目录记录和无法复现时的结论处理；不要用它代替根因分析。
---

# Bug 复现规则

只在需要回答“这个问题怎么复现、是否稳定、在哪些条件下出现”时使用这个 skill。
如果当前基础入口信息还不足，请先转 `bug-gap-rules` 或 `bug-intake-rules`；如果已经进入代码和运行时定位，请转交相邻定位 skill。

## Skill 作用与适用场景

- 构造最小复现路径和触发步骤。
- 判断问题是稳定复现、条件复现还是偶发现象。
- 明确复现环境、输入数据、账号和前置状态。
- 将复现结论统一沉淀到当前 Bug 根目录，并与测试目录建立关联。
- 为后续范围界定、根因定位和验证闭环提供统一样本。

## 自动触发信号

- 需要回答“怎么操作才能触发这个问题”。
- 团队对问题是否稳定发生、在哪些条件下发生存在分歧。
- 需要把线上现象转成测试环境或本地环境可执行步骤。
- 定位前必须先确认复现条件和频率。

## 进入后先做什么

1. 先确认复现目标是重现现象、重现日志还是重现状态变化。
2. 为当前 Bug 确认统一的根目录，继续沿用 `artifact-storage-rules` 约定的当前 Bug 根目录。
3. 梳理环境、账号、数据、输入和前置操作。
4. 尝试收敛出最小步骤，而不是堆一长串无关动作。
5. 记录复现结果、稳定性和失败时的差异。

## 默认执行流程

1. 默认先读 `references/reproduction-template.md`，先按统一格式记录复现步骤。
2. 如需继续展开，再读 `references/stability-checks.md`，需要判断问题是稳定复现还是条件复现。
3. 需要对照边界或正反例时，再读 `references/reproduction-examples.md`，需要对照复现结论样例。
4. 输出 复现步骤、复现条件、稳定性判断和未复现说明。
5. 复现成功后转 `bug-root-cause-rules` 或 `bug-runtime-debug-rules`；若稳定性不足但怀疑时序问题，可继续转运行时诊断路径。

## 权责边界与不负责事项

- 只负责复现路径，不替代 `bug-root-cause-rules` 做原因分析。
- 不负责长期测试计划或回归策略，那属于测试域。
- 不把“偶发但暂未复现”直接当成问题不存在。
- 不为了复现而大范围改环境或改代码而不留痕。
- 实际复现脚本、模拟数据和验证程序仍应按 `artifact-storage-rules` 与 `test-location-rules` 约定放在统一测试目录；本 skill 只统一 Bug 结论记录落点。

## 需要暂停并确认的条件

- 基础输入、环境或账号条件仍缺失。
- 尝试多次后复现结果高度不稳定，且差异无法解释。
- 复现需要高风险环境操作，但还没有确认。
- 当前现象与原始问题描述已经明显不一致。

## 执行通过 / 驳回标准

- 通过：能够给出清晰的复现步骤、前置条件、环境和稳定性结论，或明确说明为什么当前无法稳定复现。
- 驳回：复现步骤含糊、无法重复，或没有记录成功 / 失败条件差异。

## 执行结果归档要求

- 将复现步骤、环境、输入数据和结论统一记录到 `artifact-storage-rules` 约定的当前 Bug 根目录中。
- 当前 Bug 根目录必须包含 `README.md`，至少写明前置条件、操作步骤、结果表现和稳定性判断。
- 如果本轮复现使用了脚本、模拟数据或验证程序，应按 `artifact-storage-rules` 与 `test-location-rules` 放入对应测试任务目录，并在当前 Bug 根目录中记录对应测试目录路径。
- 如果暂未复现，应记录已尝试路径和缺失条件，避免重复试错。

## references 读取规则

- 默认先读 `references/reproduction-template.md`。
- 在决定当前 Bug 根目录、测试目录映射和复用策略时，先读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在 判断稳定性和触发条件 时，再读 `references/stability-checks.md`。
- 只有在 对照复现正反例或处理未复现结论 时，再读 `references/reproduction-examples.md`。
