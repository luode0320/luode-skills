/* 业务组件类策展变体：机械派生覆盖不到的数据长度、选中态、步骤与加载态差异。
   与 base、generated 归并后每个组件 ≥3 组可用示例。
   最近修改时间：2026-10-17 11:00:00；改动原因：补部门/字典选择空态、权限矩阵单角色、
   岗位全量等真实差异，并新增 DeptSelect / DictSelect / FormDialog 策展条目。 */
import type { VariantShape } from './demo-variants.types'
import {
  BOARD_COLUMNS, DICT_TYPES, GEN_TABLE, LADDER_POSTS, MATRIX_ROLES, MENU_TREE,
} from './demo-business-samples'

/** 业务组件的策展变体 */
export const CURATED_BUSINESS: Record<string, VariantShape[]> = {
  AskDock: [
    { label: '紧凑', props: { compact: true } },
    { label: '指定分组', props: { group: '系统管理', placeholder: '问问系统管理…' } },
    { label: '默认分组', props: { group: '全部', placeholder: '输入问题后回车' } },
  ],
  BoardView: [
    { label: '不可拖拽', props: { draggable: false } },
    { label: '单列看板', props: { columns: BOARD_COLUMNS.slice(0, 1) } },
    { label: '两列看板', props: { columns: BOARD_COLUMNS.slice(0, 2) } },
  ],
  DeptTree: [
    { label: '选市场', props: { modelValue: 12 } },
    { label: '未选中', props: { modelValue: null } },
    { label: '选华东', props: { modelValue: 21 } },
  ],
  DeptSelect: [
    { label: '未选部门', props: { modelValue: null } },
    { label: '选市场部', props: { modelValue: 12 } },
    { label: '顶层可选项', props: { modelValue: 0, rootLabel: '无上级部门' } },
  ],
  DictSelect: [
    { label: '未选值', props: { modelValue: '' } },
    { label: '停用值', props: { modelValue: '0' } },
    { label: '带全部项', props: { allLabel: '全部状态', modelValue: '' } },
  ],
  DictSwatchbook: [
    /* loading 的文案门控条件是 !types.length：只改 loading 而数据仍在，卡片与基础格完全一致，
       必须连空数据一起给才出加载态 */
    { label: '加载态', props: { loading: true, types: [] } },
    { label: '单类型', props: { types: DICT_TYPES.slice(0, 1) } },
  ],
  FormDialog: [
    { label: '超窄弹窗', props: { width: 380 } },
    { label: '超宽弹窗', props: { width: 900 } },
    { label: '保存中', props: { saving: true, submitText: '保存中…' } },
  ],
  DictTag: [
    { label: '停用', props: { value: '0' } },
    { label: '空值', props: { value: null } },
    { label: '启用', props: { value: '1' } },
    { label: '数值型停用', props: { value: 0 } },
  ],
  GeneratorPipeline: [
    { label: '第二步', props: { step: 2, table: GEN_TABLE } },
    { label: '第三步', props: { step: 3, table: GEN_TABLE } },
    { label: '空表第一步', props: { step: 1, table: null } },
  ],
  InsightPanel: [
    { label: '部门维度', props: { kind: 'dept', title: '部门洞察', contentKey: 'demo-dept', subtitle: '研发部 · 12 人' } },
    { label: '带指标条', props: { contentKey: 'demo-metric', status: '已复核', metric: { label: '请求量', value: 128, unit: '次/分', bars: [3, 6, 4, 8, 5] } } },
    { label: '角色维度', props: { kind: 'role', title: '角色洞察', contentKey: 'demo-role', subtitle: '超级管理员 · 3 人', status: '待复核' } },
  ],
  ListPage: [
    { label: '不可选', props: { selectable: false } },
    { label: '副表视图', props: { altView: true, tableTitle: '账号清单' } },
  ],
  /* DataTable 基础示例：selectable:true，selected:[]；机械派生只剩 loading 与 tree，
     这里补「空数据」「不可选」「宽表横向滚动」。rowKey 只影响选中项的取值，
     selected 为空时改它看不出任何差别，故不作示例维度。 */
  DataTable: [
    { label: '空数据', props: { data: [], emptyText: '暂无记录' } },
    { label: '不可选', props: { selectable: false } },
    { label: '宽表横向滚动', props: { minWidth: 640 } },
  ],
  MenuStarMap: [
    { label: '单目录', props: { tree: MENU_TREE.slice(0, 1) } },
    { label: '平铺无层级', props: { tree: MENU_TREE.map((m) => ({ ...m, children: [] })) } },
    { label: '仅监控目录', props: { tree: MENU_TREE.filter((m) => m.id === 2) } },
  ],
  OrgCanvas: [
    { label: '未选中', props: { selectedId: null } },
    { label: '选市场部', props: { selectedId: 12 } },
    { label: '选总部', props: { selectedId: 1 } },
  ],
  PermissionMatrix: [
    { label: '只读', props: { editable: false } },
    { label: '保存中', props: { saving: true, editable: false } },
    { label: '单角色', props: { roles: MATRIX_ROLES.slice(0, 1) } },
  ],
  PermissionTrace: [
    { label: '画布 320 高', canvas: 320 },
    { label: '画布 440 高', canvas: 440 },
    { label: '画布 560 高', canvas: 560 },
  ],
  PermissionTree: [
    { label: '多选两个', props: { modelValue: [11, 12] } },
    { label: '未勾选', props: { modelValue: [] } },
    { label: '全选目录', props: { modelValue: MENU_TREE.map((m) => m.id) } },
  ],
  PostLadder: [
    /* loading 在本组件没有可见分支（只有 !loading && !steps.length 才渲染空态），
       改 loading 看不出差异，示例差异只能做在岗位台阶数量上 */
    { label: '单个岗位', props: { posts: LADDER_POSTS.slice(0, 1) } },
    { label: '两个岗位', props: { posts: LADDER_POSTS.slice(0, 2) } },
    { label: '全部岗位', props: { posts: LADDER_POSTS } },
  ],
  SearchForm: [
    { label: '加载态', props: { loading: true } },
    { label: '空闲态', props: { loading: false } },
  ],
  UserSelect: [
    /* 基础示例已选 admin 且可清除：给未选与不可清除两种真实可选态；
       valueKey=nickname 已由派生覆盖，这里不再重复 */
    { label: '未选人', props: { modelValue: null } },
    { label: '不可清除', props: { clearable: false } },
    { label: '选中另一人', props: { modelValue: 'lin' } },
  ],
}
