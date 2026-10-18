---
name: frontend-design
description: 创建具有鲜明风格、达到生产级质量的高品质前端界面。当用户要求构建 Web 组件、页面、前端应用，或进行前端 UI、组件、样式的调整/改进/界面 Bug 修复时优先使用这个 skill。中后台/管理端 design 默认使用珍珠玻璃组件库（152 个 Vue 组件 + 七层令牌样式，字节级还原基线守卫，附组件目录索引；全部组件的用法示例内置在后台路由 /gallery 内，共 749 组可操作示例、平均每个组件 4.93 组，按「父分类 + 子组件分类」两级菜单导航 10 个父分类 / 101 个单一概念子分组，示例页宽屏一行 3 格大卡，品类广度对齐 Arco Design Vue），选组件前先查 references/component-catalog.md。它会生成有创意、打磨精细的代码，并避免出现千篇一律的 AI 模板化审美。触发词：前端设计、页面设计、UI 设计、组件设计、界面样式、前端审美、网页设计、设计风格、组件库、珍珠玻璃、后台管理界面、中后台、管理端、组件目录、组件索引、找组件、组件示例、组件菜单、示例分组、多变体示例、字体加载失败、字体乱码、tofu、@fontsource、字体子集、文字显示不全。
license: Complete terms in LICENSE.txt
metadata:
  version: "2.2.0"
---

这个 skill 用于指导构建具有鲜明风格、达到生产级质量的前端界面，并避免出现通用化的“AI 味”审美。实现时要输出真实可运行的代码，并且在审美细节与创意选择上保持极高关注。

用户会提供前端需求，例如要构建一个组件、页面、应用或界面。用户也可能同时提供用途、受众或技术约束等上下文。

## 默认组件库：珍珠玻璃（中后台场景强制入口）

本 skill 内置一套完整的**珍珠玻璃组件库**（`component-library/`），来源：[scaffold-master](https://github.com/wbr664393425-lgtm/scaffold-master) `scaffold-vue`，上游冻结 commit `577079e9a347555fadddd3865fc0bbcdb00d9fb4`，MIT License（GSAP 为其自有许可，不在 MIT 内）。

**路由规则**：当用户要求 design 的页面属于**中后台 / 管理端 / 数据面板 / 系统管理类**（列表页、表单、工作台、看板、权限矩阵、日志监控等），**默认走本组件库**，从库中选组件组装页面，不从零手写样式；用户明确要求其它风格或非中后台场景（营销页、着陆页、移动端 H5 等）时，走下方通用审美工作流。

### 组件库结构（七层样式 + 六类组件目录）

| 层 | 位置 | 内容 |
| --- | --- | --- |
| 基础控件 | `component-library/src/components/ui/` | 27 个：Button/IconButton/TextInput/Select/Checkbox/Switch/Segmented/Tag/StatusTag/Avatar/Panel/DataTable/Pagination/Modal/Drawer/Field/EmptyState/Metric/Odometer/SectionLabel/SpecPlate/DeltaPill/Ruler/HoverCard/PageHeader/ToastHost/ConfirmHost |
| 业务组件 | `component-library/src/components/business/` | 20 个：ListPage/FormDialog/SearchForm/BoardView/PermissionMatrix/PermissionTree/PermissionTrace/MenuStarMap/OrgCanvas/PostLadder/DictSwatchbook/DictTag/DictSelect/DeptTree/DeptSelect/UserSelect/GeneratorPipeline/InsightPanel/AskDock/PermissionButton |
| 工作台版式 | `component-library/src/components/workspace/` | 8 个（本地扩展）：BentoGrid/BentoCard/Band/ReadoutStrip/KeyValueReadout/ShareList/ActivityList/ShortcutGrid |
| Arco 品类对齐 | `component-library/src/components/extend/` | 本地扩展 82 个：把品类广度补齐到 Arco Design Vue 同等水平（Tabs/Steps/Upload/Tooltip/Dropdown/TreeSelect/Transfer/DatePicker/Calendar/Timeline/Watermark/InputPassword/Descriptions/Form/Textarea…），**品类**覆盖状态见 `references/arco-parity.json`（74 品类）+ `references/arco-categories.json`，**组件粒度**覆盖状态见 `references/arco-component-parity.json`（131 导出名）+ `references/arco-components.json` |
| 自研图表 | `component-library/src/components/charts/` | 6 个：TrendChart/BarChart/TickRing/HeatGrid/Swimlane/RelationGraph（零图表库） |
| 外壳 | `component-library/src/components/layout/` | 6 个：AppShell/Sidebar/Topbar/CommandPalette/AppearanceDialog/PasswordDialog |
| 根级 | `component-library/src/components/` | 2 个：Icon/NeuralNet |
| 样式七层 | `component-library/src/styles/` | tokens → base → materials → components → instruments → layout → pages（严格按此顺序引入） |
| 动效 | `component-library/src/composables/motion.ts` | 唯一动效入口（GSAP）：EASE/DUR 令牌、spring、createFrameLoop、revealCascade 等 |

> `workspace/` 与 `extend/` 都是本仓库的**本地扩展层**（不属于上游 61 个组件，不参与还原度基线）。`workspace/` 把工作台页面里只以 `pages.css` 类名存在的版式词汇固化为组件；`extend/` 用于品类广度对齐——组件样式写在自身 `<style scoped>` 内、只引用 `tokens.css` 令牌，材质复用 `.m-*`、动效复用 `composables/motion.ts`，因而不需要改动冻结的七层样式与 `src/main.ts`。

### 组件目录索引（一键查找，优先读这个）

**选组件前先查 `references/component-catalog.md`**：它由 `scripts/build_component_catalog.mjs` 从组件源码自动生成（含全部组件的引入路径、必填 props、类型字面量、默认值、事件、插槽、导出类型、用法骨架与参考实现位置），是"组件名 → 怎么用"的唯一速查入口；机器可读版本为 `references/component-catalog.json`。

- 查组件：在 `component-catalog.md` 的「速查表」按名称 / 分类 / 物理目录 / 必填 props 定位，再读同文件的「组件契约」取完整 props 与用法骨架。
- 语义分类：分类真相源在 `component-library/src/data/component-categories.ts`（对齐 Arco 组件菜单，两级结构：10 个父分类 → 101 个单一概念子分组（不使用「A与B」复合命名），声明数据分放 `component-categories.basic.ts` / `.data.ts` / `.extended.ts`，组装文件只做派生索引）。示例页侧栏导航、菜单种子与目录索引的「分类」列都由它驱动；新增/删除组件必须同步对应分域文件，收口前跑 `node frontend-design/scripts/check_component_categories.mjs`（必须 `CATEGORIES: PASS`：每个磁盘组件恰好归入一个子分组一次，无遗漏无幽灵，父分类数不低于 8、子分组不为空、子分组键唯一、图标名均已注册；守卫直接 import 分类模块，不重解析源文件结构）。
- 人工核对全部组件真实渲染：登录后台后进入「组件库」分组（`/gallery/<父分类键>/<子分组键>`，101 个子分组各一条路由；父分类是不可点的目录节点，面包屑对不可路由层级只渲染文本），逐卡显示组件名、变体标签、仓库内路径与挂载状态；一个组件多组示例，props 与插槽样本由 `src/views/gallery/demo-*.ts` 与 `demo-variants.curated-*.ts` 提供，派生样本由 `scripts/build_demo_variants.mjs` 从组件契约生成。示例卡片内容超出时走限高滚动而不是裁切，窄窗口不丢样式。示例页本身也是后台页面，使用真实壳层与真实路由，不再有独立 html 入口。
- 示例可用性收口：`node frontend-design/scripts/check_demo_variants.mjs` → 必须 `DEMO_VARIANTS: PASS`（每个组件含基础示例 ≥3 组，单一可覆盖维度的契约组件降档到 1 组并逐个点名；每组示例必须与同组件其它示例有可见差异，只在打开态才可见的差异不得计为重复，须在浏览器点开实测或登记为不可见候选）。
- 契约变化后重跑：`node scripts/build_component_catalog.mjs`（生成）/ `--check`（校验索引与磁盘是否同步，签名含分类，分类漂移即 STALE）。


### 中后台 design 工作流（第 3 步的展开）

1. **运行组件库**：`cd component-library && npm install && npm run dev`（内置 mock，零后端可跑，登录页任意账号可进），到 `http://localhost:5173` 实际查看组件真实视觉与动效。
2. **选组件组装**：先查 `references/component-catalog.md` 速查表（名称 / 分组 / 必填 props / 引入路径），再读同文件的组件契约取完整 props、事件、插槽与用法骨架——列表页用 `ListPage` + `DataTable` + `SearchForm`；表单用 `FormDialog` + `Field` + `TextInput`/`Select`/`Switch`；概览读数用 `Metric`/`Odometer`/`SpecPlate`/`DeltaPill`；工作台主次布局用 `workspace/` 的 `BentoGrid` + `BentoCard`，横带分区用 `Band` + `ReadoutStrip`，构成类用 `ShareList`，流水用 `ActivityList`，入口宫格用 `ShortcutGrid`；分区标题用 `SectionLabel`；图表放 `charts/` 对应组件。**新页面不另写一套按钮/表格/弹窗/筛选/卡片布局**，页面只补业务差异。
3. **遵守七层样式纪律**：通用变化写入所属样式层；页面只引用 `tokens.css` 令牌，不手写颜色/圆角/阴影取值；玻璃材质只挂 `m-rail/m-pill/m-float/m-surface/m-groove` 工具类；动效一律 import `composables/motion.ts` 原语，不复制 GSAP 配方。
4. **参考实现**：`component-library/src/views/` 下 15 个页面（Users/Roles/Menus/Depts/Posts/Dict/Configs/OperLog/LoginLog/Generator/Dashboard/Login）是组件组合的权威范例，新页面照其结构组装。
5. **设计规范**：视觉语言、令牌表、版式清单、动效四语态（放/导/结/停摆）、性能红线见 `component-library/DESIGN.md`。

### 还原度守卫（强制）

- 参照物唯一来自上游 `git cat-file blob` 取回的**对象库原始字节**，不受本机 `core.autocrlf` 与工作树换行展平影响；`references/component-library-baseline.json` 只能由联网模式（`--write-baseline`）生成并带防篡改指纹，离线模式拒绝非上游派生或指纹失配的基线（防止用本地文件自证）。
- 每次涉及组件库的改动收口前运行：
  - `python frontend-design/scripts/verify_fidelity.py`（联网权威）或 `--offline` → 必须 `FIDELITY: PASS`（上游 61 组件与七层样式逐字节一致；`workspace/`、`extend/`、`mock/`、`src/views/gallery/` 等本地新增只记 `LOCAL_ONLY`；`src/composables/auth.ts` 的登记缝隙记 `SEAM`，剥离声明行后必须与上游逐字节相等）
  - `python frontend-design/scripts/verify_fidelity_selftest.py` → 必须 `GUARD_SELFTEST: PASS`（反向变异：本地漂移/缺失/CRLF、基线篡改/自证派生都必须被抓到）
  - `python frontend-design/scripts/test_component_inventory.py` → 必须 `INVENTORY: PASS`（上游 61 + 本地 workspace 8 + extend 品类对齐层，含 barrel 导出契约；extend 名单由 `references/arco-parity.json` 动态派生）
  - `python frontend-design/scripts/check_arco_parity.py` → 必须 `PARITY: PASS`（品类粒度三重校验：`DANGLING` 标 covered 但组件缺失、`STALE_GAP` 标 gap 却已实现、`PHANTOM_CATEGORY`/`MISSING_CATEGORY` 与真实 Arco 品类对不上）
  - `python frontend-design/scripts/check_arco_component_parity.py` → 必须 `COMPONENT_PARITY: PASS`（**组件粒度**校验：`arco-parity.json` 只对齐到 74 个品类目录，而 Arco 实际对外导出 131 个组件名（含 Col/Row、InputSearch、RangePicker、MonthPicker 等子组件）；本守卫逐条校验 `references/arco-component-parity.json` 的 `kind`（covered 有独立实现 / merged 由已有组件配置或插槽覆盖 / gap 真实缺口），`gap` 必须清零）
  - 两份 Arco 真相源均从 npm 包 `@arco-design/web-vue@2.58.0` 的 `es/index.js` 派生、文件内 `extract_command` 可复现重建：`references/arco-categories.json`（74 个品类目录）与 `references/arco-components.json`（131 个导出组件名）；不手抄清单
  - `node frontend-design/scripts/check_component_categories.mjs` → 必须 `CATEGORIES: PASS`（分类真相源 `component-categories.ts` 与磁盘 `.vue` 双向对账：覆盖、唯一、无幽灵、分类数≥8；直接 import 生产模块，不重解析源文件，源文件结构漂移即判失败）
  - `node frontend-design/scripts/build_component_catalog.mjs --check` → 必须 `CATALOG: PASS`（组件契约与目录索引同步，签名含分类，分类漂移即 STALE）
  - `node frontend-design/scripts/check_admin_component_coverage.mjs` → 必须 `ADMIN_COVERAGE: PASS`（后台组件覆盖率：以 `src/views/**` + `src/App.vue` + `src/router/**` 为入口做真实 import/模板引用闭包，152 个组件必须全部可达；只 import 不渲染不计入，防止一行批量导入刷满覆盖率；`import.meta.glob` 按实际匹配集计入，变异自测已验证收窄 glob 会真实掉覆盖率）
  - `node frontend-design/scripts/check_shadow_clipping.mjs` → 必须 `SHADOW_CLIP: PASS`（投影留白守卫：从源码解析全部非内阴影层的四向延展（`left = blur/2 + spread − ox` 等，`var()` 当场展开），与外壳 `.stage`、示例卡 `.g-cell-body`、登录页 `.login` 三个容器的四向留白逐维比对；留白不足会被 `overflow: clip` 的裁切边切成方形暗块。卡内预算排除 `pages.css`/`layout.css`（页面级与外壳级投影各有承接方）。判据全部由源码推导不写死数字，内置阳性对照：把三个落点（`.stage`、`.g-cell-body`、`.login`）的留白清零后，必须逐落点四向全部报缺（共 12 条），少一条即判守卫自身失效）
  - `python frontend-design/scripts/check_corner_occlusion.py` → 必须 `CORNER_OCCLUSION: PASS`（边角一致性守卫：先启动本地开发服务，逐页扫描全部菜单页的圆角容器与贴角子元素。判据一「粗描边父级的内弧被直角子元素盖住」——`内弧 = 外弧 − 描边`，子元素该角圆角小于内弧即判遮挡，会让深色描边在角部露出方角缺口；判据二「有背景的圆角父级下，方角子元素外露」——父级自身 `overflow: hidden/clip` 时子元素被裁到圆角内不判。内置两条阳性对照：移除 `.rail` 内弧圆角必须报 `border-occluded`，注入「20px 圆角父级 + 直角有背景子元素」必须报 `corner-mismatch`）
  - `python frontend-design/scripts/check_help_tip_interaction.py` → 必须 `HELP_TIP: PASS`（图标式气泡帮助交互守卫：先启动本地开发服务，实测悬停浮出、指针移出收起、键盘聚焦、Esc 收起并清除 `aria-describedby`、焦点保持（悬停后聚焦再移开指针，说明必须仍在——用 DOM 真实焦点判断，不用本地标记）、视口四边夹取、长文 260px 宽度上限；浮层沿 `offsetParent` 祖先链检查未被滚动容器裁切）
  - `python frontend-design/scripts/check_content_padding.py` → 必须 `CONTENT_PADDING: PASS`（内容留白守卫：先启动本地开发服务，逐页扫描全部示例页。候选容器 = 四边有可见边框、带非透明背景，或本身是 `button` / `menuitem` 等交互控件；判据用 Range 取**文本字形矩形**（不是元素盒）与容器边框内沿比对，**左右任一方向 < 4px 即判 FAIL**。三类按语义豁免：无可见边界的纯文字按钮与布局 div（贴自身盒边属流式排版）、圆形容器（字形受弧线约束，如头像）、自身可滚动的容器。表格单元格、泳道、分页按布局语义豁免。路由从 `component-categories` 真相源派生，不手写清单。**必须配阳性对照**：移除 `overrides.css` 中 Panel 的留白规则后应报出 `panel > P` 贴边，移除 `MenuNode.vue` 的 `padding-right` 后应精确报出 1 处 `x-menu-item > .x-menu-label`（`r:0`）——该对照曾因把 `.workspace` 写进排除面而整页失效，排除面必须与被验面严格一致）
  - `python frontend-design/scripts/check_demo_visibility.py` → 必须 `DEMO_VISIBILITY: PASS`（示例卡可见性守卫：先启动本地开发服务，逐页扫描全部示例页。三条判据——空白卡（内容区可见元素数为 0）、出卡（组件根元素完全落在内容区可视矩形之外，如 `position: fixed` 浮层飘到视口角落）、塌缩（可见宽与高都小于 4px，1px 竖线按线状组件豁免）。定位包装层不参与判定：`absolute/fixed` 且恰好铺满内容区的元素会盖住真正飘出去的浮层。路由从分类真相源派生；内置三项自证——阳性对照（注入视口固定元素必须被出卡判据命中）、示例卡数量下限、空页检测。**必须配阳性对照**：把 `BackTop.vue` 的 `docked` 强制为 `false` 后应精确报出 4 处 `BackTop ... all-outside | BUTTON.x-backtop`；恢复后转 `PASS`）
  - `python frontend-design/scripts/check_demo_guides.py` → 必须 `DEMO_GUIDES: PASS`（示例文字提示守卫：先启动本地开发服务，逐页扫描全部示例页。四条判据——每张卡头必须有 `.x-help` 触发图标、提示正文必须含「组件说明 + 本格示例」两段、非基础示例不得退回「默认形态」、同一组件内不同变体的提示不得全部相同。说明数据源为 `src/data/component-guides.ts`（152 条，覆盖全部组件；17 个上游冻结文件因源码无头部注释由该文件补齐，不得改冻结文件），本格差异由 `views/gallery/demo-guides.ts` 按该格 props 覆盖项推导。内置示例卡数量下限与空页检测。**必须配阳性对照**：把 `demo-guides.ts` 的差异推导改成恒返回 `BASE_TEXT` 后必须报出大量「非基础示例却写默认形态」；移除 `DemoCell.vue` 的 `<HelpTip>` 后必须报出大量「缺少提示图标」——两者恢复后转 `PASS`）
  - `python frontend-design/scripts/build_font_overrides.py --check` → 必须 `FONT_OVERRIDES: PASS`（字号整数化派生块同步守卫：从冻结的 `src/styles/*.css` 自动提取全部非整数字号规则的选择器，按 10.5→11 / 11.5→12 / 12.5→13 / 13.5→14 / 14.5→15 映射生成 `overrides.css` 里的受管块，`--check` 只比对不写入。上游升级新增或删除非整数字号规则时，派生块会与冻结源失配并报 FAIL，防止静默漏改。派生块由 `BEGIN/END GENERATED` 标记包裹，禁止手改）
  - `python frontend-design/scripts/check_demo_health.py` → 必须 `DEMO_HEALTH: PASS`（示例页运行时健康守卫：先启动本地开发服务，逐页扫描全部示例页。九条判据——渲染异常（卡头徽标转 `is-bad`）、框架告警（控制台 error、`[Vue warn]` / `Invalid prop` 类 warning、页面未捕获异常）、坏文本（`NaN` / `undefined` / `Invalid Date` / `[object Object]` / `[object Promise]`）、坏图（`img` 加载完成但 `naturalWidth` 为 0）、零尺寸图标（可见 svg 宽或高 < 2px）、缺可访问名（交互元素既无文本又无 `aria-label` / `title`）、文字裁切（内容超宽且既无省略号也非可滚动容器）、页面横向溢出、低对比文字（文字色与逐层 alpha 合成后的有效背景色对比度 < 1.5，`--theme light` / `--theme dark` 两个主题都要扫，漏改颜色变量会整片命中）。视觉隐藏元素（绝对定位且宽高 ≤1px 或 `clip` 生效）豁免裁切判定；半透明与禁用态元素豁免对比度判定；文字与不透明底之间存在渐变或图片背景时返回 `measurable = false` 不判对比度，因为实际底色取决于色标与图像内容，硬判会把深色盘上的浅字报成缺陷。控制台豁免面集中在 `KNOWN_CONSOLE_ALLOW` 一处定义，每条必须写明根因与解除条件；示例卡数量下限防扫描根不全。`--selftest` 跑阳性对照：注入一张放齐七类违例的坏卡与两条坏控制台消息，逐条断言判据真的会报，并回显注入前后卡数证明扫描根覆盖到被验面。本守卫按 diamond 拆成四个同级文件：`demo_health_env.py`（路由派生、已登录页面装配、页内量测脚本 `PROBE`）、`demo_health_judges.py`（`KNOWN_CONSOLE_ALLOW` 与控制台判据）、`demo_health_selftest.py`（阳性对照注入物与自测流程）、`check_demo_health.py`（入口与全量流程）；改判据只动前三个，改流程只动入口）
  - `node frontend-design/scripts/build_demo_events.mjs --check` → 必须 `DEMO_EVENTS: PASS`（事件表派生同步守卫：从各组件 `defineEmits` 机械派生「组件 → 声明事件名」表写入 `src/views/gallery/demo-events.generated.ts`，示例层据此把每个声明事件都接上一次可见反馈。`--check` 只比对不写入，组件改了 `emits` 而未重跑生成即报 FAIL。生成物禁止手改）
  - `python frontend-design/scripts/check_demo_event_wiring.py` → 必须 `EVENT_WIRING: PASS`（示例事件接线守卫：先启动本地开发服务，逐页扫描全部示例页。沿 `__vueParentComponent` 找到卡内与卡名同名的组件实例，读它 vnode 上真实绑定的 `on*` 处理器，与派生事件表对账；组件声明了却没接处理器的事件即判缺口——这类格子上的按钮点了完全没反馈，看起来像坏控件。事件名按 Vue 的 camelize 规则归一（`row-click` 对应 `onRowClick`），直接比原文会把带横线事件全量误报。`update:*` 由样本状态写回负责，不在本判据范围。非手势触发的逐帧/逐秒/指针移动类事件走集中豁免面，且豁免条目必须是事件表里真实存在的事件，防止豁免面腐烂。`--selftest` 跑六条判据阳性对照：未接必报、接上必不报、带横线事件名不误报、`update:*` 不计入、多事件只报漏的那个、豁免面无失效条目。本守卫按 diamond 拆成两个同级文件：`demo_event_wiring_probe.py`（页内量测脚本 `PROBE`、豁免面 `NO_FEEDBACK`、事件名归一与缺口判定、事件表读取）、`check_demo_event_wiring.py`（路由派生、全量流程与裁决）；改判据只动探针层，改流程只动入口）
  - `cd component-library && npm run build` → 必须 vue-tsc 类型检查 + 构建成功
  - `cd component-library && npm run test:unit` → 上游单测必须全绿
- 上游升级：重新冻结 commit → 运行 `python frontend-design/scripts/verify_fidelity.py --write-baseline` 刷新基线，并同步更新本文件顶部的 commit 号。

## 工作流（5 步，每步带检查点）

### 第 1 步：理解需求与上下文

- **输入**：前端需求（组件/页面/应用）、用途、受众、技术约束。
- **动作**：明确四个问题——目的（解决什么问题/谁用）、语气风格候选、技术约束（框架/性能/可访问性）、差异化记忆点。
- **查询积累的用户偏好**（从 `frontend-ui-visual-rules/references/visual-preference-learning.md` 获取方向）：
  ① 检查 `总体审美` 与 `明确拒绝` 分类，确保方向不与已有偏好冲突；
  ② 匹配当前媒介类型（如着陆页/移动端），加载 `按介质` 的对应偏好；
  ③ 若当前项目属于已记录的品牌项目，加载对应的风格约束；
  ④ 将偏好引用作为候选方向依据："基于你之前偏好的 X 风格，我们建议..."
- **输出**：需求理解摘要 + 候选审美方向列表 + 偏好匹配情况。

### 第 2 步：选定审美方向（检查点）

- **输入**：候选审美方向列表。
- **动作**：选一个**大胆且清晰**的方向（极端极简/极繁/复古未来/自然有机/编辑杂志感/粗野主义/装饰艺术等），并说明选它的理由。
- **检查点【必确认】**：方向涉及极端风格、大面积留白、非预期布局等激进选择时，先向用户确认审美方向与接受度再进入实现；用户无明确偏好时，给出 2-3 个方向供其选择，不擅自定稿。
- **输出**：确认后的设计方向一句话陈述（含风格、主色、字体基调）。

### 第 3 步：实现真实可运行的代码

- **输入**：已确认的设计方向。
- **动作**：实现 HTML/CSS/JS、React 或 Vue 代码，确保生产级、可用、功能真实成立；按「前端审美指导」打磨字体/颜色/动效/空间/背景细节。
- **输出**：可运行代码 + 关键设计决策说明（为什么这个字体/配色/动效）。

### 第 4 步：自查与打磨

- **输入**：首版实现。
- **动作**：对照审美立场逐项自查——风格是否统一、细节是否打磨到位、是否落入通用 AI 审美（Inter/Roboto/Arial、白底紫渐变、可预测布局）；复杂度是否与审美愿景匹配。**交互校验**（参考 `references/apple-fluid-design.md` 核心交互校验清单）：按下有无即时反馈、拖拽是否 1:1 跟随、动画是否可打断、是否使用弹簧而非固定时长 transition、手势释放是否移交动量。
- **输出**：自查清单结果 + 需要微调的细节项。

### 第 5 步：交付与验收（检查点）

- **输入**：打磨后的实现。
- **动作**：验证功能可用性（交互/响应式/可访问性），并向用户展示设计决策摘要。
- **检查点【必确认】**：交付前向用户确认视觉效果与功能是否符合预期；用户提出修改时回到第 3 步迭代，不擅自扩大改动范围。
- **输出**：最终交付 + 修改迭代记录。

## 触发后强制联动

- 凡本轮新增或修改 `.vue`、`.tsx`、`.jsx`、`.ts`、`.js`、`.html`、`.css`、`.scss`、`.less` 前端代码文件，必须同时命中：
  - `comment-rules`
  - `code-style-consistency-rules`
  - `code-change-finalization-gate-rules`
- 上述任一 skill 未命中，不得给出“已完成前端改动”或“可提交”结论。
- 前端测试前收口统一并入 `code-style-consistency-rules`：至少检查 import 排序/分组、重复或未使用 import、缩进、连续空行、模板 / script / style 区块排版，以及语法、类型、引用与目录归位；若项目存在 Prettier、ESLint、vue-tsc、tsc、npm/yarn/pnpm lint 等本地命令，优先执行对应命令并记录结果。
- 前端注释收口必须覆盖新增或修改的函数、事件处理、异步数据加载、条件渲染、复杂样式和兼容/兜底逻辑；前端代码和后端代码一样属于代码改动，不能以“这是前端”作为跳过注释双 skill 的理由。

## 职责边界与引用

- **珍珠玻璃组件库**（中后台默认组件库：152 组件 + 七层令牌样式 + mock 运行时 + 还原度守卫）→ `component-library/`（来源与许可见 `component-library/README.md`；设计规范见 `component-library/DESIGN.md`；守卫脚本在 `scripts/`）
- **组件目录索引**（152 组件契约与用法速查，按 Arco 语义分类与物理目录双维度导航，选组件的第一入口）→ `references/component-catalog.md` / `references/component-catalog.json`（生成器 `scripts/build_component_catalog.mjs`）
- **组件库示例页**（后台内的组件用法目录，人工核对全部组件真实渲染与挂载状态）→ 后台「组件库」分组，路由 `/gallery/<分类键>`，源码 `component-library/src/views/gallery/`；独立 html 入口已退役，示例统一在真实后台壳层与真实路由内呈现
- **Apple 流体交互设计**（弹簧物理参数、毛玻璃材质、动效降级、交互校验）→ `references/apple-fluid-design.md`
- **设计偏好学习**（从历史交互积累用户视觉品味）→ `frontend-ui-visual-rules/references/visual-preference-learning.md`
- **UI 视觉硬规则**（配色规范、主题变量、可访问性底线）→ `frontend-ui-visual-rules`
- **Vue 工程实现** → `vue-best-practices` / `vue`；**React 工程实现** → `vercel-react-best-practices`
- **UI 代码审查**（是否符合 Web Interface Guidelines）→ `web-design-guidelines`
- **组件拆分与目录归属** → `frontend-component-rules`

## 前端审美指导

重点关注：
- **字体**：选择真正好看、有辨识度、有趣味的字体。避免使用 Arial、Inter 这类过于通用的字体，优先使用能提升界面气质的独特字体；要敢于使用有性格、有记忆点的选择。可采用“有辨识度的展示字体 + 克制精致的正文字体”的组合。
- **颜色与主题**：坚持一个统一的审美体系。使用 CSS 变量保持一致性。与其用平均分配、胆小保守的配色，不如使用主导色明确、强调色锐利的方案。
- **动效**：使用动画来表达效果与微交互。对 HTML 场景优先使用纯 CSS 方案；如果是 React 且项目可用 Motion 库，则优先使用它。把重点放在高影响力时刻，例如一套编排良好的页面初始加载动效，配合错峰 reveal（如 animation-delay），往往比到处撒微交互更有感染力。也要使用能制造惊喜的滚动触发与 hover 状态。
- **弹簧物理驱动**：引入弹簧物理参数替代固定时长 transition，使动效更自然。核心参数参考 `references/apple-fluid-design.md`：阻尼比（damping ratio，1.0=无弹跳、<1=弹跳震荡）和响应时间（response，秒）。典型场景：底部 sheet 用 `damping=0.8, response=0.3`，普通 UI 入场用 `damping=1.0, response=0.4`。手势释放时移交原始速度，通过动量投射公式计算吸附点，实现"丢出去自己找到位置"的流畅体验。
- **空间构图**：允许出现非预期布局、不对称、重叠、斜向流动、打破网格的元素，以及大面积留白或受控的高密度排布。
- **背景与视觉细节**：不要默认用纯色背景了事，而要创造氛围与层次感。可以加入符合整体审美的情境化效果与纹理，例如渐变网格、噪点纹理、几何图案、分层透明、戏剧化阴影、装饰性边框、自定义光标、颗粒覆盖层等。
- **毛玻璃材质**：在需要层次感的面板、工具栏、底部 sheet 等场景，使用 `backdrop-filter: blur(20px) saturate(180%)` 配合半透明背景色实现毛玻璃效果。标准配方：`background: rgba(255,255,255,0.6); backdrop-filter: blur(20px) saturate(180%); border-top: 1px solid rgba(255,255,255,0.4)`。深色模式对应调整为 `rgba(0,0,0,0.6)` + `rgba(255,255,255,0.1)`。详细参数见 `references/apple-fluid-design.md`。

**绝对不要**使用那种通用化的 AI 生成审美，例如被过度使用的字体组合（Inter、Roboto、Arial、系统字体）、陈词滥调的配色方案（尤其是白底紫渐变）、可预测的布局与组件套路，以及缺乏场景个性的模板化设计。

要带着创造性去理解上下文，并做出真正像“为这个场景量身设计”的意外选择。每一次设计都不应该长得一样。要在明暗主题、字体选择和审美方向之间主动变化。**不要**不断回到相同的常见选择（例如 Space Grotesk 这一类）。

**重要**：实现复杂度必须与审美愿景匹配。极繁风格需要足够丰富的代码、动画和视觉效果；极简或精致路线则需要克制、精确，以及对间距、字体和细微细节的高度把控。优雅来自于把一种愿景执行到位，而不是把所有效果堆在一起。

## 字体工程可靠性（自托管字体必查，2026-09 实证）

审美之外，字体还有工程可靠性维度。以下问题都在真实项目里翻过车，使用自托管字体（@fontsource 或手写 @font-face）时必须逐项验收：

- **@fontsource 子集陷阱（最易踩）**：@fontsource 按「字重 × 子集（latin / latin-ext / …）」拆分 @font-face 声明。产物目录里存在某字重的字体**文件** ≠ CSS **声明**完整——实测 Outfit 的 500/600 权重只有 latin-ext 子集（unicode-range 不含基本拉丁 a-z），用该字重渲染拉丁文本会因无可用字形回退失败，显示为**乱码块（tofu）**，而非简单变小。
  - **验收动作**：构建后 grep 产物 CSS（不是源码），确认所用字重的 `latin` 基本子集声明真实存在——如 `font-weight:500` 的规则里引用了 `xxx-latin-500.woff2`，而不仅是 `xxx-latin-ext-500`。
  - 需要加粗小字时优先选用已验证 latin 子集完整的字体组合（如 Manrope + JetBrains Mono 各字重子集齐全）。
- **input/textarea 必须显式 line-height**：input 元素默认 `overflow: hidden`，自托管几何字体（Outfit/Manrope 类）字体度量偏紧，依赖 `normal` 行高会裁掉字形下缘。文本输入类元素显式声明 `line-height: 1.5`（或更高）。
- **SPA 自托管必须控缓存**：入口页（index.html，含 SPA 回退分支）响应 `Cache-Control: no-cache`；带 hash 的 assets 加 `Cache-Control: public, max-age=31536000, immutable`。否则浏览器启发式缓存旧入口页、引用旧 hash 资源，出现"改了样式刷新也看不到"的假 bug——排查会浪费大量时间在错误方向上。
- **选型补一条视觉标准**：拉丁字体的 x-height 决定与中文混排的视觉均衡——Outfit 拉丁小写字母视觉高度只有字号的 ~55%，与方块中文同排会显得小一号、弱一档。为中文界面选拉丁字体时优先 x-height 大的（如 Manrope），需要加粗小字时同时用 500/600 字重增强笔画存在感（前提是子集声明完整）。
- **故障定性方法**：用户反馈"文字显示不全"时，先获取清晰放大截图区分三种形态——**乱码块**（tofu → 字体子集/字形缺失）、**偏小**（字号/字重/x-height 视觉问题）、**裁切**（line-height/overflow 问题），三者修法完全不同。再用产物级 grep（检查构建产物 CSS 而非源码）区分"构建丢失 / 浏览器缓存 / 代码错误"，避免在错误层反复修。

## 边界条件

- **需求模糊**（用途/受众/技术栈未知）：先在第 1 步补齐信息再进入设计，不脑补默认受众。
- **技术栈约束冲突**：审美理想与现实约束冲突时（如性能、可访问性、老旧浏览器），优先保可访问性与性能，并向用户说明取舍。
- **无障碍动效降级**：使用 `prefers-reduced-motion` 和 `prefers-reduced-transparency` 媒体查询提供降级方案——弹窗/sheet 降为简单淡入淡出（transition opacity 200ms）、毛玻璃降为纯色背景。不得默认禁用所有动效，降级后保留核心功能语义。无障 config 适配代码参考 `references/apple-fluid-design.md`。
- **用户对激进设计犹豫**：退回提供 2-3 个收敛方向供选择，不强行坚持单一方向。
- **迭代失控**：用户连续多轮提修改时，每轮只改本轮要求范围，不顺手重构无关部分。

## 退出机制

用户输入「结束」或确认交付 → 停止，回复设计交付摘要；未获方向确认前不进入大段实现（第 2 步检查点）。

## 约束

- 输出真实可运行的代码，禁止伪代码或占位实现。
- 审美方向必须在第 2 步获得用户确认后才定稿。
- 复杂度与愿景匹配：极繁要足够丰富，极简要足够克制，不堆砌效果。
