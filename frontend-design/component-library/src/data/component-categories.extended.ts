/* 组件分类真相源·扩展类（图表/业务组件/工作台版式/外壳与系统）：二级拆分后的静态映射表，
   按仓库规则允许突破单文件行数基准。
   子分组一律按「单一概念」命名：不使用「A与B」把两类能力塞进同一个菜单项。
   最近修改时间：2026-10-17 10:42:00；改动原因：用户要求菜单继续分细，
   图表、业务、工作台与外壳里的复合项拆成单一概念（矩阵、热力、权限矩阵、字典、组织等各自成页）。 */
import type { ComponentCategory } from './component-categories.types'

export const EXTENDED_CATEGORIES: ComponentCategory[] = [
  {
    key: 'charts',
    label: '图表',
    icon: 'chart',
    desc: '零图表库自研：趋势、柱状、环形刻度、热力、泳道、关系图',
    subGroups: [
      { key: 'axis', label: '直角坐标', icon: 'chart', desc: '趋势图与柱状图', components: ['TrendChart', 'BarChart'] },
      { key: 'ring', label: '环形刻度', icon: 'activity', desc: '环形刻度读数', components: ['TickRing'] },
      { key: 'heat', label: '热力矩阵', icon: 'grid', desc: '二维热力格', components: ['HeatGrid'] },
      { key: 'swimlane', label: '泳道图', icon: 'activity', desc: '泳道时序分布', components: ['Swimlane'] },
      { key: 'graph', label: '关系图', icon: 'activity', desc: '节点关系与星系图', components: ['RelationGraph'] },
    ],
  },
  {
    key: 'business',
    label: '业务组件',
    icon: 'board',
    desc: '面向后台的中后台成套组件：列表页、权限、字典、组织等',
    subGroups: [
      { key: 'crud', label: '增删改查', icon: 'table', desc: '列表页、查询表单、表单弹窗与看板', components: ['ListPage', 'SearchForm', 'FormDialog', 'BoardView'] },
      { key: 'permission', label: '权限', icon: 'shield', desc: '权限矩阵、权限树、溯源与按钮', components: ['PermissionMatrix', 'PermissionTree', 'PermissionTrace', 'PermissionButton'] },
      { key: 'menustar', label: '菜单星系', icon: 'layers', desc: '菜单关系星系图', components: ['MenuStarMap'] },
      { key: 'org', label: '组织架构', icon: 'dept', desc: '组织画布与洞察面板', components: ['OrgCanvas', 'InsightPanel'] },
      { key: 'post', label: '岗位阶梯', icon: 'post', desc: '岗位层级阶梯', components: ['PostLadder'] },
      { key: 'dict', label: '字典', icon: 'dict', desc: '字典簿与字典标签、字典下拉', components: ['DictSwatchbook', 'DictTag', 'DictSelect'] },
      { key: 'dept', label: '部门选择', icon: 'dept', desc: '部门树与部门选择器', components: ['DeptTree', 'DeptSelect'] },
      { key: 'user', label: '用户选择', icon: 'user', desc: '用户选择器', components: ['UserSelect'] },
      { key: 'assistant', label: '智能辅助', icon: 'mail', desc: '问答 dock 与代码生成流水线', components: ['AskDock', 'GeneratorPipeline'] },
    ],
  },
  {
    key: 'workspace',
    label: '工作台版式',
    icon: 'dashboard',
    desc: '把工作台页面版式固化的组件：便当格、横带、读数条、流水与宫格',
    subGroups: [
      { key: 'bento', label: '便当格', icon: 'grid', desc: '便当格与便当卡', components: ['BentoGrid', 'BentoCard'] },
      { key: 'band', label: '横带', icon: 'sidebar', desc: '横向分区带', components: ['Band'] },
      { key: 'readout', label: '读数条', icon: 'activity', desc: '读数条与键值读数', components: ['ReadoutStrip', 'KeyValueReadout'] },
      { key: 'share', label: '分享榜', icon: 'chart', desc: '分享占比榜', components: ['ShareList'] },
      { key: 'activity', label: '动态列表', icon: 'activity', desc: '动态时间流', components: ['ActivityList'] },
      { key: 'shortcut', label: '快捷入口', icon: 'power', desc: '宫格快捷入口', components: ['ShortcutGrid'] },
    ],
  },
  {
    key: 'shell',
    label: '外壳与系统',
    icon: 'monitor',
    desc: '应用外壳、侧栏顶栏与外观/口令等系统级对话框',
    subGroups: [
      { key: 'frame', label: '应用外壳', icon: 'sidebar', desc: '整机外壳', components: ['AppShell'] },
      { key: 'sidebar', label: '侧栏', icon: 'menu', desc: '导航轨与菜单树', components: ['Sidebar'] },
      { key: 'topbar', label: '顶栏', icon: 'board', desc: '页面顶栏与操作区', components: ['Topbar'] },
      { key: 'system', label: '系统对话框', icon: 'gear', desc: '外观设置与口令修改', components: ['AppearanceDialog', 'PasswordDialog'] },
      { key: 'neural', label: '神经网络视图', icon: 'activity', desc: '授权关系神经网画布', components: ['NeuralNet'] },
    ],
  },
]
