/* ============================================================
   示例卡展示规格：组件类型 → 卡片在网格里占几列。
   此前所有组件共用同一张等宽卡，结果是弹层类只剩「预览弹层」四个字，
   数据密集类（表格、看板、矩阵）在卡内横向溢出、右侧列被裁。
   规格按「子分组」定义而不是按组件名：子分组本身就是一个品类，
   新增组件只要归进已有子分组就自动继承规格，不必回来补第二份清单。

   这里调的是宽度（跨列数）而不是高度：表格被裁是缺横向空间，
   加高只会把空白放大。高度仍由内容自然决定，同一档位的卡片保持等高。
   ============================================================ */
import { COMPONENT_SUB_GROUPS } from '../../data/component-categories'

/** inline 行内件 / panel 面板件 / stage 舞台件 / overlay 弹层件 */
export type DemoSpec = 'inline' | 'panel' | 'stage' | 'overlay'

/**
 * 各档占用的网格列数（以 6 列基准计）。
 * 6 列是为了让三档都能整除、每行不留空位：
 * 行内件与弹层件占 2 列（每行 3 张，与原来的三列观感一致），
 * 面板件占 3 列（每行 2 张，表格与看板才放得下），舞台件占满 6 列。
 * 具体列宽由 Gallery 的媒体查询消费，这里只登记基准值供文档与断言引用。
 */
export const SPEC_SPAN: Record<DemoSpec, number> = {
  inline: 2,
  panel: 3,
  stage: 6,
  overlay: 2,
}

/**
 * 子分组 → 规格。
 * 未登记的子分组按 inline 处理；这里是唯一真相源，改动只落这一处。
 */
const SPEC_BY_SUB_GROUP: Record<string, DemoSpec> = {
  // 通用：都是行内小件
  button: 'inline', link: 'inline', icon: 'inline',
  typography: 'inline', tag: 'inline', avatar: 'inline',

  // 布局：栅格、容器、分栏、滚动条需要真实占位才看得出结构
  space: 'inline', divider: 'inline',
  grid: 'panel', container: 'panel', split: 'panel', scrollbar: 'panel',

  // 导航：菜单、步骤条、标签页、页头是区块级；下拉是弹层
  menu: 'panel', steps: 'panel', tabs: 'panel', pageheader: 'panel', locate: 'panel',
  breadcrumb: 'inline', pager: 'inline',
  dropdown: 'overlay',

  // 数据输入：表单、穿梭、上传需要成片空间；选择类弹层收起时只是一行控件
  text: 'inline', search: 'inline', password: 'inline', number: 'inline',
  taginput: 'inline', mention: 'inline', select: 'inline',
  checkbox: 'inline', radio: 'inline', switch: 'inline', slider: 'inline',
  rate: 'inline', date: 'inline', range: 'inline', time: 'inline', verify: 'inline',
  form: 'panel', transfer: 'panel', upload: 'panel',
  cascader: 'overlay', treeselect: 'overlay', autocomplete: 'overlay', color: 'overlay',

  // 数据展示：数据密集件全部升到面板档；读数、刻度尺、空态仍是行内件
  table: 'panel', list: 'panel', tree: 'panel', descriptions: 'panel',
  collapse: 'panel', timeline: 'panel', card: 'panel', carousel: 'panel',
  image: 'panel', comment: 'panel', calendar: 'panel', skeleton: 'panel', watermark: 'panel',
  empty: 'inline', metric: 'inline', spec: 'inline', section: 'inline',
  ruler: 'inline', countdown: 'inline',
  hovercard: 'overlay', tooltip: 'overlay',

  // 反馈：警示条、转圈、进度是行内件；结果页需要成片空间；弹层类不渲染静态缩略
  alert: 'inline', spin: 'inline', progress: 'inline', trigger: 'inline',
  result: 'panel',
  modal: 'overlay', drawer: 'overlay', popover: 'overlay', popconfirm: 'overlay',
  notification: 'overlay', toast: 'overlay', confirm: 'overlay',

  // 图表：坐标图、刻度环、关系图半行即可；热力矩阵与泳道需要整行才看得出结构
  axis: 'panel', ring: 'panel', graph: 'panel',
  heat: 'stage', swimlane: 'stage',

  // 业务组件：列表页、矩阵、图谱、阶梯都是整屏版式
  crud: 'stage', permission: 'stage', menustar: 'stage',
  org: 'stage', post: 'stage', assistant: 'stage',
  dict: 'panel', dept: 'inline', user: 'inline',

  // 工作台版式与外壳：都是整页级版式
  bento: 'stage', band: 'stage', readout: 'stage',
  share: 'stage', activity: 'stage', shortcut: 'stage',
  frame: 'stage', sidebar: 'stage', topbar: 'stage', system: 'stage', neural: 'stage',
}

/** 组件名 → 规格，由子分组归属派生，不手抄第二份。 */
const SPEC_BY_NAME: Record<string, DemoSpec> = (() => {
  const map: Record<string, DemoSpec> = {}
  for (const sub of COMPONENT_SUB_GROUPS) {
    const spec = SPEC_BY_SUB_GROUP[sub.key] ?? 'inline'
    for (const name of sub.components) map[name] = spec
  }
  return map
})()

/**
 * 取组件的展示规格。
 *
 * [参数] name 组件名 [返回] 该组件的展示规格，未登记时按 inline
 */
export function specOf(name: string): DemoSpec {
  return SPEC_BY_NAME[name] ?? 'inline'
}

/** 规格的中文名，用于分组标题与无障碍说明 */
export const SPEC_LABEL: Record<DemoSpec, string> = {
  inline: '行内件',
  panel: '面板件',
  stage: '舞台件',
  overlay: '弹层件',
}
