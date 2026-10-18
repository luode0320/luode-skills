<script setup lang="ts">
/* 多行文本域：在 TextInput 的 multiline 之外补两项真实能力——自动高度与字数统计。
   之所以不直接给 TextInput 加这两个开关：它属上游冻结层，字节基线不允许改。
   自动高度按内容测 scrollHeight 并夹到 [minRows, maxRows]，超出后回落内部滚动，
   字数统计只在给了 maxlength 时才出现，避免无上限时显示一个没有意义的计数。 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  readonly?: boolean
  invalid?: boolean
  rows?: number
  /** 自动高度：随内容增高，超出 maxRows 后内部滚动 */
  autoSize?: boolean
  maxRows?: number
  maxlength?: number
  showCount?: boolean
}>(), {
  modelValue: '',
  rows: 3,
  maxRows: 8,
  showCount: true,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const el = ref<HTMLTextAreaElement | null>(null)
/* 单行像素高度：只在挂载时量一次，供 maxRows 换算上限，避免每次输入都重排读尺寸。
   取计算样式而不是元素属性——HTMLTextAreaElement 本身不暴露 lineHeight。 */
const line = ref(20)
/* 计数行需要唯一 id 才能被 aria-describedby 引用，同页多实例不能共用固定 id */
const countId = `ta-count-${Math.random().toString(36).slice(2, 8)}`

/** [参数] 无 [返回] 无；按内容测高并夹到上下限，保持与固定 rows 模式可切换 */
function resize() {
  const node = el.value
  if (!node) return
  node.style.height = 'auto'
  const natural = node.scrollHeight
  if (!props.autoSize) {
    node.style.height = ''
    return
  }
  const min = props.rows * line.value
  const max = props.maxRows * line.value
  node.style.height = `${Math.min(Math.max(natural, min), max)}px`
  /* 超过上限时把溢出交给内部滚动，否则高度被夹住后尾行会被裁掉 */
  node.style.overflowY = natural > max ? 'auto' : 'hidden'
}

let observer: ResizeObserver | null = null
/* 只认宽度变化：autoSize 自己会改高度，若对高度也响应就构成回环 */
let lastWidth = 0

onMounted(() => {
  if (el.value) {
    const lh = parseFloat(getComputedStyle(el.value).lineHeight)
    if (!Number.isNaN(lh)) line.value = lh
  }
  nextTick(resize)
  /* 容器宽度变化会改变折行数，需要在宽度变化后重新测高 */
  if (el.value && typeof ResizeObserver !== 'undefined') {
    lastWidth = el.value.getBoundingClientRect().width
    observer = new ResizeObserver(([entry]) => {
      const width = entry.contentRect.width
      if (width === lastWidth) return
      lastWidth = width
      resize()
    })
    observer.observe(el.value)
  }
})

onBeforeUnmount(() => observer?.disconnect())

watch(() => props.modelValue, () => nextTick(resize))
watch(() => [props.autoSize, props.rows, props.maxRows], () => nextTick(resize))

/** [参数] event 输入事件 [返回] 无；受控用法下不存本地副本，避免与父级值分叉 */
function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLTextAreaElement).value)
}

const count = computed(() => Array.from(props.modelValue ?? '').length)
const showLimit = computed(() => props.showCount && props.maxlength !== undefined)

defineExpose({ focus: () => el.value?.focus() })
</script>

<template>
  <span class="x-textarea-wrap">
    <span :class="['input-shell', 'is-multiline', 'x-textarea', autoSize && 'is-auto', invalid && 'is-invalid', disabled && 'is-disabled']">
      <textarea
        ref="el"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :rows="rows"
        :maxlength="maxlength"
        :aria-invalid="invalid || undefined"
        :aria-describedby="showLimit ? countId : undefined"
        @input="onInput"
      />
    </span>
    <span v-if="showLimit" :id="countId" class="x-textarea-count" :class="{ 'is-full': count >= (maxlength ?? 0) }">{{ count }} / {{ maxlength }}</span>
  </span>
</template>

<style scoped>
/* 描边与聚焦态复用全局 .input-shell.is-multiline，深色主题自动随令牌翻转；
   这里只补自动高度所需的溢出控制与计数行排版 */
.x-textarea-wrap { display: flex; flex-direction: column; gap: 4px; min-width: 0; }
.x-textarea { width: 100%; }
.x-textarea textarea { resize: vertical; }
.x-textarea.is-auto textarea { resize: none; }
.x-textarea-count { align-self: flex-end; font-size: 12px; color: var(--ink-faint); font-variant-numeric: tabular-nums; }
.x-textarea-count.is-full { color: var(--red-text); }
</style>
