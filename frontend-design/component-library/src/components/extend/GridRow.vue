<script setup lang="ts">
/* 栅格行：24 栅格制的 flex 轨道容器，横纵两个方向各有一份间距。
   行只负责提供 gutter 给子列，列自己用 padding 半宽撑出沟槽，
   因此外层不会出现负 margin 溢出，调用方直接嵌即可。 */
import { computed, provide } from 'vue'

const props = withDefaults(defineProps<{
  gutter?: number | [number, number]
  justify?: 'start' | 'center' | 'end' | 'space-between' | 'space-around'
  align?: 'start' | 'center' | 'end' | 'stretch'
  wrap?: boolean
}>(), {
  gutter: 0,
  justify: 'start',
  align: 'stretch',
  wrap: true,
})

/** gutter 归一成 [水平, 垂直]，单值时两轴同宽 */
const gaps = computed<[number, number]>(() => (
  Array.isArray(props.gutter) ? props.gutter : [props.gutter, 0]
))

provide('xGridGutter', gaps)

const style = computed(() => ({
  rowGap: `${gaps.value[1]}px`,
}))
</script>

<template>
  <div
    :class="[
      'x-row',
      `is-justify-${justify}`,
      `is-align-${align}`,
      wrap && 'is-wrap',
    ]"
    :style="style"
  >
    <slot />
  </div>
</template>

<style scoped>
/* 横向 gutter 由子列 padding 撑出，所以行自身不带 column-gap，避免双倍间距 */
.x-row { display: flex; box-sizing: border-box; min-width: 0; }
.x-row.is-wrap { flex-wrap: wrap; }
.x-row.is-justify-start { justify-content: flex-start; }
.x-row.is-justify-center { justify-content: center; }
.x-row.is-justify-end { justify-content: flex-end; }
.x-row.is-justify-space-between { justify-content: space-between; }
.x-row.is-justify-space-around { justify-content: space-around; }
.x-row.is-align-start { align-items: flex-start; }
.x-row.is-align-center { align-items: center; }
.x-row.is-align-end { align-items: flex-end; }
.x-row.is-align-stretch { align-items: stretch; }
</style>
