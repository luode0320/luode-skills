---
name: team-development-rules
description: 当任务阶段不明确、领域边界不清、多个 skill 同时触发、流程需要暂停/重启/继续/终止，或需要先判断应该进入历史回忆、需求、Bug、编码、测试还是交付处理时触发。负责阶段分析、路由分流、冲突裁决和流程阻断；不要在单一明确的 SQL、API、配置、测试、评审等任务中触发。
---

# 团队研发总控规则

仅在研发流程需要协调时使用这个 skill。
如果当前任务已经是明确的小型单域任务，立即让位给对应的小 skill，不要抢执行权。

## Skill 作用与适用场景

- 先判断当前处于需求、Bug、编码、编码审查、测试还是交付阶段。
- 如果用户先问历史记录、历史方案或项目历程，先判断是否应进入记忆域。
- 再判断应该交给哪个域或哪个小 skill 接手。
- 在多个 skill 同时命中时做去重、裁决和让路。
- 在前置条件未满足时阻断流程，防止跳阶段推进。
- 进入编码阶段时，默认提醒联动 `comment-placement-granularity-rules` 与 `comment-completion-gate-rules`，避免改动位点注释漏触发。
- 前端样式排版异常（如对不齐、歪斜、间距错乱）默认先命中 `web-design-guidelines` 做审查，再由 `frontend-design` 实施修复。
- 用户提交图片/截图时，默认先命中 `image-redbox-focus-rules`，优先聚焦红框标注区域再进入对应主域 skill。
- Go 场景命中外部 skill 时，默认以本仓库内置自适应规则为主，外部 skill 仅作补充约束，不得覆盖内置强制规则。

## 自动触发信号

- 新任务刚进入，但阶段不明确。
- 用户问题可能是“历史回忆 / 项目历程”，但还不清楚该进入哪个记忆类 skill。
- 描述同时像需求又像 Bug，或同时跨多个阶段。
- 多个 skill 同时命中，可能重复、冲突或顺序错位。
- 需要决定流程是暂停、重启、继续还是终止。
- 用户明确要求按团队完整研发流程处理。

## 进入后先做什么

1. 先判断当前阶段。
2. 如果问题明显是在查历史，优先判断是否应进入记忆域。
3. 再判断这是需求类、Bug 类还是交付收口类问题。
4. 若任务包含图片/截图输入，先路由到 `image-redbox-focus-rules` 抽取红框重点，再路由到对应主域 skill。
5. 若任务属于前端样式排版异常（如对不齐、歪斜、间距错乱），优先路由到 `web-design-guidelines` 做审查，输出问题清单后再路由到 `frontend-design` 修复。
6. 若任务属于前端 UI、组件、样式的调整/改进或界面 Bug 修复（且非上述排版审查类），优先路由到 `frontend-design`，再按需叠加 `frontend-component-rules` 或 `frontend-ui-visual-rules`。
7. 若任务属于 Go，先叠加本仓库内置 Go 相关规则（如 `package-structure-rules`、`api-endpoint-rules`、`api-request-rules`、`api-response-rules`、`database-query-rules`、`database-schema-rules`），再按需叠加外部 skill（如 `golang-patterns`）。
8. 如果已经进入写代码阶段，默认叠加 `code-minimal-change-rules`、`code-readability-rules`、`code-style-consistency-rules`、`comment-placement-granularity-rules` 与 `comment-completion-gate-rules`，再判断代码位点 skill。
9. 最后判断当前流程是否应该被阻断，或是否允许进入下一阶段。

## 默认执行流程

1. 读取 `references/routing-rules.md`，判断当前任务应进入哪个域或 skill。
2. 如果存在阶段跳跃风险，读取 `references/stage-blockers.md` 判断是否阻断。
3. 如果存在多 skill 并行命中或冲突，读取 `references/conflict-examples.md` 做裁决。
4. 输出当前阶段、建议接手 skill、是否阻断、阻断原因和下一步动作。
5. 在结论明确后退出，不继续代替目标 skill 执行细则。

## 权责边界与不负责事项

- 只负责阶段分析、路由分流、冲突裁决和流程阻断。
- 不代替数据库、接口、配置、日志、错误处理、测试、交付等小 skill 执行细则。
- 不因为任务涉及“全流程”就默认长期驻留在上下文中。
- 对明确的小 skill 场景，只做一次分流或直接让路，不做主执行。

## 需要暂停并确认的条件

- 需求和 Bug 无法判定，且两条路径会导向不同处理流程。
- 当前任务同时跨两个阶段，但前一阶段的前置条件未满足。
- 多个 skill 的规则明显冲突，且不能按既定优先级裁决。
- 用户要求跳过关键环节，例如跳过需求澄清、Bug 定位、编码审查或测试。

## 执行通过 / 驳回标准

- 通过：能够明确给出当前阶段、所属域、建议命中的 skill、是否阻断下一阶段，以及阻断原因。
- 驳回：仍然无法说明任务归属，或把已经明确的小 skill 场景错误拦回总控层，或允许任务跳过关键前置阶段。

## 执行结果归档要求

- 出现冲突裁决、阶段阻断、流程重启、流程终止时，将结论归档到 `analysis/` 或 `review/`。
- 归档内容至少包含任务背景、当前阶段、裁决或阻断原因、下一步建议和涉及的 skill。
- 如果只是普通分流且没有冲突或阻断，可以不单独归档。

## references 读取规则

- 默认先读 `references/routing-rules.md`。
- 只有在判断是否允许进入下一阶段时，再读 `references/stage-blockers.md`。
- 只有在多个 skill 冲突、重复命中或顺序错位时，再读 `references/conflict-examples.md`。
