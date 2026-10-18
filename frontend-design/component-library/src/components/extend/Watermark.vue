<script setup lang="ts">
/* 水印：用 canvas 把文字 / 图片绘成 dataURL，作为背景图平铺在内容之上。
   覆盖层 pointer-events: none，不干扰插槽内的交互。 */
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  content?: string | string[]
  image?: string
  rotate?: number
  gap?: [number, number]
  font?: { fontSize?: number; color?: string }
  zIndex?: number
}>(), {
  content: () => [],
  rotate: -22,
  gap: () => [100, 100],
  zIndex: 9,
})

const dataUrl = ref('')

/** [参数] 无 [返回] 归一后的水印文本行数组 */
const lines = computed(() => (Array.isArray(props.content) ? props.content : props.content ? [props.content] : []))

/** [参数] 无 [返回] 水印默认色：读根令牌 --ink 叠加透明度，令牌缺失才回落字面值 */
function defaultColor() {
  const ink = getComputedStyle(document.documentElement).getPropertyValue('--ink').trim()
  /* 令牌是 #rrggbb 时转成带透明度的 rgba，让水印足够淡；其它形态统一回落字面值 */
  const hex = /^#([0-9a-f]{6})$/i.exec(ink)
  if (!hex) return 'rgba(16, 20, 24, .14)'
  const n = Number.parseInt(hex[1], 16)
  return `rgba(${(n >> 16) & 255}, ${(n >> 8) & 255}, ${n & 255}, .14)`
}

/** [参数] 无 [返回] 生成水印背景图；无文本也无图片时清空 */
function render() {
  if (!lines.value.length && !props.image) {
    dataUrl.value = ''
    return
  }
  const fontSize = props.font?.fontSize ?? 14
  const color = props.font?.color ?? defaultColor()
  const [gapX, gapY] = props.gap
  const canvas = document.createElement('canvas')
  const ctx = canvas.getContext('2d')
  if (!ctx) return
  const lineHeight = fontSize * 1.4
  const textWidth = lines.value.reduce((max, line) => Math.max(max, ctx.measureText(line).width), 0) || fontSize * 4
  // 旋转后需要更大的画布，用对角线长度兜住四个角
  const diagonal = Math.ceil(Math.hypot(textWidth, lineHeight * lines.value.length))
  const tileW = Math.max(diagonal + 40, gapX)
  const tileH = Math.max(diagonal + 40, gapY)
  canvas.width = tileW
  canvas.height = tileH
  ctx.translate(tileW / 2, tileH / 2)
  ctx.rotate((props.rotate * Math.PI) / 180)
  const paint = () => {
    ctx.font = `${fontSize}px "SF Pro Text", "PingFang SC", sans-serif`
    ctx.fillStyle = color
    ctx.textAlign = 'center'
    ctx.textBaseline = 'middle'
    const offset = ((lines.value.length - 1) * lineHeight) / 2
    lines.value.forEach((line, i) => ctx.fillText(line, 0, i * lineHeight - offset))
  }

  if (props.image) {
    /* 图片水印：按字号等比缩放后居中绘制，绘制完成再取 dataURL，避免拿到空图 */
    const img = new Image()
    img.crossOrigin = 'anonymous'
    img.onload = () => {
      const w = fontSize * 3
      const h = (img.height / img.width) * w
      ctx.drawImage(img, -w / 2, -h / 2, w, h)
      paint()
      dataUrl.value = canvas.toDataURL()
    }
    img.src = props.image
    return
  }
  paint()
  dataUrl.value = canvas.toDataURL()
}

onMounted(render)
watch(() => [props.content, props.image, props.rotate, props.gap, props.font], render, { deep: true })

onBeforeUnmount(() => { dataUrl.value = '' })

/** [参数] 无 [返回] 平铺覆盖层样式，无图时不渲染 */
const layerStyle = computed(() => (dataUrl.value
  ? { backgroundImage: `url(${dataUrl.value})`, zIndex: props.zIndex }
  : undefined))
</script>

<template>
  <div class="x-watermark">
    <slot />
    <div v-if="dataUrl" class="x-watermark-layer" :style="layerStyle" aria-hidden="true" />
  </div>
</template>

<style scoped>
.x-watermark { position: relative; }
.x-watermark-layer {
  position: absolute;
  inset: 0;
  pointer-events: none;
  background-repeat: repeat;
  background-position: 0 0;
}
</style>
