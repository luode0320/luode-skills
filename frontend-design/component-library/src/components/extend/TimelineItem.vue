<script setup lang="ts">
/* 时间轴节点：圆点 + 竖线 + 时间 / 标题 / 内容，可单独使用也可被 Timeline 批量渲染。
   dot 支持 custom 时改走 dot 插槽，color 只覆盖圆点色，不改竖线。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  label?: string
  content?: string
  time?: string
  color?: string
  dot?: string
}>(), {
  label: '',
  content: '',
  time: '',
  dot: 'default',
})

/** [参数] 无 [返回] 圆点样式；color 走内联自定义属性注入色值 */
const dotStyle = computed(() => (props.color ? { background: props.color, borderColor: props.color } : undefined))
</script>

<template>
  <li class="x-timeline-item">
    <span class="x-timeline-rail" aria-hidden="true">
      <slot name="dot">
        <span class="x-timeline-dot" :style="dotStyle" />
      </slot>
    </span>
    <div class="x-timeline-box">
      <div v-if="time" class="x-timeline-time faint">{{ time }}</div>
      <div v-if="label" class="x-timeline-label">{{ label }}</div>
      <div v-if="content || $slots.default" class="x-timeline-content">
        <slot>{{ content }}</slot>
      </div>
    </div>
  </li>
</template>

<style scoped>
.x-timeline-item { position: relative; display: flex; gap: 12px; padding: 0 0 18px; list-style: none; }
.x-timeline-item:not(:last-child) .x-timeline-rail::after {
  content: '';
  position: absolute;
  top: 16px;
  bottom: 0;
  left: 50%;
  width: 1px;
  transform: translateX(-50%);
  background: var(--line-strong);
}
.x-timeline-rail { position: relative; flex: none; width: 14px; display: flex; justify-content: center; }
.x-timeline-dot {
  position: relative;
  z-index: 1;
  width: 10px;
  height: 10px;
  margin-top: 4px;
  border: 2px solid var(--surface-solid);
  border-radius: 9999px;
  background: var(--ink-soft);
  box-shadow: 0 0 0 1px var(--line-strong);
}
.x-timeline-box { display: flex; flex-direction: column; gap: 3px; min-width: 0; flex: 1; padding-top: 1px; }
.x-timeline-time { font-size: 11px; }
.x-timeline-label { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-timeline-content { font-size: 13px; line-height: 1.6; color: var(--ink-muted); overflow-wrap: anywhere; }
</style>
