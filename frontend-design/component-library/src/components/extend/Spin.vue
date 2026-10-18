<script setup lang="ts">
/* 加载中：只渲染一个转圈，或用 wrapper 在内容上叠一层遮罩。
   转圈复用全局 .spinner（currentColor 描边），这里只负责尺寸与语义色。 */
withDefaults(defineProps<{
  loading?: boolean
  size?: 'sm' | 'md' | 'lg'
  tip?: string
  /** 包裹内容时遮罩 */
  wrapper?: boolean
}>(), {
  loading: true,
  size: 'md',
})
</script>

<template>
  <div v-if="wrapper" class="x-spin-wrap">
    <slot />
    <div v-if="loading" :class="['x-spin-mask', `is-${size}`]" role="status" aria-live="polite">
      <span class="x-spin-ring spinner" aria-hidden="true" />
      <span v-if="tip" class="x-spin-tip">{{ tip }}</span>
      <span v-else class="sr-only">加载中</span>
    </div>
  </div>

  <div v-else-if="loading" :class="['x-spin', `is-${size}`]" role="status" aria-live="polite">
    <span class="x-spin-ring spinner" aria-hidden="true" />
    <span v-if="tip" class="x-spin-tip">{{ tip }}</span>
    <span v-else class="sr-only">加载中</span>
  </div>
</template>

<style scoped>
/* 独立转圈：横向排布，tip 落在圈右侧 */
.x-spin { display: inline-flex; align-items: center; gap: 8px; color: var(--blue); }
.x-spin .x-spin-ring { width: 18px; height: 18px; }
.x-spin.is-sm .x-spin-ring { width: 14px; height: 14px; border-width: 1.5px; }
.x-spin.is-lg .x-spin-ring { width: 24px; height: 24px; border-width: 2.5px; }
.x-spin-tip { font-size: 13px; color: var(--ink-muted); }

/* 包裹态：内容保留布局，遮罩绝对定位压在内容上。
   最近修改时间：2026-10-18 18:20:00；改动原因：遮罩底色用的是 --overlay（浅色主题下只有
   .26 透明度的淡色遮罩），文字与转圈却取 --plate-ink / --plate-soft（深色盘专用的浅色），
   浅字压浅底实测对比度只有 1.46，提示文字基本读不出。改用随主题翻转的 --ink / --ink-muted：
   浅色主题是深字压淡遮罩，深色主题是浅字压深遮罩，两侧都成立。 */
.x-spin-wrap { position: relative; }
.x-spin-mask {
  position: absolute;
  inset: 0;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  border-radius: var(--r-sm);
  background: var(--overlay);
  backdrop-filter: blur(2px);
  -webkit-backdrop-filter: blur(2px);
  color: var(--ink);
}
.x-spin-mask .x-spin-ring { width: 22px; height: 22px; }
.x-spin-mask.is-sm .x-spin-ring { width: 16px; height: 16px; border-width: 1.5px; }
.x-spin-mask.is-lg .x-spin-ring { width: 30px; height: 30px; border-width: 2.5px; }
.x-spin-mask .x-spin-tip { color: var(--ink-muted); }
</style>
