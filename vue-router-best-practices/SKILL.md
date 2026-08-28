---
name: vue-router-best-practices
description: 处理 Vue Router 4 导航守卫、路由参数变化、路由生命周期、next() 废弃写法等坑点时使用。触发词：导航守卫 / 路由参数 / beforeRouteEnter / next 废弃 / 无限重定向 / 脏数据 / 路由生命周期 / vue-router 坑点 / router-view / hashchange。
license: MIT
metadata:
  author: github.com/vuejs-ai
  version: "1.1.0"
  displayName: Vue Router 最佳实践
---

# Vue Router 最佳实践与坑点决策

## 一、定位与适用边界

- **做什么**：把 Vue Router 4 的 8 个高频坑点按症状分类，提供「症状 → 判定 → 修复」的可执行决策路由。
- **何时用**：用户报障或写码时出现导航守卫异常、路由参数不更新、组件生命周期与路由交互异常、`next()` 废弃写法、无限重定向等场景。
- **触发词**：导航守卫 / 路由参数 / beforeRouteEnter / next 废弃 / 无限重定向 / 路由生命周期 / vue-router 坑点。
- **不适用**：组件内部的响应式、状态管理（Pinia）、构建配置等问题不属于本 skill，转 `vue-best-practices`（见交叉引用）。

## 二、症状决策流程（4 步）

1. **识别症状类别**：导航守卫（守卫不触发 / 挂起 / 循环）/ 路由生命周期（数据不刷新 / 监听残留）/ 基础搭建（简易路由 vs Vue Router）。
2. **查 impact 分级决策表**：按下表症状与判定标准定位坑点，按 impact 优先级处理（HIGH 优先）。
3. **读对应 reference 全文**：每篇含「问题代码 → 修复代码 → Key Points」，必须读全文再动手，禁止只看决策表一行就改。
4. **按 Task Checklist 应用修复并验证**：逐项勾选该篇 Task Checklist，修复后跑一次真实导航验证（含同路由参数变化场景）。

## 三、impact 分级决策表（8 坑点）

### HIGH（3 项，优先处理）

| 症状 | 判定标准 | reference | 修复要点 |
|---|---|---|---|
| 无限重定向循环（浏览器崩溃/应用不可用） | 守卫 return 目标路由但无「已在目标路由」短路；A→B→A 互跳 | `reference/router-navigation-guard-infinite-loop.md` | 重定向前先查是否已在目标路由；用 route meta 控制保护范围；devtools 查重定向链 |
| 导航挂起 / 静默失败（`next()` 废弃写法） | 守卫签名含 `next` 参数；多次调用 / 忘记调用 / 条件调用 | `reference/router-navigation-guard-next-deprecated.md` | 改用 return-based：`return false` 取消、`return 路由` 重定向、`return undefined` 放行；async 检查用 async/await |
| 同路由参数变化后数据不刷新（脏数据） | 数据加载写在 `onMounted`/`created` 且依赖 `route.params`；`/users/1`→`/users/2` 不触发 | `reference/router-param-change-no-lifecycle.md` | `watch(() => route.params)` 或 `onBeforeRouteUpdate` 重新拉取；`:key` 强制重建（低效，最后手段） |

### MEDIUM（4 项）

| 症状 | 判定标准 | reference | 修复要点 |
|---|---|---|---|
| 仅参数/query/hash 变化时 `beforeEnter` 不触发（校验被绕过） | 校验逻辑放在 route 级 `beforeEnter` 且依赖参数 | `reference/router-beforeenter-no-param-trigger.md` | 组件内 `onBeforeRouteUpdate` 或全局 `beforeEach` 检查 params/query；注明各守卫保护场景 |
| `beforeRouteEnter` 中 `this` 为 undefined | Options API 守卫内访问 `this` | `reference/router-beforerouteenter-no-this.md` | 用 `next(vm => ...)` 回调访问实例；按数据时机选守卫 |
| 守卫内 async 检查未 await（未授权访问/数据缺失） | 守卫回调非 async 且未返回 promise；或 async 但漏 return | `reference/router-guard-async-await-pattern.md` | 守卫内 `async/await` 或 `return promise`；慢请求加 loading；超时与错误处理防挂起 |
| hashchange 监听未清理（内存泄漏/多 handler 并发） | 组件内 `addEventListener('hashchange')` 无对应移除 | `reference/router-simple-routing-cleanup.md` | 存监听引用，`onUnmounted` 移除；生产应用直接改用 Vue Router |

### LOW（1 项）

| 症状 | 判定标准 | reference | 修复要点 |
|---|---|---|---|
| 简易 hash 路由不满足生产 SPA 需求 | 生产应用手写 hash 路由，缺守卫/嵌套路由/懒加载/history 集成 | `reference/router-use-vue-router-for-production.md` | 安装官方 vue-router；仅学习/原型/2-3 页微应用可保留简易路由 |

## 四、执行规则

- **修复前**：必须读取目标坑点的 reference 全文（问题代码 + 修复代码 + Key Points），不得凭决策表一行直接改码。
- **修复中**：逐项完成该篇 Task Checklist；守卫类修改必须覆盖「同路由参数变化」「失败/重定向路径」两类导航验证。
- **修复后**：用 Vue Router devtools 或真实导航确认无重定向循环、无守卫挂起。

## 五、交叉引用（不复制正文）

- `vue-best-practices`：整体 Vue 执行（组件 / composables / 响应式 / 性能）指回该 skill；其 keep-alive/suspense 涉及 RouterView 嵌套时，路由专精坑点以本 skill 为准。
- `vue__skillhub`：无路由专精需求时的 Vue 速查兜底（注意其 frontmatter 有合规问题，仅引用内容不联动校验）。

## 六、边界与维护

- `reference/` 8 篇是坑点内容的**唯一事实源**，本 SKILL.md 只做决策路由，**不复制正文**（防双份漂移）。
- 修改某坑点文档时，必须同步更新本表对应行（症状/判定/修复要点），保持路由一致。
- `SYNC.md` 为上游 vendor 同步记录，只读保留，不参与本 skill 逻辑。
