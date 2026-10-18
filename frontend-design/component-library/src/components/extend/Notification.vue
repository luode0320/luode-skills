<script setup lang="ts">
/* 通知卡片：单条展示型，只负责一条通知的排版与关闭。
   堆叠、计时与进出场由宿主（如 ToastHost）负责，这里不做队列。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'
import IconButton from '@/components/ui/IconButton.vue'

const props = withDefaults(defineProps<{
  type?: 'info' | 'success' | 'warning' | 'error'
  title?: string
  message?: string
  closable?: boolean
  showIcon?: boolean
}>(), {
  type: 'info',
  showIcon: true,
})

const emit = defineEmits<{ (e: 'close'): void }>()

/* 四型各自的图标：信息圆点、成功打勾、警告三角、失败禁用圈 */
const ICONS = { info: 'info', success: 'check', warning: 'alert', error: 'ban' } as const

/** [参数] 无 [返回] 当前语义对应的图标名 */
const iconName = computed(() => ICONS[props.type])
</script>

<template>
  <article :class="['x-notify', 'm-float', `is-${type}`]" role="status">
    <span class="x-notify-bar" aria-hidden="true" />
    <Icon v-if="showIcon" class="x-notify-ico" :name="iconName" :size="17" :stroke="2" />
    <div class="x-notify-body">
      <div v-if="title" class="x-notify-title">{{ title }}</div>
      <div v-if="message" class="x-notify-msg">{{ message }}</div>
      <slot />
    </div>
    <IconButton v-if="closable" class="x-notify-close" name="x" label="关闭通知" small @click="emit('close')" />
  </article>
</template>

<style scoped>
.x-notify {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  width: 100%;
  max-width: 360px;
  padding: 13px 12px 13px 16px;
  border-radius: var(--r-md);
  overflow: hidden;
  color: var(--ink);
}
/* 左缘语义色条：比整块染色克制，也不影响深色态的对比度 */
.x-notify-bar {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  width: 3px;
  background: var(--blue);
}
.x-notify-ico { flex: none; margin-top: 1px; color: var(--blue); }
.x-notify-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 4px; }
.x-notify-title { font-size: 13px; font-weight: 640; color: var(--ink); }
.x-notify-msg { font-size: 13px; line-height: 1.6; color: var(--ink-muted); }
.x-notify-close { margin: -2px -3px 0 0; }

.x-notify.is-success .x-notify-bar { background: var(--lime); }
.x-notify.is-success .x-notify-ico { color: var(--leaf-text); }
.x-notify.is-warning .x-notify-bar { background: var(--cat-1-ink); }
.x-notify.is-warning .x-notify-ico { color: var(--cat-1-ink); }
.x-notify.is-error .x-notify-bar { background: var(--red); }
.x-notify.is-error .x-notify-ico { color: var(--red-text); }
</style>
