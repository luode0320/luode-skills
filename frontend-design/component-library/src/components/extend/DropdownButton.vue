<script setup lang="ts">
/* 下拉按钮：按钮主体点一下走默认动作，右侧小箭头单独点开菜单，两件事互不干扰。
   存在的理由就是「主操作 + 次要选项」并列时不必让用户先展开再点两次；
   定位、翻转与外部关闭沿用 Dropdown 的 place() 口径，菜单 Teleport 到 body 并跟随所在浮层层级。 */
import { nextTick, onBeforeUnmount, ref } from 'vue'
import Button from '@/components/ui/Button.vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface DropdownButtonItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
  /** 在该项上方补一条分隔线，用于分组 */
  divided?: boolean
}

const props = withDefaults(defineProps<{
  items: DropdownButtonItem[]
  type?: 'primary' | 'secondary' | 'ghost' | 'text' | 'danger'
}>(), {
  type: 'secondary',
})

const emit = defineEmits<{
  (e: 'click'): void
  (e: 'select', key: string): void
}>()

const triggerEl = ref<HTMLElement | null>(null)
const menu = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0, width: 0 })

/**
 * [参数] 无
 * [返回] 无。按触发区包围盒定位菜单；下方空间不足就翻到上方，左右再夹进视口，
 * 保证菜单既不会跑到屏幕外，也不会和按钮重叠
 */
function place() {
  const rect = triggerEl.value?.getBoundingClientRect()
  if (!rect) return
  const height = menu.value?.offsetHeight ?? 0
  const width = Math.max(rect.width, 160)
  const gap = 6
  const top = window.innerHeight - rect.bottom < height + gap ? rect.top - height - gap : rect.bottom + gap
  const left = Math.min(rect.left, window.innerWidth - width - 8)
  pos.value = { top: Math.max(8, top), left: Math.max(8, left), width }
}

/**
 * [参数] 无
 * [返回] 无。先渲染再量高再定位：菜单高度只有挂载后才知道，一次 nextTick 后的二次 place 才不会跳位
 */
async function show() {
  if (open.value) return
  open.value = true
  place()
  await nextTick()
  place()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/**
 * [参数] 无
 * [返回] 无。收起菜单并撤掉全局监听，防止关掉后还留着定位开销
 */
function hide() {
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
}

/**
 * [参数] 无
 * [返回] 无。箭头独立开关，不触碰主体动作，这正是本组件与普通 Dropdown 的关键差别
 */
function toggle() {
  if (open.value) hide()
  else show()
}

/**
 * [参数] item 被点的选项
 * [返回] 无。禁用项既不派发也不关闭，用户能明确感到这一项点不动
 */
function pick(item: DropdownButtonItem) {
  if (item.disabled) return
  emit('select', item.key)
  hide()
}

/**
 * [参数] event 全局指针按下事件
 * [返回] 无。落在触发区或菜单内不关，避免点菜单时先被判定成外部点击
 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (triggerEl.value?.contains(target) || menu.value?.contains(target)) return
  hide()
}

/**
 * [参数] 无
 * [返回] 无。主体点击只派发事件，由调用方决定默认动作，组件不自带行为
 */
function onMain() {
  emit('click')
}

onBeforeUnmount(hide)
</script>

<template>
  <span ref="triggerEl" class="x-dbtn">
    <Button :variant="type" class="x-dbtn-main" @click="onMain">
      <slot />
    </Button>
    <Button
      :variant="type"
      class="x-dbtn-arrow"
      :aria-expanded="open"
      aria-haspopup="menu"
      aria-label="展开菜单"
      @click="toggle"
    >
      <Icon name="chevronDown" :size="14" />
    </Button>
  </span>
  <Teleport to="body">
    <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
      <div
        v-if="open"
        ref="menu"
        class="x-dbtn-menu m-float"
        role="menu"
        :style="{ top: `${pos.top}px`, left: `${pos.left}px`, minWidth: `${pos.width}px`, zIndex: floatingLayerFor(triggerEl) }"
      >
        <button
          v-for="item in items"
          :key="item.key"
          type="button"
          role="menuitem"
          :class="['x-dbtn-item', item.divided && 'is-divided']"
          :disabled="item.disabled"
          @click="pick(item)"
        >
          <Icon v-if="item.icon" :name="item.icon" :size="15" />
          <span class="x-dbtn-label">{{ item.label }}</span>
        </button>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
/* 两段按钮拼成一个整体：靠内侧圆角归零 + 一条分隔线，视觉上仍读作一个控件 */
.x-dbtn { display: inline-flex; }
.x-dbtn :deep(.x-dbtn-main) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.x-dbtn :deep(.x-dbtn-arrow) {
  width: 30px;
  padding: 0;
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
  box-shadow: inset 1px 0 0 var(--line);
}
.x-dbtn-menu {
  position: fixed;
  padding: 6px;
  border-radius: var(--r-md);
  display: flex;
  flex-direction: column;
}
.x-dbtn-item {
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
.x-dbtn-item:hover:not(:disabled) { background: var(--hover-bg); }
.x-dbtn-item:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-dbtn-item.is-divided { margin-top: 6px; border-top: 1px solid var(--line); padding-top: 6px; }
.x-dbtn-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
</style>
