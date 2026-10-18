<script setup lang="ts">
/* 级联选择面板：Cascader 里被下拉触发器包住的那部分，抽出来后可独立嵌进页面
   （例如侧栏筛选、表单内联区、抽屉里的多列联动），不依赖任何浮层定位与关外逻辑。
   面板自身只维护「草稿路径」，点上级列会截断其后的路径再追加，
   因此改上层必然使下层已选失效——这一步由截断保证，不需要额外清理失效项。
   末级（无 children）点击即落定并上抛 change，中间层只更新草稿，
   让调用方能在未选完时拿到稳定的中间态。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'

/** 级联选项：children 自引用构成任意层数，无 children 即末级 */
export interface CascaderPanelOption {
  label: string
  value: string | number
  disabled?: boolean
  children?: CascaderPanelOption[]
}

const props = withDefaults(defineProps<{
  options: CascaderPanelOption[]
  /** 已选路径值数组，逐层对应；受控用法下由外部回写 */
  modelValue?: Array<string | number>
  /** 每列宽度（px） */
  columnWidth?: number
  /** 每列最大高度（px），超出纵向滚动 */
  maxHeight?: number
}>(), {
  modelValue: () => [],
  columnWidth: 152,
  maxHeight: 300,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: Array<string | number>): void
  (e: 'change', value: Array<string | number>): void
}>()

/** [参数] 无 [返回] 按当前路径展开的各级列数据，末级后不再续列 */
const columns = computed(() => {
  const cols: CascaderPanelOption[][] = [props.options]
  let list = props.options
  for (const value of props.modelValue) {
    const node = list.find(option => option.value === value)
    if (!node?.children?.length) break
    cols.push(node.children)
    list = node.children
  }
  return cols
})

/** [参数] 无 [返回] 每列的固定尺寸，列宽与限高统一由 props 下发，各列口径一致 */
const columnStyle = computed(() => ({
  width: `${props.columnWidth}px`,
  maxHeight: `${props.maxHeight}px`,
}))

/**
 * [参数] option 被点中的选项
 * [参数] depth 该选项所在列序号
 * [返回] 无；截断当前路径到该列后写入选中值
 *         路径一变就上抛 change，调用方既能拿中间层也能拿末级，不必再自己判层
 */
function pick(option: CascaderPanelOption, depth: number) {
  if (option.disabled) return
  const next = [...props.modelValue.slice(0, depth), option.value]
  emit('update:modelValue', next)
  emit('change', next)
}
</script>

<template>
  <div class="x-cascader-panel" role="group" aria-label="级联选择">
    <div
      v-for="(column, depth) in columns"
      :key="depth"
      class="x-cascader-col"
      role="listbox"
      :style="columnStyle"
    >
      <div
        v-for="option in column"
        :key="option.value"
        role="option"
        :aria-selected="modelValue[depth] === option.value"
        :aria-disabled="option.disabled || undefined"
        :class="['x-cascader-option', modelValue[depth] === option.value && 'is-active', option.disabled && 'is-disabled']"
        @click="pick(option, depth)"
      >
        <span class="x-cascader-label">{{ option.label }}</span>
        <Icon v-if="option.children?.length" name="chevronRight" :size="14" class="x-cascader-caret" />
        <Icon v-else-if="modelValue[depth] === option.value" name="check" :size="14" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.x-cascader-panel {
  display: flex;
  min-width: 0;
  border-radius: var(--r-md);
  overflow-x: auto;
  overscroll-behavior: contain;
}
.x-cascader-col { flex: none; overflow-y: auto; overscroll-behavior: contain; }
/* 分隔线只画在列之间，首列不留线，避免面板外沿多出一道描边 */
.x-cascader-col:not(:first-child) { border-left: 1px solid var(--line); }
.x-cascader-option {
  display: flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  cursor: pointer;
  transition: background var(--ease-premium) .2s, color var(--ease-premium) .2s;
}
.x-cascader-option:hover { background: var(--hover-bg); }
.x-cascader-option.is-active { background: var(--blue-soft); color: var(--blue); font-weight: 620; }
.x-cascader-option.is-disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-cascader-option:focus-visible { outline: 2px solid var(--focus); outline-offset: -2px; }
.x-cascader-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-cascader-caret { flex: none; color: var(--ink-faint); }
</style>
