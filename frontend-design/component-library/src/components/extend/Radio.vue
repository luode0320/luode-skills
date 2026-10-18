<script setup lang="ts">
/* 单选框：优先读最近 RadioGroup 的上下文，独立使用时退回自身 props。
   选中态画在圆形轨道上，勾上时一次落定弹入。 */
import { computed, inject, ref, watch } from 'vue'
import { settlePop } from '@/composables/motion'
import { radioGroupKey, type RadioValue } from './RadioGroup.vue'

const props = defineProps<{
  modelValue?: RadioValue
  value: RadioValue
  disabled?: boolean
  label?: string
}>()

const emit = defineEmits<{ (e: 'update:modelValue', value: RadioValue): void }>()

const group = inject(radioGroupKey, null)
const dot = ref<HTMLElement | null>(null)

/** [返回] 是否处于选中态，组内看组的选中值，独立时看自身 */
const checked = computed(() => (group ? group.modelValue.value === props.value : props.modelValue === props.value))

/** [返回] 是否禁用，组禁用与自身禁用任一成立即禁用 */
const locked = computed(() => Boolean(props.disabled) || Boolean(group?.disabled.value))

watch(checked, (on) => { if (on) settlePop(dot.value) })

/** [返回] 无 */
function pick() {
  if (locked.value) return
  if (group) group.select(props.value)
  else emit('update:modelValue', props.value)
}
</script>

<template>
  <label :class="['x-radio', checked && 'is-on', locked && 'is-disabled']">
    <input
      type="radio"
      :checked="checked"
      :disabled="locked"
      :value="String(value)"
      :aria-label="label ? undefined : '单选'"
      @change="pick"
    />
    <span class="x-radio-box">
      <span ref="dot" v-if="checked" class="x-radio-dot" />
    </span>
    <span v-if="label">{{ label }}</span>
    <slot />
  </label>
</template>

<style scoped>
.x-radio {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  font-size: 13px;
  color: var(--ink);
  user-select: none;
}
.x-radio.is-disabled { cursor: not-allowed; opacity: .5; }
.x-radio-box {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 17px;
  height: 17px;
  flex: none;
  border-radius: 999px;
  border: 1.5px solid rgba(var(--shade), .28);
  background: var(--input-bg);
  transition: background .18s ease, border-color .18s ease, box-shadow .18s ease;
}
:root[data-theme="dark"] .x-radio-box { border-color: rgba(255, 255, 255, .22); }
.x-radio:hover .x-radio-box { border-color: var(--blue); }
.x-radio.is-on .x-radio-box { background: var(--blue); border-color: var(--blue); box-shadow: 0 2px 6px var(--blue-soft); }
.x-radio-dot { width: 7px; height: 7px; border-radius: 999px; background: var(--plate-ink); }
.x-radio input { position: absolute; opacity: 0; width: 0; height: 0; }
.x-radio input:focus-visible + .x-radio-box { outline: 2px solid var(--focus); outline-offset: 2px; }
</style>
