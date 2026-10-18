<script setup lang="ts">
/* 图标式帮助：一个小图标按钮，悬停或键盘聚焦时浮出功能 / 字段 / 业务说明。
   浮层走 .m-float 材质与 pop 动效；定位按触发区实测尺寸计算，超出视口自动翻面并夹边。
   最近修改时间：2026-10-17 21:54:00；改动原因：补齐图标式气泡帮助，指针与焦点各自独立触发。 */
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  /** 浮层里的说明正文 */
  content: string
  /** 可选的小标题：给出「这是什么」的短标签 */
  title?: string
  /** info 用主蓝色信息圈，help 用中性墨色问号圈 */
  tone?: 'info' | 'help'
  placement?: 'top' | 'bottom' | 'left' | 'right'
  /** 图标边长，点击区随它放大但保底 24px */
  size?: number
  /** 按钮的可读名称，读屏用户听到的就是它 */
  label?: string
  disabled?: boolean
  delay?: number
}>(), {
  tone: 'info',
  placement: 'top',
  size: 15,
  label: '查看说明',
  delay: 120,
})

/* 图标表属上游冻结面，问号圈无法登记进 src/data/icons.ts，故在此内联。 */
const PATHS = {
  info: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zm0-10v5m0-8h.01',
  help: 'M12 21a9 9 0 1 0 0-18 9 9 0 0 0 0 18zM9.8 9.3a2.3 2.3 0 1 1 3.4 2c-.8.5-1.2 1-1.2 1.9M12 16.6h.01',
} as const

const trigger = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
const id = `ht-${Math.random().toString(36).slice(2, 8)}`
let timer: number | undefined

/* 点击区随图标放大但保底 24px：小图标不缩水可点面积，大图标也不会溢出按钮 */
const hitSize = computed(() => `${Math.max(24, props.size + 9)}px`)

/** [参数] 无 [返回] 无；按触发区与浮层实测尺寸算出贴边位置并夹进视口 */
function place() {
  // 1. 两个矩形都拿不到时直接放弃，避免在未挂载阶段写入 NaN。
  const rect = trigger.value?.getBoundingClientRect()
  const box = panel.value?.getBoundingClientRect()
  if (!rect || !box) return
  // 2. 先按首选方向算中心对齐的位置。
  const gap = 8
  const vertical = props.placement === 'top' || props.placement === 'bottom'
  const after = props.placement === 'bottom' || props.placement === 'right'
  let top = vertical
    ? (after ? rect.bottom + gap : rect.top - box.height - gap)
    : rect.top + rect.height / 2 - box.height / 2
  let left = vertical
    ? rect.left + rect.width / 2 - box.width / 2
    : (after ? rect.right + gap : rect.left - box.width - gap)
  // 3. 该方向放不下就翻到对侧，4. 再四边夹住保证说明不被裁掉。
  if (vertical && top + box.height > window.innerHeight - 8) top = rect.top - box.height - gap
  else if (vertical && top < 8) top = rect.bottom + gap
  if (!vertical && left + box.width > window.innerWidth - 8) left = rect.left - box.width - gap
  else if (!vertical && left < 8) left = rect.right + gap
  left = Math.min(Math.max(8, left), window.innerWidth - box.width - 8)
  top = Math.min(Math.max(8, top), window.innerHeight - box.height - 8)
  pos.value = { top, left }
}

/** [参数] on：true 挂监听、false 撤监听 [返回] 无；滚动与缩放时重新定位 */
function bindReposition(on: boolean) {
  if (on) {
    window.addEventListener('scroll', place, true)
    window.addEventListener('resize', place)
    return
  }
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
}

/** [参数] now：true 跳过延迟（键盘聚焦用） [返回] 无；打开浮层并接上重新定位监听 */
async function show(now = false) {
  if (props.disabled || !props.content) return
  window.clearTimeout(timer)
  timer = window.setTimeout(async () => {
    if (open.value) return
    open.value = true
    await nextTick()
    place()
    bindReposition(true)
  }, now ? 0 : props.delay)
}

/** [参数] 无 [返回] 无；收起浮层并撤掉定位监听 */
function hide() {
  window.clearTimeout(timer)
  if (!open.value) return
  open.value = false
  bindReposition(false)
}

/** [参数] source：指针或焦点 [返回] 无；指针移出时以 DOM 真实焦点为准，聚焦中不移除说明 */
function release(source: 'hover' | 'focus') {
  // Esc 只关闭说明、按钮仍可能持有焦点；若改存本地标记，再次聚焦不会重复触发 focus 事件，
  // 标记会与真实焦点长期不一致，故这里直接查 DOM。
  if (source === 'hover' && document.activeElement === trigger.value) return
  hide()
}

/** [参数] 无 [返回] 无；Esc 属显式关闭，先让按钮失焦，否则下次悬停会被残留焦点卡住 */
function dismiss() {
  trigger.value?.blur()
  hide()
}

/** 内容变了就收起，避免旧说明继续挂在页面上 */
watch(() => props.content, hide)
onBeforeUnmount(() => { window.clearTimeout(timer); bindReposition(false) })
</script>

<template>
  <button
    ref="trigger"
    type="button"
    :class="['x-help', `is-${tone}`]"
    :style="{ width: hitSize, height: hitSize }"
    :aria-label="label"
    :aria-describedby="open ? id : undefined"
    :disabled="disabled"
    @pointerenter="show()"
    @pointerleave="release('hover')"
    @focus="show(true)"
    @blur="release('focus')"
    @keydown.esc.stop="dismiss"
  >
    <svg :width="size" :height="size" viewBox="0 0 24 24" fill="none" stroke="currentColor"
      stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <path :d="PATHS[tone]" />
    </svg>
  </button>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        :id="id"
        ref="panel"
        class="x-help-tip m-float"
        role="tooltip"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div v-if="title" class="x-help-tip-title">{{ title }}</div>
        <div class="x-help-tip-body">{{ content }}</div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* 点击区保底 24px 包住小图标，视觉上仍是文字旁的一个符号；尺寸由 hitSize 按图标档位给 */
.x-help {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  border-radius: 50%;
  vertical-align: middle;
  line-height: 0;
  color: var(--ink-muted);
  transition: color .2s ease, background .2s ease;
}
.x-help.is-info { color: var(--blue); }
.x-help:hover:not(:disabled) { background: var(--hover-bg); color: var(--ink); }
.x-help.is-info:hover:not(:disabled) { background: var(--blue-soft); color: var(--blue-hover); }
.x-help:disabled { opacity: .45; cursor: default; }

.x-help-tip {
  position: fixed;
  max-width: 260px;
  padding: 8px 11px;
  border-radius: var(--r-xs);
  font-size: 12px;
  line-height: 1.55;
  color: var(--ink);
  box-shadow: var(--e2);
  pointer-events: none;
}
.x-help-tip-title { font-weight: 620; }
/* 有标题时正文退一档，形成标题 / 说明两级 */
.x-help-tip-title + .x-help-tip-body { margin-top: 2px; color: var(--ink-muted); }
</style>
