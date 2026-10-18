<script setup lang="ts">
/* 图片：加载中显示骨架，失败回落 fallback 或占位图标；preview 时点击开全屏遮罩。
   遮罩支持 Esc 与点击关闭，动作走 overlayEnter / overlayLeave 的 pop 语态。
   最近修改时间：2026-10-18 17:32:00；改动原因：放大按钮只包一个图标 svg，
   role=button 却没有可访问名，读屏念不出用途；同时补齐 role=button 应有的空格键激活。 */
import { computed, onBeforeUnmount, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  src: string
  alt?: string
  width?: number | string
  height?: number | string
  fit?: 'fill' | 'contain' | 'cover' | 'none' | 'scale-down'
  preview?: boolean
  fallback?: string
}>(), {
  alt: '',
  fit: 'cover',
})

const emit = defineEmits<{ (e: 'load'): void; (e: 'error'): void }>()

const status = ref<'loading' | 'ok' | 'fail'>('loading')
const previewOpen = ref(false)
const root = ref<HTMLElement | null>(null)

const boxStyle = computed(() => ({
  width: typeof props.width === 'number' ? `${props.width}px` : props.width,
  height: typeof props.height === 'number' ? `${props.height}px` : props.height,
}))

const currentSrc = computed(() => (status.value === 'fail' ? (props.fallback ?? '') : props.src))

watch(() => props.src, () => { status.value = 'loading' })

/** [参数] 无 [返回] 标记加载成功并派发 load */
function onLoad() {
  status.value = 'ok'
  emit('load')
}

/** [参数] 无 [返回] 标记加载失败并派发 error */
function onError() {
  status.value = 'fail'
  emit('error')
}

/** [参数] 无 [返回] 打开全屏预览遮罩 */
function openPreview() {
  if (!props.preview || status.value !== 'ok') return
  previewOpen.value = true
  document.addEventListener('keydown', onKey)
}

/** [参数] 无 [返回] 关闭预览并解绑键盘监听 */
function closePreview() {
  previewOpen.value = false
  document.removeEventListener('keydown', onKey)
}

/** [参数] event 键盘事件 [返回] Esc 时关闭预览 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape') closePreview()
}

onBeforeUnmount(() => document.removeEventListener('keydown', onKey))
</script>

<template>
  <span ref="root" class="x-image" :style="boxStyle">
    <!-- 真实图片始终挂载：加载中藏起来让骨架占位，成功后显现，失败时若配置 fallback 则换源 -->
    <img
      v-if="currentSrc"
      :src="currentSrc"
      :alt="alt"
      :class="['x-image-el', status !== 'ok' && 'is-hidden']"
      :style="{ objectFit: fit }"
      @load="onLoad"
      @error="onError"
    />
    <span v-if="status === 'loading'" class="x-image-skeleton skeleton" aria-hidden="true" />
    <span v-if="status === 'fail' && !fallback" class="x-image-fallback m-groove">
      <Icon name="file" :size="20" />
    </span>
    <span v-if="preview && status === 'ok'" class="x-image-zoom" role="button" tabindex="0" :aria-label="alt ? `放大预览 ${alt}` : '放大预览'" @click="openPreview" @keydown.enter="openPreview" @keydown.space.prevent="openPreview">
      <Icon name="eye" :size="15" />
    </span>

    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'modal')" @leave="(el, done) => overlayLeave(el, done, 'modal')">
        <div v-if="previewOpen" class="x-image-mask overlay" :style="{ zIndex: floatingLayerFor(root) }" @click.self="closePreview">
          <img :src="src" :alt="alt" class="x-image-full" />
        </div>
      </Transition>
    </Teleport>
  </span>
</template>

<style scoped>
.x-image { position: relative; display: inline-flex; overflow: hidden; border-radius: var(--r-sm); }
.x-image-el { display: block; width: 100%; height: 100%; object-fit: cover; }
.x-image-el.is-hidden { opacity: 0; }
.x-image-skeleton { position: absolute; inset: 0; min-height: 80px; min-width: 80px; }
.x-image-fallback {
  position: absolute;
  inset: 0;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  color: var(--ink-faint);
}
.x-image-zoom {
  position: absolute;
  right: 8px;
  bottom: 8px;
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--r-xs);
  background: var(--float-bg);
  color: var(--ink);
  box-shadow: var(--e1);
  cursor: pointer;
  opacity: 0;
  transition: opacity var(--ease-premium) .26s;
}
.x-image:hover .x-image-zoom { opacity: 1; }
.x-image-mask {
  position: fixed;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--overlay);
  backdrop-filter: blur(6px);
}
.x-image-full { max-width: 88vw; max-height: 88vh; border-radius: var(--r-md); box-shadow: var(--e3); }
</style>
