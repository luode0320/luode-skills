<script setup lang="ts">
/* 周选择：列出 ISO 周（周一开头，第 1 周含当年首个周四），每行显示周序号与起止日期。
   对外输出 YYYY-Www 字符串，如 2026-W42。
   跨年月用「周所属的周四」定归属，而不是周一的年份，
   否则元旦落在周一之前的那些天会被错算到上一年，与后端周筛选口径对不上。
   exemption: ISO 周归属计算、列表渲染与定位事件同属一个交互单元，拆开反而割裂可读性。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
}>(), {
  placeholder: '请选择周',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
/* 面板展示的年份：只决定渲染哪一年的 52/53 行，不直接改已选值 */
const viewYear = ref(new Date().getFullYear())

/** [参数] date 任意日期 [返回] 当天 00:00 的副本：逐日比较必须丢掉时分秒 */
function atMidnight(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate())
}

/**
 * [参数] date 目标日期
 * [返回] 该日所属 ISO 周的周一
 * ISO 规定周从周一开始，于是把周日视作第 7 天再回退
 */
function mondayOf(date: Date): Date {
  const base = atMidnight(date)
  const day = base.getDay() || 7
  base.setDate(base.getDate() - day + 1)
  return base
}

/**
 * [参数] date 目标日期
 * [返回] ISO 周的年份与周序号
 * 用「周四归属法」：某周的周四落在哪一年，整个周就算那一年的
 */
function isoWeekOf(date: Date): { year: number; week: number } {
  const thursday = mondayOf(date)
  thursday.setDate(thursday.getDate() + 3)
  const year = thursday.getFullYear()
  const jan1 = new Date(year, 0, 1)
  /* 以首个周四为第 1 周，往前补齐的几天归上一年末周 */
  const firstThursday = mondayOf(jan1)
  firstThursday.setDate(firstThursday.getDate() + 3)
  const diff = thursday.getTime() - firstThursday.getTime()
  return { year, week: Math.round(diff / 604800000) + 1 }
}

/** [参数] year 年份 [返回] 该年 ISO 周总数（52 或 53） */
function weeksInYear(year: number): number {
  return isoWeekOf(new Date(year, 11, 28)).week
}

/** [参数] year 年，week ISO 周序号 [返回] YYYY-Www 串 */
function toIso(year: number, week: number): string {
  return `${year}-W${String(week).padStart(2, '0')}`
}

/** [参数] value YYYY-Www 串 [返回] 年份与周序号，非法时 null */
function parse(value?: string): { year: number; week: number } | null {
  if (!value) return null
  const match = /^(\d{4})-W(\d{2})$/.exec(value)
  if (!match) return null
  const year = Number(match[1])
  const week = Number(match[2])
  return week >= 1 && week <= weeksInYear(year) ? { year, week } : null
}

/** [参数] year 年，week 周序号 [返回] 该周的周一日期 */
function mondayOfWeek(year: number, week: number): Date {
  const day = mondayOf(new Date(year, 0, 4))
  day.setDate(day.getDate() + (week - 1) * 7)
  return day
}

/** [参数] date 日期 [返回] M/D 短格式，行内第二列只用来看位置 */
function short(date: Date): string {
  return `${date.getMonth() + 1}/${date.getDate()}`
}

const picked = computed(() => parse(props.modelValue))

/** [返回] 触发器上的周文案，附上起止日期让人一眼确认 */
const display = computed(() => {
  if (!picked.value) return ''
  const mon = mondayOfWeek(picked.value.year, picked.value.week)
  const sun = new Date(mon)
  sun.setDate(sun.getDate() + 6)
  return `${toIso(picked.value.year, picked.value.week)}（${short(mon)} ~ ${short(sun)}）`
})

/* 面板行：一年最多 53 个 ISO 周，少的年份只渲染实际存在的那几行 */
const rows = computed(() => Array.from({ length: weeksInYear(viewYear.value) }, (_, i) => {
  const week = i + 1
  const mon = mondayOfWeek(viewYear.value, week)
  const sun = new Date(mon)
  sun.setDate(sun.getDate() + 6)
  return { week, range: `${short(mon)} ~ ${short(sun)}` }
}))

/** [参数] week 周序号 [返回] 该行是否已选 */
function isSelected(week: number): boolean {
  return picked.value?.year === viewYear.value && picked.value.week === week
}

/** [参数] row 被点中的周 [返回] 无 */
function pick(row: { week: number }) {
  emit('update:modelValue', toIso(viewYear.value, row.week))
  hide(true)
}

/** [参数] step 年份偏移 [返回] 无 */
function shiftYear(step: number) {
  viewYear.value += step
}

/** [返回] 无：浮层贴触发器下方，空间不足翻上方 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 280
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  pos.value = { top, left: Math.max(8, Math.min(rect.left, window.innerWidth - 296)) }
}

/** [返回] 无 */
function bind() {
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/** [返回] 无 */
function unbind() {
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
}

/** [返回] 无 */
async function show() {
  if (props.disabled || open.value) return
  viewYear.value = picked.value?.year ?? isoWeekOf(new Date()).year
  open.value = true
  place()
  bind()
  await nextTick()
  place()
  /* 面板约 280px 高，选中行可能在下面：开面板后定位过去，省掉手动滚动 */
  menu.value?.querySelector('.is-selected')?.scrollIntoView({ block: 'nearest' })
}

/** [参数] refocus 关闭后是否把焦点还给触发器 [返回] 无 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  unbind()
  if (refocus) trigger.value?.focus()
}

/** [参数] event 指针事件 [返回] 无 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/** [返回] 无：清空值 */
function clear() {
  emit('update:modelValue', '')
  trigger.value?.focus()
}

/** [参数] event 键盘事件 [返回] 无：Esc 收起面板 */
function onKey(event: KeyboardEvent) {
  if (event.key !== 'Escape' || !open.value) return
  event.preventDefault()
  hide(true)
}

onBeforeUnmount(() => hide())
</script>

<template>
  <div class="x-weekpicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-week', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide(true) : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-week-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
      <span
        v-if="clearable && display && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else class="x-week-caret" name="chevronDown" :size="15" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-week-menu m-float"
          role="dialog"
          aria-label="周选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-week-head">
            <button type="button" class="x-week-nav" aria-label="上一年" @click="shiftYear(-1)"><Icon name="chevronLeft" :size="15" /></button>
            <span class="x-week-title">{{ viewYear }} 年</span>
            <button type="button" class="x-week-nav" aria-label="下一年" @click="shiftYear(1)"><Icon name="chevronRight" :size="15" /></button>
          </div>
          <ul class="x-week-list" role="listbox" aria-label="周列表">
            <li
              v-for="row in rows"
              :key="row.week"
              role="option"
              :aria-selected="isSelected(row.week)"
              :class="['x-week-row', isSelected(row.week) && 'is-selected']"
              @click="pick(row)"
            >
              <span class="x-week-no">W{{ String(row.week).padStart(2, '0') }}</span>
              <span class="x-week-range tnum">{{ row.range }}</span>
            </li>
          </ul>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-weekpicker { display: inline-flex; width: 100%; }
.x-week { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-week-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-week-value.is-placeholder { color: var(--ink-faint); }
.x-week-caret { color: var(--ink-soft); flex: none; }
.x-week-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-week-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-week-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-week-nav {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border: 0;
  border-radius: var(--r-xs);
  background: transparent;
  color: var(--ink-soft);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-week-nav:hover { background: var(--hover-bg); color: var(--ink); }
/* 一年 53 行超过面板高，滚动发生在列表自身，头部翻年按钮固定不动 */
.x-week-list {
  margin: 0;
  padding: 2px;
  max-height: 260px;
  list-style: none;
  overflow-y: auto;
  overscroll-behavior: contain;
  border-radius: var(--r-sm);
  background: var(--groove-bg);
  box-shadow: var(--groove-inset);
}
.x-week-row {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 28px;
  padding: 0 8px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink-muted);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-week-row:hover { background: var(--hover-bg); color: var(--ink); }
.x-week-no { flex: none; width: 34px; font-weight: 620; color: var(--ink); font-variant-numeric: tabular-nums; }
.x-week-range { flex: 1; min-width: 0; color: var(--ink-soft); }
.x-week-row.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 620; box-shadow: var(--e-accent); }
.x-week-row.is-selected .x-week-no,
.x-week-row.is-selected .x-week-range { color: var(--plate-ink); }
</style>
