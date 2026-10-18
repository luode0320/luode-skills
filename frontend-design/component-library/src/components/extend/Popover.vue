<script setup lang="ts">
/* 气泡卡片：比 Tooltip 更重的一块浮层，可放标题、正文与可点内容。
   与 Tooltip 同一套定位与 pop 动效；差别是面板接指针事件、可点内部，
   hover 模式下给 120ms 宽限，允许指针从触发区移进卡片而不闪断。 */
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  title?: string
  content?: string
  trigger?: 'click' | 'hover'
  placement?: 'top' | 'bottom' | 'left' | 'right'
  width?: number
}>(), {
  trigger: 'hover',
  placement: 'top',
  width: 240,
})

const anchorRef = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
let timer: number | undefined

/** [参数] 无 [返回] 无；按触发区与卡片实测尺寸算出贴边位置并夹进视口 */
function place() {
  const rect = anchorRef.value?.getBoundingClientRect()
  const box = panel.value?.getBoundingClientRect()
  if (!rect || !box) return
  const gap = 8
  const vertical = props.placement === 'top' || props.placement === 'bottom'
  const after = props.placement === 'bottom' || props.placement === 'right'
  let top = vertical
    ? (after ? rect.bottom + gap : rect.top - box.height - gap)
    : rect.top + rect.height / 2 - box.height / 2
  let left = vertical
    ? rect.left + rect.width / 2 - box.width / 2
    : (after ? rect.right + gap : rect.left - box.width - gap)
  /* 该方向放不下就翻到对侧，再四边夹住，杜绝卡片被裁掉 */
  if (vertical && top + box.height > window.innerHeight - 8) top = rect.top - box.height - gap
  else if (vertical && top < 8) top = rect.bottom + gap
  if (!vertical && left + box.width > window.innerWidth - 8) left = rect.left - box.width - gap
  else if (!vertical && left < 8) left = rect.right + gap
  left = Math.min(Math.max(8, left), window.innerWidth - box.width - 8)
  top = Math.min(Math.max(8, top), window.innerHeight - box.height - 8)
  pos.value = { top, left }
}

/** [参数] 无 [返回] 无；打开卡片并接上外部点击与 Esc 监听 */
async function show() {
  window.clearTimeout(timer)
  if (open.value) return
  open.value = true
  await nextTick()
  place()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
  document.addEventListener('keydown', onKey)
}

/** [参数] 无 [返回] 无；收起卡片并撤掉全部监听 */
function hide() {
  window.clearTimeout(timer)
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
  document.removeEventListener('keydown', onKey)
}

/** [参数] 无 [返回] 无；hover 模式留一点宽限，让指针能移进卡片 */
function hideSoon() {
  if (props.trigger !== 'hover') return
  window.clearTimeout(timer)
  timer = window.setTimeout(hide, 120)
}

/** [参数] event 指针按下事件 [返回] 无；点在卡片与触发区之外就收起 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (panel.value?.contains(target) || anchorRef.value?.contains(target)) return
  hide()
}

/** [参数] event 键盘事件 [返回] 无；Esc 收起并把事件吞掉，避免上层一起关 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape' && open.value) {
    event.stopPropagation()
    hide()
  }
}

/** [参数] 无 [返回] 无；按 trigger 模式把当前开合态取反 */
function toggle() {
  if (props.trigger === 'click') (open.value ? hide() : show())
}

watch(() => props.placement, () => { if (open.value) nextTick(place) })
onBeforeUnmount(() => {
  window.clearTimeout(timer)
  hide()
})
</script>

<template>
  <span
    ref="anchorRef"
    class="x-pop-trigger"
    @click="toggle"
    @pointerenter="trigger === 'hover' && show()"
    @pointerleave="hideSoon"
    @focusin="trigger === 'hover' && show()"
    @focusout="hideSoon"
  >
    <slot />
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="panel"
        class="x-pop m-float"
        role="dialog"
        :aria-label="title"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, width: `${width}px`, zIndex: floatingLayerFor(anchorRef) }"
        @pointerenter="trigger === 'hover' && show()"
        @pointerleave="hideSoon"
      >
        <div v-if="title" class="x-pop-title">{{ title }}</div>
        <div v-if="content" class="x-pop-text">{{ content }}</div>
        <div v-if="$slots.content" class="x-pop-slot"><slot name="content" /></div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-pop-trigger { display: inline-flex; }
.x-pop {
  position: fixed;
  padding: 12px 14px;
  border-radius: var(--r-sm);
  font-size: 13px;
  line-height: 1.6;
  color: var(--ink);
}
.x-pop-title { font-size: 13px; font-weight: 640; margin-bottom: 4px; }
.x-pop-text { color: var(--ink-muted); }
.x-pop-slot:not(:first-child) { margin-top: 6px; }
</style>
