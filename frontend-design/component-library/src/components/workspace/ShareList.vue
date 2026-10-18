<script setup lang="ts">
/* 占比条列表：横向条形 + 数值，用于「数据权限分布」这类按数量排序的构成展示。
   颜色取自 cat-1..5 分类令牌，按序号循环；条形宽度按最大值归一，避免小项不可见。 */
import { computed } from 'vue'

export interface ShareItem {
  label: string
  value: number
}

const props = withDefaults(defineProps<{
  items: ShareItem[]
  unit?: string
}>(), {
  unit: '',
})

/* 宽度按最大值归一（不是按总和），让各项相对大小可比 */
const rows = computed(() => {
  const max = Math.max(1, ...props.items.map((i) => i.value))
  const total = props.items.reduce((a, b) => a + b.value, 0) || 1
  return props.items.map((item, index) => ({
    ...item,
    cat: (index % 5) + 1,
    width: (item.value / max) * 100,
    pct: Math.round((item.value / total) * 100),
  }))
})
</script>

<template>
  <ul class="share-list">
    <li v-for="row in rows" :key="row.label" :class="`cat-${row.cat}`">
      <span class="share-label">{{ row.label }}</span>
      <span class="share-track"><i :style="{ width: `${row.width}%` }" /></span>
      <span class="share-value tnum">{{ row.value }}<small v-if="unit"> {{ unit }}</small><small> · {{ row.pct }}%</small></span>
    </li>
  </ul>
</template>
