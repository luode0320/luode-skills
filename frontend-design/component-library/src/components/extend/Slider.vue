<script setup lang="ts">
/* 滑块：原生 <input type="range"> 作无障碍底座，视觉轨道与滑块叠在其上。
   range 模式用两个 range 输入并排，各自管一端，保证键盘与读屏两段都可操作。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: number | [number, number]
  min?: number
  max?: number
  step?: number
  disabled?: boolean
  showTicks?: boolean
  range?: boolean
}>(), {
  min: 0,
  max: 100,
  step: 1,
  modelValue: 0,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: number | [number, number]): void }>()

/* 区间端点：range 取数组，否则单值 */
const lowValue = computed(() => (props.range ? (props.modelValue as [number, number])[0] : (props.modelValue as number)))
const highValue = computed(() => (props.range ? (props.modelValue as [number, number])[1] : (props.modelValue as number)))

const span = computed(() => Math.max(1, props.max - props.min))

/**
 * [参数] value 原始值
 * [返回] 归一化后的 0-100 百分比，用于轨道几何
 */
function percentOf(value: number): number {
  return ((value - props.min) / span.value) * 100
}

const lowPercent = computed(() => Math.min(100, Math.max(0, percentOf(lowValue.value))))
const highPercent = computed(() => Math.min(100, Math.max(0, percentOf(highValue.value))))

/* 已选区间的左右两端：单值滑到左端起，range 取两值之间 */
const fillLeft = computed(() => (props.range ? lowPercent.value : 0))
const fillWidth = computed(() => Math.max(0, highPercent.value - fillLeft.value))

/* 刻度值：步长均匀分布时的候选点 */
const ticks = computed(() => {
  if (!props.showTicks) return []
  const total = (props.max - props.min) / props.step
  if (total > 20) return []
  const list: number[] = []
  for (let i = 0; i <= total; i += 1) list.push(props.min + i * props.step)
  return list
})

/**
 * [参数] event 输入事件 [返回] 无：单值模式回写数值
 */
function onInput(event: Event) {
  const next = Number((event.target as HTMLInputElement).value)
  if (props.range) return
  emit('update:modelValue', next)
}

/**
 * [参数] event 输入事件 which 'low' | 'high' 移动的是哪一端
 * [返回] 无：range 模式把两端夹成不交叉的数组回写
 */
function onRangeInput(event: Event, which: 'low' | 'high') {
  const next = Number((event.target as HTMLInputElement).value)
  const [lo, hi] = props.modelValue as [number, number]
  /* 两端互相挤压时把另一端推着走，避免出现 low > high */
  if (which === 'low') emit('update:modelValue', [Math.min(next, hi), hi])
  else emit('update:modelValue', [lo, Math.max(next, lo)])
}
</script>

<template>
  <div :class="['x-slider', disabled && 'is-disabled']">
    <div class="x-slider-rail">
      <div class="x-slider-fill" :style="{ left: `${fillLeft}%`, width: `${fillWidth}%` }" />
      <span
        v-for="t in ticks"
        :key="t"
        class="x-slider-tick"
        :style="{ left: `${percentOf(t)}%` }"
        aria-hidden="true"
      />
    </div>
    <!-- 单值：一个原生 range 铺满轨道 -->
    <input
      v-if="!range"
      class="x-slider-input"
      type="range"
      :min="min"
      :max="max"
      :step="step"
      :value="modelValue as number"
      :disabled="disabled"
      aria-label="滑块"
      @input="onInput"
    />
    <!-- 区间：两个 range 叠加，各自的拇指端点透明，命中区只在拇指附近 -->
    <template v-else>
      <input
        class="x-slider-input is-range"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        :value="lowValue"
        :disabled="disabled"
        aria-label="区间下限"
        @input="onRangeInput($event, 'low')"
      />
      <input
        class="x-slider-input is-range is-upper"
        type="range"
        :min="min"
        :max="max"
        :step="step"
        :value="highValue"
        :disabled="disabled"
        aria-label="区间上限"
        @input="onRangeInput($event, 'high')"
      />
      <span class="x-slider-thumb" :style="{ left: `${lowPercent}%` }" aria-hidden="true" />
      <span class="x-slider-thumb is-upper" :style="{ left: `${highPercent}%` }" aria-hidden="true" />
    </template>
    <span v-if="!range" class="x-slider-thumb" :style="{ left: `${highPercent}%` }" aria-hidden="true" />
    <span class="x-slider-value tnum">
      {{ range ? `${lowValue} – ${highValue}` : modelValue }}
    </span>
  </div>
</template>

<style scoped>
.x-slider { position: relative; display: flex; align-items: center; gap: 12px; min-height: 32px; }
.x-slider.is-disabled { opacity: .5; }
.x-slider-rail {
  position: relative;
  flex: 1;
  height: 6px;
  border-radius: 999px;
  background: var(--groove-bg);
  box-shadow: var(--groove-inset);
}
.x-slider-fill {
  position: absolute;
  top: 0;
  height: 100%;
  border-radius: 999px;
  background: var(--blue);
  transition: left .12s ease, width .12s ease;
}
.x-slider-tick {
  position: absolute;
  top: 50%;
  width: 2px;
  height: 8px;
  margin-left: -1px;
  transform: translateY(-50%);
  border-radius: 999px;
  background: var(--line-strong);
}
/* 原生 range 铺满且透明：拇指与轨道由视觉层负责，交互仍归原生 */
.x-slider-input {
  position: absolute;
  left: 0;
  right: 0;
  width: calc(100% - 56px);
  height: 32px;
  margin: 0;
  background: transparent;
  appearance: none;
  -webkit-appearance: none;
  cursor: pointer;
}
.x-slider-input.is-range { width: 100%; pointer-events: none; }
.x-slider-input.is-range::-webkit-slider-thumb { pointer-events: auto; }
.x-slider-input::-webkit-slider-thumb {
  appearance: none;
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 999px;
  border: 2px solid var(--blue);
  background: var(--surface-solid);
  box-shadow: var(--e1);
  cursor: pointer;
}
.x-slider-input::-moz-range-thumb {
  width: 16px;
  height: 16px;
  border: 2px solid var(--blue);
  border-radius: 999px;
  background: var(--surface-solid);
  box-shadow: var(--e1);
  cursor: pointer;
}
.x-slider-input:focus-visible { outline: none; }
.x-slider-input:focus-visible::-webkit-slider-thumb { outline: 2px solid var(--focus); outline-offset: 2px; }
.x-slider-input::-moz-range-track { background: transparent; }
.x-slider-thumb {
  position: absolute;
  top: 50%;
  width: 16px;
  height: 16px;
  margin-left: -8px;
  transform: translateY(-50%);
  border-radius: 999px;
  border: 2px solid var(--blue);
  background: var(--surface-solid);
  box-shadow: var(--e1);
  transition: left .12s ease;
}
.x-slider-value { flex: none; min-width: 44px; text-align: right; font-size: 12px; font-weight: 620; color: var(--ink-muted); }
</style>
