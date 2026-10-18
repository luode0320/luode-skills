<script setup lang="ts">
/* 徽标：挂在任意元素右上角的数字 / 圆点角标，数字超过 max 显示为 max+。
   颜色只走四种语义色，与 Tag 同一口径；角标压在实色底上，所以文字固定用铭牌亮色。 */
import { computed } from 'vue'

const props = withDefaults(defineProps<{
  value?: string | number
  dot?: boolean
  max?: number
  tone?: 'danger' | 'info' | 'ok' | 'neutral'
  showZero?: boolean
  /** 相对右上角的微调偏移，单位百分比，用于避开圆形头像等异形宿主 */
  offset?: [number, number]
}>(), {
  max: 99,
  tone: 'danger',
})

const text = computed(() => {
  const v = props.value
  if (v === undefined || v === null || v === '') return ''
  return typeof v === 'number' && v > props.max ? `${props.max}+` : String(v)
})

const visible = computed(() => Boolean(props.dot) || Boolean(text.value) || (props.showZero && props.value === 0))

const style = computed(() => (props.offset
  ? { transform: `translate(${50 + props.offset[0]}%, ${-50 + props.offset[1]}%)` }
  : undefined))
</script>

<template>
  <span class="x-badge-wrap">
    <slot />
    <span
      v-if="visible"
      :class="['x-badge', `tone-${tone}`, dot && 'is-dot']"
      :style="style"
      role="status"
      :aria-label="dot ? '有新内容' : undefined"
    >{{ dot ? '' : text }}</span>
  </span>
</template>

<style scoped>
.x-badge-wrap { position: relative; display: inline-flex; }
.x-badge {
  position: absolute;
  top: 0;
  right: 0;
  transform: translate(50%, -50%);
  box-sizing: border-box;
  min-width: 18px;
  height: 18px;
  padding: 0 5px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 9999px;
  font-size: 11px;
  font-weight: 640;
  line-height: 1;
  font-variant-numeric: tabular-nums;
  color: var(--plate-ink);
  box-shadow: 0 0 0 2px var(--surface-solid);
}
.x-badge.is-dot { min-width: 8px; width: 8px; height: 8px; padding: 0; }
.x-badge.tone-danger { background: var(--red); }
.x-badge.tone-info { background: var(--blue); }
/* 青柠是亮底，必须配深字，用铭牌底色而非会随主题翻转的 --ink */
.x-badge.tone-ok { background: var(--lime); color: var(--plate-bg); }
.x-badge.tone-neutral { background: var(--ink-soft); }
</style>
