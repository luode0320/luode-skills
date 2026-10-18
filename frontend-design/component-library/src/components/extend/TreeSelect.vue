<script setup lang="ts">
/* 树选择：触发区点开一个下拉树面板，支持层级缩进、展开折叠、单选与多选。
   面板定位 / 关外 / 键盘导航沿用 Select.vue 的写法，只把扁平选项换成递归树行。
   最近修改时间：2026-10-18 17:30:00；改动原因：modelValue 的声明窄于实现——多选分支
   一直按数组读写并用 as any 绕过校验，调用方传数组会触发 Vue 的 prop 类型告警，
   现把数组形态写进公开契约，去掉两处 as any。 */
import { computed, nextTick, onBeforeUnmount, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

export interface TreeNode {
  key: string | number
  title: string
  disabled?: boolean
  children?: TreeNode[]
}

/** 选中值：单选是单个 key，多选是 key 数组，未选是 null */
export type TreeSelectValue = string | number | Array<string | number> | null

const props = withDefaults(defineProps<{
  modelValue?: TreeSelectValue
  data: TreeNode[]
  placeholder?: string
  disabled?: boolean
  clearable?: boolean
  multiple?: boolean
}>(), {
  modelValue: null,
  placeholder: '请选择',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: TreeSelectValue): void }>()

const trigger = ref<HTMLElement | null>(null)
const panel = ref<HTMLElement | null>(null)
const open = ref(false)
const pos = ref({ top: 0, left: 0, width: 0 })
/* 已展开节点的 key 集合 */
const expanded = ref<Set<string | number>>(new Set())

/* 多选值按数组理解 / 非多选按单值理解，两种契约都收在 selectedKeys 里 */
const selectedKeys = computed<Array<string | number>>(() => {
  const v = props.modelValue
  if (v === null || v === undefined || v === '') return []
  return Array.isArray(v) ? v : [v]
})

/**
 * [参数] 无
 * [返回] 展平后的可见行（含 depth 与 parentKey），折叠节点的子行被剔除
 *        摊平是为了键盘上下键与高亮索引能顺序走一遍
 */
const rows = computed(() => {
  const out: Array<{ node: TreeNode; depth: number; parentKey: string | number | null }> = []
  const walk = (list: TreeNode[], depth: number, parentKey: string | number | null) => {
    list.forEach(node => {
      out.push({ node, depth, parentKey })
      if (node.children?.length && expanded.value.has(node.key)) walk(node.children, depth + 1, node.key)
    })
  }
  walk(props.data, 0, null)
  return out
})

/**
 * [参数] key 节点标识
 * [返回] 该节点对象，找不到返回 undefined
 * 最近修改时间：2026-10-17 04:25:00；改动原因：修收起态选中值不显示。
 * 必须在完整树里找而不是在可见行里找：rows 会剔除折叠节点的子行，
 * 收起状态下选中的二级节点用 rows 查不到，触发区会退化成占位符、看不出已选中。
 */
function nodeOf(key: string | number) {
  const find = (list: TreeNode[]): TreeNode | undefined => {
    for (const node of list) {
      if (node.key === key) return node
      const hit = node.children?.length ? find(node.children) : undefined
      if (hit) return hit
    }
    return undefined
  }
  return find(props.data)
}

/**
 * [参数] 无
 * [返回] 无：面板贴触发区下方，空间不足翻上方，宽度对齐触发区
 */
function place() {
  const rect = trigger.value?.getBoundingClientRect()
  if (!rect) return
  const panelHeight = panel.value?.offsetHeight ?? 260
  const below = window.innerHeight - rect.bottom
  const top = below < panelHeight + 12 && rect.top > panelHeight + 12 ? rect.top - panelHeight - 6 : rect.bottom + 6
  const width = Math.max(rect.width, 200)
  const left = Math.min(rect.left, window.innerWidth - width - 8)
  pos.value = { top, left, width }
}

/** [参数] 无 [返回] 无：开面板、默认展开顶层，并绑定关外监听 */
async function show() {
  if (props.disabled || open.value) return
  if (!expanded.value.size) props.data.slice(0, 4).forEach(n => expanded.value.add(n.key))
  open.value = true
  place()
  await nextTick()
  place()
  document.addEventListener('pointerdown', onOutside, true)
  window.addEventListener('scroll', place, true)
  window.addEventListener('resize', place)
}

/** [参数] refocus 关闭后是否把焦点还给触发区 [返回] 无：收面板并摘监听 */
function hide(refocus = false) {
  if (!open.value) return
  open.value = false
  document.removeEventListener('pointerdown', onOutside, true)
  window.removeEventListener('scroll', place, true)
  window.removeEventListener('resize', place)
  if (refocus) trigger.value?.focus()
}

/** [参数] event 指针事件 [返回] 无：点在触发区与面板外才收 */
function onOutside(event: PointerEvent) {
  const target = event.target as Node
  if (trigger.value?.contains(target) || panel.value?.contains(target)) return
  hide()
}

/** [参数] node 目标节点 [返回] 无：就地切换展开态，不冒泡到选中逻辑 */
function toggleExpand(node: TreeNode) {
  const set = new Set(expanded.value)
  if (set.has(node.key)) set.delete(node.key)
  else set.add(node.key)
  expanded.value = set
}

/** [参数] node 被点节点 [返回] 无：按单选 / 多选写值，单选选完即收 */
function select(node: TreeNode) {
  if (node.disabled) return
  if (props.multiple) {
    const list = selectedKeys.value
    const next = list.includes(node.key) ? list.filter(k => k !== node.key) : [...list, node.key]
    emit('update:modelValue', next)
  } else {
    emit('update:modelValue', node.key)
    hide(true)
  }
}

/** [参数] 无 [返回] 无：清空当前选择 */
function clear() {
  emit('update:modelValue', props.multiple ? [] : null)
  hide()
}

/** [参数] 无 [返回] 无：选中标题串太长时截断到前两个 */
const summary = computed(() => {
  const keys = selectedKeys.value
  if (!keys.length) return ''
  const labels = keys.map(k => nodeOf(k)?.title).filter(Boolean) as string[]
  return labels.length > 2 ? `${labels.slice(0, 2).join('、')} 等 ${labels.length} 项` : labels.join('、')
})

/** [参数] event 键盘事件 [返回] 无：下拉打开 / 关闭与上下移动焦点 */
function onKey(event: KeyboardEvent) {
  if (!open.value) {
    if (['ArrowDown', 'Enter', ' '].includes(event.key)) {
      event.preventDefault()
      show()
    }
    return
  }
  if (event.key === 'Escape') {
    event.preventDefault()
    hide(true)
  } else if (event.key === 'Tab') {
    hide(true)
  }
}

onBeforeUnmount(() => hide())
</script>

<template>
  <div class="x-treeselect">
    <button
      ref="trigger"
      type="button"
      :class="['input-shell', 'x-tree-trigger', disabled && 'is-disabled']"
      :disabled="disabled"
      aria-haspopup="tree"
      :aria-expanded="open"
      @click="open ? hide() : show()"
      @keydown="onKey"
    >
      <Icon name="layers" :size="15" />
      <span :class="['x-tree-value', !selectedKeys.length && 'is-placeholder']">{{ summary || placeholder }}</span>
      <span
        v-if="clearable && selectedKeys.length && !disabled"
        class="input-clear"
        role="button"
        aria-label="清空"
        @click.stop="clear"
      ><Icon name="x" :size="14" /></span>
      <Icon v-else name="chevronDown" :size="15" class="x-tree-caret" />
    </button>
    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          ref="panel"
          class="x-tree-panel m-float"
          role="tree"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, width: `${pos.width}px`, zIndex: floatingLayerFor(trigger) }"
        >
          <p v-if="!rows.length" class="x-tree-empty">暂无数据</p>
          <div
            v-for="row in rows"
            :key="row.node.key"
            role="treeitem"
            :aria-level="row.depth + 1"
            :aria-selected="selectedKeys.includes(row.node.key)"
            :aria-expanded="row.node.children?.length ? expanded.has(row.node.key) : undefined"
            :aria-disabled="row.node.disabled || undefined"
            :class="['x-tree-row', selectedKeys.includes(row.node.key) && 'is-selected', row.node.disabled && 'is-disabled']"
            :style="{ paddingLeft: `${10 + row.depth * 18}px` }"
            @click="select(row.node)"
          >
            <span
              v-if="row.node.children?.length"
              class="x-tree-arrow"
              role="button"
              :aria-label="expanded.has(row.node.key) ? '折叠' : '展开'"
              @click.stop="toggleExpand(row.node)"
            ><Icon :name="expanded.has(row.node.key) ? 'chevronDown' : 'chevronRight'" :size="13" /></span>
            <span v-else class="x-tree-arrow is-blank" aria-hidden="true" />
            <span class="x-tree-title ellipsis">{{ row.node.title }}</span>
            <Icon v-if="selectedKeys.includes(row.node.key)" name="check" :size="14" />
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<style scoped>
.x-treeselect { display: inline-flex; width: 100%; }
.x-tree-trigger { width: 100%; cursor: pointer; justify-content: space-between; text-align: left; color: var(--ink); }
.x-tree-value { flex: 1; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-size: 13px; }
.x-tree-value.is-placeholder { color: var(--ink-faint); }
.x-tree-caret { color: var(--ink-soft); flex: none; }
.x-tree-panel {
  max-height: 280px;
  padding: 6px;
  border-radius: var(--r-md);
  overflow-y: auto;
  overscroll-behavior: contain;
}
.x-tree-row {
  display: flex;
  align-items: center;
  gap: 6px;
  min-height: 32px;
  padding-right: 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  color: var(--ink);
  cursor: pointer;
  transition: background .15s ease, color .15s ease;
}
.x-tree-row:hover { background: var(--hover-bg); }
.x-tree-row.is-selected { background: var(--blue-soft); color: var(--blue); font-weight: 620; }
.x-tree-row.is-disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-tree-arrow { display: inline-flex; color: var(--ink-soft); flex: none; }
.x-tree-arrow.is-blank { width: 13px; }
.x-tree-title { flex: 1; min-width: 0; }
.x-tree-empty { margin: 0; padding: 20px 10px; text-align: center; font-size: 13px; color: var(--ink-faint); }
</style>
