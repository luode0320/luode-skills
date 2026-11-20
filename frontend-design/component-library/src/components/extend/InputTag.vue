<script setup lang="ts">
/* 标签输入：回车把当前文本收成标签，退格在空输入时删末尾，标签上的叉逐个移除。
   max 限制标签总数，allowDuplicate 控制是否允许重复值。 */
import { computed, nextTick, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { collapseOut } from '@/composables/morph'

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

const root = ref<HTMLElement | null>(null)
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
/** [参数] index 要移除的标签下标 [参数] event 点击事件（键盘删除时不传） [返回] 无
 *  先让标签收拢到 0 再改数组：直接 splice 会让元素瞬间消失，
 *  在一排标签里看不出是哪一个没了。 */
async function remove(index: number, event?: MouseEvent) {
  const el = event
    ? (event.currentTarget as HTMLElement | null)?.closest('.x-tag')
    : root.value?.querySelectorAll('.x-tag')[index] ?? null
  await collapseOut(el)
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
  <span ref="root" :class="['input-shell', 'x-tags', disabled && 'is-disabled']" @click="focusInput">
    <span v-for="(tag, i) in tags" :key="`${tag}-${i}`" class="tag x-tag">
      {{ tag }}
      <span
        v-if="!disabled"
        class="x-tag-x"
        role="button"
        :aria-label="`移除 ${tag}`"
        @click.stop="remove(i, $event)"
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
  transition: color .15s var(--ease-reveal);
}
.x-tag-x:hover { color: var(--red-text); }
</style>
