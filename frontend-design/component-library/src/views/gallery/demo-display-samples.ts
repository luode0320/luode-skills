/* 展示类样本：列表、树、菜单、时间线与内联图片等 demo 数据。
   属于组件库示例页（后台路由 /gallery）的展示样本，不参与组件库生产运行；
   数据形状严格对齐组件真实类型定义。
   最近修改时间：2026-10-16 18:58:00；改动原因：示例页迁入后台真实路由后本批样本进入 src，
   原单文件 666 行突破仓库单文件行数基线，按业务语义拆成同级文件。
*/
import type { ShareItem } from '../../components/workspace/ShareList.vue'
import type { ActivityItem } from '../../components/workspace/ActivityList.vue'
import type { ShortcutItem } from '../../components/workspace/ShortcutGrid.vue'
import type { ReadoutItem } from '../../components/workspace/ReadoutStrip.vue'
import type { ReadoutRow } from '../../components/workspace/KeyValueReadout.vue'

export const SHARE_ITEMS: ShareItem[] = [
  { label: '全部数据', value: 18 },
  { label: '本部门及以下', value: 12 },
  { label: '本部门', value: 7 },
  { label: '仅本人', value: 3 },
]

/** 动态列表。 */
export const ACTIVITY_ITEMS: ActivityItem[] = [
  { who: '罗德', target: '登录系统', time: '10:24:31', ok: true },
  { who: '林可', target: '修改角色权限', time: '09:58:02', ok: true },
  { who: '陈舟', target: '登录系统', time: '09:12:47', ok: false },
]

/** 快捷入口。 */
export const SHORTCUT_ITEMS: ShortcutItem[] = [
  { key: 'users', label: '用户管理', group: '系统管理', icon: 'user', path: '/system/users' },
  { key: 'roles', label: '角色管理', group: '系统管理', icon: 'role', path: '/system/roles' },
  { key: 'operlog', label: '操作日志', group: '监控中心', icon: 'log', path: '/monitor/operlog' },
]

/** 读数条与键值读数。 */
export const READOUT_ITEMS: ReadoutItem[] = [
  { label: '操作次数', value: 1284, unit: '次' },
  { label: '成功率', value: 98.6, decimals: 1, unit: '%' },
  { label: '失败', value: 18, unit: '次', alert: true },
]
export const READOUT_ROWS: ReadoutRow[] = [
  { label: '峰值', value: 31 },
  { label: '均值', value: 20.4 },
  { label: '范围', value: '近 7 天' },
]

/** Arco 品类对齐层（extend）的样本数据。 */
export const STEP_ITEMS = [
  { title: '提交申请', desc: '填写变更单' },
  { title: '部门审批', desc: '直属主管' },
  { title: '发布上线', desc: '运维执行' },
]
export const ANCHOR_ITEMS = [
  { id: 'sec-1', title: '基本信息' },
  { id: 'sec-2', title: '权限配置', depth: 1 },
  { id: 'sec-3', title: '操作日志' },
]
export const BREADCRUMB_ITEMS = [
  { label: '首页', to: '/' },
  { label: '系统管理', to: '/system' },
  { label: '用户管理' },
]
export const DROPDOWN_ITEMS = [
  { key: 'edit', label: '编辑', icon: 'edit' },
  { key: 'copy', label: '复制', icon: 'copy' },
  { key: 'del', label: '删除', icon: 'trash', disabled: true },
]
export const MENU_ITEMS = [
  { key: 'users', label: '用户管理', icon: 'user' },
  { key: 'roles', label: '角色管理', icon: 'role' },
  {
    key: 'monitor',
    label: '监控中心',
    icon: 'monitor',
    children: [
      { key: 'operlog', label: '操作日志', icon: 'log' },
      { key: 'loginlog', label: '登录日志', icon: 'key' },
    ],
  },
]
/* MenuNode 是 Menu 的递归单元，核对页单独挂载时需补必填的 item/depth/vertical */
export const MENU_NODE_ITEM = MENU_ITEMS[2]
export const TAB_ITEMS = [  { key: 'tab1', label: '概览' },
  { key: 'tab2', label: '明细' },
  { key: 'tab3', label: '日志', disabled: true },
]
export const CASCADER_OPTIONS = [
  {
    label: '总部',
    value: 1,
    children: [
      { label: '研发部', value: 11 },
      { label: '市场部', value: 12 },
    ],
  },
  { label: '分公司', value: 2, children: [{ label: '华东', value: 21 }] },
]
export const TRANSFER_DATA = [
  { key: 1, label: '用户管理' },
  { key: 2, label: '角色管理' },
  { key: 3, label: '字典管理' },
  { key: 4, label: '操作日志', disabled: true },
]
export const TREE_SELECT_DATA = [
  {
    key: 1,
    title: '总部',
    children: [
      { key: 11, title: '研发部' },
      { key: 12, title: '市场部' },
    ],
  },
  { key: 2, title: '分公司', children: [{ key: 21, title: '华东' }] },
]
/* 通用树样本用 label 字段（Tree 的契约），与上面 TreeSelect 的 title 契约不同，不能互相顶替 */
export const TREE_DATA = [
  {
    key: 1,
    label: '总部',
    children: [
      { key: 11, label: '研发部' },
      { key: 12, label: '市场部', children: [{ key: 121, label: '品牌组' }] },
    ],
  },
  { key: 2, label: '分公司', children: [{ key: 21, label: '华东' }] },
]
export const UPLOAD_FILES = [
  { uid: 'f1', name: '权限清单.xlsx', size: 24576, status: 'success' as const, percent: 100 },
  { uid: 'f2', name: '接口文档.pdf', size: 512000, status: 'uploading' as const, percent: 46 },
]
export const OVERFLOW_ITEMS = [
  { key: 'a', label: '系统管理' },
  { key: 'b', label: '监控中心' },
  { key: 'c', label: '工具中心' },
  { key: 'd', label: '系统设置' },
]
/* 复选组样本：一项预选、一项禁用，既看得出选中态也能看出边界态 */
export const CHECKBOX_OPTIONS = [
  { label: '用户管理', value: 'a' },
  { label: '角色管理', value: 'b' },
  { label: '字典管理', value: 'c', disabled: true },
]
export const TIMELINE_ITEMS = [
  { label: '2026-10-15', content: '发布 v1.0', time: '10:24' },
  { label: '2026-10-14', content: '完成权限矩阵重构', time: '18:02' },
]
/* 内联 SVG 占位图：核对页不依赖外网资源，避免离线时图片组件显示为加载失败 */
export const IMAGE_SRC = 'data:image/svg+xml,' + encodeURIComponent(
  '<svg xmlns="http://www.w3.org/2000/svg" width="200" height="110"><rect width="200" height="110" fill="#d7e7fb"/><circle cx="100" cy="55" r="26" fill="#236de9" opacity=".5"/></svg>',
)
/* 预览组需要多张可区分的图，同色会让人看不出切图是否真的生效 */
function previewSvg(fill: string, accent: string) {
  return 'data:image/svg+xml,' + encodeURIComponent(
    `<svg xmlns="http://www.w3.org/2000/svg" width="480" height="300"><rect width="480" height="300" fill="${fill}"/><circle cx="240" cy="150" r="70" fill="${accent}" opacity=".55"/></svg>`,
  )
}
export const PREVIEW_IMAGES = [
  { src: previewSvg('#d7e7fb', '#236de9'), alt: '示例图一' },
  { src: previewSvg('#dff3e2', '#3f9d54'), alt: '示例图二' },
  { src: previewSvg('#fbe8d7', '#d97b2b'), alt: '示例图三' },
]
