<script setup lang="ts">
/* 链接文字：语义色 + 可选下划线，禁用态降级为纯文本，无 href 时退化为 span。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  href?: string
  target?: '_blank' | '_self'
  disabled?: boolean
  underline?: boolean
  type?: 'default' | 'primary' | 'success' | 'warning' | 'danger'
}>(), {
  target: '_self',
  type: 'primary',
})

/** [参数] 无 [返回] 禁用时渲染为 span，否则渲染为 a */
const tag = computed(() => (props.disabled || !props.href ? 'span' : 'a'))
</script>

<template>
  <component
    :is="tag"
    :class="['x-link', `tone-${type}`, underline && 'is-underline', disabled && 'is-disabled']"
    :href="disabled ? undefined : href"
    :target="tag === 'a' ? target : undefined"
    :rel="tag === 'a' && target === '_blank' ? 'noopener noreferrer' : undefined"
    :aria-disabled="disabled || undefined"
  >
    <slot />
  </component>
</template>

<style scoped>
.x-link {
  color: var(--blue);
  text-decoration: none;
  cursor: pointer;
  transition: color var(--ease-premium) .22s;
}
.x-link:hover { color: var(--blue-hover); }
.x-link.is-underline { text-decoration: underline; text-underline-offset: 3px; }
.x-link.tone-default { color: var(--ink-muted); }
.x-link.tone-default:hover { color: var(--ink); }
.x-link.tone-success { color: var(--leaf-text); }
.x-link.tone-warning { color: var(--cat-1-ink); }
.x-link.tone-danger { color: var(--red-text); }
.x-link.tone-danger:hover { color: var(--red); }
.x-link.is-disabled { color: var(--ink-faint); cursor: not-allowed; text-decoration: none; }
</style>
