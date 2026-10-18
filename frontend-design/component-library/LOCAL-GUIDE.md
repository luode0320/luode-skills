# 珍珠玻璃组件库（Pearl Glass Component Library）

> 来源：[scaffold-master](https://github.com/wbr664393425-lgtm/scaffold-master) `scaffold-vue`，
> 上游冻结 commit `577079e9a347555fadddd3865fc0bbcdb00d9fb4`，MIT License（GSAP 除外，见 LICENSE 注意事项）。
> 本目录是 `frontend-design` skill 的**默认前端组件库**：用户要求做后台/中后台页面 design 时，默认走这一套。

## 目录结构

```
component-library/
├── src/
│   ├── styles/          七层样式：tokens → base → materials → components
│   │                    → instruments → layout → pages（main.ts 按此顺序引入）
│   ├── components/
│   │   ├── ui/          27 个基础控件（Button/DataTable/Modal/Drawer/Select…）
│   │   ├── business/    20 个业务组件（ListPage/BoardView/PermissionMatrix…）
│   │   ├── workspace/   8 个本地扩展版式组件（BentoGrid/BentoCard/Band/ShareList…）
│   │   ├── extend/      78 个本地扩展组件：Arco 品类对齐（Tabs/Steps/Upload/Tooltip…）
│   │   ├── charts/      6 个自研图表（TrendChart/BarChart/TickRing/HeatGrid/Swimlane/RelationGraph）
│   │   ├── layout/      6 个外壳组件（AppShell/Sidebar/Topbar/CommandPalette…）
│   │   ├── Icon.vue / NeuralNet.vue
│   ├── composables/     14 个组合式函数（motion/appearance/focus/toast/neural/viewport…）
│   ├── data/            图标表与展示数据
│   ├── directives/      权限指令
│   ├── utils/           csv/clipboard/validate/heatmap 等纯函数（含单测）
│   ├── views/           16 个参考页面（Dashboard/Login/system/monitor/tool/gallery）
│   ├── api/             API 层（组件库默认走 mock，见下）
│   └── router/          路由
├── mock/                本地 mock 中间件（新增，不属于上游）
├── DESIGN.md            上游设计规范（视觉语言/令牌表/版式/动效语态）
├── LICENSE              上游 MIT 许可证
└── package.json         仅 vue / vue-router / gsap 三个运行时依赖
```

> 上游共 61 个组件；`workspace/` 8 个是本仓库新增的**本地扩展版式层**，`extend/` 是本仓库新增的 **Arco 品类对齐层**（两者都不属于上游、不参与还原度基线）。`extend/` 用于把组件品类广度补齐到 Arco Design Vue 同等水平：`../references/arco-parity.json` 逐品类登记覆盖状态，`../references/arco-categories.json` 是真实 Arco 包品类参照（可按文件内 `extract_command` 重建），`../scripts/check_arco_parity.py` 做三重校验——标 `gap` 却已实现报 `STALE_GAP`、标 `covered` 但文件缺失报 `DANGLING`、清单与真实品类对不上报 `PHANTOM_CATEGORY`（虚构）/ `MISSING_CATEGORY`（漏登），全部清零才算对齐完成。

> **品类对齐之外还有组件粒度对齐**：一个 Arco 品类目录里往往导出多个组件（如 `date-picker/` 导出 `DatePicker`/`RangePicker`/`MonthPicker`/`WeekPicker`/`QuarterPicker`/`YearPicker`），只对平目录会漏掉子组件。因此另有 `../references/arco-component-parity.json` 逐条登记 Arco 实际导出的 **131 个组件名**（`../references/arco-components.json` 为真实导出参照），`../scripts/check_arco_component_parity.py` 做五重校验：`COVERAGE_GAP`（gap 未清零）、`STALE_GAP`（标 gap 却已实现）、`DANGLING`（标 covered 但文件缺失）、`PHANTOM_COMPONENT`（登记了 Arco 没有的）、`MISSING_COMPONENT`（Arco 有但漏登），全部清零才算对齐完成。

## 组件目录索引与示例页

- **选组件先查 `../references/component-catalog.md`**：全部 152 个组件的引入路径、props、事件、插槽、导出类型、用法骨架与参考实现位置，由 `../scripts/build_component_catalog.mjs` 从源码自动生成；机器可读版为 `../references/component-catalog.json`。
- **人工核对真实渲染**：`npm run dev` 后登录后台，进入侧栏「组件库」分组，路由 `/gallery/<分类键>`（general/layout/navigation/inputs/display/feedback/charts/business/workspace/shell）。示例页本身就是后台页面——走真实 `AppShell` 壳层、真实动态路由与权限，不再另开独立 html 入口。逐卡显示组件名、仓库内路径与挂载状态；必填 props 与插槽样本由 `src/views/gallery/demo-props.ts`、`demo-slots.ts` 提供，保证 slot 驱动组件（Button/Tag/Field/Panel/Band/BentoCard…）也能看到真实外观而不是空白卡片。
- **分类导航**：分类集合与顺序取自单一真相源 `src/data/component-categories.ts`，菜单条目由 `mock/server.mjs` 从同一模块生成，页面按路由路径末段取当前分类；三处共用一份数据，新增分类只改数据源。搜索框按组件名与路径实时过滤。
- 组件全集靠 `entries.ts` 的 `import.meta.glob('../../components/**/*.vue')` 从磁盘发现，页面不维护第二份清单；`use-live-props.ts` 把每个组件的样本 props 提升为可回写状态，受控组件在页面上真能被点动（浅响应，避免深响应把嵌套 ref 拆包）。
- 三类需要交互才可见的组件在卡内有专门入口：弹层类（Modal/Drawer/FormDialog/GeneratorPipeline/AppearanceDialog/CommandPalette/PasswordDialog）用「预览弹层」按钮开合；全局宿主（ToastHost/ConfirmHost）用「触发宿主」按钮调用；画布类（NeuralNet/Sidebar/AskDock）由示例页给定位定高容器，页面在前台时正常绘制（上游帧循环在标签页隐藏时主动停帧，属预期）。
- 组件契约变化后重跑 `node ../scripts/build_component_catalog.mjs`，并用 `--check` 校验索引与磁盘同步；收口前跑 `node ../../frontend-design/scripts/check_admin_component_coverage.mjs`（必须 `ADMIN_COVERAGE: PASS`，152 个组件全部在后台可达）。


## 使用方式

```bash
cd frontend-design/component-library
npm install
npm run dev        # http://localhost:5173，登录页任意账号密码可进（mock 放行）
```

**Windows 双击启动**：直接双击本目录的 `启动组件库.bat`。脚本会切到自身目录、检查 Node（缺失时给出安装地址并停在窗口）、依赖缺失时自动 `npm install`，然后拉起 Vite 并自动打开浏览器；关闭窗口或按 `Ctrl+C` 即停止，端口随进程释放。

> 该 bat **必须保持纯 ASCII**：`cmd.exe` 按字节偏移逐行读取批处理文件，若在文件内 `chcp` 切换代码页后再出现中文行，后续行会被从中间截断并当作命令执行（实测报 `'口，端口随进程退出释放。' is not recognized...`）。所以中文提示统一由 `node -e` 以 `\uXXXX` 转义输出，`chcp 65001` 只影响显示。新增提示时沿用同样写法，不要直接把中文写进 bat。

## 约束（还原度守卫）

- `src/` 下**所有上游文件必须与上游基线逐字节一致**，禁止手改——视觉与行为还原度靠字节级一致保证。上游冻结面包含七层样式（`src/styles/*.css`）与 `src/main.ts`，因此新增组件**不能**改样式层或入口文件。
- 外壳级绘制缺陷（不属于新增组件）走两条受控通道：修样式只写新增文件 `src/styles/overrides.css`（本地覆盖层，不改冻结 CSS 一个字节）；若必须让它在入口生效，把引入行登记进 `../scripts/fidelity_upstream.py` 的 `SANCTIONED_SEAMS`，`verify_fidelity.py` 会剥离这些声明行后要求逐字节相等，并在通过时打印 `SEAM:` 行说明。未登记的入口改动一律判 `FIDELITY: FAIL`。
- 需要 hack 时只改 `mock/`、`src/views/gallery/`、配置层（vite.config.ts 等）或以新增文件扩展；`workspace/` 与 `extend/` 是本仓库新增的本地扩展目录，可自由演进。
- `extend/` 内组件的样式一律写在组件自身的 `<style scoped>` 里，且只允许引用 `src/styles/tokens.css` 里的 CSS 变量令牌（禁止硬编码色值）；材质复用全局 `.m-*` 类，动效复用 `src/composables/motion.ts` 的 `overlayEnter/overlayLeave/settlePop` 等入口。这是在不触碰冻结样式层的前提下保持视觉一致的做法。
- 每次改动后运行（脚本在 skill 根目录的 `scripts/`，不是本目录）：
  - `python ../scripts/verify_fidelity.py`（联网权威）或 `--offline` → `FIDELITY: PASS`
  - `python ../scripts/verify_fidelity_selftest.py` → `GUARD_SELFTEST: PASS`
  - `python ../scripts/test_component_inventory.py` → `INVENTORY: PASS`
  - `python ../scripts/check_arco_parity.py` → `PARITY: PASS`（缺口 0）
  - `node ../scripts/build_component_catalog.mjs --check` → `CATALOG: PASS`
  - `node ../scripts/check_shadow_clipping.mjs` → `SHADOW_CLIP: PASS`（校验外壳、示例卡、登录画布三处容器的四向留白都覆盖其内柔影的四向延展；留白被清零时阳性对照必须转 FAIL，防止「边角阴影块」被 `overflow: clip` 切成方形暗块回归）
  - `python ../scripts/check_corner_occlusion.py` → `CORNER_OCCLUSION: PASS`（需先启动本地开发服务。逐页扫描全部菜单页，比对圆角父级与贴角子元素的圆角：粗描边父级的内弧被直角子元素盖住、或细描边/无描边父级的方角子元素外露，都判 FAIL；父级自身 `overflow: hidden/clip` 时子元素被裁到圆角内，不判。内置两条阳性对照：去掉 `.rail` 内弧圆角必须报 `border-occluded`，注入「20px 圆角父级 + 直角子元素」必须报 `corner-mismatch`）
  - `python ../scripts/check_help_tip_interaction.py` → `HELP_TIP: PASS`（需先启动本地开发服务。实测 `HelpTip` 的悬停浮出、指针移出收起、键盘聚焦、Esc 收起与 `aria-describedby` 清除、焦点保持（悬停后聚焦再移开指针，说明必须仍在）、视口夹取、长文 260px 上限；沿 `offsetParent` 祖先链检查浮层没有被滚动容器裁切）
  - `python ../scripts/check_content_padding.py` → `CONTENT_PADDING: PASS`（需先启动本地开发服务。逐页扫描全部示例页，候选容器 = 四边有可见边框、带非透明背景，或本身是 `button` / `menuitem` 等交互控件；用 Range 取文本字形与容器边框内沿比对，**左右任一方向 < 4px 即判 FAIL**。无可见边界的纯文字按钮与布局 div、圆形容器（头像）、自身可滚动的容器按语义豁免。路由从分类真相源派生、不手写清单。判据必须配阳性对照：移除 `MenuNode.vue` 的 `padding-right` 后应精确报出 1 处 `x-menu-item > .x-menu-label` 贴边）
  - `python ../scripts/check_demo_visibility.py` → `DEMO_VISIBILITY: PASS`（需先启动本地开发服务。逐页扫描全部示例页，三条判据：空白卡、出卡、塌缩（宽高都 < 4px，1px 竖线豁免）。定位包装层不参与判定。内置阳性对照与示例卡数量下限、空页检测三项自证。判据必须配阳性对照：把 `BackTop.vue` 的 `docked` 强制为 `false` 后应精确报出 4 处 `BackTop ... all-outside | BUTTON.x-backtop`）
  - `python ../scripts/check_demo_guides.py` → `DEMO_GUIDES: PASS`（需先启动本地开发服务。逐页扫描全部示例页，四条判据：每张卡头有 `.x-help` 图标、提示含「组件说明 + 本格示例」两段、非基础示例不退回默认形态、同组件不同变体提示不重复。说明数据源 `src/data/component-guides.ts`，本格差异由 `views/gallery/demo-guides.ts` 按该格 props 推导。判据必须配阳性对照：差异推导恒返回默认文案必须报「非基础示例却写默认形态」，移除 `<HelpTip>` 必须报「缺少提示图标」）
  - `python ../scripts/build_font_overrides.py --check` → `FONT_OVERRIDES: PASS`（字号整数化派生块同步校验：从冻结的 `src/styles/*.css` 自动提取非整数字号规则的选择器，按 10.5→11 / 11.5→12 / 12.5→13 / 13.5→14 / 14.5→15 生成 `overrides.css` 的受管块。上游升级后若不重跑生成，`--check` 会报失配。该块由 `BEGIN/END GENERATED` 包裹，禁止手改）
  - `python ../scripts/check_demo_health.py` → `DEMO_HEALTH: PASS`（需先启动本地开发服务。逐页扫描全部示例页，九条判据：渲染异常、框架告警（控制台 error 与 `[Vue warn]`/`Invalid prop`）、坏文本（`NaN`/`undefined`/`Invalid Date`/`[object Object]`）、坏图、零尺寸图标、交互元素缺可访问名、文字裁切无省略号、页面横向溢出、低对比文字（对比度 < 1.5，浅色与暗色两个主题都要扫）。视觉隐藏元素豁免裁切判定；半透明与禁用态元素豁免对比度判定；文字与不透明底之间有渐变或图片背景时不判对比度。控制台豁免面集中在 `KNOWN_CONSOLE_ALLOW` 一处，每条写明根因与解除条件。`--selftest` 跑阳性对照：注入一张放齐七类违例的坏卡与两条坏控制台消息，逐条断言判据会报，并回显注入前后卡数证明扫描根覆盖。按 diamond 拆成 `demo_health_env.py`（路由派生与页内量测脚本）、`demo_health_judges.py`（豁免面与控制台判据）、`demo_health_selftest.py`（阳性对照）、`check_demo_health.py`（入口与全量流程）四个同级文件）
  - `node ../scripts/build_demo_events.mjs --check` → `DEMO_EVENTS: PASS`（事件表派生同步校验：从各组件 `defineEmits` 派生「组件 → 声明事件名」写入 `src/views/gallery/demo-events.generated.ts`，示例层据此把每个声明事件都接上一次可见反馈。组件改了 `emits` 未重跑生成即报 FAIL；生成物禁止手改）
  - `python ../scripts/check_demo_event_wiring.py` → `EVENT_WIRING: PASS`（需先启动本地开发服务。逐页扫描全部示例页，沿 `__vueParentComponent` 读卡内同名组件实例 vnode 上真实绑定的 `on*`，与派生事件表对账：声明了却没接处理器即判缺口（这类格子按钮点了没反馈，看着像坏控件）。事件名按 Vue 的 camelize 归一（`row-click` → `onRowClick`），否则带横线事件全量误报。`update:*` 由样本状态写回负责不计入；逐帧/逐秒/指针移动类事件走集中豁免面，豁免条目必须在事件表里真实存在。`--selftest` 跑六条阳性对照：未接必报、接上必不报、带横线不误报、`update:*` 不计入、多事件只报漏项、豁免面无失效条目。按 diamond 拆成 `demo_event_wiring_probe.py`（页内量测脚本、豁免面与缺口判定）与 `check_demo_event_wiring.py`（路由派生与全量流程）两个同级文件）
- 上游升级：重新冻结新 commit → `python ../scripts/verify_fidelity.py --write-baseline` 刷新 `../references/component-library-baseline.json`，并同步本文档与 `SKILL.md` 顶部的 commit 号。
