# 新增 / 改动组件检查清单

> 在 `frontend-design/` 目录下执行本文命令。每道闸门都有明确的通过串，**看到通过串才算过**，不要凭感觉收工。
> 本文是操作性清单，规则正文在 `component-library/LOCAL-GUIDE.md`；两者冲突时以 LOCAL-GUIDE 为准，并回来修本文。

## 0. 先定形态，再动手

形态决定后面所有接线，选错会一路返工。

| 组件形态 | 键盘模式 | 参照实现 | 硬约束 |
|---|---|---|---|
| 下拉 / 级联 / 组合框 | combobox：焦点留触发器 + `aria-activedescendant` | `Cascader.vue` | **不给每个选项加 `tabindex`**，一列十几项会把 Tab 序列撑爆 |
| 选项卡 / 单选组 | roving tabindex：当前项 `0`，其余 `-1` | `Tabs.vue`、`AppearanceSettings.vue` | 方向键移动时必须把焦点一起带过去 |
| 可点列表项 | 保留 `<ol>/<li>`，只给可点项补 `tabindex` | `Steps.vue` | **不换成 `role="button"`**，换了 `<ol>` 就没有列表项 |
| 纯展示 / 纯容器 | 不接键盘 | `Panel.vue`、`Band.vue` | 别为了「看起来完整」硬加 `tabindex` |

## 1. 契约层

- [ ] props 有默认值时用 `withDefaults`，默认值必须是**自包含字面量**。引用同文件里的常量会在编译期报 `defineProps() cannot reference locally declared variables`，**整个画廊 500**，页面一片空白。
- [ ] 每个声明的 prop 都真的被用到；不用就删。只在 `withDefaults` 默认值里回过一次名，不算「用到」。
- [ ] 每个派发的事件都在 `defineEmits` 里声明；声明了的事件都要真的派发。
- [ ] 新增 / 删除 prop 后按序重跑三连（顺序不能反，后一个读前一个的产物）：

```bash
node scripts/build_component_catalog.mjs          # 契约索引
node scripts/build_demo_variants.mjs              # 示例变体
node scripts/build_demo_events.mjs                # 事件表
```

## 2. 样式层

- [ ] 样式只写在组件自身 `<style scoped>` 里。`src/styles/*.css` 是上游冻结面，一个字节都不能改。
- [ ] 颜色只引用 `src/styles/tokens.css` 的变量，**禁止硬编码色值**。两个已知例外：`ColorPicker`（色板本身就是十六进制）与 `AppearanceSettings` 的主题缩略图（必须脱离当前主题取色，否则深色下三张卡糊成黑白两团）。
- [ ] 字号只用五档令牌 `--fs-caption / --fs-sm / --fs-body / --fs-lg / --fs-title`，不写裸 `font-size: 13px`。裸写会被 `FONT_OVERRIDES` 判失配。
- [ ] 材质复用全局 `.m-*` 类，动效复用 `src/composables/motion.ts` 的 `overlayEnter / overlayLeave / settlePop`。
- [ ] 浅色与深色各看一遍再收工（`DEMO_HEALTH` 默认只扫浅色，必须显式加 `--theme dark`）。

### 动效（与样式同层：落点都在 CSS / GSAP）

- [ ] 能说出这条动效属于哪种能量语态：蓄 / 放 / 导 / 结 / 停摆。说不出的是装饰，不做。
- [ ] 曲线与时长只用 `motion.ts` 的 `EASE` / `DUR`，或 `overrides.css` 动效校准层的 `--ease-*` / `--dur-*`。**不要新起一套**。
- [ ] CSS 侧的 `transition-timing-function` 走语义曲线，不写裸 `ease`（默认 `ease` 起步钝、收尾也钝，没有能量语态）。
- [ ] 退场永远快于入场；进度条 / 跑马灯 / 骨架屏保持 `linear`，不要把匀速改成变速。
- [ ] 成功用「结」，加载用 spinner，失败用图标 + `--red-text`。**三种语态不要混**：把落定做成转圈，成功会看起来没结束。
- [ ] 需要确认感的关键提交用 `ConfirmButton`（或直接调 `playCrystallize()`）；`motionSkipped()` 时必须**直接给终态**，不能停在半收拢。
- [ ] 失败态不要在主色实底上压 `--red-text`——那是给浅底用的字色，红字铺蓝只有 1.01:1。用 `--red-soft` 底 + `--red-text` 字。
- [ ] 落定后按钮里只剩图形时，可访问名要挂在**按钮本体**的 `aria-label` 上；挂在内层圆上读屏读不到按钮名（守卫判 `noName`）。

## 3. 示例层

- [ ] 至少 3 组示例：基础 + 真实可见差异。只改文字标签不算差异。
- [ ] 每格提示写「组件说明 + 本格示例差异」两段，差异由 `views/gallery/demo-guides.ts` 按该格 props 推导，不要退回默认文案。
- [ ] 声明的事件都要在示例里接一次可见反馈，否则按钮点了没反应，看着像坏控件。
- [ ] 组件归进合适的卡片规格（`inline` / `panel` / `stage` / `overlay`）：表格被裁是缺横向空间，加高只会把空白放大。
- [ ] 新组件要在后台可达（`check_admin_component_coverage.mjs` 要求 100%）。

## 4. 无障碍层

- [ ] 键位齐不齐：`ArrowDown/Up` 在当前列移动并跳过 `disabled`、`ArrowRight` 进下级、`ArrowLeft` 退上级、`Home/End` 到首末、`Enter/Space` 落定、`Esc` 收起并把焦点还给触发器。
- [ ] 所有可聚焦项都有 `:focus-visible` 焦点环。补了 `tabindex` 却没有焦点环，等于键盘用户看不见自己停在哪。
- [ ] `disabled` 不能只拦行为：要有 `aria-disabled`，视觉禁用态交给调用方按 `[data-disabled]` 处理。运行中被置为禁用时要立刻收起已打开的浮层。
- [ ] 图标按钮必须有可读名（`aria-label` / `aria-labelledby` / `title`）。
- [ ] 下列情况**属于豁免，不要当缺陷改**：`.input-clear` / `x-tag-x` / `x-tabs-close` / `x-tree-arrow` 微型动作不占 Tab 位；`role="option"` / `role="treeitem"` 由上层方向键驱动；遮罩点击（`Esc` 覆盖同一操作）；`*-trigger` 包装层（可访问元素来自插槽）；`input-shell`（点击只为聚焦内部 input）。

## 5. 收口闸门

按顺序跑，全绿才提交：

```bash
# 静态
python scripts/check_component_contracts.py --selftest   # CONTRACTS_SELFTEST: PASS
python scripts/check_component_contracts.py              # CONTRACTS: PASS
python scripts/check_a11y_wiring.py --selftest           # A11Y_WIRING_SELFTEST: PASS
python scripts/check_a11y_wiring.py                      # A11Y_WIRING: PASS
python scripts/verify_fidelity.py --offline              # FIDELITY: PASS
python scripts/test_component_inventory.py               # INVENTORY: PASS
node   scripts/build_component_catalog.mjs --check       # CATALOG: PASS
node   scripts/check_demo_variants.mjs                   # DEMO_VARIANTS: PASS
node   scripts/build_demo_events.mjs --check             # DEMO_EVENTS: PASS
python scripts/check_contrast.py                         # CONTRAST: PASS
python scripts/build_motion_overrides.py --check         # MOTION_OVERRIDES: PASS
python scripts/check_motion_language.py                  # MOTION_LANGUAGE: PASS

# 渲染（需先起本地开发服务）
python scripts/_verify_keyboard.py                       # KEYBOARD_VERIFY: PASS
python scripts/_verify_crystallize.py                    # CRYSTALLIZE_VERIFY: PASS
python scripts/check_demo_health.py                      # DEMO_HEALTH: PASS（浅色）
python scripts/check_demo_health.py --theme dark         # DEMO_HEALTH: PASS（暗色）
python scripts/check_content_padding.py                  # CONTENT_PADDING: PASS
python scripts/check_demo_visibility.py                  # DEMO_VISIBILITY: PASS
python scripts/check_demo_guides.py                      # DEMO_GUIDES: PASS
python scripts/check_demo_event_wiring.py                # EVENT_WIRING: PASS
```

一次跑完全部守卫：`bash scripts/_sweep.sh`（约 10 分钟，末尾汇总失败项）。

## 6. 已知的坑

- 渲染类守卫的 Python 必须带 playwright 与 PIL（`C:/Python314/python.exe`），托管 Python 没这些包，会静默扫到空页。
- `check_demo_health.py` 默认只扫浅色，双主题要跑两遍。
- 生成物（`*.generated.ts`、`references/component-catalog.*`）禁止手改，改了下次 `--check` 必失配。
- 看到 `CATALOG: STALE` 别直接重新生成：先备份 → 重新生成 → 逐组件比 `fingerprint` 差异字段，确认是预期变更再落地。
