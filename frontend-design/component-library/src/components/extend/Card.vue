<script setup lang="ts">
/* 通用卡片：header / body / footer 三区，外加可选的顶部封面。
   与 Panel 的分工是 Panel 只承载一段读数内容，Card 要容纳封面、副标题与底部操作，
   因此三区各自独立判空——任一区没有内容时该区整块不渲染，避免留下空白条。
   loading 只替换主体，标题与底部操作保留，让加载中的卡片仍能表意。 */
import Skeleton from './Skeleton.vue'

withDefaults(defineProps<{
  title?: string
  subtitle?: string
  /** 关闭描边后仍保留玻璃阅读面，只把边框收掉，不影响尺寸 */
  bordered?: boolean
  /** 开启后指针悬停抬升一级阴影，用于可点击的卡片 */
  hoverable?: boolean
  /** 主体区改为骨架占位 */
  loading?: boolean
}>(), {
  bordered: true,
  hoverable: false,
  loading: false,
})
</script>

<template>
  <section :class="['x-card', 'm-surface', !bordered && 'is-borderless', hoverable && 'is-hoverable']">
    <div v-if="$slots.cover" class="x-card-cover"><slot name="cover" /></div>
    <header v-if="title || subtitle || $slots.extra" class="x-card-head">
      <div class="x-card-titles">
        <h3 v-if="title" class="x-card-title">{{ title }}</h3>
        <p v-if="subtitle" class="x-card-subtitle">{{ subtitle }}</p>
      </div>
      <div v-if="$slots.extra" class="x-card-extra"><slot name="extra" /></div>
    </header>
    <div class="x-card-body">
      <Skeleton v-if="loading" :rows="3" />
      <slot v-else />
    </div>
    <footer v-if="$slots.footer" class="x-card-footer"><slot name="footer" /></footer>
  </section>
</template>

<style scoped>
.x-card {
  display: flex;
  flex-direction: column;
  min-width: 0;
  border-radius: var(--r-lg);
  overflow: hidden;
  transition: box-shadow var(--ease-premium) .28s, transform var(--ease-premium) .28s;
}
/* 无描边态：只撤掉边框颜色，保留 1px 占位，避免与有描边卡片并排时高度差 2px */
.x-card.is-borderless { border-color: transparent; }
@media (hover: hover) {
  .x-card.is-hoverable:hover { box-shadow: var(--edge), var(--e2); transform: translateY(-2px); }
}
.x-card-cover { line-height: 0; }
.x-card-cover :deep(img) { width: 100%; display: block; object-fit: cover; }

.x-card-head {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 15px 18px 0;
  min-width: 0;
}
.x-card-titles { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; }
.x-card-title { font-size: 14px; font-weight: 650; letter-spacing: -.01em; color: var(--ink); }
.x-card-subtitle { font-size: 12px; color: var(--ink-soft); }
.x-card-extra { flex: none; display: flex; align-items: center; gap: 6px; }

.x-card-body { padding: 13px 18px 16px; min-width: 0; font-size: 13px; color: var(--ink-muted); line-height: 1.62; }
/* 有头或封面时主体顶部已由上方补足间距，这里只留正常内边距 */
.x-card-head + .x-card-body { padding-top: 10px; }

.x-card-footer {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  border-top: 1px solid var(--line);
  font-size: 13px;
  color: var(--ink-soft);
}
</style>
