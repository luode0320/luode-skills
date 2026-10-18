<script setup lang="ts">
/* 定义列表（Descriptions）：详情页/订单页常见的「一组字段标签—值」只读卡片，
   支持多列排布、跨列长内容、带边框表格态与竖排（标签在上、值在下）。
   之所以独立于 KeyValueReadout（无边框横向读数）与 SpecPlate（深色单列铭牌），
   是因为这两者都不做「可跨列 + 带边框 + 标题带额外操作」的详情列表形态。
   边界：只读展示，不含编辑；项由 data 配置驱动，不另建子组件，避免第二套真相源。 */
import { computed } from 'vue'

export interface DescriptionItem {
  label: string
  value?: string | number | null
  /** 该项横跨的列数，默认 1；用于备注等长文本独占整行 */
  span?: number
}

const props = withDefaults(defineProps<{
  data: DescriptionItem[]
  title?: string
  column?: number
  bordered?: boolean
  layout?: 'horizontal' | 'vertical'
}>(), {
  column: 3,
  bordered: false,
  layout: 'horizontal',
})

/* span 需夹到列数内，否则跨列超出会让整行塌陷；模板沙箱不含 Math，故在此算好 */
const items = computed(() => props.data.map((item) => ({
  ...item,
  colSpan: Math.min(Math.max(item.span ?? 1, 1), props.column),
})))
</script>

<template>
  <section class="x-desc" :class="[bordered && 'is-bordered', `is-${layout}`]" :aria-label="title">
    <header v-if="title || $slots.extra" class="x-desc-head">
      <h3 v-if="title" class="x-desc-title">{{ title }}</h3>
      <div v-if="$slots.extra" class="x-desc-extra"><slot name="extra" /></div>
    </header>
    <dl class="x-desc-body" :style="{ gridTemplateColumns: `repeat(${column}, minmax(0, 1fr))` }">
      <div
        v-for="(item, i) in items"
        :key="`${item.label}-${i}`"
        class="x-desc-item"
        :style="{ gridColumn: `span ${item.colSpan}` }"
      >
        <dt class="x-desc-label">{{ item.label }}</dt>
        <dd class="x-desc-value">{{ item.value ?? '—' }}</dd>
      </div>
    </dl>
  </section>
</template>

<style scoped>
.x-desc { min-width: 0; }
.x-desc-head { display: flex; align-items: center; justify-content: space-between; gap: 12px; margin-bottom: 10px; }
.x-desc-title { margin: 0; font-size: 14px; font-weight: 650; color: var(--ink); letter-spacing: -.01em; }
.x-desc-extra { flex: none; display: flex; align-items: center; gap: 8px; }

/* 栅格主体：列数由内联 style 决定，行间距靠 gap，跨列项用 gridColumn span */
.x-desc-body { display: grid; gap: 2px 20px; margin: 0; min-width: 0; }

/* 横排：标签与值同一行，标签占固定宽、值占剩余 */
.x-desc.is-horizontal .x-desc-item { display: grid; grid-template-columns: auto 1fr; gap: 10px; align-items: baseline; min-width: 0; }
.x-desc.is-horizontal .x-desc-value { justify-self: start; }
/* 竖排：标签在上、值在下 */
.x-desc.is-vertical .x-desc-item { display: flex; flex-direction: column; gap: 2px; min-width: 0; }

.x-desc-label { font-size: 13px; color: var(--ink-muted); white-space: nowrap; }
.x-desc-value { margin: 0; font-size: 13px; color: var(--ink); min-width: 0; overflow-wrap: anywhere; }

/* 带边框表格态：单元格铺实色、格间留 1px 缝露出容器底色成线，
   这样跨列项的分隔线自动对齐，不需要按「每行几项」假设 nth-child。 */
.x-desc.is-bordered .x-desc-body {
  gap: 1px;
  border: 1px solid var(--line);
  border-radius: var(--r-md);
  overflow: hidden;
  background: var(--line);
}
.x-desc.is-bordered .x-desc-item { padding: 9px 14px; background: var(--surface); }
.x-desc.is-bordered .x-desc-label { color: var(--ink-muted); }
/* 横排带边框时把标签列刷成浅槽底，与值列拉开层次 */
.x-desc.is-bordered.is-horizontal .x-desc-item { grid-template-columns: minmax(72px, auto) 1fr; gap: 14px; align-items: stretch; }
.x-desc.is-bordered.is-horizontal .x-desc-label { align-self: stretch; display: flex; align-items: center; }
</style>
