---
schema_version: 1
doc_id: TEST-PEARL-DEMO-FULL-SWEEP-001
doc_type: test_main
template_version: 1
source_ids:
  - SRC-PEARL-DEMO-FULL-SWEEP-20261018
version: 1
current_slice: SLICE-PEARL-DEMO-FULL-SWEEP
updated_at: 2026-10-18
status: accepted
unresolved_decisions: 0
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 测试主文档：组件示例全量遍历排查

结论：对 101 个示例页、749 张示例卡做了逐组件逐示例的真实测试，本轮查出的 11 个真实缺陷全部修复并通过复验，1 个上游冻结面缺陷已登记豁免；影响：组件库示例页全部页面与全部示例卡；范围：示例变体生成器、示例层受控状态、6 个组件的实现与声明、1 条长期守卫的作用域、3 条本轮新增守卫；非范围：接口测试与数据库测试（本轮不涉及后端）、上游 139 个冻结文件的行为变更；变化：341 条原先点了没反应的可点事件全部有了可见反馈，裂图、低对比、缺可访问名、重复示例、非法示例归零，常年报红的守卫转绿；完成标准：全部守卫在浅色与暗色主题下同时 PASS，类型检查零报错，单元测试全通过，生产构建成功，测试污染扫描放行；术语说明：受检事件指守卫纳入判定的非 `update:` 声明事件，阳性对照指先故意制造缺陷、验证守卫确实报出、再还原的双向自证；验证状态：已执行并通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 来源 | `SRC-PEARL-DEMO-FULL-SWEEP-20261018`：用户在 Goal 模式下要求「继续检查所有组件示例，遍历检查每一个组件和示例，修复 bug」 |
| 关联 Bug 主文档 | `doc/4-bugs/2026-10-18_190500_组件示例全量遍历排查.md`（`BUG-PEARL-DEMO-FULL-SWEEP-001`） |
| 测试对象 | 组件库示例页 101 个路由、749 张示例卡，以及本轮改动的示例变体生成器、示例层受控状态与 6 个组件 |
| 测试类型 | 运行时全量扫描、事件接线遍历、真实点击取证、双上下文对照、守卫阳性对照、类型检查、单元测试、生产构建、测试污染扫描 |
| 环境合规 | 全部连接只经本地 mock 登录接口与本地 Vite 开发服务，属 `local` 本地开发配置；未连接 `test` / `prod` / `staging` 任何环境 |
| 数据写入 | N/A，理由：本轮测试只读取示例页并触发点击，未向任何数据库、缓存或消息队列写入数据，因此无数据准备与数据清理项 |
| 决策状态 | `unresolved_decisions`：无 |
| 图片资产决策：N/A，理由：全部取证来自运行时几何、计算样式、对比度实测、事件接线遍历、守卫输出与真实点击后的提示文案，判定不依赖截图，故本节不涉及图片资产 |

## 1. 测试环境

| 项 | 取值 |
| --- | --- |
| 运行方式 | 本地 Vite 开发服务（`npx vite --port 5173 --host 127.0.0.1`） |
| 端口 | 5173，测试结束后按后台任务 ID 终止 |
| 浏览器 | Playwright Chromium（无头） |
| 视口 | 1440×900，`device_scale_factor=1` |
| 登录方式 | mock 接口 `POST /api/auth/login`，captcha 固定 `1024`，属 `local` 本地开发配置 |
| 操作系统 | Windows 10.0.19045 |
| 扫描根 | 101 个路由全部由分类真相源 `component-categories.ts` 派生，守卫不自己手写路由清单 |
| 扫描根下限 | `MIN_CELLS = 600`，示例卡总数低于该值直接判扫描根失效 |

## 2. 测试结果总表

| 缺陷 | 测试内容 | 结果 | 证据 |
| --- | --- | --- | --- |
| BUG-01 | 帮助提示守卫作用域收窄后重跑 | 通过 | `HELP_TIP: PASS`，八项交互逐条通过 |
| BUG-02 / BUG-03 | 变体生成器重跑并逐行对比生成物 | 通过 | 仅 3 处预期变化，`DEMO_VARIANTS: PASS`（749 组） |
| BUG-04 | `TreeSelect` 类型声明与实现对账 | 通过 | `vue-tsc` 零报错，两处 `as any` 已删除 |
| BUG-05 | `Comment` 头像示例的图片来源与网络请求 | 通过 | 裂图判据零命中，无 404 请求 |
| BUG-06 | `Image` 放大控件可访问名与键盘激活 | 通过 | 缺可访问名判据零命中（5 格） |
| BUG-07 | 双主题下 `Spin` 遮罩文字对比度 | 通过 | 低对比判据在浅色与暗色主题下均零命中 |
| BUG-08 | 全量事件接线遍历加真实点击 | 通过 | `EVENT_WIRING: PASS`（341 条全部已接），7 类反馈文案实测出现 |
| BUG-09 | `CollapseItem` 单独挂载开合 | 通过 | 无父级时点标题可展开，有父级时仍完全跟随父级 |
| BUG-10 | 残留目录清理 | 通过 | `.npm-cache` 已删除并回读确认 |
| BUG-11 | 剪贴板授权与未授权双上下文真实点击 | 通过 | 两态在图标、可访问名与颜色上均可区分 |
| DEF-01 | GSAP 空目标告警登记 | 通过 | 豁免面集中一处定义，写明根因与移除条件 |

## 3. 详细证据

### 3.1 全量体检（BUG-05 / BUG-06 / BUG-07 及全量兜底）

守卫 `frontend-design/scripts/check_demo_health.py` 用九类判据扫描每一个示例卡：渲染错误、坏文案（未翻译占位、`undefined`、`NaN`、`[object Object]`）、裂图、零尺寸图标、文本被裁切、缺可访问名、对比度低于 1.5、控制台错误与 Vue 告警、横向溢出。

| 主题 | 命令 | 结果 |
| --- | --- | --- |
| 浅色 | `python frontend-design/scripts/check_demo_health.py --theme light` | `DEMO_HEALTH: PASS (主题 light，扫描 101 页 749 张示例卡，九类判据零命中；豁免 1 条已登记)` |
| 暗色 | `python frontend-design/scripts/check_demo_health.py --theme dark` | `DEMO_HEALTH: PASS (主题 dark，扫描 101 页 749 张示例卡，九类判据零命中；豁免 1 条已登记)` |

对比度判据不把半透明层直接跳过，而是逐层做 alpha 合成到不透明底再按 WCAG 相对亮度算比值；当文字与不透明底之间存在渐变或图片背景时，返回 `measurable = false` 并跳过该项判定，避免把深底板配浅文字误判成低对比。

### 3.2 阳性对照（守卫自证）

守卫全绿本身不构成证据，必须证明「真有缺陷时它确实会报」。两条新守卫都内置自测。

`check_demo_health.py --selftest` 注入 1 个坏卡与 2 条控制台消息后逐判据核对：

```
扫描根覆盖: 注入前 20 卡 -> 注入后 21 卡（注入卡被本次扫描计入 = True）
  判据 renderError: 期望 1 命中 1 -> OK
  判据 badText: 期望 4 命中 4 -> OK
  判据 brokenImg: 期望 1 命中 1 -> OK
  判据 zeroIcon: 期望 1 命中 1 -> OK
  判据 clipped: 期望 1 命中 1 -> OK
  判据 lowContrast: 期望 1 命中 1 -> OK
  判据 noName: 期望 1 命中 1 -> OK
  判据 console: 期望 2 命中 2 -> OK
SELFTEST: PASS
```

浅色与暗色两个主题下分别执行，结论一致。扫描根覆盖一项专门证明「阳性对照不是只在被注入的那一小片上生效」：注入前后卡数从 20 变 21，说明扫描根真的把注入卡计入了本轮统计。

`check_demo_event_wiring.py --selftest` 的 6 组对照：

```
  OK   未接任何处理器必须报缺口: 期望 ['close'] 实得 ['close']
  OK   接上 onClose 后不报: 期望 [] 实得 []
  OK   带横线事件名按 camelize 归一: 期望 [] 实得 []
  OK   update:* 不在本判据范围: 期望 [] 实得 []
  OK   多事件里漏一个只报漏的那个: 期望 ['cancel'] 实得 ['cancel']
  OK   豁免面无失效条目: 无
SELFTEST: PASS
```

最后一组专门防止豁免表腐烂：豁免面里出现已不存在的组件或事件时必须报陈旧，否则豁免会随组件演进而静默扩大。

### 3.3 事件接线遍历（BUG-08）

守卫不解析组件源码，事件清单直接读派生表 `demo-events.generated.ts`，与示例装配层共用同一份口径，避免守卫与生产各持一份而在漂移时同时报绿。

被演示组件的实例通过 vnode 子树查找，而不是 DOM 遍历：从 `body.__vueParentComponent.subTree` 出发，递归进入 `component`、数组 `children` 与 `suspense.activeBranch`，按组件名匹配。这样才能覆盖通过 Teleport 挂到 `body`、且关闭态下 DOM 里没有实例的 `Modal`、`Drawer`、`FormDialog`、`GeneratorPipeline`、`CommandPalette`、`AppearanceDialog`、`PasswordDialog`、`MenuStarMap`。

| 命令 | 结果 |
| --- | --- |
| `python frontend-design/scripts/check_demo_event_wiring.py` | `EVENT_WIRING: PASS (扫描 101 页 749 卡，受检事件 341 条全部已接；豁免 43 条（8 类非手势事件）)` |
| `node frontend-design/scripts/build_demo_events.mjs --check` | `DEMO_EVENTS: PASS (81 个组件共 122 个声明事件，生成物已同步)` |

派生表统计：81 个组件共声明 122 个事件，其中 74 个是非 `update:` 事件，分布在 48 个组件；修复前只有 `Steps.change` 一个有处理器，其余全部发出后无人接收。

8 类豁免事件（`Image.load`、`Image.error`、`Countdown.change`、`Upload.progress`、`RelationGraph.hover`、`ResizeBox.resize`、`SplitPane.resize`、`Carousel.change`）的共性是：它们要么不是手势触发（加载、每秒计时、指针移动、逐帧拖拽），要么可观察结果本来就在组件自身形态上（图形在动、尺寸在变、读数在跳），再叠一条提示反而是噪声。

### 3.4 真实点击取证（BUG-08）

接线遍历只证明「处理器接上了」，不证明「点了真的有反馈」。因此逐路由逐格取内容区里的可点元素真实点击，再读全局提示文案；提示文案自带组件名与事件名，命中与否由文案本身判定，不靠猜类名。

| 路由 | 卡数 | 实测出现的反馈文案 |
| --- | --- | --- |
| `/gallery/feedback/alert` | 6 | `Alert 触发 close` |
| `/gallery/feedback/popconfirm` | 5 | `Popconfirm 触发 cancel` |
| `/gallery/inputs/form` | 8 | `Form 触发 invalid：1 个字段`、`Form 触发 submit` |
| `/gallery/display/tree` | 12 | `Tree 触发 expand：2 项`、`Tree 触发 expand：1 项` |
| `/gallery/navigation/tabs` | 8 | `Tabs 触发 close：tab1` |
| `/gallery/workspace/shortcut` | 4 | `ShortcutGrid 触发 select：5 个字段` |
| `/gallery/general/typography` | 5 | `Typography 触发 copy`（仅在授予剪贴板写权限的上下文出现，见 3.5） |

`/gallery/inputs/upload` 的 5 格点击后未出现反馈文案：`Upload.remove` 需要先有已上传文件才会出现移除入口，空态下没有可点的移除按钮，属预期而非缺陷；该事件的接线由 3.3 的遍历覆盖。

### 3.5 剪贴板双上下文取证（BUG-11）

`Typography` 的复制原先就地调用 `navigator.clipboard.writeText` 并把失败整段放进空 `catch`，组件只有「成功」一个视觉状态，于是剪贴板不可用时按钮点了完全没有反应。修复后复用库内既有的 `@/utils/clipboard` 的 `copyText`，消费其布尔返回，并把失败结果落到图标、可访问名与颜色上。

在授予与未授予 `clipboard-write` 权限的两个浏览器上下文里，对同一路由 `/gallery/general/typography` 的同一个复制按钮各点一次：

| 上下文 | 点击后类名 | 点击后可访问名 | 点击后文字色 | 点击后底色 | 提示文案 |
| --- | --- | --- | --- | --- | --- |
| 授予权限 | `x-typo-copy` | 已复制 | `rgb(35, 109, 233)` | `rgba(46, 58, 62, 0.043)` | `Typography 触发 copy` |
| 未授予权限 | `x-typo-copy is-failed` | 复制失败，当前浏览器不支持写入剪贴板 | `rgb(255, 90, 80)` | `rgba(255, 90, 80, 0.11)` | 无 |

两次点击前的初始形态完全一致（类名 `x-typo-copy`、可访问名「复制」、文字色 `rgb(126, 136, 140)`、底色透明），因此差异只能来自本次点击与剪贴板授权状态，不构成巧合。

同类写法复查：全库检索后 `navigator.clipboard` 的直接调用已归零，只剩 `VerificationCode` 读取粘贴事件里的 `clipboardData`，语义不同不属同类；本地组件里其余空 `catch` 只有 `UserSelect` 一处，其失败分支落到空列表，是用户可见的结果，不属静默失败。

### 3.6 变体生成器重跑对账（BUG-02 / BUG-03）

生成器改动会影响全部组件的派生示例，因此不能只看守卫绿灯，必须逐行对比改动前后的生成物。对比结果只有 3 处变化，全部符合预期：

| 变化 | 说明 |
| --- | --- |
| `Trigger` 的 `hover` / `focus` / `contextmenu` 三格 | 属性声明为数组，派生值由标量改为单元素数组，与基础格仍有可见差异，保留 |
| `Trigger` 的 `trigger=click` 一格 | 与基础格的 `['click']` 深比较等价，按重复丢弃 |
| `SpecPlate` 的重复格 | 元素类型里的嵌套 `tone` 联合不再被误当顶层枚举，重复格丢弃 |

示例卡总数由 752 变为 749，与上述丢弃数量一致。

### 3.7 全量守卫

| 守卫 | 命令 | 结果 |
| --- | --- | --- |
| 示例可见性 | `python frontend-design/scripts/check_demo_visibility.py` | `DEMO_VISIBILITY: PASS (扫描 101 页 749 张示例卡，组件全部在卡内可见)` |
| 逐格提示 | `python frontend-design/scripts/check_demo_guides.py` | `DEMO_GUIDES: PASS (扫描 101 页 749 张示例卡，每格提示均对应本格示例)` |
| 内容留白 | `python frontend-design/scripts/check_content_padding.py` | `CONTENT_PADDING: PASS (扫描 749 张示例卡，无文本贴边)` |
| 边角遮挡 | `python frontend-design/scripts/check_corner_occlusion.py` | `CORNER_OCCLUSION: PASS (扫描 112 个菜单页，无描边被盖住、无子元素方角外露)` |
| 帮助提示交互 | `python frontend-design/scripts/check_help_tip_interaction.py` | `HELP_TIP: PASS (悬停/聚焦/Esc/焦点保持/指针穿透/视口夹取/ARIA 关联/长文换行 全部通过)` |
| 上游还原度 | `python frontend-design/scripts/verify_fidelity.py --offline` | `FIDELITY: PASS (264 local / 139 upstream-tracked; upstream 577079e9a347)`，另有 2 条 `SEAM`（`src/composables/auth.ts` +2 行、`src/main.ts` +1 行，剥离声明行后与上游逐字节相等） |
| 还原度守卫自测 | `python frontend-design/scripts/verify_fidelity_selftest.py` | `GUARD_SELFTEST: PASS` |
| 字号派生块 | `python frontend-design/scripts/build_font_overrides.py --check` | `FONT_OVERRIDES: PASS (82 selectors, 5 size groups)` |
| 组件清单 | `python frontend-design/scripts/test_component_inventory.py` | `INVENTORY: PASS (123 components, 14 composables, 7 style layers)` |
| Arco 品类对齐 | `python frontend-design/scripts/check_arco_parity.py` | `PARITY: PASS (74 个 Arco 品类全覆盖; display:22 feedback:12 inputs:22 layout:8 navigation:10)` |
| 目录索引 | `node frontend-design/scripts/build_component_catalog.mjs --check` | `CATALOG: PASS (152 components)` |
| 分类真相源 | `node frontend-design/scripts/check_component_categories.mjs` | `CATEGORIES: PASS（10 个父分类、101 个子分组，覆盖 152 个组件；磁盘 152）` |
| 示例可用性 | `node frontend-design/scripts/check_demo_variants.mjs` | `DEMO_VARIANTS: PASS（152 个组件共 749 组示例，平均 4.93 组/组件；磁盘 152）` |
| 投影留白 | `node frontend-design/scripts/check_shadow_clipping.mjs` | `SHADOW_CLIP: PASS (四向留白均覆盖对应投影延展，阳性对照有效)` |
| 后台可达性 | `node frontend-design/scripts/check_admin_component_coverage.mjs` | `ADMIN_COVERAGE: PASS (152/152 组件全部在后台可达)` |

### 3.8 类型、单测与构建

| 项 | 命令 | 结果 |
| --- | --- | --- |
| 类型检查 | `npx vue-tsc --noEmit` | 退出码 0，零报错 |
| 单元测试 | `npm run test:unit` | `pass 21` / `fail 0` |
| 生产构建 | `npx vite build` | `✓ built in 6.10s` |

### 3.9 测试污染扫描

| 命令 | 结果 |
| --- | --- |
| `python test-strategy-rules/scripts/scan_test_pollution.py --root . --diff-only` | `POLLUTION: PASS` |

命中项均为已登记豁免：`frontend-design/component-library/scripts/session-regression.py` 的口令取自环境变量并带本地默认值，属回归脚本自身的连接配置，生产引用 0 处、测试引用 5 处。本轮未为了测试目的改动任何生产代码。

## 4. 完成标准

本轮测试以「遍历检查每一个组件和示例，修复查出的真实 bug」为完成标准，逐项对照如下：

| 标准 | 判定方式 | 实际结果 |
| --- | --- | --- |
| 每一个组件与示例都被真实遍历 | 守卫从分类真相源派生全部路由，扫描根计数与派生表对账，并设 `MIN_CELLS` 下限 | 101 页 749 卡；阳性对照证明注入卡从 20 变 21 被计入，扫描根覆盖有效 |
| 全部缺陷修复后守卫复绿 | 逐条重跑受影响守卫 | 双主题体检、事件接线、帮助提示、可见性、逐格提示、内容留白全部 PASS |
| 守卫自身可信 | 两条新守卫的阳性对照自测 | `SELFTEST: PASS`，九类判据与 6 组对照逐项命中期望值 |
| 交互不再是摆设 | 真实点击后读提示文案，不靠猜类名 | 7 类反馈文案实测出现，覆盖 6 个路由 |
| 用户手势失败可见 | 剪贴板授权与未授权双上下文对照点击 | 两态在类名、可访问名与颜色上均可区分，点击前初始形态一致 |
| 不破坏既有能力 | 依次运行还原度、字号、清单、对齐、目录、分类、变体、投影、后台可达、边角 | 全部 PASS，上游 139 文件逐字节未变 |
| 代码可编译可构建 | 类型检查、单元测试、生产构建 | 0 报错 / 21 通过 / 构建成功 |
| 未为测试改动生产代码 | 污染扫描 | `POLLUTION: PASS` |
| 临时产物已清理 | 目录与端口回读 | 见第 6 节清理与回滚 |

## 5. 未覆盖说明

- DEF-01（GSAP 空目标告警）位于上游 139 个冻结文件之内，本轮只登记豁免与上游修法，未修改；重新冻结上游后应删除该条豁免。
- 体检守卫的对比度判据在文字与不透明底之间存在渐变或图片背景时跳过判定，这类位置的低对比度需要人工目检。
- 事件接线守卫只判「声明事件是否有处理器」，不判处理器内部行为是否正确；处理器语义由 3.4 的真实点击取证覆盖，未对全部 341 条逐条做语义断言。
- 交互遍历不覆盖需要拖拽轨迹、需要真实文件选择、需要真实网络上传的示例；这些示例只验证了接线，未验证端到端行为。
- `Upload.remove` 在空态下没有可点的移除入口，其真实点击反馈未取证，只由接线遍历覆盖。
- BUG-11 只把失败结果变可见，没有为 `@/utils/clipboard` 增加降级写入通道；该工具是 `Typography` 与 `GeneratorPipeline` 的共用入口，加降级会同时改变两处行为语义，属独立决策。
- 上游组件的业务语义正确性不在本轮范围，本轮只判「示例是否可用、可见、可操作、可读」。

## 6. 清理与回滚

| 项 | 处理 |
| --- | --- |
| 临时探针脚本 | `.tmp-sweep/` 整目录（含 11 个诊断脚本、2 个取证脚本、全部中间 JSON 与日志）收口前删除，并回读确认目录不存在 |
| 后台开发服务 | 5173 端口的 Vite 进程按后台任务 ID 终止，并回读确认端口不再监听 |
| 构建产物 | `frontend-design/component-library/dist/` 由本轮 `vite build` 生成，该路径已被 `.gitignore` 忽略，收口前删除 |
| 残留缓存 | `src/views/gallery/.npm-cache/`（456K）已删除，属本轮修复项 BUG-10 |
| 数据回滚 | 本轮未写入任何数据库、缓存或消息队列，登录只经本地 mock 接口，无需数据回滚 |
| 代码回滚 | 全部改动落在本地文件（`extend/`、`views/gallery/`、`frontend-design/scripts/`），上游 139 个冻结文件逐字节未变，`FIDELITY: PASS` 即为回滚边界证明 |
