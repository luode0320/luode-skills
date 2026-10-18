<script setup lang="ts">
/* 骨架屏：loading 为 true 时按 type / rows 渲染占位块，否则渲染 default 插槽。
   占位块复用全局 .skeleton 微光底，尺寸只由 width / height / type 决定。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  loading?: boolean
  animation?: boolean
  rows?: number
  type?: 'text' | 'image' | 'circle' | 'rect'
  width?: number | string
  height?: number | string
}>(), {
  loading: true,
  animation: true,
  rows: 1,
  type: 'text',
})

/** [参数] 数值转 px，字符串原样透传 [返回] 合法 CSS 长度 */
function size(value?: number | string) {
  if (value === undefined) return undefined
  return typeof value === 'number' ? `${value}px` : value
}

/** [参数] 无 [返回] 单块骨架的尺寸，text 默认铺满宽、其余按 type 给默认 */
const blockStyle = computed(() => {
  const w = size(props.width)
  const h = size(props.height)
  if (props.type === 'circle' || props.type === 'image') {
    const side = w ?? h ?? (props.type === 'circle' ? '40px' : '120px')
    return { width: side, height: h ?? side, borderRadius: props.type === 'circle' ? '9999px' : 'var(--r-sm)' }
  }
  return {
    width: w ?? '100%',
    height: h ?? (props.type === 'rect' ? '80px' : '14px'),
    borderRadius: props.type === 'rect' ? 'var(--r-sm)' : 'var(--r-xs)',
  }
})

/** [参数] 无 [返回] text 类型需要重复的行数，其余类型固定一块 */
const count = computed(() => (props.type === 'text' ? Math.max(1, props.rows) : 1))

/** [参数] 第 i 行 [返回] 末行收窄到 62%，制造自然段落感 */
function rowStyle(i: number) {
  if (props.type !== 'text' || count.value < 2) return blockStyle.value
  return { ...blockStyle.value, width: i === count.value - 1 ? '62%' : blockStyle.value.width }
}
</script>

<template>
  <div v-if="loading" :class="['x-skeleton', !animation && 'is-static']" aria-busy="true" aria-live="polite">
    <span v-for="i in count" :key="i" class="skeleton" :style="rowStyle(i - 1)" />
  </div>
  <slot v-else />
</template>

<style scoped>
.x-skeleton { display: flex; flex-direction: column; gap: 10px; }
.x-skeleton.is-static .skeleton { animation: none; }
</style>
