/* 按组件名取必填 props：返回空对象表示该组件无需必填 props。
   属于组件库示例页（后台路由 /gallery）的展示样本，不参与组件库生产运行；
   数据形状严格对齐组件真实类型定义。
   最近修改时间：2026-10-16 20:23:00；改动原因：示例页迁入后台真实路由后本批样本进入 src 并按业务语义拆成同级文件，
   两级分类落地后继续为子分组组件补齐最小可渲染样本。
*/
import { ref } from 'vue'
import { phone, required } from '../../utils/validate'
import { DEPT_TREE, DICT_TYPES, GRAPH_LINKS, GRAPH_NODES, HEAT_CELLS, LADDER_POSTS, MATRIX_GRANTS, MATRIX_ROLES, MENU_TREE, SEGMENT_OPTIONS, SELECT_OPTIONS, SWIM_LANES, TABLE_COLUMNS, TABLE_ROWS, TREND_LABELS, TREND_VALUES, boardDemo } from './demo-business-samples'
import { ACTIVITY_ITEMS, ANCHOR_ITEMS, BREADCRUMB_ITEMS, CASCADER_OPTIONS, CHECKBOX_OPTIONS, DROPDOWN_ITEMS, IMAGE_SRC, MENU_ITEMS, MENU_NODE_ITEM, OVERFLOW_ITEMS, PREVIEW_IMAGES, READOUT_ITEMS, READOUT_ROWS, SHARE_ITEMS, SHORTCUT_ITEMS, STEP_ITEMS, TAB_ITEMS, TIMELINE_ITEMS, TRANSFER_DATA, TREE_DATA, TREE_SELECT_DATA, UPLOAD_FILES } from './demo-display-samples'

/** ListPage 需要一个最小可用的列表状态桩（真实项目由 useListPage 组合式函数提供）。 */const DEMO_LIST = {
  query: {},
  rows: ref(TABLE_ROWS),
  total: ref(TABLE_ROWS.length),
  page: ref(1),
  pageSize: ref(10),
  loading: ref(false),
  exporting: ref(false),
  selected: ref<(string | number)[]>([]),
  load: async () => {},
  search: async () => {},
  reset: async () => {},
  setPage: async () => {},
  setPageSize: async () => {},
  exportData: async () => {},
  canExport: false,
}

/** 按组件名取 demo 属性；返回空对象表示该组件无需必填 props。 */
export function demoProps(name: string): Record<string, unknown> {
  switch (name) {
    case 'Icon': return { name: 'user', size: 20 }
    case 'IconButton': return { name: 'refresh', label: '刷新' }
    case 'Metric': case 'Odometer': case 'TickRing': return { value: 1284 }
    case 'DeltaPill': return { value: 12.4 }
    case 'PageHeader': return { title: '用户管理', desc: '维护账号、部门与角色绑定' }
    case 'Checkbox': case 'Switch': return { modelValue: true, label: '启用' }
    case 'Segmented': return { modelValue: '7d', options: SEGMENT_OPTIONS }
    case 'Select': return { modelValue: '1', options: SELECT_OPTIONS }
    case 'StatusTag': return { status: 1 }
    case 'SectionLabel': return { title: '区块标题' }
    case 'Avatar': return { name: '罗德', size: 36 }
    case 'TextInput': return { modelValue: '罗德', placeholder: '请输入负责人', clearable: true }
    case 'Field': return { label: '负责人', required: true, hint: '输入姓名' }
    case 'Ruler': return { labels: ['00', '06', '12', '18', '24'], marker: 0.62, markerLabel: '14:52' }
    case 'EmptyState': return { title: '暂无数据', desc: '调整筛选条件后重试', icon: 'search' }
    case 'Modal': case 'Drawer': case 'FormDialog': return { open: true, title: '示例弹窗' }
    /* 这三个弹层自带固定标题、不声明 title，多传会触发「extraneous non-props attributes」警告 */
    case 'AppearanceDialog': case 'CommandPalette': case 'PasswordDialog': return { open: true }
    case 'DataTable': return { columns: TABLE_COLUMNS, data: TABLE_ROWS, selectable: true, selected: [] }
    case 'Pagination': return { total: 86, page: 1, pageSize: 10 }
    case 'SpecPlate': return { title: '本次操作', rows: [{ label: '总数', value: 86 }, { label: '异常', value: 2, tone: 'red' }] }
    case 'TrendChart': case 'BarChart': return { values: TREND_VALUES, labels: TREND_LABELS }
    case 'HeatGrid': return { cells: HEAT_CELLS }
    case 'Swimlane': return { lanes: SWIM_LANES, nowSec: 15 * 3600 }
    case 'RelationGraph': return { nodes: GRAPH_NODES, links: GRAPH_LINKS }
    case 'BoardView': return boardDemo()
    case 'DictSwatchbook': return { types: DICT_TYPES }
    case 'DictTag': return { type: 'sys_status', value: '1' }
    case 'DictSelect': return { type: 'sys_status', modelValue: '1' }
    case 'PostLadder': return { posts: LADDER_POSTS }
    case 'PermissionMatrix': return { menus: MENU_TREE, roles: MATRIX_ROLES, grants: MATRIX_GRANTS, editable: true }
    case 'PermissionTree': return { menus: MENU_TREE, modelValue: [11] }
    case 'MenuStarMap': return { tree: MENU_TREE }
    case 'OrgCanvas': return { tree: DEPT_TREE, selectedId: 11 }
    case 'GeneratorPipeline': return { table: null }
    case 'InsightPanel': return { contentKey: 'demo', kind: 'user', title: '洞察' }
    case 'DeptTree': case 'DeptSelect': return { modelValue: 11 }
    case 'UserSelect': return { modelValue: 'admin' }
    case 'ListPage': return { title: '用户管理', columns: TABLE_COLUMNS, list: DEMO_LIST }
    case 'ShareList': return { items: SHARE_ITEMS }
    case 'ActivityList': return { items: ACTIVITY_ITEMS }
    case 'ShortcutGrid': return { items: SHORTCUT_ITEMS }
    case 'ReadoutStrip': return { items: READOUT_ITEMS }
    case 'KeyValueReadout': return { rows: READOUT_ROWS }
    case 'Form': return {
      model: { name: '', phone: '' },
      rules: { name: [required('请输入姓名')], phone: [phone] },
    }
    case 'Descriptions': return {
      title: '订单详情',
      column: 1,
      bordered: true,
      data: [
        { label: '订单号', value: 'SO-2026-1015-0042' },
        { label: '下单时间', value: '2026-10-15 09:20' },
        { label: '状态', value: '已发货' },
        { label: '收货人', value: '罗德' },
        { label: '金额', value: '¥1,280.00' },
        { label: '备注', value: '工作日白天送达，放前台即可。' },
      ],
    }
    case 'BentoCard': return { span: 'third', title: '示例卡片', meta: '共 3 项' }
    case 'Band': return { title: '横带分区' }
    case 'PermissionButton': return { perm: 'system:user:list', variant: 'primary', label: '新增用户' }
    /* ── Arco 品类对齐层（extend）：按组件名给最小可渲染样本 ── */
    case 'Badge': return { value: 12, max: 99 }
    case 'Steps': return { current: 1, items: STEP_ITEMS, clickable: true }
    case 'Tooltip': return { content: '这是一段提示说明' }
    case 'HelpTip': return { title: '审批时限', content: '指提交后到审批完成的最长工作日，超时自动提醒审批人。' }
    case 'Alert': return { type: 'info', title: '提示', closable: true }
    case 'Notification': return { type: 'success', title: '操作成功', message: '数据已保存到本地', closable: true }
    case 'Progress': return { percent: 62, status: 'normal' }
    case 'Result': return { status: 'success', title: '提交成功', subTitle: '审批流程已启动' }
    case 'Spin': return { loading: true, tip: '加载中' }
    case 'Popconfirm': return { title: '删除确认', message: '确定删除这条记录吗？', danger: true }
    case 'Popover': return { title: '气泡标题', content: '气泡卡片内容' }
    case 'Trigger': return { trigger: ['click'], placement: 'bottom' }
    case 'Affix': return { offsetTop: 0 }
    case 'Anchor': return { items: ANCHOR_ITEMS }
    /* 阈值 -1 让按钮在核对页（未滚动）也浮出，否则按设计只在滚动后出现，卡内看不出效果 */
    case 'BackTop': return { visibilityHeight: -1 }
    case 'Breadcrumb': return { items: BREADCRUMB_ITEMS }
    case 'Dropdown': return { items: DROPDOWN_ITEMS }
    case 'Menu': return { modelValue: 'users', items: MENU_ITEMS }
    case 'MenuNode': return { item: MENU_NODE_ITEM, depth: 0, vertical: true, selected: 'operlog' }
    case 'Tabs': return { modelValue: 'tab1', items: TAB_ITEMS }
    case 'TabPane': return { active: true, label: '标签一' }
    case 'AutoComplete': return { modelValue: '罗', options: [{ label: '罗德', value: '罗德' }, { label: '林可', value: '林可' }] }
    case 'Cascader': return { modelValue: [1, 11], options: CASCADER_OPTIONS }
    case 'CascaderPanel': return { modelValue: [1, 11], options: CASCADER_OPTIONS, columnWidth: 120 }
    /* 默认展开整棵小树，核对页打开就能看到层级与勾选态，不用先手点 */
    case 'Tree': return { modelValue: [11, 121], data: TREE_DATA, checkable: true, multiple: true, defaultExpandAll: true, showLine: true }
    /* 递归单元独立挂载时无父级上下文，给一个顶层节点即可降级为静态展示 */
    case 'TreeNode': return { node: TREE_DATA[0], depth: 0, parentKey: null }
    case 'ColorPicker': return { modelValue: '#236de9', showText: true }
    case 'DatePicker': return { modelValue: '2026-10-15' }
    case 'RangePicker': return { modelValue: ['2026-10-01', '2026-10-15'], clearable: true }
    case 'MonthPicker': return { modelValue: '2026-10', clearable: true }
    case 'WeekPicker': return { modelValue: '2026-W42', clearable: true }
    case 'QuarterPicker': return { modelValue: '2026-Q4', clearable: true }
    case 'YearPicker': return { modelValue: '2026', clearable: true }
    case 'ImagePreview': return { src: IMAGE_SRC, visible: false, title: '示例图预览' }
    case 'ImagePreviewGroup': return { images: PREVIEW_IMAGES, visible: false, initialIndex: 0 }
    case 'DropdownButton': return { items: DROPDOWN_ITEMS, type: 'primary' }
    case 'DropdownSubmenu': return { label: '更多操作', items: DROPDOWN_ITEMS }
    /* 固定剩余秒数而非 target 时间戳：核对页停留时间不确定，绝对时刻会走成负数 */
    case 'Countdown': return { remaining: 3661, format: 'HH:mm:ss' }
    case 'InputSearch': return { modelValue: '', placeholder: '搜索组件名', allowClear: true }
    case 'InputPassword': return { modelValue: 'admin123', placeholder: '请输入密码' }
    case 'Textarea': return { modelValue: '用于验证自动高度：随内容增高，超过 maxRows 后改为内部滚动。', autoSize: true, maxRows: 5, maxlength: 200, placeholder: '请输入备注' }
    case 'InputGroup': return { direction: 'horizontal' }
    case 'CheckboxGroup': return { modelValue: ['a'], options: CHECKBOX_OPTIONS, checkAll: true }
    case 'ButtonGroup': return { size: 'md' }
    case 'AvatarGroup': return { max: 3, size: 32, total: 5 }
    case 'Card': return { title: '组件卡片', subtitle: '带描边与阅读面', hoverable: true }
    case 'CardMeta': return { title: '罗德', description: '总部 · 超级管理员', avatar: '罗德' }
    case 'CardGrid': return { columns: 2, gutter: 12 }
    case 'InputNumber': return { modelValue: 12, min: 0, max: 100 }
    case 'InputTag': return { modelValue: ['系统管理', '监控中心'] }
    case 'Mention': return { modelValue: '@罗德 ', options: [{ value: '罗德', label: '罗德' }, { label: '林可', value: '林可' }] }
    case 'Radio': return { modelValue: 'a', value: 'a', label: '选项 A' }
    case 'RadioGroup': return { modelValue: 'a' }
    case 'Rate': return { modelValue: 4, count: 5 }
    case 'Slider': return { modelValue: 40, min: 0, max: 100 }
    case 'TimePicker': return { modelValue: '14:52:00' }
    case 'Transfer': return { modelValue: [1], data: TRANSFER_DATA }
    case 'TreeSelect': return { modelValue: 11, data: TREE_SELECT_DATA }
    case 'Upload': return { fileList: UPLOAD_FILES, drag: true }
    case 'VerificationCode': return { modelValue: '123', length: 6 }
    case 'Calendar': return { modelValue: '2026-10-15' }
    case 'Carousel': return { current: 0 }
    case 'Collapse': return { modelValue: ['a'] }
    case 'CollapseItem': return { name: 'a', title: '折叠面板一' }
    case 'Comment': return { author: '罗德', content: '这条记录已复核，可以放行。', datetime: '2026-10-15 10:24', actions: ['回复', '删除'] }
    case 'Image': return { src: IMAGE_SRC, alt: '示例图', width: 200, height: 110, preview: true }
    case 'LinkText': return { href: '#', type: 'primary' }
    case 'DataList': return { data: TABLE_ROWS, bordered: true }
    case 'OverflowList': return { items: OVERFLOW_ITEMS, maxCount: 2 }
    case 'Skeleton': return { loading: true, rows: 3 }
    case 'Timeline': return { items: TIMELINE_ITEMS }
    case 'TimelineItem': return { label: '2026-10-15', content: '发布 v1.0', time: '10:24' }
    case 'Typography': return { type: 'title', heading: 3, copyable: true, content: '可复制的标题' }
    case 'Watermark': return { content: '内部资料' }
    case 'Divider': return { margin: 12 }
    case 'GridRow': return { gutter: 12 }
    case 'GridCol': return { span: 12 }
    case 'ResizeBox': return { width: 180, height: 90, minWidth: 80, minHeight: 60 }
    case 'StyledScrollbar': return { maxHeight: 90 }
    case 'Space': return { size: 'md' }
    case 'SplitPane': return { modelValue: 50, min: 20, max: 80 }
    default: return {}
  }
}
