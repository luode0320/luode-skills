/* 业务组件样本：表格、看板、矩阵、流水线与图表的 demo 数据。
   属于组件库示例页（后台路由 /gallery）的展示样本，不参与组件库生产运行；
   数据形状严格对齐组件真实类型定义。
   最近修改时间：2026-10-17 04:25:00；改动原因：Swimlane 样本补第三条泳道，
   让 maxLanes 的「另有 N 个模块未显示」提示有真实可见差异。
*/
import { reactive } from 'vue'
import type { Column } from '../../components/ui/DataTable.vue'
import type { SelectOption } from '../../components/ui/Select.vue'
import type { BoardColumn } from '../../components/business/BoardView.vue'
import type { DictTypeRow } from '../../components/business/DictSwatchbook.vue'
import type { LadderPost } from '../../components/business/PostLadder.vue'
import type { MatrixRole } from '../../components/business/PermissionMatrix.vue'
import type { GenTable } from '../../components/business/GeneratorPipeline.vue'
import type { GraphNode, GraphLink } from '../../components/charts/RelationGraph.vue'
import type { SwimlaneLane } from '../../components/charts/Swimlane.vue'
import type { HeatCell } from '../../utils/heatmap'
import type { Menu, Dept } from '../../data'

/** 折线 / 柱状 / 环形共用的数值序列。 */
export const TREND_VALUES = [12, 18, 9, 24, 31, 22, 27]
export const TREND_LABELS = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']

/** 表格列与行。 */
export const TABLE_COLUMNS: Column[] = [
  { key: 'name', title: '名称' },
  { key: 'owner', title: '负责人' },
  { key: 'status', title: '状态', align: 'center' },
]
export const TABLE_ROWS = [
  { id: 1, name: '用户管理', owner: '罗德', status: '启用' },
  { id: 2, name: '角色管理', owner: '林可', status: '启用' },
  { id: 3, name: '字典管理', owner: '陈舟', status: '停用' },
]

/** 下拉与分段选项。 */
export const SELECT_OPTIONS: SelectOption[] = [
  { label: '全部', value: '' },
  { label: '启用', value: '1' },
  { label: '停用', value: '0' },
]
export const SEGMENT_OPTIONS = [
  { label: '24 小时', value: '24h' },
  { label: '7 天', value: '7d' },
  { label: '30 天', value: '30d' },
]

/** 菜单树与部门树。 */
export const MENU_TREE: Menu[] = [
  {
    id: 1, name: '系统管理', parentId: 0, type: 'dir', icon: 'setting', sort: 1, status: 1,
    children: [
      { id: 11, name: '用户管理', parentId: 1, type: 'menu', icon: 'user', path: '/system/users', permission: 'system:user:list', sort: 1, status: 1 },
      { id: 12, name: '角色管理', parentId: 1, type: 'menu', icon: 'role', path: '/system/roles', permission: 'system:role:list', sort: 2, status: 1 },
    ],
  },
  { id: 2, name: '监控中心', parentId: 0, type: 'dir', icon: 'log', sort: 2, status: 1 },
]
export const DEPT_TREE: Dept[] = [
  {
    id: 1, name: '总部', parentId: 0, leader: '罗德', memberCount: 18, sort: 1, status: 1,
    children: [
      { id: 11, name: '研发部', parentId: 1, leader: '林可', memberCount: 12, sort: 1, status: 1 },
      { id: 12, name: '市场部', parentId: 1, leader: '陈舟', memberCount: 6, sort: 2, status: 1 },
    ],
  },
]

/** 看板列。 */
export const BOARD_COLUMNS: BoardColumn<Record<string, any>>[] = [
  { key: 'todo', title: '待处理', items: [{ id: 1, title: '登录日志排查' }, { id: 2, title: '角色权限复核' }] },
  { key: 'doing', title: '进行中', items: [{ id: 3, title: '字典数据整理' }] },
  { key: 'done', title: '已完成', items: [{ id: 4, title: '菜单星图上新' }] },
]

/** [参数] 无 [返回] BoardView 所需 props；看板样本：拖拽落列时真实搬运数据，让核对页能演示「拖起→落到另一列→落定」而不是只摆四列静态卡。
    columns 用 reactive 数组而不是 ref——核对页顶层状态只做浅响应，ref 会原样传给组件导致读不到长度。
    最近修改时间：2026-10-16 16:05:00；改动原因：受控回写改为浅响应后，原 ref 形态与组件读取方式不匹配。 */
export function boardDemo() {
  const columns = reactive<BoardColumn<Record<string, any>>[]>(BOARD_COLUMNS.map((c) => ({ ...c, items: c.items.map((i) => ({ ...i })) })))
  const onMove = async ({ item, from, to }: { item: Record<string, any>; from: BoardColumn<Record<string, any>>; to: BoardColumn<Record<string, any>> }) => {
    const src = columns.find((c) => c.key === from.key)
    const dst = columns.find((c) => c.key === to.key)
    if (!src || !dst || src.key === dst.key) return false
    src.items = src.items.filter((r) => r.id !== item.id)
    dst.items = [...dst.items, item]
    return true
  }
  return { columns, itemKey: 'id', draggable: true, onMove }
}

/** 字典样本册：字典类型必须与 mock /api/system/dict/types 一致，否则核对页会显示「0 项」。 */
export const DICT_TYPES: DictTypeRow[] = [
  { id: 1, dictName: '系统状态', dictType: 'sys_status', status: 1, remark: '通用启用/停用' },
  { id: 2, dictName: '通知类型', dictType: 'notice_type', status: 1, remark: '公告 / 升级 / 安全' },
]

/** 岗位阶梯。 */
export const LADDER_POSTS: LadderPost[] = [
  { id: 1, postName: '初级工程师', postCode: 'junior', sort: 1, status: 1, userCount: 6 },
  { id: 2, postName: '高级工程师', postCode: 'senior', sort: 2, status: 1, userCount: 4 },
  { id: 3, postName: '技术专家', postCode: 'expert', sort: 3, status: 1, userCount: 2 },
]

/** 权限矩阵。 */
export const MATRIX_ROLES: MatrixRole[] = [
  { id: 1, name: '超级管理员', code: 'admin', builtin: true, status: 1 },
  { id: 2, name: '运营', code: 'operator', status: 1 },
]
export const MATRIX_GRANTS: Record<number, number[]> = { 1: [1, 11, 12, 2], 2: [1, 11] }

/** 代码生成流水线：open 由组件内部按 Boolean(table) 推导，核对页默认传 null 保持关闭。 */
export const GEN_TABLE: GenTable = {
  id: 1, tableName: 'sys_user', tableComment: '用户表', className: 'SysUser',
  module: 'system', businessName: 'user', synced: true,
}

/** 关系图节点与连线。 */
export const GRAPH_NODES: GraphNode[] = [
  { id: 'core', x: 260, y: 150, label: '系统', kind: 'core', size: 74, cat: 1 },
  { id: 'a', x: 90, y: 90, label: '用户', kind: 'item', cat: 2, from: 'core' },
  { id: 'b', x: 430, y: 90, label: '角色', kind: 'item', cat: 3, from: 'core' },
  { id: 'c', x: 90, y: 220, label: '部门', kind: 'item', cat: 4, from: 'core' },
  { id: 'd', x: 430, y: 220, label: '字典', kind: 'item', cat: 5, from: 'core' },
]
export const GRAPH_LINKS: GraphLink[] = [
  { a: 'core', b: 'a', flow: 'forward', cat: 2 },
  { a: 'core', b: 'b', flow: 'forward', cat: 3 },
  { a: 'core', b: 'c', flow: 'forward', cat: 4 },
  { a: 'core', b: 'd', flow: 'forward', cat: 5 },
]

/** 泳道。第三条是刻意多出来的：maxLanes 的「另有 N 个模块未显示」要靠泳道数超过上限才会出现，
    只有两条时限两道与不限完全看不出差别。 */
export const SWIM_LANES: SwimlaneLane[] = [
  {
    module: '用户管理', count: 3,
    blocks: [
      { startSec: 9 * 3600, endSec: 9 * 3600 + 240, count: 2, failed: 0, maxCost: 120, ids: [1, 2] },
      { startSec: 14 * 3600, endSec: 14 * 3600 + 420, count: 1, failed: 1, maxCost: 860, ids: [3] },
    ],
  },
  {
    module: '角色管理', count: 2,
    blocks: [{ startSec: 11 * 3600, endSec: 11 * 3600 + 180, count: 2, failed: 0, maxCost: 90, ids: [4, 5] }],
  },
  {
    module: '菜单管理', count: 1,
    blocks: [{ startSec: 16 * 3600, endSec: 16 * 3600 + 300, count: 1, failed: 0, maxCost: 480, ids: [6] }],
  },
]

/** 热力格：铺出工作时段的高峰，避免全空看不出分位。 */
export const HEAT_CELLS: HeatCell[] = Array.from({ length: 7 }, (_, dow) =>
  Array.from({ length: 24 }, (_, hour) => {
    const peak = hour >= 9 && hour <= 18 && dow < 5
    const total = peak ? 12 + ((hour * 7 + dow * 5) % 9) : (hour % 3)
    const failed = peak && hour % 5 === 0 ? 3 : 0
    return { dow, hour, total, failed }
  }),
).flat()

/** 占比条。 */
