<script setup lang="ts">
/* 日期区间选择：单个月历网格里两步连选，先点开始再点结束。
   联网需一次同时看两端，所以不做双月联动，避免调用方还要处理翻月同步。
   对外输出 [开始, 结束] 两个 YYYY-MM-DD 串，未选全时结束位为空串。
   exemption: 两步连选、区间高亮、定位与事件绑定同属一个交互单元，拆开反而割裂可读性。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  modelValue?: [string, string]
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
  format?: string
}>(), {
  placeholder: '请选择日期区间',
  format: 'YYYY-MM-DD',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: [string, string]): void }>()

const WEEK = ['日', '一', '二', '三', '四', '五', '六']

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
const view = ref(new Date())
/* 已经点了开始但还没点结束：此时 is-picking 为真，月历高亮只跟到指针 */
const pendingStart = ref<string | null>(null)
const hover = ref<string | null>(null)

/** [参数] date 目标日期 [返回] YYYY-MM-DD 字符串 */
function toIso(date: Date): string {
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}-${m}-${d}`
}

/** [参数] value YYYY-MM-DD 串 [返回] 对应 Date，非法时 null */
function parse(value?: string): Date | null {
  if (!value) return null
  const [y, m, d] = value.split('-').map(Number)
  if (!y || !m || !d) return null
  const date = new Date(y, m - 1, d)
  return Number.isNaN(date.getTime()) ? null : date
}

const today = new Date()

/* 区间两端：start 缺省时整段无效，结束位允许暂空 */
const start = computed(() => parse(props.modelValue?.[0])?.getTime() ?? null)
const end = computed(() => parse(props.modelValue?.[1])?.getTime() ?? null)
/* 首尾顺序交给 min/max：用户先点后一天再点前一天也算合法区间，不必额外交换 */
const lo = computed(() => (start.value === null || end.value === null ? null : Math.min(start.value, end.value)))
const hi = computed(() => (start.value === null || end.value === null ? null : Math.max(start.value, end.value)))
const picking = computed(() => pendingStart.value !== null)

/** [返回] 触发器上显示的区间文案 */
const display = computed(() => {
  const a = parse(props.modelValue?.[0])
  const b = parse(props.modelValue?.[1])
  if (!a) return ''
  return b ? `${fmt(a)} ~ ${fmt(b)}` : fmt(a)
})

/** [参数] date 日期 [返回] 按 format 拼出的显示串，仅供触发器用 */
function fmt(date: Date): string {
  const map: Record<string, string> = {
    YYYY: String(date.getFullYear()),
    MM: String(date.getMonth() + 1).padStart(2, '0'),
    DD: String(date.getDate()).padStart(2, '0'),
  }
  return props.format.replace(/YYYY|MM|DD/g, token => map[token] ?? token)
}

/** [返回] 当前月的 6×7 网格，非本月单元格为 null */
const cells = computed(() => {
  const year = view.value.getFullYear()
  const month = view.value.getMonth()
  const days = new Date(year, month + 1, 0).getDate()
  const out: Array<Date | null> = []
  for (let i = 0; i < new Date(year, month, 1).getDay(); i += 1) out.push(null)
  for (let d = 1; d <= days; d += 1) out.push(new Date(year, month, d))
  while (out.length % 7 !== 0) out.push(null)
  return out
})

/** [参数] date 单元格日期 [返回] 该格的状态类名数组 */
function cellClass(date: Date | null): string[] {
  if (!date) return []
  const t = date.getTime()
  const iso = toIso(date)
  const cls: string[] = []
  if (iso === toIso(today)) cls.push('is-today')
  if (lo.value !== null && hi.value !== null && t >= lo.value && t <= hi.value) cls.push('is-in-range')
  if (t === lo.value) cls.push('is-range-start')
  if (t === hi.value) cls.push('is-range-end')
  /* 选完第一个端点后，后续悬停预览的区间也先垫上底色，让人看到将要选的形状 */
  if (picking.value) {
    const a = parse(pendingStart.value || undefined)?.getTime()
    const b = parse(hover.value || undefined)?.getTime()
    if (a !== undefined && b !== undefined && t >= Math.min(a, b) && t <= Math.max(a, b)) cls.push('is-in-range')
    if (t === a) cls.push('is-range-start')
  }
  return cls
}

/** [参数] date 被点中的日期 [返回] 无 */
function pick(date: Date) {
  const iso = toIso(date)
  /* 第一击只记下起点，第二击才提交，避免半成品区间流到父组件 */
  if (!picking.value) {
    pendingStart.value = iso
    emit('update:modelValue', [iso, ''])
    return
  }
  const a = pendingStart.value as string
  pendingStart.value = null
  hover.value = null
  emit('update:modelValue', a <= iso ? [a, iso] : [iso, a])
  hide(true)
}

/** [参数] date 指针所在日期 [返回] 无 */
function preview(date: Date | null) {
  if (picking.value) hover.value = date ? toIso(date) : null
}

/** [参数] step 月份偏移 [返回] 无 */
function shiftMonth(step: number) {
  view.value = new Date(view.value.getFullYear(), view.value.getMonth() + step, 1)
}

/** [返回] 无：把浮层贴到触发器下方，空间不足翻上方 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 320
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
  const a = parse(props.modelValue?.[0]) ?? new Date()
  view.value = a
  open.value = true
  place()
  bind()
  await nextTick()
  place()
}

/** [参数] refocus 关闭后是否把焦点还给触发器 [返回] 无 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  pendingStart.value = null
  hover.value = null
  unbind()
  if (refocus) trigger.value?.focus()
}

/** [参数] event 指针事件 [返回] 无 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/** [返回] 无：清空整段区间 */
function clear() {
  pendingStart.value = null
  emit('update:modelValue', ['', ''])
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
  <div class="x-rangepicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-range', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide(true) : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-range-value', !display && 'is-placeholder']">{{ display || (picking ? '请选择结束日期' : placeholder) }}</span>
      <span
        v-if="clearable && display && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else class="x-range-caret" name="chevronDown" :size="15" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-range-menu m-float"
          role="dialog"
          aria-label="日期区间选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-range-head">
            <button type="button" class="x-range-nav" aria-label="上一月" @click="shiftMonth(-1)"><Icon name="chevronLeft" :size="15" /></button>
            <span class="x-range-title">{{ view.getFullYear() }} 年 {{ view.getMonth() + 1 }} 月</span>
            <button type="button" class="x-range-nav" aria-label="下一月" @click="shiftMonth(1)"><Icon name="chevronRight" :size="15" /></button>
          </div>
          <div class="x-range-week">
            <span v-for="w in WEEK" :key="w">{{ w }}</span>
          </div>
          <div class="x-range-grid" @mouseleave="preview(null)">
            <button
              v-for="(cell, i) in cells"
              :key="i"
              type="button"
              :disabled="!cell"
              :class="['x-range-cell', cellClass(cell)]"
              @click="cell && pick(cell)"
              @mouseenter="preview(cell)"
            >{{ cell ? cell.getDate() : '' }}</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-rangepicker { display: inline-flex; width: 100%; }
.x-range { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-range-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-range-value.is-placeholder { color: var(--ink-faint); }
.x-range-caret { color: var(--ink-soft); flex: none; }
.x-range-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-range-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-range-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-range-nav {
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
.x-range-nav:hover { background: var(--hover-bg); color: var(--ink); }
.x-range-week { display: grid; grid-template-columns: repeat(7, 1fr); padding-bottom: 4px; }
.x-range-week span { text-align: center; font-size: 11px; color: var(--ink-faint); }
.x-range-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
/* 区间底色用方角，端点再单独圆角：连续日期才拼得成一条不断开的带子 */
.x-range-cell {
  height: 32px;
  border: 0;
  border-radius: 0;
  background: transparent;
  color: var(--ink);
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-range-cell:hover:not(:disabled) { background: var(--hover-bg); }
.x-range-cell:disabled { cursor: default; }
.x-range-cell.is-in-range { background: var(--blue-soft); color: var(--ink); }
.x-range-cell.is-today { color: var(--blue); font-weight: 640; }
.x-range-cell.is-range-start,
.x-range-cell.is-range-end {
  position: relative;
  z-index: 1;
  border-radius: var(--r-xs);
  background: var(--blue);
  color: var(--plate-ink);
  font-weight: 640;
  box-shadow: var(--e-accent);
}
</style>
