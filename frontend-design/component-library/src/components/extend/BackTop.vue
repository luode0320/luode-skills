<script setup lang="ts">
/* 回到顶部：滚动超过阈值后浮出圆形按钮，点击平滑回顶。
   按钮走浮层材质 m-float，进出场沿用 pop 语态，与下拉、气泡同一手感。 */
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'

const props = withDefaults(defineProps<{
  /** 滚动容器选择器，缺省为 window */
  target?: string
  /** 停靠容器：给出时按钮改为容器内绝对定位，不传则固定到视口 */
  container?: HTMLElement | null
  /** 滚动超过该距离才浮出 */
  visibilityHeight?: number
  /** 距视口右侧（或容器右侧）的距离 */
  right?: number
  /** 距视口底部（或容器底部）的距离 */
  bottom?: number
}>(), {
  visibilityHeight: 400,
  right: 28,
  bottom: 28,
})

const shown = ref(false)
const root = ref<HTMLElement | null>(null)
/* 挂载后才拿得到父元素，用它驱动定位样式重算：首帧 root 为空会退化成视口固定 */
const hostReady = ref(false)
let bound: Window | HTMLElement | null = null

/** [参数] 无 [返回] 当前滚动容器，选择器查不到时回退 window */
function scroller(): Window | HTMLElement {
  if (!props.target) return window
  return document.querySelector<HTMLElement>(props.target) ?? window
}

/** [参数] 无 [返回] 停靠容器；未配置时返回 null，按钮回到视口固定 */
function dock(): HTMLElement | null {
  return props.container ?? null
}

/** [参数] 无 [返回] 直接父元素；锚点铺满它，因此它必须是定位上下文 */
function hostEl(): HTMLElement | null {
  return root.value?.parentElement ?? null
}

/** [参数] 无 [返回] 无；容器内停靠要求容器自身是定位上下文，缺失时补 relative */
function ensureDockContext(el: HTMLElement) {
  if (getComputedStyle(el).position === 'static') el.style.position = 'relative'
}

/** [参数] 无 [返回] 当前滚动容器已滚过的距离 */
function offset(): number {
  const el = bound
  if (!(el instanceof HTMLElement)) return window.scrollY
  return el.scrollTop
}

/** [参数] 无 [返回] 无；按阈值切换按钮显隐 */
function measure() {
  shown.value = offset() > props.visibilityHeight
}

/** [参数] 无 [返回] 无；平滑滚回容器顶部 */
function toTop() {
  if (bound === window || !bound) window.scrollTo({ top: 0, behavior: 'smooth' })
  else bound.scrollTo({ top: 0, behavior: 'smooth' })
}

/** [参数] 无 [返回] 无；把滚动监听挂到当前容器，切换 target 时先解绑旧容器 */
function bind() {
  unbind()
  bound = scroller()
  if (bound === window) window.addEventListener('scroll', measure, { passive: true })
  else bound.addEventListener('scroll', measure, { passive: true })
  // 锚点铺满直接父元素，父元素必须是定位上下文；缺省时补 relative。
  const host = dock() ?? hostEl()
  if (host) ensureDockContext(host)
  measure()
}

/** [参数] 无 [返回] 无；解绑滚动监听 */
function unbind() {
  if (bound === window) window.removeEventListener('scroll', measure)
  else bound?.removeEventListener('scroll', measure)
  bound = null
}

/** [参数] 无 [返回] 按钮定位样式；有停靠宿主时改绝对定位，否则维持视口固定 */
const anchorStyle = computed<Record<string, string>>(() => {
  const docked = hostReady.value && Boolean(dock() ?? hostEl())
  return { position: docked ? 'absolute' : 'fixed', right: `${props.right}px`, bottom: `${props.bottom}px` }
})

onMounted(() => {
  hostReady.value = true
  bind()
})
onBeforeUnmount(unbind)
watch(() => [props.target, props.container], bind)
</script>

<template>
  <div ref="root" class="x-backtop-anchor">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <button
        v-if="shown"
        type="button"
        class="x-backtop m-float"
        aria-label="回到顶部"
        :style="anchorStyle"
        @click="toTop"
      >
        <Icon name="arrowUp" :size="18" :stroke="2" />
      </button>
    </Transition>
  </div>
</template>

<style scoped>
/* 锚点撑满直接父容器并作为定位基准：绝对定位子元素的包含块是最近的定位祖先，
   只有锚点具备真实尺寸时 right/bottom 才指向父容器右下角。
   父容器的定位上下文由 bind() 补 relative，锚点自身不接收指针。 */
.x-backtop-anchor { position: absolute; inset: 0; pointer-events: none; }
.x-backtop {
  /* position 由内联样式给出：容器停靠时为 absolute，视口模式为 fixed。
     写在这里会压过内联值，导致 container 模式失效。 */
  z-index: 120;
  width: 42px;
  height: 42px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  color: var(--ink-muted);
  transition: color .2s ease;
}
.x-backtop:hover { color: var(--blue); }
</style>
