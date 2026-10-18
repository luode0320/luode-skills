<script setup lang="ts">
/* 标签输入：回车把当前文本收成标签，退格在空输入时删末尾，标签上的叉逐个移除。
   max 限制标签总数，allowDuplicate 控制是否允许重复值。 */
import { computed, nextTick, ref } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  modelValue?: string[]
  placeholder?: string
  max?: number
  disabled?: boolean
  allowDuplicate?: boolean
}>(), {
  placeholder: '',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string[]): void }>()

const input = ref<HTMLInputElement | null>(null)
const draft = ref('')

/** [返回] 当前标签数组 */
const tags = computed(() => props.modelValue ?? [])

/** [返回] 是否已达标签数量上限 */
const full = computed(() => props.max !== undefined && tags.value.length >= props.max)

/** [返回] 无 */
function commit() {
  const value = draft.value.trim()
  if (!value || full.value) { draft.value = ''; return }
  if (!props.allowDuplicate && tags.value.includes(value)) { draft.value = ''; return }
  emit('update:modelValue', [...tags.value, value])
  draft.value = ''
}

/** [参数] event 键盘事件 [返回] 无 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Enter') {
    event.preventDefault()
    commit()
  } else if (event.key === 'Backspace' && !draft.value && tags.value.length) {
    remove(tags.value.length - 1)
  }
}

/** [参数] index 被移除标签的下标 [返回] 无 */
function remove(index: number) {
  const next = tags.value.slice()
  next.splice(index, 1)
  emit('update:modelValue', next)
}

/** [返回] 无 */
function focusInput() {
  nextTick(() => input.value?.focus())
}
</script>

<template>
  <span :class="['input-shell', 'x-tags', disabled && 'is-disabled']" @click="focusInput">
    <span v-for="(tag, i) in tags" :key="`${tag}-${i}`" class="tag x-tag">
      {{ tag }}
      <span
        v-if="!disabled"
        class="x-tag-x"
        role="button"
        :aria-label="`移除 ${tag}`"
        @click.stop="remove(i)"
      ><Icon name="x" :size="12" /></span>
    </span>
    <input
      ref="input"
      v-model="draft"
      :placeholder="tags.length ? '' : placeholder"
      :disabled="disabled || full"
      @keydown="onKey"
      @blur="commit"
    />
  </span>
</template>

<style scoped>
.x-tags {
  height: auto;
  min-height: var(--control-h);
  flex-wrap: wrap;
  gap: 6px;
  padding: 5px 10px;
  cursor: text;
}
.x-tags input { flex: 1; min-width: 60px; height: 26px; }
.x-tag { height: 24px; }
.x-tag-x {
  display: inline-flex;
  align-items: center;
  color: var(--ink-faint);
  cursor: pointer;
  transition: color .15s ease;
}
.x-tag-x:hover { color: var(--red-text); }
</style>
