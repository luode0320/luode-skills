<script lang="ts">
/* 复选组的对外契约：子项靠 checkboxGroupKey 注入上下文，与组件的 setup 逻辑无关，
   所以放在普通 script 块里做值导出（script setup 只允许类型导出提升）。 */
import type { InjectionKey, Ref } from 'vue'

export type CheckboxValue = string | number

export interface CheckboxOption {
  label: string
  value: CheckboxValue
  disabled?: boolean
}

export interface CheckboxGroupContext {
  /** 当前已选集合（只读消费） */
  modelValue: Readonly<Ref<CheckboxValue[]>>
  /** 某个值此刻是否已选 */
  isChecked: (value: CheckboxValue) => boolean
  /** 某个值此刻是否不可改（已触达 min 或 max 边界） */
  isLocked: (value: CheckboxValue) => boolean
  /** 切换某个值的选中态，越过边界时不生效 */
  toggle: (value: CheckboxValue) => void
}

/* 插槽内的自定义子项据此注入组上下文，与组内渲染的选项共用同一份判定 */
export const checkboxGroupKey: InjectionKey<CheckboxGroupContext> = Symbol('checkboxGroup')
</script>

<script setup lang="ts">
/* 复选组：由 options 配置驱动多选，可选带一行「全选」入口（支持半选态）。
   min / max 是硬边界而不是校验提示——越界项直接不可点，用户不会先做出非法选择再被驳回。
   边界：组件只管选择集合与边界，不管业务校验与提交；options 的 label 由调用方给中文文案。 */
import { computed, provide } from 'vue'
import Checkbox from '@/components/ui/Checkbox.vue'

const props = withDefaults(defineProps<{
  modelValue?: CheckboxValue[]
  options: CheckboxOption[]
  direction?: 'horizontal' | 'vertical'
  /** 最多可选数量，达到后未选项不可再勾选 */
  max?: number
  /** 最少保留数量，达到后已选项不可再取消 */
  min?: number
  /** 是否在组头显示「全选」入口 */
  checkAll?: boolean
}>(), {
  modelValue: () => [],
  direction: 'horizontal',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: CheckboxValue[]): void
  (e: 'change', value: CheckboxValue[]): void
}>()

/** [返回] 当前已选集合，未受控时退化为空数组 */
const selected = computed(() => props.modelValue ?? [])

/** [返回] 未被单项禁用的选项，边界与全选都只在这批上计算 */
const enabled = computed(() => props.options.filter(option => !option.disabled))

/** [参数] value 待判定值 [返回] 是否已选 */
function isChecked(value: CheckboxValue): boolean {
  return selected.value.includes(value)
}

/**
 * [参数] value 待判定值
 * [返回] 该项此刻是否不可改。分两种情况：已选项在触达 min 后不能再取消，
 *         未选项在触达 max 后不能再勾选；把边界做成不可点，比事后报错更早阻断非法状态
 */
function isLocked(value: CheckboxValue): boolean {
  if (isChecked(value)) return props.min !== undefined && selected.value.length <= props.min
  return props.max !== undefined && selected.value.length >= props.max
}

/** [参数] next 新的已选集合 [返回] 无；统一出口，保证两个事件永远同步派发 */
function commit(next: CheckboxValue[]) {
  emit('update:modelValue', next)
  emit('change', next)
}

/** [参数] value 被点的值 [返回] 无；锁定项静默忽略，受控值不被越界改写 */
function toggle(value: CheckboxValue) {
  if (isLocked(value)) return
  commit(isChecked(value) ? selected.value.filter(item => item !== value) : [...selected.value, value])
}

/** [返回] 已选中的可选项数量，禁用项不计入，避免全选态被永远禁用的项卡住 */
const checkedCount = computed(() => enabled.value.filter(option => isChecked(option.value)).length)

/** [返回] 是否已全部选中 */
const allChecked = computed(() => enabled.value.length > 0 && checkedCount.value === enabled.value.length)

/** [返回] 半选：选了但不是全选，用于全选行的第三态 */
const partial = computed(() => checkedCount.value > 0 && !allChecked.value)

/** [参数] floor 需保留的已选项数 [返回] 按选项顺序截取的已选集合；按选项顺序而非点击顺序，截取结果才稳定 */
function keepFirst(floor: number): CheckboxValue[] {
  if (floor <= 0) return []
  return enabled.value.filter(option => isChecked(option.value)).slice(0, floor).map(option => option.value)
}

/** [参数] limit 目标已选数量 [返回] 在保留已有选择的前提下按选项顺序补足到上限的集合 */
function fillUpTo(limit: number): CheckboxValue[] {
  const next = [...selected.value]
  for (const option of enabled.value) {
    if (next.length >= limit) break
    if (!next.includes(option.value)) next.push(option.value)
  }
  return next
}

/** [返回] 无；已全选则退到 min 下限（无 min 即清空），否则补到 max 上限（无 max 即全选） */
function toggleAll() {
  if (allChecked.value) {
    commit(keepFirst(props.min ?? 0))
    return
  }
  commit(fillUpTo(props.max ?? enabled.value.length))
}

provide(checkboxGroupKey, {
  modelValue: computed(() => selected.value),
  isChecked,
  isLocked,
  toggle,
})
</script>

<template>
  <div :class="['x-checkbox-group', `is-${direction}`]" role="group">
    <Checkbox
      v-if="checkAll && enabled.length"
      class="x-checkbox-all"
      :model-value="allChecked"
      :indeterminate="partial"
      :label="allChecked ? '取消全选' : '全选'"
      @update:model-value="toggleAll"
    />
    <Checkbox
      v-for="option in options"
      :key="option.value"
      :model-value="isChecked(option.value)"
      :disabled="option.disabled || isLocked(option.value)"
      :label="option.label"
      @update:model-value="toggle(option.value)"
    />
    <slot />
  </div>
</template>

<style scoped>
.x-checkbox-group { display: flex; }
.x-checkbox-group.is-horizontal { flex-direction: row; flex-wrap: wrap; align-items: center; gap: 16px; }
.x-checkbox-group.is-vertical { flex-direction: column; align-items: flex-start; gap: 10px; }
/* 全选行是组级动作，与各选项之间补一条线拉开层级，避免被当成普通选项 */
.x-checkbox-group.is-horizontal .x-checkbox-all { padding-right: 16px; border-right: 1px solid var(--line); }
.x-checkbox-group.is-vertical .x-checkbox-all { padding-bottom: 10px; border-bottom: 1px solid var(--line); align-self: stretch; }
</style>
