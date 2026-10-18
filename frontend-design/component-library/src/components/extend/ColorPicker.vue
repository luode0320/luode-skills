<script setup lang="ts">
/* 取色器：色块按钮点开面板，预设色板、原生取色盘与十六进制输入三路同源。
   对外统一输出 #rrggbb 小写串，非法输入回滚到当前色。 */
import { computed, nextTick, onBeforeUnmount, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

/* 默认预设色板：一组常用色，调用方可用 presets 覆盖 */
const DEFAULT_PRESETS = [
  '#236de9', '#1d61d5', '#82dd2d', '#58a021', '#ff5a50', '#e0443b',
  '#f6e7c4', '#d7e7fb', '#e4dcf7', '#f7dce1', '#d8f0dc', '#596368',
]

const props = withDefaults(defineProps<{
  modelValue?: string
  presets?: string[]
  disabled?: boolean
  showText?: boolean
}>(), {
  showText: false,
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const trigger = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const text = ref('')
const pos = ref({ top: 0, left: 0 })

/** [参数] value 原始颜色串 [返回] 规范化的 #rrggbb 小写，非法时返回空串 */
function normalize(value: string): string {
  const raw = value.trim().replace(/^#/, '')
  if (/^[0-9a-fA-F]{3}$/.test(raw)) return `#${raw.split('').map(c => c + c).join('').toLowerCase()}`
  if (/^[0-9a-fA-F]{6}$/.test(raw)) return `#${raw.toLowerCase()}`
  return ''
}

/** [返回] 生效的预设色板 */
const swatches = computed(() => props.presets ?? DEFAULT_PRESETS)

/** [返回] 规范化后的当前色，非法时回落默认蓝 */
const current = computed(() => normalize(props.modelValue ?? '') || '#236de9')

watch(current, (value) => { text.value = value }, { immediate: true })

/** [参数] value 目标颜色 [返回] 无 */
function apply(value: string) {
  const hex = normalize(value)
  if (!hex) { text.value = current.value; return }
  text.value = hex
  emit('update:modelValue', hex)
}

/** [返回] 无 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 200
  const below = window.innerHeight - rect.bottom
  const top = below < height + 12 && rect.top > height + 12 ? rect.top - height - 6 : rect.bottom + 6
  const left = Math.max(8, Math.min(rect.left, window.innerWidth - 236))
  pos.value = { top, left }
}

/** [返回] 无 */
function bind() {
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/** [返回] 无 */
function unbind() {
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
}

/** [返回] 无 */
async function openMenu() {
  if (props.disabled || open.value) return
  open.value = true
  place()
  bind()
  await nextTick()
  place()
}

/** [参数] refocus 关闭后是否把焦点还给触发器 [返回] 无 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  unbind()
  if (refocus) trigger.value?.focus()
}

/** [参数] event 指针事件 [返回] 无 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

onBeforeUnmount(() => hide())
</script>

<template>
  <button
    ref="trigger"
    type="button"
    :class="['x-color', disabled && 'is-disabled']"
    :disabled="disabled"
    :aria-label="`当前颜色 ${current}`"
    @click="open ? hide(true) : openMenu()"
  >
    <span class="x-color-chip" :style="{ background: current }" />
    <span v-if="showText" class="x-color-text mono">{{ current }}</span>
    <Icon class="x-color-caret" name="chevronDown" :size="14" />
  </button>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-color-menu m-float"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(trigger) }"
      >
        <div class="x-color-grid">
          <button
            v-for="c in swatches"
            :key="c"
            type="button"
            class="x-color-cell"
            :class="{ 'is-active': normalize(c) === current }"
            :style="{ background: c }"
            :aria-label="c"
            @click="apply(c)"
          />
        </div>
        <div class="x-color-row">
          <input
            class="x-color-native"
            type="color"
            :value="current"
            aria-label="自定义颜色"
            @input="apply(($event.target as HTMLInputElement).value)"
          />
          <span class="input-shell x-color-hex">
            <span class="x-color-hash">#</span>
            <input
              :value="text.replace('#', '')"
              maxlength="6"
              aria-label="十六进制色值"
              @input="text = `#${($event.target as HTMLInputElement).value}`"
              @change="apply(text)"
              @keydown.enter="apply(text)"
            />
          </span>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.x-color {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  height: var(--control-h);
  padding: 0 10px;
  border: 1px solid var(--line-strong);
  border-radius: var(--r-sm);
  background: var(--input-bg);
  box-shadow: var(--edge);
  color: var(--ink-muted);
  cursor: pointer;
  transition: border-color .2s ease;
}
.x-color:hover { border-color: rgba(var(--shade), .18); }
.x-color.is-disabled { opacity: .6; cursor: not-allowed; background: var(--groove-bg); }
.x-color-chip { width: 18px; height: 18px; flex: none; border-radius: var(--r-xs); box-shadow: inset 0 0 0 1px var(--line-strong); }
.x-color-text { font-size: 12px; color: var(--ink); text-transform: uppercase; }
.x-color-caret { color: var(--ink-soft); }
.x-color-menu { position: fixed; z-index: 120; width: 216px; padding: 10px; border-radius: var(--r-md); }
.x-color-grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 6px; }
.x-color-cell {
  width: 100%;
  aspect-ratio: 1;
  padding: 0;
  border: 0;
  border-radius: var(--r-xs);
  box-shadow: inset 0 0 0 1px var(--line-strong);
  cursor: pointer;
}
.x-color-cell.is-active { box-shadow: inset 0 0 0 1px var(--line-strong), 0 0 0 2px var(--blue); }
.x-color-row { display: flex; align-items: center; gap: 8px; margin-top: 10px; }
.x-color-native {
  width: 32px;
  height: 32px;
  flex: none;
  padding: 0;
  border: 1px solid var(--line-strong);
  border-radius: var(--r-xs);
  background: var(--input-bg);
  cursor: pointer;
}
.x-color-hex { flex: 1; height: 32px; }
.x-color-hash { color: var(--ink-faint); }
</style>
