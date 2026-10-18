<script setup lang="ts">
/* 时间选择：触发区 + 下拉面板，面板里时 / 分两列滚动选择，底部提供「此刻」快捷。
   面板定位与关外逻辑照 Select.vue 的写法：Teleport 到 body + fixed 定位 + overlayEnter pop 语态。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  modelValue?: string
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
  format?: string
}>(), {
  placeholder: '选择时间',
  format: 'HH:mm:ss',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const HOURS = Array.from({ length: 24 }, (_, i) => String(i).padStart(2, '0'))
const MINUTES = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'))
const SECONDS = Array.from({ length: 60 }, (_, i) => String(i).padStart(2, '0'))

/* 小时与分钟两列滚动的 DOM 句柄，定值后把选中项滚到视野中央 */
const trigger = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const hourCol = ref<HTMLElement | null>(null)
const minuteCol = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0, width: 0 })

const parts = computed(() => {
  const raw = props.modelValue ?? ''
  const [h = '00', m = '00', s = '00'] = raw.split(':')
  return { h, m, s }
})

const hasSeconds = computed(() => /ss/i.test(props.format))

/* 触发区展示文本：按 format 决定是否带秒 */
const display = computed(() => {
  if (!props.modelValue) return ''
  return hasSeconds.value ? `${parts.value.h}:${parts.value.m}:${parts.value.s}` : `${parts.value.h}:${parts.value.m}`
})

/**
 * [参数] 无
 * [返回] 无：把面板贴到触发区下方，空间不足则翻上方，宽度对齐触发区
 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const panelHeight = panel.value?.offsetHeight ?? 220
  const below = window.innerHeight - rect.bottom
  const top = below < panelHeight + 12 && rect.top > panelHeight + 12 ? rect.top - panelHeight - 6 : rect.bottom + 6
  const width = Math.max(rect.width, 220)
  const left = Math.min(rect.left, window.innerWidth - width - 8)
  pos.value = { top, left, width }
}

/**
 * [参数] 无 [返回] 无：定值后把选中项滚到列中部
 */
function scrollToSelected() {
  nextTick(() => {
    hourCol.value?.querySelector('.is-selected')?.scrollIntoView({ block: 'center' })
    minuteCol.value?.querySelector('.is-selected')?.scrollIntoView({ block: 'center' })
  })
}

/** [参数] 无 [返回] 无：打开面板并绑定关外监听 */
async function show() {
  if (props.disabled || open.value) return
  open.value = true
  place()
  await nextTick()
  place()
  scrollToSelected()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/** [参数] refocus 关闭后是否把焦点还给触发区 [返回] 无：收起面板并摘监听 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
  if (refocus) trigger.value?.focus()
}

/** [参数] event 指针事件 [返回] 无：点在触发区与面板之外才收 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || panel.value?.contains(target)) return
  hide()
}

/**
 * [参数] which 'h' | 'm' | 's' 改哪一段，value 新值
 * [返回] 无：按 format 拼出完整时间串回写
 */
function pick(which: 'h' | 'm' | 's', value: string) {
  const next = { ...parts.value, [which]: value }
  if (which === 'h') next.m = next.m || '00'
  const text = hasSeconds.value ? `${next.h}:${next.m}:${next.s}` : `${next.h}:${next.m}`
  emit('update:modelValue', text)
  scrollToSelected()
}

/** [参数] 无 [返回] 无：取当前系统时间填入 */
function useNow() {
  const now = new Date()
  const h = String(now.getHours()).padStart(2, '0')
  const m = String(now.getMinutes()).padStart(2, '0')
  const s = String(now.getSeconds()).padStart(2, '0')
  emit('update:modelValue', hasSeconds.value ? `${h}:${m}:${s}` : `${h}:${m}`)
  scrollToSelected()
}

/** [参数] 无 [返回] 无：清空值 */
function clear() {
  emit('update:modelValue', '')
}

/** [参数] event 键盘事件 [返回] 无：回车 / 空格开面板，Esc 关闭 */
function onKey(event: KeyboardEvent) {
  if (event.key === 'Escape' && open.value) {
    event.preventDefault()
    hide(true)
  } else if (!open.value && ['Enter', ' '].includes(event.key)) {
    event.preventDefault()
    show()
  }
}

onBeforeUnmount(() => hide())
</script>

<template>
  <div class="x-timepicker">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-time-trigger', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="dialog"
      :aria-expanded="open"
      @click="open ? hide() : show()"
      @keydown="onKey"
    >
      <Icon name="clock" :size="15" />
      <span :class="['x-time-value', !display && 'is-placeholder']">{{ display || placeholder }}</span>
      <span
        v-if="clearable && modelValue && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else name="chevronDown" :size="15" class="x-time-caret" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="panel"
          class="x-time-panel m-float"
          role="dialog"
          aria-label="时间选择"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, width: `${pos.width}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <div class="x-time-cols">
            <ul ref="hourCol" class="x-time-col" role="listbox" aria-label="小时">
              <li
                v-for="h in HOURS"
                :key="h"
                role="option"
                :aria-selected="h === parts.h"
                :class="['x-time-opt', 'tnum', h === parts.h && 'is-selected']"
                @click="pick('h', h)"
              >{{ h }}</li>
            </ul>
            <ul ref="minuteCol" class="x-time-col" role="listbox" aria-label="分钟">
              <li
                v-for="m in MINUTES"
                :key="m"
                role="option"
                :aria-selected="m === parts.m"
                :class="['x-time-opt', 'tnum', m === parts.m && 'is-selected']"
                @click="pick('m', m)"
              >{{ m }}</li>
            </ul>
            <ul v-if="hasSeconds" class="x-time-col" role="listbox" aria-label="秒">
              <li
                v-for="s in SECONDS"
                :key="s"
                role="option"
                :aria-selected="s === parts.s"
                :class="['x-time-opt', 'tnum', s === parts.s && 'is-selected']"
                @click="pick('s', s)"
              >{{ s }}</li>
            </ul>
          </div>
          <div class="x-time-foot">
            <button type="button" class="btn btn-text btn-sm" @click="useNow">此刻</button>
            <button type="button" class="btn btn-primary btn-sm" @click="hide(true)">确定</button>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-timepicker { display: inline-flex; width: 100%; }
.x-time-trigger { width: 100%; cursor: pointer; justify-content: space-between; text-align: left; color: var(--ink); }
.x-time-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-time-value.is-placeholder { color: var(--ink-faint); }
.x-time-caret { color: var(--ink-soft); flex: none; }
.x-time-panel { border-radius: var(--r-md); padding: 10px; }
.x-time-cols { display: flex; gap: 6px; height: 200px; }
.x-time-col {
  flex: 1;
  margin: 0;
  padding: 4px;
  list-style: none;
  overflow-y: auto;
  overscroll-behavior: contain;
  border-radius: var(--r-sm);
  background: var(--groove-bg);
  box-shadow: var(--groove-inset);
}
.x-time-opt {
  height: 30px;
  line-height: 30px;
  text-align: center;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink-muted);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-time-opt:hover { background: var(--hover-bg); color: var(--ink); }
.x-time-opt.is-selected { background: var(--blue); color: var(--plate-ink); font-weight: 620; }
.x-time-foot {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid var(--line);
}
</style>
