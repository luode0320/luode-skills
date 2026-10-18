<script setup lang="ts">
/* 走马灯：CSS transform 位移切换，支持自动播放、循环、指示点与箭头。
   hover 暂停自动播放，切到后台（document.hidden）不推进，回来继续。 */
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  autoplay?: boolean
  interval?: number
  loop?: boolean
  indicatorPosition?: 'inside' | 'outside' | 'none'
  showArrow?: 'always' | 'hover' | 'never'
  current?: number
}>(), {
  interval: 3000,
  loop: true,
  indicatorPosition: 'inside',
  showArrow: 'hover',
  current: 0,
})

const emit = defineEmits<{
  (e: 'update:current', index: number): void
  (e: 'change', index: number): void
}>()

const track = ref<HTMLElement | null>(null)
const count = ref(0)
const hovering = ref(false)
const active = computed(() => (count.value ? ((props.current % count.value) + count.value) % count.value : 0))

/** [参数] 无 [返回] 轨道内子项数量；挂载与插槽变化后重新测量 */
function measure() {
  count.value = track.value?.children.length ?? 0
}

watch(() => props.current, (v) => {
  if (count.value && v >= count.value) emit('update:current', count.value - 1)
})

/** [参数] index 目标下标 [返回] 切到该张并同步 v-model 与 change */
function goTo(index: number) {
  if (!count.value) return
  const target = props.loop ? ((index % count.value) + count.value) % count.value : Math.min(Math.max(index, 0), count.value - 1)
  if (target === active.value) return
  emit('update:current', target)
  emit('change', target)
}

/** [参数] delta 方向步进 [返回] 上一张 / 下一张 */
function step(delta: number) {
  const next = active.value + delta
  if (!props.loop && (next < 0 || next >= count.value)) return
  goTo(next)
}

let timer: number | undefined

/** [参数] 无 [返回] 清掉自动播放定时器 */
function stopTimer() {
  window.clearInterval(timer)
  timer = undefined
}

/** [参数] 无 [返回] 在满足条件时重启自动播放定时器 */
function startTimer() {
  stopTimer()
  if (!props.autoplay || props.interval <= 0) return
  timer = window.setInterval(() => {
    /* 悬停或页面在后台时不推进，避免用户切回来后跳帧 */
    if (hovering.value || document.hidden) return
    step(1)
  }, props.interval)
}

watch(() => [props.autoplay, props.interval], startTimer)
watch(active, startTimer)

onMounted(() => {
  measure()
  startTimer()
})

onBeforeUnmount(stopTimer)
</script>

<template>
  <div
    class="x-carousel"
    :class="[`arrow-${showArrow}`, hovering && 'is-hover']"
    @pointerenter="hovering = true"
    @pointerleave="hovering = false"
  >
    <div ref="track" class="x-carousel-track" :style="{ transform: `translateX(${-active * 100}%)` }">
      <slot />
    </div>

    <button v-if="showArrow !== 'never'" class="x-carousel-arrow is-prev" type="button" aria-label="上一张" @click="step(-1)">
      <Icon name="chevronLeft" :size="16" />
    </button>
    <button v-if="showArrow !== 'never'" class="x-carousel-arrow is-next" type="button" aria-label="下一张" @click="step(1)">
      <Icon name="chevronRight" :size="16" />
    </button>

    <div v-if="indicatorPosition !== 'none'" :class="['x-carousel-dots', `is-${indicatorPosition}`]">
      <button
        v-for="i in count"
        :key="i"
        type="button"
        :class="['x-carousel-dot', i - 1 === active && 'is-active']"
        :aria-label="`第 ${i} 张`"
        @click="goTo(i - 1)"
      />
    </div>
  </div>
</template>

<style scoped>
.x-carousel { position: relative; overflow: hidden; border-radius: var(--r-md); }
.x-carousel-track { display: flex; transition: transform var(--ease-premium) .52s; }
.x-carousel-track > :deep(*) { flex: 0 0 100%; min-width: 0; }
.x-carousel-arrow {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid var(--glass-line-soft);
  border-radius: 9999px;
  background: var(--float-bg);
  color: var(--ink);
  cursor: pointer;
  box-shadow: var(--e1);
  opacity: 0;
  transition: opacity var(--ease-premium) .28s, background var(--ease-premium) .28s;
}
.x-carousel.is-hover .x-carousel-arrow, .x-carousel.arrow-always .x-carousel-arrow { opacity: 1; }
.x-carousel-arrow:hover { background: var(--surface-solid); }
.x-carousel-arrow.is-prev { left: 10px; }
.x-carousel-arrow.is-next { right: 10px; }
.x-carousel-dots { display: flex; gap: 6px; }
.x-carousel-dots.is-inside { position: absolute; left: 0; right: 0; bottom: 10px; justify-content: center; }
.x-carousel-dots.is-outside { padding: 10px 0 0; justify-content: center; }
.x-carousel-dot {
  width: 7px;
  height: 7px;
  padding: 0;
  border: 0;
  border-radius: 9999px;
  background: var(--ink-faint);
  opacity: .5;
  cursor: pointer;
  transition: width var(--ease-premium) .32s, opacity var(--ease-premium) .32s, background var(--ease-premium) .32s;
}
.x-carousel-dot.is-active { width: 18px; opacity: 1; background: var(--blue); }
</style>
