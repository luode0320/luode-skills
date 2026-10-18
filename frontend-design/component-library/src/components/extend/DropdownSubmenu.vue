<script setup lang="ts">
/* 下拉子菜单：把一组二级选项收在一个菜单项后面，指针悬停时在右侧浮出面板。
   它只负责「一级项 + 二级面板」这一段，不含触发按钮与整体开合，
   因此 Dropdown / DropdownButton / Menu 这类宿主可以直接把 items 里的一项换成它来获得二级结构。
   面板用 Teleport 到 body：宿主菜单本身常带 overflow 裁剪，留在原地会被切掉右半边。 */
import { nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface SubMenuItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<{
  label: string
  items: SubMenuItem[]
  disabled?: boolean
}>(), {
  disabled: false,
})

const emit = defineEmits<{ (e: 'select', key: string): void }>()

const triggerEl = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
let timer: number | undefined

/**
 * [参数] 无
 * [返回] 无。面板贴在一级项右侧；右边放不下就翻到左侧，上下再夹进视口，
 * 这样靠近屏幕边缘的宿主菜单也不会让二级面板被裁掉
 */
function place() {
  const rect = triggerEl.value?.getBoundingClientRect()
  if (!rect) return
  const height = panel.value?.offsetHeight ?? 0
  const width = panel.value?.offsetWidth ?? 160
  const gap = 4
  const left = rect.right + gap + width > window.innerWidth - 8 ? rect.left - width - gap : rect.right + gap
  const top = Math.min(rect.top, window.innerHeight - height - 8)
  pos.value = { top: Math.max(8, top), left: Math.max(8, left) }
}

/**
 * [参数] 无
 * [返回] 无。延迟一点再浮出：指针横扫过整列菜单时不会把每个子项都闪一下面板
 */
function show() {
  if (props.disabled) return
  window.clearTimeout(timer)
  timer = window.setTimeout(async () => {
    open.value = true
    place()
    await nextTick()
    place()
  }, 120)
}

/**
 * [参数] 无
 * [返回] 无。同样延迟收起，给指针从一级项移进面板留出通过时间
 */
function hide() {
  window.clearTimeout(timer)
  timer = window.setTimeout(() => { open.value = false }, 120)
}

/**
 * [参数] 无
 * [返回] 无。指针已进入面板，撤销待执行的收起，否则面板会在鼠标还没点到选项时先消失
 */
function keepOpen() {
  window.clearTimeout(timer)
}

/**
 * [参数] item 被点的二级选项
 * [返回] 无。禁用项不派发；选中后收起面板，并把选择交给宿主处理
 */
function pick(item: SubMenuItem) {
  if (item.disabled) return
  emit('select', item.key)
  window.clearTimeout(timer)
  open.value = false
}

onBeforeUnmount(() => {
  window.clearTimeout(timer)
  open.value = false
})
</script>

<template>
  <div
    ref="triggerEl"
    :class="['x-submenu', disabled && 'is-disabled', open && 'is-open']"
    role="menuitem"
    aria-haspopup="menu"
    :aria-expanded="open"
    :aria-disabled="disabled || undefined"
    @pointerenter="show"
    @pointerleave="hide"
    @focusin="show"
    @focusout="hide"
  >
    <span class="x-submenu-label">{{ label }}</span>
    <Icon name="chevronRight" :size="14" />
  </div>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="panel"
        class="x-submenu-panel m-float"
        role="menu"
        :aria-label="label"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: floatingLayerFor(triggerEl) }"
        @pointerenter="keepOpen"
        @pointerleave="hide"
      >
        <button
          v-for="item in items"
          :key="item.key"
          type="button"
          role="menuitem"
          class="x-submenu-item"
          :disabled="item.disabled"
          @click="pick(item)"
        >
          <Icon v-if="item.icon" :name="item.icon" :size="15" />
          <span class="x-submenu-text">{{ item.label }}</span>
        </button>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* 一级项：与 Dropdown 的 item 同一套尺寸，替换进去后菜单行高不会突然变化 */
.x-submenu {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 9px;
  width: 100%;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  cursor: pointer;
  transition: background var(--ease-premium) .15s, color var(--ease-premium) .15s;
}
.x-submenu:hover:not(.is-disabled),
.x-submenu.is-open { background: var(--hover-bg); }
.x-submenu.is-disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-submenu-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-submenu-panel {
  position: fixed;
  min-width: 160px;
  padding: 6px;
  border-radius: var(--r-md);
  display: flex;
  flex-direction: column;
}
.x-submenu-item {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  min-height: 34px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  text-align: left;
  transition: background var(--ease-premium) .15s, color var(--ease-premium) .15s;
}
.x-submenu-item:hover:not(:disabled) { background: var(--hover-bg); }
.x-submenu-item:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-submenu-text { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
</style>
