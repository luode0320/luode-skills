<script setup lang="ts">
/* 菜单：纵向或横向的导航列表，支持子菜单递归展开与折叠态。
   选中态走蓝色浅底 + 蓝色字；展开态与选中态各自独立，互不覆盖。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'
import MenuNode from '@/components/extend/MenuNode.vue'

export interface MenuItem {
  key: string
  label: string
  icon?: string
  disabled?: boolean
  children?: MenuItem[]
}

const props = withDefaults(defineProps<{
  items: MenuItem[]
  modelValue?: string
  collapsed?: boolean
  mode?: 'vertical' | 'horizontal'
}>(), {
  mode: 'vertical',
})

const emit = defineEmits<{ (e: 'update:modelValue', key: string): void }>()

/** [参数] key 被选中的菜单项 [返回] 无；选中项上抛给调用方接管 */
function select(key: string) {
  emit('update:modelValue', key)
}

/** [参数] 无 [返回] 当前菜单为纵向模式 */
const isVertical = computed(() => props.mode === 'vertical')
</script>

<template>
  <ul
    :class="['x-menu', `is-${mode}`, collapsed && 'is-collapsed']"
    role="menu"
    :aria-orientation="isVertical ? 'vertical' : 'horizontal'"
  >
    <MenuNode
      v-for="item in items"
      :key="item.key"
      :item="item"
      :depth="0"
      :vertical="isVertical"
      :collapsed="collapsed"
      :selected="modelValue"
      @select="select"
    />
  </ul>
</template>

<style scoped>
.x-menu {
  display: flex;
  gap: 2px;
  margin: 0;
  padding: 0;
  list-style: none;
}
.x-menu.is-vertical { flex-direction: column; }
.x-menu.is-horizontal { flex-direction: row; align-items: center; }
</style>
