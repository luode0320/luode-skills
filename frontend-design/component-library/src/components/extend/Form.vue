<script setup lang="ts">
/* 表单容器：把「数据模型 + 校验规则 + 错误态 + 提交」这一套编排收到一处。
   字段本体仍由 Field 承担（Field 属上游冻结层，不在此改动），本组件只负责收集与派发错误：
   过去每个调用点都要自己写一遍 errors ref、调 validate、再判 Object.keys 长度为 0，
   这里把这段重复编排上提，字段通过作用域插槽拿到当前 errors。
   边界：不做异步校验、不做字段级联动、不代替后端裁决；提交动作仍由调用方处理。 */
import { ref } from 'vue'
import { validate, type Rules } from '@/utils/validate'

/** 校验结果：字段名 -> 首条错误文案，无错误时该 key 不存在 */
export interface FormErrors {
  [key: string]: string | undefined
}

const props = withDefaults(defineProps<{
  model: Record<string, unknown>
  rules?: Rules<Record<string, unknown>>
  layout?: 'vertical' | 'inline'
}>(), {
  layout: 'vertical',
})

const emit = defineEmits<{
  (e: 'submit'): void
  (e: 'invalid', errors: FormErrors): void
}>()

const errors = ref<FormErrors>({})

/** [参数] 无 [返回] 全部通过为 true；把 validate 的结果同时写入错误态供插槽读取 */
function runValidate() {
  errors.value = validate(props.model, props.rules ?? {})
  return Object.keys(errors.value).length === 0
}

/** [参数] 无 [返回] 无；先校验再决定是否上抛 submit，失败时把错误一并交回调用方 */
function submit() {
  if (runValidate()) emit('submit')
  else emit('invalid', errors.value)
}

/** [参数] 无 [返回] 无；清空错误态（表单重置后调用） */
function clear() {
  errors.value = {}
}

defineExpose({ validate: runValidate, submit, clear })
</script>

<template>
  <form class="form-grid x-form" :class="`is-${layout}`" novalidate @submit.prevent="submit">
    <slot :errors="errors" :submit="submit" :validate="runValidate" :clear="clear" />
  </form>
</template>

<style scoped>
/* 排布复用上游 components.css 的 .form-grid（两列 + .span-2 通栏），
   这样 Field 的 span/wide 在表单里继续生效，不在扩展层再造一套栅格；
   这里只补上游没有的竖排与横排两种收口。 */
.x-form.is-vertical { grid-template-columns: minmax(0, 1fr); }
.x-form.is-inline {
  grid-template-columns: none;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  align-items: start; /* 避免辅助文案把行顶高，导致两列不对齐 */
  gap: 12px;
}
</style>
