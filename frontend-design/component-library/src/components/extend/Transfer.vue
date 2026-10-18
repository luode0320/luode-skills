<script setup lang="ts">
/* 穿梭框：左「待选」右「已选」两栏，中间箭头把勾选项推过去。
   勾选是本地临时态，只有点箭头才动 modelValue；搜索只在各自栏内过滤，不改变选择。 */
import { computed, ref } from 'vue'
import Icon from '@/components/Icon.vue'
import Checkbox from '@/components/ui/Checkbox.vue'
import EmptyState from '@/components/ui/EmptyState.vue'

export interface TransferItem {
  key: string | number
  label: string
  disabled?: boolean
}

const props = withDefaults(defineProps<{
  modelValue?: Array<string | number>
  data: TransferItem[]
  titles?: [string, string]
  searchable?: boolean
  disabled?: boolean
}>(), {
  modelValue: () => [],
  titles: () => ['待选', '已选'],
})

const emit = defineEmits<{
  (e: 'update:modelValue', value: Array<string | number>): void
  (e: 'change', value: any[], direction: 'left' | 'right', movedKeys: any[]): void
}>()

const leftKeyword = ref('')
const rightKeyword = ref('')
/* 两侧各自的勾选集合，与 modelValue 解耦 */
const leftChecked = ref<Array<string | number>>([])
const rightChecked = ref<Array<string | number>>([])

const chosen = computed(() => new Set(props.modelValue))

/* 未选中项与已选中项按 data 原顺序拆开 */
const leftItems = computed(() => props.data.filter(d => !chosen.value.has(d.key)))
const rightItems = computed(() => props.data.filter(d => chosen.value.has(d.key)))

/**
 * [参数] list 原始列，keyword 搜索词
 * [返回] 过滤后的列表，搜索词为空时原样返回
 */
function filter(list: TransferItem[], keyword: string): TransferItem[] {
  const key = keyword.trim().toLowerCase()
  return key ? list.filter(d => d.label.toLowerCase().includes(key)) : list
}

const leftVisible = computed(() => filter(leftItems.value, leftKeyword.value))
const rightVisible = computed(() => filter(rightItems.value, rightKeyword.value))

/**
 * [参数] key 项标识 [返回] 该项是否被禁用
 */
function isDisabled(key: string | number): boolean {
  return Boolean(props.data.find(d => d.key === key)?.disabled)
}

/**
 * [参数] list 当前列可见项 [返回] 可勾选的键数组（剔除禁用项）
 */
function pickableKeys(list: TransferItem[]): Array<string | number> {
  return list.filter(d => !d.disabled).map(d => d.key)
}

/**
 * [参数] event 勾选事件，item 该项，side 'left' | 'right'
 * [返回] 无：维护该侧勾选集合
 */
function onCheck(event: boolean, item: TransferItem, side: 'left' | 'right') {
  const bag = side === 'left' ? leftChecked : rightChecked
  const set = new Set(bag.value)
  if (event) set.add(item.key)
  else set.delete(item.key)
  bag.value = [...set]
}

/**
 * [参数] side 'left' | 'right'，mode 'all' | 'invert'
 * [返回] 无：对该侧可见项全选或反选
 */
function toggleAll(side: 'left' | 'right', mode: 'all' | 'invert') {
  const list = side === 'left' ? leftVisible.value : rightVisible.value
  const bag = side === 'left' ? leftChecked : rightChecked
  const keys = pickableKeys(list)
  if (mode === 'all') {
    bag.value = keys
  } else {
    const set = new Set(bag.value)
    keys.forEach(k => (set.has(k) ? set.delete(k) : set.add(k)))
    bag.value = [...set]
  }
}

/**
 * [参数] side 勾选所在的侧
 * [返回] 该侧是否全选 / 半选，供表头勾选框用
 */
const leftState = computed(() => stateOf(leftVisible.value, leftChecked.value))
const rightState = computed(() => stateOf(rightVisible.value, rightChecked.value))

/**
 * [参数] list 可见项，bag 勾选集合
 * [返回] { all, partial } 全选与半选判定
 */
function stateOf(list: TransferItem[], bag: Array<string | number>) {
  const keys = pickableKeys(list)
  if (!keys.length) return { all: false, partial: false }
  const hit = keys.filter(k => bag.includes(k)).length
  return { all: hit === keys.length, partial: hit > 0 && hit < keys.length }
}

/**
 * [参数] direction 'right' 左到右，'left' 右到左
 * [返回] 无：把该侧勾选项迁移过去并清空勾选
 */
function move(direction: 'left' | 'right') {
  if (props.disabled) return
  const moving = direction === 'right' ? leftChecked.value : rightChecked.value
  if (!moving.length) return
  const set = new Set(props.modelValue)
  moving.forEach(k => (direction === 'right' ? set.add(k) : set.delete(k)))
  const next = props.data.filter(d => set.has(d.key)).map(d => d.key)
  emit('update:modelValue', next)
  emit('change', next, direction, [...moving])
  if (direction === 'right') leftChecked.value = []
  else rightChecked.value = []
}
</script>

<template>
  <div :class="['x-transfer', disabled && 'is-disabled']">
    <section class="x-transfer-panel m-surface">
      <header class="x-transfer-head">
        <Checkbox
          :model-value="leftState.all"
          :indeterminate="leftState.partial"
          :disabled="disabled"
          @update:model-value="toggleAll('left', 'all')"
        />
        <span class="x-transfer-title">{{ titles[0] }}</span>
        <span class="x-transfer-count tnum">{{ leftChecked.length }}/{{ leftItems.length }}</span>
      </header>
      <div v-if="searchable" class="input-shell x-transfer-search">
        <Icon name="search" :size="14" />
        <input v-model="leftKeyword" placeholder="搜索" aria-label="搜索待选" />
      </div>
      <ul class="x-transfer-list">
        <li v-for="item in leftVisible" :key="item.key" class="x-transfer-item">
          <Checkbox
            :model-value="leftChecked.includes(item.key)"
            :disabled="disabled || item.disabled"
            :label="item.label"
            @update:model-value="onCheck($event, item, 'left')"
          />
        </li>
        <li v-if="!leftVisible.length" class="x-transfer-blank">
          <EmptyState title="无匹配项" icon="search" />
        </li>
      </ul>
      <footer class="x-transfer-foot">
        <button type="button" class="x-transfer-link" :disabled="disabled" @click="toggleAll('left', 'all')">全选</button>
        <button type="button" class="x-transfer-link" :disabled="disabled" @click="toggleAll('left', 'invert')">反选</button>
      </footer>
    </section>

    <div class="x-transfer-actions">
      <button
        type="button"
        class="icon-btn is-bordered"
        aria-label="移到右侧"
        :disabled="disabled || !leftChecked.length"
        @click="move('right')"
      ><Icon name="chevronRight" :size="16" /></button>
      <button
        type="button"
        class="icon-btn is-bordered"
        aria-label="移到左侧"
        :disabled="disabled || !rightChecked.length"
        @click="move('left')"
      ><Icon name="chevronLeft" :size="16" /></button>
    </div>

    <section class="x-transfer-panel m-surface">
      <header class="x-transfer-head">
        <Checkbox
          :model-value="rightState.all"
          :indeterminate="rightState.partial"
          :disabled="disabled"
          @update:model-value="toggleAll('right', 'all')"
        />
        <span class="x-transfer-title">{{ titles[1] }}</span>
        <span class="x-transfer-count tnum">{{ rightChecked.length }}/{{ rightItems.length }}</span>
      </header>
      <div v-if="searchable" class="input-shell x-transfer-search">
        <Icon name="search" :size="14" />
        <input v-model="rightKeyword" placeholder="搜索" aria-label="搜索已选" />
      </div>
      <ul class="x-transfer-list">
        <li v-for="item in rightVisible" :key="item.key" class="x-transfer-item">
          <Checkbox
            :model-value="rightChecked.includes(item.key)"
            :disabled="disabled || item.disabled"
            :label="item.label"
            @update:model-value="onCheck($event, item, 'right')"
          />
        </li>
        <li v-if="!rightVisible.length" class="x-transfer-blank">
          <EmptyState title="暂无已选项" icon="file" />
        </li>
      </ul>
      <footer class="x-transfer-foot">
        <button type="button" class="x-transfer-link" :disabled="disabled" @click="toggleAll('right', 'all')">全选</button>
        <button type="button" class="x-transfer-link" :disabled="disabled" @click="toggleAll('right', 'invert')">反选</button>
      </footer>
    </section>
  </div>
</template>

<style scoped>
.x-transfer { display: flex; align-items: stretch; gap: 12px; }
.x-transfer.is-disabled { opacity: .6; }
.x-transfer-panel {
  display: flex;
  flex-direction: column;
  flex: 1;
  min-width: 0;
  border-radius: var(--r-md);
  overflow: hidden;
}
.x-transfer-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  border-bottom: 1px solid var(--line);
}
.x-transfer-title { flex: 1; min-width: 0; font-size: 13px; font-weight: 620; color: var(--ink); }
.x-transfer-count { font-size: 12px; color: var(--ink-faint); }
.x-transfer-search { margin: 8px 12px 0; height: var(--control-h-sm); }
.x-transfer-list {
  flex: 1;
  margin: 0;
  padding: 6px;
  list-style: none;
  overflow-y: auto;
  overscroll-behavior: contain;
  max-height: 260px;
}
.x-transfer-item {
  display: flex;
  align-items: center;
  min-height: 32px;
  padding: 0 8px;
  border-radius: var(--r-xs);
  transition: background .15s ease;
}
.x-transfer-item:hover { background: var(--hover-bg); }
.x-transfer-blank { list-style: none; }
.x-transfer-foot {
  display: flex;
  gap: 12px;
  padding: 8px 12px;
  border-top: 1px solid var(--line);
}
.x-transfer-link {
  font-size: 12px;
  color: var(--blue);
  cursor: pointer;
}
.x-transfer-link:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-transfer-link:hover:not(:disabled) { color: var(--blue-hover); }
.x-transfer-actions {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 8px;
}
</style>
