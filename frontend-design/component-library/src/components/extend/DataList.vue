<script setup lang="ts">
/* 数据列表：一份 data 数组 + item 插槽渲染每行，支持分割线、加载骨架与空态。
   空态复用 EmptyState，加载态用骨架行，两者互斥，避免空数据与加载中同时出现。 */
import { computed } from 'vue'
import EmptyState from '@/components/ui/EmptyState.vue'

const props = withDefaults(defineProps<{
  data: Array<Record<string, any>>
  bordered?: boolean
  size?: 'sm' | 'md' | 'lg'
  split?: boolean
  loading?: boolean
}>(), {
  size: 'md',
  split: true,
})

const rows = computed(() => props.data ?? [])
</script>

<template>
  <div :class="['x-datalist', `is-${size}`, bordered && 'is-bordered', split && 'is-split']">
    <template v-if="loading">
      <div v-for="i in 3" :key="i" class="x-datalist-row is-loading">
        <span class="skeleton x-datalist-skeleton" />
      </div>
    </template>

    <template v-else-if="rows.length">
      <div v-for="(item, index) in rows" :key="index" class="x-datalist-row">
        <slot name="item" :item="item" :index="index">{{ item }}</slot>
      </div>
    </template>

    <div v-else class="x-datalist-empty">
      <slot name="empty"><EmptyState /></slot>
    </div>
  </div>
</template>

<style scoped>
.x-datalist { display: flex; flex-direction: column; overflow: hidden; border-radius: var(--r-sm); }
.x-datalist.is-bordered { border: 1px solid var(--line); background: var(--surface); }
.x-datalist-row { padding: 10px 14px; font-size: 13px; color: var(--ink); }
.x-datalist.is-sm .x-datalist-row { padding: 7px 12px; font-size: 12px; }
.x-datalist.is-lg .x-datalist-row { padding: 14px 18px; font-size: 14px; }
.x-datalist.is-split .x-datalist-row:not(:last-child) { border-bottom: 1px solid var(--line); }
.x-datalist-row.is-loading { display: flex; align-items: center; }
.x-datalist-skeleton { height: 14px; width: 62%; border-radius: var(--r-xs); }
.x-datalist-empty { padding: 8px 0; }
</style>
