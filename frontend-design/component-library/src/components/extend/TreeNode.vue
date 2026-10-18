<script setup lang="ts">
/* 树的递归单元：一行 = 展开箭头 + 可选复选框 + 图标 + 标签，下方按需渲染子级。
   行为全部回读 Tree 注入的上下文，本组件不持有任何状态，
   因此任意深度的节点口径一致，也不会出现父子两套展开 / 勾选真相。
   独立挂载（如组件核对页）时无父级上下文，上下文给 null 兜底并整体降级为只读展示。
   exemption: 行内展开 / 勾选 / 键盘三套事件的绑定与焦点往返同属一个节点行单元，拆开反而割裂可读性。 */
import { computed, inject } from 'vue'
import Icon from '@/components/Icon.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import type { TreeCheckState, TreeContext, TreeKey, TreeNode } from './Tree.vue'

const props = defineProps<{
  node: TreeNode
  /** 缩进层级，0 为顶层 */
  depth: number
  /** 父节点 key，用于键盘左方向键回到父级；顶层为 null */
  parentKey: TreeKey | null
}>()

/* 行首留白与箭头宽度合成缩进步长，引导线位置由同一步长推导，两者始终对齐 */
const INDENT = 20
const ARROW = 16

/* 独立挂载时没有父级 provide，给 null 兜底，避免 Vue 输出 injection 缺失告警 */
const ctx = inject<TreeContext | null>('xTree', null)

/** [参数] 无 [返回] 该节点是否含可展开子级；显式 isLeaf 优先于 children */
const hasChildren = computed(() => Boolean(props.node.children?.length) && !props.node.isLeaf)

/** [参数] 无 [返回] 当前是否展开；无上下文时按静态展开展示全部层级 */
const open = computed(() => (ctx ? ctx.isExpanded(props.node) : hasChildren.value))

/** [参数] 无 [返回] 勾选态；无上下文时视为未勾选 */
const state = computed<TreeCheckState>(() => ctx?.checkState(props.node) ?? { all: false, some: false })

/** [参数] 无 [返回] 是否处于选中态 */
const selected = computed(() => ctx?.isSelected(props.node.key) ?? false)

/** [参数] 无 [返回] 行是否可进入 Tab 序列：roving tabindex，整棵树只留一个可 Tab 落点 */
const tabbable = computed(() => (ctx?.focusKey.value ?? ctx?.firstKey.value) === props.node.key)

/** [参数] 无 [返回] 行内缩进，随层级线性增长 */
const indent = computed(() => 8 + props.depth * INDENT)

/** [参数] 无 [返回] 子级容器上引导线的横向位置，对准父级箭头中心 */
const guide = computed(() => `${indent.value + ARROW / 2}px`)

/**
 * [参数] 无
 * [返回] 标签按过滤词切好的片段序列，命中片段单独标记以便高亮
 *         逐段切分而非替换成 HTML 字符串，避免把标签当富文本渲染引入注入面
 */
const parts = computed(() => {
  const label = props.node.label
  const q = ctx?.query.value ?? ''
  const hit: Array<{ text: string; hit: boolean }> = []
  if (!q) return [{ text: label, hit: false }]
  const lower = label.toLowerCase()
  let at = 0
  while (at < label.length) {
    const found = lower.indexOf(q, at)
    if (found < 0) { hit.push({ text: label.slice(at), hit: false }); break }
    if (found > at) hit.push({ text: label.slice(at, found), hit: false })
    hit.push({ text: label.slice(found, found + q.length), hit: true })
    at = found + q.length
  }
  return hit
})

/** [参数] 无 [返回] 无；箭头就地切换展开态，不冒泡成选中 */
function onArrow() {
  if (props.node.disabled) return
  ctx?.toggleExpand(props.node)
}

/** [参数] 无 [返回] 无；整行点击走选中逻辑 */
function onRow() {
  ctx?.pick(props.node)
}

/** [参数] el 行元素或 null [返回] 无；行元素登记进父级焦点表，卸载时传 null 摘除 */
function bindRow(el: unknown) {
  ctx?.registerRow(props.node.key, el instanceof HTMLElement ? el : null)
}

/**
 * [参数] event 键盘事件
 * [返回] 无；上下按可见顺序移动，左右展开收起或进出层级，回车 / 空格选中
 *         左右键在「无子级可进 / 无父级可退」时不拦截默认行为，避免键盘用户被困在树内
 */
function onKey(event: KeyboardEvent) {
  if (!ctx) return
  const key = event.key
  const move = key === 'ArrowDown' ? 1 : key === 'ArrowUp' ? -1 : 0
  if (move) {
    event.preventDefault()
    ctx.step(props.node.key, move)
    return
  }
  if (key === 'ArrowRight' && hasChildren.value && !open.value) {
    event.preventDefault()
    ctx.toggleExpand(props.node)
  } else if (key === 'ArrowLeft') {
    if (hasChildren.value && open.value) {
      event.preventDefault()
      ctx.toggleExpand(props.node)
    } else if (props.parentKey !== null) {
      event.preventDefault()
      ctx.focusAt(props.parentKey)
    }
  } else if (key === 'Enter' || key === ' ') {
    event.preventDefault()
    ctx.pick(props.node)
  }
}

/* 子级只保留可见节点：过滤态下未命中路径的分支整体退出，不渲染空壳行 */
const visibleChildren = computed(() => (props.node.children ?? []).filter(child => ctx?.visible(child) ?? true))
</script>

<template>
  <li class="x-tree-node" role="none">
    <div
      :ref="bindRow"
      :class="['x-tree-row', selected && 'is-selected', node.disabled && 'is-disabled']"
      role="treeitem"
      :tabindex="tabbable ? 0 : -1"
      :aria-level="depth + 1"
      :aria-selected="selected"
      :aria-expanded="hasChildren ? open : undefined"
      :aria-disabled="node.disabled || undefined"
      :style="{ paddingLeft: `${indent}px` }"
      @click="onRow"
      @keydown="onKey"
    >
      <button
        v-if="hasChildren"
        type="button"
        :class="['x-tree-arrow', open && 'is-open']"
        :aria-label="open ? '收起' : '展开'"
        :disabled="node.disabled"
        @click.stop="onArrow"
      ><Icon name="chevronRight" :size="13" /></button>
      <span v-else class="x-tree-arrow is-blank" aria-hidden="true" />

      <Checkbox
        v-if="ctx?.checkable.value"
        :model-value="state.all"
        :indeterminate="state.some"
        :disabled="node.disabled"
        :aria-label="`选择 ${node.label}`"
        @update:model-value="ctx?.toggleCheck(node)"
      />
      <Icon v-if="node.icon" :name="node.icon" :size="15" class="x-tree-icon" />
      <span class="x-tree-label">
        <template v-for="(part, i) in parts" :key="i">
          <mark v-if="part.hit" class="x-tree-hit">{{ part.text }}</mark>
          <template v-else>{{ part.text }}</template>
        </template>
      </span>
    </div>

    <ul
      v-if="hasChildren && open && visibleChildren.length"
      class="x-tree-children"
      role="group"
      :style="{ '--x-tree-guide': guide }"
    >
      <!-- 递归自引用：按文件名解析到本组件，子级行为与父级天然一致 -->
      <TreeNode
        v-for="child in visibleChildren"
        :key="child.key"
        :node="child"
        :depth="depth + 1"
        :parent-key="node.key"
      />
    </ul>
  </li>
</template>

<style scoped>
.x-tree-node { list-style: none; }
.x-tree-row {
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding-right: 10px;
  border-radius: var(--r-xs);
  color: var(--ink);
  cursor: pointer;
  transition: background var(--ease-premium) .2s, color var(--ease-premium) .2s;
}
.x-tree-row:hover { background: var(--hover-bg); }
.x-tree-row.is-selected { background: var(--blue-soft); color: var(--blue); font-weight: 620; }
.x-tree-row.is-disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-tree-row:focus-visible { outline: 2px solid var(--focus); outline-offset: -2px; }
.x-tree-arrow {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 16px;
  flex: none;
  color: var(--ink-soft);
  transition: transform var(--ease-premium) .3s, color var(--ease-premium) .2s;
}
.x-tree-arrow.is-open { transform: rotate(90deg); }
.x-tree-arrow.is-blank { pointer-events: none; }
.x-tree-icon { flex: none; color: var(--ink-soft); }
.x-tree-label { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
/* 命中片段只改底色与字重，不换色相，避免与选中态的语义色互相干扰 */
.x-tree-hit { background: transparent; color: var(--blue); font-weight: 680; }
.x-tree-children { margin: 0; padding: 0; list-style: none; }
</style>
