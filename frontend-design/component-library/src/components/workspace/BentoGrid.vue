<script setup lang="ts">
/* 工作台网格：12 列自适应栅格容器，卡片按 BentoCard 的 span 语义落位。
   窄屏断点由 pages.css 统一下沉，组件侧不再重复声明。 */
</script>

<template>
  <div class="bento-grid">
    <slot />
  </div>
</template>
