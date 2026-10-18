<script setup lang="ts">
/* 结果页：一次操作或一个错误码的终态陈述。
   图标、语义色与缺省标题由 status 单点派生，调用方只关心业务文案。 */
import { computed } from 'vue'
import Icon from '@/components/Icon.vue'

type Status = 'success' | 'error' | 'warning' | 'info' | '404' | '403' | '500'

const props = withDefaults(defineProps<{
  status?: Status
  title?: string
  subTitle?: string
}>(), {
  status: 'info',
})

/* 每个状态对应：图标名、语义色调后缀、缺省标题 */
const PRESET: Record<Status, { icon: string; tone: string; title: string }> = {
  success: { icon: 'check', tone: 'ok', title: '操作成功' },
  error: { icon: 'x', tone: 'danger', title: '操作失败' },
  warning: { icon: 'alert', tone: 'warn', title: '请注意' },
  info: { icon: 'info', tone: 'info', title: '提示' },
  404: { icon: 'search', tone: 'neutral', title: '页面不存在' },
  403: { icon: 'lock', tone: 'info', title: '无权访问' },
  500: { icon: 'alert', tone: 'danger', title: '服务异常' },
}

/** [参数] 无 [返回] 当前状态对应的预设项 */
const preset = computed(() => PRESET[props.status])

/** [参数] 无 [返回] 实际标题，未传 title 时回落状态缺省文案 */
const heading = computed(() => props.title ?? preset.value.title)
</script>

<template>
  <div :class="['x-result', `is-${preset.tone}`]" role="status">
    <span class="x-result-ico"><Icon :name="preset.icon" :size="28" :stroke="2" /></span>
    <h3 class="x-result-title">{{ heading }}</h3>
    <p v-if="subTitle" class="x-result-sub">{{ subTitle }}</p>
    <div v-if="$slots.default" class="x-result-body"><slot /></div>
    <div v-if="$slots.extra" class="x-result-extra"><slot name="extra" /></div>
  </div>
</template>

<style scoped>
.x-result {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 40px 24px;
}
/* 大号圆形语义底：图标是唯一焦点，颜色只表达状态 */
.x-result-ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 64px;
  height: 64px;
  border-radius: 999px;
  color: var(--blue);
  background: var(--blue-soft);
  box-shadow: var(--edge);
}
.x-result.is-ok .x-result-ico { color: var(--leaf-text); background: var(--lime-soft); }
.x-result.is-danger .x-result-ico { color: var(--red-text); background: var(--red-soft); }
.x-result.is-warn .x-result-ico { color: var(--cat-1-ink); background: var(--cat-1-bg); }
.x-result.is-neutral .x-result-ico { color: var(--ink-soft); background: var(--groove-bg); }
.x-result-title { margin-top: 16px; font-size: 18px; font-weight: 680; letter-spacing: -.015em; color: var(--ink); }
.x-result-sub { margin-top: 6px; max-width: 420px; font-size: 13px; line-height: 1.6; color: var(--ink-muted); }
.x-result-body { margin-top: 16px; width: 100%; }
.x-result-extra { margin-top: 22px; display: flex; align-items: center; justify-content: center; gap: 10px; }
</style>
