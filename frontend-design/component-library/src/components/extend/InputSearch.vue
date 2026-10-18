<script setup lang="ts">
/* 搜索输入：把「填词 + 触发搜索」收成一个控件，回车与点右侧按钮完全等价。
   之所以不直接复用 TextInput 外面挂一个按钮，是因为搜索按钮必须长在同一圈描边里：
   独立按钮会多出一条边框接缝，读起来像两个并排控件，而不是一个输入框带动作。
   边界：组件只负责取值与派发意图，不发请求、不做防抖，节流与请求由调用方掌握。 */
import { ref } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  loading?: boolean
  disabled?: boolean
  allowClear?: boolean
}>(), {
  modelValue: '',
  placeholder: '',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
  (e: 'search', value: string): void
}>()

const el = ref<HTMLInputElement | null>(null)

/** [参数] event 输入事件 [返回] 无；即时回传，受控用法下不做本地副本，避免与父级值分叉 */
function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}

/** [参数] 无 [返回] 无；清空后把焦点还给输入框，用户可以立刻重打 */
function clear() {
  emit('update:modelValue', '')
  el.value?.focus()
}

/** [参数] 无 [返回] 无；搜索词取自受控值而非 DOM，保证父级改写后搜索的仍是可见内容 */
function trigger() {
  if (props.disabled || props.loading) return
  emit('search', props.modelValue ?? '')
}

defineExpose({ focus: () => el.value?.focus() })
</script>

<template>
  <span :class="['x-search', disabled && 'is-disabled']">
    <Icon name="search" :size="15" />
    <input
      ref="el"
      type="text"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="onInput"
      @keydown.enter.prevent="trigger"
    />
    <button
      v-if="allowClear && modelValue && !disabled"
      type="button"
      class="x-search-clear"
      aria-label="清空"
      @click="clear"
    >
      <Icon name="x" :size="14" />
    </button>
    <button
      type="button"
      class="x-search-btn"
      :disabled="disabled || loading"
      :aria-busy="loading || undefined"
      aria-label="搜索"
      @click="trigger"
    >
      <span v-if="loading" class="x-search-ring" aria-hidden="true" />
      <Icon v-else name="search" :size="15" />
    </button>
  </span>
</template>

<style scoped>
/* 描边两档都用令牌：深色主题下 --shade 翻成纯黑，手写 rgba(var(--shade), .18)
   会越悬停越不可见；--line → --line-strong 在两种主题下都保持「悬停变实」的方向 */
.x-search {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 0;
  height: var(--control-h);
  padding-left: 12px;
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  background: var(--input-bg);
  box-shadow: var(--edge);
  color: var(--ink-soft);
  transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
}
.x-search:hover:not(.is-disabled) { border-color: var(--line-strong); }
.x-search:focus-within {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
  border-color: transparent;
}
.x-search.is-disabled { opacity: .6; background: var(--groove-bg); }

.x-search input {
  flex: 1;
  min-width: 0;
  height: 100%;
  padding: 0;
  border: 0;
  background: transparent;
  color: var(--ink);
  font-size: 13px;
  outline: none;
}
.x-search input::placeholder { color: var(--ink-faint); }

.x-search-clear {
  display: inline-flex;
  flex: none;
  color: var(--ink-faint);
  border-radius: 999px;
  transition: color .15s ease;
}
.x-search-clear:hover { color: var(--ink-muted); }

/* 按钮自己撑满高度并吃掉右侧圆角，视觉上与输入框共用一圈描边；
   inset 细线代替 border，避免和容器边框叠成两像素的粗缝 */
.x-search-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  align-self: stretch;
  width: 38px;
  border-radius: 0 calc(var(--r-sm) - 1px) calc(var(--r-sm) - 1px) 0;
  color: var(--ink-soft);
  box-shadow: inset 1px 0 0 var(--line);
  transition: color .2s ease, background .2s ease;
}
.x-search-btn:hover:not(:disabled) { color: var(--ink); background: var(--hover-bg); }
.x-search-btn:disabled { opacity: .45; cursor: not-allowed; }

/* 转圈就地替换图标，宽度不变，输入内容不会因状态切换而左右抖动 */
.x-search-ring {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  border: 2px solid currentColor;
  border-right-color: transparent;
  animation: x-search-spin .7s linear infinite;
}
@keyframes x-search-spin { to { transform: rotate(360deg); } }
</style>
