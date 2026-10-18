/* 组件分类真相源·基础类（通用/布局/导航）：二级拆分后的静态映射数据。
   本文件为纯声明式静态映射表，按仓库规则允许突破单文件行数基准。
   约束：每个组件恰好归入一个子分组，子分组恰好归属一个父分类，由
   scripts/check_component_categories.mjs 与磁盘全集双向对账，漂移即 FAIL。
   子分组一律按「单一概念」命名：不用「A与B」把两类能力塞进同一个菜单项，
   每项只收同一类组件，菜单点进去才是一个语义明确的页面。
   最近修改时间：2026-10-17 10:42:00；改动原因：用户要求菜单继续分细，
   「标识与头像」拆成标识、头像，其余带「与」的复合项同步拆成单一概念。 */
import type { ComponentCategory } from './component-categories.types'

export const BASIC_CATEGORIES: ComponentCategory[] = [
  {
    key: 'general',
    label: '通用',
    icon: 'layers',
    desc: '按钮、图标、排版、标签与头像等最基础的原子组件',
    subGroups: [
      { key: 'button', label: '按钮', icon: 'tool', desc: '主/次/幽灵按钮、图标按钮与按钮组', components: ['Button', 'IconButton', 'ButtonGroup'] },
      { key: 'link', label: '文字链接', icon: 'arrowRight', desc: '行内文字链接的语义与下划线形态', components: ['LinkText'] },
      { key: 'icon', label: '图标', icon: 'file', desc: '按名取用的图标集', components: ['Icon'] },
      { key: 'typography', label: '排版', icon: 'edit', desc: '标题、正文、辅助文字等排版原子', components: ['Typography'] },
      { key: 'tag', label: '标识', icon: 'check', desc: '普通标签、状态标签与徽标', components: ['Tag', 'StatusTag', 'Badge'] },
      { key: 'avatar', label: '头像', icon: 'user', desc: '单个头像与头像组折叠', components: ['Avatar', 'AvatarGroup'] },
    ],
  },
  {
    key: 'layout',
    label: '布局',
    icon: 'grid',
    desc: '间距、分割、栅格、容器、分栏与滚动等排布能力',
    subGroups: [
      { key: 'space', label: '间距', icon: 'grid', desc: '横向/纵向间距与对齐', components: ['Space'] },
      { key: 'divider', label: '分割线', icon: 'minus', desc: '区块与行内分割线', components: ['Divider'] },
      { key: 'grid', label: '栅格', icon: 'grid', desc: '行列栅格与跨列布局', components: ['GridRow', 'GridCol'] },
      { key: 'container', label: '容器', icon: 'fit', desc: '面板容器与可拉伸容器', components: ['Panel', 'ResizeBox'] },
      { key: 'split', label: '分栏', icon: 'sidebar', desc: '可拖拽的左右分栏', components: ['SplitPane'] },
      { key: 'scrollbar', label: '滚动条', icon: 'more', desc: '自绘滚动条', components: ['StyledScrollbar'] },
    ],
  },
  {
    key: 'navigation',
    label: '导航',
    icon: 'menu',
    desc: '菜单、下拉、面包屑、定位、分页、步骤与标签页',
    subGroups: [
      { key: 'menu', label: '菜单', icon: 'menu', desc: '侧栏菜单树与菜单节点', components: ['Menu', 'MenuNode'] },
      { key: 'dropdown', label: '下拉', icon: 'chevronDown', desc: '下拉菜单、下拉按钮、子菜单与命令面板', components: ['Dropdown', 'DropdownButton', 'DropdownSubmenu', 'CommandPalette'] },
      { key: 'breadcrumb', label: '面包屑', icon: 'chevronRight', desc: '层级路径导航', components: ['Breadcrumb'] },
      { key: 'locate', label: '定位', icon: 'activity', desc: '锚点、固钉与回到顶部', components: ['Anchor', 'Affix', 'BackTop'] },
      { key: 'pager', label: '分页', icon: 'more', desc: '分页器与分段器', components: ['Pagination', 'Segmented'] },
      { key: 'steps', label: '步骤条', icon: 'check', desc: '多步流程的进度指引', components: ['Steps'] },
      { key: 'tabs', label: '标签页', icon: 'board', desc: '标签页与标签面板', components: ['Tabs', 'TabPane'] },
      { key: 'pageheader', label: '页头', icon: 'file', desc: '页面级标题、描述与操作区', components: ['PageHeader'] },
    ],
  },
]
