---
name: frontend-component-rules
description: 当新增或修改 React、Vue、前端组件拆分、组件目录归属、props 设计、emits 设计、slots 设计、状态归属、事件上抛、组合方式、hooks、composables、复用边界、受控/非受控切换、渲染副作用或客户端展示逻辑时自动触发。负责组件边界、状态边界、接口契约、组合复用和渲染可维护性；若任务同时涉及前端 UI/组件/样式调整、体验改进或界面 Bug 修复，优先让位给 `frontend-design`，本 skill 仅补充组件工程边界。
---

# 前端组件工程规则

只在判断“这个前端能力应该拆成什么组件、状态该放哪里、组件之间怎么传递和复用”时使用这个 skill。
如果当前任务包含前端 UI、组件、样式的调整/改进或界面 Bug 修复，请优先交给 `frontend-design`；`frontend-ui-visual-rules` 作为视觉约束补充。

## Skill 作用与适用场景

- 约束组件拆分粒度，防止页面逻辑、状态和渲染细节堆成一个大组件。
- 明确 props、emits、slots、children、回调和数据流的边界。
- 判断状态应留在局部、上提到父层，还是进入全局状态。
- 统一 hooks、composables、容器组件、展示组件和复用代码的职责边界。
- 减少组件耦合、重复渲染、隐式副作用和跨层穿透。
- 当前端组件文件发生代码新增或修改时，必须联动注释双 skill、格式清理和语法检查；不得只完成组件工程判断就直接收口。

## 自动触发信号

- 新增或修改 `.tsx`、`.jsx`、`.vue` 中的组件定义、组件拆分或组件合并。
- 新增或修改 props、emits、slots、children、render props、上下文透传。
- 新增或修改 hooks、composables、本地 state、store、受控/非受控表单逻辑。
- 新增或修改列表项组件、弹窗组件、表单组件、容器组件、页面内复用组件。
- 用户明确要求“组件拆干净”“状态别乱飞”“这个组件太大了”“复用边界不清”。

## 进入后先做什么

1. 先判断当前问题是视觉问题还是组件工程问题，不要混用两个 skill。
2. 明确当前组件的职责：展示、容器、流程编排、状态桥接，还是纯复用包装。
3. 先收口状态归属，再设计 props、事件和组合方式。
4. 判断当前抽象是否真的复用，避免过早抽象和层层包装。
5. 检查渲染副作用、请求、副作用清理和依赖变化是否稳定。

## 默认执行流程

1. 默认先读 `references/component-boundary-rules.md`，先判断应拆到什么粒度。
2. 如果当前任务涉及本地 state、父子状态、共享状态或表单状态，再读 `references/state-ownership-rules.md`。
3. 如果当前任务涉及 props、events、slots、children、回调设计，再读 `references/props-events-contract-rules.md`。
4. 如果当前任务涉及组合复用、包装组件、hooks、composables 或公共组件抽象，再读 `references/composition-reuse-rules.md`。
5. 如果当前任务涉及渲染副作用、请求时机、watch / effect / lifecycle、副作用清理，再读 `references/render-side-effect-rules.md`。
6. 完成前默认再读 `references/component-review-checklist.md` 做一轮组件工程自审。
7. 若本轮修改 `.vue`、`.tsx`、`.jsx`、`.ts`、`.js` 前端组件代码，完成前必须确认 `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`cleanup-format-review-rules`、`syntax-check-review-rules` 已执行；任一缺失不得给“已完成”结论。

## 权责边界与不负责事项

- 只负责组件工程边界、数据流边界和渲染可维护性，不负责页面视觉风格。
- 不代替 `frontend-design` 处理前端 UI、组件、样式的调整、改进和界面 Bug 修复主路线。
- 不代替 `frontend-ui-visual-rules` 决定页面气质、配色、排版和视觉层级。
- 不代替接口规则、数据库规则或后端状态模型设计。
- 不因为“未来可能复用”就提前把组件抽成公共层。
- 不把页面业务流程硬塞进通用组件，导致组件表面通用、实际强业务耦合。

## 需要暂停并确认的条件

- 当前组件既承担页面流程编排，又承担大量展示细节，拆分方向还不清。
- 状态既像局部状态，又被多个页面或多个链路共享，暂时无法裁定归属。
- props 越传越多、事件越抛越深，已经出现明显的透传链。
- 当前抽象依赖具体业务上下文，却计划抽成通用组件或通用 hook。

## 执行通过 / 驳回标准

- 通过：能明确组件职责、拆分边界、状态归属、props / events 契约和复用边界，并让渲染逻辑和副作用保持可理解、可维护。
- 驳回：只是把大组件机械切块，或让 props / emits / 状态透传更混乱，或为了复用把强业务逻辑伪装成通用组件。

## 执行结果归档要求

- 如果本次形成了稳定的组件边界、状态归属规则、hooks / composables 约束或目录放置约束，应记录到项目现有前端工程说明、组件规范文档或对应需求文档中。
- 如果项目已有组件规范或前端架构说明，优先更新原文档，不重复新建平行说明。
- 归档内容至少包含组件职责、状态归属、props / events 边界、复用边界和副作用约束。

## references 读取规则

- 默认先读 `references/component-boundary-rules.md`。
- 只有在处理状态归属时，再读 `references/state-ownership-rules.md`。
- 只有在处理 props、events、slots 或 children 契约时，再读 `references/props-events-contract-rules.md`。
- 只有在处理组合复用、公共抽象和 hooks / composables 时，再读 `references/composition-reuse-rules.md`。
- 只有在处理副作用、生命周期和渲染稳定性时，再读 `references/render-side-effect-rules.md`。
- 完成前默认读 `references/component-review-checklist.md`。
