<script setup lang="ts">
/* 年份选择：一页 12 年（十年跨度加前后各一年的缓冲），头部显示跨度并整页翻。
   对外输出 YYYY 字符串。
   页首按 12 的倍数对齐，而不是从当前年往后铺 12 格：
   对齐后每页边界固定，翻回来还是同一批年份，用户建立的位置感不会被打乱。
   exemption: 年份分页、12 年布局与选后回写同属一个交互单元，拆开反而割裂可读性。 */
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
  placeholder: '请选择年份',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

/* 一页 12 格：中间十年是主区间，首尾各留一格当邻页提示 */
const PAGE = 12

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
/* 当前页的起始年，永远对齐到 PAGE 的整数倍 */
const pageStart = ref(Math.floor(new Date().getFullYear() / PAGE) * PAGE)

/** [参数] value YYYY 串 [返回] 年份数字，非法时 null */
function parse(value?: string): number | null {
  if (!value) return null
  const year = Number(value)
  /* 四位数且落在一个合理区间，避免把 '0000' 这类脏值当成年份 */
  return Number.isInteger(year) && year >= 1 && year <= 9999 ? year : null
}

/** [参数] step 页偏移 [返回] 无：整页前翻 / 后翻 */
function shiftPage(step: number) {
  pageStart.value += step * PAGE
}

const picked = computed(() => parse(props.modelValue))
const thisYear = new Date().getFullYear()

/** [返回] 触发器上的年份文案 */
const display = computed(() => (picked.value === null ? '' : String(picked.value)))

/** [返回] 页头跨度文案，如 2020 - 2031 */
const pageLabel = computed(() => `${pageStart.value} - ${pageStart.value + PAGE - 1}`)

/* 本页 12 个年份：不再过滤首尾，保持网格 12 格等宽，翻页时格子位置不跳动 */
const years = computed(() => Array.from({ length: PAGE }, (_, i) => pageStart.value + i))

/** [参数] year 年份 [返回] 该格的选中 / 今年状态类名 */
function cellClass(year: number): string[] {
  const cls: string[] = []
  if (picked.value === year) cls.push('is-selected')
  if (year === thisYear) cls.push('is-current')
  return cls
}

/** [参数] year 被点中的年份 [返回] 无 */
function pick(year: number) {
  emit('update:modelValue', String(year))
  hide(true)
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
  /* 打开时把页定位到已选年份所在页，否则每次都要从头翻 */
  pageStart.value = Math.floor((picked.value ?? new Date().getFullYear()) / PAGE) * PAGE
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
  <div class="x-yearpicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-year', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide(true) : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-year-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
      <span
        v-if="clearable && display && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else class="x-year-caret" name="chevronDown" :size="15" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-year-menu m-float"
          role="dialog"
          aria-label="年份选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-year-head">
            <button type="button" class="x-year-nav" aria-label="上一页" @click="shiftPage(-1)"><Icon name="chevronLeft" :size="15" /></button>
            <span class="x-year-title">{{ pageLabel }}</span>
            <button type="button" class="x-year-nav" aria-label="下一页" @click="shiftPage(1)"><Icon name="chevronRight" :size="15" /></button>
          </div>
          <div class="x-year-grid">
            <button
              v-for="y in years"
              :key="y"
              type="button"
              :class="['x-year-cell', cellClass(y)]"
              @click="pick(y)"
            >{{ y }}</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-yearpicker { display: inline-flex; width: 100%; }
.x-year { width: 100%; cursor: pointer; text-align: left; color: var(--ink); }
.x-year-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-year-value.is-placeholder { color: var(--ink-faint); }
.x-year-caret { color: var(--ink-soft); flex: none; }
.x-year-menu { position: fixed; z-index: 120; width: 272px; padding: 10px; border-radius: var(--r-md); }
.x-year-head { display: flex; align-items: center; justify-content: space-between; padding: 0 2px 8px; }
.x-year-title { font-size: 13px; font-weight: 620; color: var(--ink); font-variant-numeric: tabular-nums; }
.x-year-nav {
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
.x-year-nav:hover { background: var(--hover-bg); color: var(--ink); }
.x-year-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; }
.x-year-cell {
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
.x-year-cell:hover { background: var(--hover-bg); }
.x-year-cell.is-current { color: var(--blue); font-weight: 640; }
.x-year-cell.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 640; box-shadow: var(--e-accent); }
</style>
