<script setup lang="ts">
/* 时间轴：由 items 数据派生节点，左侧 / 右侧 / 交替三种排布，可反向。
   每个节点复用 TimelineItem 的表现，保证单独使用与批量渲染口径一致。 */
import { computed } from 'vue'
import TimelineItem from './TimelineItem.vue'

export interface TimelineEntry {
  label?: string
  content?: string
  time?: string
  color?: string
  dot?: string
}

const props = withDefaults(defineProps<{
  items: TimelineEntry[]
  mode?: 'left' | 'right' | 'alternate'
  reverse?: boolean
}>(), {
  mode: 'left',
})

const list = computed(() => (props.reverse ? [...props.items].reverse() : props.items))
</script>

<template>
  <ul :class="['x-timeline', `is-${mode}`]">
    <TimelineItem
      v-for="(item, i) in list"
      :key="i"
      :label="item.label"
      :content="item.content"
      :time="item.time"
      :color="item.color"
      :dot="item.dot"
      :class="mode === 'alternate' && i % 2 === 1 && 'is-flip'"
    />
  </ul>
</template>

<style scoped>
.x-timeline { display: flex; flex-direction: column; margin: 0; padding: 0; list-style: none; }
/* 竖线由子项统一绘制，父级只负责交替模式下的左右镜像 */
.x-timeline.is-alternate :deep(.x-timeline-item) { width: 50%; }
.x-timeline.is-alternate :deep(.x-timeline-item.is-flip) { align-self: flex-end; }
</style>
