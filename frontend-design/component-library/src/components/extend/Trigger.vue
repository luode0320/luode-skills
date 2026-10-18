<script setup lang="ts">
/* 触发器：通用「定位 + 显隐」底层原语，Dropdown / Popover 这类浮层都由它派生。
   只负责四件事：把触发区摆好、把浮层贴到触发区旁并避让视口、
   按 trigger 列表响应交互、把开合态以 popupVisible 双向同步出去。
   浮层内容与样式完全交给调用方，本组件不自带任何外观。 */
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

type Placement = 'top' | 'bottom' | 'left' | 'right' | 'bottom-start' | 'bottom-end'

const props = withDefaults(defineProps<{
  trigger?: Array<'click' | 'hover' | 'focus' | 'contextmenu'>
  placement?: Placement
  popupVisible?: boolean
  disabled?: boolean
  popupClass?: string
}>(), {
  trigger: () => ['hover'],
  placement: 'bottom',
  popupVisible: false,
})

const emit = defineEmits<{ (e: 'update:popupVisible', v: boolean): void }>()

const anchor = ref<HTMLElement | null>(null)
const popup = ref<HTMLElement | null>(null)
const inner = ref(false)
const pos = ref({ top: 0, left: 0 })
let timer: number | undefined

/** [参数] name 触发方式 [返回] 该方式是否在启用列表内 */
function has(name: 'click' | 'hover' | 'focus' | 'contextmenu') {
  return props.trigger.includes(name)
}

/** [参数] next 目标开合态 [返回] 无；内部状态落地后按需接线、等 DOM 更新再定位 */
async function apply(next: boolean) {
  inner.value = next
  toggleListeners(next)
  if (!next) return
  await nextTick()
  if (inner.value) place()
}

/** [参数] next 目标开合态 [返回] 无；同步内部状态并向上派发 update:popupVisible */
function setVisible(next: boolean) {
  if (inner.value === next) return
  emit('update:popupVisible', next)
  apply(next)
}

/** [参数] 无 [返回] 无；把浮层定位到触发区旁，放不下就翻边并夹进视口 */
function place() {
  const rect = anchor.value?.getBoundingClientRect()
  const box = popup.value?.getBoundingClientRect()
  if (!rect || !box) return
  const gap = 8
  const p = props.placement
  const vertical = p !== 'left' && p !== 'right'
  const after = p === 'bottom' || p === 'right' || p === 'bottom-start' || p === 'bottom-end'
  let top = vertical
    ? (after ? rect.bottom + gap : rect.top - box.height - gap)
    : rect.top + rect.height / 2 - box.height / 2
  let left: number
  if (!vertical) {
    left = after ? rect.right + gap : rect.left - box.width - gap
  } else if (p === 'bottom-start') {
    left = rect.left
  } else if (p === 'bottom-end') {
    left = rect.right - box.width
  } else {
    left = rect.left + rect.width / 2 - box.width / 2
  }
  /* 主方向空间不够就翻到对侧，再四边夹住，杜绝浮层被裁掉 */
  if (vertical && after && top + box.height > window.innerHeight - 8) top = rect.top - box.height - gap
  else if (vertical && !after && top < 8) top = rect.bottom + gap
  else if (!vertical && after && left + box.width > window.innerWidth - 8) left = rect.left - box.width - gap
  else if (!vertical && !after && left < 8) left = rect.right + gap
  left = Math.min(Math.max(8, left), window.innerWidth - box.width - 8)
  top = Math.min(Math.max(8, top), window.innerHeight - box.height - 8)
  pos.value = { top, left }
}

/** [参数] on 是否接线 [返回] 无；统一管理外部点击、滚动与 Esc 三类监听 */
function toggleListeners(on: boolean) {
  if (on) {
    document.addEventListener('pointerdown', onOutside, true)
    window.addEventListener('scroll', place, true)
    window.addEventListener('resize', place)
    document.addEventListener('keydown', onKey)
    return
  }
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
  document.removeEventListener('keydown', onKey)
}

/** [参数] event 指针按下事件 [返回] 无；点在浮层与触发区之外就收起 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (popup.value?.contains(target) || anchor.value?.contains(target)) return
  setVisible(false)
}

/** [参数] event 键盘事件 [返回] 无；Esc 收起并吞掉事件，避免上层一起关 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape' && inner.value) {
    event.stopPropagation()
    setVisible(false)
  }
}

/** [参数] event 鼠标或焦点事件 [返回] 无；按 click / contextmenu 取反，其余方式直接打开 */
function onOpen(event: MouseEvent | FocusEvent, mode: 'click' | 'hover' | 'focus' | 'contextmenu') {
  if (props.disabled || !has(mode)) return
  if (event instanceof MouseEvent && mode === 'contextmenu') event.preventDefault()
  setVisible(mode === 'hover' || mode === 'focus' ? true : !inner.value)
}

/** [参数] 无 [返回] 无；hover 离开延迟收起，给指针移进浮层的宽限 */
function onLeave() {
  if (!has('hover')) return
  window.clearTimeout(timer)
  timer = window.setTimeout(() => setVisible(false), 120)
}

/** [参数] event 焦点事件 [返回] 无；焦点移进浮层内部时不收起，其余情况收起 */
function onFocusOut(event: FocusEvent) {
  if (!has('focus')) return
  const next = event.relatedTarget as Node | null
  if (next && popup.value?.contains(next)) return
  setVisible(false)
}

/* 外部 popupVisible 变化时补一次定位；首次挂载若已为 true 也走同一条路径 */
watch(() => props.popupVisible, (value) => { if (inner.value !== value) apply(value) }, { immediate: true })

watch(() => props.placement, () => { if (inner.value) nextTick(place) })

onBeforeUnmount(() => {
  window.clearTimeout(timer)
  toggleListeners(false)
})
</script>

<template>
  <span
    ref="anchor"
    class="x-trigger"
    :aria-expanded="inner"
    @click="onOpen($event, 'click')"
    @pointerenter="onOpen($event, 'hover')"
    @pointerleave="onLeave"
    @focusin="onOpen($event, 'focus')"
    @focusout="onFocusOut"
    @contextmenu="onOpen($event, 'contextmenu')"
  >
    <slot />
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="inner"
        ref="popup"
        :class="['x-trigger-popup', popupClass]"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(anchor) }"
        @pointerenter="onOpen($event, 'hover')"
        @pointerleave="onLeave"
      >
        <slot name="content" />
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-trigger { display: inline-flex; }
/* 只做定位容器，外观（玻璃、边框、内边距）由调用方经 popupClass 或插槽内容给 */
.x-trigger-popup { position: fixed; }
</style>
