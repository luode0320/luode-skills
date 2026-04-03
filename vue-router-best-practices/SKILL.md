---
name: vue-router-best-practices
description: "Vue Router 4 模式、导航守卫、路由参数以及路由与组件生命周期交互的最佳实践。"
version: 1.0.0
license: MIT
author: github.com/vuejs-ai
---

Vue Router 最佳实践、常见坑点与导航模式指南。

### 导航守卫
- 在同一路由间仅参数变化时导航问题 → 参见 [router-beforeenter-no-param-trigger](reference/router-beforeenter-no-param-trigger.md)
- 在 `beforeRouteEnter` 中访问组件实例问题 → 参见 [router-beforerouteenter-no-this](reference/router-beforerouteenter-no-this.md)
- 导航守卫中发起 API 请求但未正确 `await` → 参见 [router-guard-async-await-pattern](reference/router-guard-async-await-pattern.md)
- 用户陷入无限重定向循环 → 参见 [router-navigation-guard-infinite-loop](reference/router-navigation-guard-infinite-loop.md)
- 导航守卫仍使用已过时的 `next()` 写法 → 参见 [router-navigation-guard-next-deprecated](reference/router-navigation-guard-next-deprecated.md)

### 路由生命周期
- 同一路由切换参数后数据未更新（脏数据）→ 参见 [router-param-change-no-lifecycle](reference/router-param-change-no-lifecycle.md)
- 组件卸载后事件监听仍残留 → 参见 [router-simple-routing-cleanup](reference/router-simple-routing-cleanup.md)

### 基础搭建
- 构建生产级单页应用（SPA）→ 参见 [router-use-vue-router-for-production](reference/router-use-vue-router-for-production.md)
