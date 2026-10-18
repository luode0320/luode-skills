<script setup lang="ts">
/* 分栏：一块区域按可拖动的分隔条切成两半，横向出左右、纵向出上下。
   尺寸由 v-model 单向持有，拖动时只 emit，调用方回填后组件才变宽窄，
   因此父级可以随时从外部改比例；双击分隔条复位到 50%。
   指针事件全程 setPointerCapture，拖出分栏范围也不丢手势。 */
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
  direction?: 'horizontal' | 'vertical'
  modelValue?: number
  min?: number
  max?: number
  /** 单位 px */
}>(), {
  direction: 'horizontal',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: number): void
  (e: 'resize', size: number): void
}>()

const root = ref<HTMLElement | null>(null)
const dragging = ref(false)

const isHorizontal = computed(() => props.direction === 'horizontal')

/**
 * [参数] value 原始像素值
 * [返回] 夹紧到 min/max 与容器尺寸共同允许区间的数值
 */
function clamp(value: number) {
  const total = isHorizontal.value ? (root.value?.offsetWidth ?? 0) : (root.value?.offsetHeight ?? 0)
  /* 上下限缺省时退化成容器自身边界，避免第一片把第二片挤没 */
  const lower = props.min ?? 0
  const upper = props.max ?? (total || Number.POSITIVE_INFINITY)
  return Math.min(Math.max(value, lower), Math.max(lower, upper))
}

/**
 * [参数] event 按下事件，来源是分隔条
 * [返回] 无。开启拖拽并捕获指针
 */
function startDrag(event: PointerEvent) {
  if (event.button !== 0) return
  dragging.value = true
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
  event.preventDefault()
}

/**
 * [参数] event 指针移动事件
 * [返回] 无。把指针在容器内的位置换算成第一片尺寸
 */
function onDrag(event: PointerEvent) {
  if (!dragging.value || !root.value) return
  const rect = root.value.getBoundingClientRect()
  const next = clamp(isHorizontal.value ? event.clientX - rect.left : event.clientY - rect.top)
  emit('update:modelValue', next)
  emit('resize', next)
}

/**
 * [参数] event 抬起或取消事件
 * [返回] 无。结束拖拽并释放指针捕获
 */
function endDrag(event: PointerEvent) {
  if (!dragging.value) return
  dragging.value = false
  const target = event.currentTarget as HTMLElement
  if (target.hasPointerCapture(event.pointerId)) target.releasePointerCapture(event.pointerId)
}

/** [参数] 无 [返回] 无。双击分隔条把比例复位到容器的一半 */
function resetToHalf() {
  if (!root.value) return
  const total = isHorizontal.value ? root.value.offsetWidth : root.value.offsetHeight
  const next = clamp(total / 2)
  emit('update:modelValue', next)
  emit('resize', next)
}

/* 无 v-model 时给第一片一个可用的兜底尺寸，有值时严格听调用方的 */
const firstStyle = computed(() => ({
  flex: props.modelValue === undefined ? '0 0 50%' : `0 0 ${props.modelValue}px`,
}))
</script>

<template>
  <div ref="root" :class="['x-split', isHorizontal ? 'is-horizontal' : 'is-vertical', dragging && 'is-dragging']">
    <div class="x-split-part is-first" :style="firstStyle">
      <slot :name="isHorizontal ? 'left' : 'top'" />
    </div>
    <div
      class="x-split-bar"
      role="separator"
      :aria-orientation="isHorizontal ? 'vertical' : 'horizontal'"
      :aria-valuenow="modelValue"
      :aria-valuemin="min"
      :aria-valuemax="max"
      aria-label="拖动调整分栏比例"
      tabindex="0"
      @pointerdown="startDrag"
      @pointermove="onDrag"
      @pointerup="endDrag"
      @pointercancel="endDrag"
      @dblclick="resetToHalf"
      @keydown.enter.prevent="resetToHalf"
    >
      <span class="x-split-grip" aria-hidden="true" />
    </div>
    <div class="x-split-part is-second">
      <slot :name="isHorizontal ? 'right' : 'bottom'" />
    </div>
  </div>
</template>

<style scoped>
.x-split { display: flex; box-sizing: border-box; min-width: 0; min-height: 0; width: 100%; height: 100%; }
.x-split.is-horizontal { flex-direction: row; }
.x-split.is-vertical { flex-direction: column; }
/* 第二片吃掉剩余空间；两片都允许收缩，否则长内容会把分栏撑破 */
.x-split-part { min-width: 0; min-height: 0; overflow: auto; }
.x-split-part.is-first { flex: 0 0 50%; }
.x-split-part.is-second { flex: 1 1 0; }
.x-split-bar {
  flex: none;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--line-strong);
  touch-action: none;
  outline: none;
}
.x-split.is-horizontal .x-split-bar { width: 6px; cursor: col-resize; }
.x-split.is-vertical .x-split-bar { height: 6px; cursor: row-resize; }
.x-split.is-dragging .x-split-bar { background: var(--blue); }
.x-split-bar:focus-visible { background: var(--blue); }
/* 抓握提示：分隔条正中一小段玻璃条，hover 时点亮成主色 */
.x-split-grip { border-radius: 9999px; background: var(--ink-faint); opacity: .55; transition: background var(--ease-premium) .24s; }
.x-split.is-horizontal .x-split-grip { width: 2px; height: 22px; }
.x-split.is-vertical .x-split-grip { width: 22px; height: 2px; }
.x-split-bar:hover .x-split-grip { background: var(--blue); opacity: 1; }
</style>
