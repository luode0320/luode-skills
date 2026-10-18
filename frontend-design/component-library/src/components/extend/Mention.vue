<script setup lang="ts">
/* 提及输入：textarea 里敲出 trigger（默认 @）即浮出候选，选中后把触发词替换成候选值。
   只在光标前最近一个触发符到光标之间没有空白时才算命中，避免误触发。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface MentionOption {
  value: string
  label: string
}

const props = withDefaults(defineProps<{
  modelValue?: string
  options: MentionOption[]
  trigger?: string
  placeholder?: string
  rows?: number
}>(), {
  trigger: '@',
  rows: 3,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const root = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const area = ref<HTMLTextAreaElement | null>(null)
const open = ref(false)
const activeIndex = ref(0)
const query = ref('')
const pos = ref({ top: 0, left: 0, width: 0 })
/* 触发符在文本中的下标，插入时据此定位替换区间 */
let triggerIndex = -1

/** [返回] 按 query 过滤后的候选 */
const matched = computed(() => {
  const key = query.value.trim().toLowerCase()
  if (!key) return props.options
  return props.options.filter(o => o.label.toLowerCase().includes(key) || o.value.toLowerCase().includes(key))
})

/** [返回] 无 */
function place() {
  const rect = root.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 220
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  pos.value = { top, left: rect.left, width: rect.width }
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
  open.value = true
  activeIndex.value = 0
  place()
  bind()
  await nextTick()
  place()
}

/** [返回] 无 */
function hide() {
  if (!open.value) return
  open.value = false
  triggerIndex = -1
  unbind()
}

/** [参数] event 指针事件 [返回] 无 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (root.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/** [参数] value 当前文本 [参数] caret 光标位置 [返回] 无 */
function detect(value: string, caret: number) {
  const head = value.slice(0, caret)
  const index = head.lastIndexOf(props.trigger)
  if (index < 0) { hide(); return }
  const segment = head.slice(index + props.trigger.length)
  if (/\s/.test(segment)) { hide(); return }
  triggerIndex = index
  query.value = segment
  if (!open.value) openMenu()
  else nextTick(place)
}

/** [参数] event 输入事件 [返回] 无 */
function onInput(event: Event) {
  const el = event.target as HTMLTextAreaElement
  emit('update:modelValue', el.value)
  detect(el.value, el.selectionStart ?? el.value.length)
}

/** [参数] event 键盘事件 [返回] 无 */
function onKey(event: KeyboardEvent) {
  if (!open.value) return
  const list = matched.value
  if (event.key === 'ArrowDown') { event.preventDefault(); if (list.length) activeIndex.value = (activeIndex.value + 1) % list.length }
  else if (event.key === 'ArrowUp') { event.preventDefault(); if (list.length) activeIndex.value = (activeIndex.value - 1 + list.length) % list.length }
  else if (event.key === 'Enter') {
    const option = list[activeIndex.value]
    if (!option) return
    event.preventDefault()
    insert(option)
  } else if (event.key === 'Escape') { event.preventDefault(); hide() }
}

/** [参数] option 被选中的候选 [返回] 无 */
function insert(option: MentionOption) {
  const el = area.value
  const value = props.modelValue ?? ''
  const caret = el?.selectionStart ?? value.length
  const head = value.slice(0, triggerIndex)
  const tail = value.slice(caret)
  const token = `${props.trigger}${option.value} `
  const next = `${head}${token}${tail}`
  emit('update:modelValue', next)
  hide()
  nextTick(() => {
    if (!el) return
    const at = head.length + token.length
    el.focus()
    el.setSelectionRange(at, at)
  })
}

onBeforeUnmount(() => hide())
</script>

<template>
  <div ref="root" class="x-mention">
    <span class="input-shell is-multiline x-mention-shell">
      <textarea
        ref="area"
        :value="modelValue ?? ''"
        :placeholder="placeholder"
        :rows="rows"
        @input="onInput"
        @keydown="onKey"
        @blur="hide"
      />
    </span>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="menu"
          class="x-mention-menu m-float"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, width: `${pos.width}px`, zIndex: floatingLayerFor(root) }"
        >
          <div role="listbox">
            <div
              v-for="(o, i) in matched"
              :key="o.value"
              role="option"
              :aria-selected="i === activeIndex"
              :class="['x-mention-option', i === activeIndex && 'is-active']"
              @pointerenter="activeIndex = i"
              @mousedown.prevent
              @click="insert(o)"
            >
              <span class="x-mention-label">{{ o.label }}</span>
              <span class="x-mention-value faint">{{ o.value }}</span>
            </div>
            <div v-if="!matched.length" class="x-mention-empty">无匹配项</div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-mention { position: relative; }
.x-mention-shell { width: 100%; }
.x-mention-menu {
  position: fixed;
  z-index: 120;
  min-width: 160px;
  max-height: 240px;
  overflow-y: auto;
  overscroll-behavior: contain;
  padding: 6px;
  border-radius: var(--r-md);
}
.x-mention-option {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 32px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  cursor: pointer;
  transition: background .15s ease;
}
.x-mention-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-mention-value { font-size: 11px; }
.x-mention-option.is-active { background: var(--hover-bg); }
.x-mention-empty { padding: 14px 10px; font-size: 12px; color: var(--ink-soft); text-align: center; }
</style>
