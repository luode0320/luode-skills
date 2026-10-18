<script setup lang="ts">
/* 卡片元信息区：头像 + 标题 + 描述的一行横排，供 Card 主体或列表项复用。
   avatar 属性只负责传名字走默认头像；要用图片或自定义图形时走 avatar 插槽，
   两者同时存在以插槽优先，避免调用方在两个入口之间来回猜哪个生效。 */
import Avatar from '@/components/ui/Avatar.vue'

withDefaults(defineProps<{
  title?: string
  description?: string
  /** 传给默认头像的显示名，非图片地址 */
  avatar?: string
}>(), {
  title: '',
  description: '',
  avatar: '',
})
</script>

<template>
  <div class="x-card-meta">
    <div v-if="$slots.avatar || avatar" class="x-card-meta-avatar">
      <slot name="avatar">
        <Avatar :name="avatar" :size="36" />
      </slot>
    </div>
    <div class="x-card-meta-main">
      <div class="x-card-meta-title">
        <slot name="title">{{ title }}</slot>
      </div>
      <div v-if="$slots.description || description" class="x-card-meta-desc">
        <slot name="description">{{ description }}</slot>
      </div>
    </div>
  </div>
</template>

<style scoped>
.x-card-meta { display: flex; align-items: center; gap: 11px; min-width: 0; }
.x-card-meta-avatar { flex: none; display: flex; }
.x-card-meta-main { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }
.x-card-meta-title { font-size: 14px; font-weight: 620; color: var(--ink); }
.x-card-meta-desc { font-size: 12px; color: var(--ink-soft); line-height: 1.55; }
</style>
