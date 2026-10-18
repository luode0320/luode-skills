/* 组件分类的树形契约：父分类（导航分组标题）→ 子分组（一个可点页面）。
   侧栏与路由由冻结的上游 buildNav 只支持「分组 → 组内项」两级，
   因此父分类必须作为顶层节点、子分组作为带 component 的叶子，不能三层嵌套。
   最近修改时间：2026-10-17 02:35:00；改动原因：目标要求组件菜单做细，
   把单级 10 类升级为父分类 + 子组件分类两级。 */

export interface ComponentSubGroup {
  /** 子分组键：全局唯一，直接作为示例页路由的最后一段 */
  key: string
  /** 中文子分组名：同时作为侧栏组内项文案 */
  label: string
  /** 导航图标，取自 src/data/icons.ts 已注册图标名 */
  icon: string
  /** 一句话说明：本子分组覆盖的能力范围 */
  desc: string
  /** 归入本子分组的组件文件名（不含 .vue），全局唯一、恰好一次 */
  components: string[]
}

export interface ComponentCategory {
  /** 父分类键，用于路由第一段与统计 */
  key: string
  /** 中文父分类名：作为侧栏分组标题 */
  label: string
  /** 导航图标，取自 src/data/icons.ts 已注册图标名 */
  icon: string
  /** 一句话说明：本类覆盖的能力范围 */
  desc: string
  /** 本父分类下的子分组，至少一个 */
  subGroups: ComponentSubGroup[]
}
