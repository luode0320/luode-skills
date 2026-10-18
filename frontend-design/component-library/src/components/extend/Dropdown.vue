<script setup lang="ts">
/* 下拉菜单：点或悬停触发区后浮出选项列表，选中即派发 key 并关闭。
   菜单 Teleport 到 body，层级用 floatingLayerFor 跟随所在浮层；点击外部按 pointerdown 捕获关闭。 */
import { nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface DropdownItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
  /** 在该项上方补一条分隔线，用于分组 */
  divided?: boolean
}

const props = withDefaults(defineProps<{
  items: DropdownItem[]
  trigger?: 'click' | 'hover'
  placement?: 'bottom' | 'top'
}>(), {
  trigger: 'click',
  placement: 'bottom',
})

const emit = defineEmits<{ (e: 'select', key: string): void }>()

const triggerEl = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0, width: 0 })
let hoverTimer: number | undefined

/** [参数] 无 [返回] 无；按触发区包围盒定位菜单，空间不足时向另一侧翻转并夹在视口内 */
function place() {
  const rect = triggerEl.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 0
  const width = Math.max(rect.width, 160)
  const gap = 6
  const preferTop = props.placement === 'top'
  const below = window.innerHeight - rect.bottom
  const flip = preferTop ? rect.top < height + gap : below < height + gap
  const top = preferTop !== flip ? rect.top - height - gap : rect.bottom + gap
  const left = Math.min(rect.left, window.innerWidth - width - 8)
  pos.value = { top: Math.max(8, top), left: Math.max(8, left), width }
}

/** [参数] 无 [返回] 无；打开菜单并绑定外部关闭与跟随定位 */
async function show() {
  if (open.value) return
  open.value = true
  place()
  await nextTick()
  place()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/** [参数] 无 [返回] 无；关闭菜单并解绑全局监听 */
function hide() {
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
}

/** [参数] item 被点的选项 [返回] 无；禁用项不派发，正常项派发 key 后关闭 */
function pick(item: DropdownItem) {
  if (item.disabled) return
  emit('select', item.key)
  hide()
}

/** [参数] event 全局指针按下事件 [返回] 无；落在触发区或菜单内则不关闭 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (triggerEl.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/** [参数] 无 [返回] 无；click 模式下切换开关 */
function onClick() {
  if (props.trigger !== 'click') return
  if (open.value) hide()
  else show()
}

/** [参数] 无 [返回] 无；hover 模式延迟浮出，避免扫过时闪动 */
function onEnter() {
  if (props.trigger !== 'hover') return
  window.clearTimeout(hoverTimer)
  hoverTimer = window.setTimeout(show, 120)
}

/** [参数] 无 [返回] 无；hover 模式移出即收，光标进入菜单时由菜单侧取消 */
function onLeave() {
  if (props.trigger !== 'hover') return
  window.clearTimeout(hoverTimer)
  hoverTimer = window.setTimeout(hide, 120)
}

/** [参数] 无 [返回] 无；光标从触发区移进菜单，撤销待执行的收起 */
function keepOpen() {
  window.clearTimeout(hoverTimer)
}

onBeforeUnmount(() => {
  window.clearTimeout(hoverTimer)
  hide()
})
</script>

<template>
  <span
    ref="triggerEl"
    class="x-dropdown-trigger"
    @click="onClick"
    @pointerenter="onEnter"
    @pointerleave="onLeave"
  >
    <slot />
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-dropdown m-float"
        role="menu"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, minWidth: `${pos.width}px`, zIndex: floatingLayerFor(triggerEl) }"
        @pointerenter="keepOpen"
        @pointerleave="onLeave"
      >
        <button
          v-for="item in items"
          :key="item.key"
          type="button"
          role="menuitem"
          :class="['x-dropdown-item', item.divided && 'is-divided']"
          :disabled="item.disabled"
          @click="pick(item)"
        >
          <Icon v-if="item.icon" :name="item.icon" :size="15" />
          <span class="x-dropdown-label">{{ item.label }}</span>
        </button>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-dropdown-trigger { display: inline-flex; }
.x-dropdown {
  position: fixed;
  z-index: 120;
  min-width: 160px;
  padding: 6px;
  border-radius: var(--r-md);
  display: flex;
  flex-direction: column;
}
.x-dropdown-item {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  text-align: left;
  transition: background .15s ease, color .15s ease;
}
.x-dropdown-item:hover:not(:disabled) { background: var(--hover-bg); }
.x-dropdown-item:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-dropdown-item.is-divided { margin-top: 6px; border-top: 1px solid var(--line); padding-top: 6px; }
.x-dropdown-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
</style>
