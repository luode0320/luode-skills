<script setup lang="ts">
/* 分割线：横向分隔段落、纵向分隔并排区块，可带文字居中或靠左靠右。
   虚线只换线型不改颜色，间距走 margin 口径，避免调用方手写 magic number。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  direction?: 'horizontal' | 'vertical'
  orientation?: 'left' | 'right' | 'center'
  dashed?: boolean
  margin?: number | string
}>(), {
  direction: 'horizontal',
  orientation: 'center',
})

/** 把 number 补成 px，字符串原样透传，允许调用方传百分比等相对单位 */
const gap = computed(() => {
  if (props.margin === undefined) return undefined
  return typeof props.margin === 'number' ? `${props.margin}px` : props.margin
})
</script>

<template>
  <div
    v-if="direction === 'horizontal'"
    :class="['x-divider', `is-${orientation}`, dashed && 'is-dashed']"
    :style="gap === undefined ? undefined : { marginBlock: gap }"
    role="separator"
    aria-orientation="horizontal"
  >
    <span v-if="$slots.default" class="x-divider-text"><slot /></span>
  </div>
  <span
    v-else
    :class="['x-divider-vertical', dashed && 'is-dashed']"
    :style="gap === undefined ? undefined : { marginInline: gap }"
    role="separator"
    aria-orientation="vertical"
  />
</template>

<style scoped>
/* 横向：带文字时两端各补一根线，文字夹在中间；无线时用 :has 撤掉本体横线 */
.x-divider {
  display: flex;
  align-items: center;
  gap: 12px;
  border-top: 1px solid var(--line-strong);
}
.x-divider.is-dashed { border-top-style: dashed; }
.x-divider.is-center::before,
.x-divider.is-center::after,
.x-divider.is-left::after,
.x-divider.is-right::before {
  content: '';
  flex: 1;
  height: 1px;
  background: var(--line-strong);
}
/* 无文字时整条线由本体 border-top 承担，伪元素退出，避免出现两截断线 */
.x-divider:not(:has(.x-divider-text))::before,
.x-divider:not(:has(.x-divider-text))::after { content: none; }
/* 有文字时线由伪元素补，横线本体撤掉 */
.x-divider:has(.x-divider-text) { border-top: none; }
.x-divider.is-left::before { display: none; }
.x-divider.is-right::after { display: none; }
.x-divider.is-dashed:has(.x-divider-text)::before,
.x-divider.is-dashed:has(.x-divider-text)::after {
  background: repeating-linear-gradient(to right, var(--line-strong) 0 4px, transparent 4px 8px);
}
.x-divider-text {
  font-size: 12px;
  color: var(--ink-soft);
  white-space: nowrap;
}
/* 纵向：一根竖线，靠自身高度撑开，用 margin 与相邻内容拉开距离 */
.x-divider-vertical {
  display: inline-block;
  width: 0;
  align-self: stretch;
  min-height: 1em;
  border-left: 1px solid var(--line-strong);
  vertical-align: middle;
}
.x-divider-vertical.is-dashed { border-left-style: dashed; }
</style>
