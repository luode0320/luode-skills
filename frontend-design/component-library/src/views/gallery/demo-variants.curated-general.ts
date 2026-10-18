/* 通用 / 导航 / 布局类策展变体：机械派生覆盖不到的值域、插槽内容差异在此补齐，
   与 base、generated 归并后每个组件 ≥3 组可用示例。
   最近修改时间：2026-10-17 11:00:00；改动原因：补头像/图标/按钮组/规格牌/折叠/标签页/下拉等
   真实可见差异，并新增 Collapse、Tabs、Dropdown、Affix 策展条目。 */
import { h } from 'vue'
import Avatar from '../../components/ui/Avatar.vue'
import Button from '../../components/ui/Button.vue'
import type { VariantShape } from './demo-variants.types'
import { ANCHOR_ITEMS, BREADCRUMB_ITEMS, DROPDOWN_ITEMS, MENU_ITEMS, MENU_NODE_ITEM } from './demo-display-samples'

/** 通用、导航与布局类组件的策展变体 */
export const CURATED_GENERAL: Record<string, VariantShape[]> = {
  Menu: [
    /* 基础示例：竖排、选中「用户管理」。折叠态与切换选中项都是点得动的真实差异 */
    { label: '折叠侧栏', props: { collapsed: true } },
    { label: '选中监控中心', props: { modelValue: MENU_ITEMS[2].key } },
  ],
  SplitPane: [
    /* 基础示例左右各 50%：给初始偏移与可拖拽边界两种真实差异 */
    { label: '左栏 30%', props: { modelValue: 30 } },
    { label: '限定 40~70', props: { min: 40, max: 70, modelValue: 55 } },
  ],
  /* BackTop 会向上找最近的定位祖先停靠：示例卡里落在画布内，不再飘到视口右下角。
     不能改 visibilityHeight（一改就永远不出现），所以按 right / bottom 给出三个不重叠的停靠位 */
  BackTop: [
    { label: '贴右缘停靠', props: { right: 16 } },
    { label: '抬高停靠', props: { right: 16, bottom: 32 } },
    { label: '居中偏下', props: { right: 120, bottom: 16 } },
  ],
  Breadcrumb: [
    { label: '单项', props: { items: BREADCRUMB_ITEMS.slice(0, 1) } },
    { label: '带图标', props: { items: [{ ...BREADCRUMB_ITEMS[0], icon: 'setting' }] } },
    { label: '四项深层', props: { items: [{ label: '首页', to: '/' }, { label: '系统管理', to: '/system' }, { label: '用户管理', to: '/system/users' }, { label: '编辑账号' }] } },
  ],
  MenuNode: [
    { label: '折叠态', props: { collapsed: true } },
    {
      label: '子节点层',
      props: { item: MENU_NODE_ITEM.children?.[0] ?? MENU_NODE_ITEM, depth: 1 },
    },
    { label: '横向浮层', props: { vertical: false, depth: 0 } },
    { label: '选中态', props: { selected: MENU_NODE_ITEM.children?.[0]?.key ?? 'operlog', depth: 1 } },
  ],
  /* 纵向分割线靠并排邻居撑高：单独挂载只剩一条 1em 短线，看不出分隔语义，
     所以用 frame 补左右两块内容与固定行高，让竖线按 stretch 撑满真实高度 */
  Divider: [
    { label: '纵向分隔', props: { direction: 'vertical' }, frame: { before: '订单号', after: '创建时间', height: 72 } },
    { label: '纵向虚线', props: { direction: 'vertical', dashed: true }, frame: { before: '左栏内容', after: '右栏内容', height: 72 } },
    { label: '纵向加大间距', props: { direction: 'vertical', margin: 24 }, frame: { before: '摘要', after: '明细', height: 72 } },
  ],
  /* 不提供 active=false 的示例：未激活面板由 v-show 整体隐藏，单独挂载时只能呈现空白卡，
     看不出组件形态；未激活语义由 Tabs 示例里切换标签来演示，这里只给可见的面板内容差异 */
  TabPane: [
    { label: '内容差异', props: { active: true, label: '明细' }, slots: { default: () => h('p', {}, '明细面板内容。') } },
    { label: '命名面板', props: { name: 'tab3', active: true, label: '日志' }, slots: { default: () => h('p', {}, '带 name 的日志面板。') } },
    {
      label: '多段内容',
      props: { active: true, label: '详情' },
      slots: { default: () => [h('p', {}, '第一段：面板可承载任意块级内容。'), h('p', {}, '第二段：内容区高度随内容自然撑开。')] },
    },
  ],
  Tag: [
    { label: '危险调', props: { tone: 'danger' } },
    { label: '成功调带圆点', props: { tone: 'ok', dot: true } },
    { label: '无圆点中性', props: { tone: 'neutral', dot: false } },
  ],
  StatusTag: [
    { label: '停用态', props: { status: 0 } },
    { label: '自定义文案', props: { status: 1, on: '在线', off: '离线' } },
    { label: '布尔真值', props: { status: true, on: '启用中', off: '已停用' } },
  ],
  /* Avatar 只有 name / size 两项：机械派生已给两档尺寸，再补名字长度差异
     （中文取后两字、英文取首字母，两种命名规则的呈现完全不同） */
  Avatar: [
    { label: '英文名首字母', props: { name: 'Arthur' } },
    { label: '长中文名', props: { name: '欧阳长风' } },
    { label: '空名占位', props: { name: '' } },
  ],
  Icon: [
    { label: '细描边', props: { stroke: 1.2 } },
    { label: '粗描边', props: { stroke: 2.4 } },
    { label: '另一图标', props: { name: 'shield' } },
  ],
  ButtonGroup: [
    {
      label: '三个按钮',
      props: { size: 'md' },
      slots: { default: () => [h(Button, { variant: 'secondary', size: 'sm' }, () => '新增'), h(Button, { variant: 'secondary', size: 'sm' }, () => '编辑'), h(Button, { variant: 'secondary', size: 'sm' }, () => '删除')] },
    },
    {
      label: '小号纵向',
      props: { size: 'sm', direction: 'vertical' },
      slots: { default: () => [h(Button, { variant: 'secondary', size: 'sm' }, () => '上移'), h(Button, { variant: 'secondary', size: 'sm' }, () => '下移')] },
    },
  ],
  DeltaPill: [
    { label: '负值下跌', props: { value: -3.2 } },
    { label: '零值', props: { value: 0 } },
    { label: '新增中性态', props: { value: 8, fresh: true } },
    { label: '强制上升箭头', props: { value: -2, up: true } },
  ],
  Odometer: [
    { label: '两位小数', props: { decimals: 2, value: 1284.56 } },
    { label: '不分组', props: { group: false, value: 1284567 } },
    { label: '整数读数', props: { decimals: 0, value: 86 } },
  ],
  SpecPlate: [
    { label: '无标题两行', props: { title: '', rows: [{ label: '总数', value: 86 }, { label: '异常', value: 2, tone: 'red' }] } },
    { label: '空值占位', props: { title: '巡检结果', rows: [{ label: '最近巡检', value: null }, { label: '通过率', value: '99.2%', tone: 'lime' }] } },
    { label: '四行读数', props: { title: '容量规格', rows: [{ label: '节点', value: 12 }, { label: '内存', value: '64 GB' }, { label: '磁盘', value: '2 TB' }, { label: '带宽', value: '10 Gbps' }] } },
  ],
  PageHeader: [
    { label: '无描述', props: { desc: '' } },
    { label: '长标题', props: { title: '权限矩阵与角色绑定维护中心', desc: '勾选即生效，保存前会做一次冲突校验' } },
    { label: '极简标题', props: { title: '概览', desc: '' } },
  ],
  Panel: [
    { label: '带元信息', props: { meta: '共 3 项' } },
    { label: '内容差异', slots: { default: () => h('p', {}, '面板内容变体：换一组正文核对排版。') } },
    { label: '无标题', props: { title: '' }, slots: { default: () => h('p', {}, '只有内容区的面板。') } },
  ],
  Ruler: [
    { label: '无游标', props: { marker: null, markerLabel: '' } },
    { label: '细刻度', props: { minor: 2, marker: 0.28, markerLabel: '06:43' } },
    { label: '四段刻度', props: { labels: ['0', '25', '50', '75', '100'], marker: 0.75, markerLabel: '75' } },
  ],
  EmptyState: [
    { label: '仅标题', props: { desc: '', icon: '' } },
    { label: '搜索无果', props: { title: '没有找到匹配项', desc: '换个关键词试试', icon: 'search' } },
    { label: '权限不足', props: { title: '暂无查看权限', desc: '请联系管理员开通该模块', icon: 'lock' } },
  ],
  AvatarGroup: [
    {
      label: '只 2 人不折叠',
      props: { max: 5, total: 2 },
      slots: { default: () => [h(Avatar, { name: '罗德', size: 32 }), h(Avatar, { name: '林可', size: 32 })] },
    },
  ],
  /* Anchor 的 offsetTop 只作用于点击滚动补偿与观察 rootMargin，静态渲染看不出差异，
     因此示例差异做在目录项本身：单项与带二级缩进的真实层级差。 */
  /* SectionLabel 只有 title 与 as 两个契约项，as 默认就是 h2（派生只留 as=h3），
     第三条差异给标题文案长度——这是卡片上直接可见的排布差别 */
  SectionLabel: [
    { label: '长标题', props: { title: '权限矩阵与角色授予情况总览（近 7 天）' } },
    { label: '极短标题', props: { title: '概览' } },
  ],
  Collapse: [
    { label: '手风琴', props: { accordion: true } },
    { label: '无描边', props: { bordered: false } },
    { label: '两项展开', props: { modelValue: ['a', 'b'] } },
  ],
  Tabs: [
    { label: '卡片型', props: { type: 'card' } },
    { label: '可关闭', props: { closable: true } },
    { label: '选中明细页', props: { modelValue: 'tab2' } },
  ],
  Dropdown: [
    { label: '悬停触发', props: { trigger: 'hover' } },
    { label: '向上弹出', props: { placement: 'top' } },
    { label: '单项菜单', props: { items: DROPDOWN_ITEMS.slice(0, 1) } },
  ],
  Affix: [
    { label: '距顶 24', props: { offsetTop: 24 } },
    { label: '距顶 80', props: { offsetTop: 80 } },
    { label: '底部吸附', props: { offsetBottom: 40 } },
  ],
  Anchor: [
    { label: '仅单项', props: { items: ANCHOR_ITEMS.slice(0, 1) } },
    { label: '全二级缩进', props: { items: ANCHOR_ITEMS.map((i) => ({ ...i, depth: 1 })) } },
    { label: '无二级项', props: { items: ANCHOR_ITEMS.filter((i) => !i.depth) } },
  ],
  DropdownSubmenu: [
    { label: '禁用', props: { disabled: true } },
    { label: '单项列表', props: { items: DROPDOWN_ITEMS.slice(0, 1) } },
    { label: '两项列表', props: { items: DROPDOWN_ITEMS.slice(0, 2) } },
  ],
  /* 滚动条组件的滑块由挂载后实测的溢出几何决定：基础槽内容只有纵向溢出，
     direction=both 单独改属性不会多出横滑块，必须同时把内容改成横向也溢出才算真实差异。 */
  StyledScrollbar: [
    {
      label: '横向滚动',
      props: { direction: 'horizontal', maxWidth: 240, maxHeight: 120 },
      slots: { default: () => h('div', { style: 'width:420px;height:96px' }, '横向长内容：需要左右拖动才能看完。') },
    },
    {
      label: '横竖双滑块',
      props: { direction: 'both', maxWidth: 240, maxHeight: 120 },
      slots: {
        default: () => h('div', { style: 'width:420px;height:240px' }, '两轴都溢出的长内容，横竖滑块同时工作。'),
      },
    },
  ],
}
