<script lang="ts">
/* 单选组的对外契约：Radio 依赖 radioGroupKey 注入上下文，独立于组件的 setup 逻辑，
   所以放在普通 script 块里做值导出（script setup 只允许类型导出提升）。 */
import type { InjectionKey, Ref } from 'vue'

export type RadioValue = string | number | boolean

export interface RadioGroupContext {
  /** 当前选中值（只读消费） */
  modelValue: Readonly<Ref<RadioValue | undefined>>
  /** 整组是否禁用（只读消费） */
  disabled: Readonly<Ref<boolean>>
  /** 选中某个值 */
  select: (value: RadioValue) => void
}

/* Radio 据此注入组上下文；无 group 时 Radio 回落到自身 props */
export const radioGroupKey: InjectionKey<RadioGroupContext> = Symbol('radioGroup')
</script>

<script setup lang="ts">
/* 单选组：把选中值与禁用态注入给子 Radio，方向由 direction 决定横排或竖排。 */
import { computed, provide } from 'vue'

const props = withDefaults(defineProps<{
  modelValue: RadioValue
  disabled?: boolean
  direction?: 'horizontal' | 'vertical'
}>(), {
  direction: 'horizontal',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: RadioValue): void }>()

/** [参数] value 被选中的值 [返回] 无 */
function select(value: RadioValue) {
  if (props.disabled) return
  emit('update:modelValue', value)
}

provide(radioGroupKey, {
  modelValue: computed(() => props.modelValue),
  disabled: computed(() => Boolean(props.disabled)),
  select,
})
</script>

<template>
  <div :class="['x-radio-group', `is-${direction}`]" role="radiogroup">
    <slot />
  </div>
</template>

<style scoped>
.x-radio-group { display: flex; gap: 16px; }
.x-radio-group.is-horizontal { flex-direction: row; flex-wrap: wrap; align-items: center; }
.x-radio-group.is-vertical { flex-direction: column; align-items: flex-start; gap: 10px; }
</style>
