<script setup lang="ts">
/* 面包屑：展示层级路径，末项是当前页，前面的项只有给了 to 才可点。
   分隔符统一用 chevronRight 图标，避免调用方自己拼字符。 */
import Icon from '@/components/Icon.vue'

export interface CrumbItem {
  label: string
  /** 目标地址，末项忽略该值 */
  to?: string
  icon?: string
}

defineProps<{ items: CrumbItem[] }>()
</script>

<template>
  <nav class="x-crumb" aria-label="面包屑">
    <template v-for="(item, i) in items" :key="`${item.label}-${i}`">
      <span v-if="i > 0" class="x-crumb-sep" aria-hidden="true">
        <Icon name="chevronRight" :size="13" />
      </span>
      <span v-if="i === items.length - 1" class="x-crumb-now" aria-current="page">
        <Icon v-if="item.icon" :name="item.icon" :size="14" />
        {{ item.label }}
      </span>
      <a v-else-if="item.to" class="x-crumb-link" :href="item.to">
        <Icon v-if="item.icon" :name="item.icon" :size="14" />
        {{ item.label }}
      </a>
      <span v-else class="x-crumb-text">
        <Icon v-if="item.icon" :name="item.icon" :size="14" />
        {{ item.label }}
      </span>
    </template>
  </nav>
</template>

<style scoped>
.x-crumb { display: flex; align-items: center; flex-wrap: wrap; gap: 6px; font-size: 13px; }
.x-crumb-sep { display: inline-flex; align-items: center; color: var(--ink-faint); }
.x-crumb-link,
.x-crumb-text,
.x-crumb-now { display: inline-flex; align-items: center; gap: 5px; }
.x-crumb-link { color: var(--ink-muted); text-decoration: none; transition: color .2s ease; }
.x-crumb-link:hover { color: var(--blue); }
.x-crumb-text { color: var(--ink-soft); }
/* 当前页不给链接语义，用正文色与字重强调，避免误点回跳 */
.x-crumb-now { color: var(--ink); font-weight: 620; }
</style>
