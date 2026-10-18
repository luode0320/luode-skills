<script setup lang="ts">
/* 工作台卡片：主次布局的基本单元。span 决定栅格占位（复用 pages.css 的 bento-* 变体），
   glow 开启指针跟随高光层，title 走 SectionLabel，右侧工具区放 tools 插槽。 */
import SectionLabel from '@/components/ui/SectionLabel.vue'
import { trackGlow } from '@/composables/motion'

withDefaults(defineProps<{
  span?: 'hero' | 'side' | 'third' | 'wide' | 'narrow' | 'half' | 'full'
  title?: string
  meta?: string
  glow?: boolean
}>(), {
  span: 'third',
  glow: false,
})
</script>

<template>
  <section :class="['bento', `bento-${span}`, glow && 'm-glow']" @pointermove="glow ? trackGlow($event) : undefined">
    <span v-if="glow" class="glow-layer" aria-hidden="true" />
    <div :class="span === 'hero' ? 'hero-head' : 'bento-head'">
      <SectionLabel v-if="title" :title="title" />
      <slot name="tools">
        <span v-if="meta" class="bento-meta">{{ meta }}</span>
      </slot>
    </div>
    <slot />
  </section>
</template>
