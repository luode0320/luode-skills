<script setup lang="ts">
/* 月份选择：一格一月共 12 格，头部只翻年不翻月，选完立即回写。
   对外输出 YYYY-MM 字符串；跨年选择靠点头部年份翻页，不做下拉年份列表，
   因为月份面板本身就够小，再叠一层列表会让视线在两处年份间来回跳。
   exemption: 翻年、12 格布局与选后回写同属一个交互单元，拆开反而割裂可读性。 */
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
  placeholder: '请选择月份',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const MONTHS = Array.from({ length: 12 }, (_, i) => i + 1)

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
/* 面板当前展示的年份，与已选值解耦：翻页浏览不该顺手改掉已选月份 */
const viewYear = ref(new Date().getFullYear())

/** [参数] value YYYY-MM 串 [返回] 拆出的年份与月份，非法时为 null */
function parse(value?: string): { year: number; month: number } | null {
  if (!value) return null
  const [y, m] = value.split('-').map(Number)
  if (!y || !m || m < 1 || m > 12) return null
  return { year: y, month: m }
}

/** [参数] year 年，month 月 [返回] 补零后的 YYYY-MM 串 */
function toIso(year: number, month: number): string {
  return `${year}-${String(month).padStart(2, '0')}`
}

/** [返回] 触发器上的月份文案 */
const display = computed(() => {
  const picked = parse(props.modelValue)
  return picked ? toIso(picked.year, picked.month) : ''
})

const picked = computed(() => parse(props.modelValue))
const thisYear = new Date().getFullYear()
const thisMonth = new Date().getMonth() + 1

/** [参数] month 月份数字 [返回] 该格的选中 / 当月状态类名 */
function cellClass(month: number): string[] {
  const cls: string[] = []
  if (picked.value?.year === viewYear.value && picked.value.month === month) cls.push('is-selected')
  /* 「今年本月」只在面板刚好翻到当年当月时才成立，否则会误导成已选 */
  if (viewYear.value === thisYear && month === thisMonth) cls.push('is-current')
  return cls
}

/** [参数] month 被点中的月份 [返回] 无 */
function pick(month: number) {
  emit('update:modelValue', toIso(viewYear.value, month))
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
  const height = menu.value?.offsetHeight ?? 200
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
  <div class="x-monthpicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-month', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide(true) : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-month-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
      <span
        v-if="clearable && display && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else class="x-month-caret" name="chevronDown" :size="15" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-month-menu m-float"
          role="dialog"
          aria-label="月份选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-month-head">
            <button type="button" class="x-month-nav" aria-label="上一年" @click="shiftYear(-1)"><Icon name="chevronLeft" :size="15" /></button>
            <span class="x-month-title">{{ viewYear }} 年</span>
            <button type="button" class="x-month-nav" aria-label="下一年" @click="shiftYear(1)"><Icon name="chevronRight" :size="15" /></button>
          </div>
          <div class="x-month-grid">
            <button
              v-for="m in MONTHS"
              :key="m"
              type="button"
              :class="['x-month-cell', cellClass(m)]"
              @click="pick(m)"
            >{{ m }} 月</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-monthpicker { display: inline-flex; width: 100%; }
.x-month { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-month-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-month-value.is-placeholder { color: var(--ink-faint); }
.x-month-caret { color: var(--ink-soft); flex: none; }
.x-month-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-month-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-month-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-month-nav {
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
.x-month-nav:hover { background: var(--hover-bg); color: var(--ink); }
.x-month-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.x-month-cell {
  height: 36px;
  border: 0;
  border-radius: var(--r-sm);
  background: transparent;
  color: var(--ink);
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-month-cell:hover { background: var(--hover-bg); }
.x-month-cell.is-current { color: var(--blue); font-weight: 640; }
.x-month-cell.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 640; box-shadow: var(--e-accent); }
</style>
