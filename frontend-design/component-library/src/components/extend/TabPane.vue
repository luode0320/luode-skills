<script setup lang="ts">
/* 标签面板：Tabs 内容区的单页容器，active 为真才显示，切换只切可见性不销毁内容。
   保留 DOM 是为了让面板内的滚动位置、输入态在来回切换时不丢失。
   注：面板标识走 name 而非 key —— key 是 Vue 保留属性名，声明为 prop 会触发
   Invalid prop name 警告且取值恒为空，无法承载标识语义。 */
import { computed } from 'vue'

const props = defineProps<{
  /** 与 Tabs 的 item.key 对应，用于生成面板标识 */
  name?: string
  label?: string
  active?: boolean
}>()

/** [参数] 无 [返回] 面板的 DOM id，未给 name 时不生成 */
const panelId = computed(() => (props.name ? `x-tabpanel-${props.name}` : undefined))
</script>

<template>
  <section
    v-show="active"
    :id="panelId"
    class="x-tabpane"
    role="tabpanel"
    :aria-label="label"
    :aria-hidden="active ? undefined : true"
  >
    <slot />
  </section>
</template>

<style scoped>
.x-tabpane { min-width: 0; }
</style>
