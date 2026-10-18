<script setup lang="ts">
/* 图片预览组：一组图共用一个全屏预览器，底部缩略图导航，左右箭头或方向键切上下张。
   与 ImagePreview 的分工：单图预览管「这一张怎么看」，预览组管「在多张之间怎么走」，
   所以这里不重复做缩放旋转，只把切换、计数与缩略图对齐做扎实。
   索引是半受控的：initialIndex 只在每次打开时作为起点，打开后的翻页由组件自己记，
   否则调用方不监听 change 就会把用户翻到的那一页弹回去。 */
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface PreviewImage {
  src: string
  alt?: string
}

const props = withDefaults(defineProps<{
  images: PreviewImage[]
  visible?: boolean
  initialIndex?: number
}>(), {
  visible: false,
  initialIndex: 0,
})

const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'change', index: number): void
}>()

const anchor = ref<HTMLElement | null>(null)
const mask = ref<HTMLElement | null>(null)
const index = ref(0)

const open = computed({
  get: () => props.visible,
  set: (value: boolean) => emit('update:visible', value),
})

const current = computed<PreviewImage | undefined>(() => props.images[index.value])

/** 只有多张时才显示切换与缩略图，单张图退化成纯大图，避免出现一个没意义的「1 / 1」 */
const multiple = computed(() => props.images.length > 1)

/**
 * [参数] target 目标下标
 * [返回] 无。下标按张数取模，越界自动绕回，箭头在首尾也能继续走
 */
function goTo(target: number) {
  const count = props.images.length
  if (!count) return
  const next = ((target % count) + count) % count
  if (next === index.value) return
  index.value = next
  emit('change', next)
}

/**
 * [参数] delta 方向步进，正数下一张负数上一张
 * [返回] 无
 */
function step(delta: number) {
  goTo(index.value + delta)
}

/**
 * [参数] 无
 * [返回] 无。只改受控值，遮罩销毁交给调用方，组件不额外造一个 close 事件
 */
function close() {
  open.value = false
}

/**
 * [参数] event 键盘事件
 * [返回] 无。左右方向键切图、Esc 退出，符合看图时的直觉操作
 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
  else if (event.key === 'ArrowLeft') step(-1)
  else if (event.key === 'ArrowRight') step(1)
}

/* 打开时把索引重置到调用方给的起点，并挂上键盘监听；关掉立即撤监听 */
watch(() => props.visible, (value) => {
  if (value) {
    index.value = Math.min(Math.max(props.initialIndex, 0), Math.max(props.images.length - 1, 0))
    document.addEventListener('keydown', onKey)
  } else {
    document.removeEventListener('keydown', onKey)
  }
}, { immediate: true })

onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <span ref="anchor" class="x-group-anchor" aria-hidden="true" />
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'modal')" @leave="(el, done) => overlayLeave(el, done, 'modal')">
      <div
        v-if="visible && current"
        ref="mask"
        class="x-group-mask"
        role="dialog"
        aria-modal="true"
        aria-label="图片预览组"
        @click.self="close"
      >
        <div class="x-group-stage">
          <button v-if="multiple" type="button" class="x-group-arrow is-prev" aria-label="上一张" @click="step(-1)">
            <Icon name="chevronLeft" :size="18" />
          </button>
          <img class="x-group-image" :src="current.src" :alt="current.alt ?? '图片预览'" />
          <button v-if="multiple" type="button" class="x-group-arrow is-next" aria-label="下一张" @click="step(1)">
            <Icon name="chevronRight" :size="18" />
          </button>
        </div>

        <div class="x-group-bar" :style="{ zIndex: floatingLayerFor(mask) }">
          <span v-if="current.alt" class="x-group-caption">{{ current.alt }}</span>
          <div v-if="multiple" class="x-group-thumbs">
            <button
              v-for="(image, i) in images"
              :key="image.src"
              type="button"
              :class="['x-group-thumb', i === index && 'is-active']"
              :aria-label="image.alt ?? `第 ${i + 1} 张`"
              :aria-current="i === index || undefined"
              @click="goTo(i)"
            >
              <img :src="image.src" :alt="image.alt ?? ''" />
            </button>
          </div>
          <span v-if="multiple" class="x-group-counter">{{ index + 1 }} / {{ images.length }}</span>
          <button type="button" class="x-group-close" aria-label="关闭预览" @click="close">
            <Icon name="x" :size="15" />
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-group-anchor { display: none; }
.x-group-mask {
  position: fixed;
  inset: 0;
  z-index: var(--layer-overlay);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding: 36px 32px 24px;
  background: var(--overlay);
  backdrop-filter: blur(6px);
  -webkit-backdrop-filter: blur(6px);
}
/* 舞台用 grid 叠三层：图片居中，箭头压在两侧，图片宽度变化时箭头不会跟着跑 */
.x-group-stage {
  position: relative;
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  align-items: center;
  gap: 14px;
  max-width: 92vw;
}
.x-group-image {
  grid-column: 2;
  max-width: 100%;
  max-height: 66vh;
  border-radius: var(--r-md);
  box-shadow: var(--e3);
}
.x-group-arrow {
  width: 38px;
  height: 38px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  background: var(--float-bg);
  color: var(--ink);
  box-shadow: var(--e3), var(--float-inset);
  cursor: pointer;
  transition: background var(--ease-premium) .2s;
}
.x-group-arrow:hover { background: var(--surface-solid); }
.x-group-arrow.is-prev { grid-column: 1; }
.x-group-arrow.is-next { grid-column: 3; }
.x-group-bar {
  display: inline-flex;
  align-items: center;
  gap: 12px;
  max-width: 92vw;
  padding: 7px 10px;
  border-radius: 9999px;
  background: var(--float-bg);
  box-shadow: var(--e3), var(--float-inset);
}
.x-group-caption {
  max-width: 260px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  color: var(--ink-muted);
  font-size: 13px;
}
.x-group-thumbs { display: inline-flex; gap: 6px; }
.x-group-thumb {
  width: 42px;
  height: 30px;
  padding: 0;
  overflow: hidden;
  border: 1px solid var(--line-strong);
  border-radius: var(--r-xs);
  cursor: pointer;
  opacity: .55;
  transition: opacity var(--ease-premium) .24s, border-color var(--ease-premium) .24s;
}
.x-group-thumb img { width: 100%; height: 100%; object-fit: cover; }
.x-group-thumb:hover { opacity: .85; }
/* 选中缩略图同时抬高不透明度和描边色：只靠不透明度区分在浅色图上不够明显 */
.x-group-thumb.is-active { opacity: 1; border-color: var(--blue); }
.x-group-counter {
  color: var(--ink-muted);
  font-family: var(--font-mono);
  font-size: 12px;
  font-variant-numeric: tabular-nums;
}
.x-group-close {
  width: 28px;
  height: 28px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  color: var(--ink);
  cursor: pointer;
  transition: background var(--ease-premium) .2s;
}
.x-group-close:hover { background: var(--hover-bg); }
</style>
