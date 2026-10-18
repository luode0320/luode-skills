<script setup lang="ts">
/* 评论：头像 + 作者 + 时间 + 正文，底部动作条可点或走 actions 插槽。
   正文可用 default 插槽整段替换，动作可用 actions 插槽自定义。 */
import Avatar from '@/components/ui/Avatar.vue'

withDefaults(defineProps<{
  author?: string
  avatar?: string
  content?: string
  datetime?: string
  actions?: string[]
}>(), {
  author: '',
  content: '',
  datetime: '',
  actions: () => [],
})
</script>

<template>
  <article class="x-comment">
    <div class="x-comment-avatar">
      <img v-if="avatar" :src="avatar" :alt="author" class="x-comment-photo" />
      <Avatar v-else :name="author" :size="34" />
    </div>
    <div class="x-comment-main">
      <header class="x-comment-head">
        <span class="x-comment-author">{{ author }}</span>
        <span v-if="datetime" class="x-comment-time faint">{{ datetime }}</span>
      </header>
      <div class="x-comment-body">
        <slot>{{ content }}</slot>
      </div>
      <footer v-if="$slots.actions || actions.length" class="x-comment-actions">
        <slot name="actions">
          <button v-for="a in actions" :key="a" type="button" class="x-comment-action btn-text">{{ a }}</button>
        </slot>
      </footer>
    </div>
  </article>
</template>

<style scoped>
.x-comment { display: flex; gap: 10px; padding: 4px 0; }
.x-comment-avatar { flex: none; }
.x-comment-photo { width: 34px; height: 34px; border-radius: 9999px; object-fit: cover; }
.x-comment-main { display: flex; flex-direction: column; gap: 5px; min-width: 0; flex: 1; }
.x-comment-head { display: flex; align-items: baseline; gap: 8px; min-width: 0; }
.x-comment-author { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-comment-time { font-size: 11px; }
.x-comment-body { font-size: 13px; line-height: 1.62; color: var(--ink-muted); overflow-wrap: anywhere; }
.x-comment-actions { display: flex; align-items: center; gap: 14px; }
.x-comment-action {
  padding: 0;
  border: 0;
  background: transparent;
  font: inherit;
  font-size: 12px;
  color: var(--ink-soft);
  cursor: pointer;
  transition: color var(--ease-premium) .22s;
}
.x-comment-action:hover { color: var(--blue); }
</style>
