# Web Interface Guidelines（本地兜底版）

> 本文件为远程规范的本地兜底副本（v1 快照）。远程拉取失败时按此执行；成功后以远程最新版为准。
> 同步源：https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md

## 无障碍（Accessibility）
- 图标按钮需 `aria-label`
- 表单控件需 `<label>` 或 `aria-label`
- 交互元素需键盘处理（`onKeyDown`/`onKeyUp`）
- 动作用 `<button>`，导航用 `<a>`/`<Link>`（禁用 `<div onClick>`）
- 图片需 `alt`（装饰性图片 `alt=""`）
- 装饰性图标需 `aria-hidden="true"`
- 异步更新（toast、校验）需 `aria-live="polite"`
- 优先语义 HTML（`<button>`/`<a>`/`<label>`/`<table>`）再用 ARIA
- 标题层级 `<h1>`–`<h6>` 有序；主内容区提供 skip link
- 标题锚点加 `scroll-margin-top`
- 有意义的媒体需字幕/转录/描述；媒体控件需键盘支持；装饰性媒体隐藏于辅助技术

## 焦点状态（Focus States）
- 交互元素需可见焦点：`focus-visible:ring-*` 或等价
- 禁止无替换的 `outline-none` / `outline: none`
- 用 `:focus-visible` 而非 `:focus`（避免点击出焦点环）
- 复合控件用 `:focus-within` 分组焦点
- 吸顶头/脚/浮层不得遮挡焦点元素

## 表单（Forms）
- 输入需 `autocomplete` 与有意义的 `name`
- 使用正确 `type`（`email`/`tel`/`url`/`number`）与 `inputmode`
- 禁止阻止粘贴（`onPaste` + `preventDefault`）
- 标签可点击（`htmlFor` 或包裹控件）
- 邮箱/验证码/用户名禁用拼写检查（`spellCheck={false}`）
- 复选框/单选：标签+控件共享命中区域（无死区）
- 提交按钮在请求开始前保持启用；请求中显示 spinner
- 错误内联显示在字段旁；提交时聚焦第一个错误
- 占位符以 `…` 结尾并给出示例格式
- 非认证字段 `autocomplete="off"` 防密码管理器误触发
- 未保存更改的导航需提醒（`beforeunload` 或路由守卫）

## 动画（Animation）
- 尊重 `prefers-reduced-motion`（提供降级或禁用）
- 只动画 `transform`/`opacity`（合成器友好）
- 禁止 `transition: all`——显式列出属性
- 设置正确 `transform-origin`
- SVG：在 `<g>` 包装器上做变换，配 `transform-box: fill-box; transform-origin: center`
- 动画可中断——响应动画中的用户输入
- 与其他内容并排的自动播放动效 >5 秒需提供暂停/停止/隐藏
- 装饰性循环动效在 `prefers-reduced-motion` 下必须停止

## 排版（Typography）
- 省略号用 `…` 不用 `...`
- 弯引号 `“”` 不用直引号 `"`
- 不换行空格：`10&nbsp;MB`、`⌘&nbsp;K`、品牌名
- 加载态以 `…` 结尾：`"Loading…"`、`"Saving…"`
- 数字列/比较用 `font-variant-numeric: tabular-nums`
- 标题用 `text-wrap: balance` 或 `text-pretty`（防孤行）

## 内容处理（Content Handling）
- 文本容器处理长内容：`truncate`、`line-clamp-*` 或 `break-words`
- flex 子项需 `min-w-0` 以支持文本截断
- 处理空状态——空字符串/数组不渲染破碎 UI
- 用户生成内容：预判短、中、超长输入

## 图片（Images）
- `<img>` 需显式 `width` 与 `height`（防 CLS）
- 首屏以下图片 `loading="lazy"`
- 首屏关键图片 `priority` 或 `fetchpriority="high"`

## 性能（Performance）
- 大列表（>50 项）虚拟化（`virtua`、`content-visibility: auto`）
- 渲染中不做布局读取（`getBoundingClientRect`、`offsetHeight`、`offsetWidth`、`scrollTop`）
- 批量 DOM 读/写，不交错
- 优先非受控输入；受控输入需按键成本低
- CDN/资源域名加 `<link rel="preconnect">`
- 关键字体 `<link rel="preload" as="font">` + `font-display: swap`
- 优先 `<video autoplay muted loop playsinline>` 而非 GIF；提供静态替代

## 导航与状态（Navigation & State）
- URL 反映状态——筛选/标签/分页/展开面板进 query 参数
- 链接用 `<a>`/`<Link>`（支持 Cmd/Ctrl+点击、中键）
- 有状态 UI 可深链（用 `useState` 的考虑 URL 同步，如 nuqs）
- 破坏性操作需确认弹窗或撤销窗口——绝不立即执行

## 触摸与交互（Touch & Interaction）
- `touch-action: manipulation`（防双击缩放延迟）
- `-webkit-tap-highlight-color` 有意设置
- 弹窗/抽屉/面板内 `overscroll-behavior: contain`
- 拖拽期间禁用文本选择，拖拽元素加 `inert`
- 拖拽/滑动/捏合/路径手势需点击/键盘替代（非必需场景）
- `autoFocus` 慎用——仅桌面、单一主输入；移动端避免

## 安全区与布局（Safe Areas & Layout）
- 全出血布局用 `env(safe-area-inset-*)` 适配刘海
- 避免多余滚动条：容器 `overflow-x-hidden`，修复内容溢出
- 布局用 flex/grid 而非 JS 测量

## 深色模式与主题（Dark Mode & Theming）
- 深色主题 `<html>` 设 `color-scheme: dark`（修复滚动条、输入框）
- `<meta name="theme-color">` 匹配页面背景
- 原生 `<select>` 显式 `background-color` 与 `color`（Windows 深色模式）

## 本地化（Locale & i18n）
- 日期/时间用 `Intl.DateTimeFormat` 而非硬编码格式
- 数字/货币用 `Intl.NumberFormat` 而非硬编码格式
- 语言检测用 `Accept-Language`/`navigator.languages`，不用 IP
- 品牌名、代码令牌、标识符包 `translate="no"` 防自动翻译损坏

## 水合安全（Hydration Safety）
- 带 `value` 的输入需 `onChange`（或非受控用 `defaultValue`）
- 日期/时间渲染防水合不一致（服务端 vs 客户端）
- `suppressHydrationWarning` 仅在确需处使用

## 悬停与交互状态（Hover & Interactive States）
- 按钮/链接需 `hover:` 状态（视觉反馈）
- 交互状态提升对比度：hover/active/focus 比其余更突出

## 文案（Content & Copy）
- 主动语态："Install the CLI" 而非 "The CLI will be installed"
- 标题/按钮 Title Case（Chicago 风格）
- 计数用数字："8 deployments" 而非 "eight"
- 按钮标签具体："Save API Key" 而非 "Continue"
- 错误信息含修复/下一步，而非只报问题
- 第二人称；避免第一人称
- 空间受限处用 `&` 代替 "and"

## 反模式（必须标记）
- `user-scalable=no` 或 `maximum-scale=1` 禁用缩放
- `onPaste` + `preventDefault`
- `transition: all`
- 无 focus-visible 替代的 `outline-none`
- 无 `<a>` 的内联 `onClick` 导航
- 带点击处理器的 `<div>`/`<span>`（应为 `<button>`）
- 无尺寸的图片
- 大数组 `.map()` 未虚拟化
- 无标签的表单输入
- 无 `aria-label` 的图标按钮
- 硬编码日期/数字格式（用 `Intl.*`）
- 无明确理由的 `autoFocus`
- 适合压缩视频却用动画 GIF
- 纯手势操作无点击/键盘替代

## 输出格式

按文件分组，`file:line` 格式（VS Code 可点击），结论精炼：

```text
## src/Button.tsx

src/Button.tsx:42 - icon button missing aria-label
src/Button.tsx:18 - input lacks label
src/Button.tsx:55 - animation missing prefers-reduced-motion
src/Button.tsx:67 - transition: all → list properties

## src/Modal.tsx

src/Modal.tsx:12 - missing overscroll-behavior: contain
src/Modal.tsx:34 - "..." → "…"

## src/Card.tsx

✓ pass
```

只给问题+位置，除非修复不显然否则不解释。无开场白。
