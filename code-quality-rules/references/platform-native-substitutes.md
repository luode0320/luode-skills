# 平台原生替代方案速查目录

> 归属 owner：`code-quality-rules`（最小改动主线：阶梯第 4 阶「平台原生能力覆盖了吗？」支持清单）。
> 核心原则：**在伸手去装包或手写复杂 JS/胶水代码之前，先查阅平台底层是否原生支持。**
> 原生能力由平台/运行环境团队持续优化，随应用零体积发布、性能极致且天然免除版本漂移与维护负担。

---

## 1. HTML5 原生表单与交互元素

浏览器已原生内置多种复杂控件，无需额外引入笨重的第三方 UI 组件库或大型插件：

| 传统习惯引入第三方库 | 现代平台原生能力 | 说明与优势 |
|---|---|---|
| 日期选择器库（如 flatpickr） | `<input type="date">` | 移动端自动唤起原生滚轮，键盘可访问性天然支持 |
| 时间选择器库 | `<input type="time">` | 平台统一交互规范，支持精确到分秒 |
| 颜色选择器库 | `<input type="color">` | 操作系统原生调色板支持 |
| 滑块组件库 | `<input type="range">` | 轻量、支持语义化 min/max/step 属性 |
| 进度条组件 | `<progress value="70" max="100">` | 具备无障碍 aria 属性，天然可读 |
| 仪表盘/度量组件 | `<meter value="0.7">` | 表达标量测量或分段阈值状态 |
| 模态弹窗库（如 SweetAlert） | `<dialog>` + `dialog.showModal()` | 原生支持顶层渲染（Top Layer）、Esc 键关闭、焦点捕获与背景遮罩 `::backdrop` |
| 手风琴折叠面板/FAQ 组件 | `<details><summary>标题</summary>内容</details>` | 零 JS 代码实现内容展开/收起，可原生索引 |
| 可搜索自动补全下拉框 | `<input list="opts"> <datalist id="opts">` | 无需 JS 监听键盘事件，原生过滤下拉候选 |
| 自适应高度多行文本域 | CSS `field-sizing: content` | 现代 CSS 新特性，取代手写 scrollHeight 计算脚本 |

---

## 2. 现代 CSS 布局与样式能力

开发者过去习惯依赖 JS 动态计算、事件监听或预处理器才能实现的效果，现代 CSS 已原生全面覆盖：

| 传统依赖 JS 或预处理器 | 现代 CSS 原生能力 | 核心用法 / 优势 |
|---|---|---|
| 动态计算响应式字号 | `font-size: clamp(1rem, 2.5vw, 2rem)` | 单行声明区间限制，无需 JS 监听 resize |
| 流式弹性内间距 | `padding: clamp(1rem, 5vw, 3rem)` | 自适应窗口缩放，无断点断层 |
| 深色模式监听与切换 | `@media (prefers-color-scheme: dark)` | 自动跟随操作系统偏好，无感知切换 |
| 减弱动效偏好适配 | `@media (prefers-reduced-motion: reduce)` | 尊重无障碍与健康偏好，优雅降级过渡 |
| 复杂计算的自适应网格 | `grid-template-columns: repeat(auto-fill, minmax(240px, 1fr))` | 零媒体查询实现卡片瀑布流自适应布局 |
| 组件容器级响应式 | `@container (min-width: 400px)` | 摆脱视口依赖，组件依据其容器尺寸自适应排版 |
| 全局主题与动态传值 | CSS 自定义属性（`var(--primary-color)`） | 原生支持继承与运行时动态修改 |
| JS 平滑滚动脚本 | `scroll-behavior: smooth` | 零代码实现页面锚点平滑过渡 |
| 轮播吸附定位库 | `scroll-snap-type: x mandatory` + `scroll-snap-align: start` | 原生硬件加速，体验顺滑无掉帧 |
| 保持固定比例容器（如 16:9） | `aspect-ratio: 16 / 9` | 告别 `padding-top: 56.25%` 的黑魔法历史债务 |
| 单行文本截断加省略号 | `overflow: hidden; text-overflow: ellipsis; white-space: nowrap;` | 原生纯样式截断 |
| 多行文本截断加省略号 | `display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden;` | 原生多行文本裁剪 |
| 样式层级冲突（避免 !important） | `@layer base, components, utilities` | 原生控制样式优先级与层叠规则 |
| CSS 预处理器嵌套语法（Sass/Less） | 原生 CSS 嵌套（Native CSS Nesting） | 现代浏览器全面原生支持选择器嵌套，免编译 |
| 根据子元素状态修改父元素样式 | `:has(input:checked)` / `:has(.active)` | 彻底消除为了修饰父节点而手写的大量 JS 状态监听 |

---

## 3. 现代 JavaScript / Web API 替代第三方依赖

在 Node.js 与现代浏览器中，以下高频第三方 npm 依赖包大多已被标准 API 完整内建替代，**严禁在无特殊边界需求时额外引入对应第三方包**：

| 过去习惯安装的第三方 npm 包 | 现代原生 API 替代方案 | 替代代码范式与说明 |
|---|---|---|
| `query-string` / `qs` | `new URLSearchParams(location.search)` | `params.get("id")`、`params.append(...)` 原生支持 |
| `lodash.clonedeep` | `structuredClone(obj)` | 真正深拷贝，支持循环引用、Date、RegExp、Map、Set 等 |
| `lodash.groupby` | `Object.groupBy(array, item => item.type)` | ES2024 标准方法，原生分组输出对象 |
| `numeral` / `accounting` | `new Intl.NumberFormat("zh-CN", { style: "currency", currency: "CNY" })` | 支持货币、百分比、千分位及多国语言规范 |
| `date-fns` / `moment`（仅格式化） | `new Intl.DateTimeFormat("zh-CN", { dateStyle: "long", timeStyle: "short" })` | 平台本地化标准时间格式化 |
| `date-fns`（相对时间计算） | `new Intl.RelativeTimeFormat("zh", { numeric: "auto" }).format(-3, "day")` | 原生输出“3天前”、“昨天”等相对表达 |
| `clipboard.js` | `navigator.clipboard.writeText(text)` | 基于 Promise 的现代异步剪贴板 API |
| `uuid`（仅生成 v4 UUID） | `crypto.randomUUID()` | 浏览器与 Node.js 14.17+ 均原生支持，性能极佳 |
| `intersection-observer`（无限滚动） | `new IntersectionObserver(callback).observe(el)` | 视口交叉监听，无需手写 scroll 事件节流计算 |
| `resize-observer-polyfill` | `new ResizeObserver(callback).observe(el)` | 元素尺寸变化精确感知 |
| 请求超时封装库 | `fetch(url, { signal: AbortSignal.timeout(5000) })` | 原生支持超时中断信号，免除手动写 Promise.race 计时器 |
| 跨组件事件总线库（如 eventemitter3） | `new EventTarget()` / `dispatchEvent(new CustomEvent("ev", { detail }))` | 浏览器与现代 Node.js 内置标准事件分发模型 |

### 极简一行版高频工具（防引包范例）

当需要防抖（debounce）等逻辑且未装大型函数式工具库时，几行代码即可自闭环，绝不为此类小功能新增一个依赖：

```javascript
// 简单极简防抖：满足绝大多数单事件防重/延迟触发需求
const debounce = (fn, ms) => {
  let timer;
  return (...args) => {
    clearTimeout(timer);
    timer = setTimeout(() => fn(...args), ms);
  };
};
```

---

## 4. 后端语言平台（Go / Python）原生优先启示

不仅前端如此，后端研发同样遵守阶梯第 3 阶（标准库）与第 4 阶（平台原生）：

- **Go 语言**：
  - 切片与映射处理：优先使用 Go 1.21+ 标准库 `slices`（`Contains`, `Sort`, `Index`, `Compact`）与 `maps`，不手写遍历查找或引入第三方切片操作包；
  - 路径与文件：优先使用 `filepath.Clean`、`os.ReadFile`，不封装多余的 IO 包装器；
  - 格式化与解析：标准库 `encoding/json` 已能满足大多数业务，除非性能剖析证明是系统绝对瓶颈，否则不盲目换用第三方黑盒序列化库。
- **Python 语言**：
  - 数据模型：优先使用标准库 `dataclasses` 或 `typing.NamedTuple`，纯数据载体不写繁琐的 `__init__` 与 `__repr__`；
  - 缓存机制：优先使用标准库 `functools.lru_cache` 或 `functools.cache`，不手写基于全局 dict 的有缺陷缓存类；
  - 路径处理：优先使用标准库 `pathlib.Path`，以面向对象风格直观处理路径，不手写字符串拼接或碎片化 `os.path`；
  - 字典排序与计数：优先使用标准库 `collections.Counter` / `defaultdict`，不手写字典初始化判空逻辑。
