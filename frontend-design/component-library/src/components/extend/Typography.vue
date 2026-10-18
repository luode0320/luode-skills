<script setup lang="ts">
/* 排版：按 type / heading 决定语义标签，叠加加粗、高亮、下划线、删除线、行内代码、省略、复制等修饰。
   ellipsis 数字走 -webkit-line-clamp 多行省略，布尔走单行省略；复制统一走 @/utils/clipboard。 */
import { computed, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { copyText } from '@/utils/clipboard'

const props = withDefaults(defineProps<{
  type?: 'title' | 'text' | 'paragraph'
  heading?: 1 | 2 | 3 | 4 | 5
  ellipsis?: boolean | number
  bold?: boolean
  mark?: boolean
  underline?: boolean
  delete?: boolean
  code?: boolean
  disabled?: boolean
  copyable?: boolean
  content?: string
}>(), {
  type: 'text',
})

const emit = defineEmits<{ (e: 'copy'): void }>()

const copied = ref(false)
const copyFailed = ref(false)

/** [参数] 无 [返回] 语义标签：标题按 heading 出 h1..h5，段落出 p，文本出 span */
const tag = computed(() => {
  if (props.type === 'title') return `h${props.heading ?? 3}`
  return props.type === 'paragraph' ? 'p' : 'span'
})

/** [参数] 无 [返回] 是否触发多行省略（数字且大于 1） */
const multiLine = computed(() => typeof props.ellipsis === 'number' && props.ellipsis > 1)

/* delete 是 JS 保留字，模板表达式里不能直接引用，桥接成 strike 供模板使用 */
const strike = computed(() => props.delete)

/** [参数] 无 [返回] 多行省略的行内样式 */
const clampStyle = computed(() => (multiLine.value
  ? { display: '-webkit-box', WebkitLineClamp: String(props.ellipsis), WebkitBoxOrient: 'vertical', overflow: 'hidden' }
  : undefined))

/** [参数] text 待复制文本 [返回] 写入剪贴板，成功派发 copy，失败把结果落到图标与可访问名上 */
async function copy(text: string) {
  const ok = await copyText(text || '')
  if (ok) emit('copy')
  copied.value = ok
  copyFailed.value = !ok
  window.setTimeout(() => {
    copied.value = false
    copyFailed.value = false
  }, 1400)
}

/** [参数] 无 [返回] 复制按钮当前形态：成功出对勾，失败出禁止符，其余出复制符 */
const copyIcon = computed(() => {
  if (copied.value) return 'check'
  return copyFailed.value ? 'ban' : 'copy'
})

/** [参数] 无 [返回] 复制按钮的可访问名，随结果变化让读屏也能听到失败 */
const copyLabel = computed(() => {
  if (copied.value) return '已复制'
  return copyFailed.value ? '复制失败，当前浏览器不支持写入剪贴板' : '复制'
})
</script>

<template>
  <div :class="['x-typo', `is-${type}`, disabled && 'is-disabled']">
    <component
      :is="tag"
      :class="[
        'x-typo-el',
        ellipsis !== undefined && !multiLine && 'is-ellipsis',
        multiLine && 'is-clamp',
        bold && 'is-bold',
        mark && 'is-mark',
        underline && 'is-underline',
        strike && 'is-delete',
        code && 'is-code',
      ]"
      :style="clampStyle"
    >
      <slot />
    </component>
    <button
      v-if="copyable"
      :class="['x-typo-copy', copyFailed && 'is-failed']"
      type="button"
      :aria-label="copyLabel"
      @click="copy(content ?? '')"
    >
      <Icon :name="copyIcon" :size="13" />
    </button>
  </div>
</template>

<style scoped>
.x-typo { display: inline-flex; align-items: center; gap: 6px; max-width: 100%; }
.x-typo.is-paragraph { display: flex; }
.x-typo-el { margin: 0; color: var(--ink); font-size: 13px; line-height: 1.62; }
.x-typo.is-title .x-typo-el { font-weight: 660; line-height: 1.35; }
.x-typo.is-title .x-typo-el:is(h1) { font-size: 22px; }
.x-typo.is-title .x-typo-el:is(h2) { font-size: 19px; }
.x-typo.is-title .x-typo-el:is(h3) { font-size: 16px; }
.x-typo.is-title .x-typo-el:is(h4) { font-size: 14px; }
.x-typo.is-title .x-typo-el:is(h5) { font-size: 13px; }
.x-typo.is-paragraph .x-typo-el { color: var(--ink-muted); }
.x-typo-el.is-ellipsis { display: block; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.x-typo-el.is-clamp { overflow-wrap: anywhere; }
.x-typo-el.is-bold { font-weight: 660; }
.x-typo-el.is-mark { padding: 1px 4px; border-radius: var(--r-xs); background: var(--lime-soft); color: var(--ink); }
.x-typo-el.is-underline { text-decoration: underline; text-underline-offset: 3px; }
.x-typo-el.is-delete { text-decoration: line-through; color: var(--ink-faint); }
.x-typo-el.is-code {
  padding: 1px 5px;
  border-radius: var(--r-xs);
  background: var(--groove-bg);
  box-shadow: var(--groove-inset);
  font-family: var(--font-mono);
  font-size: 12px;
}
.x-typo.is-disabled .x-typo-el { color: var(--ink-faint); }
.x-typo-copy {
  flex: none;
  width: 22px;
  height: 22px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 0;
  border-radius: var(--r-xs);
  background: transparent;
  color: var(--ink-soft);
  cursor: pointer;
  transition: background var(--ease-premium) .22s, color var(--ease-premium) .22s;
}
.x-typo-copy:hover { background: var(--hover-bg); color: var(--blue); }
/* 剪贴板不可用时给出可见结果，不让复制按钮退化成点了没反应的死按钮 */
.x-typo-copy.is-failed,
.x-typo-copy.is-failed:hover { background: var(--red-soft); color: var(--red); }
</style>
