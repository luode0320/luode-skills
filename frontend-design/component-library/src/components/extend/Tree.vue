<script setup lang="ts">
/* 通用递归树：只认 key/label/children 这套通用结构，不绑定任何业务数据模型，
   因此可以被部门、菜单、分类等任意层级数据复用。
   展开集合与勾选集合都收敛在本组件，递归子节点通过 provide 注入的上下文回读，
   任意深度的节点行为一致，子组件不必层层透传 props（沿用 Collapse / CollapseItem 的口径）。
   勾选口径：modelValue 是唯一真相源，本组件不另存一份勾选镜像。
   父节点只有在「自身与全部后代都在集合里」时才算勾上，半选态由当场推导得出；
   勾满子树后向上回填已满的祖先，但绝不写入未满的祖先——否则 modelValue 里会混进
   既非全选也非未选的中间态，外部拿到这份数组无法还原界面。
   选中与勾选共用同一个 modelValue（对外只有一个 v-model），同时开启两种能力时两者会写同一个数组，
   需要分别受控时应拆成两次使用。
   exemption: 递归索引、展开 / 勾选 / 半选推导与键盘导航同属一棵树的交互单元，拆文件会割裂这套状态口径。 */
import { computed, provide, ref, watch, type ComputedRef, type Ref } from 'vue'
import TreeNodeItem from './TreeNode.vue'

/** 树节点：children 自引用构成任意深度，isLeaf 用于「有子项但不可展开」的场景 */
export interface TreeNode {
  key: string | number
  label: string
  children?: TreeNode[]
  disabled?: boolean
  icon?: string
  /** 显式声明为叶子：即使带 children 也不显示展开箭头、不渲染下级 */
  isLeaf?: boolean
}

export type TreeKey = string | number
/** 勾选态：all 全选，some 半选（有后代命中但未满） */
export type TreeCheckState = { all: boolean; some: boolean }

/* 递归子节点据此回读父级状态并回调，本组件是这些能力的唯一实现方 */
export interface TreeContext {
  checkable: ComputedRef<boolean>
  query: ComputedRef<string>
  focusKey: Ref<TreeKey | null>
  firstKey: ComputedRef<TreeKey | null>
  isExpanded: (node: TreeNode) => boolean
  toggleExpand: (node: TreeNode) => void
  isSelected: (key: TreeKey) => boolean
  pick: (node: TreeNode) => void
  checkState: (node: TreeNode) => TreeCheckState
  toggleCheck: (node: TreeNode) => void
  visible: (node: TreeNode) => boolean
  focusAt: (key: TreeKey) => void
  step: (key: TreeKey, delta: number) => void
  registerRow: (key: TreeKey, el: HTMLElement | null) => void
}

const props = withDefaults(defineProps<{
  data: TreeNode[]
  /** 选中 / 勾选的 key 数组 */
  modelValue?: TreeKey[]
  checkable?: boolean
  /** 点节点即写入 modelValue */
  selectable?: boolean
  /** 多选：再点一次取消该项；关闭时每次只保留一项 */
  multiple?: boolean
  defaultExpandAll?: boolean
  /** 展开层级间画引导竖线 */
  showLine?: boolean
  /** 高亮过滤词，命中节点与其祖先路径保留，其余隐藏 */
  filterText?: string
}>(), {
  modelValue: () => [],
  checkable: false,
  selectable: true,
  multiple: false,
  defaultExpandAll: false,
  showLine: false,
  filterText: '',
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: TreeKey[]): void
  (e: 'select', key: TreeKey): void
  (e: 'check', keys: TreeKey[]): void
  (e: 'expand', keys: TreeKey[]): void
}>()

/** [参数] nodes 根列表 [返回] 子→父映射与可展开 key 表，勾选回填与展开播种共用同一次遍历 */
function indexTree(nodes: TreeNode[]) {
  const parents = new Map<TreeKey, TreeNode>()
  const expandable: TreeKey[] = []
  const walk = (list: TreeNode[]) => list.forEach((node) => {
    if (!node.children?.length) return
    expandable.push(node.key)
    node.children.forEach((child) => { parents.set(child.key, node); walk([child]) })
  })
  walk(nodes)
  return { parents, expandable }
}

/** [参数] node 节点 [返回] 含自身与全部后代的 key，勾选联动的基本单位 */
function keysOf(node: TreeNode): TreeKey[] {
  return [node.key, ...(node.children ?? []).flatMap(keysOf)]
}

const expanded = ref<Set<TreeKey>>(new Set())
const tree = computed(() => indexTree(props.data))
const checked = computed(() => new Set(props.modelValue))
const query = computed(() => props.filterText.trim().toLowerCase())
const selectedKeys = computed(() => new Set(props.modelValue))

/* 数据异步到达时 defaultExpandAll 需要补播种，所以 immediate 也要跑一次；
   同时剔除已消失的 key，否则换数据源会残留上一棵树的展开态，表现为「点开是空的」 */
watch(() => props.data, (list) => {
  const alive = new Set(indexTree(list).expandable)
  const next = new Set([...expanded.value].filter(key => alive.has(key)))
  if (props.defaultExpandAll) alive.forEach(key => next.add(key))
  expanded.value = next
}, { immediate: true })

/** [参数] node 节点 [返回] 自身标签是否命中过滤词 */
function selfHit(node: TreeNode) {
  return Boolean(query.value) && node.label.toLowerCase().includes(query.value)
}

/** [参数] node 节点 [返回] 是否有任一后代命中；命中则自身必须留在树上充当路径 */
function childHit(node: TreeNode): boolean {
  return Boolean(query.value) && (node.children ?? []).some(child => selfHit(child) || childHit(child))
}

/** [参数] node 节点 [返回] 该节点是否渲染（无过滤时全部渲染） */
function visible(node: TreeNode) {
  return !query.value || selfHit(node) || childHit(node)
}

/** [参数] node 节点 [返回] 是否展开；过滤态由命中路径强制展开，否则结果藏在折叠里看不见 */
function isExpanded(node: TreeNode) {
  return query.value ? childHit(node) : expanded.value.has(node.key)
}

/** [参数] node 节点 [返回] 全选 / 半选态，直接由 modelValue 推导，不额外维护中间状态 */
function checkState(node: TreeNode): TreeCheckState {
  const ids = keysOf(node)
  const on = ids.filter(id => checked.value.has(id)).length
  return { all: on === ids.length, some: on > 0 && on < ids.length }
}

/** [参数] node 节点 [返回] 无；展开集合是本地状态，切换后把快照整体上抛 */
function toggleExpand(node: TreeNode) {
  const next = new Set(expanded.value)
  if (next.has(node.key)) next.delete(node.key)
  else next.add(node.key)
  expanded.value = next
  emit('expand', [...next])
}

/** [参数] set 待回填的集合 [参数] key 起点 [返回] 无；自下而上补进已勾满的祖先，遇到未满即停 */
function fillParents(set: Set<TreeKey>, key: TreeKey) {
  let parent = tree.value.parents.get(key)
  while (parent) {
    if (!keysOf(parent).every(id => set.has(id))) break
    set.add(parent.key)
    parent = tree.value.parents.get(parent.key)
  }
}

/** [参数] node 节点 [返回] 无；整棵子树全选则整体取消，否则整体勾上并回填已满祖先 */
function toggleCheck(node: TreeNode) {
  if (node.disabled) return
  const set = new Set(props.modelValue)
  const ids = keysOf(node)
  if (ids.every(id => set.has(id))) ids.forEach(id => set.delete(id))
  else {
    ids.forEach(id => set.add(id))
    fillParents(set, node.key)
  }
  emit('update:modelValue', [...set])
  emit('check', [...set])
}

/** [参数] node 节点 [返回] 无；多选切进切出，单选整体替换 */
function pick(node: TreeNode) {
  if (node.disabled || !props.selectable) return
  const list = props.modelValue
  const next = props.multiple
    ? (list.includes(node.key) ? list.filter(key => key !== node.key) : [...list, node.key])
    : [node.key]
  emit('update:modelValue', next)
  emit('select', node.key)
}

/* 键盘上下键按「当前可见顺序」走，这份扁平序列只服务焦点顺序，渲染仍走递归子组件 */
const order = computed<TreeKey[]>(() => {
  const out: TreeKey[] = []
  const walk = (list: TreeNode[]) => list.forEach((node) => {
    if (!visible(node)) return
    out.push(node.key)
    if (isExpanded(node)) walk(node.children ?? [])
  })
  walk(props.data)
  return out
})

const roots = computed(() => props.data.filter(visible))
const focusKey = ref<TreeKey | null>(null)
/* 行元素登记表：按 key 直接取真实 DOM 移交焦点，避免拼接属性选择器时 key 的转义问题 */
const rowEls = new Map<TreeKey, HTMLElement>()

/** [参数] key 节点标识 [参数] el 行元素或 null [返回] 无；卸载时传 null 摘除登记 */
function registerRow(key: TreeKey, el: HTMLElement | null) {
  if (el) rowEls.set(key, el)
  else rowEls.delete(key)
}

/** [参数] key 目标节点 [返回] 无；先记焦点位再移交 DOM 焦点，两者始终同步 */
function focusAt(key: TreeKey) {
  focusKey.value = key
  rowEls.get(key)?.focus()
}

/** [参数] key 当前焦点 [参数] delta 移动步长 [返回] 无；越界时保持原位 */
function step(key: TreeKey, delta: number) {
  const at = order.value.indexOf(key)
  const next = at < 0 ? undefined : order.value[at + delta]
  if (next !== undefined) focusAt(next)
}

provide('xTree', {
  checkable: computed(() => props.checkable),
  query,
  focusKey,
  firstKey: computed(() => order.value[0] ?? null),
  isExpanded,
  toggleExpand,
  isSelected: (key: TreeKey) => selectedKeys.value.has(key),
  pick,
  checkState,
  toggleCheck,
  visible,
  focusAt,
  step,
  registerRow,
})
</script>

<template>
  <div :class="['x-tree', showLine && 'is-line']">
    <p v-if="!order.length" class="x-tree-empty">暂无数据</p>
    <ul class="x-tree-list" role="tree" :aria-multiselectable="multiple || undefined">
      <TreeNodeItem v-for="node in roots" :key="node.key" :node="node" :depth="0" :parent-key="null" />
    </ul>
  </div>
</template>

<style scoped>
.x-tree { min-width: 0; font-size: 13px; }
.x-tree-list { margin: 0; padding: 0; list-style: none; }
.x-tree-empty { margin: 0; padding: 20px 10px; text-align: center; color: var(--ink-faint); }
/* 引导线画在子级容器上，横向位置由行下发的 --x-tree-guide 决定，对齐父级箭头中心 */
.x-tree.is-line .x-tree-children { position: relative; }
.x-tree.is-line .x-tree-children::before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 10px;
  left: var(--x-tree-guide, 14px);
  width: 1px;
  background: var(--line-strong);
}
</style>
