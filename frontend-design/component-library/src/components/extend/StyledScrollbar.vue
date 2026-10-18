<script setup lang="ts">
/* 自定义滚动条：滚动容器保持原生 overflow / 键盘 / 触控板行为，只额外画一条浮动滑块压在上面。
   滑块位置与比例由 scroll 事件同步，hover / 滚动 / 聚焦时显现，静止一段时间后淡出。
   本条只做视觉呈现，不接管滚动，所以鼠标滚轮、方向键、触摸惯性都仍是浏览器原生的。
   两轴几何各自独立计算，direction='both' 时横竖滑块同时工作，不会串用对方数据。 */
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

const props = withDefaults(defineProps<{
  direction?: 'vertical' | 'horizontal' | 'both'
  maxHeight?: number | string
  maxWidth?: number | string
  always?: boolean
}>(), {
  direction: 'vertical',
})

const view = ref<HTMLElement | null>(null)
const active = ref(false)
/* 两轴各自的滑块几何：size 是滑块长度，offset 是轴向上的起点 */
const vThumb = ref({ size: 0, offset: 0 })
const hThumb = ref({ size: 0, offset: 0 })
const vOverflow = ref(false)
const hOverflow = ref(false)
let idleTimer: number | undefined
let observer: ResizeObserver | undefined

const showVertical = computed(() => props.direction === 'vertical' || props.direction === 'both')
const showHorizontal = computed(() => props.direction === 'horizontal' || props.direction === 'both')

/**
 * [参数] value 尺寸值，可为 number 或带单位的字符串
 * [返回] 补上 px 的字符串；字符串原样透传，缺省时返回 undefined
 */
function toSize(value?: number | string) {
  if (value === undefined) return undefined
  return typeof value === 'number' ? `${value}px` : value
}

const style = computed(() => ({
  maxHeight: toSize(props.maxHeight),
  maxWidth: toSize(props.maxWidth),
}))

/**
 * [参数] offset 内容滚动偏移，content 内容总长，viewport 视口长度，minThumb 滑块最短像素
 * [返回] 该轴的 { size, offset }；无溢出时返回零值，滑块不渲染
 */
function geometry(offset: number, content: number, viewport: number, minThumb: number) {
  if (content <= viewport || viewport <= 0) return { size: 0, offset: 0 }
  const size = Math.max((viewport / content) * viewport, Math.min(minThumb, viewport))
  const travel = viewport - size
  return { size, offset: (offset / (content - viewport)) * travel }
}

/** [参数] 无 [返回] 无。重新量内容与视口，分别算出两轴滑块的长度与位置 */
function sync() {
  const el = view.value
  if (!el) return
  vOverflow.value = el.scrollHeight > el.clientHeight
  hOverflow.value = el.scrollWidth > el.clientWidth
  vThumb.value = geometry(el.scrollTop, el.scrollHeight, el.clientHeight, 24)
  hThumb.value = geometry(el.scrollLeft, el.scrollWidth, el.clientWidth, 24)
}

/** [参数] 无 [返回] 无。滚动时唤醒滑块并同步一次位置 */
function onScroll() {
  sync()
  wake()
}

/** [参数] 无 [返回] 无。让滑块显现，并重置淡出倒计时 */
function wake() {
  active.value = true
  window.clearTimeout(idleTimer)
  idleTimer = window.setTimeout(() => { active.value = false }, 900)
}

onMounted(() => {
  sync()
  /* 容器尺寸变化时重新量一次比例，取代一次性快照 */
  if (typeof ResizeObserver !== 'undefined' && view.value) {
    observer = new ResizeObserver(sync)
    observer.observe(view.value)
  }
})

onBeforeUnmount(() => {
  window.clearTimeout(idleTimer)
  observer?.disconnect()
})
</script>

<template>
  <div
    :class="['x-scroll', active && 'is-active', always && 'is-always']"
    :style="style"
    @pointerenter="wake"
  >
    <div
      ref="view"
      class="x-scroll-view"
      tabindex="0"
      @scroll.passive="onScroll"
    >
      <slot />
    </div>
    <span v-if="showVertical && vOverflow" class="x-scroll-bar is-y" aria-hidden="true">
      <span
        class="x-scroll-thumb"
        :style="{ height: `${vThumb.size}px`, transform: `translateY(${vThumb.offset}px)` }"
      />
    </span>
    <span v-if="showHorizontal && hOverflow" class="x-scroll-bar is-x" aria-hidden="true">
      <span
        class="x-scroll-thumb"
        :style="{ width: `${hThumb.size}px`, transform: `translateX(${hThumb.offset}px)` }"
      />
    </span>
  </div>
</template>

<style scoped>
.x-scroll { position: relative; min-width: 0; }
.x-scroll-view {
  box-sizing: border-box;
  max-height: inherit;
  max-width: inherit;
  overflow: auto;
  outline: none;
  /* 原生滚动条收起，只留自绘滑块；滚动能力与键盘可达性不受影响 */
  scrollbar-width: none;
}
.x-scroll-view::-webkit-scrollbar { width: 0; height: 0; }
.x-scroll-view:focus-visible { box-shadow: inset 0 0 0 2px var(--focus); border-radius: inherit; }
.x-scroll-bar {
  position: absolute;
  border-radius: 9999px;
  opacity: 0;
  transition: opacity var(--ease-premium) .24s;
  pointer-events: none;
}
.x-scroll.is-active .x-scroll-bar,
.x-scroll.is-always .x-scroll-bar { opacity: 1; }
.x-scroll-bar.is-y { top: 2px; right: 2px; bottom: 2px; width: 6px; }
.x-scroll-bar.is-x { left: 2px; right: 2px; bottom: 2px; height: 6px; }
.x-scroll-thumb {
  position: absolute;
  display: block;
  border-radius: 9999px;
  background: var(--ink-faint);
  opacity: .5;
}
.x-scroll-bar.is-y .x-scroll-thumb { left: 0; right: 0; top: 0; }
.x-scroll-bar.is-x .x-scroll-thumb { top: 0; bottom: 0; left: 0; }
.x-scroll.is-active .x-scroll-thumb { opacity: .72; }
</style>
