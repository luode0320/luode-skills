<script setup lang="ts">
/* 密码输入框：在输入框内自带一个「明文/密文」切换钮，点击即在 password 与 text 间切换。
   之所以不复用 TextInput 外挂一个眼睛按钮，是因为可见性必须与输入框共用同一圈描边：
   独立按钮会多出一条边框接缝，读起来像两个并排控件，而不是一个会自己切换的密码框。
   边界：组件只持有「是否明文」这一显示态并回传取值，不做强度校验、不发请求。
   切换态用内联 SVG（eyeOff 属本扩展层私有图标，不外溢改动上游冻结的 src/data/icons.ts）。 */
import { computed, ref } from 'vue'
import Icon from '@/components/Icon.vue'

/* 密文态用 Icon 的 eye，明文态用下面这条"划线眼"路径；eyeOff 属本扩展层私有，不外溢改动上游冻结的 src/data/icons.ts */
const EYE_OFF_PATH = 'M4 4l16 16M9.9 5.1A9.6 9.6 0 0 1 12 5c6 0 10 7 10 7a17 17 0 0 1-3.2 3.9M6.6 6.6A16.7 16.7 0 0 0 2 12s4 7 10 7a9.7 9.7 0 0 0 4-.85M9.9 9.9a3 3 0 0 0 4.2 4.2'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  defaultVisible?: boolean
}>(), {
  modelValue: '',
  placeholder: '请输入密码',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: string): void
}>()

const el = ref<HTMLInputElement | null>(null)
const visible = ref(props.defaultVisible ?? false)
const type = computed(() => (visible.value ? 'text' : 'password'))

/** [参数] event 输入事件 [返回] 无；即时回传，受控用法下不做本地副本，避免与父级值分叉 */
function onInput(event: Event) {
  emit('update:modelValue', (event.target as HTMLInputElement).value)
}

/** [参数] 无 [返回] 无；切换明文/密文后把焦点还给输入框，用户可以立刻继续输入 */
function toggle() {
  if (props.disabled) return
  visible.value = !visible.value
  el.value?.focus()
}

defineExpose({ focus: () => el.value?.focus() })
</script>

<template>
  <span :class="['x-password', disabled && 'is-disabled']">
    <Icon name="lock" :size="15" />
    <input
      ref="el"
      :type="type"
      :value="modelValue"
      :placeholder="placeholder"
      :disabled="disabled"
      @input="onInput"
    />
    <button
      type="button"
      class="x-password-toggle"
      :disabled="disabled"
      :aria-label="visible ? '隐藏密码' : '显示密码'"
      :aria-pressed="visible"
      @click="toggle"
    >
      <svg
        v-if="visible"
        width="15"
        height="15"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="1.6"
        stroke-linecap="round"
        stroke-linejoin="round"
        style="flex: none"
        aria-hidden="true"
      >
        <path :d="EYE_OFF_PATH" />
      </svg>
      <Icon v-else name="eye" :size="15" />
    </button>
  </span>
</template>

<style scoped>
/* 描边与聚焦态全部走令牌，深色主题下随 --line/--focus 自动翻转，不手写取值 */
.x-password {
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
.x-password:hover:not(.is-disabled) { border-color: var(--line-strong); }
.x-password:focus-within {
  outline: 2px solid var(--focus);
  outline-offset: 2px;
  border-color: transparent;
}
.x-password.is-disabled { opacity: .6; background: var(--groove-bg); }

.x-password input {
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
.x-password input::placeholder { color: var(--ink-faint); }

/* 切换钮自己撑满高度并吃掉右侧圆角，与输入框共用一圈描边；
   inset 细线代替 border，避免和容器边框叠成两像素的粗缝 */
.x-password-toggle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  align-self: stretch;
  width: 38px;
  border-radius: 0 calc(var(--r-sm) - 1px) calc(var(--r-sm) - 1px) 0;
  color: var(--ink-faint);
  box-shadow: inset 1px 0 0 var(--line);
  transition: color .2s ease, background .2s ease;
}
.x-password-toggle:hover:not(:disabled) { color: var(--ink); background: var(--hover-bg); }
.x-password-toggle:disabled { opacity: .45; cursor: not-allowed; }
</style>
