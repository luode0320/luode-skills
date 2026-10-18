<script setup lang="ts">
/* 栅格列：24 栅格制，span 决定占比，offset 前置留白，push / pull 做顺序视觉交换。
   响应式断点不用 JS 监听窗口：基数列宽写成内联样式，各断点的覆盖值挂成 CSS 变量，
   media query 命中时才把变量抬上来，因此缩放窗口零重排开销。
   断点回退方向是从小到大逐档覆盖，未声明的档位沿用更小档位的值。 */
import { computed, inject, type ComputedRef } from 'vue'

const props = withDefaults(defineProps<{
  span?: number
  offset?: number
  push?: number
  pull?: number
  xs?: number
  sm?: number
  md?: number
  lg?: number
  xl?: number
}>(), {
  span: 24,
})

const gaps = inject<ComputedRef<[number, number]>>('xGridGutter', computed(() => [0, 0] as [number, number]))

/** [参数] span 栅格数 [返回] 换算出的百分比字符串，超出 0-24 一律夹回合法区间 */
function percentOf(span: number) {
  return `${(Math.min(Math.max(span, 0), 24) / 24) * 100}%`
}

const style = computed(() => {
  const half = gaps.value[0] / 2
  return {
    flex: `0 0 ${percentOf(props.span)}`,
    maxWidth: percentOf(props.span),
    marginLeft: props.offset ? percentOf(props.offset) : undefined,
    left: props.push ? percentOf(props.push) : undefined,
    right: props.pull ? percentOf(props.pull) : undefined,
    paddingLeft: `${half}px`,
    paddingRight: `${half}px`,
    /* 各断点的覆盖值；没传就不写变量，该断点沿用更小档位的列宽 */
    '--col-xs': props.xs === undefined ? undefined : percentOf(props.xs),
    '--col-sm': props.sm === undefined ? undefined : percentOf(props.sm),
    '--col-md': props.md === undefined ? undefined : percentOf(props.md),
    '--col-lg': props.lg === undefined ? undefined : percentOf(props.lg),
    '--col-xl': props.xl === undefined ? undefined : percentOf(props.xl),
  }
})
</script>

<template>
  <div class="x-col" :style="style">
    <slot />
  </div>
</template>

<style scoped>
.x-col { position: relative; box-sizing: border-box; min-width: 0; }

/* ≥576：优先 sm，两者都缺省时交回 auto，让基数列宽继续生效 */
@media (min-width: 576px) {
  .x-col { flex-basis: var(--col-sm, var(--col-xs, auto)); max-width: var(--col-sm, var(--col-xs, none)); }
}
/* ≥820：库内既有断点，md 覆盖更小档位 */
@media (min-width: 820px) {
  .x-col { flex-basis: var(--col-md, var(--col-sm, var(--col-xs, auto))); max-width: var(--col-md, var(--col-sm, var(--col-xs, none))); }
}
/* ≥992：lg 档 */
@media (min-width: 992px) {
  .x-col { flex-basis: var(--col-lg, var(--col-md, var(--col-sm, var(--col-xs, auto)))); max-width: var(--col-lg, var(--col-md, var(--col-sm, var(--col-xs, none)))); }
}
/* ≥1200：最大档 xl */
@media (min-width: 1200px) {
  .x-col { flex-basis: var(--col-xl, var(--col-lg, var(--col-md, var(--col-sm, var(--col-xs, auto))))); max-width: var(--col-xl, var(--col-lg, var(--col-md, var(--col-sm, var(--col-xs, none))))); }
}
</style>
