<script setup lang="ts">
/* 快捷入口宫格：图标 + 标题 + 分组副标题，点击上抛 key 与路径。
   视觉复用 quick-link / m-surface / lift，页面只提供条目数据。 */
import Icon from '@/components/Icon.vue'

export interface ShortcutItem {
  key: string | number
  label: string
  group: string
  icon: string
  path: string
}

defineProps<{ items: ShortcutItem[] }>()
const emit = defineEmits<{ (e: 'select', item: ShortcutItem): void }>()
</script>

<template>
  <div class="shortcut-grid">
    <button
      v-for="item in items"
      :key="item.key"
      type="button"
      class="quick-link lift m-surface"
      @click="emit('select', item)"
    >
      <span class="quick-ico m-groove"><Icon :name="item.icon" :size="17" /></span>
      <span class="quick-text">
        <span class="quick-title">{{ item.label }}</span>
        <span class="quick-sub">{{ item.group }}</span>
      </span>
      <Icon name="arrowRight" :size="15" class="quick-go" />
    </button>
  </div>
</template>
