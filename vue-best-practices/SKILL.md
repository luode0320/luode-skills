---
name: vue-best-practices
description: Vue.js 任务必须命中本 skill。默认推荐使用 Composition API + `<script setup>` + TypeScript。覆盖 Vue 3、SSR、Volar、vue-tsc。凡是 Vue、`.vue`、Vue Router、Pinia 或 Vite + Vue 相关工作都应加载。除非项目明确要求 Options API，否则始终优先 Composition API。
license: MIT
metadata:
  author: github.com/vuejs-ai
  version: "18.0.0"
---

# Vue 最佳实践工作流

把本 skill 当作执行指令集。除非用户明确要求调整顺序，否则按以下流程执行。

## 核心原则
- **状态可预测：** 保持单一事实来源，其余尽量派生。
- **数据流显式：** 大多数场景遵循 Props 向下、Events 向上。
- **组件小而专注：** 更易测试、复用与维护。
- **避免不必要重渲染：** 合理使用 `computed` 与 `watch`。
- **可读性优先：** 写清晰、可自解释的代码。

## 1) 编码前先确认架构（必做）

- 默认栈：Vue 3 + Composition API + `<script setup lang="ts">`。
- 若项目明确使用 Options API，若可用请加载 `vue-options-api-best-practices`。
- 若项目明确使用 JSX，若可用请加载 `vue-jsx-best-practices`。

### 1.1 必读核心资料（必做）

- 在执行任何 Vue 任务前，先阅读并应用以下核心资料：
  - `references/reactivity.md`
  - `references/sfc.md`
  - `references/component-data-flow.md`
  - `references/composables.md`
- 这些资料应在整个任务期间保持为活跃上下文，不是只在问题出现时才看。

### 1.2 编码前先规划组件边界（必做）

对任何非 trivial 功能，先给出简要组件图。

- 用一句话定义每个组件的单一职责。
- 入口/根组件和路由级视图组件默认仅作为组合层。
- 除非是刻意的小型单文件 demo，否则将功能 UI 与逻辑从入口/根/视图组件中拆出。
- 在组件图中定义每个子组件的 props / emits 合约。
- 新增超过一个组件时，优先使用 feature 目录结构（`components/<feature>/...`、`composables/use<Feature>.ts`）。

## 2) 应用 Vue 基础能力（必做）

这些是必须掌握并在每个 Vue 任务中落实的基础能力，请结合 `1.1` 中已加载资料执行。

### 响应式

- 必读资料： [reactivity](references/reactivity.md)
- 源状态保持最小化（`ref`/`reactive`），能派生的都用 `computed`。
- 副作用场景按需使用 watcher。
- 避免在模板中重复计算高开销逻辑。

### SFC 结构与模板安全

- 必读资料： [sfc](references/sfc.md)
- SFC 区块顺序固定为：`<script>` → `<template>` → `<style>`。
- SFC 职责保持聚焦；组件过大要拆分。
- 模板保持声明式；分支与派生逻辑放到 script。
- 遵守 Vue 模板安全规则（`v-html`、列表渲染、条件渲染选择）。

### 保持组件聚焦

当组件出现**不止一个明确职责**时必须拆分（例如：数据编排 + 大量 UI，或多个相互独立 UI 区块）。

- 优先 **小组件 + composables**，避免“巨型组件”
- 将 **UI 区块** 拆到子组件（props 输入，events 输出）。
- 将 **状态/副作用** 拆到 composables（`useXxx()`）。

按客观触发条件拆分，只要满足任一条件就拆：

- 同时承担编排/状态和多个区块的展示模板。
- 模板中有 3 个及以上独立 UI 区块（例如：表单、筛选、列表、底部状态）。
- 模板块出现重复或具备复用价值（列表项、卡片、条目行等）。

入口/根组件与路由视图规则：

- 入口/根组件与路由视图应保持轻量，仅承载壳层布局、provider 接线、功能组合。
- 当功能包含独立部分时，不要把完整功能实现塞进入口/根/视图组件。
- 对 CRUD/列表类功能（todo、table、catalog、inbox），至少拆为：
  - 功能容器组件
  - 输入/表单组件
  - 列表（和/或条目）组件
  - 底部动作或筛选/状态组件
- 仅在非常小的一次性 demo 中允许单文件实现，且要明确说明不拆分的理由。

### 组件数据流

- 必读资料： [component-data-flow](references/component-data-flow.md)
- 默认模型：props 向下、events 向上。
- 仅在真实双向绑定合约下使用 `v-model`。
- 仅在深层树共享上下文时使用 provide/inject。
- 使用 `defineProps`、`defineEmits`、`InjectionKey` 等保持合约显式且可类型约束。

### Composables

- 必读资料： [composables](references/composables.md)
- 当逻辑可复用、有状态或副作用较重时，抽为 composable。
- composable API 保持小、可预测、类型清晰。
- 功能逻辑与展示组件分离。

## 3) 仅在需求明确时使用可选能力

### 3.1 常见可选能力

默认不要主动加入，仅在需求明确时加载对应资料。

- Slots：父组件需要控制子组件内容/布局 -> [component-slots](references/component-slots.md)
- Fallthrough attributes：包装/基础组件需要安全透传 attrs/events -> [component-fallthrough-attrs](references/component-fallthrough-attrs.md)
- 内置组件 `<KeepAlive>`：需要缓存视图状态 -> [component-keep-alive](references/component-keep-alive.md)
- 内置组件 `<Teleport>`：需要弹层/portal -> [component-teleport](references/component-teleport.md)
- 内置组件 `<Suspense>`：需要异步子树 fallback 边界 -> [component-suspense](references/component-suspense.md)
- 动画相关能力：按需求选择最简单可行方案。
  - `<Transition>`：进入/离开动画 -> [transition](references/component-transition.md)
  - `<TransitionGroup>`：列表变更动画 -> [transition-group](references/component-transition-group.md)
  - 基于 class 的动画：非进入/离开类动画 -> [animation-class-based-technique](references/animation-class-based-technique.md)
  - 基于状态驱动动画：用户输入驱动动画 -> [animation-state-driven-technique](references/animation-state-driven-technique.md)

### 3.2 低频可选能力

仅在有明确产品或技术需求时使用：

- Directives：行为强依赖 DOM，且不适合 composable/component -> [directives](references/directives.md)
- Async components：重型或低频 UI 需要懒加载 -> [component-async](references/component-async.md)
- Render functions：模板无法表达需求时再使用 -> [render-functions](references/render-functions.md)
- Plugins：需要全局安装行为 -> [plugins](references/plugins.md)
- 状态管理模式：跨功能边界的全局共享状态 -> [state-management](references/state-management.md)

## 4) 功能正确后再做性能优化

性能优化属于功能完成后的第二阶段，不要先优化再实现行为。

- 大列表渲染瓶颈 -> [perf-virtualize-large-lists](references/perf-virtualize-large-lists.md)
- 静态子树反复重渲染 -> [perf-v-once-v-memo-directives](references/perf-v-once-v-memo-directives.md)
- 热路径列表中过度抽象 -> [perf-avoid-component-abstraction-in-lists](references/perf-avoid-component-abstraction-in-lists.md)
- 高开销更新触发过频 -> [updated-hook-performance](references/updated-hook-performance.md)

## 5) 完成前自检

- 核心行为正确并符合需求。
- 所有必读资料已阅读并落实。
- 响应式模型最小且可预测。
- SFC 结构与模板规则满足要求。
- 组件已按职责聚焦并在需要时拆分。
- 入口/根组件与路由视图保持组合层（除非明确小型 demo 例外）。
- 组件拆分决策可解释且边界清晰。
- 数据流合约显式且带类型约束。
- 在复用/复杂度需要时已使用 composables。
- 适用场景下已将状态/副作用迁移到 composables。
- 可选能力仅在需求要求时使用。
- 性能优化是在功能完成后才进行。
