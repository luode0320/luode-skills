<script setup lang="ts">
/* 菜单节点：菜单的递归单元，自身承载子项列表。
   展开与选中是两条独立状态：展开只影响子列表可见性，选中由 Menu 统一上抛；
   折叠态或横向模式下子菜单改为浮层浮出，避免把父级列表撑开。 */
import { computed, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { EASE, gsap, motionSkipped } from '@/composables/motion'

/* 与 Menu.vue 的 MenuItem 保持同一结构：只描述本节点消费的字段，递归由 children 自引用 */
interface MenuNodeItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
  children?: MenuNodeItem[]
}

const props = defineProps<{
  item: MenuNodeItem
  /** 缩进层级，0 为顶层 */
  depth: number
  vertical: boolean
  collapsed?: boolean
  selected?: string
}>()

const emit = defineEmits<{ (e: 'select', key: string): void }>()

const expanded = ref(false)
const hovered = ref(false)

/** [参数] 无 [返回] 该节点是否含子项 */
const hasChildren = computed(() => Boolean(props.item.children?.length))
/** [参数] 无 [返回] 是否只留图标，折叠的纵向导航成立 */
const iconOnly = computed(() => Boolean(props.collapsed) && props.vertical)
/** [参数] 无 [返回] 子菜单是否改用浮层：横向模式或折叠态成立 */
const floating = computed(() => !props.vertical || Boolean(props.collapsed))
/** [参数] 无 [返回] 子列表当前是否可见，浮层态跟随悬停、内联态跟随点击 */
const subOpen = computed(() => hasChildren.value && (floating.value ? hovered.value : expanded.value))
/** [参数] 无 [返回] 层级缩进，折叠态不缩进 */
const indent = computed(() => (iconOnly.value ? 10 : 10 + props.depth * 14))

/** [参数] 无 [返回] 无；叶子节点派发选中，含子项节点切换内联展开态 */
function activate() {
  if (props.item.disabled) return
  if (hasChildren.value) {
    if (!floating.value) expanded.value = !expanded.value
    return
  }
  emit('select', props.item.key)
}

/* 展开形变：子菜单是「被拉开」而不是「瞬间出现」。
   用高度 0 → auto 的过渡，和 CollapseItem 同一套语式（展开 Unfold）。
   收起同样走一遍——v-if 直接卸载会让整块凭空消失，这正是「僵硬」的来源。 */
function onSubEnter(el: Element) {
  if (motionSkipped()) return
  gsap.fromTo(
    el,
    { height: 0, opacity: 0 },
    { height: 'auto', opacity: 1, duration: 0.24, ease: EASE.swap, clearProps: 'height', overwrite: true },
  )
}

function onSubLeave(el: Element, done: () => void) {
  if (motionSkipped()) { done(); return }
  gsap.to(el, { height: 0, opacity: 0, duration: 0.18, ease: EASE.exit, overwrite: true, onComplete: done })
}

/** [参数] key 子节点派发上来的选中项 [返回] 无；继续向上冒泡 */
function relay(key: string) {
  emit('select', key)
}

/** [参数] 无 [返回] 无；浮层态悬停展开子菜单 */
function onEnter() {
  if (floating.value) hovered.value = true
}

/** [参数] 无 [返回] 无；浮层态移出收起子菜单 */
function onLeave() {
  if (floating.value) hovered.value = false
}
</script>

<template>
  <li
    :class="['x-menu-node', floating && 'is-floating', !vertical && 'is-horizontal']"
    @pointerenter="onEnter"
    @pointerleave="onLeave"
  >
    <button
      type="button"
      role="menuitem"
      :class="['x-menu-item', item.key === selected && 'is-active']"
      :style="{ paddingLeft: `${indent}px` }"
      :disabled="item.disabled"
      :title="iconOnly ? item.label : undefined"
      :aria-expanded="hasChildren ? subOpen : undefined"
      @click="activate"
    >
      <Icon v-if="item.icon" :name="item.icon" :size="16" />
      <span v-if="!iconOnly" class="x-menu-label">{{ item.label }}</span>
      <Icon
        v-if="hasChildren && !floating"
        class="x-menu-caret"
        :class="{ 'is-open': subOpen }"
        name="chevronDown"
        :size="14"
      />
    </button>
    <Transition :css="false" @enter="onSubEnter" @leave="onSubLeave">
      <ul v-if="subOpen" :class="['x-menu-sub', floating && 'm-float']" role="menu">
        <MenuNode
          v-for="child in item.children"
          :key="child.key"
          :item="child"
          :depth="depth + 1"
          :vertical="vertical"
          :collapsed="collapsed"
          :selected="selected"
          @select="relay"
        />
      </ul>
    </Transition>
  </li>
</template>

<style scoped>
.x-menu-node { position: relative; list-style: none; }
.x-menu-item {
  display: flex;
  align-items: center;
  gap: 9px;
  width: 100%;
  height: var(--control-h);
  /* 左内边距由行内缩进按层级覆盖，右侧必须同值收口：横向模式下按钮宽度贴合内容，
     缺右内边距会让文字末尾直接贴到选中底色块的右边缘（实测 padR=0）。 */
  padding-right: 10px;
  border-radius: var(--r-xs);
  font-size: var(--fs-body);
  color: var(--ink-muted);
  text-align: left;
  transition: background .18s var(--ease-reveal), color .18s var(--ease-reveal);
}
.x-menu-item:hover:not(:disabled) { background: var(--hover-bg); color: var(--ink); }
.x-menu-item.is-active { background: var(--blue-soft); color: var(--blue); font-weight: 620; }
.x-menu-item:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-menu-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.x-menu-caret { color: var(--ink-faint); transition: transform .24s var(--ease-premium); }
.x-menu-caret.is-open { transform: rotate(180deg); }
/* 子菜单是「被拉开」的：高度 0 ↔ auto 由 Transition 钩子驱动（见 onEnter / onLeave），
   这里只负责裁切与原点。早先做的是「子项逐条落下」，但收起仍是 v-if 瞬删，
   一半有动效一半没有，反而更显僵硬——改为双向高度形变后两端一致。 */
.x-menu-sub {
  margin: 0;
  padding: 0;
  list-style: none;
  overflow: hidden;
  transform-origin: top center;
}
/* 浮层子菜单：折叠态贴节点右侧，横向菜单贴节点下方 */
.x-menu-node.is-floating > .x-menu-sub {
  position: absolute;
  z-index: 120;
  min-width: 168px;
  padding: 6px;
  border-radius: var(--r-md);
}
.x-menu-node.is-floating:not(.is-horizontal) > .x-menu-sub { left: 100%; top: 0; }
.x-menu-node.is-floating.is-horizontal > .x-menu-sub { left: 0; top: 100%; }
</style>
