<script setup lang="ts">
/* 提示气泡：hover / focus 时在目标旁浮出说明，位置自动避让视口边缘。
   动效走 overlayEnter/overlayLeave 的 pop 语态，与 Select 下拉同一手感。 */
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  content?: string
  placement?: 'top' | 'bottom' | 'left' | 'right'
  disabled?: boolean
  /** 悬停多久才浮出，避免扫过时闪动 */
  delay?: number
}>(), {
  placement: 'top',
  delay: 120,
})

const trigger = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
let timer: number | undefined

function place() {
  const rect = trigger.value?.getBoundingClientRect()
  const box = panel.value?.getBoundingClientRect()
  if (!rect || !box) return
  const gap = 8
  let top = rect.top - box.height - gap
  let left = rect.left + rect.width / 2 - box.width / 2
  if (props.placement === 'bottom') top = rect.bottom + gap
  else if (props.placement === 'left') { top = rect.top + rect.height / 2 - box.height / 2; left = rect.left - box.width - gap }
  else if (props.placement === 'right') { top = rect.top + rect.height / 2 - box.height / 2; left = rect.right + gap }
  /* 顶部空间不够就翻到下方，四边一律夹在视口内，杜绝气泡被裁掉 */
  if (props.placement === 'top' && top < 8) top = rect.bottom + gap
  if (props.placement === 'bottom' && top + box.height > window.innerHeight - 8) top = rect.top - box.height - gap
  left = Math.min(Math.max(8, left), window.innerWidth - box.width - 8)
  top = Math.min(Math.max(8, top), window.innerHeight - box.height - 8)
  pos.value = { top, left }
}

function show() {
  if (props.disabled || !props.content) return
  window.clearTimeout(timer)
  timer = window.setTimeout(async () => {
    open.value = true
    await nextTick()
    place()
  }, props.delay)
}

function hide() {
  window.clearTimeout(timer)
  open.value = false
}

watch(() => props.content, hide)
onBeforeUnmount(() => window.clearTimeout(timer))
</script>

<template>
  <span
    ref="trigger"
    class="x-tip-trigger"
    @pointerenter="show"
    @pointerleave="hide"
    @focusin="show"
    @focusout="hide"
  >
    <slot />
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="panel"
        class="x-tip m-float"
        role="tooltip"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >{{ content }}</div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-tip-trigger { display: inline-flex; }
.x-tip {
  position: fixed;
  max-width: 260px;
  padding: 7px 10px;
  border-radius: var(--r-xs);
  font-size: 12px;
  line-height: 1.5;
  color: var(--ink);
  box-shadow: var(--e2);
  pointer-events: none;
}
</style>
