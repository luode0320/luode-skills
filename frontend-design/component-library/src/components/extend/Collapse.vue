<script setup lang="ts">
/* 折叠面板：以 modelValue 数组承载展开项，accordion 下互斥展开。
   子项通过 provide 与本组件通信，高度过渡由 CSS grid-template-rows 0fr/1fr 驱动。 */
import { provide, reactive, toRef, watch } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: string[]
  accordion?: boolean
  bordered?: boolean
  expandIconPosition?: 'left' | 'right'
}>(), {
  modelValue: () => [],
  expandIconPosition: 'left',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string[]): void }>()

const opened = reactive(new Set<string>(props.modelValue))
/** 外部改写 modelValue 时回灌本地集合，保证受控用法下展开态不脱节 */
watch(() => props.modelValue, (v) => {
  const next = v ?? []
  if (next.length === opened.size && next.every(n => opened.has(n))) return
  opened.clear()
  next.forEach(n => opened.add(n))
})

/** [参数] 无 [返回] 把本地集合派发成新的数组，避免外部直接改数组 */
function sync() {
  emit('update:modelValue', Array.from(opened))
}

/** [参数] name 面板标识 [返回] 当前是否展开 */
function isOpen(name: string) {
  return opened.has(name)
}

/** [参数] name 面板标识 [返回] 切换展开态；accordion 时清空后再只保留该面板 */
function toggle(name: string) {
  if (opened.has(name)) {
    opened.delete(name)
  } else {
    if (props.accordion) opened.clear()
    opened.add(name)
  }
  sync()
}

provide('xCollapse', {
  isOpen,
  toggle,
  iconPosition: toRef(props, 'expandIconPosition'),
})
</script>

<template>
  <div :class="['x-collapse', bordered && 'is-bordered']">
    <slot />
  </div>
</template>

<style scoped>
.x-collapse { display: flex; flex-direction: column; border-radius: var(--r-sm); }
.x-collapse.is-bordered {
  border: 1px solid var(--line);
  overflow: hidden;
  background: var(--surface);
  box-shadow: var(--e1);
}
.x-collapse.is-bordered :deep(.x-collapse-item:not(:last-child)) { border-bottom: 1px solid var(--line); }
</style>
