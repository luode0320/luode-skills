# 珍珠玻璃组件库（Pearl Glass Component Library）

> 来源：[scaffold-master](https://github.com/wbr664393425-lgtm/scaffold-master) `scaffold-vue`，
> 上游冻结 commit `577079e9a347555fadddd3865fc0bbcdb00d9fb4`，MIT License（GSAP 除外，见 LICENSE 注意事项）。
> 本目录是 `frontend-design` skill 的**默认前端组件库**：用户要求做后台/中后台页面 design 时，默认走这一套。

## 目录结构

```
component-library/
├── src/
│   ├── styles/          八层样式：tokens → base → materials → components
│   │                    → instruments → layout → pages → overrides
│   │                    （main.ts 按此顺序引入；前七层属上游冻结面，overrides 是本地覆盖层）
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

## 尺寸与 prop 语义

`DESIGN.md` 属上游基线、逐字节冻结，本地约定写在这里。

`size` 只表示**控件档位**，取值 `xs / sm / md / lg`，高度与字号分别读 `--control-h-xs|sm|md|lg` 与 `--fs-control-xs|sm|md|lg`。这组令牌定义在 `src/styles/overrides.css`，其中 `md` 直接别名到上游 `--control-h`（36px），既有页面不产生位移。

几何量与数据量不走 `size`，各用独立名字：

| 含义 | prop | 用在哪 |
| --- | --- | --- |
| 圆形直径（px） | `diameter` | `AvatarGroup` 头像、`Progress` 环形 |
| 图标边长（px） | `iconSize` | `HelpTip` 图标 |
| 精确间距（px） | `gap` | `Space`；`size` 仍可只给档位 |
| 文件字节数 | `UploadFile.size` | 上传记录，不是 UI 尺寸 |

上游冻结组件保留各自的 `size` 原义，调用前先查下表，不要假设它一定是档位：

| 组件 | `size` 的实际含义 |
| --- | --- |
| `Button` / `PermissionButton` | 控件档位 `md / sm` |
| `Metric` | 读数档位 `xl / l / m / s` |
| `Icon` / `IconButton` | 图标边长（px，默认 18 / 17） |
| `Avatar` | 头像直径（px，默认 32） |
| `TickRing` | 外环直径（px，默认 168） |
| `RelationGraph` | 珍珠球与刻度表盘直径（px） |

上游文件逐字节冻结，不改其 prop 名；本地扩展层（`extend/`）一律按上面的约定执行。

示例变体由 `../scripts/build_demo_variants.mjs` 从组件契约派生。同名 prop 在不同组件里量纲不同时，必须在脚本的 `NUMBER_VARIANTS_BY_COMPONENT` 里给出该组件自己的值域，否则会派生出越界示例（曾把 168px 的刻度环缩成 16px、把 44px 图标塞进 32px 按钮）。改完组件 props 后的生成顺序固定为：`build_component_catalog.mjs` → `build_demo_variants.mjs`，顺序颠倒会沿用旧契约。

## 字号标度

正文字号基准是 **14px**（`body` 与 `.btn` / `.table` / `.input-shell` 一致），最小字号 **12px**。字号只有 5 档，分 3 个整体档位，由 `data-font-scale` 切换：

| 档位 | caption | sm | body | lg | title |
| --- | --- | --- | --- | --- | --- |
| `compact` | 12 | 12 | 13 | 14 | 15 |
| `regular`（缺省） | 12 | 13 | **14** | 15 | 16 |
| `large` | 13 | 14 | 15 | 16 | 17 |

每档都显式给整数，不用 `calc` 缩放——1.1 倍会算出 15.4px 这种半像素，与「字号必须整数」的验收条件冲突。属性打在根元素是全局生效，打在任意容器上只影响该子树。

**三档的 caption 一律不低于 12px**：12px 是「辅助字号下限」这条验收条件本身，不能因为用户选了紧凑档就破例。紧凑档的收紧体现在 `body`（13px）与 `sm`（12px），而不是把最小字号再往下压。

5 档令牌的承载关系：

| 令牌 | 承载 | 迁移前 |
| --- | --- | --- |
| `--fs-caption` | 元信息、图表轴、角标、校验提示 | 10 / 10.5 / 11 / 11.5px |
| `--fs-sm` | 字段标签、标签胶囊、表头、次级正文 | 11.5 / 12px |
| `--fs-body` | 正文、按钮、输入、表格、导航 | 12.5 / 13px |
| `--fs-lg` | 面板标题、强调名称 | 13.5 / 14px |
| `--fs-title` | 区块标题、品牌名 | 14.5 / 15px |

16px 以上（页面标题 22px、读数 56 / 40 / 28px）不进标度：它们不承担「读不清」的问题，改动只有风险没有收益。

**为什么不直接改 `body`**：`.btn`、`.table`、`.input-shell` 历史上各自写死了字号，改基准碰不到它们。字号统一靠覆盖块，因此调整基准只改上表 5 个令牌值，不触碰冻结样式；这也是「字号可调」的唯一入口。

**与 `--fs-control-*` 的区别**：那组是「控件档位」（`xs / sm / md / lg`，配 `size` prop，经 `controlVars()` 转成 `--ctl-fs`），管同一个控件在不同尺寸下的字号；`--fs-caption / sm / body / lg / title` 是「文本角色」，管这段文字在信息层级里属于哪一档。两者数值有重叠但语义不同，不要混用。

**组件内字号已并入标度**：`extend/` 层 110 处 `<style scoped>` 字号已改为 `var(--fs-*)`，与页面级共用同一套档位，切换字号时组件内部同步跟随。剩余 6 处分落在 `layout/`、`business/`、`ui/`，属上游冻结文件不可改，且都是 11–12px 的辅助文字，影响面很小。

## 主色色板

主色由 `data-accent` 切换，预置 5 套：`blue`（珍珠蓝，缺省）、`teal`（青碧）、`violet`（丁香紫）、`moss`（苔绿）、`amber`（琥珀）。属性打在根元素是全局生效，打在任意容器上只影响该子树。

**加一套色板**：在 `../references/accent-palettes.json` 加一条（键 + 中文名 + 浅色种子 + 深色种子），重跑 `build_accent_palette.py`。不需要手写任何派生值——一套色板要出 12 个令牌 × 2 主题，手写必然漂移。

**主色必须拆成两个令牌**，因为两种角色的明度要求方向相反：

| 令牌 | 角色 | 要求 |
| --- | --- | --- |
| `--blue` | 文字、描边、图标、选中态 | 对内容底 ≥4.5:1 |
| `--blue-solid` | 实心按钮背景（白字压在上面） | 白字对比 ≥4.5:1 |

深底上当文字要够亮（L≥0.206），当背景配白字要够暗（L≤0.183），两个区间不重叠，一个令牌无法兼顾。实测不拆时，深色主题下 5 套色板的按钮白字只有 2.09–3.20。所以实心件（`.btn-primary` 等）必须读 `--blue-solid`，装饰性小圆点与竖条继续用 `--blue`。

种子色不达标时，生成器按 HSL 明度轴自动修正到达标并留 0.1 余量；修正后的取值与幅度用 `--report` 查看。

**自定义色板**：属性与注入点必须写在同一个元素上——`--blue` 的别名在定义处就求值完了，在祖先上改注入变量穿不进去（实测）。

```html
<section data-accent="custom" style="--pg-accent:#ff6600;--pg-accent-hover:#e65c00">
```

**不随主色变化**：`--lime`（正常状态）、`--red`（警示）、`--cat-*`（分类色）语义独立，跟随主色会让状态含义被主色污染。

**明暗与密度的限制**：`data-theme` 与 `data-density` 绑在 `:root` 上，只支持全局切换，局部嵌套不生效；主色与字号用不绑 root 的选择器，支持任意子树。

## 外观设置的接入

上游的 `AppearanceDialog`（主题 + 密度）与 `appearance.ts` 都是逐字节冻结文件，不能扩展。主色、字号与面板正文做在三个新文件里：

| 文件 | 职责 |
| --- | --- |
| `src/composables/appearance-ext.ts` | 管理 `accent` 与 `fontScale`，写根元素属性，持久化到 `scaffold.appearance.ext` |
| `src/components/workspace/AppearanceSettings.vue` | 外观设置的**正文**：主题 / 主色 / 字号 / 密度四区合一。不带动弹窗外壳，可直接嵌进业务自己的设置页 |
| `src/components/layout/AppearanceDialog.vue` | 上游冻结文件，仅通过登记缝隙挂载上面这个正文（见下） |

**为什么正文要独立成组件**：上游把「主题」「密度」两个 `Segmented` 直接写死在对话框里，文件逐字节冻结、内部无法扩展。而把主色与字号另做成一个独立弹窗，用户会在「外观设置」里找不到字号——所以正文整块交给本地组件，对话框只负责外壳。挂载方式是在 `AppearanceDialog.vue` 追加两行（`import` 与 `<AppearanceSettings />`），已登记在 `../scripts/fidelity_upstream.py` 的 `SANCTIONED_SEAMS`；原有的 `.pref-list` 由 `overrides.css` 的 `.modal-body:has(> .apx) > .pref-list { display: none }` 隐藏，`:has()` 把范围锁死在真正挂了新正文的那个弹窗上。

**尾部按钮不重做**：对话框的「完成」按钮与标题都在冻结层，保持上游形态。要合并成一个品牌化的弹窗，得等上游升级或多开缝隙做深度侵入，不建议。

**顶部栏入口按钮**：上游用的是 stroke-only 的 `contrast` 字形（空心圆加竖线），17px 下读不出「深浅对比」，也没有控件边界。它在冻结的 `Topbar.vue` 里，图标名不可改，因此在覆盖层用掩码补画「半实心对比圆」并套上与搜索框同款的胶囊材质。上游 `<svg>` 保留在 DOM 中、只把描边设为透明——直接 `display: none` 会让它变成零尺寸图标，而「零尺寸图标」是 `check_demo_health.py` 的一条判据。

**为什么不并进上游模块**：`appearance.ts` 用整对象回写 `scaffold.appearance`，把新字段塞进同一个键，任何一次主题或密度切换都会把它们冲掉。所以扩展维度独立成键。

**首屏防闪烁**：`index.html` 的内联脚本要同步写入 `data-accent` 与 `data-font-scale`。这三行已登记在 `../scripts/fidelity_upstream.py` 的 `SANCTIONED_SEAMS`，校验时剥离后仍要求与上游逐字节相等。新增维度若要再进首屏，必须按同样方式登记，不能直接改该文件。

**使用方接入**：在入口模块 `import '@/composables/appearance-ext'` 即可让属性生效。需要完整面板就渲染 `AppearanceSettings`，自己套一个 `Modal` 即可——它只出正文，不假设外层是哪个弹窗。业务方若只想局部覆盖，把 `data-accent` / `data-font-scale` 打在任意容器上，只影响该子树。

## 字色用途与对比度基线

`--ink` / `--ink-muted` / `--ink-soft` / `--ink-faint` 四档不是同一灰度的四个深浅，而是按用途分工——其中只有前三档承载文本：

| 令牌 | 用途 | 承载文本 | 对比度基线 |
| --- | --- | --- | --- |
| `--ink` | 正文、标题 | 是 | 4.5:1 |
| `--ink-muted` | 次级正文 | 是 | 4.5:1 |
| `--ink-soft` | 标签、元信息小字、占位符、图表轴标签 | 是 | 4.5:1 |
| `--ink-faint` | 停用态、装饰图形（分隔点、排序箭头、删除线） | 否 | 3:1 |

`--ink-faint` **不得承载 12px 级小字**。它在画布底上只到非文本档，用作正文会出现「字在但读不出来」。浅色四档已于 2026-10-31 整改到 AA（`--ink-soft` 4.55 / `--ink-faint` 3.14 / `--leaf-text` 4.71 / `--red-text` 4.86，取三个内容底的最差值），同时把承载文本的 `.faint`（35 处调用）与 `instruments.css` 里 10–11px 的图表轴标签、元信息迁到 `--ink-soft`；装饰性使用（标签圆点、排序箭头、省略号、关闭图标）继续走 `--ink-faint`。四种语义色同样按文本标准要求：`--blue`（主操作）、`--leaf-text`（正常状态）、`--red-text`（警示）。

深色主题复用同一套语义、色值各自调整，不拿浅色值直接反色；深色下不存在纯白内容面，因此它的比对底只有 `--canvas` 与 `--surface-solid`。

判定由 `../scripts/check_contrast.py` 执行：解析两层样式的生效值（`overrides.css` 覆盖 `tokens.css`），把每个字色令牌铺到白 / `--canvas` / `--surface-solid` 三个内容面取最差值。调整字色必须让该守卫转 `CONTRAST: PASS`，不接受口头说明；`--selftest` 提供「注入低对比必报错、提亮后必放行」两条阳性对照。

## 示例卡展示规格

示例卡按组件品类分四档，规格表在 `src/views/gallery/demo-specs.ts`，按**子分组**定义而非组件名，新增组件归进已有子分组即自动继承。

| 档位 | 网格占用 | 用在 |
| --- | --- | --- |
| 行内件 `inline` | 2 / 6 列（每行 3 张） | 按钮、标签、头像、开关、读数、刻度尺 |
| 面板件 `panel` | 3 / 6 列（每行 2 张） | 表格、列表、树、看板、表单、坐标图、刻度环 |
| 舞台件 `stage` | 6 / 6 列（整行） | 热力矩阵、泳道、关系图、列表页、矩阵、阶梯、外壳 |
| 弹层件 `overlay` | 2 / 6 列（每行 3 张） | 模态、抽屉、气泡、通知、命令面板 |

网格以 6 列为基准是为了让三档都能整除、每行不留空位；3 列基准下面板件跨 2 列会剩 1 列空位，每行只能放一张。弹层件的卡片另把内容区留白收紧到接住按钮柔影（14/16/22），否则六张卡里各只有一个按钮会白占两屏。

调宽度而不是调高度：表格被裁是缺横向空间，加高只会把空白放大。

### 示例内容本身也要成材

示例卡是组件库的脸面，**不是调试沙盘**。示例里塞的占位块必须和库内元素用同一套视觉语言：有圆角、有描边、有材质，字号走 `--fs-*` 令牌。

反例（`demo-slots.ts` 里曾真实存在，用户一眼指出「和我们的风格不一致」）：

```ts
// ❌ 只刷一层背景色，没有圆角、没有描边、没有材质 —— 看着像调试残留
h('div', { style: 'padding:8px;background:var(--blue-soft)' }, '半宽列')

// ✅ 用库内槽材质 + 圆角 + 字号令牌
h('div', { class: 'm-groove',
  style: 'padding:10px 12px;border-radius:var(--r-sm);font-size:var(--fs-sm);color:var(--ink-muted);text-align:center' }, '半宽列')
```

`DEMO_STYLE` 守卫（`scripts/check_demo_style.py`）会拦住这类写法：示例层内联 style 里出现 `background` 却没有 `border-radius` / `border` / 材质类，一律判失败。

边界：只管示例层。组件自身样式走另一套守卫（材质、投影、对比度），不在这里重复判定；示例图片里的 SVG 色值和取色器的色值属于**内容**，不算违规。

## 约束（还原度守卫）

- `src/` 下**所有上游文件必须与上游基线逐字节一致**，禁止手改——视觉与行为还原度靠字节级一致保证。上游冻结面包含七层样式（`src/styles/*.css`）与 `src/main.ts`，因此新增组件**不能**改样式层或入口文件。
- 外壳级绘制缺陷（不属于新增组件）走两条受控通道：修样式只写新增文件 `src/styles/overrides.css`（本地覆盖层，不改冻结 CSS 一个字节）；若必须让它在入口生效，把引入行登记进 `../scripts/fidelity_upstream.py` 的 `SANCTIONED_SEAMS`，`verify_fidelity.py` 会剥离这些声明行后要求逐字节相等，并在通过时打印 `SEAM:` 行说明。未登记的入口改动一律判 `FIDELITY: FAIL`。
- 需要 hack 时只改 `mock/`、`src/views/gallery/`、配置层（vite.config.ts 等）或以新增文件扩展；`workspace/` 与 `extend/` 是本仓库新增的本地扩展目录，可自由演进。
- `extend/` 内组件的样式一律写在组件自身的 `<style scoped>` 里，且只允许引用 `src/styles/tokens.css` 里的 CSS 变量令牌（禁止硬编码色值）；材质复用全局 `.m-*` 类，动效复用 `src/composables/motion.ts` 的 `overlayEnter/overlayLeave/settlePop` 等入口。这是在不触碰冻结样式层的前提下保持视觉一致的做法。
- 每次改动后运行（脚本在 skill 根目录的 `scripts/`，不是本目录）：
  - `python ../scripts/verify_fidelity.py`（联网权威）或 `--offline` → `FIDELITY: PASS`
  - `python ../scripts/check_contrast.py` → `CONTRAST: PASS`（字色令牌铺到白 / 画布 / 阅读面三个内容面取最差值的 WCAG 对比度：正文 4.5:1、非文本档 3:1；`--selftest` 跑「注入低对比必报错、提亮必放行」两条阳性对照。只判定令牌层，不判定页面里是否用对了令牌）
  - `python ../scripts/build_accent_palette.py --check` → `ACCENT_PALETTES: PASS`（主色色板派生块同步校验：从 `../references/accent-palettes.json` 的种子色派生 12 令牌 × 5 套 × 2 主题，种子色不达标时按 HSL 明度自动修正；`--report` 打印每套的实测对比度。加色板只改 JSON 后重跑，禁止手改块内内容）
  - `python ../scripts/verify_fidelity_selftest.py` → `GUARD_SELFTEST: PASS`
  - `python ../scripts/test_component_inventory.py` → `INVENTORY: PASS`
  - `python ../scripts/check_component_contracts.py` → `CONTRACTS: PASS`（死契约守卫：声明了却从未使用的 props / emits 即 FAIL。计数前遮蔽类型字面量与 `withDefaults` 默认值对象，否则只在默认值里回过一次名的 prop 会被算成已使用。`--selftest` 断言三类必报、正常组件零误报）
  - `python ../scripts/check_a11y_wiring.py` → `A11Y_WIRING: PASS`（接线守卫：派发了未声明的事件、绑了 `@click` 却没有 role/tabindex 的元素即 FAIL。豁免面集中在 `exempt_reason()` 一处，与「交互无障碍」节逐条对应。`--selftest` 断言七类豁免零上抛、两类缺口各报 1 项）
  - `python ../scripts/check_arco_parity.py` → `PARITY: PASS`（缺口 0）
  - `node ../scripts/build_component_catalog.mjs --check` → `CATALOG: PASS`
  - `node ../scripts/check_shadow_clipping.mjs` → `SHADOW_CLIP: PASS`（校验外壳、示例卡、登录画布三处容器的四向留白都覆盖其内柔影的四向延展；留白被清零时阳性对照必须转 FAIL，防止「边角阴影块」被 `overflow: clip` 切成方形暗块回归）
  - `python ../scripts/check_corner_occlusion.py` → `CORNER_OCCLUSION: PASS`（需先启动本地开发服务。逐页扫描全部菜单页，比对圆角父级与贴角子元素的圆角：粗描边父级的内弧被直角子元素盖住、或细描边/无描边父级的方角子元素外露，都判 FAIL；父级自身 `overflow: hidden/clip` 时子元素被裁到圆角内，不判。内置两条阳性对照：去掉 `.rail` 内弧圆角必须报 `border-occluded`，注入「20px 圆角父级 + 直角子元素」必须报 `corner-mismatch`）
  - `python ../scripts/check_help_tip_interaction.py` → `HELP_TIP: PASS`（需先启动本地开发服务。实测 `HelpTip` 的悬停浮出、指针移出收起、键盘聚焦、Esc 收起与 `aria-describedby` 清除、焦点保持（悬停后聚焦再移开指针，说明必须仍在）、视口夹取、长文 260px 上限；沿 `offsetParent` 祖先链检查浮层没有被滚动容器裁切）
  - `python ../scripts/check_content_padding.py` → `CONTENT_PADDING: PASS`（需先启动本地开发服务。逐页扫描全部示例页，候选容器 = 四边有可见边框、带非透明背景，或本身是 `button` / `menuitem` 等交互控件；用 Range 取文本字形与容器边框内沿比对，**左右任一方向 < 4px 即判 FAIL**。无可见边界的纯文字按钮与布局 div、圆形容器（头像）、自身可滚动的容器按语义豁免。路由从分类真相源派生、不手写清单。判据必须配阳性对照：移除 `MenuNode.vue` 的 `padding-right` 后应精确报出 1 处 `x-menu-item > .x-menu-label` 贴边）
  - `python ../scripts/check_demo_visibility.py` → `DEMO_VISIBILITY: PASS`（需先启动本地开发服务。逐页扫描全部示例页，三条判据：空白卡、出卡、塌缩（宽高都 < 4px，1px 竖线豁免）。定位包装层不参与判定。内置阳性对照与示例卡数量下限、空页检测三项自证。判据必须配阳性对照：把 `BackTop.vue` 的 `docked` 强制为 `false` 后应精确报出 4 处 `BackTop ... all-outside | BUTTON.x-backtop`）
  - `python ../scripts/check_demo_guides.py` → `DEMO_GUIDES: PASS`（需先启动本地开发服务。逐页扫描全部示例页，四条判据：每张卡头有 `.x-help` 图标、提示含「组件说明 + 本格示例」两段、非基础示例不退回默认形态、同组件不同变体提示不重复。说明数据源 `src/data/component-guides.ts`，本格差异由 `views/gallery/demo-guides.ts` 按该格 props 推导。判据必须配阳性对照：差异推导恒返回默认文案必须报「非基础示例却写默认形态」，移除 `<HelpTip>` 必须报「缺少提示图标」）
  - `python ../scripts/build_font_overrides.py --check` → `FONT_OVERRIDES: PASS`（字号标度派生块同步校验：从冻结的 `src/styles/*.css` 自动提取 10–15px 的 `font-size` 规则，按相邻 0.5px 合并成 5 档令牌——`caption` 12 / `sm` 13 / `body` 14 / `lg` 15 / `title` 16——生成 `overrides.css` 的受管块；16px 以上不纳入。媒体查询块整体排除，一旦块内出现标度范围内字号脚本直接报错，不静默漏掉。上游升级或改动脚本后未重跑生成，`--check` 会报失配。该块由 `BEGIN/END GENERATED` 包裹，禁止手改）
  - `python ../scripts/check_demo_health.py` → `DEMO_HEALTH: PASS`（需先启动本地开发服务。逐页扫描全部示例页，九条判据：渲染异常、框架告警（控制台 error 与 `[Vue warn]`/`Invalid prop`）、坏文本（`NaN`/`undefined`/`Invalid Date`/`[object Object]`）、坏图、零尺寸图标、交互元素缺可访问名、文字裁切无省略号、页面横向溢出、低对比文字（对比度 < 1.5，浅色与暗色两个主题都要扫）。视觉隐藏元素豁免裁切判定；半透明与禁用态元素豁免对比度判定；文字与不透明底之间有渐变或图片背景时不判对比度。控制台豁免面集中在 `KNOWN_CONSOLE_ALLOW` 一处，每条写明根因与解除条件。`--selftest` 跑阳性对照：注入一张放齐七类违例的坏卡与两条坏控制台消息，逐条断言判据会报，并回显注入前后卡数证明扫描根覆盖。按 diamond 拆成 `demo_health_env.py`（路由派生与页内量测脚本）、`demo_health_judges.py`（豁免面与控制台判据）、`demo_health_selftest.py`（阳性对照）、`check_demo_health.py`（入口与全量流程）四个同级文件）
  - `node ../scripts/build_demo_events.mjs --check` → `DEMO_EVENTS: PASS`（事件表派生同步校验：从各组件 `defineEmits` 派生「组件 → 声明事件名」写入 `src/views/gallery/demo-events.generated.ts`，示例层据此把每个声明事件都接上一次可见反馈。组件改了 `emits` 未重跑生成即报 FAIL；生成物禁止手改）
  - `python ../scripts/check_demo_event_wiring.py` → `EVENT_WIRING: PASS`（需先启动本地开发服务。逐页扫描全部示例页，沿 `__vueParentComponent` 读卡内同名组件实例 vnode 上真实绑定的 `on*`，与派生事件表对账：声明了却没接处理器即判缺口（这类格子按钮点了没反馈，看着像坏控件）。事件名按 Vue 的 camelize 归一（`row-click` → `onRowClick`），否则带横线事件全量误报。`update:*` 由样本状态写回负责不计入；逐帧/逐秒/指针移动类事件走集中豁免面，豁免条目必须在事件表里真实存在。`--selftest` 跑六条阳性对照：未接必报、接上必不报、带横线不误报、`update:*` 不计入、多事件只报漏项、豁免面无失效条目。按 diamond 拆成 `demo_event_wiring_probe.py`（页内量测脚本、豁免面与缺口判定）与 `check_demo_event_wiring.py`（路由派生与全量流程）两个同级文件）
- 上游升级：重新冻结新 commit → `python ../scripts/verify_fidelity.py --write-baseline` 刷新 `../references/component-library-baseline.json`，并同步本文档与 `SKILL.md` 顶部的 commit 号。

## 组件库侧栏（画廊导航折叠）

上游 `layout/Sidebar.vue` 把分类标题渲染成**不可点的静态标签**，100+ 子项全部平铺——分类多了以后，标题看着像分隔线而不是可操作项。改造受两条约束：`Sidebar.vue` 逐字节冻结；分类数据来自服务端 `navGroups`（不能只改数据层）。

做法是「缝隙 + 本地接管」：

1. `Sidebar.vue` 只追加两行缝隙（已登记 `SANCTIONED_SEAMS`）：`import GalleryNav` 与 `<GalleryNav />`。
2. `src/views/gallery/GalleryNav.vue` 渲染可折叠分组，**只在 `/gallery` 且不在 `.g-cell` 内**接管。
3. 上游的平铺分组与它的滑动块由 `overrides.css` 的 `.rail-nav:has(.gn) > .nav-group` 隐藏。

四个容易踩的点：

- **必须在 `.g-cell` 内不渲染**。示例页的 `AppShell` 样本挂的是同一个冻结侧栏，会连带挂上本组件；不管的话演示卡里会多出一整套导航，卡内 4 个嵌套外壳一次制造 816 条 `zeroIcon` 判据（真侧栏收起后是 0 条）。
- **`.nav-thumb` 在 `.gn-list` 里要 `left/right` 归零**。上游那 12px 是相对 `.rail-nav` 内边距算的，`.gn-list` 已经在同样的内边距里，再套一次就双重内缩——实测项目 207px、玻璃块只有 183px，盖不住整行。
- **分类头用 `--ink-soft` 不用 `--ink-faint`**。后者是「元信息」档、3.1:1，达不到正文 AA；分类头是可点文字，13 个分组一屏里最需要读清的就是它。计数同样守 12px 下限，不靠压小 + 降透明度做层级。
- **折叠用 `grid-template-rows: 0fr ↔ 1fr`**，比 `max-height` 可靠（不用猜高度）；同时给收起态加 `inert`，否则 Tab 会走进被裁掉的子项里。

交互规则：默认只展开当前路由所在的分类（全展开等于回到平铺长列表）；用户点过之后按他的选择持久化到 `scaffold.galleryNav.open`；路由变化时自动把目标分类展开；**收起的分组若含当前页，标题与计数转主色**，避免用户以为导航丢了。

## 动效（能量语态与确认落定）

动效唯一入口是 `src/composables/motion.ts`，**不要在组件里新起一套曲线或时长**。全库把默认 `ease` 收敛到这套曲线的分批计划见 `../references/motion-upgrade-plan.md`（现状 225/236 段仍是默认 `ease`）。

### 五种能量语态

每条动效都要能说出属于哪一种，说不出的是装饰，不做。

| 语态 | 含义 | 曲线 | 用途 |
|---|---|---|---|
| 蓄 Charge | 输入 | `EASE.glide` / `DUR.hoverIn` | 悬停、聚焦 |
| 放 Discharge | 开始工作 | `EASE.swap` / `DUR.press` | 按压、提交、收拢 |
| 导 Conduct | 进行中 | spinner、进度 | 加载中（**不要**用落定冒充） |
| 结 Crystallize | 交付落定 | `EASE.reveal` + `EASE.settle` | 成功确认、结果出现 |
| 停摆 Halt | 停止恢复 | `EASE.exit` / `DUR.pageOut` | 失败、取消、收起 |

### CSS 侧：动效校准层

`overrides.css` 的「动效校准层」把 CSS 侧拉回同一套语言。审计数据：全库 236 段 `transition` 里 **180 段用浏览器默认 `ease`**（含未声明缓动），56 段用了 `--ease-premium`。默认 `ease` 起步钝、收尾也钝，没有能量语态——这正是「登录那个确认动画比别处高级」的根因：不是形变更花哨，而是它拿到了真曲线。

令牌与 `EASE` 一一对应，改一边必须同步另一边（`cubic-bezier` 为 GSAP 曲线的标准近似）：

| CSS 令牌 | 值 | 对应 GSAP |
|---|---|---|
| `--ease-reveal` | `cubic-bezier(.16, 1, .3, 1)` | `expo.out` |
| `--ease-glide` | `cubic-bezier(.22, 1, .36, 1)` | `power4.out` |
| `--ease-exit` | `cubic-bezier(.55, .085, .68, .53)` | `power2.in` |
| `--ease-swap` | `cubic-bezier(.455, .03, .515, .955)` | `power2.inOut` |
| `--ease-settle` | `cubic-bezier(.34, 1.56, .64, 1)` | `back.out(1.6)` |

时长同理：`--dur-hover` .18s / `--dur-swap` .22s / `--dur-reveal` .32s / `--dur-exit` .16s。**退场永远快于入场**，关闭动画拖在手上比不做动画还难受。

**分派规则：属性优先、选择器兜底。** 同一个 `.card:hover`，只改阴影是「着色」（`reveal`），改 `transform` 是「位移」（`glide`）；属性判不出语义时才看选择器（含 `is-active` / `thumb` / `open` → `swap`）。退场选择器（`leave` / `exit` / `close` / `collapse`）优先级最高，且时长按 0.8 折算。

落地方式分两层，**都不改冻结样式一个字节**：

| 层 | 范围 | 做法 |
|---|---|---|
| 可写层 | `components/extend`、`components/workspace` | 直接改 scoped 样式里的缓动实参 |
| 冻结层 | `src/styles/*.css` | `build_motion_overrides.py` 机械派生覆盖块（同特异度 + 本文件最后加载） |

```bash
python -X utf8 -B ../scripts/build_motion_overrides.py           # 重新派生
python -X utf8 -B ../scripts/build_motion_overrides.py --check   # MOTION_OVERRIDES: PASS
python -X utf8 -B ../scripts/check_motion_language.py            # MOTION_LANGUAGE: PASS
```

生成器只动缓动，不动属性与时长；`linear`、自定义 `bezier`、`--ease-*` 一律原样保留；`prefers-reduced-motion` 整块排除；`@media` 内的规则原样复刻包裹。**目录里新增 `.css` 却没登记进 `SOURCE_FILES` 会直接 FAIL**——漏一个文件就是静默少一整层。

### 补建过渡（原本没有动效的地方）

「重定时」和「补建」是两件事，别混：

- **重定时**：元素已经有 `transition`，只是缓动是默认 `ease` → 换曲线。53 条规则覆盖 96 段。
- **补建**：元素的状态确实在变（`:hover` / `.is-*` 声明了可视属性），但从来没有 `transition` → 瞬间闪变。这类**不能靠重定时解决**，必须新增声明。

现状：154 个组件里 **106 个的 scoped 样式一条 `transition` 都没有**。收紧判据（只认真正交互态）后全量审计剩 **34 个基选择器**在硬跳，已补 **26 处**（含 2 处图形类）。

```bash
python -X utf8 -B ../scripts/build_motion_overrides.py --audit   # 列出所有硬跳的基选择器
```

**图形类单独走 `EXTRA_RULES`，不要混进 `CURATED_BASES`。** 原因：它们的基选择器带变体类（`.rg-node.is-item` / `.mx-row.is-hover`），按选择器匹配会漏，而且每个变体都要单列一条；直接按「元素 + 属性」写死一条规则，覆盖面反而更稳。目前只做了两个：`.rg-node .rg-body`（节点悬停描边与投影）、`.mx-row .mx-label`（矩阵行悬停底色）。

图形类要避开两类：

- **靠渐变驱动的不能补**。`.bar-col` 悬停改的是 `background: linear-gradient(…)`，`background-color` 过渡不了，补了也是硬跳。
- **变体类不是状态**。`.heat-cell.is-risky`、`.org-node.is-root` 这类挂载即确定，补过渡只会在首屏闪一下。

**判据必须区分「交互态」和「变体」**。`.is-on` / `.is-active` / `.is-selected` / `.is-open` 是状态，会随交互切换，该有过渡；`.is-info` / `.is-success` / `.is-bordered` / `.is-sm` / `.is-disabled` 是**变体**，挂载时就确定，给它们加过渡只会在首屏闪一下，是伪需求。第一版判据用 `\.is-[a-z]` 一把抓，把变体全算成硬跳，数字虚高一倍多（97 → 55）。

**自动识别只回答「谁在硬跳」，回答不了「该不该动」**，所以生成走「自动审计 + 人工确认名单」：只有 `CURATED_BASES` 里的选择器才会落盘，属性仍由脚本从状态规则里机械读取。

四条必须守住的约束：

1. **非法选择器绝不能落盘**。自动派生的基选择器可能留下 `:has()` / `:not()` 空参或括号不配平；这种规则一进样式表，浏览器会从它开始丢弃后续规则，整段覆盖直接失效。生成器有 `selector_is_valid()` 兜底。
2. **别给已经有过渡的元素补 shorthand**。`.btn-primary:not(:disabled)` 这类元素同时带着 `.btn`，`.btn` 已有过渡；再补一条 `transition` 会整条重置，把原来的 color/border/shadow 一起丢掉。这类必须跳过。
3. **逗号分组的选择器要拆开**。`.checkbox.is-on .checkbox-box, .checkbox.is-partial .checkbox-box { background: … }` 整串拿去匹配基选择器对不上，属性会被静默漏掉——这正是「复选框只补到 `border-color`、补不到 `background-color`」的原因。`split_selectors()` 负责拆。
4. **曲线只看属性，不看选择器名**。基选择器里可能带 `.is-sortable` 这类**能力标记**（可排序 ≠ 状态在切换），按 `is-` 判「交接」会误用对称曲线。

属性分派：位移类（`transform` / `translate` / `rotate` / `scale`）走 `--ease-swap`（对称）+ `--dur-swap`；纯着色走 `--ease-reveal` + `--dur-hover`。位移若用 expo 会冲得太猛，滑块观感会变「弹」。

**看曲线用 `../references/motion-compare.html`**（可直接双击打开）。左右两栏组件、颜色、时长完全相同，只有缓动不同；「定格 25%」会把两条过渡同时暂停在四分之一处——同一点上旧 `ease` 只走到约 41%，新语态已到约 83%，这是差距最大的位置。小尺寸下颜色差看不出来，所以页里用同参数驱动的进度条把曲线形状放大呈现。

keyframes 的缓动只有 4 段需要人工判语义（2 个入场 → `reveal`、2 个呼吸循环 → `swap`），其余 7 段是 spinner 与倒计时进度，**必须保持 `linear`**。新增动画若带默认 `ease`，`MOTION_LANGUAGE` 会拦下。

### 形变（Morph）：形状在变，而不只是变色

**先分清两件事，混淆过一次，代价很大**：

| | 缓动 | 形变 |
|---|---|---|
| 变的是什么 | 同一个形状的**颜色 / 位置** | 形状**本身** |
| 载体 | `transition-timing-function` | 宽高、圆角、`scale`、`translate`、`stroke-dashoffset` |
| 观感 | 变顺了，但不注意看不出来 | 一眼看到「它变形了」 |
| 本库现状 | 已统一到五条语态曲线 | **只有 6 处**，且各写各的 |

登录那颗按钮之所以好看，是形变不是缓动：**宽条收拢成圆 → 圆环一笔描出 → 对勾再描一笔 → 回弹落定**。只改缓动永远做不出这个。

**形变有两个硬门槛，先验证再动手**：

1. **元素必须在两个状态下都存在于 DOM**。复选框的勾是 `<Icon v-if="modelValue">`，未选中时 SVG 根本不在，没有「从无到有」的起点，只能凭空出现——描线做不了。要做得先让图标常驻、用 `stroke-dashoffset` 控制显隐，这需要改 DOM。
2. **几何属性必须真的在变**。如果一个状态只改颜色，形变无从谈起，那属于缓动范畴。

**哪些组件有资格**（全库扫描结果）：状态规则里出现 `width` / `height` / `border-radius` / `transform` / `translate` / `rotate` 的只有 **19 条规则**，集中在 Card、Carousel 圆点、Collapse 箭头、MenuNode 箭头、Rate 星标、Steps、Anchor、Tree 箭头、开关滑块、组织节点、矩阵勾选、色板、关系图节点等。其余组件的状态切换只是换色，**想给它们加形变等于重新设计状态表达，不是补过渡**。

全量形变方案见 `../references/morph-upgrade-plan.md`：定义了四类形变语式（收拢 / 描线 / 落定 / 展开）、三步适配判定、四个批次与逐组件设计。42 个候选组件**全部落在可写层**，真正的障碍不是冻结面，而是 26 个组件用 `<Icon v-if>` 让描线没有起点。

**已落地的形变**：

| 组件 | 形变 | 实现 |
|---|---|---|
| `Progress`（line + 100% + success） | 条收拢成圆 → 描环 → 画勾 → 回弹 | 复用 `playCrystallize`，见下 |
| `ConfirmButton` | 同上三拍 | `playCrystallize` |
| `Radio` | 外环按压 `1→0.89→1` + 圆点 `0→0.86→1.09→1` | `morph.ts` 的 `morphSelect` |
| `Rate` | 被点的星 `1→0.86→1` 按压落定 | `morph.ts` 的 `pressSettle` |
| `CollapseItem` | 内容高度 0fr ↔ 1fr | `grid-template-rows` |
| `Switch` | 轨道填充 0%→100% + 滑块位移 | `@property --fill` + `translate` |
| `Tabs` / 侧栏导航 | 滑动块同时改 `x` 与 `width` | `slideThumb` |
| `Checkbox` | 勾选落定回弹 | `settlePop`（挂在常驻包裹 span 上，所以有效） |
| `Steps` | 完成步骤的勾一笔描出，数字同步淡出 | 常驻 SVG + `stroke-dashoffset` 过渡（纯 CSS） |
| `InputTag` | 删除标签时宽度收拢到 0 | `morph.ts` 的 `collapseOut` |
| `Tree` | 子行逐条落下 | `nth-child` 错位 26ms |
| `MenuNode` | 子菜单高度 `0 ↔ auto`，展开收起都有过程 | `Transition` + GSAP 钩子，见下 |

**`MenuNode` 的展开必须是双向的。** 早先做的是「子项逐条落下」——展开有动效、收起仍旧 `v-if` 瞬删，一半有一半没有，用户直接反馈「太僵硬，一点动画效果都没有」。改成 `<Transition :css="false">` 包住 `<ul v-if="subOpen">`，`@enter` 走 `height: 0 → auto`（0.24s `--ease-swap`）、`@leave` 走 `height → 0`（0.18s `--ease-exit`），两端一致。`.x-menu-sub` 需要 `overflow: hidden` 才能裁切。

两个实现坑：
- **`onEnter` / `onLeave` 在 `MenuNode` 里已被悬停逻辑占用**（`@pointerenter` / `@pointerleave`）。Transition 钩子必须换名（现用 `onSubEnter` / `onSubLeave`），否则 TypeScript 报 `Duplicate function implementation`——这是 TS 帮忙挡下的一次覆盖事故。
- 箭头绑 `subOpen` 而不是 `expanded`：浮层态下可见性由 `hovered` 驱动，绑 `expanded` 会让箭头在浮层里永远不转。

### 浮层（弹出子层级）的入场形态

`overlayEnter(el, done, kind)` 第三个参数是**入场形态**，不是组件类型。实测差别：

| 分支 | 入场 | 缩放幅度 | 观感 |
|---|---|---|---|
| `pop` | `y -6` + `scale .98` | **1.4%** | 只剩淡入，等同没有动画 |
| `modal` | 从锚点 `scale .86` 展开（键盘打开时 `y 14` 滑入） | **14%** | 明显的「长出来」 |
| `drawer` | 共享元素 ghost 从被点的行长成抽屉 | — | 最强，用于抽屉 |

**内容面板从锚点缩放展开**，通过 `morph.ts` 的语义包装调用：

```ts
import { overlayMenuEnter, overlayMenuLeave } from '@/composables/morph'
// <Transition :css="false" @enter="overlayMenuEnter" @leave="overlayMenuLeave">
```

**为什么是缩放而不是位移**（这里推翻过一次判断）：按 Material 规范，对话框用 `scale 0.86`、菜单用 fade + slide，我据此把下拉改成了位移——但用户实测反馈**缩放更「丝滑」**。原因是缩放有「从触发器长出来」的来源感，位移只是「滑进来」，缺来源。规范是通用参考，实际观感优先。

上游 `modal` 分支的缩放有三个缺陷，所以在 `morph.ts` 自己实现，逐项修掉：

| 缺陷 | 表现 | 修法 |
|---|---|---|
| **长尾** | `expo.out` 在 46ms 已到 0.944，之后 150ms 只再走 0.05，像「唰一下然后停着」 | 换 `glide`（`power4.out`），时长 380 → 280ms |
| **文字重栅格化** | 缩放期间文字发虚，落定才清晰 | 入场挂 `will-change: transform, opacity` 提升合成层，结束立即清理 |
| **原点不准** | 上游按面板几何算 `transformOrigin`，轴心可能落在中部，像「从肚子鼓起来」 | 固定为**顶边中心**（面板在视口上半则底边） |

实测：`0.914 → 0.955 → 0.98 → 0.992 → 1`，**209ms 到位**（原版 262ms 才到 0.995）。

注意这**不是掉帧**：实测 rAF 稳定 16.7ms、零超 20ms 帧。观感问题来自曲线与栅格化，不在主线程。

**分派规则（不是一刀切）**：入口按面板里**有没有可操作项**决定形态——命中 `button` / `[role="menuitem"]` / `[role="option"]` / `[role="treeitem"]` / `input` 等即走缩放入场，纯文字提示走上游 `pop` 分支。

用「可操作性」而不是宽度：下拉菜单可能只有 160px 宽、确认气泡反而更宽，按尺寸分会把两者判反。实测：

| 组件 | 形态 | 实测 |
|---|---|---|
| Dropdown / Cascader / DatePicker / Select / Popconfirm | 从锚点缩放，0.28s | scale `0.88 → 1`，209ms 落定 |
| Tooltip / HelpTip / BackTop | `pop` 轻量淡入 | 起始 scale 0.986 |

退场只淡出 0.14s、不做缩放——退出不该纠缠。

**全库 22 个浮层已全部接入统一入口**，没有裸 `overlayEnter(..., 'pop')` 调用；新增浮层只要写 `@enter="overlayMenuEnter"`，形态由判据自己决定。`OVERLAY_MOTION` 守卫会拦住绕过入口的写法。

**对比工具**：`../references/overlay-motion-compare.html`（A 原版缩放 / A+ 优化缩放 / B 位移对照，带真实 `backdrop-filter` 材质——普通背景看不出差别）。

**冻结面破例**：`Select`（`ui/`）、`HoverCard`（`ui/`）、`Modal`（`ui/`）、`Topbar`（`layout/`）、`CommandPalette`（`layout/`）改不了 Transition，已登记进 `fidelity_upstream.py` 的 `LOCAL_MANAGED`，校验时显示 `OVERRIDE: ... (local-managed, declared)`。

**代价必须知道**：这五个文件从此**不再与上游比对**，上游若修 bug 或改交互，本地收不到漂移告警。非必须不要再往 `LOCAL_MANAGED` 加 `src` 文件。

### 弹窗 / 遮罩：同一套参数，换轴心

`overlayDialogEnter` / `overlayDialogLeave` 与菜单共用参数规格（`280ms`、`power4.out`、入场期 `will-change`），**只把轴心从顶边换到中心**——弹窗从自身中心升起，菜单从触发器那一侧生长。

| 类型 | 处理 | 理由 |
|---|---|---|
| `Modal` / `CommandPalette` | 遮罩淡入 0.2s + 面板（`.modal` / `.cmd-panel`）`scale 0.92 → 1` | 有内层面板，缩放作用在面板上，遮罩不跟着动 |
| `Image` / `ImagePreview` / `ImagePreviewGroup` | **只淡入，不缩放** | 图片的 `zoom` / `pan` 是用户交互状态、写在自己的 inline transform 上，GSAP 直接动 `transform` 会把它覆盖掉 |
| `Drawer` | 保持上游 `'drawer'` 分支 | 共享元素 ghost（从被点的行长成抽屉），是它专属的形变 |

`OVERLAY_MOTION` 守卫的豁免清单现在只剩 `morph.ts`（分派实现自身）与 `Drawer.vue`——弹窗和图片预览不需要豁免，它们各自有专用入口。

`src/composables/morph.ts` 是形变语式的落点（与 `motion.ts` 分工：那边管曲线，这边管几何动作），现有三个原语 `growIn` / `pressSettle` / `morphSelect`。它会在动效期间**临时关掉元素自身的 `transition: transform`**——GSAP 每帧写的 inline 值会被 CSS 再插值一次，不关的话动作会变软变慢（`Rate` 星标就有 `transition: transform`）。

**踩过的坑**：`Radio` 原来写 `watch(checked, () => settlePop(dot.value))`，但 `dot` 是 `v-if`，`watch` 默认在渲染前触发，那一刻拿到的还是 `null`，`settlePop` 静默返回——**圆点 scale 恒为 1，注释里的「落定弹入」从未生效**。凡是对 `v-if` 元素做进场动效，必须 `await nextTick()` 再取元素。

`Progress` 的触发条件刻意收紧成 **`percent >= 100` 且 `status === 'success'`**：单给 `status` 不给 `percent` 不变形——「62% 却打对勾」语义自相矛盾。示例里专门留了 `status=success`（62%）这一格做反例。

### 确认落定（Crystallize）

`src/composables/crystallize.ts` 的 `playCrystallize()` 把登录页那套三拍抽成可复用件：

1. **收拢**：容器宽度从实测值收到 `size`，0.42s + `EASE.swap`；
2. **描环**：`stroke-dashoffset` 126 → 0，0.5s + `EASE.reveal`，比第一拍**提前 0.08s** 交接，不等它完全停下；
3. **画勾**：再压 0.22s 起笔，0.32s + `EASE.settle`——笔顺感就靠这个错位，两笔同时起笔会读成一闪而过；
4. **回弹**：`scale` 1 → 1.06 → 1，确认感来自这一下，不是靠放大停留。

尺寸约束：环与勾的 SVG 取圆的 **88%**。按登录页那颗 46px 圆的 0.87 比例换算到 36px 按钮高度，环会贴住蓝底边只剩 1.3px；88% 能留出约 2.4px 呼吸，且比例不随尺寸漂移。

降级：`motionSkipped()`（reduced-motion 或页面在后台）时**直接给终态**，绝不停在半收拢的中间态。

### ConfirmButton

`src/components/extend/ConfirmButton.vue` 是这套动效的落地件，`variant` / `size` 与 `Button` 同名同值，换用时只改标签名。

- **受控**：传 `status`，`idle / pending / success / error` 由调用方掌握；`status` 变成 `success` 的那一拍播落定。
- **自驱**：不传 `status`，点一下自己走完 `pending`（620ms）→ 落定 → 复位。示例卡用它，点得动、可反复演示。
- `block` 默认 `true`：形变需要一个能收拢的宽度，窄按钮上看不出「收拢」。
- 三种语态不要混：加载用 spinner，成功用落定，失败用图标 + `--red-text`。把落定做成转圈，成功会看起来没结束。

改完跑 `python ../scripts/_verify_crystallize.py`（需先启动本地开发服务）：逐帧采集宽度、两笔 `stroke-dashoffset`、回弹缩放，断言「宽度是渐变不是跳变」「对勾晚于圆环起笔」「收拢后宽高比为 1」「动画结束必须描满」「自驱能复位」。

## 交互无障碍（键盘可达）

判定基线只有一句：**鼠标能完成的操作，键盘也要能完成；键盘用户必须能看见自己停在哪一格。**

按组件形态分三种接线方式，新增组件时对号入座，不要混用：

| 形态 | 代表组件 | 做法 |
|---|---|---|
| 下拉 / 级联 / 组合框 | `Cascader`、`Select`、`TreeSelect`、`AutoComplete` | 焦点始终留在触发器（`role="combobox"`），用 `aria-activedescendant` 指向当前项；**不给每个选项加 `tabindex`**，否则一列十几项会把 Tab 序列撑爆 |
| 选项卡 / 单选组 | `Tabs`、`AppearanceSettings` | roving tabindex：组内只有当前项 `tabindex="0"`，其余 `-1`，方向键移动并把焦点带过去 |
| 可点列表项 | `Steps` | 保留 `<ol>/<li>` 列表语义，只给可点项补 `tabindex` 与 Enter/Space，**不换成 `role="button"`**（换了就等于 `<ol>` 不再有列表项） |

键位约定：`ArrowDown/Up` 在当前列移动（跳过 `disabled`）、`ArrowRight` 进入下级、`ArrowLeft` 退回上级、`Home/End` 到首末项、`Enter/Space` 落定、`Esc` 收起并把焦点还给触发器。所有可聚焦项必须有 `:focus-visible` 焦点环，`Steps` 实测 `2px solid`。

明确豁免，不必当缺陷改：

- `.input-clear` 这类输入框内的清除伪按钮不占 Tab 位（与 Arco 一致）。键盘用户走「全选 + 删除」，为一个可选的清除动作在每张表单里多插一个 Tab 停靠点不划算。
- `role="option"` / `role="treeitem"` 的列表项不单独 `tabindex`，由上面的 combobox / tree 模式统一驱动。
- 遮罩类元素（`.rail-scrim`、图片预览遮罩）的点击关闭是鼠标便利，`Esc` 已覆盖同一操作。

`Trigger` 的 `disabled` 只负责「拦住开合」，不接管外观：被禁用时根元素带 `aria-disabled` 与 `data-disabled`，外观由调用方按 `[data-disabled]` 自行处理；运行中置为禁用会立即收起已打开的浮层。

改完跑 `python ../scripts/_verify_keyboard.py`（需先启动本地开发服务）：实测 `Steps` 可聚焦步骤数与 Enter 切换、`Cascader` 的开关 / 上下 / 进退 / 焦点归还，任一项不达标即 FAIL。

两个静态守卫（已转录进 `_sweep.sh`，改动组件后随手跑）：

- `python ../scripts/check_component_contracts.py` → `CONTRACTS: PASS`。死契约扫描：声明了却从未使用的 `props` / `emits`。计数前会把类型字面量与 `withDefaults` 默认值对象整块遮蔽——否则只在默认值里回过一次名的 prop 会被误判成「已使用」，这是这类扫描最主要的漏报源。`--selftest` 断言「死 prop / 只在默认值出现的 prop / 死 emit」三类必报、正常组件零误报。
- `python ../scripts/check_a11y_wiring.py` → `A11Y_WIRING: PASS`。接线扫描：未在 `defineEmits` 里声明就派发的事件、绑了 `@click` 却键盘到不了的元素。豁免口径写在同一文件的 `exempt_reason()` 里，与本节逐条对应，改豁免要两边一起改。`--selftest` 断言七类豁免零上抛。
- 新增或改动组件时的逐项清单见 `../references/component-checklist.md`（形态选型、契约、样式、示例、无障碍、收口命令）。
