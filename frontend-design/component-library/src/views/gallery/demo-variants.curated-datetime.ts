/* 日期与时间类策展变体：这一族组件的公开契约高度同形（modelValue / placeholder /
   disabled / clearable / format），机械派生只能覆盖 disabled 与 clearable，
   空值占位与格式差异必须策展补齐，故单独成文件，避免与其余输入控件混在一处。
   最近修改时间：2026-10-17 11:07:00；改动原因：原 curated-inputs 超过 200 行基线，
   按业务语义把日期时间族拆为同级 diamond 文件。 */
import type { VariantShape } from './demo-variants.types'

/** 日期与时间族组件的策展变体 */
export const CURATED_DATETIME: Record<string, VariantShape[]> = {
  /* 基础示例取 clearable: true，这里给不可清除、禁用与空值占位三态 */
  MonthPicker: [
    { label: '不可清除', props: { clearable: false } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: '', placeholder: '选择统计月份' } },
  ],
  QuarterPicker: [
    { label: '不可清除', props: { clearable: false } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: '', placeholder: '选择统计季度' } },
  ],
  WeekPicker: [
    { label: '不可清除', props: { clearable: false } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: '', placeholder: '选择统计周' } },
  ],
  YearPicker: [
    { label: '不可清除', props: { clearable: false } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: '', placeholder: '选择统计年份' } },
  ],
  RangePicker: [
    { label: '不可清除', props: { clearable: false } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: ['', ''], placeholder: '选择统计区间' } },
  ],
  DatePicker: [
    { label: '空值占位', props: { modelValue: '', placeholder: '选择生效日期' } },
    { label: '另一位日期', props: { modelValue: '2026-01-01' } },
  ],
  TimePicker: [
    { label: '空值占位', props: { modelValue: '', placeholder: '选择执行时刻' } },
    { label: '仅时分', props: { format: 'HH:mm', modelValue: '08:30:00' } },
  ],
}
