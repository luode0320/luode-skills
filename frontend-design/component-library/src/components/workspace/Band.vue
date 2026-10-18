<script setup lang="ts">
/* 横带分层容器：监控页与详情页的整块分区（Stacked Bands）。
   title 走 SectionLabel，右侧工具区放 tools 插槽；空态用 empty 插槽占位。 */
import SectionLabel from '@/components/ui/SectionLabel.vue'

withDefaults(defineProps<{
  title?: string
  reveal?: boolean
}>(), {
  reveal: true,
})
</script>

<template>
  <section :class="['band', reveal && 'reveal']">
    <div class="band-head">
      <SectionLabel v-if="title" :title="title" />
      <slot name="tools" />
    </div>
    <slot />
  </section>
</template>
