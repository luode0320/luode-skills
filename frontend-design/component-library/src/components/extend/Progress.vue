<script setup lang="ts">
/* 进度条：line 用宽度过渡、circle 用 SVG 描边偏移，两条实现共用一套状态色。
   percent 由调用方保证在 0~100 之间，组件只做夹取不做业务换算。

   line 型在 status 变成 success 时不做「染绿」，而是**形变**：
   整条收拢成一个圆 → 圆环一笔描出 → 对勾再描一笔 → 回弹落定。
   形变只改形状不改结构，与登录按钮是同一套语态（放 / 结）。 */
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { playCrystallize } from '@/composables/crystallize'

const props = withDefaults(defineProps<{
  percent: number
  type?: 'line' | 'circle'
  status?: 'normal' | 'success' | 'error' | 'warning'
  /** 环形直径，px。用 diameter 而不是 size：size 专指控件档位，直径是几何量 */
  diameter?: number
  showText?: boolean
  strokeWidth?: number
}>(), {
  type: 'line',
  status: 'normal',
  diameter: 120,
  showText: true,
  strokeWidth: 8,
})

/** [参数] 无 [返回] 夹在 0~100 的百分比，避免外部传入越界值把条撑爆 */
const safe = computed(() => Math.min(100, Math.max(0, props.percent)))

/** [参数] 无 [返回] 带一位小数的百分比文案，读数不抖动 */
const text = computed(() => `${Number(safe.value.toFixed(1))}%`)

/* 环形几何：半径取掉描边宽度，周长供 dasharray 使用 */
/** [参数] 无 [返回] 环形半径，已扣掉描边宽度避免环被裁 */
const radius = computed(() => (props.diameter - props.strokeWidth) / 2)

/** [参数] 无 [返回] 环形周长，作为 dasharray 的整圈长度 */
const circumference = computed(() => 2 * Math.PI * radius.value)
/** [参数] 无 [返回] 当前进度对应的实线长度，直接喂给 stroke-dasharray */
const dash = computed(() => `${(circumference.value * safe.value) / 100} ${circumference.value}`)

/* ── 完成态形变 ────────────────────────────────────────────── */
const orb = ref<HTMLElement | null>(null)
const ring = ref<SVGCircleElement | null>(null)
const check = ref<SVGPathElement | null>(null)

/** 只有 line 型、真正走完（100%）且状态为 success 时才收拢成圆。
    条件里必须带 percent，否则「62% + success」会直接打出对勾，语义自相矛盾。 */
const done = computed(() => props.type === 'line' && props.status === 'success' && safe.value >= 100)

/** [参数] 无 [返回] 无；收拢后按钮区只剩图形，宽度直接给圆直径 */
function settle() {
  if (!orb.value) return
  orb.value.style.width = `${orb.value.getBoundingClientRect().height}px`
}

/* 进入完成态才播放：只在这一拍变形，来回切状态不该反复表演 */
watch(done, async (on) => {
  if (!on) return
  await nextTick()
  if (!orb.value) return
  await playCrystallize({ orb: orb.value, ring: ring.value, check: check.value })
})

/* 挂载时就已经完成（回显历史数据）：没有动画可播，直接给收拢后的宽度 */
onMounted(async () => {
  if (!done.value) return
  await nextTick()
  settle()
})
</script>

<template>
  <div v-if="type === 'line'" :class="['x-progress', `is-${status}`, done && 'is-done']">
    <template v-if="!done">
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
    </template>

    <div v-else ref="orb" class="x-progress-orb" role="status" aria-label="已完成">
      <svg viewBox="0 0 46 46" aria-hidden="true">
        <circle ref="ring" cx="23" cy="23" r="20" stroke-dasharray="126" />
        <path ref="check" d="m15 23.5 5.5 5.5L31.5 18" stroke-dasharray="24" />
      </svg>
    </div>
  </div>

  <div v-else :class="['x-progress-circle', `is-${status}`]" :style="{ width: `${diameter}px`, height: `${diameter}px` }">
    <svg :width="diameter" :height="diameter" :viewBox="`0 0 ${diameter} ${diameter}`" role="progressbar" :aria-valuenow="safe" aria-valuemin="0" aria-valuemax="100">
      <circle
        class="x-progress-ring-track"
        :cx="diameter / 2"
        :cy="diameter / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
      />
      <circle
        class="x-progress-ring-fill"
        :cx="diameter / 2"
        :cy="diameter / 2"
        :r="radius"
        fill="none"
        :stroke-width="strokeWidth"
        stroke-linecap="round"
        :stroke-dasharray="dash"
        :transform="`rotate(-90 ${diameter / 2} ${diameter / 2})`"
      />
    </svg>
    <span v-if="showText" class="x-progress-circle-text tnum">{{ text }}</span>
  </div>
</template>

<style scoped>
.x-progress { display: flex; align-items: center; gap: 10px; width: 100%; }
/* 完成态不再是一行「条 + 读数」，而是单个徽标：让收拢后的圆靠左落定 */
.x-progress.is-done { display: block; }
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
  transition: width .5s var(--ease-premium), background .3s var(--ease-reveal);
}
.x-progress-text { flex: none; font-size: var(--fs-sm); color: var(--ink-muted); min-width: 42px; text-align: right; }

/* 完成徽标：初始满宽（占住原来那条的位置），由 playCrystallize 收到与高度相等的正圆 */
.x-progress-orb {
  display: grid;
  place-items: center;
  width: 100%;
  height: 34px;
  overflow: hidden;
  border-radius: 999px;
  background: var(--lime);
  color: var(--ink);
}
.x-progress-orb svg { display: block; width: 88%; height: 88%; }
/* 描线三件套：无填充、圆头圆角，靠 dashoffset 一笔一笔画出来 */
.x-progress-orb circle,
.x-progress-orb path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.x-progress-circle { position: relative; display: inline-grid; place-items: center; }
.x-progress-ring-track { stroke: var(--groove-bg); }
.x-progress-ring-fill { stroke: var(--blue); transition: stroke-dasharray .5s var(--ease-premium), stroke .3s var(--ease-reveal); }
.x-progress-circle-text {
  position: absolute;
  font-size: var(--fs-lg);
  font-weight: 640;
  color: var(--ink);
}

/* success 是「走完并落定」时才形变成徽标；没到 100% 的 success 仍按条显示，
   所以这条染色要留着，否则「62% + success」会变成一条没有颜色的空槽 */
.x-progress.is-success .x-progress-fill { background: var(--lime); }
.x-progress.is-error .x-progress-fill { background: var(--red); }
.x-progress.is-warning .x-progress-fill { background: var(--cat-1-ink); }
.x-progress-circle.is-success .x-progress-ring-fill { stroke: var(--lime); }
.x-progress-circle.is-error .x-progress-ring-fill { stroke: var(--red); }
.x-progress-circle.is-warning .x-progress-ring-fill { stroke: var(--cat-1-ink); }
</style>
