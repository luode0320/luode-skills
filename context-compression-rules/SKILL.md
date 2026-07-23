---
name: context-compression-rules
description: 当当前会话已发生“压缩上下文 / 自动压缩上下文 / 上下文太多”后的压缩重组，或继续执行前刚得到压缩摘要时自动触发。负责按共享 context-recovery-contract 重新读取当前平台规则文件与项目当前上下文，恢复目标、阶段、约束、必命中 skill 和“是否允许开始/继续实现代码”的许可状态；只有确认缺少继续任务所需的近期项目事实时，才条件联动 recent-context-bootstrap-rules 补载近 3 天上下文与 skill 索引。不要把它代替 history-recall-rules 的深度历史回忆、project-timeline-rules 的长期时间线分析或当前主域执行。
---

# 上下文压缩规则

只在上下文压缩已经发生后使用这个 skill；尚未压缩时不得提前触发。

## Skill 作用与适用场景

- 按共享恢复契约重建继续当前任务所需的最小上下文。
- 强制重新读取当前平台规则文件和项目当前上下文，恢复仓库级硬规则与主线状态。
- 判断近期事实是 `sufficient`、`missing` 还是 `uncertain`；不得把“发生压缩”直接等同于“必须预热最近 3 天”。
- 只有确认状态为 `missing` 时，才条件联动 `recent-context-bootstrap-rules`。
- 恢复编码许可状态 `confirmed` / `not-confirmed` / `unknown`；未确认默认 `unknown`，不得直接编码。
- 输出可立即交还主域的最小上下文包，不代替主域执行。

## 自动触发信号

- 刚完成“压缩上下文 / 自动压缩上下文 / 上下文太多”后的摘要重组。
- 系统自动压缩后准备继续执行当前任务。
- 用户明确表示“已经压缩完了，继续”或“按压缩结果继续执行”。
- 压缩后存在规则、Skill、范围、许可或下一执行点丢失风险。

## 进入后先做什么

1. 确认压缩已经完成；未完成则不触发。
2. 读取 `references/context-recovery-contract.md`，按固定顺序恢复规则、项目状态、目标、范围、验证和许可。
3. 重新读取当前平台规则文件；项目存在 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md` 时按契约读取，不把 `PROJECT_HISTORY.md` 当作默认来源。
4. `PROJECT_CURRENT.md` 存在任务投影托管区时，先调用 `task-plan-rehydration-rules` 校验有效活动投影并真实调用 `update_plan` 重建悬浮任务列表；失活、损坏、过期、工具不可用分别记录状态，不伪报恢复。
5. 评估近期事实状态：只有明确缺少继续任务所需的最近改动、证据或执行点时才标记 `missing`。
6. 状态为 `missing` 时条件联动 `recent-context-bootstrap-rules`；`sufficient` 时直接继续，`uncertain` 时先核验现有来源，不得无条件预热。
7. 输出最小上下文包并交还当前主域。

## 默认执行流程

1. 读 `references/trigger-signals.md` 确认压缩后触发。
2. 读 `references/context-recovery-contract.md` 执行共享恢复顺序和近期事实判定。
3. 读 `references/compression-playbook.md` 生成保留、折叠和剔除结果。
4. 读 `references/boundary-rules.md` 确认与近期预热、历史回忆和主域的边界。
5. 读取当前状态后按 `task-plan-rehydration-rules` 输出 `task_projection` 恢复状态；进行中步骤只恢复 UI，不直接继续未知写操作。
6. 仅当 `recent_context_state=missing` 时调用 `recent-context-bootstrap-rules`；否则记录未调用原因。
7. 输出当前目标、已确认事实、约束、关键路径、待确认项、下一动作、编码许可、规则重载状态、任务投影和近期事实路由状态。
8. 立即退出并交还主执行权。

## 权责边界与不负责事项

- 不代替需求、Bug、编码、测试、审查、验收或交付。
- 不代替 `history-recall-rules` 的明确历史回溯，也不输出长期时间线。
- 不把压缩摘要、旧记忆或近期材料伪装成当前已确认事实。
- 不因压缩而删除仍影响决策的用户习惯、安全、授权、停止、回滚和范围边界。
- 不得在规则未恢复或编码许可不是 `confirmed` 时继续编码。
- 用户明确停止、终止或不要继续时，恢复动作只允许形成最小收口，不得重启原任务。

## 需要暂停并确认的条件

- 当前平台规则文件缺失、损坏或无法读取。
- 现有摘要、项目状态与当前工作区事实冲突，无法确定有效来源。
- 编码许可为 `not-confirmed` 或 `unknown`，但下一步要求修改代码。
- 近期事实状态持续为 `uncertain`，且继续会引入错误决策。
- 用户明确停止、终止或撤销继续执行授权。

## 执行通过 / 驳回标准

- 通过：规则与项目状态已恢复，近期事实完成三态判定，只有 `missing` 才调用近期预热，编码许可和下一动作明确。
- 驳回：压缩后无条件调用 `recent-context-bootstrap-rules`、跳过规则重载、把不确定内容写成事实，或未确认许可就继续编码。

## 执行结果归档要求

- 默认不新建持久化文档；恢复结果进入当前会话上下文。
- 若主域要求更新当前任务状态，由对应项目记忆或文档 Owner 执行，本 skill 不越权写入。
- 最小证据包括规则重载状态、项目状态来源、近期事实三态、是否调用近期预热及原因、编码许可和下一执行点。

## references 读取规则

- 触发判断：`references/trigger-signals.md`
- 共享恢复契约：`references/context-recovery-contract.md`
- 压缩模板：`references/compression-playbook.md`
- 边界与让路：`references/boundary-rules.md`
