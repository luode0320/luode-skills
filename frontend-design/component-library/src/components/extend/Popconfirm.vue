<script setup lang="ts">
/* 气泡确认：点触发区浮出一个小气泡，确认或取消后收起。
   与 Tooltip 同一套定位与动效语态，区别是气泡可交互（可点按钮），
   点外部或 Esc 一律按「取消」处理，不会把用户悬在中间态。 */
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import Button from '@/components/ui/Button.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  title?: string
  message?: string
  okText?: string
  cancelText?: string
  danger?: boolean
  placement?: 'top' | 'bottom' | 'left' | 'right'
}>(), {
  okText: '确定',
  cancelText: '取消',
  placement: 'top',
})

const emit = defineEmits<{
  (e: 'ok'): void
  (e: 'confirm'): void
  (e: 'cancel'): void
}>()

const trigger = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })

/* 主边与交叉轴的初值：先按 placement 摆好，再按视口修正 */
const vertical = computed(() => props.placement === 'top' || props.placement === 'bottom')
const after = computed(() => props.placement === 'bottom' || props.placement === 'right')

/** [参数] 无 [返回] 无；按触发区与气泡实测尺寸算出贴边位置并夹进视口 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  const box = panel.value?.getBoundingClientRect()
  if (!rect || !box) return
  const gap = 8
  const isVertical = vertical.value
  const isAfter = after.value
  let top = isVertical
    ? (isAfter ? rect.bottom + gap : rect.top - box.height - gap)
    : rect.top + rect.height / 2 - box.height / 2
  let left = isVertical
    ? rect.left + rect.width / 2 - box.width / 2
    : (isAfter ? rect.right + gap : rect.left - box.width - gap)
  /* 该方向放不下就翻到对侧，再四边夹住，杜绝气泡被裁掉 */
  if (isVertical && top + box.height > window.innerHeight - 8) top = rect.top - box.height - gap
  else if (isVertical && top < 8) top = rect.bottom + gap
  if (!isVertical && left + box.width > window.innerWidth - 8) left = rect.left - box.width - gap
  else if (!isVertical && left < 8) left = rect.right + gap
  left = Math.min(Math.max(8, left), window.innerWidth - box.width - 8)
  top = Math.min(Math.max(8, top), window.innerHeight - box.height - 8)
  pos.value = { top, left }
}

/** [参数] 无 [返回] 无；打开气泡并把定位、外部点击与 Esc 监听接上 */
async function show() {
  if (open.value) return
  open.value = true
  await nextTick()
  place()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
  document.addEventListener('keydown', onKey)
}

/** [参数] 无 [返回] 无；收起气泡并撤掉全部监听 */
function hide() {
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
  document.removeEventListener('keydown', onKey)
}

/** [参数] event 指针按下事件 [返回] 无；点在气泡与触发区之外按取消收起 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (panel.value?.contains(target) || trigger.value?.contains(target)) return
  cancel()
}

/** [参数] event 键盘事件 [返回] 无；Esc 按取消收起 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape' && open.value) {
    event.stopPropagation()
    cancel()
  }
}

/** [参数] 无 [返回] 无；确认动作，ok 与 confirm 同时派发以兼容两种监听口径 */
function confirm() {
  hide()
  emit('ok')
  emit('confirm')
}

/** [参数] 无 [返回] 无；取消动作，点外部与 Esc 也走这里 */
function cancel() {
  hide()
  emit('cancel')
}

onBeforeUnmount(hide)
watch(() => props.placement, () => { if (open.value) nextTick(place) })
</script>

<template>
  <span
    ref="trigger"
    class="x-pc-trigger"
    aria-haspopup="dialog"
    :aria-expanded="open"
    @click="open ? cancel() : show()"
  >
    <slot />
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="panel"
        class="x-pc m-float"
        role="dialog"
        :aria-label="title"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div class="x-pc-body">
          <span :class="['x-pc-ico', danger && 'is-danger']">
            <Icon :name="danger ? 'alert' : 'info'" :size="16" :stroke="2" />
          </span>
          <div class="x-pc-text">
            <div v-if="title" class="x-pc-title">{{ title }}</div>
            <div v-if="message" class="x-pc-msg">{{ message }}</div>
          </div>
        </div>
        <div class="x-pc-foot">
          <Button variant="ghost" size="sm" @click="cancel">{{ cancelText }}</Button>
          <Button :variant="danger ? 'danger' : 'primary'" size="sm" @click="confirm">{{ okText }}</Button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-pc-trigger { display: inline-flex; }
.x-pc {
  position: fixed;
  width: 240px;
  padding: 12px 12px 10px;
  border-radius: var(--r-sm);
  color: var(--ink);
}
.x-pc-body { display: flex; align-items: flex-start; gap: 9px; }
.x-pc-ico {
  flex: none;
  display: inline-flex;
  margin-top: 1px;
  color: var(--blue);
}
.x-pc-ico.is-danger { color: var(--red-text); }
.x-pc-text { min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.x-pc-title { font-size: 13px; font-weight: 620; }
.x-pc-msg { font-size: 12px; line-height: 1.6; color: var(--ink-muted); }
.x-pc-foot {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  margin-top: 10px;
  padding-top: 8px;
  border-top: 1px solid var(--line);
}
</style>
