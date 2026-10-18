<script setup lang="ts">
/* 折叠子项：标题行 + 内容区，展开态、图标位置全部从父级 Collapse inject 读取。
   内容区高度用 grid-template-rows 0fr → 1fr 过渡，无需 JS 测高。
   最近修改时间：2026-10-18 17:58:00；改动原因：独立挂载（组件示例页就是这种用法）时
   inject 拿不到父级上下文，原来只做 null 兜底避免告警，结果标题行点了永远没反应、
   正文永远展不开——示例格等于不可操作。现补一份本地开合态作为非受控回退。 */
import { computed, inject, ref, type Ref } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  name: string
  title?: string
  disabled?: boolean
}>(), {
  title: '',
})

interface CollapseCtx {
  isOpen: (name: string) => boolean
  toggle: (name: string) => void
  iconPosition: Ref<'left' | 'right'>
}

/* 独立挂载（如组件核对页）时无父级提供上下文，给 null 兜底，避免 Vue 输出 injection 缺失告警 */
const ctx = inject<CollapseCtx | null>('xCollapse', null)

/* 无父级时的本地开合态：有 Collapse 包裹就完全跟随父级，不产生第二份真相 */
const selfOpen = ref(false)

/** 直接由父级展开集合派生，父级 modelValue 变化时自动跟随，无需本地镜像 */
const open = computed(() => {
  if (props.disabled) return false
  return ctx ? Boolean(ctx.isOpen(props.name)) : selfOpen.value
})

/** [参数] 无 [返回] 点击标题行时切换；disabled 直接忽略 */
function onHead() {
  if (props.disabled) return
  if (ctx) ctx.toggle(props.name)
  else selfOpen.value = !selfOpen.value
}
</script>

<template>
  <section :class="['x-collapse-item', `icon-${ctx?.iconPosition.value ?? 'left'}`, open && 'is-open', disabled && 'is-disabled']">
    <button class="x-collapse-head" type="button" :disabled="disabled" :aria-expanded="open" @click="onHead">
      <span class="x-collapse-icon"><Icon name="chevronRight" :size="14" /></span>
      <slot name="title">{{ title }}</slot>
      <span v-if="$slots.extra" class="x-collapse-extra" @click.stop><slot name="extra" /></span>
    </button>
    <div class="x-collapse-body">
      <div class="x-collapse-inner"><slot /></div>
    </div>
  </section>
</template>

<style scoped>
.x-collapse-item { background: transparent; }
.x-collapse-head {
  width: 100%;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border: 0;
  background: transparent;
  color: var(--ink);
  font: inherit;
  font-size: 13px;
  font-weight: 620;
  text-align: left;
  cursor: pointer;
  transition: background var(--ease-premium) .24s;
}
.x-collapse-head:hover { background: var(--hover-bg); }
.x-collapse-head:disabled { color: var(--ink-faint); cursor: not-allowed; }
.x-collapse-item.icon-right .x-collapse-head { flex-direction: row; }
.x-collapse-icon { display: inline-flex; color: var(--ink-soft); transition: transform var(--ease-premium) .3s; }
.x-collapse-item.is-open .x-collapse-icon { transform: rotate(90deg); }
.x-collapse-item.icon-right .x-collapse-icon { order: 2; margin-left: auto; }
.x-collapse-extra { margin-left: auto; }
.x-collapse-item.icon-right .x-collapse-extra { margin-left: 0; }
/* 0fr 收起、1fr 展开：只做过渡不做测高的关键 */
.x-collapse-body { display: grid; grid-template-rows: 0fr; transition: grid-template-rows var(--ease-premium) .34s; }
.x-collapse-item.is-open .x-collapse-body { grid-template-rows: 1fr; }
.x-collapse-inner { padding: 0 14px 20px; font-size: 13px; color: var(--ink-muted); line-height: 1.6; } /* padding-bottom 从 14px 抬到 20px，避免最后一行被裁切 */
</style>
