/**
 * 本地扩展视图注册表：`sys_menu.component` 取值 → 后台页面组件。
 *
 * [用途] 上游 `composables/auth.ts` 的页面登记表属字节冻结基线，本地新增的后台页面
 *   统一在此登记；上游只保留一行展开动作，后续加页面不再触碰冻结文件。
 * [约束] 键必须与菜单数据里的 `component` 字段逐字一致，否则该菜单项会被判定为不可达页面。
 * 最近修改时间：2026-10-16 18:05:00；改动原因：组件库示例页要迁入后台真实路由，
 *   需要一条不破坏上游还原度基线的本地页面注册通道。
 */
import type { Component } from 'vue'

/** 菜单 `component` 字段到懒加载页面组件的映射 */
export const LOCAL_VIEWS: Record<string, () => Promise<{ default: Component }>> = {
  'gallery/index': () => import('@/views/gallery/Gallery.vue'),
}
