<script setup lang="ts">
/* 日期选择：用原生 Date 自绘月历网格，支持上下月切换、选日、今天与选中高亮。
   对外输出 YYYY-MM-DD 字符串；format 仅用于触发器上的显示文案。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
  format?: string
}>(), {
  placeholder: '请选择日期',
  format: 'YYYY-MM-DD',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const WEEK = ['日', '一', '二', '三', '四', '五', '六']

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
/* 视图所在月份：只关心年月，日固定为 1 */
const view = ref(new Date())

/** [参数] date 目标日期 [返回] YYYY-MM-DD 字符串 */
function toIso(date: Date): string {
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${date.getFullYear()}-${m}-${d}`
}

/** [参数] value YYYY-MM-DD 串 [返回] 对应 Date，非法时返回 null */
function parse(value?: string): Date | null {
  if (!value) return null
  const [y, m, d] = value.split('-').map(Number)
  if (!y || !m || !d) return null
  const date = new Date(y, m - 1, d)
  return Number.isNaN(date.getTime()) ? null : date
}

const today = new Date()

/** [返回] 触发器上显示的日期文案 */
const display = computed(() => {
  const date = parse(props.modelValue)
  if (!date) return ''
  const map: Record<string, string> = {
    YYYY: String(date.getFullYear()),
    MM: String(date.getMonth() + 1).padStart(2, '0'),
    DD: String(date.getDate()).padStart(2, '0'),
  }
  return props.format.replace(/YYYY|MM|DD/g, token => map[token] ?? token)
})

/** [返回] 当前月的 6×7 日期网格，非本月单元格为 null */
const cells = computed(() => {
  const year = view.value.getFullYear()
  const month = view.value.getMonth()
  const first = new Date(year, month, 1)
  const start = first.getDay()
  const days = new Date(year, month + 1, 0).getDate()
  const out: Array<Date | null> = []
  for (let i = 0; i < start; i += 1) out.push(null)
  for (let d = 1; d <= days; d += 1) out.push(new Date(year, month, d))
  while (out.length % 7 !== 0) out.push(null)
  return out
})

/** [参数] step 月份偏移，-1 上月 / 1 下月 [返回] 无 */
function shiftMonth(step: number) {
  view.value = new Date(view.value.getFullYear(), view.value.getMonth() + step, 1)
}

/** [参数] date 被点中的日期 [返回] 无 */
function pick(date: Date) {
  emit('update:modelValue', toIso(date))
  hide(true)
}

/** [返回] 无 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 320
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  const left = Math.max(8, Math.min(rect.left, window.innerWidth - 296))
  pos.value = { top, left }
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
async function openMenu() {
  if (props.disabled || open.value) return
  view.value = parse(props.modelValue) ?? new Date()
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

/** [返回] 无 */
function clear() {
  emit('update:modelValue', '')
  trigger.value?.focus()
}

onBeforeUnmount(() => hide())
</script>

<template>
  <button
    ref="trigger"
    type="button"
    :class="['input-shell', 'x-date', disabled && 'is-disabled']"
    :disabled="disabled"
    aria-haspopup="dialog"
    :aria-expanded="open"
    @click="open ? hide(true) : openMenu()"
  >
    <Icon name="clock" :size="15" />
    <span :class="['x-date-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
    <span
      v-if="clearable && display && !disabled"
      class="input-clear"
      role="button"
      aria-label="清空"
      @click.stop="clear"
    ><Icon name="x" :size="14" /></span>
    <Icon v-else class="x-date-caret" name="chevronDown" :size="15" />
  </button>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-date-menu m-float"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div class="x-date-head">
          <button type="button" class="x-date-nav" aria-label="上一月" @click="shiftMonth(-1)"><Icon name="chevronLeft" :size="15" /></button>
          <span class="x-date-title">{{ view.getFullYear() }} 年 {{ view.getMonth() + 1 }} 月</span>
          <button type="button" class="x-date-nav" aria-label="下一月" @click="shiftMonth(1)"><Icon name="chevronRight" :size="15" /></button>
        </div>
        <div class="x-date-week">
          <span v-for="w in WEEK" :key="w">{{ w }}</span>
        </div>
        <div class="x-date-grid">
          <button
            v-for="(cell, i) in cells"
            :key="i"
            type="button"
            :disabled="!cell"
            :class="[
              'x-date-cell',
              cell && toIso(cell) === modelValue && 'is-selected',
              cell && toIso(cell) === toIso(today) && 'is-today',
            ]"
            @click="cell && pick(cell)"
          >{{ cell ? cell.getDate() : '' }}</button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-date { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-date-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-date-value.is-placeholder { color: var(--ink-faint); }
.x-date-caret { color: var(--ink-soft); flex: none; }
.x-date-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-date-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-date-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-date-nav {
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
.x-date-nav:hover { background: var(--hover-bg); color: var(--ink); }
.x-date-week { display: grid; grid-template-columns: repeat(7, 1fr); padding-bottom: 4px; }
.x-date-week span { text-align: center; font-size: 11px; color: var(--ink-faint); }
.x-date-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 2px; }
.x-date-cell {
  height: 32px;
  border: 0;
  border-radius: var(--r-xs);
  background: transparent;
  color: var(--ink);
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-date-cell:hover:not(:disabled) { background: var(--hover-bg); }
.x-date-cell:disabled { cursor: default; }
.x-date-cell.is-today { color: var(--blue); font-weight: 640; }
.x-date-cell.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 640; box-shadow: var(--e-accent); }
</style>
