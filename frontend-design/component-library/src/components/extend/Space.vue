<script setup lang="ts">
/* 间距：给一组子项之间垫出统一距离，方向与对齐由一行 flex 决定。
   用 gap 而不是逐个包 margin，子项自身不需要知道相邻是谁，追加删减都不错位。
   split 时在相邻子项之间补一条细线，线由 flex 排布自动落在两子项正中。 */
import { computed, useSlots, Comment, Fragment, type VNode } from 'vue'

const props = withDefaults(defineProps<{
  direction?: 'horizontal' | 'vertical'
  size?: 'sm' | 'md' | 'lg' | number
  align?: 'start' | 'center' | 'end' | 'baseline'
  wrap?: boolean
  split?: boolean
}>(), {
  direction: 'horizontal',
  size: 'md',
  align: 'center',
  wrap: false,
})

const slots = useSlots()

/* 三档语义间距，数值走固定阶梯，与其它组件的疏密口径一致 */
const sizes: Record<string, number> = { sm: 8, md: 12, lg: 20 }

const gapPx = computed(() => (typeof props.size === 'number' ? props.size : sizes[props.size] ?? 12))

/**
 * [参数] 无
 * [返回] 展开后的子节点数组，已剔除条件渲染留下的注释占位；
 *         多子节点会被包进 Fragment，拆开才能逐项插线。
 */
const children = computed<VNode[]>(() => {
  const out: VNode[] = []
  ;(slots.default?.() ?? []).forEach((node) => {
    if (node.type === Comment) return
    if (node.type === Fragment) (node.children as VNode[]).forEach(child => out.push(child))
    else out.push(node)
  })
  return out
})

const style = computed(() => ({ gap: `${gapPx.value}px` }))
</script>

<template>
  <div
    :class="[
      'x-space',
      `is-${direction}`,
      `is-align-${align}`,
      wrap && 'is-wrap',
      split && 'is-split',
    ]"
    :style="style"
  >
    <template v-if="split">
      <template v-for="(node, i) in children" :key="i">
        <component :is="node" />
        <span v-if="i < children.length - 1" class="x-space-split" aria-hidden="true" />
      </template>
    </template>
    <slot v-else />
  </div>
</template>

<style scoped>
.x-space { display: flex; box-sizing: border-box; min-width: 0; }
.x-space.is-horizontal { flex-direction: row; }
.x-space.is-vertical { flex-direction: column; }
.x-space.is-wrap { flex-wrap: wrap; }
.x-space.is-align-start { align-items: flex-start; }
.x-space.is-align-center { align-items: center; }
.x-space.is-align-end { align-items: flex-end; }
.x-space.is-align-baseline { align-items: baseline; }
/* 拆分线：横排竖线靠自身高度撑开，纵排横线拉满容器宽度 */
.x-space-split { flex: none; background: var(--line-strong); }
.x-space.is-horizontal .x-space-split { width: 1px; align-self: stretch; min-height: 1em; }
.x-space.is-vertical .x-space-split { height: 1px; align-self: stretch; }
</style>
