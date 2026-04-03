---
name: vercel-react-best-practices
description: 来自 Vercel Engineering 的 React / Next.js 性能优化指南。适用于编写、评审、重构 React/Next.js 代码时，确保采用高性能实现模式。触发场景包括 React 组件、Next.js 页面、数据获取、包体积优化与性能改进任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
---

# Vercel React 最佳实践

这是由 Vercel 维护的 React 与 Next.js 综合性能优化指南。  
包含 8 大类别、共 69 条规则，按影响力排序，可用于指导自动化重构与代码生成。

## 何时使用

以下场景建议应用本指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取逻辑（客户端或服务端）
- 评审性能相关问题
- 重构现有 React / Next.js 代码
- 优化包体积和加载时长

## 按优先级划分的规则类别

| 优先级 | 类别 | 影响等级 | 前缀 |
|----------|----------|--------|--------|
| 1 | 消除请求瀑布 | CRITICAL | `async-` |
| 2 | 包体积优化 | CRITICAL | `bundle-` |
| 3 | 服务端性能 | HIGH | `server-` |
| 4 | 客户端数据获取 | MEDIUM-HIGH | `client-` |
| 5 | 重渲染优化 | MEDIUM | `rerender-` |
| 6 | 渲染性能 | MEDIUM | `rendering-` |
| 7 | JavaScript 性能 | LOW-MEDIUM | `js-` |
| 8 | 高级模式 | LOW | `advanced-` |

## 快速索引

### 1. 消除请求瀑布（CRITICAL）

- `async-cheap-condition-before-await` - 在等待远端值前，先判断廉价同步条件
- `async-defer-await` - 将 `await` 延后到真正需要的分支中
- `async-parallel` - 对独立任务使用 `Promise.all()`
- `async-dependencies` - 对部分依赖任务使用更合理的并行方式
- `async-api-routes` - API 路由中尽早启动 Promise、尽晚 await
- `async-suspense-boundaries` - 使用 Suspense 实现流式内容输出

### 2. 包体积优化（CRITICAL）

- `bundle-barrel-imports` - 直接按文件导入，避免 barrel 聚合导入
- `bundle-dynamic-imports` - 重组件使用 `next/dynamic`
- `bundle-defer-third-party` - 第三方统计/日志在 hydration 后再加载
- `bundle-conditional` - 模块仅在功能启用时按需加载
- `bundle-preload` - 在 hover/focus 时预加载提升体感速度

### 3. 服务端性能（HIGH）

- `server-auth-actions` - 服务端 action 要像 API 一样做鉴权
- `server-cache-react` - 使用 `React.cache()` 做单次请求内去重
- `server-cache-lru` - 使用 LRU 做跨请求缓存
- `server-dedup-props` - 避免 RSC props 重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、logo）提升到模块级
- `server-no-shared-module-state` - 在 RSC/SSR 中避免模块级可变请求状态
- `server-serialization` - 最小化传给客户端组件的数据
- `server-parallel-fetching` - 重构组件结构以并行拉取数据
- `server-parallel-nested-fetching` - 列表项内嵌请求也应并行链式处理
- `server-after-nonblocking` - 使用 `after()` 执行非阻塞任务

### 4. 客户端数据获取（MEDIUM-HIGH）

- `client-swr-dedup` - 使用 SWR 自动去重请求
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 滚动监听优先使用 passive
- `client-localstorage-schema` - 对 localStorage 做版本化并控制体积

### 5. 重渲染优化（MEDIUM）

- `rerender-defer-reads` - 仅在回调里用到的状态，不要提前订阅
- `rerender-memo` - 将高开销逻辑抽到 memo 化组件
- `rerender-memo-with-default-value` - 非原始类型默认值上提，保持引用稳定
- `rerender-dependencies` - effect 依赖尽量使用原始值
- `rerender-derived-state` - 优先订阅派生布尔值，而不是原始大对象
- `rerender-derived-state-no-effect` - 派生状态在 render 阶段计算，避免 effect 二次同步
- `rerender-functional-setstate` - 使用函数式 `setState` 保证回调稳定
- `rerender-lazy-state-init` - `useState` 传函数做懒初始化
- `rerender-simple-expression-in-memo` - 简单原始值表达式不必 `memo`
- `rerender-split-combined-hooks` - 按依赖拆分复合 hooks
- `rerender-move-effect-to-event` - 交互逻辑放事件处理器，不滥用 effect
- `rerender-transitions` - 非紧急更新使用 `startTransition`
- `rerender-use-deferred-value` - 重渲染代价高时用 `useDeferredValue`
- `rerender-use-ref-transient-values` - 高频临时值用 ref 存储
- `rerender-no-inline-components` - 不要在组件内部定义子组件

### 6. 渲染性能（MEDIUM）

- `rendering-animate-svg-wrapper` - 动画作用在外层 wrapper，不直接操作 SVG 本体
- `rendering-content-visibility` - 长列表使用 `content-visibility`
- `rendering-hoist-jsx` - 静态 JSX 提升到组件外
- `rendering-svg-precision` - 降低 SVG 坐标精度以减小体积
- `rendering-hydration-no-flicker` - 客户端专属数据可配合内联脚本减少闪烁
- `rendering-hydration-suppress-warning` - 预期不一致场景使用抑制警告
- `rendering-activity` - 用 Activity 组件处理显示/隐藏
- `rendering-conditional-render` - 条件渲染优先三元表达式而非 `&&`
- `rendering-usetransition-loading` - loading 状态优先 `useTransition`
- `rendering-resource-hints` - 使用 React DOM resource hints 做预加载
- `rendering-script-defer-async` - 脚本使用 `defer` 或 `async`

### 7. JavaScript 性能（LOW-MEDIUM）

- `js-batch-dom-css` - 通过 class 或 cssText 批量修改样式
- `js-index-maps` - 重复查找场景用 Map 建索引
- `js-cache-property-access` - 循环内缓存对象属性访问
- `js-cache-function-results` - 使用模块级 Map 缓存函数结果
- `js-cache-storage` - 缓存 localStorage / sessionStorage 读取
- `js-combine-iterations` - 合并多次 filter/map 为一次遍历
- `js-length-check-first` - 先做 length 检查再做高成本比较
- `js-early-exit` - 尽早 return，减少无效执行
- `js-hoist-regexp` - RegExp 创建提升到循环外
- `js-min-max-loop` - 求最值优先循环，不要先排序
- `js-set-map-lookups` - 查找操作优先 Set/Map 的 O(1)
- `js-tosorted-immutable` - 不可变排序优先 `toSorted()`
- `js-flatmap-filter` - 使用 `flatMap` 一次完成映射和过滤
- `js-request-idle-callback` - 非关键任务延后到浏览器空闲时执行

### 8. 高级模式（LOW）

- `advanced-effect-event-deps` - 不要把 `useEffectEvent` 结果放进 effect 依赖
- `advanced-event-handler-refs` - 事件处理器可存入 ref 保持稳定
- `advanced-init-once` - 应用初始化每次加载只执行一次
- `advanced-use-latest` - 使用 `useLatest` 维护稳定回调引用

## 使用方式

需要查看详细解释和代码示例时，直接阅读对应规则文件：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每条规则文件通常包含：
- 规则价值的简要说明
- 错误示例与原因
- 正确示例与原因
- 补充背景与参考资料

## 完整汇总文档

所有规则展开版请查看：`AGENTS.md`
