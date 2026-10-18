<script setup lang="ts">
/* 进度条：line 用宽度过渡、circle 用 SVG 描边偏移，两条实现共用一套状态色。
   percent 由调用方保证在 0~100 之间，组件只做夹取不做业务换算。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  percent: number
  type?: 'line' | 'circle'
  status?: 'normal' | 'success' | 'error' | 'warning'
  size?: number
  showText?: boolean
  strokeWidth?: number
}>(), {
  type: 'line',
  status: 'normal',
  size: 120,
  showText: true,
  strokeWidth: 8,
})

/** [参数] 无 [返回] 夹在 0~100 的百分比，避免外部传入越界值把条撑爆 */
const safe = computed(() => Math.min(100, Math.max(0, props.percent)))

/** [参数] 无 [返回] 带一位小数的百分比文案，读数不抖动 */
const text = computed(() => `${Number(safe.value.toFixed(1))}%`)

/* 环形几何：半径取掉描边宽度，周长供 dasharray 使用 */
/** [参数] 无 [返回] 环形半径，已扣掉描边宽度避免环被裁 */
const radius = computed(() => (props.size - props.strokeWidth) / 2)

/** [参数] 无 [返回] 环形周长，作为 dasharray 的整圈长度 */
const circumference = computed(() => 2 * Math.PI * radius.value)
/** [参数] 无 [返回] 当前进度对应的实线长度，直接喂给 stroke-dasharray */
const dash = computed(() => `${(circumference.value * safe.value) / 100} ${circumference.value}`)
</script>

<template>
  <div v-if="type === 'line'" :class="['x-progress', `is-${status}`]">
    <div
      class="x-progress-track"
      role="progressbar"
      :aria-valuenow="safe"
      aria-valuemin="0"
      aria-valuemax="100"
    >
      <span class="x-progress-fill" :style="{ width: `${safe}%`, height: `${strokeWidth}px` }" />
    </div>
    <span v-if="showText" class="x-progress-text tnum">{{ text }}</span>
  </div>

  <div v-else :class="['x-progress-circle', `is-${status}`]" :style="{ width: `${size}px`, height: `${size}px` }">
    <svg :width="size" :height="size" :viewBox="`0 0 ${size} ${size}`" role="progressbar" :aria-valuenow="safe" aria-valuemin="0" aria-valuemax="100">
      <circle
        class="x-progress-ring-track"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
      />
      <circle
        class="x-progress-ring-fill"
        :cx="size / 2"
        :cy="size / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="dash"
        :transform="`rotate(-90 ${size / 2} ${size / 2})`"
      />
    </svg>
    <span v-if="showText" class="x-progress-circle-text tnum">{{ text }}</span>
  </div>
</template>

<style scoped>
.x-progress { display: flex; align-items: center; gap: 10px; width: 100%; }
.x-progress-track {
  flex: 1;
  min-width: 0;
  border-radius: 999px;
  background: var(--groove-bg);
  box-shadow: var(--groove-inset);
  overflow: hidden;
}
/* 宽度过渡走项目缓动，进度推进像滑块滑过去而不是跳过去 */
.x-progress-fill {
  display: block;
  border-radius: 999px;
  background: var(--blue);
  transition: width .5s var(--ease-premium), background .3s ease;
}
.x-progress-text { flex: none; font-size: 12px; color: var(--ink-muted); min-width: 42px; text-align: right; }

.x-progress-circle { position: relative; display: inline-grid; place-items: center; }
.x-progress-ring-track { stroke: var(--groove-bg); }
.x-progress-ring-fill { stroke: var(--blue); transition: stroke-dasharray .5s var(--ease-premium), stroke .3s ease; }
.x-progress-circle-text {
  position: absolute;
  font-size: 14px;
  font-weight: 640;
  color: var(--ink);
}

.x-progress.is-success .x-progress-fill { background: var(--lime); }
.x-progress.is-error .x-progress-fill { background: var(--red); }
.x-progress.is-warning .x-progress-fill { background: var(--cat-1-ink); }
.x-progress-circle.is-success .x-progress-ring-fill { stroke: var(--lime); }
.x-progress-circle.is-error .x-progress-ring-fill { stroke: var(--red); }
.x-progress-circle.is-warning .x-progress-ring-fill { stroke: var(--cat-1-ink); }
</style>
