<script setup lang="ts">
/* 数字输入：左右步进按钮夹住中间输入框，越界钳制、按 precision 定小数位。
   外部值为 number | null，空输入回传 null，避免把空串混进数值域。 */
import { computed, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  modelValue?: number | null
  min?: number
  max?: number
  step?: number
  precision?: number
  disabled?: boolean
  placeholder?: string
}>(), {
  step: 1,
  precision: 0,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: number | null): void }>()

const text = ref('')

/** [参数] value 数值 [返回] 按 precision 收敛后的数值 */
function clamp(value: number): number {
  let next = value
  if (props.min !== undefined) next = Math.max(props.min, next)
  if (props.max !== undefined) next = Math.min(props.max, next)
  const p = Math.max(0, props.precision ?? 0)
  return Number(next.toFixed(p))
}

/** [返回] 展示用文本，外部值变化时同步 */
const display = computed(() => (props.modelValue === null || props.modelValue === undefined ? '' : String(props.modelValue)))

watch(display, (value) => { text.value = value }, { immediate: true })

/** [参数] value 目标值 [返回] 无 */
function commit(value: number | null) {
  if (value === null) { emit('update:modelValue', null); return }
  const next = clamp(value)
  emit('update:modelValue', next)
  text.value = String(next)
}

/** [参数] direction 步进方向，1 加 / -1 减 [返回] 无 */
function stepBy(direction: number) {
  if (props.disabled) return
  const base = props.modelValue ?? (direction > 0 ? (props.min ?? 0) : (props.max ?? 0))
  commit(base + direction * props.step)
}

/** [参数] event 输入事件 [返回] 无 */
function onInput(event: Event) {
  const raw = (event.target as HTMLInputElement).value
  text.value = raw
  if (raw.trim() === '') { emit('update:modelValue', null); return }
  const parsed = Number(raw)
  if (!Number.isNaN(parsed)) emit('update:modelValue', clamp(parsed))
}

/** [返回] 无 */
function onBlur() {
  text.value = display.value
}

/** [参数] event 键盘事件 [返回] 无 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'ArrowUp') { event.preventDefault(); stepBy(1) }
  else if (event.key === 'ArrowDown') { event.preventDefault(); stepBy(-1) }
}
</script>

<template>
  <span :class="['input-shell', 'x-num', disabled && 'is-disabled']">
    <button type="button" class="x-num-btn" :disabled="disabled" aria-label="减少" @click="stepBy(-1)">
      <Icon name="minus" :size="14" />
    </button>
    <input
      class="tnum"
      inputmode="decimal"
      :value="text"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="onInput"
      @blur="onBlur"
      @keydown="onKey"
    />
    <button type="button" class="x-num-btn" :disabled="disabled" aria-label="增加" @click="stepBy(1)">
      <Icon name="plus" :size="14" />
    </button>
  </span>
</template>

<style scoped>
.x-num { padding: 0 4px; }
.x-num input { text-align: center; }
.x-num-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  flex: none;
  border: 0;
  border-radius: var(--r-xs);
  background: transparent;
  color: var(--ink-soft);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-num-btn:hover:not(:disabled) { background: var(--hover-bg); color: var(--ink); }
.x-num-btn:disabled { opacity: .45; cursor: not-allowed; }
</style>
