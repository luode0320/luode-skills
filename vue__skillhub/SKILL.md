---
name: vue
description: "构建 Vue 3 应用：Composition API 组织、ref/reactive 响应式正确用法、watch/computed 选择、props/emits 类型化、模板 ref、生命周期清理、provide/inject、Vue Router 集成、v-if/v-for 常见错误、性能优化。适用于开发/审查 Vue 3 组件、排查界面不更新/响应式丢失/watch 不触发、性能问题场景。触发词：vue、vue3、vue 组件、composable、ref、reactive、响应式不生效、界面不更新、watch 不触发、computed、defineProps、defineEmits、v-model、onMounted、provide inject、vue 性能、vue 报错。"
license: MIT
metadata:
  displayName: "Vue 3 组件开发"
  version: "1.1.0"
  author: "Clawhub Developer"
---

# Vue 3 组件开发

Vue 3 组件正确性与性能手册。**先走「工作流」再查「知识区」**：开发组件、排查响应式失效、排查性能各有固定流程；陷阱细节按主题索引文件深入。

## 工作流

### 组件开发流程
1. **组织**：`<script setup>` + Composition API，按**功能分组**（不是按选项类型分组）。
2. **接口**：`defineProps<{...}>()` 类型化 props；`defineEmits<{...}>()` 类型化事件；props 只读不直接改。
3. **响应式**：基础值用 `ref`、对象用 `reactive`；解构 `reactive` 前用 `toRefs`；从 props 派生状态用 `computed`。
4. **副作用**：`watch` 处理副作用（需要 old/new 时）；`onUnmounted` 清理订阅/定时器/事件。
5. **验证**：交互一次 + 数据更新一次，确认 UI 与状态同步（无控制台告警）。

### 响应式失效排查流程
1. 界面不更新：检查是否 `state = {...}` 整体重新赋值了 `reactive` → 用 `Object.assign` 或 ref。
2. 解构后丢失响应：`const { name } = state` → 改 `toRefs(state)`。
3. `watch` 不触发：观察 reactive 对象需 `deep: true` 或 watch 一个 getter；首次不执行加 `immediate: true`。
4. 模板 ref 拿不到：确认 `ref="name"` 与 `const name = ref(null)` 名字完全一致，且访问发生在 `onMounted` 后。

### 性能排查流程
1. 大列表卡顿：`v-for` 必须有稳定 `:key`；考虑虚拟滚动。
2. 频繁重渲染：检查是否过度 `watch` 大对象、computed 里塞副作用。
3. 按需加载：路由级 code-splitting；重组件 `defineAsyncComponent`。
4. 验证：DevTools Performance 录制一次交互，重渲染次数与耗时明显下降。

## When to Use

User needs Vue expertise — from Composition API patterns to production optimization. Agent handles reactivity, component design, state management, and performance.

## Quick Reference

| Topic | File |
|-------|------|
| Reactivity patterns | `reactivity.md` |
| Component patterns | `components.md` |
| Composables design | `composables.md` |
| Performance optimization | `performance.md` |

## Composition API Philosophy

- Composition API is not about replacing Options API—it's about better code organization
- Group code by feature, not by option type—related logic stays together
- Extract reusable logic into composables—the main win of Composition API
- `<script setup>` is the recommended syntax—cleaner and better performance

## Reactivity Traps

- `ref` for primitives—access with `.value` in script, auto-unwrapped in template
- `reactive` can't reassign whole object—`state = {...}` breaks reactivity
- Destructuring `reactive` loses reactivity—use `toRefs(state)` to preserve
- Array index assignment reactive in Vue 3—`arr[0] = x` works, unlike Vue 2
- Nested refs unwrap inside reactive—`reactive({count: ref(0)}).count` is number, not ref

## Watch vs Computed

- `computed` for derived state—cached, recalculates only when dependencies change
- `watch` for side effects—when you need to DO something in response to changes
- `computed` should be pure—no side effects, no async
- `watchEffect` for immediate reaction with auto-tracked dependencies

## Watch Traps

- Watching reactive object needs `deep: true`—or watch a getter function
- `watch` is lazy by default—use `immediate: true` for initial run
- Watch callback receives old/new—`watch(source, (newVal, oldVal) => {})`
- `watchEffect` can't access old value—use `watch` if you need old/new comparison
- Stop watchers with returned function—`const stop = watch(...); stop()`

## Props and Emits Traps

- `defineProps` for type-safe props—`defineProps<{ msg: string }>()`
- Props are readonly—don't mutate, emit event to parent
- `defineEmits` for type-safe events—`defineEmits<{ (e: 'update', val: string): void }>()`
- `v-model` is `:modelValue` + `@update:modelValue`—custom v-model with `defineModel()`
- Default value for objects must be factory function—`default: () => ({})`

## Template Ref Traps

- `ref="name"` + `const name = ref(null)`—names must match exactly
- Template refs available after mount—access in `onMounted`, not during setup
- `ref` on component gives component instance—`ref` on element gives DOM element
- Template ref with `v-for` becomes array of refs

## Lifecycle Traps

- `onMounted` for DOM access—component mounted to DOM
- `onUnmounted` for cleanup—subscriptions, timers, event listeners
- `onBeforeMount` runs before DOM insert—rarely needed but exists
- Hooks must be called synchronously in setup—not inside callbacks or conditionals
- Async setup needs `<Suspense>` wrapper

## Provide/Inject Traps

- `provide('key', value)` in parent—`inject('key')` in any descendant
- Reactive if value is ref/reactive—otherwise static snapshot
- Default value: `inject('key', defaultVal)`—third param for factory function
- Symbol keys for type safety—avoid string key collisions

## Vue Router Traps

- `useRoute` for current route—reactive, use in setup
- `useRouter` for navigation—`router.push('/path')`
- Navigation guards: `beforeEach`, `beforeResolve`, `afterEach`—return `false` to cancel
- `<RouterView>` with named views—multiple views per route

## Common Mistakes

- `v-if` vs `v-show`—v-if removes from DOM, v-show toggles display
- Key on `v-for` required—`v-for="item in items" :key="item.id"`
- Event modifiers order matters—`.prevent.stop` vs `.stop.prevent`
- Teleport for modals—`<Teleport to="body">` renders outside component tree

## 适用边界

**何时用**：开发/审查 Vue 3 组件与组合式逻辑、排查响应式/watch/生命周期问题、做性能优化。

**何时不用**：
- Vue Router 路由编排深度问题 → 转 `vue-router-best-practices`；
- 自动生成组件/页面代码 → 转 `vue-component-generator__skillhub`；
- 前端视觉/主题/UI 规范 → 转 `frontend-ui-visual-rules`、`frontend-design`；
- 前端组件拆分/目录归属 → 转 `frontend-component-rules`；
- 项目工程结构（非 Vue 语法）→ 转 `package-structure-rules`。

## 验收清单

- [ ] 组件用 `<script setup>`，逻辑按功能分组
- [ ] props/emits 已类型化；未直接修改 props
- [ ] 无 `reactive` 整体重赋值 / 解构丢响应性问题
- [ ] `watch` 已考虑 `deep`/`immediate`；副作用在 `onUnmounted` 清理
- [ ] `v-for` 有稳定 `:key`；无 computed 内副作用
- [ ] 模板 ref 命名一致且在 `onMounted` 后访问
