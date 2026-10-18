<script setup lang="ts">
/* 读数条：一排并列的 Metric，带分隔线；用于概览统计。
   items 只给数值与标签，分隔与响应式换行由 readout-strip 统一下沉。 */
import Metric from '@/components/ui/Metric.vue'

export interface ReadoutItem {
  label: string
  value: number | null | undefined
  unit?: string
  decimals?: number
  alert?: boolean
}

withDefaults(defineProps<{
  items: ReadoutItem[]
}>(), {})
</script>

<template>
  <div class="readout-strip">
    <Metric
      v-for="item in items"
      :key="item.label"
      :label="item.label"
      :value="item.value"
      :unit="item.unit"
      :decimals="item.decimals"
      :class="{ 'is-alert': item.alert }"
    />
  </div>
</template>
