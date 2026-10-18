<script setup lang="ts">
/* 固钉：让内容在滚动容器内吸附在顶部或底部，滚出后仍保持可见。
   吸附交给 position: sticky，JS 只上报是否已进入吸附态，不手写滚动位移计算。 */
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = defineProps<{
  /** 距容器顶部多远开始吸附，缺省 0 */
  offsetTop?: number
  /** 距容器底部多远开始吸附，与 offsetTop 同时给出时以 offsetTop 为准 */
  offsetBottom?: number
  /** 滚动容器选择器，缺省为 window */
  target?: string
}>()

const wrap = ref<HTMLElement | null>(null)
/** 是否已钉住，供调用方在 is-pinned 上加自己的视觉反馈 */
const pinned = ref(false)

/** [参数] 无 [返回] 当前滚动容器，选择器查不到时回退 window */
function scroller(): Window | HTMLElement {
  if (!props.target) return window
  return document.querySelector<HTMLElement>(props.target) ?? window
}

/** [参数] 无 [返回] 是否按底部吸附，顶部未指定且底部已指定时成立 */
const useBottom = computed(() => props.offsetBottom !== undefined && props.offsetTop === undefined)

/** [参数] 无 [返回] 无；比较占位块与视口边界，得出是否已吸附 */
function measure() {
  const rect = wrap.value?.getBoundingClientRect()
  if (!rect) return
  if (useBottom.value) {
    pinned.value = rect.bottom >= window.innerHeight - (props.offsetBottom ?? 0)
    return
  }
  pinned.value = rect.top <= (props.offsetTop ?? 0)
}

let bound: EventTarget | null = null

/** [参数] 无 [返回] 无；把滚动监听挂到当前容器，切换 target 时先解绑旧容器 */
function bind() {
  unbind()
  bound = scroller()
  bound.addEventListener('scroll', measure, { passive: true })
  window.addEventListener('resize', measure)
  measure()
}

/** [参数] 无 [返回] 无；解绑滚动与尺寸监听 */
function unbind() {
  bound?.removeEventListener('scroll', measure)
  bound = null
  window.removeEventListener('resize', measure)
}

onMounted(bind)
onBeforeUnmount(unbind)
watch(() => props.target, bind)

/** [参数] 无 [返回] 吸附方向的内联样式，sticky 靠它定位 */
const stickyStyle = computed(() => (
  useBottom.value ? { bottom: `${props.offsetBottom}px` } : { top: `${props.offsetTop ?? 0}px` }
))
</script>

<template>
  <div ref="wrap" :class="['x-affix', pinned && 'is-pinned']">
    <div class="x-affix-inner" :style="stickyStyle">
      <slot />
    </div>
  </div>
</template>

<style scoped>
.x-affix { position: relative; }
.x-affix-inner { position: sticky; z-index: 1; }
/* 吸附后压在滚动内容之上，避免被后续内容盖住 */
.x-affix.is-pinned .x-affix-inner { z-index: 2; }
</style>
