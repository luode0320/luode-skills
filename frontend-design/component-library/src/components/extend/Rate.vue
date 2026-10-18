<script setup lang="ts">
/* 评分：五角星按整数或半星打分，hover 预览、点击定值、再点同一值得可清空。
   星星是自绘 SVG（实心填充走 currentColor），不引图标库，避免描边星在选中态显脏。 */
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: number
  count?: number
  allowHalf?: boolean
  readonly?: boolean
  disabled?: boolean
  allowClear?: boolean
}>(), {
  count: 5,
  modelValue: 0,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: number): void }>()

/* 五角星路径：外顶点半径 9、内顶点半径 3.6，围绕画布中心 10,10 展开 */
const STAR_PATH = 'M10 1.6 12.47 6.6 17.99 7.4 14 11.3 14.94 16.8 10 14.2 5.06 16.8 6.01 11.3 2.01 7.4 7.53 6.6Z'

const hover = ref<number | null>(null)

/* 显示值优先取预览值；非只读且未悬停时回落到绑定值 */
const shown = computed(() => (hover.value !== null ? hover.value : (props.modelValue ?? 0)))

/**
 * [参数] index 星序号，half 是否落在左半区
 * [返回] 该星应得的分数（1 / 0.5 / 0）
 */
function scoreAt(index: number, half: boolean): number {
  const value = shown.value
  const base = index + 1
  if (value >= base) return 1
  if (props.allowHalf && value >= base - 0.5) return half ? 1 : 0.5
  return 0
}

/**
 * [参数] event 指针事件
 * [返回] 指针落点对应的分数（整数或半值）
 */
function valueOf(event: PointerEvent): number {
  const target = event.currentTarget as HTMLElement
  const rect = target.getBoundingClientRect()
  let ratio = (event.clientX - rect.left) / rect.width
  ratio = Math.min(1, Math.max(0, ratio))
  const index = Number(target.dataset.index ?? 0)
  const half = props.allowHalf && ratio < 0.5
  return index + (half ? 0.5 : 1)
}

/** [参数] event 指针移动事件 [返回] 无：写入预览分 */
function onMove(event: PointerEvent) {
  if (props.readonly || props.disabled) return
  hover.value = valueOf(event)
}

/** [参数] 无 [返回] 无：清掉 hover 预览 */
function onLeave() {
  hover.value = null
}

/** [参数] event 点击事件 [返回] 无：定值，命中当前值且可清空时归零；同时清除 hover 预览态 */
function pick(event: PointerEvent) {
  if (props.readonly || props.disabled) return
  const next = valueOf(event)
  hover.value = null // 立即清除预览态，让 shown 回落到真实绑定值，点击后立即上色
  emit('update:modelValue', props.allowClear && next === props.modelValue ? 0 : next)
}

/** [参数] 无 [返回] 无：键盘增减，左右方向键步长为半或一 */
function onKey(event: KeyboardEvent) {
  if (props.readonly || props.disabled) return
  const step = props.allowHalf ? 0.5 : 1
  const current = props.modelValue ?? 0
  if (event.key === 'ArrowRight' || event.key === 'ArrowUp') {
    event.preventDefault()
    emit('update:modelValue', Math.min(props.count, current + step))
  } else if (event.key === 'ArrowLeft' || event.key === 'ArrowDown') {
    event.preventDefault()
    emit('update:modelValue', Math.max(0, current - step))
  }
}
</script>

<template>
  <div
    :class="['x-rate', disabled && 'is-disabled', readonly && 'is-readonly']"
    role="slider"
    :aria-valuemin="0"
    :aria-valuemax="count"
    :aria-valuenow="modelValue ?? 0"
    aria-label="评分"
    :tabindex="readonly || disabled ? -1 : 0"
    @pointermove="onMove"
    @pointerleave="onLeave"
    @keydown="onKey"
  >
    <button
      v-for="i in count"
      :key="i"
      type="button"
      :class="['x-star', scoreAt(i - 1, false) === 1 && 'is-full', scoreAt(i - 1, false) === 0.5 && 'is-half']"
      :data-index="i - 1"
      :disabled="disabled || readonly"
      :aria-label="`${i} 星`"
      @click="pick"
    >
      <!-- 底槽星：未点亮的描边；stroke-width 改细避免渲染为小圆环 -->
      <svg class="x-star-track" viewBox="0 0 20 20" aria-hidden="true">
        <path :d="STAR_PATH" fill="none" stroke="currentColor" stroke-width="0.8" stroke-linejoin="round" />
      </svg>
      <!-- 实心星：满值全亮，半星用 50% 宽的裁剪窗口露出左半 -->
      <svg
        v-if="scoreAt(i - 1, false) > 0"
        class="x-star-fill"
        :class="scoreAt(i - 1, false) === 0.5 && 'is-half'"
        viewBox="0 0 20 20"
        aria-hidden="true"
      >
        <path :d="STAR_PATH" fill="currentColor" />
      </svg>
    </button>
    <span v-if="modelValue" class="x-rate-value tnum">{{ modelValue }}</span>
  </div>
</template>

<style scoped>
.x-rate { display: inline-flex; align-items: center; gap: 4px; }
.x-rate.is-disabled { opacity: .5; }
.x-rate:focus-visible { outline: 2px solid var(--focus); outline-offset: 3px; border-radius: var(--r-xs); }
.x-star {
  position: relative;
  display: inline-flex;
  width: 24px;
  height: 24px;
  padding: 0;
  color: var(--ink-faint);
  transition: color .18s ease, transform .18s ease;
}
.x-rate:not(.is-readonly):not(.is-disabled) .x-star { cursor: pointer; }
.x-rate:not(.is-readonly):not(.is-disabled) .x-star:hover { transform: scale(1.08); }
.x-star.is-full,
.x-star.is-half { color: var(--blue); }
.x-star-track,
.x-star-fill { position: absolute; inset: 0; width: 100%; height: 100%; }
.x-star-fill { color: var(--blue); }
.x-star-fill.is-half { clip-path: inset(0 50% 0 0); }
.x-rate-value { margin-left: 6px; font-size: 13px; font-weight: 620; color: var(--ink-muted); }
</style>
