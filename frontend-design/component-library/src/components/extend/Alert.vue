<script setup lang="ts">
/* 提示条：页内静态提示，四型语义色 + 可关闭。
   图标与配色由 type 单点派生，调用方只选语义，不自己拼颜色。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'
import IconButton from '@/components/ui/IconButton.vue'

const props = withDefaults(defineProps<{
  type?: 'info' | 'success' | 'warning' | 'error'
  title?: string
  closable?: boolean
  showIcon?: boolean
  banner?: boolean
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
  <div :class="['x-alert', `is-${type}`, banner && 'is-banner']" role="alert">
    <Icon v-if="showIcon" class="x-alert-ico" :name="iconName" :size="16" :stroke="2" />
    <div class="x-alert-body">
      <div v-if="title" class="x-alert-title">{{ title }}</div>
      <div v-if="$slots.default" class="x-alert-desc"><slot /></div>
    </div>
    <IconButton v-if="closable" class="x-alert-close" name="x" label="关闭" small @click="emit('close')" />
  </div>
</template>

<style scoped>
.x-alert {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 12px 14px;
  border-radius: var(--r-sm);
  border: 1px solid transparent;
  background: var(--blue-soft);
  color: var(--ink);
}
/* 通栏：贴边展开，去掉圆角与左右描边 */
.x-alert.is-banner {
  border-radius: 0;
  border-inline: 0;
  padding: 10px 16px;
}
.x-alert-ico { flex: none; margin-top: 1px; color: var(--blue); }
.x-alert-body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: 3px; }
.x-alert-title { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-alert-desc { font-size: 13px; line-height: 1.6; color: var(--ink-muted); }
/* 关闭键压到首行文字基线附近，避免把整条撑高 */
.x-alert-close { margin: -3px -4px 0 0; }

.x-alert.is-info { background: var(--blue-soft); }
.x-alert.is-info .x-alert-ico { color: var(--blue); }
.x-alert.is-success { background: var(--lime-soft); }
.x-alert.is-success .x-alert-ico { color: var(--leaf-text); }
.x-alert.is-warning { background: var(--cat-1-bg); }
.x-alert.is-warning .x-alert-ico { color: var(--cat-1-ink); }
.x-alert.is-error { background: var(--red-soft); }
.x-alert.is-error .x-alert-ico { color: var(--red-text); }
</style>
