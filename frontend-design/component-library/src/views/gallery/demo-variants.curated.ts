/* 策展变体索引：把五类 diamond 文件合并成「组件名 → 变体清单」的唯一入口。
   entries.ts 只消费本文件，不逐类 import，新增分类文件只在此追加一行。
   同一组件可能同时出现在展示类与外壳类，因此按 label 去重后拼接而不是覆盖，
   否则后合并者会清掉前者，使该组件凑不满 ≥3 组示例。
   最近修改时间：2026-10-17 11:07:00；改动原因：日期时间族拆出独立策展文件，索引追加来源。 */
import type { VariantShape } from './demo-variants.types'
import { CURATED_BUSINESS } from './demo-variants.curated-business'
import { CURATED_DATETIME } from './demo-variants.curated-datetime'
import { CURATED_DISPLAY } from './demo-variants.curated-display'
import { CURATED_GENERAL } from './demo-variants.curated-general'
import { CURATED_INPUTS } from './demo-variants.curated-inputs'
import { CURATED_SHELL } from './demo-variants.curated-shell'

const SOURCES = [CURATED_GENERAL, CURATED_INPUTS, CURATED_DATETIME, CURATED_DISPLAY, CURATED_BUSINESS, CURATED_SHELL]

/** 组件名 → 策展变体清单（跨文件同名按 label 去重拼接） */
export const CURATED_VARIANTS: Record<string, VariantShape[]> = (() => {
  const map: Record<string, VariantShape[]> = {}
  for (const source of SOURCES) {
    for (const [name, list] of Object.entries(source)) {
      const merged = map[name] ?? (map[name] = [])
      for (const variant of list) {
        if (!merged.some((v) => v.label === variant.label)) merged.push(variant)
      }
    }
  }
  return map
})()
