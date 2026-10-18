<script setup lang="ts">
/* 级联选择：按层级逐列展开，每点一层同步回写路径，选到叶子即落定。
   面板随层数横向生长，列宽固定，超出视口宽度时横向滚动。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface CascaderOption {
  label: string
  value: string | number
  disabled?: boolean
  children?: CascaderOption[]
}

const props = withDefaults(defineProps<{
  modelValue?: Array<string | number>
  options: CascaderOption[]
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
}>(), {
  placeholder: '请选择',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: Array<string | number>): void }>()

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const draft = ref<Array<string | number>>([])
const pos = ref({ top: 0, left: 0 })

/** [返回] 按当前草稿路径展开的各级列数据 */
const columns = computed(() => {
  const cols: CascaderOption[][] = [props.options]
  let list = props.options
  for (const value of draft.value) {
    const node = list.find(o => o.value === value)
    if (!node?.children?.length) break
    cols.push(node.children)
    list = node.children
  }
  return cols
})

/** [返回] 已选路径的标签链 */
const labels = computed(() => {
  const out: string[] = []
  let list: CascaderOption[] | undefined = props.options
  for (const value of props.modelValue ?? []) {
    const node: CascaderOption | undefined = list?.find(o => o.value === value)
    if (!node) break
    out.push(node.label)
    list = node.children
  }
  return out
})

/** [返回] 无 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 300
  const width = menu.value?.offsetWidth ?? 152
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  const left = Math.max(8, Math.min(rect.left, window.innerWidth - width - 8))
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
  draft.value = [...(props.modelValue ?? [])]
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

/** [参数] option 被点中的节点 [参数] depth 所在列序号 [返回] 无 */
function pick(option: CascaderOption, depth: number) {
  if (option.disabled) return
  const next = draft.value.slice(0, depth)
  next.push(option.value)
  draft.value = next
  emit('update:modelValue', next)
  if (!option.children?.length) hide(true)
  else nextTick(place)
}

/** [返回] 无 */
function clear() {
  draft.value = []
  emit('update:modelValue', [])
  trigger.value?.focus()
}

onBeforeUnmount(() => hide())
</script>

<template>
  <button
    ref="trigger"
    type="button"
    :class="['input-shell', 'x-cas', disabled && 'is-disabled']"
    :disabled="disabled"
    role="combobox"
    aria-haspopup="listbox"
    :aria-expanded="open"
    @click="open ? hide(true) : openMenu()"
  >
    <span :class="['x-cas-value', !labels.length && 'is-placeholder']">{{ labels.length ? labels.join(' / ') : placeholder }}</span>
    <span
      v-if="clearable && labels.length && !disabled"
      class="input-clear"
      role="button"
      aria-label="清空"
      @click.stop="clear"
    ><Icon name="x" :size="14" /></span>
    <Icon v-else class="x-cas-caret" name="chevronDown" :size="15" />
  </button>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-cas-menu m-float"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div v-for="(col, depth) in columns" :key="depth" class="x-cas-col" role="listbox">
          <div
            v-for="o in col"
            :key="o.value"
            role="option"
            :aria-selected="draft[depth] === o.value"
            :aria-disabled="o.disabled || undefined"
            :class="['x-cas-option', draft[depth] === o.value && 'is-active', o.disabled && 'is-disabled']"
            @click="pick(o, depth)"
          >
            <span class="x-cas-label">{{ o.label }}</span>
            <Icon v-if="o.children?.length" name="chevronRight" :size="14" />
            <Icon v-else-if="draft[depth] === o.value" name="check" :size="14" />
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-cas { width: 100%; justify-content: space-between; text-align: left; cursor: pointer; color: var(--ink); }
.x-cas-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-cas-value.is-placeholder { color: var(--ink-faint); }
.x-cas-caret { color: var(--ink-soft); flex: none; transition: color .2s ease; }
.x-cas-menu {
  position: fixed;
  z-index: 120;
  display: flex;
  max-width: 70vw;
  padding: 6px;
  border-radius: var(--r-md);
  overflow-x: auto;
  overscroll-behavior: contain;
}
.x-cas-col { width: 152px; flex: none; max-height: 300px; overflow-y: auto; overscroll-behavior: contain; }
.x-cas-col:not(:first-child) { border-left: 1px solid var(--line); }
.x-cas-option {
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
.x-cas-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-cas-option.is-active { background: var(--hover-bg); color: var(--blue); font-weight: 620; }
.x-cas-option.is-disabled { color: var(--ink-faint); cursor: not-allowed; }
</style>
