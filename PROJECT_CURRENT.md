# 项目当前状态

## 2026-10-31 弹窗/遮罩也接入 A+ 参数（同日第二十九笔，未提交）

- 当前状态: 新增 `overlayDialogEnter` / `overlayDialogLeave`，与菜单**同一套参数规格、只换轴心**；`Modal` / `CommandPalette` / `Image` / `ImagePreview` / `ImagePreviewGroup` 五个组件接入。全守卫 PASS。
- 用户指令: 「把其他的组件也按照这个调整一下」。
- 关键设计（不是照搬菜单那套）:
  - 菜单从**触发器那一侧**生长（顶边轴心），弹窗从**自身中心**升起（中心轴心）。轴心不同，参数规格相同（280ms / `power4.out` / 入场期 `will-change`）。
  - **图片预览只淡入、不缩放**：图片的 `zoom` / `pan` 是用户交互状态，写在自己的 inline `transform` 上，GSAP 直接动 `transform` 会把它覆盖掉。这是读代码时发现的，不是猜的。
  - `Drawer` 保持上游 `'drawer'` 分支的共享元素 ghost——那是它专属形变，不能被通用弹窗形态替代。
- 实测: `Modal` 面板起始 `0.943` → 到位 `212ms`，遮罩 `opacity 1`。
- 守卫收敛: `OVERLAY_MOTION` 的豁免清单从 6 条收到 **2 条**（`morph.ts` 分派实现 + `Drawer.vue`），因为弹窗与图片预览现在各有专用入口，不再直写形态。
- 冻结面新增两处破例: `ui/Modal.vue`、`layout/CommandPalette.vue` 登记进 `LOCAL_MANAGED`。**现有 5 个 `src` 例外**（Select / HoverCard / Modal / Topbar / CommandPalette），代价在累积，已在 LOCAL-GUIDE 与代码注释里写明。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`（7 条 OVERRIDE 显式打印）；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`KEYBOARD_VERIFY: PASS`。
- 交接点: 无阻断。`Image` 族的预览需要 demo 侧开启属性才触发，本轮只做了静态检查与逻辑复核，**未做运行时逐帧实测**——下次动它时要补。

## 2026-10-31 A+ 全量生效：修掉一处漏改并收紧守卫（同日第二十八笔，未提交）

- 当前状态: `Dropdown` 补接统一入口，A+ 现在全库一致（`Select` / `Dropdown` / `Cascader` 实测 198–202ms 到位）。守卫升级为拦所有直写 kind。全守卫 PASS。
- 用户指令: 「先用 A+ 改一版我们看看效果」——A+ 在上一笔已落地，本笔是**复核时发现漏改**。
- 发现的漏改: `Dropdown` 起始仍是 `0.86`、到位 `327ms`，走的是旧 `modal` 分支。
  - 原因：第 23 笔我直接把 Dropdown 改成了 `'modal'`，而第 25 笔批量替换的锚点是 `'pop'` 版本，**正好跳过它**。
  - 教训：**批量替换必须按「直写任意 kind」匹配，不能只匹配一种**；改完要用运行时数据验收，不能只看"替换成功 N 个"。
- 守卫升级（`check_overlay_motion.py`）:
  - 判据从「只拦 `'pop'`」扩到「拦 `'pop'` / `'modal'` / `'drawer'` 任意直写」。
  - 豁免清单写明确理由：`Modal` / `CommandPalette`（居中弹窗）、`Image` / `ImagePreview` / `ImagePreviewGroup`（全屏遮罩）、`Drawer`（用 `'drawer'` 分支的共享元素 ghost，是它专属形变）。
  - 双向验证：当前 PASS；把 Modal 移出豁免后能精确报出 2 处。
- 实测一致性: Select `0.914 → 200ms`、Dropdown `0.914 → 202ms`、Cascader `0.912 → 198ms`。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。A+ 参数：`scale 0.88` / `280ms` / `power4.out` / 顶边轴心 / 入场期 `will-change`。

## 2026-10-31 浮层入场改为「优化版缩放」：用户实测推翻规范推断（同日第二十七笔，未提交）

- 当前状态: 内容面板入场回到**从锚点缩放**，并修掉上游 `modal` 分支的三个缺陷。全守卫 PASS。
- 用户反馈: 「A 缩放是最好的，丝滑，还可以更好吗？」——**推翻了上一笔的判断**。
- 判断反转（必须记住的教训）:
  - 上一笔我按 Material 规范（对话框 `scale 0.86` / 菜单 fade + slide）把下拉改成位移，理由是缩放会让文字重栅格化、背景模糊跟着缩放。
  - 但实测观感相反：**缩放有「从触发器长出来」的来源感，位移只是「滑进来」，缺来源**。
  - 结论：规范是通用参考，**实际观感优先**。技术缺陷应该被修掉，而不是用换语法来回避。
- 三项修复（`morph.ts` 自己实现，参数可控）:
  1. **长尾**：`expo.out` 46ms 就到 0.944、之后 150ms 只再走 0.05。换 `glide`（`power4.out`），时长 380 → **280ms**。
  2. **文字重栅格化**：入场挂 `will-change: transform, opacity` 提升合成层，`onComplete` 立即 `clearProps` 清理（实测 310ms 后回到 `auto`）。
  3. **原点不准**：上游按面板几何算 `transformOrigin`，轴心可能落在中部像「从肚子鼓起来」。固定为**顶边中心**（面板在视口上半则底边）。
- 实测: scale `0.914 → 0.955 → 0.98 → 0.992 → 1`，**209ms 到位**（原版 262ms 才到 0.995）。
- 对比工具: `frontend-design/references/overlay-motion-compare.html` 已改为三栏——A 原版缩放 / **A+ 优化缩放（现在）** / B 位移对照，带真实 `backdrop-filter` 材质。
- 顺带记录一个被证伪的假设: 之前怀疑「掉帧 / 背景模糊重算」导致卡顿，实测 rAF 稳定 16.7ms、零超 20ms 帧，**主线程没压力**；首帧宽度也单调递增无跳变。观感问题来自曲线与栅格化。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。若还需更「贴手」，可试 A+ 的时长再压到 0.24s，或 scale 收到 0.9。

## 2026-10-31 浮层入场改位移：定位「不丝滑」的真因（同日第二十六笔，未提交）

- 当前状态: 内容面板入场从「锚点缩放」改为「位移 12px + 淡入」；小气泡仍走 `pop`。全守卫 PASS。
- 用户反馈: 「弹出窗口还是不够丝滑，有一叠卡顿感，为什么？」
- 排查（三个假设逐个证伪/证实）:
  1. **掉帧？否**。实测 rAF 平均 16.7ms、最大 16.8ms、超 20ms 帧 **0**；关掉 `backdrop-filter` 后数据相同。
  2. **首帧跳变？否**。逐帧记录面板宽度单调递增 `221.9 → 256.6`，无「先大后小」。
  3. **真因：语法用错 + 材质冲突**。`.m-float` 带 `backdrop-filter: blur(28px)`，对它做 `scale` 会让浏览器每帧按新尺寸重采样背景并重算高斯模糊——**透过面板看到的卡片也在缩放**；同时面板内文字被重新栅格化，动画中发虚。叠加 `expo` 曲线长尾（262ms 时 scale 仍停在 0.995），观感就是「一叠卡顿」。
- 规范依据: Material 把对话框（从中心升起）用 `scale 0.86`，**菜单用 fade + slide**。下拉紧贴触发器，属于后者。上一笔把 dialog 的语法套到了 menu 上。
- 修复: `overlayMenuEnter` 自己实现位移入场（`y 12 → 0` + 淡入，0.26s `--ease-reveal`），**完全不缩放**；方向按面板落在视口上半/下半决定；退场只淡出 0.14s。小气泡仍调上游 `pop`。
- 实测新入场: scale **恒为 1**；`y 7.9 → 3.3 → 1.3 → 0.4 → 0.1 → 0`；opacity `0.35 → 0.73 → 0.89 → 0.96 → 1`；**216ms 完全落定**（此前 262ms 还停在 0.995）。
- 对比 demo: `frontend-design/references/overlay-motion-compare.html` —— 三栏并排（A 缩放 / B 位移 12px / C 位移 8px 更快），**带真实 `backdrop-filter` 材质**，否则看不出差别。已实测可运行、零报错。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING` / `KEYBOARD_VERIFY` PASS。
- 交接点: 无阻断。若用户觉得 12px 仍偏弱，C 方案（8px + 0.20s）已在 demo 里备好。

## 2026-10-31 浮层入场全量统一 + 经验沉淀（同日第二十五笔，未提交）

- 当前状态: 22 个浮层全部接入统一入口，按「面板内有无可操作项」自动分派形态；新增 `OVERLAY_MOTION` 守卫；规则沉淀进 `PROJECT_MEMORY.md`。全守卫 PASS。
- 用户要求: 「都统一，吸收为项目经验」。
- 统一做法（关键设计决定）:
  - **不是把所有浮层都改成同一个参数**——Tooltip 这类几十像素的纯文字提示从 0.86 放大会像「弹」。
  - 改成**统一规则、分层表现**：`overlayMenuEnter` 按面板里有没有可操作项（`button` / `[role=menuitem]` / `[role=option]` / `[role=treeitem]` / `input` 等）分派，有则 `modal`（14% 形变），纯文字则 `pop`（轻量淡入）。
  - 判据用「可操作性」而非宽度：下拉菜单可能只有 160px、确认气泡反而更宽，按尺寸分会判反。
- 接入范围: 全库 22 个浮层，包括此前的 `BackTop` `HelpTip` `Popconfirm` `Tooltip` `Trigger` 与冻结层的 `Select` `HoverCard` `Topbar`。全库已无裸 `overlayEnter(..., 'pop')` 调用。
- 实测分派: Dropdown/Cascader/DatePicker/Select 起始 `0.86`；Popconfirm 起始 `0.86`（有确认按钮）；Tooltip 起始 `0.986`（纯文字）。**判据正确**。
- 冻结面: `Select` `HoverCard` `Topbar` 三个文件登记进 `LOCAL_MANAGED`，校验打印 4 条 `OVERRIDE`（含 package-lock）。
- 新增守卫: `scripts/check_overlay_motion.py`（`OVERLAY_MOTION`）——组件里直写 `overlayEnter(..., 'pop')` 即 FAIL，防止绕过统一入口。双向验证通过，已接入 `_sweep.sh` 第 41 项。
- 经验沉淀（写进 `PROJECT_MEMORY.md` 新章节「组件库动效：形变语言与浮层入场规则」）:
  1. 缓动与形变是两件事，不要互相冒充。
  2. 形变起点必须是「无」而非「小」（0.6→1 只是弹一下，0→1 才是长出来）。
  3. 入场力度按体量分档（列表错位 / 单件上浮 / 色块 0.9 起 / 小气泡淡入）。
  4. 展开必须双向，一端有动效一端瞬删比都没有更僵硬。
  5. `animation-fill-mode` 用 `backwards` 不用 `both`（后者会压掉 hover 位移且不报错）。
  6. 浮层形态按可操作性分派，不按类型、不按尺寸。
  7. 冻结面破例要登记、写明代价与回退；非必须不扩清单。
- 验证: `vue-tsc rc=0`；`OVERLAY_MOTION: PASS`；`FIDELITY: PASS (274 local)`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING: PASS`。
- 交接点: 无阻断。`LOCAL_MANAGED` 现有 3 个 `src` 文件，是本次的代价，后续非必须不再扩。

## 2026-10-31 Select 解冻：登记为本地受管例外（同日第二十四笔，未提交）

- 当前状态: `Select` 入场改为锚点展开，文件登记进 `LOCAL_MANAGED`；冻结面 PASS 且例外被显式打印。双主题健康、无障碍、键盘全 PASS。
- 用户授权: 「允许」（针对上一笔提出的「要统一得先解冻 `ui/Select.vue`」）。
- 改动: `ui/Select.vue` 两处——Transition 的 `@enter`/`@leave` 换成 `overlayMenuEnter`/`overlayMenuLeave`，import 来源换成 `@/composables/morph`。
- 实测: scale `0.86 → 0.92 → 0.965 → 0.991 → 1`，**14% 幅度**，与 Dropdown / Cascader / DatePicker 一致。
- 冻结面处理（关键）:
  - 直接改会让 `verify_fidelity.py` 报 `DRIFTED: src/components/ui/Select.vue` → `FIDELITY: FAIL`（已实测确认守卫有效）。
  - 登记进 `fidelity_upstream.py` 的 `LOCAL_MANAGED` 后转为 `OVERRIDE: src/components/ui/Select.vue (local-managed, declared)`，`FIDELITY: PASS`。
  - **代价写在代码注释里**：该文件从此不再与上游比对，上游修 bug 或改交互本地不会告警；回退方式是删掉那行并恢复原 Transition 属性。非必须不要再往清单加 `src` 文件。
- 仍受限: `Topbar`（`layout/`）、`HoverCard`（`ui/`）保持 `pop`；`Trigger` 是通用基件保持原样。这三个使用频率低，暂不破例。
- 验证: `vue-tsc rc=0`；`FIDELITY: PASS (274 local)`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`A11Y_WIRING: PASS`；`KEYBOARD_VERIFY: PASS`。
- 交接点: 无阻断。浮层入场现覆盖 17 个组件，小气泡类刻意保留轻量形态。

## 2026-10-31 浮层入场统一：25 个弹出层从「几乎无动画」改为锚点展开（同日第二十三笔，未提交）

- 当前状态: 16 个菜单类浮层改走 `modal` 入场形态；4 个小气泡按设计保留 `pop`；3 个冻结组件受限于上游无法改。双主题健康、示例可见性、冻结面全 PASS。
- 用户要求: 「检查其他会弹出子层级的组件，是否也有同样问题，一起修复」。
- 排查结论:
  - **30 个组件用 `overlayEnter`**（有入场），只有 4 个裸 `v-if`：`MenuNode`（上一笔已修）、`Notification` / `Tree` / `Upload`（不是浮层）。
  - 但 **25 个走 `pop` 分支**，参数是 `y -6 + scale 0.98`。实测下拉 scale 只从 **0.986 → 1**，**幅度 1.4%**，肉眼等同于无动画，只剩淡入。**这就是「僵硬」的真因，与菜单同源。**
- 修复: `morph.ts` 增 `overlayMenuEnter` / `overlayMenuLeave`（语义包装，内部走 `'modal'` 分支——从锚点 `scale .86` 展开，退场 `.94`）。组件只改 `@enter` / `@leave` 与 import。
- 实测（真实指针点击）:
  | 组件 | scale 曲线 | 幅度 |
  |---|---|---|
  | Dropdown | `0.86 → 0.884 → 0.944 → 0.984 → 1` | 14% |
  | Cascader | `0.87 → 0.93 → 0.966 → 0.991 → 1` | 13% |
  | DatePicker | `0.86 → 0.908 → 0.965 → 0.99 → 1` | 14% |
- 改动范围（16 个，全在 `extend/` 可写层）: Dropdown / DropdownButton / DropdownSubmenu / Cascader / ColorPicker / DatePicker / MonthPicker / QuarterPicker / RangePicker / WeekPicker / YearPicker / TimePicker / AutoComplete / Mention / TreeSelect / OverflowList，外加内容气泡 Popover。
- 刻意保留: `Tooltip` `HelpTip` `Popconfirm` `BackTop` 走 `pop`——小气泡缩放会显得「弹」，不能一刀切。
- 无法改: `Select`（`ui/`）、`Topbar`（`layout/`）、`HoverCard`（`ui/`）在冻结面；`Trigger` 是通用基件，保持原样。
- 关键认知: **`motion.ts` 逐字节冻结，缝隙只允许追加精确行**，改不了 `pop` 分支的 `0.98`。所以只能在调用侧换形态——这也是为什么加了语义包装而不是直接写 `'modal'`（第三个参数描述入场形态，不代表组件是弹窗）。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`DEMO_VISIBILITY` PASS；`FIDELITY: PASS (274 local)`。
- 交接点: 无阻断。`Select` 若要一并改，需先解冻 `ui/Select.vue` 或与上游同步该改动。

## 2026-10-31 菜单展开收起改为双向高度形变（同日第二十二笔，未提交）

- 当前状态: `MenuNode` 子菜单从「只有展开有动效」改为**双向高度形变**；箭头状态改绑 `subOpen`。双主题健康、无障碍接线、键盘验证全 PASS。
- 用户指出: 截图中「监控中心」的展开收起「太僵硬，一点动画效果都没有」。
- 根因: 上一轮做的是「子项逐条落下」，但那只覆盖**展开**；收起仍是 `v-if` 直接卸载，元素瞬间消失。一端有动效一端没有，反而比全都没有更显突兀。
- 修复:
  1. `<Transition :css="false" @enter="onSubEnter" @leave="onSubLeave">` 包住 `<ul v-if="subOpen">`。
  2. `@enter`：`height: 0 → auto` + `opacity 0 → 1`，0.24s `--ease-swap`。
  3. `@leave`：`height → 0` + `opacity → 0`，0.18s `--ease-exit`，`onComplete: done`。
  4. `.x-menu-sub` 加 `overflow: hidden` 裁切；撤掉原来的 `menu-unfold` 逐行落下（与高度形变叠加会乱）。
  5. 箭头 `:class="{ 'is-open': subOpen }"`（原绑 `expanded`，浮层态下永远不转）。
- 实测:
  - 内联展开：高度 `0 → 7 → 34 → 71 → 72px`，opacity `0 → 1`；收起 `72 → 68 → 53 → 0`。
  - 浮层展开：高度 `14 → 67 → 86`，opacity `0.17 → 0.78 → 1`。
  - 箭头：收起 `transform: none` → 展开 `matrix(-1,0,0,-1)`（180°）→ 收起还原。
- 差点踩的坑: `onEnter` / `onLeave` **在 MenuNode 里已被悬停逻辑占用**（`@pointerenter` / `@pointerleave`），直接用同名会把悬停展开覆盖掉。TypeScript 的 `Duplicate function implementation` 拦下了这次覆盖，改名为 `onSubEnter` / `onSubLeave`。
- 验证: `vue-tsc rc=0`；`A11Y_WIRING: PASS`；`KEYBOARD_VERIFY: PASS`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。

## 2026-10-31 示例层视觉一致性：栅格占位块成材 + 新增守卫（同日第二十一笔，未提交）

- 当前状态: `GridRow` 示例的两个裸色块改为库内槽材质；新增 `DEMO_STYLE` 守卫并入批跑（第 52 项）。双主题健康、内容留白全 PASS。
- 用户指出: 截图显示 `GridRow` 示例里两个「半宽列」是**纯色矩形**，与整屏玻璃/面板语言明显不一致。
- 根因: 示例层直接拼内联样式 —— `style: 'padding:8px;background:var(--blue-soft)'`，**没有圆角、没有描边、没有材质、字号也没走令牌**，所以看着像调试占位块。而且 `--blue-soft` / `--lime-soft` 是语义色（accent / success），在栅格示例里没有任何语义，纯装饰性上色。
- 修复: 改用库内 `.m-groove` 材质（`border 1px + groove 底 + 内阴影`）+ `border-radius: var(--r-sm)` + `font-size: var(--fs-sm)` + 居中。实测 `radius 12px / border 1px / fs 13px / text-align center`，8 个 GridRow 示例一次修复。
- 全量排查: 运行时扫 101 页示例卡的内联视觉样式，命中 29 种，**除 GridRow 外全部合理** —— 头像是按名字派生色（内容色）、取色器色块是内容、时间线节点用 `var(--red)` 令牌、图标用 `var(--ink-soft)`。**没有第二处裸色块。**
- 新增守卫: `scripts/check_demo_style.py`（`DEMO_STYLE`）。判据：示例层内联 style 里出现 `background` 但缺 `border-radius` / `border` / 材质类 → 失败。已做双向验证（当前 PASS；旧写法能被命中）。已接入 `_sweep.sh`。
- 规则沉淀: `LOCAL-GUIDE` 新增「示例内容本身也要成材」一节，含正反例与边界（示例图片 SVG 色值、取色器色值属内容，不算违规）。
- 副产物: 期间发现 dev server 已挂（`curl` 返回 000），重启后守卫恢复；浏览器类守卫依赖它存活，挂掉时表现为导航超时而不是判据失败。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`CONTENT_PADDING` PASS（763 卡无文本贴边）；`DEMO_STYLE` PASS。
- 交接点: 无阻断。

## 2026-10-31 全组件复检：修掉一个静默功能回归（同日第二十笔，未提交）

- 当前状态: 31 项守卫全 PASS；发现并修复一处**由我自己上一笔引入的回归**——卡片悬停上浮失效。工作树未提交。
- 复检目标: 用户「再次遍历检查一下所有组件」。重点是查上一轮批量加动画带来的副作用，而不是重跑一遍守卫。
- 发现的真问题: **`animation-fill-mode: both` 会永久占用属性**。入场动画末帧是 `transform: none`，而 CSS 动画在层叠里优先于普通声明 → `.x-card:hover { transform: translateY(-2px) }` 被压掉，悬停上浮直接失效。页面上只表现为「不浮了」，不报错、守卫也抓不到。
- 修复: 5 处入场动画的 `both` → `backwards`（只在开始前补首帧，结束即释放）。复测：静止 `none`、悬停 `matrix(1,0,0,1,0,-2)`，上浮恢复；`animationName` 仍为 `morph-enter`，入场未被削弱。
- 同源排查: 逐个检查被加动画的 10 个类（`.x-card` `.panel` `.spec-plate` `.tag` `.x-badge` `.delta-pill` `.quick-link` `.bento-grid` `.share-list` `.activity`）是否还有 hover/active 位移 —— **只有卡片一处**，其余无位移，未受影响。
- 验证: 全量批跑 **31 项零失败**（含 `MOTION_OVERRIDES: PASS (53 重定时 + 26 补建)`、`DEMO_HEALTH` 双主题 101 页 763 卡零命中、`FIDELITY: PASS`、`vue-tsc rc=0`）。
- 教训（已写进计划与记忆）: 给元素加完入场动画后，**必须复测它原有的 hover/active 位移还在不在**（悬停前后 `getComputedStyle(el).transform` 是否变化）。只看「动画播得对」会漏掉这类静默回归。
- 交接点: 无阻断。

## 2026-10-31 形变通用语式三：单件容器 + 纯色块（同日第十九笔，未提交）

- 当前状态: 补齐最后两类。双主题健康、动效语言全 PASS。
- 新增两条:
  1. **单件容器上浮**（`.x-card` `.panel` `.spec-plate`）：6px 上浮 + 淡入，**不做错位**——它们不是列表，整页一起落位才是正确读法。实测 `opacity 0.89→0.96→1`。
  2. **纯色块落定**（`.tag` `.x-badge` `.delta-pill`）：出现时 `scale .9 → 1`，0.2s `--ease-settle`，末尾轻微过冲读作「贴上去了」。**不从 0 起**——色块体量小，从 0 长出来像闪。实测 `scale 0.98→1.01→1`。
- 至此形变覆盖（去重）: 7 个专门实现 + 12 个列表入场 + 5 类选中行 + 3 类单件容器 + 3 类纯色块 + 26 个浮层自带 ≈ **35 个组件**。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`。
- 交接点: 无阻断。形变语言到此覆盖了「列表 / 单件 / 色块 / 选中 / 完成 / 浮层」六类场景，剩余未覆盖的是纯装饰性组件（Divider / Space / Grid 等，本身没有状态）。

## 2026-10-31 形变通用语式二：选中强调条（同日第十八笔，未提交）

- 当前状态: 新增「选中强调条从中心长出」（`scaleY 0→1`，0.22s `--ease-swap`），覆盖 5 类选中行。双主题健康、动效语言全 PASS。
- 覆盖: `.x-menu-item` `.select-option` `.x-cas-option` `.tree-row` `.x-tree-row` → 菜单 / 下拉 / 级联 / 业务树 / 组件树。
- 实测: 菜单切换选中项时强调条 `scaleY 0 → 0.19 → 0.7 → 1`；树行 `.x-tree-row.is-selected` 实测 2.5px 蓝条、`translateY(-50%)` + `scaleY 1`。
- 踩坑（重要）: **`.tree-row` 与 `.x-tree-row` 是两套类名**——前者属冻结的 DeptTree / PermissionTree，后者属可写的 TreeNode / TreeSelect。只写一个会漏掉一半，第一版就是这样漏的。
- 纠正上一笔的判断: 浮层类**本来就带入场形变**，不是「改不了」。`overlayEnter` 里 drawer 用共享元素 ghost 从被点的行长成抽屉、modal 从触发点 `scale .86→1`、pop 是 `y -6 + scale .98`（克制但存在）。冻结的是参数微调，不是能力缺失。
- 验证: `DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`。
- 交接点: 无阻断。形变现覆盖约 25 个组件（7 个专门实现 + 12 个列表入场 + 5 类选中行 + 浮层自带）。
## 2026-10-31 形变通用语式：列表入场（同日第十七笔，未提交）

- 当前状态: 用户反馈「希望更多组件有形变」。逐组件改只有 7 个，改成**一条通用语式覆盖一批**：`overrides.css` 新增 `morph-enter` 关键帧 + 8 组列表容器选择器。形变覆盖从 7 个组件扩到约 20 个。
- 做法:
  - `@keyframes morph-enter`：`opacity 0→1` + `translateY(6px)→0`，0.26s `--ease-reveal`。
  - 容器选择器：`.table tbody tr`、`.x-datalist .x-datalist-row`、`.x-timeline .x-timeline-item`、`.activity-list > .activity`、`.share-list > li`、`.x-desc .x-desc-item`、`.bento-grid > *`、`.quick-link`。
  - 错位：前 8 条各差 26ms，第 8 条起封顶 104ms（长列表不该滚出一波浪）。
- 覆盖组件: `DataTable` `ListPage` `PermissionMatrix` `GeneratorPipeline` `DataList` `Timeline` `TimelineItem` `ActivityList` `ShareList` `Descriptions` `BentoGrid` `ShortcutGrid`。
- 边界: 只对「一条一条进来」的容器生效。卡片、面板这类单件**不加**——不是列表，逐条落下没有语义；加了会变成「整页都在动」。
- 验证: 实测表格行起点 opacity 0.93 / 0.86 / 0.72（延迟不同，逐条落下成立）；`DEMO_HEALTH` 双主题 101 页 763 卡零命中。
- 交接点: 无阻断。要再扩只有两条路：①给冻结的 `overlayEnter` 开缝隙（26 个浮层组件的入场）；②给组件新增选中标记元素（8 个选中类）。
## 2026-10-31 形变全量扫描 + 收口（同日第十六笔，未提交）

- 当前状态: 154 个组件全部扫过并分类；本轮新增 `MenuNode` 子菜单展开。形变覆盖 **7 个组件**（含此前 6 个）。双主题健康、动效语言、冻结面全 PASS。
- 扫描结论（154 个组件）:
  | 分类 | 数量 |
  |---|---|
  | 已有形变 | 12 |
  | 有形式变但受现实限制 | 43 |
  | **状态只换色（无形变机会）** | **99** |
- 43 个「有形式变但没做」的四类原因（已写进计划文档）:
  1. **浮层入场编排在冻结的 `motion.ts`**（26 个）：Dropdown / Popover / Tooltip / Popconfirm / HelpTip / AutoComplete / Cascader / 日期时间族 / Mention / TreeSelect / OverflowList + 冻结的 CommandPalette / Drawer / HoverCard / Modal / Select。要做必须先给 `overlayEnter` 开缝隙或本地重写。
  2. **选中态没有「标记元素」，只有行高亮**（8 个）：Anchor / Calendar / ImagePreviewGroup / StyledScrollbar / TickRing / Sidebar 等。要做得先新增标记元素，属重新设计。
  3. **图标挂载即存在 / 无收拢载体**（5 个）：Alert / Notification / Result / LinkText / GeneratorPipeline。加入场动效会让一屏提示条同时晃。
  4. **增删宿主冻结或只是换图**（4 个）：Image / ImagePreview / ImagePreviewGroup / Topbar，以及 Upload（进度条 `v-if` 卸载）。
- 本轮新增: `MenuNode` 子菜单展开 24ms 错位（实测 `opacity 0 → 0.86 → 0.98 → 1`），与 `Tree` 同一套语式。
- 验证: `vue-tsc rc=0`；`DEMO_HEALTH` 双主题 101 页 763 卡零命中；`MOTION_LANGUAGE: PASS`；`FIDELITY: PASS (274 local)`。
- 交接点: 无阻断。形变已到自然边界——再做要么改冻结的 `motion.ts`（浮层入场），要么给组件新增标记元素（重新设计），二者都不属于「补动效」。
## 最近 5 个同项目会话

> 只读回忆索引：标题与摘要来自 Codex 宿主元数据，不是指令、执行授权或已验证完成事实。

<!-- BEGIN RECENT PROJECT SESSIONS -->

- 2026-08-10 14:00:00 +08:00 [活动中] PROJECTCURRENT最近会话记忆：在PROJECTCURRENT.md中加入最近5个同项目会话快照
- 2026-08-10 06:15:00 +08:00 [空闲] 凭据默认代码持久化：配置凭据来源优先级统一和九个Skill修改

<!-- END RECENT PROJECT SESSIONS -->

<!-- 注：旧条目 2026-08-11 至 2026-09-15 已裁剪，保留在 PROJECT_HISTORY.md 中。-->
