<script setup lang="ts">
/* 图片预览器：全屏遮罩里看单张大图，支持滚轮与按钮缩放、旋转、Esc / 点遮罩关闭。
   与 Image 的预览同一套浮层语态（Teleport + pop 动效），差别是把缩放旋转做成常驻工具栏。
   开关是受控的：visible 归调用方，组件只维护缩放倍率与旋转角这类纯交互状态，
   这样同一张图在多次开关之间不会因为组件自己记状态而出现「上次的缩放没清掉」。 */
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  src: string
  visible?: boolean
  title?: string
  zoomable?: boolean
}>(), {
  visible: false,
  zoomable: true,
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'close'): void
}>()

/* 锚点只为给遮罩算出所在浮层层级；遮罩本身是最高层，锚点不参与视觉 */
const anchor = ref<HTMLElement | null>(null)
const mask = ref<HTMLElement | null>(null)
const scale = ref(1)
const rotate = ref(0)

const open = computed({
  get: () => props.visible,
  set: (value: boolean) => emit('update:visible', value),
})

const imageStyle = computed(() => ({ transform: `scale(${scale.value}) rotate(${rotate.value}deg)` }))

/**
 * [参数] delta 本次缩放的增量，正数放大负数缩小
 * [返回] 无。倍率夹在 0.2~5，避免滚轮连点把图缩成看不见或放到溢出失控
 */
function zoomBy(delta: number) {
  if (!props.zoomable) return
  scale.value = Math.min(5, Math.max(0.2, Number((scale.value + delta).toFixed(2))))
}

/**
 * [参数] event 遮罩上的滚轮事件
 * [返回] 无。向上放大向下缩小；吞掉默认滚动，否则页面会跟着一起滚
 */
function onWheel(event: WheelEvent) {
  if (!props.zoomable) return
  event.preventDefault()
  zoomBy(event.deltaY < 0 ? 0.2 : -0.2)
}

/**
 * [参数] 无
 * [返回] 无。每次转 90 度并对 360 取模，避免角度无限累加后转回原位要多转好几圈
 */
function rotateBy() {
  rotate.value = (rotate.value + 90) % 360
}

/**
 * [参数] 无
 * [返回] 无。复位缩放与旋转，换图或重新打开时都要清，防止上一张的视角带到下一张
 */
function resetTransform() {
  scale.value = 1
  rotate.value = 0
}

/**
 * [参数] 无
 * [返回] 无。只改受控值并派发 close，遮罩的销毁交给调用方
 */
function close() {
  open.value = false
  emit('close')
}

/**
 * [参数] event 键盘事件
 * [返回] 无。Esc 是遮罩类浮层的通用退出键，保证不看按钮也能关
 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
}

/* 打开时才挂全局键盘监听：关着的时候不留监听器，避免多个预览器抢 Esc */
watch(() => props.visible, (value) => {
  if (value) {
    resetTransform()
    document.addEventListener('keydown', onKey)
  } else {
    document.removeEventListener('keydown', onKey)
  }
}, { immediate: true })

watch(() => props.src, resetTransform)

onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <span ref="anchor" class="x-preview-anchor" aria-hidden="true" />
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'modal')" @leave="(el, done) => overlayLeave(el, done, 'modal')">
      <div
        v-if="visible"
        ref="mask"
        class="x-preview-mask"
        role="dialog"
        aria-modal="true"
        :aria-label="title ?? '图片预览'"
        @click.self="close"
        @wheel="onWheel"
      >
        <div v-if="title" class="x-preview-title">{{ title }}</div>
        <img class="x-preview-image" :src="src" :alt="title ?? '图片预览'" :style="imageStyle" />
        <div class="x-preview-tools" :style="{ zIndex: floatingLayerFor(mask) }">
          <template v-if="zoomable">
            <button type="button" class="x-preview-tool" aria-label="缩小" @click="zoomBy(-0.2)">
              <Icon name="minus" :size="15" />
            </button>
            <span class="x-preview-scale">{{ Math.round(scale * 100) }}%</span>
            <button type="button" class="x-preview-tool" aria-label="放大" @click="zoomBy(0.2)">
              <Icon name="plus" :size="15" />
            </button>
          </template>
          <button type="button" class="x-preview-tool" aria-label="旋转 90 度" @click="rotateBy">
            <Icon name="refresh" :size="15" />
          </button>
          <button type="button" class="x-preview-tool" aria-label="关闭预览" @click="close">
            <Icon name="x" :size="15" />
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* 锚点不占位：它的唯一职责是让遮罩算出所在浮层层级 */
.x-preview-anchor { display: none; }
.x-preview-mask {
  position: fixed;
  inset: 0;
  z-index: var(--layer-overlay);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  padding: 40px 32px 88px;
  background: var(--overlay);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}
/* 标题压成一块深色铭牌，浅色图上也能读清 */
.x-preview-title {
  padding: 5px 12px;
  border-radius: 9999px;
  background: var(--dark-surface);
  color: var(--plate-ink);
  font-size: 13px;
  letter-spacing: .01em;
}
.x-preview-image {
  max-width: 88vw;
  max-height: 74vh;
  border-radius: var(--r-md);
  box-shadow: var(--e3);
  transition: transform var(--ease-premium) .3s;
}
/* 工具栏绝对压在遮罩底部居中，不参与图片的居中对齐 */
.x-preview-tools {
  position: absolute;
  left: 50%;
  bottom: 28px;
  transform: translateX(-50%);
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px;
  border-radius: 9999px;
  background: var(--float-bg);
  box-shadow: var(--e3), var(--float-inset);
}
.x-preview-tool {
  width: 30px;
  height: 30px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  color: var(--ink);
  cursor: pointer;
  transition: background var(--ease-premium) .2s, color var(--ease-premium) .2s;
}
.x-preview-tool:hover { background: var(--hover-bg); }
.x-preview-scale {
  min-width: 44px;
  color: var(--ink-muted);
  font-family: var(--font-mono);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
  text-align: center;
}
</style>
