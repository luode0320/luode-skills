<script setup lang="ts">
/* 标签页：横向切换一组视图，line 型用滑动下划线、card 型用底色切换。
   标签头由本组件渲染，内容区交给 default 插槽配 TabPane，选中态与关闭都由调用方数据驱动。 */
import { nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { slideThumb } from '@/composables/motion'

export interface TabItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
  /** 该项是否可关闭，全局 closable 打开时再按此项单独收口 */
  closable?: boolean
}

const props = withDefaults(defineProps<{
  modelValue: string
  items: TabItem[]
  type?: 'line' | 'card'
  /** 全局开启关闭按钮，可被单项 closable: false 覆盖 */
  closable?: boolean
}>(), {
  type: 'line',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'close', key: string): void
}>()

const root = ref<HTMLElement | null>(null)
const thumb = ref<HTMLElement | null>(null)
let observer: ResizeObserver | null = null

/** [参数] 无 [返回] 当前选中项对应的标签按钮，找不到时返回 null */
function activeTab(): HTMLElement | null {
  const index = props.items.findIndex(item => item.key === props.modelValue)
  return root.value?.querySelectorAll<HTMLElement>('.x-tabs-tab')[index] ?? null
}

/** [参数] instant 是否跳过补间直接落位 [返回] 无；line 型同步下划线位置，card 型不参与 */
function sync(instant = false) {
  if (props.type !== 'line') return
  slideThumb(thumb.value, activeTab(), 'x', instant)
}

/** [参数] item 被点的标签 [返回] 无；禁用项不响应，正常项上抛选中 key */
function pick(item: TabItem) {
  if (item.disabled) return
  emit('update:modelValue', item.key)
}

/** [参数] key 被关的标签 [返回] 无；关闭与选中解耦，仅上抛关闭意图 */
function close(key: string) {
  emit('close', key)
}

/** [参数] item 标签数据 [返回] 该项是否显示关闭按钮 */
function canClose(item: TabItem) {
  return Boolean(props.closable) && item.closable !== false
}

/** [参数] event 键盘事件 [返回] 无；左右键在可选标签间移动并同步选中 */
function onKey(event: KeyboardEvent) {
  const step = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0
  if (!step) return
  event.preventDefault()
  const list = props.items
  if (!list.length) return
  let index = list.findIndex(item => item.key === props.modelValue)
  for (let i = 0; i < list.length; i += 1) {
    index = (index + step + list.length) % list.length
    if (!list[index].disabled) break
  }
  emit('update:modelValue', list[index].key)
  nextTick(() => activeTab()?.focus())
}

/** [参数] 无 [返回] 无；标签或容器尺寸变化都重新对位下划线 */
function observeAll() {
  observer?.disconnect()
  if (!root.value || !observer) return
  observer.observe(root.value)
  root.value.querySelectorAll('.x-tabs-tab').forEach(tab => observer!.observe(tab))
}

onMounted(() => {
  nextTick(() => sync(true))
  observer = new ResizeObserver(() => sync(true))
  observeAll()
})
onBeforeUnmount(() => observer?.disconnect())
watch(() => props.modelValue, () => nextTick(() => sync()))
watch(() => props.items.map(item => item.label).join('\u0000'), () => nextTick(() => { observeAll(); sync(true) }))
</script>

<template>
  <div class="x-tabs-wrap">
    <div
      ref="root"
      :class="['x-tabs', `is-${type}`]"
      role="tablist"
      @keydown="onKey"
    >
      <span v-if="type === 'line'" ref="thumb" class="x-tabs-thumb" aria-hidden="true" />
      <button
        v-for="item in items"
        :key="item.key"
        type="button"
        role="tab"
        :class="['x-tabs-tab', item.key === modelValue && 'is-active']"
        :aria-selected="item.key === modelValue"
        :tabindex="item.key === modelValue ? 0 : -1"
        :disabled="item.disabled"
        @click="pick(item)"
      >
        <Icon v-if="item.icon" :name="item.icon" :size="15" />
        <span class="x-tabs-label">{{ item.label }}</span>
        <span
          v-if="canClose(item)"
          class="x-tabs-close"
          role="button"
          :aria-label="`关闭 ${item.label}`"
          @click.stop="close(item.key)"
        ><Icon name="x" :size="13" /></span>
      </button>
    </div>
    <div class="x-tabs-body">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.x-tabs-wrap { display: flex; flex-direction: column; min-width: 0; }
.x-tabs {
  position: relative;
  display: flex;
  align-items: center;
  gap: 2px;
  min-width: 0;
  overflow-x: auto;
  overscroll-behavior: contain;
}
.x-tabs.is-line { border-bottom: 1px solid var(--line-strong); padding-bottom: 1px; }
.x-tabs.is-card { gap: 6px; }
.x-tabs-thumb {
  position: absolute;
  left: 0;
  bottom: 0;
  height: 2px;
  border-radius: 9999px;
  background: var(--blue);
  pointer-events: none;
}
.x-tabs-tab {
  position: relative;
  display: inline-flex;
  align-items: center;
  gap: 7px;
  flex: none;
  height: var(--control-h);
  padding: 0 13px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink-muted);
  white-space: nowrap;
  transition: color .2s ease, background .2s ease, box-shadow .2s ease;
}
.x-tabs-tab:hover:not(:disabled) { color: var(--ink); }
.x-tabs-tab:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-tabs.is-line .x-tabs-tab.is-active { color: var(--blue); font-weight: 620; }
.x-tabs.is-card .x-tabs-tab { background: var(--groove-bg); box-shadow: var(--groove-inset); }
.x-tabs.is-card .x-tabs-tab.is-active {
  background: var(--surface-solid);
  color: var(--ink);
  font-weight: 620;
  box-shadow: var(--e1), var(--edge);
}
.x-tabs-label { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.x-tabs-close {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  height: 16px;
  margin-right: -4px;
  border-radius: 9999px;
  color: var(--ink-faint);
  transition: background .18s ease, color .18s ease;
}
.x-tabs-close:hover { background: var(--press-bg); color: var(--ink); }
.x-tabs-body { min-width: 0; }
</style>
