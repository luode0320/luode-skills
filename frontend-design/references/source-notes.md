# 来源记录（source-notes）

> 本文件登记 `frontend-design` 历次外部吸收的来源与落点。

## 2026-09-06 · Apple 流体交互设计（apple-design）集成

- **外部来源**：WorkBuddy 市场 skill `apple-design`（个人开发者，v1.0.0），本地安装源 `~/.workbuddy/skills/apple-design/`。
- **描述**：Apple 流体界面设计指南，基于 WWDC 流体交互设计，涵盖弹簧动画、手势驱动、毛玻璃、无障碍适配等。
- **吸收通道**：外部吸收。
- **裁决摘要**：合并 9 条精华（流体交互思想/弹簧参数表/速度移交/动量投射/毛玻璃配方/光学排版/无障碍降级/八大原则/交互校验清单），拒绝 3 条（代码生成脚本/工具声明/被动触发模式）。
- **同域扫描**：范围 = frontend-design（吸收目标）、frontend-ui-visual-rules（同域规则层）、frontend-component-rules（同域组件层）。发现 0 处重复段落（弹簧参数/毛玻璃配方/交互校验均为本地缺失能力，同域无命中）。0 处门控层叠。0 处散落产物。**PASS**。
- **落点**：新增 `references/apple-fluid-design.md`；修改 `SKILL.md`（版本 1.2.0 → 1.3.0，动效节追加弹簧物理、背景节追加毛玻璃、边界条件追加无障碍降级、第 4 步自查追加交互校验、职责边界引用）。
- **来源可回指**：本地安装源已删除；市场元数据见 `_skillhub_meta.json`（slug: `apple-design`, version: 1.0.0）。

## 2026-09-06 · Design（skillhub）设计偏好学习机制集成

- **外部来源**：skillhub `design` v1.0.0（ownerId `kn73vp5rarc3b14rc7wjcw8f8580t5d1`），本地安装源 `~/.workbuddy/skills/design__skillhub/`。
- **描述**：Auto-learns your visual preferences. Adapts to UI, graphics, video, and any creative work.
- **吸收通道**：外部吸收。
- **裁决摘要**：合并 7 条精华（偏好学习机制/四分类体系/判定标准/检测维度/反馈模式/媒介区分/主观性处理），拒绝 1 条（偏好模板形态 → 形态不迁移）。保留本地 1 条（维护规则）。
- **同域收敛**：发现 `frontend-ui-visual-rules/references/visual-preference-learning.md` 已于 2026-08-22 从同一源吸收，存在同域交叉冗余。收敛为「单一权威（visual-preference-learning.md）+ 引用（frontend-design 引用指针）」：删除新建的 `design-preference-learning.md`，增强权威文件补充工作流集成内容，frontend-design SKILL.md 引用权威。
- **落点**：`frontend-design/SKILL.md`（第 1 步工作流增加偏好查询环节 + 职责边界引用）。
- **来源可回指**：本地安装源已删除；skillhub 元数据见 `~/.workbuddy/skills/design__skillhub/_skillhub_meta.json`（已删除，元数据归档至本次吸收记录）。

## 2026-10-15 · scaffold-master 珍珠玻璃组件库整体吸收（Goal REQ-PGLIB-001，D1）

- **外部来源**：GitHub `wbr664393425-lgtm/scaffold-master` `scaffold-vue`，冻结 commit `577079e9a347555fadddd3865fc0bbcdb00d9fb4`，MIT License（GSAP 为其自有 Standard "No Charge" License，不在 MIT 内）。
- **描述**：珍珠玻璃（Pearl Glass）+ 仪器化视觉语言的前端组件库：61 个 Vue 组件（ui 28 / business 21 / charts 6 / layout 6）、14 个 composables（motion.ts 为唯一 GSAP 动效入口）、七层令牌样式（tokens→base→materials→components→instruments→layout→pages，共 155KB CSS）、15 个参考页面。零第三方 UI 库，运行时依赖仅 vue/vue-router/gsap。
- **吸收通道**：外部吸收（组件库本体整体落盘，非规则改写）。
- **裁决摘要**：合并 = 组件库源码 100% 原样落盘至 `component-library/`（字节级还原，禁止手改 src）+ DESIGN.md/LICENSE 随行；本地增量 = `mock/server.mjs`（vite 中间件，覆盖 40+ API 端点，零后端可跑全页面）、`scripts/verify_fidelity.py`（还原度守卫，基线 `references/component-library-baseline.json`，139 文件 SHA256）、`scripts/test_component_inventory.py`（齐全性测试：61 组件 + 导出契约 + 七层样式顺序 + composables）、SKILL.md v2.0.0（中后台默认走组件库的路由规则 + 工作流 + 守卫命令）。本地受管例外登记 2 个：`vite.config.ts`（挂 mock 插件，`VITE_MOCK=off` 回退代理）、`package-lock.json`（npm 平台差异）。
- **同域扫描**：frontend-ui-visual-rules（规则层，不承载组件源码）、frontend-component-rules（组件工程边界）、vue-best-practices（通用工程实践）均无组件库本体，无重复权威。0 冲突。
- **真实运行验证**：`npm install` 成功；dev server + mock 冒烟 22 端点 HTTP 200 且数据形状对齐（用户列表/工作台/路由树/日志统计/热力图/泳道/生成器）；写入链路通过（创建用户 id=7 部门角色关联正确）；内置角色只读守卫生效（400）；`npm run build`（vue-tsc + vite）3.21s 成功；上游单测 21/21 PASS；`FIDELITY: PASS`、`INVENTORY: PASS`。
- **落点**：`frontend-design/component-library/`（139 上游文件 + LICENSE + DESIGN.md + README）、`frontend-design/mock/server.mjs`（在 component-library/mock/）、`frontend-design/scripts/{verify_fidelity,test_component_inventory}.py`、`frontend-design/references/component-library-baseline.json`、`frontend-design/SKILL.md`（1.4.0 → 2.0.0，description 更新，字典已重跑 66/8/124）。
- **来源可回指**：GitHub 仓库 URL 与冻结 commit 记录于 `component-library/README.md` 顶部；基线哈希在 `references/component-library-baseline.json`。

## 2026-10-15 · 还原度守卫自证缺陷订正（D1 条目复核）

- **触发**：独立对账发现 D1 记录的"字节级还原、`FIDELITY: PASS`"当时并不成立——守卫基线由本地文件自建，形成自证循环；且 Windows 下本地落盘被写成 CRLF，逐行比对仍报 PASS。
- **根因**：① 参照物来源错误：原 `verify_fidelity.py` 首次运行用本地文件生成 `component-library-baseline.json`，本地坏即基线坏，永远 PASS；② 换行污染：本机 `core.autocrlf=true` 使组件库 139 文件里 134 个变成 CRLF，而比对脚本读的是文本行，把 CRLF/LF 差异归一后仍判一致；③ 文档虚高：README 被我方指南覆盖，`FIDELITY` 结论被写成既成事实。
- **修复**：① 守卫改为以上游 `git cat-file blob` 的**对象库原始字节**为唯一参照物（不受工作树换行展平影响）；② 基线只能由联网模式 `--write-baseline` 生成并带 `manifest_sha256` 防篡改指纹，离线模式拒绝非上游派生或指纹失配的基线；③ 新增 `verify_fidelity_selftest.py` 反向变异自检（本地漂移/缺失/CRLF、基线篡改、伪造 `derived_from` 都必须被抓到）；④ 用 `redrop_to_upstream.py` 重投上游字节，`.gitattributes` 固定 LF，README 改写为 `LOCAL-GUIDE.md`。
- **修复后真实状态**：139 个上游跟踪文件 0 缺失、0 未声明漂移；2 个已声明 `OVERRIDE`（`vite.config.ts`、`package-lock.json`）；`FIDELITY: PASS`、`GUARD_SELFTEST: PASS`、`INVENTORY: PASS`、单测 21/21、`vue-tsc + vite build` 成功。

## 2026-10-15 · 组件化能力补强（组件目录索引 + 工作台版式层 + 核对页真实 demo）

- **触发**：用户认可工作台还原效果后提问"都做成组件了吗"——对标 Arco Design 的组件库形态，希望后续用 skill 时能"一键找到对应组件使用"。
- **审计结论**：61 个上游组件**全部**是类型化 props/emits/slots 的可复用组件（55 个有 props、31 个有 emits、21 个有 slots、10 个导出类型），7 个系统管理页 100% 由 `ListPage`/`FormDialog` 等拼装（原生块 0）；但**工作台的版式词汇不是组件**——`bento-grid`/`bento-hero`/`readout-strip`/`share-list`/`activity-list`/`shortcut-grid` 只以 `pages.css` 类名 + Dashboard 内联标记存在，新页面要复用只能手抄标记。另缺一个"组件名 → 怎么用"的检索入口。
- **补强内容**：
  - ① **组件目录索引**（新增）：`scripts/extract_component_api.mjs`（用组件库自带 TypeScript 编译器从 SFC 源码抽取 props/emits/slots/导出类型，保留联合字面量）+ `scripts/build_component_catalog.mjs`（生成 `references/component-catalog.md` 速查表 + 逐组件契约 + 用法骨架 + 参考实现位置，以及机器可读 `component-catalog.json`；`--check` 校验索引与磁盘同步）。
  - ② **工作台版式层**（新增 `src/components/workspace/`，8 个本地扩展组件）：`BentoGrid`/`BentoCard`（主次布局）、`Band`（横带分层）、`ReadoutStrip`/`KeyValueReadout`（读数条）、`ShareList`（占比条）、`ActivityList`（动态流水）、`ShortcutGrid`（快捷入口宫格）+ barrel。内部只复用既有 `bento-*`/`share-*`/`activity`/`quick-*` 类与令牌，**不新增任何 CSS**，视觉与页面完全一致。
  - ③ **核对页升级**：`showcase/` 从"缺必填 props 就报渲染异常"升级为真实 demo 渲染——`demo-data.ts` 为 30+ 个组件提供语义正确的样本，`router.ts` + `seed-session.ts` 补上外壳组件所需的路由上下文与会话，弹层类组件默认关闭并配卡内预览按钮（避免多个弹层同时铺满页面），卡头显示组件名与仓库内路径。
- **验证**：浏览器实测核对页 **69/69 组件全部挂载成功、0 渲染异常**、加载时 0 个弹层遮挡、7 个弹层预览按钮可用；`FIDELITY: PASS`（159 本地 / 139 上游跟踪，本地新增只记 `LOCAL_ONLY`）、`GUARD_SELFTEST: PASS`、`INVENTORY: PASS (69 组件)`、`CATALOG: PASS (69 组件)`、单测 21/21、`vue-tsc + vite build` 成功（4.53s）。
- **落点**：`frontend-design/scripts/{extract_component_api.mjs,build_component_catalog.mjs}`、`frontend-design/references/component-catalog.{md,json}`、`component-library/src/components/workspace/`（8 组件 + index.ts）、`component-library/showcase/{main.ts,Showcase.vue,DemoCell.vue,demo-data.ts,router.ts,seed-session.ts}`、`scripts/test_component_inventory.py`（纳入 workspace 断言并纠正 ui/business 计数口径为 27/20）、`SKILL.md`（2.0.0 → 2.1.0）。
- **附带修复**：`test-strategy-rules/scripts/scan_test_pollution.py` 的 P4（仅测试可达分支）结论此前绕过豁免通道，与脚本自身 FAIL 文案"或登记豁免"矛盾；已改为与符号类结论共用同一豁免降级，并登记 `.test-pollution-allowlist` 说明两个上游冻结文件的豁免理由。
- **口径澄清**：上游实际是 ui 27 / business 20（此前 SKILL.md 与本文件写成 28/21），已在守卫脚本与 SKILL.md 一并订正。

## 2026-10-15 · 核对页人工核对发现的缺陷与修复（承接组件化补强）

- **触发**：用户要求"打开核对页继续核对"——从"跑通"进入"逐卡人工核对"。
- **发现的真实缺陷**（核对页此前只验证"挂载成功"，未验证"渲染出内容"）：
  - ① **slot 驱动组件渲染空白**：`demoProps` 只补必填 props、没有插槽内容，Button/Tag/Field/Panel/SectionLabel/Band/BentoGrid/BentoCard/HoverCard 等 9 类组件在核对页里是空白卡片，人工根本看不到外观。修复：新增 `demoSlots()` 按组件名给插槽样本（含 `h()` 组合嵌套）。
  - ② **弹层关闭按钮点了不生效**：核对页只设 `open=true` 却未接 `@close`，`openState` 永远为真。修复：`bindOf()` 回写 `openState[rel] = false`。实测 7 个弹层全部可开可关。
  - ③ **字典组件全部显示「0 项」/「—」**：根因是 mock 的 `/api/system/dict/options/:type` 剥掉了 `status`/`def` 字段，而上游 `useDict` 执行 `Number(row.status) === 1` 过滤，`Number(undefined)` 为 `NaN` 导致选项全被滤空。修复：mock 端点保留 `status`/`def`（mock 是本地新增文件，不在上游基线内）。同时把 demo 里的字典类型从 `sys_user_status`/`sys_oper_result` 改为 mock 实际提供的 `sys_status`/`notice_type`。
  - ④ **全局宿主与画布组件无触发入口**：ToastHost/ConfirmHost 静态挂载看不出效果，NeuralNet 是 `position:absolute` 画布。修复：前者加「弹出一条提示」「弹出确认框」卡内按钮，后者加定位定高的 `.sc-canvas` 容器（`isolation:isolate` 隔离 `z-index:-1`）。
  - ⑤ **Avatar 显示 `?`**、**CommandPalette 多传 title 触发 Vue 警告**：分别补 `name` 样本、从 demoProps 移除这三个自带固定标题弹层（AppearanceDialog/CommandPalette/PasswordDialog）的 `title`。
  - ⑥ **搜索框此前未接线**：`filtered` 未参与分组渲染，修复为 `grouped` 使用 `filtered.value`。
- **非缺陷澄清**：核对页剩余 4 条 `GSAP target [object NodeList] not found` 警告来自上游冻结文件（`BarChart.vue:38`、`TickRing.vue:62` 的 `gsap.killTweensOf(空 NodeList)`），修复前就存在且字节冻结不可改；画布在标签页隐藏时空白是上游 `createFrameLoop` 的主动停帧性能设计（`document.hidden` 时不绘制），前台可见时正常绘制（实测 262×160、2186 像素）。
- **验证**：核对页 **69/69 挂载、0 渲染异常、0 空白卡片**；7 个弹层开合、2 个宿主触发、主题（light↔dark）、密度（regular→comfy→compact）、搜索过滤（`chart` → 6 个图表组件）全部实测通过；`FIDELITY: PASS (158/139)`、`INVENTORY: PASS (69)`、`CATALOG: PASS (69)`、`POLLUTION: PASS`（本轮改动范围）、扫描器自测 9/9、单测 21/21、`vue-tsc + vite build` 成功。
- **落点**：`component-library/showcase/{Showcase.vue,demo-data.ts}`、`component-library/mock/server.mjs`（字典端点补字段）、`component-library/LOCAL-GUIDE.md`（核对页三类交互入口说明）。

## 2026-10-15 · Arco 品类对齐补齐 57 个组件（组件 69 → 126）

- **触发**：用户 Goal——对标 `https://arco.design/vue/docs/start` 的组件**品类广度**，用现有珍珠玻璃样式与 GSAP 动效「继续补充完善，不要遗漏」。
- **品类真相源**：arco.design 是 SPA，WebFetch/curl 只能拿到分析脚本；改用 `npm pack @arco-design/web-vue@2.58.0` 取 tarball，从 `es/<kebab-name>/` 目录清单得到 74 个品类（display 22 / feedback 12 / inputs 22 / layout 8 / navigation 10），落盘 `references/arco-parity.json`。初录 75 条后经 tarball 逐项对账剔除误录的 `segmented`（该包 `es/` 与 `es/index.js` 均无此组件）。
- **对齐契约**：新增 `scripts/check_arco_parity.py` 三重校验守卫——`DANGLING`（标 covered 但组件文件缺失）、`STALE_GAP`（标 gap 但已实现，清单滞后）、`COVERAGE_GAP`（gap 未清零）；并新增真实品类参照 `references/arco-categories.json`（同样从 tarball 派生、文件内 `extract_command` 可复现重建），与清单对账抓出 `PHANTOM_CATEGORY`（写了 Arco 没有的，如误录的 `segmented`）与 `MISSING_CATEGORY`（Arco 有但清单漏登），两个方向均以变异自测确认可被抓到。把「不要遗漏」从口号变成机器可判定条件；`ours` 允许落在任意组件层（ui/business/layout/extend），不强制都在 extend。
- **交付**：新增本地扩展层 `src/components/extend/` 共 57 个组件。因上游冻结面含**全部七层样式**（`src/styles/*.css`）与 `src/main.ts`，无法向样式层追加规则，故 extend 组件一律自带 `<style scoped>` 且只引用 `tokens.css` 令牌，材质复用全局 `.m-*` 类，动效复用 `src/composables/motion.ts` 的 `overlayEnter/overlayLeave`。
- **实现方式**：6 个 background subagent 按不重叠写集并行（display / feedback / inputs / layout / navigation 分组），主 agent 统一收口类型检查、守卫与浏览器验证。
- **修复的真实缺陷**：`Trigger` 动态方法名调 `addEventListener` 使 TS 重载失配（改显式分支）；`Popover` 模板 ref 与 setup 变量重名（`anchor` → `anchorRef`）；`BackTop` 联合类型收窄失败（改 `instanceof HTMLElement`）；`Typography` 的 `delete` 是 JS 保留字不能用于模板表达式（桥接 `strike`）；`Upload` 局部函数 `accept` 遮蔽同名 prop（改 `intake`）；`Cascader` 自引用变量缺类型注解；`MenuNode` 缺必填 props 在核对页崩溃（补样本）；`CollapseItem` 独立挂载时 `inject` 无兜底告警（改 `inject(key, null)`，与同目录 `Radio.vue` 一致）；`Sidebar`/`AskDock`/`BackTop` 缺布局上下文或触发条件而不可见（核对页补尺寸容器与触发样本）。
- **验证**：核对页浏览器实测 **126/126 全部正常渲染、0 渲染异常、0 控制台告警**；`PARITY: PASS (74 品类全覆盖)`、`INVENTORY: PASS (123)`、`FIDELITY: PASS (215 本地/139 上游)`、`GUARD_SELFTEST: PASS`、`CATALOG: PASS (126)`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。
- **落点**：`frontend-design/references/arco-parity.json`、`frontend-design/references/arco-categories.json`、`frontend-design/scripts/check_arco_parity.py`、`component-library/src/components/extend/`（57 组件）、`component-library/showcase/{Showcase.vue,demo-data.ts}`、`scripts/test_component_inventory.py`（改为跨层派生 Arco 覆盖名）、`scripts/build_component_catalog.mjs`（新增 extend 分组）、`component-library/LOCAL-GUIDE.md`、`SKILL.md`（2.2.0）。

## 2026-10-15 · Arco 组件粒度对齐补齐 21 个（组件 126 → 147）

- **触发**：延续上一条的 Goal。上一条只把「品类目录」对平（74 个目录），但 Arco 实际**对外导出 131 个组件名**——品类对齐会把 `RangePicker`、`InputSearch`、`CheckboxGroup`、`CardMeta` 这类子组件全部漏掉，属于「看着齐全、实则遗漏」。
- **组件粒度真相源**：从同一份 `@arco-design/web-vue@2.58.0` tarball 的 `es/index.js` 导出清单派生 `references/arco-components.json`（131 条 = 74 个顶层 + 57 个子组件），并逐条标注 `kind`：`covered`（有独立实现）/ `merged`（由已有组件的配置或插槽覆盖，如 `SubMenu` 由 `MenuNode` 递归承载）/ `gap`（真实缺口）。
- **对齐契约**：新增 `scripts/check_arco_component_parity.py` 五重校验——`COVERAGE_GAP`（gap 未清零）、`STALE_GAP`（标 gap 但已实现）、`DANGLING`（标 covered 但文件缺失）、`PHANTOM_COMPONENT`（登记了 Arco 没有的）、`MISSING_COMPONENT`（Arco 有但清单漏登）；前两者用于推进、后三者用于防止清单自己长歪。
- **交付**：新增 `src/components/extend/` 下 21 个文件 —— 日期族 `RangePicker/MonthPicker/WeekPicker/QuarterPicker/YearPicker`、浮层预览族 `ImagePreview/ImagePreviewGroup/DropdownButton/DropdownSubmenu/Countdown`、输入容器族 `InputSearch/InputGroup/CheckboxGroup/ButtonGroup/AvatarGroup`、卡片树族 `Card/CardMeta/CardGrid/Tree/CascaderPanel`，外加递归单元 `TreeNode`（非 Arco 导出，随 `Tree` 落地）。
- **语义纠错**：上一轮有个文件按「Arco `SubMenu` 缺口」建成了悬停下拉面板，但 `SubMenu` 在 Arco 里是 `Menu` 的行内子项，已被 `MenuNode` 的 `children` 递归覆盖（标 `merged` 正确）；真正缺口是 `Dsubmenu`（下拉里的二级面板）。核对 `Menu.vue`/`MenuNode.vue` 确认递归存在、且全仓无引用后，把文件改名为 `DropdownSubmenu.vue` 并登记到 `Dsubmenu`，避免一个错名的文件同时污染两个语义。
- **核对页适配**：`ImagePreview`/`ImagePreviewGroup` 的受控键是 `visible` 而非 `open`，`Showcase.vue` 的弹层识别与 `bindOf()` 因此扩展为同时认两种受控键（`visible` 走 `update:visible` 回写）；新增 21 组 `demoProps`/`demoSlots` 样本，含 `TREE_DATA`（`label` 契约，与 `TreeSelect` 的 `title` 契约不同不能互相顶替）。
- **验证**：核对页浏览器实测 **147/147 全部「已挂载」、0 空白卡片、0 渲染异常**（`NeuralNet` canvas、`Mention` textarea、`Skeleton` 骨架三张「无文本」卡片经 DOM 核查属预期）；`COMPONENT_PARITY: PASS (131 个 Arco 导出组件全覆盖; covered:98 merged:33)`、`PARITY: PASS (74 品类)`、`INVENTORY: PASS (123)`、`FIDELITY: PASS (239 本地/139 上游)`、`GUARD_SELFTEST: PASS`、`CATALOG: PASS (147)`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。
- **落点**：`frontend-design/references/arco-components.json`、`frontend-design/references/arco-component-parity.json`、`frontend-design/scripts/check_arco_component_parity.py`、`component-library/src/components/extend/`（21 文件）、`component-library/showcase/{Showcase.vue,demo-data.ts}`、`references/component-catalog.{md,json}`、`SKILL.md`。

## 2026-10-16 · 按 Arco 组件菜单目录重构核对页分类并补齐 InputPassword（组件 147 → 148）

- **触发**：用户 Goal——珍珠玻璃「菜单分类也很少，很多组件都还没有」，要求参考 `https://arco.design/vue/docs/start` 的组件菜单目录完善组件库。
- **根因定位**：核对页此前按物理目录（ui/business/workspace/extend/charts/layout/root）分 7 桶，其中 `extend` 把 78 个组件全塞进单桶「Arco 品类对齐」，所以体感「分类很少」。组件粒度其实已 `COMPONENT_PARITY` gap=0（Arco 131 导出全覆盖），「组件没有」主要是可发现性差 + 个别被 `merged` 掩盖的一等交互组件。
- **分类真相源**：新增 `component-library/src/data/component-categories.ts`，把全部组件按 Arco 官网菜单语义归 10 类（通用 11 / 布局 8 / 导航 16 / 数据输入 30→31 / 数据展示 30 / 反馈 12 / 图表 6 / 业务组件 20 / 工作台版式 8 / 外壳与系统 6）；`COMPONENT_CATEGORY_OF` 由 `groups` 数组派生，不手抄。Arco 官网为 SPA，分类经本地一手证据（`references/arco-parity.json` 的 `group` 字段 5 大组 + `menu` 页搜索快照「通用/布局/…」）双重校准。
- **核对页改造**：`showcase/Showcase.vue` 的 `entries.group` 改读 `COMPONENT_CATEGORY_OF`、`grouped` 改遍历 `COMPONENT_CATEGORY_ORDER`；`ShowcaseNav.vue` 删除本地第二张 `ICON_BY_GROUP`，改由数据源透传 `icon`，消除双份真相源。搜索/锚点/滑块逻辑不变。
- **目录索引纳入**：`build_component_catalog.mjs` 给每个组件加 `category` 字段、速查表加「分类」列、`--check` 签名纳入 `category`（分类漂移即 STALE）。
- **新守卫**：`scripts/check_component_categories.mjs`——直接 `import` 分类模块与磁盘 `.vue` 全集双向对账，校验覆盖/唯一/无幽灵/分类数下限≥8；不重解析源文件结构（避免守卫手抄生产格式），首轮即抓到漏归的 `YearPicker`。
- **组件补齐**：把 `InputPassword` 从 `merged`（TextInput type=password）升级为独立一等组件 `extend/InputPassword.vue`——明文/密文切换是 TextInput 静态 `type` 不具备的真实交互态（参照同层 `InputSearch` 的独立价值判据）；切换态 eyeOff 用组件内联 SVG，**不外溢改动上游冻结的 `src/data/icons.ts`**（曾误改 icons.ts，被 `FIDELITY: FAIL drifted=1` 抓到，回退并改自包含）。其余 `merged` 项（Form/Table 列/Typography 等）按设计为配置/插槽驱动，拆分即套壳，维持不动；`Textarea` 当时按 TextInput multiline 的转封装判断不拆（该结论已被后续 2026-10-16 复核推翻，见同日 Textarea 条目）。`arco-component-parity.json` 翻转该条为 `covered`（covered 98→99，merged 33→32）。
- **验证**：核对页浏览器 DOM 实测 **148/148 挂载、0 渲染异常**，左侧导航 10 类、数据输入计数 31 与守卫一致；InputPassword 点击切换 `password↔text`、`aria-pressed` 翻转、eyeOff 内联路径渲染均实测通过；`CATEGORIES: PASS(148)`、`CATALOG: PASS(148)`、`COMPONENT_PARITY: PASS(covered:99 merged:32)`、`PARITY: PASS(74)`、`INVENTORY: PASS(123)`、`FIDELITY: PASS(240 本地/139 上游)`、`GUARD_SELFTEST: PASS`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。
- **落点**：新增 `component-library/src/data/component-categories.ts`、`component-library/src/components/extend/InputPassword.vue`、`scripts/check_component_categories.mjs`；修改 `component-library/showcase/{Showcase.vue,ShowcaseNav.vue,demo-data.ts}`、`scripts/build_component_catalog.mjs`、`references/arco-component-parity.json`、`references/component-catalog.{md,json}`、`SKILL.md`、`component-library/LOCAL-GUIDE.md`。

## 2026-10-16 · 补齐 Descriptions 描述列表组件（组件 148 → 149）

- **触发**：延续同一 Goal 的 Arco 组件菜单目录逐个核对，在「数据展示」品类发现 `Descriptions`（描述列表/键值详情卡）是一等缺失形态。
- **真缺判定**：`Descriptions` 与既有 `KeyValueReadout`/`SpecPlate` 不是同一形态——后两者是单行键值条与规格铭牌样式，不具备「多列网格 + label/value 版式 + span 跨列 + 带边框表格式 + 标题与 extra 插槽」的描述列表语义；Arco 把它列为独立组件，按 `merged` 归并会掩盖真实可用的详情卡能力，故升级为 `covered` 独立实现。
- **组件**：`extend/Descriptions.vue`，props `data`（`{label,value?,span?}[]`）/`title`/`column`(默认 3)/`bordered`/`layout`(horizontal|vertical)，`extra` 插槽。`colSpan` 在 computed 里预计算并钳制到 `[1, column]`——Vue 模板表达式沙箱没有 `Math`，直接在模板里调用会运行时报错。
- **自修三坑**：① 模板引用 `Math.min` 失败 → 移入 computed 预计算；② `bordered` 初版用 `nth-child` 画分隔线，遇跨列项即错位 → 改为容器 `gap:1px` + 背景 `var(--line)`、单元格背景 `var(--surface)` 的透缝法，对任意 span 都稳健；③ 残留一条永不命中的 `:has()` 空规则 → 删除。
- **核对页适配**：`demo-data.ts` 增加 `Descriptions` 样本（订单详情，`column:1`——261px 的画廊格子放 3 列会把值挤没）；`component-categories.ts` 把 `Descriptions` 归入 display；`arco-component-parity.json` 中 `Descriptions` 登记为 `covered`（独立实现，非借 `KeyValueReadout` 的 `merged`），当前磁盘分布 `covered:99 / merged:32`（`COMPONENT_PARITY: PASS`）。
- **验证**：以真实磁盘与守卫为准——`CATEGORIES: PASS（10 类，覆盖 149）`、`CATALOG: PASS(149)`、`COMPONENT_PARITY: PASS`、`PARITY: PASS(74)`、`INVENTORY: PASS`、`FIDELITY: PASS`、`GUARD_SELFTEST: PASS`、`POLLUTION: PASS`、`vue-tsc + vite build` 成功、单测全绿；核对页浏览器挂载 149/149、0 渲染异常（详见本轮收口证据）。
- **落点**：新增 `component-library/src/components/extend/Descriptions.vue`；修改 `component-library/src/data/component-categories.ts`、`component-library/showcase/demo-data.ts`、`references/arco-component-parity.json`、`references/component-catalog.{md,json}`、`SKILL.md`、`component-library/LOCAL-GUIDE.md`、本文件。
## 2026-10-16 · 补齐 Form 表单容器并把核对页改为可操作（组件 149 → 150）

- **触发**：同一 Goal 续做时用户追加要求「showcase.html 我们希望组件是完善的，单独的组件可以支持简单的使用，而不是完全静态的」。
- **真缺判定（Form）**：Arco 的 `Form` 此前被标 `merged`（由 Field/SearchForm/FormDialog 覆盖）。核对 `src/components/layout/PasswordDialog.vue` 与 8 个 `views/system/*.vue` 后发现，9 个真实调用点都在重复同一段编排：自建 `errors` ref → 调 `utils/validate` → 判 `Object.keys(errors).length` → 拦截提交。这是可上提的真实能力缺口，不是套壳：`ui/Field.vue` 属上游冻结层不可改，用作用域插槽把 `errors` 交回调用方是唯一不落补丁的落点。`SearchForm` 经查无校验职责，不冲突。
- **组件**：`extend/Form.vue`，props `model`/`rules`/`layout`，作用域插槽透出 `errors`/`submit`/`validate`/`clear`，emits `submit`/`invalid`。排布复用上游 `components.css` 的 `.form-grid`（两列 + `.span-2` 通栏），不自造第二套栅格——否则 `Field` 的 `span`/`wide` 在表单内失效。
- **核对页可操作化（根因修复，非加开关）**：`showcase/Showcase.vue` 此前把 `demoProps` 的一次性字面量直接绑给组件，受控组件（输入、开关、标签页、下拉、树、表单）点了不生效。改为把每个格子的 props 提升为 `liveProps` 响应式状态，并按 `update:<已有 prop 键>` 约定自动回写；`Steps` 这类不走 `update:` 而用自定义 `change` 上抛的组件，单独登记事件写回。回写键由组件已有 props 派生，不维护第二份清单。
- **顺带修掉的真实缺陷**：① `ResizeBox` 的 demo 用 `resize: () => null` 覆盖了组件自带拖拽把手，核对页因此失去可拖拽入口 → 不再覆盖该插槽；② `DataTable`/`Notification`/`Image`/`Steps` 的 demo 未开启 `selectable`/`closable`/`preview`/`clickable`，组件本可交互却被展示成静态 → 补开；③ 我把 Form 的 `model`/`rules` 误写进 `demoSlots`，产生两个重复的 `case 'Form'`（第二个永不可达、字段数为 0）→ 归位到 `demoProps`。
- **验证（真实浏览器 DOM，非静态）**：核对页 **150/150 挂载、0 渲染异常**，左侧导航 10 类，数据输入 32 / 数据展示 31 与守卫一致；TextInput 打字保留 `罗德X`、Switch `aria-checked` false↔true、Tabs 受控 active 迁移且 disabled 项被忽略、Segmented 切换、Collapse 展开收起、Tree 选中与折叠、InputNumber 10→11、DataTable 勾选生效、Dropdown 开→选→闭环、Image 预览遮罩 teleport 到 body 且点击关闭、Tooltip/Popover 悬停出浮层（全局 2 层）、Form 点提交后必填错误落位。**40 个无操作句柄的组件经逐个判据复核均为语义只读件**（图标、标签、进度、图表、骨架、水印、版式等），不属于缺陷。
- **取证陷阱（记入经验）**：`innerHTML` 比较与「卡片内查找」都不能判定 Teleport 到 body 的浮层组件是否可交互；核对页的浮层类（Dropdown/Image 预览/Tooltip）必须查 `document` 而不是查 `.sc-cell-body`。
- **行数收口**：受控回写逻辑一度把 `Showcase.vue` 从 169 行推到 202 行（越过仓库 200 行基准），按同级 `use-anchor-nav.ts` 的惯例抽出 `showcase/use-live-props.ts`（30 行）后回到 174 行；期间先误写成渲染期建 handler 的 `createLiveProps(name,state)`，改为 setup 期一次性建好状态与处理器，避免每次渲染重建闭包。过程中产生的重名文件 `live-props.ts` 已删除。
- **落点**：新增 `component-library/src/components/extend/Form.vue`、`showcase/use-live-props.ts`；修改 `src/data/component-categories.ts`、`showcase/{Showcase.vue,demo-data.ts}`、`references/{arco-component-parity.json,component-catalog.md,component-catalog.json}`、`SKILL.md`、`component-library/LOCAL-GUIDE.md`、本文件；`doc/6-review/` 与 `doc/5-tests/` 对应记录。
## 2026-10-16 · 补齐 Textarea 自动高度与字数统计（组件 150 → 151）

- **触发**：同一 Goal 续做，继续按 Arco 组件菜单目录核对「数据输入」品类。
- **推翻先前判断的依据**：同日早先记录认为 `Textarea` 只是 TextInput multiline 的转封装，不值得拆。实际读 `src/components/ui/TextInput.vue` 的模板后确认：multiline 分支只有固定 `rows`、`maxlength` 和 `resize: vertical`，**没有自动高度、也没有字数统计**。这两项是 Arco Textarea 的真实能力，不是样式差异，因此「纯转封装」的前提不成立，先前结论已在原条目就地标注为被推翻。
- **为什么不直接给 TextInput 加开关**：`ui/TextInput.vue` 属上游冻结层，改它会被 `FIDELITY` 字节基线抓到（本轮已因误改 `icons.ts` 被 `drifted=1` 抓过一次），所以在 extend 层独立实现。
- **组件**：`extend/Textarea.vue`，props `modelValue/placeholder/disabled/readonly/invalid/rows/autoSize/maxRows/maxlength/showCount`。描边复用全局 `.input-shell.is-multiline`（与 `Mention` 同口径），不自造一套输入框外观。
- **自修三处**：① `is-auto` 类只在 CSS 出现却没绑到元素上（死样式）→ 绑到 `autoSize`；② 用 `el.value.lineHeight` 读行高（HTMLTextAreaElement 不暴露该属性）→ 改 `getComputedStyle` 解析；③ 计数行用固定 `id`，同页多实例会产生重复 id → 改为随机后缀，并与 `aria-describedby` 联动。
- **回环防护**：自动测高本身会改 textarea 高度，最初用 `ResizeObserver` 观察同一元素会造成「测高→尺寸变化→再测高」回环；改为只在**宽度**变化时重算（宽度变才会改变折行数），高度变化直接忽略。
- **验证**：核对页真实浏览器实测——151/151 挂载、0 渲染异常；输入八行文本高度 `64px → 101px` 并在 `maxRows: 5` 上限处停住转内部滚动（`overflow-y: auto`）；字数实时跟随 `34 / 200 → 31 / 200`；`[id^=ta-count-]` 数量与计数元素数量一致。守卫：`CATEGORIES: PASS(151)`、`CATALOG: PASS(151)`、`COMPONENT_PARITY: PASS(covered:101 merged:30)`、`PARITY: PASS(74)`、`FIDELITY: PASS(244 本地/139 上游)`、`POLLUTION: PASS`、单测 21/21、`vue-tsc + vite build` 成功。
- **落点**：新增 `component-library/src/components/extend/Textarea.vue`；修改 `src/data/component-categories.ts`、`showcase/demo-data.ts`、`references/{arco-component-parity.json,component-catalog.md,component-catalog.json}`、`SKILL.md`、`component-library/LOCAL-GUIDE.md`、本文件；同日早先条目已就地标注判断被推翻。

## 2026-10-16 · 组件库后台化：核对页迁入真实路由 + 覆盖率守卫 + 登记缝隙（组件 151 全覆盖）

- **触发**：用户 Goal「管理后台应该把组件都用上，才是完整组件库后台示例；有后台就不需要独立 html」。
- **根因（为什么不能改现有页面）**：全部 139 个上游文件（含每个业务视图、路由与页面登记表）被 `verify_fidelity.py` 逐字节冻结，且没有任何冻结文件 import 本地模块 —— 覆盖率无法靠改上游页面提高，必须新增本地后台页面并开出一条登记缝隙。
- **登记缝隙做法**：新增 `src/data/view-registry.ts` 作本地页面唯一登记处，`src/composables/auth.ts` 的 `COMPONENT_MAP` 首项展开它（+2 行）。缝隙不按「整文件豁免」处理——那会让该行为文件后续真实改动静默不可见；改为在 `verify_fidelity.py` 声明精确允许行，扫描时先剥离这些行再要求剩余字节等于上游，缝隙外任何改动仍报 `DRIFTED`。变异自测：追加一行未声明注释 → `FIDELITY: FAIL drifted=1`；移除后恢复 PASS 且校验和回到注入前。
- **覆盖率守卫**：新增 `scripts/check_admin_component_coverage.mjs`（裁决入口）+ `admin_coverage_graph.mjs`（访问器）+ `admin_coverage_reach.mjs`（引用边遍历）+ `admin_coverage_parse.mjs`（源码解析口径）。判据当场从磁盘推导：组件全集取 `src/components` 递归、入口取 `src/views/**` + `src/router/**` + `src/App.vue`；边必须同时满足「import 命中该文件」与「导入的本地名真被使用」，只 import 不渲染不计入，防止一行批量导入刷满覆盖率。迁移前基线为 60/151，迁移后 151/151。变异自测：把示例页发现面从全部组件目录收窄到 `ui/` 子目录 → 立刻 `FAIL (75/151)` 并列出缺口。
- **双轨收敛**：独立入口 `showcase.html` 与 `showcase/` 用可逆搬迁移到系统临时目录 `pg-retired-showcase`（未删除：本仓库配置了 Git content filters，`git ls-files` 无法作为还原兜底路径，故保留物理副本）。构建产物只剩 `dist/index.html`，全仓 `showcase` 引用扫描命中 0。
- **菜单单一真相源**：`mock/server.mjs` 直接 import `src/data/component-categories.ts`，用 `COMPONENT_CATEGORY_ORDER` 映射生成「组件库」目录下的 10 条分类菜单，不再手抄第二份分类清单。
- **行数基准返工**：首版守卫 250 行、还原度守卫 270 行、可达图工厂函数 157 行均越过仓库基准（文件 200 / 函数 80）。返工为守卫各拆两到四个模块（最终 90 / 167 / 107 / 115 与 151 / 181 行，最大函数 23 行），示例页样本 666 行单文件无损拆为四类样本文件；拆分只做搬运，守卫输出与拆分前逐项一致。
- **重复逻辑收敛**：barrel 再导出的名称拆解原在守卫里内联重写一遍，改抽到解析侧 `parseReExports` 单一口径，并与 `parseClause`（导入语义：默认导入落到 `default`）区分开。barrel 通道在当前引用图里经插桩实测被调用 178 次，属真实遍历通道而非未验证分支。
- **行尾符返工**：拆分样本文件时按默认方式写出，导致 `demo-props.ts` / `demo-slots.ts` / `demo-display-samples.ts` 三个文件为 CRLF，与组件库 `.gitattributes` 的 `* text=auto eol=lf` 及同目录其余文件冲突；按字节归一后复核 CRLF=0，还原度守卫复跑仍 PASS。
- **污染豁免**：全仓扫描命中 2 条均在上游冻结基线内（`scripts/session-regression.py` 的本地登录默认口令分支、`src/composables/motion.ts` 的 `revealPage` 死导出），非本轮引入且 `FIDELITY` 禁止改动；前者登记进 `component-library/.test-pollution-allowlist` 并写明理由，后者转 6-review 判断（结论：上游既有，不动）。增量口径 `POLLUTION: PASS`。
- **验证**：`ADMIN_COVERAGE: PASS(151/151)`、`CATEGORIES: PASS(10 类 151)`、`CATALOG: PASS(151)`、`FIDELITY: PASS(244 本地/139 上游)` + `SEAM`、`GUARD_SELFTEST: PASS`、`INVENTORY: PASS`、`COMPONENT_PARITY: PASS`、`PARITY: PASS(74)`、`POLLUTION: PASS`、`vue-tsc` 零报错、`vite build` 成功、单测 21/21；真实浏览器十个分类挂载 11/8/16/33/31/12/6/20/8/6=151、空白卡片 0、渲染错误 0，输入回写、开关翻转、弹层开合、提示与确认宿主均出现真实状态迁移。详见 `doc/5-tests/2026-10-16_193800_REQ-PEARL-ADMIN-GALLERY-001_组件库后台化_测试主文档.md`。
- **取证陷阱**：⓪ 变异自证的还原要按字节不能按文本——用文本改写还原登记缝隙文件时多留一个文件末尾空行，还原后仍判漂移且校验和与注入前不一致；改按原始字节截去多余换行才真正复原，故还原完成判据是校验和一致而非守卫恢复。① 分类切换探测必须等标题文本切到目标分类后再计数，只等「卡片数>0」会把上一页残留卡片读成当前页（曾误报 layout=11，真实 8）；② `history.pushState` 不通知 vue-router，验证侧栏跳转要点真实按钮；③ 标签页隐藏时上游帧循环主动停帧，画布类组件只能在前台取像素；④ 本仓库单元测试入口是 `npm run test:unit`（Node 原生 test runner），直接调第三方 runner 会因找不到用例而全红，不属于项目回归。
- **落点**：新增 `src/views/gallery/`（示例页、单元格、发现入口、受控回写、四类样本）、`src/data/view-registry.ts`、四个守卫模块、`component-library/.test-pollution-allowlist`；修改 `src/composables/auth.ts`（2 行缝隙）、`mock/server.mjs`、`scripts/verify_fidelity.py`、`SKILL.md`、`component-library/LOCAL-GUIDE.md`、本文件；新增 `doc/3-实施/`、`doc/5-tests/`、`doc/6-review/` 对应记录；退役 `showcase.html` 与 `showcase/`。

## 2026-10-19 · design 组件库术语映射纠偏

- **触发与来源**：用户明确纠正术语：“design 组件库”默认就是 `frontend-design` skill 中的组件库；要求按该库调整前端时不得误判。
- **通道与裁决**：内部规则更新；将“design 组件库 / design组件库 / 按 design 组件库调整前端”明确指向本 skill 的 `component-library/` 珍珠玻璃组件库，优先于按页面类别选择默认入口；仅用户明确指定另一套库时才切换。
- **落点**：`SKILL.md` 的组件库路由增加术语优先级与默认指代，并继续以 `references/component-catalog.md` 为选型索引；知识库笔记只作该规则的检索入口。
- **同域去重**：核对 `frontend-component-rules` 已将 UI 主路线交给 `frontend-design`，`frontend-ui-visual-rules` 不绑定任何 UI 库默认外观与本次采用内置库不冲突；无重复规则或引用层叠。
- **独立复核**：D1-D7 改前为 8/8/7/8/7/7/8，改后为 9/9/9/8/9/9/8；D8 未执行真实场景 prompt，不评分。
- **验证**：`quick_validate.py` → Skill is valid；`git diff --check` → PASS；独立只读路由审查 → PASS。描述和 `##` 级标题未改，无需刷新技能字典。
- **环境依赖**：N/A。

## 2026-10-19 · 珍珠玻璃组件库路径与安装资产恢复

- **触发与证据**：关联会话 01a15229-342e-7a40-968f-30441c03cd93 中，已加载的 C:/Users/luode/.agents/skills/frontend-design 缺少 component-library/、目录索引与脚本；随后 WSL 因 D 盘挂载失败而得到空搜索结果，并误把它当成资源不存在。
- **根因与裁决**：规范源 D:/谷歌云盘/luode-skills/frontend-design 有完整目录，但 skill 正文未明确资产路径相对当前加载的 SKILL.md 根目录，也未说明目标项目无需自带组件目录、安装副本缺资产时如何回退。规则补齐路径基准、规范源回退、WSL 挂载检查、缺失结论门槛与分发完整性。
- **安装副本修复**：更新已安装副本的 SKILL.md，补入缺失的组件目录、脚本和目录索引；保留该副本原有的 references/source-notes.md 与已有 apple-fluid-design.md，未复制 .npm-cache/、node_modules/、dist/ 或 .git/。
- **同域去重**：frontend-component-rules 将 UI 主路线交给 frontend-design；frontend-ui-visual-rules 不声明默认 UI 库。本修复归 frontend-design 唯一维护，不扩散到相邻 skill。
- **验证**：UTF-8 回读、安装资产逐文件哈希比对、quick_validate.py、git diff --check；只调整正文与三级标题，未修改 description 或二级标题，技能字典无需刷新。
- **评分（间隔后的第三方视角）**：按 darwin-rubric 对已记录基线 D1-D7=9/9/9/8/9/9/8（加权 65.3/75）复评，得 9/9/10/8/10/10/8（68.3/75，+3.0）；边界、路径具体性、资产可达性提升，其他维度无退化。D8 未运行真实场景 prompt，本轮未要求 prompt 实测，故不评分；未把先前独立审阅结果冒充本轮评分。

- 环境依赖：Windows 宿主安装路径可读；组件库开发 / 构建命令未运行（本轮只修复 Skill 规则与分发资产）。

## 2026-10-19 · design+组件库设计思考与页面重设计闭环

- **触发与来源**：用户进一步明确“design 组件库”的目的不止替换控件，还要重新思考页面设计并优化样式布局；来源为内部规则更新，不是外部 skill 吸收。
- **原子裁决**：合并“默认进入 design+ 模式”“先锁定业务边界”“先做页面设计诊断”“组件选型服务于布局”“统一令牌 / 材质 / 动效表达”“交付必须给出设计决策摘要”六条规则；保留现有第 1～5 步审美工作流作为通用设计流程；拒绝新增独立 skill，也拒绝把完整视觉流程复制到相邻 skill。
- **落点**：`SKILL.md` 新增“design+组件库：组件落地与页面重设计同时完成”，并在工作流第 2～5 步补充页面骨架、布局重排、冲突样式自查与交付摘要；`frontend-ui-visual-rules/SKILL.md`、`frontend-component-rules/SKILL.md` 只补职责指向，统一由 `frontend-design` 维护 design+ 主规则。
- **边界**：默认做一轮页面级重排审视，但不为形式强行大改；用户明确要求只换组件、只修组件或不改布局时，按用户边界执行组件级最小改动；默认不改查询、接口、权限和业务逻辑。
- **同域去重**：范围 = `frontend-design`、`frontend-ui-visual-rules`、`frontend-component-rules`；发现 0 处重复流程、0 处门控层叠、0 处散落产物，兄弟 skill 仅保留单句职责引用；引用链与安装副本均复核，**PASS**。
- **验证**：规范源与 `C:/Users/luode/.agents/skills/frontend-design/SKILL.md` 的新规则回读一致；组件库路径、目录索引与 design+ 术语检索均可达；未改 description 或 `##` 级标题，技能字典无需刷新；本轮不涉及前端源码，未运行构建或业务测试。
- **评分**：独立复核代理两次因模型容量不足未启动，按 darwin-rubric 改用间隔后的第三方视角静态复评；D1-D7 改前沿用 2026-10-19 基线 `9/9/10/8/10/10/8`（68.3/75），改后为 `9/10/10/8/10/10/9`（71.3/75，+3.0），提升来自 design+ 工作流、边界和架构闭环；D8 未运行真实场景 prompt，不把静态复核冒充实测。
- **环境依赖 / agent 通用性**：环境依赖 N/A；规则落点为通用 `SKILL.md` 与 references，所有 agent 可读取执行。
