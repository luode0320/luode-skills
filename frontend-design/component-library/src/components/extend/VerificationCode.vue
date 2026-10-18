<script setup lang="ts">
/* 验证码输入：定长数字格，逐格输入自动跳格，退格回跳，支持整串粘贴。
   输入过程用 tabular-nums 保证数字不跳动；完成后自动聚焦到最后一格。 */
import { computed, nextTick, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: string
  length?: number
  disabled?: boolean
  invalid?: boolean
  /** 仅允许数字；关掉后可输入字母用于邮箱验证码 */
  numeric?: boolean
  placeholder?: string
  autofocus?: boolean
}>(), {
  length: 6,
  numeric: true,
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'complete', value: string): void
}>()

const cells = ref<HTMLInputElement[]>([])
const active = ref(0)

const digits = computed(() => {
  const raw = props.modelValue ?? ''
  return Array.from({ length: props.length }, (_, i) => raw[i] ?? '')
})

const pattern = computed(() => (props.numeric ? /\D/g : /\s/g))

function setCellRef(el: Element | null, index: number) {
  if (el) cells.value[index] = el as HTMLInputElement
}

/* 把整串写回并推进焦点；越界时停在末格，避免焦点飞出组件 */
function commit(raw: string) {
  const value = raw.replace(pattern.value, '').slice(0, props.length)
  emit('update:modelValue', value)
  const next = Math.min(value.length, props.length - 1)
  active.value = next
  nextTick(() => cells.value[next]?.focus())
  if (value.length === props.length) emit('complete', value)
}

/* 单格输入：把该位并入整串，其余位保持不变 */
function onInput(event: Event, index: number) {
  const el = event.target as HTMLInputElement
  const chars = el.value.replace(pattern.value, '')
  if (!chars) return
  const current = digits.value.slice()
  current[index] = chars[0]
  el.value = chars[0]
  commit(current.join('').replace(/\s/g, ''))
}

/* 退格：本格有值先清本格，本格已空则回退并清上一格 */
function onBackspace(index: number) {
  const current = digits.value.slice()
  if (current[index]) {
    current[index] = ''
    emit('update:modelValue', current.join(''))
    return
  }
  if (index === 0) return
  current[index - 1] = ''
  emit('update:modelValue', current.join(''))
  active.value = index - 1
  nextTick(() => cells.value[index - 1]?.focus())
}

function onPaste(event: ClipboardEvent) {
  const text = event.clipboardData?.getData('text') ?? ''
  if (!text) return
  event.preventDefault()
  commit(text)
}

function onArrow(index: number, step: number) {
  const next = Math.min(Math.max(index + step, 0), props.length - 1)
  active.value = next
  cells.value[next]?.focus()
}

watch(() => props.modelValue, (value) => {
  if ((value ?? '').length === props.length) active.value = props.length - 1
})

defineExpose({ focus: () => cells.value[Math.min(active.value, props.length - 1)]?.focus() })
</script>

<template>
  <div :class="['x-vcode', invalid && 'is-invalid', disabled && 'is-disabled']" role="group" aria-label="验证码输入">
    <input
      v-for="(char, i) in digits"
      :key="i"
      :ref="(el) => setCellRef(el as Element | null, i)"
      class="x-vcode-cell"
      type="text"
      inputmode="numeric"
      autocomplete="one-time-code"
      maxlength="1"
      :value="char"
      :disabled="disabled"
      :placeholder="i === 0 ? placeholder : undefined"
      :aria-label="`第 ${i + 1} 位验证码`"
      :aria-invalid="invalid || undefined"
      @input="onInput($event, i)"
      @keydown.backspace.prevent="onBackspace(i)"
      @keydown.left.prevent="onArrow(i, -1)"
      @keydown.right.prevent="onArrow(i, 1)"
      @paste="onPaste"
      @focus="active = i"
    />
  </div>
</template>

<style scoped>
.x-vcode { display: inline-flex; gap: 8px; }
.x-vcode-cell {
  width: var(--control-h);
  height: var(--control-h);
  padding: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--r-xs);
  background: var(--input-bg);
  box-shadow: var(--edge);
  color: var(--ink);
  font-family: var(--font-mono);
  font-size: 16px;
  font-weight: 640;
  font-variant-numeric: tabular-nums;
  text-align: center;
  outline: none;
  transition: border-color var(--ease-premium) .2s, box-shadow var(--ease-premium) .2s, background var(--ease-premium) .2s;
}
.x-vcode-cell::placeholder { font-size: 12px; font-weight: 400; color: var(--ink-faint); }
.x-vcode-cell:focus {
  border-color: transparent;
  background: var(--surface-solid);
  box-shadow: 0 0 0 2px var(--focus);
}
.x-vcode.is-invalid .x-vcode-cell { border-color: var(--red); }
.x-vcode.is-invalid .x-vcode-cell:focus { box-shadow: 0 0 0 2px var(--red-soft); }
.x-vcode.is-disabled { opacity: .5; }
.x-vcode.is-disabled .x-vcode-cell { cursor: not-allowed; }
</style>
