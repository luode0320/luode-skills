# 形变语言升级计划：从 6 处特例到一套语式

> 状态：**已执行（2026-10-31）**——6 个组件落地形变，4 处按理由跳过
> 起因：用户指出「登录的动效是按钮由一个形状变成另一个形状，而不是底色的变化」——此前的十几轮改造全部属于**缓动**（颜色/位置变化的曲线），不是**形变**（形状本身改变）。
> 结论先行：**能变形的不多，但刚好都是最需要它的地方**。42 个组件在状态里动几何，且**全部落在可写层**；真正的障碍不是冻结面，而是 `v-if`。

## 全量扫描结论（154 个组件）

按「有没有形变机会」四类扫全库，结果：**12 个已有形变、43 个有形式变但受现实限制、99 个状态只换色**。

| 分类 | 数量 | 处置 |
|---|---|---|
| 已有形变 | 12 | 见执行状态表 |
| 有形式变、但被现实卡住 | 43 | 逐条列出原因，见下 |
| 状态只换色 | 99 | 加形变等于重新设计状态表达，不属于形变升级 |

### 43 个「有形式变但没做」的原因分类

**① 开合靠浮层入场，而 `overlayEnter` 在冻结的 `motion.ts` 里（26 个）**

`Dropdown` `DropdownButton` `DropdownSubmenu` `Popover` `Popconfirm` `Tooltip` `HelpTip` `AutoComplete` `Cascader` `CascaderPanel` `ColorPicker` `DatePicker` `MonthPicker` `QuarterPicker` `RangePicker` `WeekPicker` `YearPicker` `TimePicker` `Mention` `TreeSelect` `OverflowList`，以及冻结的 `CommandPalette` `Drawer` `HoverCard` `Modal` `Select`。

→ 要做必须先给 `overlayEnter` 开缝隙，或本地重写一份入场。这两个都是结构改造，不属于「补形变」。

**② 选中态没有「标记元素」，只有行高亮（8 个）**

`Anchor` `Calendar` `ImagePreviewGroup` `StyledScrollbar` `AppearanceSettings`（色点环已有）、`Carousel`（圆点宽度已在变）、冻结的 `TickRing` `Sidebar`。

→ 它们选中时变的是底色或文字色，没有可生长的圆点/勾。要做形变得**先新增一个标记元素**，那是重新设计而不是补动效。

**③ 有完成语义但图标挂载即存在 / 没有可收拢的载体（5 个）**

`Alert` `Notification` `Result` `LinkText`、冻结的 `GeneratorPipeline`。

→ 图标由属性驱动、出现即存在；给它们加入场动效会让一屏提示条同时晃。`Result` 的图标倒是可以落定，但它是整页级组件、一次只出现一个，收益低。

**④ 增删但宿主冻结或只是图片切换（4 个）**

`Image` `ImagePreview` `ImagePreviewGroup`（换图不是增删）、冻结的 `Topbar`、以及 `Upload`（进度条 `v-if` 卸载，没有收拢余地）。

→ `Upload` 要做得先把列表行改成「进度条常驻 + 宽度收到 0」，属结构改造。

## 执行状态

### 通用语式：列表入场（一次覆盖一批组件）

逐组件改完只有 7 个，覆盖面太小。改成定义**一条通用语式**放在 `overrides.css`：

```css
@keyframes morph-enter {
  from { opacity: 0; transform: translateY(6px); }
  to   { opacity: 1; transform: none; }
}
```

再把这组容器选择器挂上去：`.table tbody tr`、`.x-datalist-row`、`.x-timeline-item`、`.activity-list > .activity`、`.share-list > li`、`.x-desc-item`、`.bento-grid > *`、`.quick-link`，前 8 条各差 26ms、第 8 条起封顶（长列表不该滚出一波浪）。

覆盖组件：`DataTable` `ListPage` `PermissionMatrix` `GeneratorPipeline` `DataList` `Timeline` `TimelineItem` `ActivityList` `ShareList` `Descriptions` `BentoGrid` `ShortcutGrid`。**新增列表只要把容器选择器加进这组即可，不用改组件。**

判据：只对「一条一条进来」的容器生效。卡片、面板这类单件不加——它们不是列表，逐条落下没有语义。

### 通用语式二：选中强调条生长

选中态原来只靠底色变化（缓动，不是形变）。补一处几何变化：左侧 2.5px 强调条**从中心向两端长出**（`scaleY 0 → 1`，0.22s `--ease-swap`）。

覆盖 `.x-menu-item` `.select-option` `.x-cas-option` `.tree-row` `.x-tree-row` —— 五类都是「在一列里选一个」，强调条承担「我选的是这一条」。

两个要点：
- 改 `scaleY` 不改宽高，行内文字不会被推走。
- **`.tree-row` 与 `.x-tree-row` 是两套**：前者属冻结的业务树（DeptTree / PermissionTree），后者属可写的 TreeNode / TreeSelect。只写一个会漏一半——这是实际踩到的坑。

另外纠正一个判断：浮层类的入场**本来就有形变**，不是「改不了」。`overlayEnter` 里 drawer 用共享元素 ghost 从被点的行长成抽屉，modal 从触发点 `scale .86 → 1`，pop 是 `y -6 + scale .98`（很克制）。冻结的是参数微调，不是能力缺失。

### 通用语式三：单件容器上浮 + 纯色块落定

**单件容器**（`.x-card` `.panel` `.spec-plate`）：只做一次 6px 上浮 + 淡入，**不做错位**。它们不是列表，逐条落下没有语义；整页一起落位才是它们该有的读法。

**纯色块**（`.tag` `.x-badge` `.delta-pill`）：出现时 `scale .9 → 1`，0.2s 走 `--ease-settle`（末尾轻微过冲，读作「贴上去了」）。**不用从 0 起**——色块体量小，从 0 长出来会像闪。

实测：卡片 `opacity 0.89→0.96→1`；色块 `scale 0.98→1.01→1`。

**fill-mode 必须用 `backwards`，不能用 `both`**——这是个静默功能回归：`both` 让最后一帧在动画结束后继续生效，而 CSS 动画在层叠里优先于普通声明，于是 `.x-card:hover { transform: translateY(-2px) }` 被压掉，悬停上浮直接失效，页面上只表现为「不浮了」，不报错也不会被守卫抓到。`backwards` 只在开始前补首帧，结束即释放属性。

判据：加完入场动画后**必须复测元素原有的 hover/active 位移还在不在**（悬停前后 `getComputedStyle(el).transform` 是否变化）。

| 批次 | 组件 | 语式 | 结果 |
|---|---|---|---|
| 1 | `Radio` | 落定 + 生长 | ✅ 环 `1→0.89→1`，点 `0→0.86→1.09→1` |
| 1 | `Rate` | 落定 | ✅ 被点的星 `1→0.86→1` |
| 2 | `Steps` | 描线 | ✅ 勾常驻 + `dashoffset 20→3.1→-1.9→0`，数字同步淡出 |
| 3 | `InputTag` | 收拢 | ✅ 宽度 `87→85→72→22→移除` |
| 4 | `Tree` | 展开 | ✅ 子行 `opacity 0→0.35→0.83→1`，逐行 26ms 错位 |
| 4 | `MenuNode` | 展开 | ✅ 子菜单同套语式，24ms 错位 |
| 0 | `Progress` | 收拢 + 描线 | ✅ 条收拢成圆 → 描环 → 画勾 → 回弹 |

**跳过 4 处，都有具体理由（不是漏做）**：

| 组件 | 原因 |
|---|---|
| `Checkbox` | `settlePop` 挂在**常驻包裹 span** 上，本来就正常，不需要改 |
| `Segmented` / `Tabs` | 已有滑块 `x + width` 位移，再叠按压是噪声 |
| `Upload` | 进度条是 `v-if="status==='uploading'"`，状态一变整条卸载，没有「收拢」的余地；要做得先重构列表行 |
| `Alert` / `Notification` | 图标由 `showIcon` 属性驱动、挂载即存在，加入场动效会让一屏提示条同时晃 |
| `Dropdown` / `Popover` / `Drawer` | 入场编排在 `motion.ts` 的 `overlayEnter` 里，而该文件逐字节冻结，改不了 |

---

## 1. 四类形变语式

先定义词表，后面所有设计都从这里取，不再各写各的。

| 语式 | 几何动作 | 参数 | 用在哪 |
|---|---|---|---|
| **收拢 Collapse** | 宽度/高度 → 一个圆，或 → 0 | `--ease-swap` 0.42s | 完成态、关闭态 |
| **描线 Draw** | `stroke-dashoffset` 满 → 0，两笔错位 0.22s | `--ease-reveal` / `--ease-settle` | 勾选、确认、连接 |
| **落定 Settle** | `scale` 1 → 1.06 → 1 | `--ease-settle` | 选中、确认 |
| **展开 Unfold** | 高度/宽度 0 ↔ 1 | `--ease-swap` 0.22s | 折叠、抽屉、出现 |

三拍组合（收拢 → 描环 → 画勾 → 落定）就是登录那颗按钮的完整语法，已封装为 `playCrystallize()`。

---

## 2. 适配判定：三步筛

一个组件能不能做形变，按顺序问：

1. **状态是否改形状**（而非只改颜色）。只换色的，形变无从谈起——那是缓动范畴。
2. **两个状态的元素是否都在 DOM**。`<Icon v-if="checked">` 是个死结：未选中时 SVG 不存在，描线没有起点，只能凭空出现。要做得先把图标改成常驻 + `stroke-dashoffset` 控显隐。
3. **是否可写层**。`extend/` 与 `workspace/` 可自由演进；`ui/` `layout/` `charts/` `business/` 逐字节冻结，只能走覆盖层。

---

## 3. 现状盘点（全库扫描，非估计）

| 指标 | 数量 |
|---|---|
| 组件总数 | 154 |
| 有状态规则（`:hover` / `.is-*`） | 46 |
| 状态里出现几何属性 | 42 |
| 用了 `<Icon v-if>`（描线障碍） | 26 |
| 可写层 / 冻结层 | 95 / 59 |
| **42 个候选里落在可写层的** | **42（全部）** |

**结论**：形变改造不受冻结面限制，42 个候选全在可写层。真正的限制是第 2 条——26 个组件因为 `v-if` 无法做描线。

已有形变（6 处，各写各的）：`Progress`(已完成三拍)、`ConfirmButton`(三拍)、`CollapseItem`(高度)、`Switch`(填充+位移)、`Tabs`/侧栏(滑块 x+width)、`Checkbox`/`Radio`(落定)。

---

## 4. 分批设计

### 批次 1：落定（Settle）——零 DOM 改动，收益最快

已落地 `src/composables/morph.ts`，三个原语：`growIn`（0 → 1 长出）、`pressSettle`（1 → 0.88 → 1 按压）、`morphSelect`（环按压 + 点生长 60ms 错位）。动效期间会临时关掉元素自身的 `transition: transform`，否则 GSAP 每帧写的 inline 值会被 CSS 再插值一次，动作变软。

| 组件 | 形变设计 | 状态 |
|---|---|---|
| `Radio`（可写） | 选中：外环按压 `1→0.89→1` + 圆点 `0→0.86→1.09→1` | ✅ 已落地，**顺带修掉一个死代码**（见下） |
| `Rate`（可写） | 点击：被点的星 `1→0.86→1` 按压落定 | ✅ 已落地 |
| `Checkbox`（冻结） | 方块按压 | ⏭ 跳过：它的 `settlePop` 挂在**常驻包裹 span** 上，本来就正常 |
| `Segmented` / `Tabs` | 选中项轻压 | ⏭ 跳过：两者已有滑块 `x + width` 位移，再叠按压是噪声 |

**顺带修掉的死代码**：`Radio` 原来写的是 `watch(checked, () => settlePop(dot.value))`，但 `dot` 是 `v-if="checked"`，而 `watch` 默认在渲染前触发——那一刻 `dot` 还是 `null`，`settlePop(null)` 静默返回。**实测圆点 scale 恒为 1**，源码注释里「勾上时一次落定弹入」从未生效。修法：`await nextTick()` 再取元素。

判据：`scale` 峰值与回落曲线可见，且相邻元素不位移（用 `transform`，不用宽高）。

### 批次 2：描线（Draw）——需要先把图标改常驻

前置动作：把 `<Icon v-if="done">` 改为常驻 + `stroke-dasharray/offset` 控显隐。这是本批的主要工作量。

| 组件 | 形变设计 |
|---|---|
| `Steps`（可写） | 完成的步骤圆点：勾一笔描出（0.32s `settle`），圆点同时落定 |
| `Upload`（可写） | 单个文件上传成功：状态标签里的勾描出 |
| `Alert` / `Notification`（可写） | 图标入场：描线或落定，替代现在的瞬间出现 |

风险：图标常驻会改变 DOM，需复核可访问名与「零尺寸图标」判据（`DEMO_HEALTH` 会查）。

### 批次 3：收拢（Collapse-to-badge）

| 组件 | 形变设计 | 可行性 |
|---|---|---|
| `Upload`（可写） | 文件上传完成：进度条**收拢成圆**并描勾 | 直接复用 `playCrystallize`（同 `Progress`） |
| `InputTag`（可写） | 删除标签：宽度收拢到 0 + 圆角变圆 + 淡出 | 需父级保留到动画结束（加 `is-closing` 类） |

### 批次 4：展开（Unfold）

| 组件 | 形变设计 | 可行性 |
|---|---|---|
| `Tree` / `TreeNode`（可写） | 展开时子节点 stagger 淡入（每层 30ms），箭头 `rotate` 已具备 | 需给子节点加进场动画 |
| `Dropdown` / `Popover` / `Drawer`（可写/冻结混合） | 从触发点 `scale(.96) → 1` 展开 | `lastPointer` 已有触发点记录，`overlayEnter` 已有入场 |

---

## 5. 明确不做

| 对象 | 原因 |
|---|---|
| `Tag` 关闭形变 | 组件本身**没有关闭按钮**，也没有 `Transition` 包装。做形变要先加按钮 + 改所有调用方用法，改动面远超形变本身。 |
| 约 112 个纯换色组件 | 它们的状态只改颜色，加形变等于**重新设计状态表达**，不是本轮任务。 |
| 图形类（`.rg-*` / `.heat-*` / `.org-*`） | 上一轮已确认：状态是变色 / 变透明。给画布加位移会干扰读图。 |

---

## 6. 验收标准

每个形变必须过三关，缺一不可：

1. **逐帧有中间值**。宽度、`scale`、`dashoffset` 三件套至少一项在 t=25%/50% 处既不等于起点也不等于终点。只看首尾两帧证明不了是渐变。
2. **不产生布局位移**。优先 `transform`；必须改宽高时，确认相邻元素没有被推走。
3. **双主题守卫零命中**。`DEMO_HEALTH` 浅色 + 暗色各 101 页。

手感复核用 `../references/motion-compare.html`——把形变也做进去，左右对照。

---

## 7. 风险

| 风险 | 处置 |
|---|---|
| 形变触发重排，列表整体抖动 | 优先 `transform` / `opacity`；确实要改宽高时限制在独立容器内 |
| 图标改常驻后读屏多念一遍 | 常驻图标加 `aria-hidden`，可访问名留在父级 |
| 冻结组件只能走 keyframes，参数不可调 | 只对「落定」这类短促动效用 keyframes；需要编排的走本地新增组件 |
| 形变被误当装饰 | 每个形变必须能说出对应哪种语式，说不出就不做 |

---

## 8. 工作量与顺序

批次 1 最小（纯 transform，零 DOM 改动），建议先做并把三拍语式固化成 `morph.ts` 工具；批次 2 是主要工作量（26 个 `v-if` 里挑 3 个改）；批次 3、4 各含一处结构改动。

顺序不可颠倒：**先批次 1 验证语式与参数，再动 DOM 做描线**。若批次 1 做完发现形变在小控件上过火，回退成本远低于改完 DOM 再退。
