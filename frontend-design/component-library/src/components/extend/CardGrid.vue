<script setup lang="ts">
/* 卡片网格：把若干张卡按固定列数排布，列宽等分、间距统一。
   列数走 CSS 变量下发，窄屏降列只用媒体查询改这一个变量，
   不必在 JS 里做宽度探测——降列是版式问题，交给样式层更稳。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  /** 宽屏下的列数，窄屏由样式层逐档下调 */
  columns?: number
  /** 卡片之间的横纵间距（px） */
  gutter?: number
}>(), {
  columns: 3,
  gutter: 16,
})

/** 列数与间距合成一份自定义属性，模板只挂一次 style */
const style = computed(() => ({
  '--x-card-cols': String(Math.max(1, props.columns)),
  '--x-card-gutter': `${Math.max(0, props.gutter)}px`,
}))
</script>

<template>
  <div class="x-card-grid" :style="style">
    <slot />
  </div>
</template>

<style scoped>
.x-card-grid {
  display: grid;
  grid-template-columns: repeat(var(--x-card-cols, 3), minmax(0, 1fr));
  gap: var(--x-card-gutter, 16px);
  align-items: stretch;
  min-width: 0;
}
/* 降列只改列数变量，卡片自身不需要知道当前是几列 */
@media (max-width: 1080px) {
  .x-card-grid { grid-template-columns: repeat(min(var(--x-card-cols, 3), 2), minmax(0, 1fr)); }
}
@media (max-width: 720px) {
  .x-card-grid { grid-template-columns: minmax(0, 1fr); }
}
</style>
