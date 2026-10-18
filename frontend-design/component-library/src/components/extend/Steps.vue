<script setup lang="ts">
/* 步骤条：横向或纵向的工序进度，已完成打勾、当前高亮、未开始置灰。
   状态由 current 单一驱动，调用方不必自己算 done/active 两套标记。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'

export interface StepItem {
  title: string
  desc?: string
}

const props = withDefaults(defineProps<{
  current: number
  items: StepItem[]
  direction?: 'horizontal' | 'vertical'
  clickable?: boolean
}>(), {
  direction: 'horizontal',
})

const emit = defineEmits<{ (e: 'change', index: number): void }>()

const stateOf = computed(() => props.items.map((_, i) => (
  i < props.current ? 'done' : i === props.current ? 'active' : 'wait'
)))

function pick(index: number) {
  if (props.clickable && index <= props.current) emit('change', index)
}
</script>

<template>
  <ol :class="['x-steps', `is-${direction}`]">
    <li
      v-for="(item, i) in items"
      :key="item.title"
      :class="['x-step', `is-${stateOf[i]}`, clickable && i <= current && 'is-clickable']"
      :aria-current="stateOf[i] === 'active' ? 'step' : undefined"
      @click="pick(i)"
    >
      <span class="x-step-mark">
        <Icon v-if="stateOf[i] === 'done'" name="check" :size="13" :stroke="2.6" />
        <span v-else>{{ i + 1 }}</span>
      </span>
      <span class="x-step-text">
        <span class="x-step-title">{{ item.title }}</span>
        <span v-if="item.desc" class="x-step-desc">{{ item.desc }}</span>
      </span>
    </li>
  </ol>
</template>

<style scoped>
.x-steps { display: flex; gap: 0; margin: 0; padding: 0; list-style: none; }
.x-steps.is-vertical { flex-direction: column; }
.x-step {
  position: relative;
  flex: 1;
  display: flex;
  align-items: flex-start;
  gap: 10px;
  min-width: 0;
  padding-right: 16px;
}
.x-steps.is-vertical .x-step { flex: none; padding: 0 0 22px; }
/* 连接线：横排在标记右侧，纵排在标记下方 */
.x-step:not(:last-child)::after {
  content: '';
  position: absolute;
  background: var(--line-strong);
}
.x-steps.is-horizontal .x-step:not(:last-child)::after {
  top: 13px;
  left: 30px;
  right: 6px;
  height: 1px;
}
.x-steps.is-vertical .x-step:not(:last-child)::after {
  top: 30px;
  bottom: 4px;
  left: 13px;
  width: 1px;
}
.x-step-mark {
  position: relative;
  z-index: 1;
  flex: none;
  width: 26px;
  height: 26px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  border: 1px solid var(--line-strong);
  background: var(--surface-solid);
  color: var(--ink-soft);
  font-size: 12px;
  font-weight: 640;
  font-variant-numeric: tabular-nums;
  transition: background var(--ease-premium) .28s, color var(--ease-premium) .28s, border-color var(--ease-premium) .28s;
}
.x-step.is-done .x-step-mark { background: var(--lime-soft); border-color: transparent; color: var(--leaf-text); }
.x-step.is-active .x-step-mark {
  background: var(--blue);
  border-color: transparent;
  color: var(--plate-ink);
  box-shadow: var(--e-accent);
}
.x-step-text { display: flex; flex-direction: column; gap: 2px; min-width: 0; padding-top: 3px; }
.x-step-title { font-size: 13px; font-weight: 620; color: var(--ink-muted); }
.x-step.is-active .x-step-title { color: var(--ink); }
.x-step.is-done .x-step-title { color: var(--ink-muted); }
.x-step-desc { font-size: 11px; color: var(--ink-faint); }
.x-step.is-clickable { cursor: pointer; }
.x-step.is-clickable:hover .x-step-title { color: var(--blue); }
</style>
