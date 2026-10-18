<script setup lang="ts">
/* 季度选择：一格一季共 4 格，头部只翻年。
   对外输出 YYYY-Qn 字符串，如 2026-Q4。
   季度区间按自然季度切（1-3 / 4-6 / 7-9 / 10-12），界面上把月份范围标出来，
   因为「Q3」到底是哪几个月，不同团队口径不一致，写出来才不会选错。
   exemption: 翻年、4 格布局与选后回写同属一个交互单元，拆开反而割裂可读性。 */
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
  placeholder: '请选择季度',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

/* 四个季度连同它们的月份区间一起声明，界面上直接展示，避免口头对齐口径 */
const QUARTERS = [
  { n: 1, months: '1-3 月' },
  { n: 2, months: '4-6 月' },
  { n: 3, months: '7-9 月' },
  { n: 4, months: '10-12 月' },
]

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
/* 面板展示的年份，与已选季度解耦：翻页浏览不该改掉已选值 */
const viewYear = ref(new Date().getFullYear())

/** [参数] value YYYY-Qn 串 [返回] 年份与季度号，非法时 null */
function parse(value?: string): { year: number; quarter: number } | null {
  if (!value) return null
  const match = /^(\d{4})-Q([1-4])$/.exec(value)
  return match ? { year: Number(match[1]), quarter: Number(match[2]) } : null
}

/** [参数] year 年，quarter 季度号 [返回] YYYY-Qn 串 */
function toIso(year: number, quarter: number): string {
  return `${year}-Q${quarter}`
}

const picked = computed(() => parse(props.modelValue))

/** [返回] 触发器上的季度文案 */
const display = computed(() => (picked.value ? toIso(picked.value.year, picked.value.quarter) : ''))

/* 当前季度：只在面板翻到今年时才参与高亮，否则会误导成已选 */
const now = new Date()
const thisYear = now.getFullYear()
const thisQuarter = Math.floor(now.getMonth() / 3) + 1

/** [参数] quarter 季度号 [返回] 该格的选中 / 当季状态类名 */
function cellClass(quarter: number): string[] {
  const cls: string[] = []
  if (picked.value?.year === viewYear.value && picked.value.quarter === quarter) cls.push('is-selected')
  if (viewYear.value === thisYear && quarter === thisQuarter) cls.push('is-current')
  return cls
}

/** [参数] quarter 被点中的季度 [返回] 无 */
function pick(quarter: number) {
  emit('update:modelValue', toIso(viewYear.value, quarter))
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
  const height = menu.value?.offsetHeight ?? 160
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
  viewYear.value = picked.value?.year ?? new Date().getFullYear()
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
  <div class="x-quarterpicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-quarter', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide(true) : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-quarter-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
      <span
        v-if="clearable && display && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else class="x-quarter-caret" name="chevronDown" :size="15" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-quarter-menu m-float"
          role="dialog"
          aria-label="季度选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-quarter-head">
            <button type="button" class="x-quarter-nav" aria-label="上一年" @click="shiftYear(-1)"><Icon name="chevronLeft" :size="15" /></button>
            <span class="x-quarter-title">{{ viewYear }} 年</span>
            <button type="button" class="x-quarter-nav" aria-label="下一年" @click="shiftYear(1)"><Icon name="chevronRight" :size="15" /></button>
          </div>
          <div class="x-quarter-grid">
            <button
              v-for="q in QUARTERS"
              :key="q.n"
              type="button"
              :class="['x-quarter-cell', cellClass(q.n)]"
              @click="pick(q.n)"
            >
              <span class="x-quarter-no">Q{{ q.n }}</span>
              <span class="x-quarter-months">{{ q.months }}</span>
            </button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-quarterpicker { display: inline-flex; width: 100%; }
.x-quarter { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-quarter-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-quarter-value.is-placeholder { color: var(--ink-faint); }
.x-quarter-caret { color: var(--ink-soft); flex: none; }
.x-quarter-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-quarter-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-quarter-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-quarter-nav {
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
.x-quarter-nav:hover { background: var(--hover-bg); color: var(--ink); }
.x-quarter-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; }
/* 季度格纵向叠两行文字，月份区间用弱色，选择时看的是 Q 号而不是月份 */
.x-quarter-cell {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
  padding: 8px 10px;
  border: 0;
  border-radius: var(--r-sm);
  background: transparent;
  color: var(--ink);
  text-align: left;
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-quarter-cell:hover { background: var(--hover-bg); }
.x-quarter-no { font-size: 13px; font-weight: 620; font-variant-numeric: tabular-nums; }
.x-quarter-months { font-size: 11px; color: var(--ink-faint); }
/* 当季降级到弱色而不是换成蓝系浅色：--blue-soft 是半透明底，当文字色会发虚看不清 */
.x-quarter-cell.is-current { color: var(--blue); }
.x-quarter-cell.is-current .x-quarter-months { color: var(--ink-soft); }
.x-quarter-cell.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 640; box-shadow: var(--e-accent); }
.x-quarter-cell.is-selected .x-quarter-months { color: var(--plate-ink); }
</style>
