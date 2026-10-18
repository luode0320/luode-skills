<script setup lang="ts">
/* 动态列表：头像 + 主文 + 时间 + 右侧标记，用于「最近登录」这类流水。
   items 只提供数据，行的视觉与分隔线由组件统一承担，页面不再手写 activity 结构。 */
import Avatar from '@/components/ui/Avatar.vue'
import Tag from '@/components/ui/Tag.vue'

export interface ActivityItem {
  who: string
  target: string
  time: string
  ok?: boolean
}

withDefaults(defineProps<{
  items: ActivityItem[]
  avatarSize?: number
}>(), {
  avatarSize: 30,
})
</script>

<template>
  <div class="activity-list">
    <div v-for="(item, index) in items" :key="index" class="activity">
      <Avatar :name="item.who" :size="avatarSize" />
      <div class="activity-main">
        <div class="ellipsis"><b>{{ item.who }}</b> <span class="muted">{{ item.target }}</span></div>
        <div class="faint mono-time">{{ item.time }}</div>
      </div>
      <Tag :tone="item.ok === false ? 'danger' : 'ok'" dot>{{ item.ok === false ? '失败' : '成功' }}</Tag>
    </div>
  </div>
</template>
