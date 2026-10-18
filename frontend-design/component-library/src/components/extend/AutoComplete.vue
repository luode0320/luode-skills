<script setup lang="ts">
/* 自动补全：输入框敲字时在下方浮出匹配候选，上下键切换、回车落定。
   默认按 label 子串过滤，调用方可用 filter 换成任意匹配策略。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface AutoCompleteOption {
  label: string
  value: string
}

const props = withDefaults(defineProps<{
  modelValue?: string
  options: AutoCompleteOption[]
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
  filter?: (input: string, option: AutoCompleteOption) => boolean
}>(), {
  placeholder: '',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'select', value: string): void
}>()

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const input = ref<HTMLInputElement | null>(null)
const open = ref(false)
const activeIndex = ref(-1)
const pos = ref({ top: 0, left: 0, width: 0 })
const listId = `ac-${Math.random().toString(36).slice(2, 8)}`

/** [返回] 按当前输入过滤后的候选列表 */
const matched = computed(() => {
  const key = (props.modelValue ?? '').trim().toLowerCase()
  if (!key) return props.options
  const test = props.filter ?? ((text: string, option: AutoCompleteOption) => option.label.toLowerCase().includes(text))
  return props.options.filter(option => test(key, option))
})

/** [返回] 无 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 260
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  const width = Math.max(rect.width, 160)
  const left = Math.max(8, Math.min(rect.left, window.innerWidth - width - 8))
  pos.value = { top, left, width }
}

/** [返回] 无 */
function scrollActiveIntoView() {
  nextTick(() => menu.value?.querySelector('.x-ac-option.is-active')?.scrollIntoView({ block: 'nearest' }))
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
  open.value = true
  activeIndex.value = matched.value.length ? 0 : -1
  place()
  bind()
  await nextTick()
  place()
  scrollActiveIntoView()
}

/** [参数] refocus 关闭后是否把焦点还给输入框 [返回] 无 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  unbind()
  if (refocus) input.value?.focus()
}

/** [参数] option 被选中的候选 [返回] 无 */
function pick(option: AutoCompleteOption) {
  emit('update:modelValue', option.value)
  emit('select', option.value)
  hide(true)
}

/** [参数] event 指针事件 [返回] 无 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/** [参数] step 移动方向 [返回] 无 */
function move(step: number) {
  const list = matched.value
  if (!list.length) return
  activeIndex.value = (activeIndex.value + step + list.length) % list.length
  scrollActiveIntoView()
}

/** [参数] event 输入事件 [返回] 无 */
function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
  if (props.disabled) return
  if (!open.value) { openMenu(); return }
  activeIndex.value = matched.value.length ? 0 : -1
  nextTick(() => { place(); scrollActiveIntoView() })
}

/** [参数] event 键盘事件 [返回] 无 */
function onKey(event: KeyboardEvent) {
  if (!open.value) {
    if (event.key === 'ArrowDown') { event.preventDefault(); openMenu() }
    return
  }
  if (event.key === 'ArrowDown') { event.preventDefault(); move(1) }
  else if (event.key === 'ArrowUp') { event.preventDefault(); move(-1) }
  else if (event.key === 'Enter') {
    const option = matched.value[activeIndex.value]
    if (option) { event.preventDefault(); pick(option) }
  } else if (event.key === 'Escape') { event.preventDefault(); event.stopPropagation(); hide(true) }
  else if (event.key === 'Tab') hide(true)
}

/** [返回] 无 */
function clear() {
  emit('update:modelValue', '')
  input.value?.focus()
}

onBeforeUnmount(() => hide())
</script>

<template>
  <span ref="trigger" :class="['input-shell', 'x-ac', disabled && 'is-disabled']">
    <Icon name="search" :size="15" />
    <input
      ref="input"
      :value="modelValue ?? ''"
      :placeholder="placeholder"
      :disabled="disabled"
      role="combobox"
      aria-autocomplete="list"
      :aria-expanded="open"
      :aria-controls="listId"
      @input="onInput"
      @keydown="onKey"
      @click="openMenu"
    />
    <span
      v-if="clearable && modelValue && !disabled"
      class="input-clear"
      role="button"
      aria-label="清空"
      @click.stop="clear"
    ><Icon name="x" :size="14" /></span>
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-ac-menu m-float"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, width: `${pos.width}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div :id="listId" class="x-ac-list" role="listbox">
          <div
            v-for="(o, i) in matched"
            :key="o.value"
            role="option"
            :aria-selected="o.value === modelValue"
            :class="['x-ac-option', i === activeIndex && 'is-active', o.value === modelValue && 'is-selected']"
            @pointerenter="activeIndex = i"
            @mousedown.prevent
            @click="pick(o)"
          >
            <span class="x-ac-label">{{ o.label }}</span>
            <Icon v-if="o.value === modelValue" name="check" :size="14" />
          </div>
          <div v-if="!matched.length" class="x-ac-empty">无匹配项</div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-ac { width: 100%; }
.x-ac-menu {
  position: fixed;
  z-index: 120;
  min-width: 160px;
  max-height: 300px;
  display: flex;
  flex-direction: column;
  padding: 6px;
  border-radius: var(--r-md);
  overflow: hidden;
}
.x-ac-list { overflow-y: auto; overscroll-behavior: contain; }
.x-ac-option {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-ac-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-ac-option.is-active { background: var(--hover-bg); }
.x-ac-option.is-selected { color: var(--blue); font-weight: 620; }
.x-ac-empty { padding: 14px 10px; font-size: 12px; color: var(--ink-soft); text-align: center; }
</style>
