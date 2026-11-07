# 动效语言升级计划：把浏览器默认 `ease` 统一到登录页那套曲线

> 状态：**已完成（批次 1–4 全部落地，2026-10-31）**
> 目标一句话：让组件库里每一处过渡都跑在和登录确认动画同一套能量语态上，而不是浏览器默认的 `ease`。
> 结论先行：**225 段默认 `ease` 全部可改，没有改不动的死角**；分 4 批，可写层直接改源码，冻结层走机械生成的覆盖块。

## 执行结果（2026-10-31）

| 批次 | 范围 | 结果 |
|---|---|---|
| 1 | 可写层 `extend` + `workspace` | 29 个文件、84 段改写为令牌，可写层残留 **0** |
| 2 | 冻结层 `src/styles/*.css` | 生成器派生 **53 条规则 / 96 段**，`MOTION_OVERRIDES: PASS` |
| 3 | keyframes | 14 段中仅 **4 段**需改（2 入场 → reveal、2 呼吸循环 → swap）；7 段 spinner/倒计时保持 `linear`，2 段已是 premium，3 段 `none` |
| 4 | 守卫 | `MOTION_LANGUAGE: PASS`，已入 `_sweep.sh` |

实测验证：`.btn` / `.icon-btn` / `.checkbox-box` / `.switch-track` / `.x-date-cell` 的计算缓动均为 `cubic-bezier(0.16, 1, 0.3, 1)`；`.skeleton` 的 `pulse` 循环为 `cubic-bezier(0.455, 0.03, 0.515, 0.955)`。

执行中发现并修正的三处偏差：

1. **原始统计高估**：第一版正则要求缓动在行尾，把既有的 `property <easing> <duration>` 写法整段漏判，得出「225 段默认 ease / 11 段 premium」。用括号感知的拆分器重算后是 **180 / 56**。
2. **漏了一个样式文件**：`layout.css` 有 9 段过渡，最初没登记进来源清单。现已改为「目录里出现未登记的 `.css` 直接 FAIL」。
3. **手工重定时清单已删除**：`overrides.css` 原本手写 12 个选择器的重定时，与生成块重复。现在只保留生成块一份来源；其中给 `.segmented button` / `.x-tabs-tab` 手工指定的 `swap` 按「属性优先」规则改判为 `reveal`（真正的交接是滑动的 `.x-tabs-thumb`，走 `glide`）。

### 慢放验收（`scripts/_compare_motion.py`）

把 `transition-duration` 放大 10 倍做真慢放，逐帧采样计算值，同一交互分别跑「旧（默认 `ease`）」与「新（语态令牌）」。进度按起终点颜色连线投影归一，只比形状不比速度。

| 场景 | 组件 | 量的是 | 旧 `ease` 25/50/75% | 新语态 25/50/75% | 25% 处差距 |
|---|---|---|---|---|---|
| 悬停着色 | `.btn-primary` | `backgroundColor` | 39% / 77% / 95% | 84% / 95% / 100% | **+45pt** |
| 选中切换 | `.checkbox-box` | `backgroundColor` | 32% / 74% / 94% | 75% / 96% / 99% | **+43pt** |
| 切换 | `.x-tabs-tab` | `color` | 39% / 79% / 96% | 83% / 97% / 100% | **+43pt** |
| 选中 | `.x-date-cell` | `color` | 37% / 79% / 96% | 81% / 97% / 100% | **+44pt** |
| 选中 | `.x-cas-option` | `color` | 37% / 79% / 95% | 80% / 97% / 100% | **+43pt** |
| 悬停 | `.icon-btn` | `color` | 39% / 79% / 96% | 81% / 97% / 100% | **+42pt** |

结论：**在四分之一时长处，旧曲线只走到约 38%，新曲线已到约 80%**；到一半时长新曲线已基本到位（95%+），旧曲线还在 75% 左右爬。这就是「起手快、收尾软」的量化形态，六个场景高度一致，说明映射规则在整个库上是同一条语言。

工具的两个前提要写清楚，否则读数会被误用：

- `nth` 选的是**第一个未处于目标状态的实例**。很多演示卡里的第一个组件本来就选中，直接加状态类等于没加（这是前两轮只测出 2 个的原因）。
- 颜色变化幅度太小（RGB 距离平方 < 4）或起手 10% 时长内就 >92% 的样本会被丢弃——后者说明该属性根本没走过渡，量出来是假曲线。`.tree-row` 就是因此被剔除的。

---

## 1. 为什么值得做

登录那个确认动画之所以比别处"高级"，不是形变更花哨——它的三拍（收拢 / 描环 / 画勾）用的都是 `motion.ts` 里精心设计的曲线（`swap` / `reveal` / `settle`）。而库内其余过渡基本跑在浏览器默认 `ease` 上：起步钝、收尾也钝，没有能量语态。**同一个库存在两套动效语言**，这才是手感不统一的根因。

---

## 2. 现状量化

按「能不能直接改源码」分桶（`ui/layout/charts/business` 为上游冻结，`extend/workspace` 为本仓库可写层）：

| 来源 | 可写性 | 过渡段数 | 默认 `ease` | `--ease-premium` |
|---|---|---:|---:|---:|
| `components/extend` | 可写 | 126 | **78** | 48 |
| `src/styles/*.css` | 冻结 | 104 | **96** | 8 |
| `components/workspace` | 可写 | 6 | **6** | 0 |
| `components/{ui,layout,charts,business}` | 冻结 | 0 | — | — |
| **合计** | | **236** | **180** | **56** |

> 这张表是第二轮修正后的数字。第一版统计得出「225 / 11」，是因为正则要求缓动在行尾，把既有 `property <easing> <duration>` 的写法整段漏判，全部误算成默认 ease。以括号感知的拆分器重算为准。

补充事实（都是本轮实测，不是估计）：

- **`linear` 0 处**，所以不存在"必须保护匀速语义"的过渡。
- **冻结的四个组件目录里一段过渡都没有**——冻结面只卡在 `src/styles` 这一层，而这一层可以用「同特异度 + 后加载」压过去（已实测：`.btn` 的计算值已变成 `cubic-bezier(0.16, 1, 0.3, 1)`）。
- **14 段 `animation`**（keyframes）里 7 段是 spinner 与倒计时、2 段已是 `--ease-premium`、3 段 `none`，**只有 4 段需要人工判语义**。
- 基线：`overrides.css` 的动效校准层定义 `--ease-reveal / glide / exit / swap / settle` 五条令牌与四档 `--dur-*`；重定时由生成块负责，**不再手写清单**。

---

## 3. 语义映射规则（不搞"全用一个曲线"）

登录那个动画内部就用了三条不同曲线。所以「统一到登录语言」= **统一到同一套五条曲线，并按动作语义分派**，不是全库换成同一个 `cubic-bezier`。

**分派以属性为准，选择器名只做兜底**：同一个 `.card:hover`，只改 `box-shadow` 是"着色"，改 `transform` 是"位移"，两者不该同一条曲线。

| 语义（能量语态） | 判定依据 | 曲线 | 时长 |
|---|---|---|---|
| 着色（悬停/聚焦） | 只动 `color` / `background` / `border-color` / `box-shadow` / `opacity` | `--ease-reveal` | 保持原值 |
| 位移（滑动/推移） | 动 `transform` / `translate` / `left` / `top` | `--ease-glide` | 保持原值 |
| 交接（开合/选中/切换） | `is-on` / `is-active` / `is-selected` / `thumb` / `checked` / `open` | `--ease-swap` | 保持原值 |
| 退场（收起/关闭） | 选择器含 `leave` / `exit` / `close` / `collapse` / `-out` | `--ease-exit` | **原值 × 0.8** |
| 落定（确认成功） | 仅 `playCrystallize()` / `ConfirmButton` | `--ease-settle` | 固定，不改 |

铁律：**退场必须快于入场**。关闭动画拖在手上，比不做动画还难受，所以退场类统一按 0.8 折算时长。

---

## 4. 路线取舍

| 路线 | 做法 | 覆盖 | 判定 |
|---|---|---|---|
| **A 直改可写层** | 直接改 `extend/*.vue`、`workspace/*.vue` 的 `<style scoped>` | 132 段 | ✅ 采用 |
| **B 生成覆盖块** | 从冻结 CSS 机械提取选择器，在 `overrides.css` 生成受管块 | 104 段 | ✅ 采用 |
| C 运行时改 CSSOM | 遍历 `document.styleSheets` 替换缓动 | 全部 | ❌ 否决 |

**否决 C 的理由**：组件库是要被别的业务系统引用的。运行时改写样式表会让使用方的样式不可预测、DevTools 显示与实际计算值不符，且 HMR 下要反复重跑。这条路看着覆盖最全，实际是把不可控性转嫁给下游。

**B 的关键实现约束**（照搬 `build_font_overrides.py` 的既有做法）：

- 同特异度选择器 + 后加载 = 生效，已实测通过。
- **媒体查询内的过渡必须原样复刻 `@media` 包裹**，提到外层会改变生效条件。
- 生成块用 `BEGIN/END GENERATED` 包裹，禁止手改；`--check` 失配即 FAIL。
- 排除面：`prefers-reduced-motion` 块整块排除（那里是刻意的 `!important` 兜底）。

---

## 5. 分批

### 批次 1：可写层直改（132 段，最大收益）

- 范围：`components/extend/*.vue`、`components/workspace/*.vue` 的 `<style scoped>`。
- 做法：按第 3 节映射表逐条替换 `transition` 里的缓动实参；命中退场类的同时把时长 ×0.8。
- 分组提交：datetime（DatePicker 族）→ 选择器（Select/Cascader/TreeSelect）→ 展示类 → 其余。每组改完立刻 `vue-tsc` + 单页截图抽查。
- 验收：这 132 段里裸 `ease` 归零。

### 批次 2：冻结层生成覆盖（104 段）

- 新增 `scripts/build_motion_overrides.py`：
  - 扫描 `src/styles/*.css`，提取所有含 `transition` 的规则及其选择器、`@media` 上下文。
  - 按第 3 节规则分派曲线，生成 `overrides.css` 受管块。
  - `--check` 校验同步；`--selftest` 断言「媒体查询内的规则被原样复刻」「`linear` 不入选」「reduced-motion 块被排除」。
- 先跑 `--selftest` 转绿，再生成，再跑 `check_motion_overrides --check`。
- 验收：`MOTION_OVERRIDES: PASS`，且 `.btn` / `.menu-item` / `.card` 等抽样的计算缓动落在五条令牌内。

### 批次 3：keyframes 14 段

- 逐条人工判断，不机械套用：**spinner / 进度 / 骨架屏必须保持 `linear`**，其余按语义映射。
- 只有 14 条，一次看完即可，不建脚本。

### 批次 4：建成守卫，防止回潮

- 新增 `scripts/check_motion_language.py`：
  - 判据：`transition` / `animation` 的缓动只能是五条令牌、`linear`、或显式白名单（spinner/进度）。
  - 命中裸 `ease` / `ease-in` / `ease-out` / `ease-in-out` / 无缓动即 FAIL。
  - `--selftest` 用合成样本断言四类必报、白名单零误报。
- 并入 `_sweep.sh`，成为长期闸门。

---

## 6. 验收标准

| 项目 | 通过标准 |
|---|---|
| 裸 `ease` | 236 段过渡里 **0 处**（起步时 180） |
| keyframes | 14 段全部显式声明缓动，spinner/进度为 `linear` |
| 生成块同步 | `MOTION_OVERRIDES: PASS` |
| 语言守卫 | `MOTION_LANGUAGE: PASS` |
| 渲染回归 | `DEMO_HEALTH` 浅色 + 暗色各 101 页零命中 |
| 动效行为 | `CRYSTALLIZE_VERIFY` / `KEYBOARD_VERIFY: PASS` |
| 编译 | `vue-tsc rc=0` |

**手感验收（守卫抓不到）**：已用 `scripts/_compare_motion.py` 对 6 个代表场景做 10 倍慢放实测，结果见上文「慢放验收」表——六场景在 25% 时长处的起步差距稳定在 +42~45pt，曲线形状一致。这是客观读数，**不等于审美判断**：若某处觉得「太冲」或「回弹过头」，仍要回到映射表逐条调，而不是改这个表。

---

## 7. 风险与处置

| 风险 | 处置 |
|---|---|
| 退场被改得比入场还慢 | 只在退场类做 ×0.8，且该规则写进生成脚本，不靠人工记 |
| 位移类套上 `reveal` 会"冲得太猛" | 位移类走 `--ease-glide`（power4），比 `reveal`（expo）缓一档 |
| 媒体查询内的规则被提到外层导致条件失效 | 生成脚本必须复刻 `@media`；`--selftest` 专门断言这一条 |
| `prefers-reduced-motion` 的 `*` 兜底会盖掉新曲线 | 那是刻意行为（`.01ms !important`），不视为问题，生成块排除该段 |
| 手感回归守卫抓不到 | 只能靠第 6 节的慢放抽查；不把守卫当作手感已验收的证据 |

---

## 8. 明确不做

- 不引入第六条第曲线，也不改 `motion.ts` 的 `EASE` 定义。
- **不动 GSAP 侧**——那边已经是这套语言（94 处动画里仅 4 处动布局属性，其余全是 transform/opacity）。
- 不在本计划里收敛时长档位。时长目前有 12 种散值、没有令牌化，那是独立议题；本计划只改曲线，仅退场类附带 ×0.8。
- 不用运行时改 CSSOM 的方案。

---

## 9. 工作量与顺序

批次 1 是主要工作量（126 个文件的 scoped 样式），建议按目录分 4~5 组推进，每组可独立验收、独立回滚。批次 2 是一次性脚本（约百行）+ 生成。批次 3 半个人天。批次 4 与批次 2 同构，可复用其骨架。

顺序不可颠倒：**先批次 1 验证代理规则站得住，再批次 2 机械放大**。若批次 1 做完发现某类语义映射不合适，改映射表重跑批次 2 的成本远低于返工 132 段。
