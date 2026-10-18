/* ============================================================
   组件语义分类：示例页导航、菜单与目录索引的唯一分类真相源。
   结构为两级：父分类（侧栏分组标题）→ 子分组（一个可点示例页）。
   参照 Arco Design Vue 官网组件菜单作主干，并保留珍珠玻璃自有扩展类。
   约束：每个组件恰好归入一个子分组，子分组键全局唯一；数据按基础/数据/扩展
   三个文件分放，本文件只做组装与派生索引，新增组件必须同步对应数据文件，
   由 scripts/check_component_categories.mjs 与磁盘全集双向对账，漂移即 FAIL。
   最近修改时间：2026-10-17 04:25:00；改动原因：删除全仓无消费的 COMPONENT_SUB_GROUP_OF，
   页面归属由 Gallery 直接按路由两段查子分组，不需要第二张反查表。
   ============================================================ */
import { BASIC_CATEGORIES } from './component-categories.basic.ts'
import { DATA_CATEGORIES } from './component-categories.data.ts'
import { EXTENDED_CATEGORIES } from './component-categories.extended.ts'
import type { ComponentCategory, ComponentSubGroup } from './component-categories.types.ts'

export type { ComponentCategory, ComponentSubGroup } from './component-categories.types.ts'

/** 父分类全集：按侧栏自上而下的展示顺序排列。 */
export const COMPONENT_CATEGORY_ORDER: ComponentCategory[] = [
  ...BASIC_CATEGORIES,
  ...DATA_CATEGORIES,
  ...EXTENDED_CATEGORIES,
]

/** 子分组全集（带所属父分类键）：菜单与路由的唯一生成来源。 */
export const COMPONENT_SUB_GROUPS: (ComponentSubGroup & { categoryKey: string; categoryLabel: string })[] =
  COMPONENT_CATEGORY_ORDER.flatMap((cat) =>
    cat.subGroups.map((sub) => ({ ...sub, categoryKey: cat.key, categoryLabel: cat.label }))
  )

/** 组件名 → 父分类键：由子分组归属派生，不手抄。 */
export const COMPONENT_CATEGORY_OF: Record<string, string> = (() => {
  const map: Record<string, string> = {}
  for (const cat of COMPONENT_CATEGORY_ORDER) for (const sub of cat.subGroups) for (const name of sub.components) map[name] = cat.key
  return map
})()
