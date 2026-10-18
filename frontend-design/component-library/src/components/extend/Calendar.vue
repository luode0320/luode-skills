<script setup lang="ts">
/* 日历：月 / 年两种粒度，月网格含上下月补白，今天与选中高亮。
   网格日期全部由原生 Date 推导，调用方通过 default 插槽按 { date } 自定义单元格内容。 */
import { computed, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'

const props = withDefaults(defineProps<{
  modelValue?: string
  mode?: 'month' | 'year'
}>(), {
  mode: 'month',
})

const emit = defineEmits<{ (e: 'update:modelValue', value: string): void }>()

const WEEK_LABELS = ['一', '二', '三', '四', '五', '六', '日']

/** 把 Date 归一成本地 yyyy-MM-dd，避免 toISOString 的时区偏移 */
function toKey(date: Date): string {
  const y = date.getFullYear()
  const m = String(date.getMonth() + 1).padStart(2, '0')
  const d = String(date.getDate()).padStart(2, '0')
  return `${y}-${m}-${d}`
}

/** 由 yyyy-MM-dd 解析出本地 Date；非法或空值回落到今天 */
function parseKey(value?: string): Date {
  if (value) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value)
    if (m) return new Date(Number(m[1]), Number(m[2]) - 1, Number(m[3]))
  }
  return new Date()
}

const todayKey = toKey(new Date())
const cursor = ref(parseKey(props.modelValue))
const activeKey = computed(() => props.modelValue ?? '')

watch(() => props.modelValue, (v) => {
  if (v) cursor.value = parseKey(v)
})

const monthLabel = computed(() => `${cursor.value.getFullYear()} 年 ${cursor.value.getMonth() + 1} 月`)

/** 当月 6×7 网格：从该周周一起算，前补上月、后补下月 */
const days = computed(() => {
  const year = cursor.value.getFullYear()
  const month = cursor.value.getMonth()
  const first = new Date(year, month, 1)
  // getDay 周日为 0，转成周一为 0 的偏移
  const lead = (first.getDay() + 6) % 7
  const start = new Date(year, month, 1 - lead)
  const list: { date: Date; key: string; inMonth: boolean }[] = []
  for (let i = 0; i < 42; i += 1) {
    const date = new Date(start.getFullYear(), start.getMonth(), start.getDate() + i)
    list.push({ date, key: toKey(date), inMonth: date.getMonth() === month })
  }
  return list
})

/** 月视图顶栏的年份列表，供快速跳年 */
const years = computed(() => {
  const base = cursor.value.getFullYear()
  return Array.from({ length: 12 }, (_, i) => base - 5 + i)
})

/** 上 / 下月（或上 / 下年）切换 */
function step(delta: number) {
  const d = cursor.value
  cursor.value = props.mode === 'year'
    ? new Date(d.getFullYear() + delta, d.getMonth(), 1)
    : new Date(d.getFullYear(), d.getMonth() + delta, 1)
}

/** [参数] date 目标日期 [返回] 选中该日期并派发 update:modelValue */
function pick(date: Date) {
  cursor.value = date
  emit('update:modelValue', toKey(date))
}

/** [参数] year 目标年份 [返回] 切到该年 */
function pickYear(year: number) {
  cursor.value = new Date(year, cursor.value.getMonth(), 1)
}
</script>

<template>
  <div class="x-calendar m-surface">
    <header class="x-cal-head">
      <button class="icon-btn" type="button" aria-label="上一页" @click="step(-1)">
        <Icon name="chevronLeft" :size="15" />
      </button>
      <span class="x-cal-title">{{ monthLabel }}</span>
      <button class="icon-btn" type="button" aria-label="下一页" @click="step(1)">
        <Icon name="chevronRight" :size="15" />
      </button>
    </header>

    <div v-if="mode === 'month'" class="x-cal-week">
      <span v-for="w in WEEK_LABELS" :key="w" class="x-cal-weekday">{{ w }}</span>
    </div>

    <div :class="['x-cal-grid', `is-${mode}`]">
      <template v-if="mode === 'month'">
        <button
          v-for="cell in days"
          :key="cell.key"
          type="button"
          :class="['x-cal-cell', !cell.inMonth && 'is-out', cell.key === activeKey && 'is-active', cell.key === todayKey && 'is-today']"
          @click="pick(cell.date)"
        >
          <slot :date="cell.date">
            <span class="x-cal-day tnum">{{ cell.date.getDate() }}</span>
          </slot>
        </button>
      </template>

      <template v-else>
        <button
          v-for="y in years"
          :key="y"
          type="button"
          :class="['x-cal-cell', 'is-year', y === cursor.getFullYear() && 'is-active']"
          @click="pickYear(y)"
        >
          <span class="tnum">{{ y }}</span>
        </button>
      </template>
    </div>
  </div>
</template>

<style scoped>
.x-calendar { display: flex; flex-direction: column; gap: 8px; padding: 12px; border-radius: var(--r-md); }
.x-cal-head { display: flex; align-items: center; justify-content: space-between; gap: 8px; }
.x-cal-title { font-size: 13px; font-weight: 640; color: var(--ink); }
.x-cal-week { display: grid; grid-template-columns: repeat(7, 1fr); }
.x-cal-weekday { text-align: center; font-size: 11px; color: var(--ink-faint); }
.x-cal-grid { display: grid; gap: 2px; }
.x-cal-grid.is-month { grid-template-columns: repeat(7, 1fr); grid-template-rows: repeat(6, 1fr); }
.x-cal-grid.is-year { grid-template-columns: repeat(3, 1fr); gap: 6px; }
.x-cal-cell {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 34px;
  padding: 4px;
  border: 0;
  border-radius: var(--r-xs);
  background: transparent;
  color: var(--ink);
  font: inherit;
  font-size: 12px;
  cursor: pointer;
  transition: background var(--ease-premium) .24s, color var(--ease-premium) .24s;
}
.x-cal-cell:hover { background: var(--hover-bg); }
.x-cal-cell.is-out { color: var(--ink-faint); }
.x-cal-cell.is-today { box-shadow: inset 0 0 0 1px var(--glass-line); color: var(--blue); font-weight: 660; }
.x-cal-cell.is-active { background: var(--blue); color: var(--plate-ink); box-shadow: var(--e-accent); font-weight: 660; }
.x-cal-cell.is-year { min-height: 40px; }
.x-cal-day { pointer-events: none; }
</style>
