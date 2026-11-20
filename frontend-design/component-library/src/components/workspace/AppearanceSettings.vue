<script setup lang="ts">
import Icon from '@/components/Icon.vue'
import Segmented from '@/components/ui/Segmented.vue'
import { appearance, type Density, type ThemeMode } from '@/composables/appearance'
import { appearanceExt, type FontScale } from '@/composables/appearance-ext'
import { ACCENT_PALETTES } from '@/data/accent-palettes.generated'

/* 外观设置的正文：把四个正交维度放进同一个面板。

   为什么做成「正文组件」而不是独立弹窗：上游 `AppearanceDialog.vue` 是逐字节冻结文件，
   内部无法扩展；而把主色与字号单独做成第二个弹窗，用户会在「外观设置」里找不到字号
   （这正是本轮要修的问题）。所以这里只出正文，由对话框通过登记缝隙挂载，
   对外仍然是同一个「外观设置」，用户不需要知道它在哪一层实现。

   四个维度互不耦合：
   - 主题（明暗）与表格密度绑在 `:root`，只能全局生效；
   - 主色与字号用不绑 `:root` 的选择器，打在任意容器上只影响该子树。
   面板把它们并列展示，但语义差异写在下方的说明文字里。

   `sections` 让宿主按需裁剪：业务系统自己的设置页往往只放其中两项
   （例如「字号 + 主色」放进通用偏好，「主题 + 密度」留在顶栏菜单），
   整块塞进去反而会把不归这个页面管的东西也带出来。 */

export type AppearanceSection = 'theme' | 'accent' | 'fontScale' | 'density'

const props = withDefaults(defineProps<{
  /** 要显示的维度，缺省四项全显示；只做过滤，不改各自位置 */
  sections?: AppearanceSection[]
}>(), {
  // `defineProps` 会被提升到 setup 之外，默认值必须是自包含字面量，
  // 引用同文件里的常量会在编译期直接报错（整个画廊 500）。
  sections: () => ['theme', 'accent', 'fontScale', 'density'],
})

const shown = (key: AppearanceSection) => props.sections.includes(key)

/* 两组「单选」控件（主题卡、主色点）补方向键：分段控件 Segmented 自带 roving tabindex，
   这两组是同语义的 radiogroup，若只支持 Tab + Enter 就和库内其余单选控件不一致，
   键盘用户得逐个 Tab 过去才能换一个值。按原生 radio 的约定，方向键同时移动焦点并选中。 */
function onRadioKey<T>(list: readonly T[], current: number, event: KeyboardEvent, apply: (value: T) => void) {
  const forward = event.key === 'ArrowRight' || event.key === 'ArrowDown'
  const backward = event.key === 'ArrowLeft' || event.key === 'ArrowUp'
  if (!forward && !backward) return
  event.preventDefault()
  const next = (current + (forward ? 1 : -1) + list.length) % list.length
  apply(list[next])
  const group = (event.currentTarget as HTMLElement).parentElement
  ;(group?.children[next] as HTMLElement | undefined)?.focus()
}

const themeIndex = () => themes.findIndex(t => t.value === appearance.theme)
const accentIndex = () => ACCENT_PALETTES.findIndex(p => p.key === appearanceExt.accent)

const themes: Array<{ label: string; value: ThemeMode; icon: string }> = [
  { label: '浅色', value: 'light', icon: 'sun' },
  { label: '深色', value: 'dark', icon: 'moon' },
  { label: '跟随系统', value: 'auto', icon: 'monitor' },
]
const fontScales: Array<{ label: string; value: FontScale }> = [
  { label: '紧凑', value: 'compact' },
  { label: '标准', value: 'regular' },
  { label: '宽松', value: 'large' },
]

const densities: Array<{ label: string; value: Density }> = [
  { label: '宽松', value: 'comfy' },
  { label: '标准', value: 'regular' },
  { label: '紧凑', value: 'compact' },
]

/* 档位对应的真实像素，来源是 `build_font_overrides.py` 生成的三组令牌。
   面板上直接标出数值：只写「紧凑 / 标准 / 宽松」，用户无从判断到底多大，
   而这套系统最容易被抱怨的恰恰就是「字太小」。 */
const SCALE_PX: Record<FontScale, { body: number; caption: number }> = {
  compact: { body: 13, caption: 12 },
  regular: { body: 14, caption: 12 },
  large: { body: 15, caption: 13 },
}
</script>

<template>
  <div class="apx">
    <section v-if="shown('theme')" class="apx-block">
      <div class="apx-label">主题</div>
      <p class="apx-desc">跟随系统时按操作系统的浅色 / 深色自动切换</p>
      <div class="apx-themes" role="radiogroup" aria-label="主题">
        <button
          v-for="t in themes"
          :key="t.value"
          type="button"
          role="radio"
          :aria-checked="appearance.theme === t.value"
          :aria-label="`主题：${t.label}`"
          :tabindex="appearance.theme === t.value ? 0 : -1"
          :class="['apx-theme', `is-${t.value}`, { 'is-on': appearance.theme === t.value }]"
          @click="appearance.theme = t.value"
          @keydown="onRadioKey(themes, themeIndex(), $event, (v) => (appearance.theme = v.value))"
        >
          <span class="apx-shot" aria-hidden="true">
            <span class="apx-shot-bar" />
            <span class="apx-shot-line is-1" />
            <span class="apx-shot-line is-2" />
          </span>
          <span class="apx-theme-name">
            <Icon :name="t.icon" :size="14" />
            <span>{{ t.label }}</span>
          </span>
          <span v-if="appearance.theme === t.value" class="apx-check" aria-hidden="true">
            <Icon name="check" :size="10" :stroke="3" />
          </span>
        </button>
      </div>
    </section>

    <section v-if="shown('accent')" class="apx-row">
      <div class="apx-text">
        <div class="apx-label">主色</div>
        <p class="apx-desc">影响主操作、选中态与图表强调色</p>
      </div>
      <div class="apx-dots" role="radiogroup" aria-label="主色">
        <!-- 色点自身挂 data-accent：色块用 var(--blue) 取色，深浅两套值自动跟随当前主题，
             不需要在这里判断主题，也不需要复制一份色值。 -->
        <button
          v-for="p in ACCENT_PALETTES"
          :key="p.key"
          type="button"
          role="radio"
          :aria-checked="appearanceExt.accent === p.key"
          :aria-label="`主色：${p.label}`"
          :tabindex="appearanceExt.accent === p.key ? 0 : -1"
          :data-accent="p.key"
          :class="['apx-dot', { 'is-on': appearanceExt.accent === p.key }]"
          @click="appearanceExt.accent = p.key"
          @keydown="onRadioKey(ACCENT_PALETTES, accentIndex(), $event, (v) => (appearanceExt.accent = v.key))"
        >
          <span class="apx-dot-fill" aria-hidden="true" />
        </button>
      </div>
    </section>

    <section v-if="shown('fontScale')" class="apx-row is-stack">
      <div class="apx-row-top">
        <div class="apx-text">
          <div class="apx-label">字号</div>
          <p class="apx-desc">整体文字与控件尺寸，最小 12px</p>
        </div>
        <Segmented v-model="appearanceExt.fontScale" :options="fontScales" label="字号" />
      </div>
      <div class="apx-sample">
        <span class="apx-sample-main">Aa 正文示例 · 保存并提交</span>
        <span class="apx-sample-meta">辅助说明</span>
        <span class="apx-sample-px">{{ SCALE_PX[appearanceExt.fontScale].body }} / {{ SCALE_PX[appearanceExt.fontScale].caption }}px</span>
      </div>
    </section>

    <section v-if="shown('density')" class="apx-row">
      <div class="apx-text">
        <div class="apx-label">表格密度</div>
        <p class="apx-desc">影响所有列表的行高</p>
      </div>
      <Segmented v-model="appearance.density" :options="densities" label="表格密度" />
    </section>
  </div>
</template>

<style scoped>
.apx {
  display: flex;
  flex-direction: column;
}

/* 分区之间用同一条分隔线，和面板外的表单行保持一致的节奏 */
.apx > * + * {
  border-top: 1px solid var(--line);
}

.apx-block,
.apx-row {
  padding: 14px 0;
}

.apx-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

/* 字号行要放下「说明 + 分段控件 + 实时示例」，横排会挤，改为上下两段 */
.apx-row.is-stack {
  display: block;
}

.apx-row-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
}

.apx-text {
  min-width: 0;
}

.apx-label {
  font-size: var(--fs-body);
  font-weight: 640;
  color: var(--ink);
}

.apx-desc {
  margin: 2px 0 0;
  font-size: var(--fs-sm);
  color: var(--ink-soft);
}

/* ── 主题：三张预览卡 ─────────────────────────────────────────
   原来是三个纯文字分段项，塞不下只能换行，既没有层级也看不出选的是什么。
   改成带缩略图的卡片：一眼能看见「选了之后长什么样」，也是设置面板的通行做法。 */
.apx-themes {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
  margin-top: 10px;
}

.apx-theme {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 7px;
  padding: 6px 6px 7px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  background: transparent;
  cursor: pointer;
  transition: border-color .16s var(--ease-reveal), background .16s var(--ease-reveal), box-shadow .16s var(--ease-reveal);
}

.apx-theme:hover {
  border-color: var(--line-strong);
  background: var(--canvas);
}

.apx-theme.is-on {
  border-color: var(--blue);
  background: var(--canvas);
  box-shadow: inset 0 0 0 1px var(--blue), var(--e1);
}

.apx-theme:focus-visible,
.apx-dot:focus-visible {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
}

/* 缩略图里必须写真实色值：浅色卡在深色主题下也要显示成浅色，
   用令牌会跟着当前主题一起反色，预览就失去意义。 */
.apx-shot {
  display: flex;
  flex-direction: column;
  gap: 4px;
  height: 46px;
  padding: 5px;
  border-radius: var(--r-sm);
  overflow: hidden;
  box-shadow: inset 0 0 0 1px rgba(125, 133, 135, .3);
}

.apx-shot-bar,
.apx-shot-line {
  display: block;
  border-radius: 2px;
}

.apx-shot-bar { height: 8px; }
.apx-shot-line { height: 4px; }
.apx-shot-line.is-1 { width: 72%; }
.apx-shot-line.is-2 { width: 44%; }

/* 缩略图内部的对比刻意拉开：一开始按真实界面比例取色，深色卡在深色主题下
   几乎看不出结构，三张卡变成两个黑块加一个白块，预览就白做了。 */
.is-light .apx-shot { background: #ffffff; }
.is-light .apx-shot-bar { background: #d7dedd; }
.is-light .apx-shot-line { background: #c7d0cf; }

.is-dark .apx-shot { background: #0f1213; }
.is-dark .apx-shot-bar { background: #333d3f; }
.is-dark .apx-shot-line { background: #414c4e; }

/* 跟随系统：对角切开，明暗各占一半，比加一行说明文字更直观 */
.is-auto .apx-shot {
  background: linear-gradient(135deg, #ffffff 0 50%, #0f1213 50% 100%);
}
.is-auto .apx-shot-bar { background: rgba(122, 132, 134, .55); }
.is-auto .apx-shot-line { background: rgba(122, 132, 134, .45); }

.apx-theme-name {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: var(--fs-sm);
  font-weight: 600;
  color: var(--ink-soft);
  transition: color .16s var(--ease-reveal);
}

.apx-theme.is-on .apx-theme-name { color: var(--ink); }

/* 选中角标压在卡片右上角，跨出边框 6px，避免压住缩略图 */
.apx-check {
  position: absolute;
  top: -6px;
  right: -6px;
  display: grid;
  place-items: center;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--blue-solid);
  color: #fff;
  box-shadow: var(--e1);
}

/* ── 主色 ──────────────────────────────────────────────────── */
.apx-dots {
  display: flex;
  align-items: center;
  gap: 6px;
  flex: none;
}

.apx-dot {
  display: grid;
  place-items: center;
  width: 26px;
  height: 26px;
  padding: 0;
  border: 0;
  border-radius: 50%;
  background: transparent;
  cursor: pointer;
}

.apx-dot-fill {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  background: var(--blue);
  box-shadow: inset 0 0 0 1px rgba(0, 0, 0, .08);
  transition: transform .16s var(--ease-glide), box-shadow .16s var(--ease-reveal);
}

.apx-dot:hover .apx-dot-fill { transform: scale(1.08); }

/* 选中环用该色板自己的 --blue：外圈是色板色，内圈留一道底色缝，
   五种颜色都不会糊在一起 */
.apx-dot.is-on .apx-dot-fill {
  box-shadow: 0 0 0 2px var(--surface-solid), 0 0 0 3px var(--blue), inset 0 0 0 1px rgba(0, 0, 0, .08);
}

/* ── 字号示例 ──────────────────────────────────────────────── */
.apx-sample {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-top: 10px;
  padding: 9px 12px;
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  background: var(--canvas);
}

.apx-sample-main {
  font-size: var(--fs-body);
  color: var(--ink);
}

.apx-sample-meta {
  font-size: var(--fs-caption);
  color: var(--ink-soft);
}

.apx-sample-px {
  margin-left: auto;
  font-size: var(--fs-caption);
  color: var(--ink-soft);
  font-variant-numeric: tabular-nums;
}
</style>
