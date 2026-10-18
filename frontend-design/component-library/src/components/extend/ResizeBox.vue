<script setup lang="ts">
/* 伸缩框：拖动右下角把手把内容压成指定宽高，宽高直接落到容器尺寸上。
   指针事件全程走 setPointerCapture，拖到容器外也不丢手势；min/max 在移动时实时夹紧。
   direction 决定把手只吃哪一轴：horizontal 只改宽、vertical 只改高，
   另一轴保持拖拽开始时的尺寸原样回传，调用方拿到的宽高始终是一份完整快照。 */
import { computed, ref } from 'vue'

const props = withDefaults(defineProps<{
  direction?: 'horizontal' | 'vertical'
  width?: number
  height?: number
  minWidth?: number
  maxWidth?: number
  minHeight?: number
  maxHeight?: number
}>(), {
  direction: 'horizontal',
})

const emit = defineEmits<{ (e: 'resize', size: { width: number; height: number }): void }>()

const box = ref<HTMLElement | null>(null)
const dragging = ref(false)
/* 拖拽起点：指针位置 + 起始尺寸，move 时用增量算目标值 */
const origin = ref({ x: 0, y: 0, width: 0, height: 0 })

const style = computed(() => ({
  width: props.width === undefined ? undefined : `${props.width}px`,
  height: props.height === undefined ? undefined : `${props.height}px`,
}))

/**
 * [参数] value 目标值，min 下限，max 上限，均可缺省
 * [返回] 夹紧到合法区间的数值；任一上下限缺省时不参与夹紧
 */
function clamp(value: number, min?: number, max?: number) {
  let next = value
  if (min !== undefined) next = Math.max(min, next)
  if (max !== undefined) next = Math.min(max, next)
  return next
}

/**
 * [参数] event 按下事件，来源是把手区
 * [返回] 无。开启拖拽、记下起始尺寸并捕获指针
 */
function startDrag(event: PointerEvent) {
  if (event.button !== 0 || !box.value) return
  dragging.value = true
  origin.value = {
    x: event.clientX,
    y: event.clientY,
    width: box.value.offsetWidth,
    height: box.value.offsetHeight,
  }
  /* 捕获指针：快速拖出容器仍持续收到 move/up */
  ;(event.currentTarget as HTMLElement).setPointerCapture(event.pointerId)
  event.preventDefault()
}

/**
 * [参数] event 指针移动事件
 * [返回] 无。按 direction 只更新允许的那一轴，另一轴沿用起始尺寸
 */
function onDrag(event: PointerEvent) {
  if (!dragging.value) return
  const start = origin.value
  const nextWidth = props.direction === 'horizontal'
    ? clamp(start.width + (event.clientX - start.x), props.minWidth, props.maxWidth)
    : start.width
  const nextHeight = props.direction === 'vertical'
    ? clamp(start.height + (event.clientY - start.y), props.minHeight, props.maxHeight)
    : start.height
  emit('resize', { width: nextWidth, height: nextHeight })
}

/**
 * [参数] event 抬起或取消事件，用于释放捕获
 * [返回] 无
 */
function endDrag(event: PointerEvent) {
  if (!dragging.value) return
  dragging.value = false
  const target = event.currentTarget as HTMLElement
  if (target.hasPointerCapture(event.pointerId)) target.releasePointerCapture(event.pointerId)
}
</script>

<template>
  <div ref="box" :class="['x-resize', `is-${direction}`, dragging && 'is-dragging']" :style="style">
    <div class="x-resize-body"><slot /></div>
    <div
      class="x-resize-handle"
      role="separator"
      aria-label="拖动调整尺寸"
      @pointerdown="startDrag"
      @pointermove="onDrag"
      @pointerup="endDrag"
      @pointercancel="endDrag"
    >
      <slot name="resize">
        <span class="x-resize-grip" aria-hidden="true" />
      </slot>
    </div>
  </div>
</template>

<style scoped>
.x-resize {
  position: relative;
  display: inline-flex;
  box-sizing: border-box;
  min-width: 0;
  min-height: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--r-md);
  background: var(--surface);
  box-shadow: var(--edge), var(--e1);
  overflow: hidden;
}
.x-resize.is-dragging { border-color: var(--focus); }
.x-resize-body { flex: 1; min-width: 0; min-height: 0; overflow: auto; }
/* 把手押在右下角，只吃自己那一小块命中区，不遮内容 */
.x-resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 22px;
  height: 22px;
  display: flex;
  align-items: flex-end;
  justify-content: flex-end;
  padding: 4px;
  touch-action: none;
}
/* 光标方向跟真实可拖的轴一致：横向只改宽、纵向只改高 */
.x-resize.is-horizontal .x-resize-handle { cursor: ew-resize; }
.x-resize.is-vertical .x-resize-handle { cursor: ns-resize; }
/* 默认把手：右下角一段折角线，构成常见的「缩放角」提示 */
.x-resize-grip {
  width: 10px;
  height: 10px;
  border-right: 1.5px solid var(--ink-faint);
  border-bottom: 1.5px solid var(--ink-faint);
  border-bottom-right-radius: 3px;
}
.x-resize.is-dragging .x-resize-grip { border-color: var(--blue); }
</style>
