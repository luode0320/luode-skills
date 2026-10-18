<script setup lang="ts">
/* 键值读数组：主卡与刻度环旁的「峰值 / 均值 / 范围」小表。
   columns 决定列数（默认 3），值为数字时自动套等宽数字字形。 */
export interface ReadoutRow {
  label: string
  value: string | number
}

withDefaults(defineProps<{
  rows: ReadoutRow[]
  columns?: number
}>(), {
  columns: 3,
})
</script>

<template>
  <dl class="hero-readouts" :style="{ gridTemplateColumns: `repeat(${columns}, auto)` }">
    <div v-for="row in rows" :key="row.label">
      <dt>{{ row.label }}</dt>
      <dd :class="{ tnum: typeof row.value === 'number' }">{{ row.value }}</dd>
    </div>
  </dl>
</template>
