/* 数据展示与图表类策展变体：机械派生覆盖不到的值域、数据长度、插槽内容差异在此补齐。
   与 base、generated 归并后每个组件 ≥3 组可用示例。
   最近修改时间：2026-10-17 11:00:00；改动原因：补日历年度模式、卡片悬浮态、评论空态、
   时间线方形节点、水印双行等真实差异，并新增 Spin / Modal / Drawer 策展条目。 */
import { h } from 'vue'
import type { VariantShape } from './demo-variants.types'
import { IMAGE_SRC, OVERFLOW_ITEMS, PREVIEW_IMAGES, TIMELINE_ITEMS, TREE_DATA } from './demo-display-samples'
import { HEAT_CELLS } from './demo-business-samples'

/** 展示与图表类组件的策展变体（工作台版式类归 shell，见 demo-variants.curated-shell） */
export const CURATED_DISPLAY: Record<string, VariantShape[]> = {
  Calendar: [
    { label: '二月视图', props: { modelValue: '2026-02-14' } },
    { label: '年末视图', props: { modelValue: '2026-12-31' } },
    { label: '年度模式', props: { mode: 'year', modelValue: '2026-06-15' } },
  ],
  Card: [
    { label: '无描边', props: { bordered: false } },
    { label: '封面图', props: { subtitle: '' }, slots: { cover: () => h('img', { src: IMAGE_SRC, alt: '封面', style: 'width:100%;display:block' }) } },
    { label: '不可悬浮', props: { hoverable: false } },
  ],
  CardMeta: [
    { label: '无头像', props: { avatar: '' } },
    { label: '无描述', props: { description: '' } },
    { label: '长描述换行', props: { description: '总部 · 超级管理员 · 最近一次登录 2026-10-15 09:20' } },
  ],
  Comment: [
    { label: '无操作项', props: { actions: [] } },
    /* avatar 收的是图片地址（Comment 内部渲染 <img :src>），文字首字母头像是 avatar 为空时
       由内部 Avatar 按 author 派生的另一条分支；这里曾误填「罗」，<img src="罗"> 被解析成
       相对路径请求当前路由下的 /罗 而 404，示例卡里只剩一个破图占位。 */
    { label: '带头像', props: { avatar: IMAGE_SRC }, slots: { default: () => h('p', {}, '评论正文变体。') } },
    { label: '无头像无操作', props: { avatar: '', actions: [], content: '只保留作者与正文的极简评论。' } },
  ],
  Descriptions: [
    /* 基础示例：1 列、带描边、横排。这里给「三列无边框」与「两列竖排」，
       与派生的 layout=vertical 各自的差异键组合都不同，不会被判为重复 */
    { label: '三列无边框', props: { column: 3, bordered: false } },
    { label: '两列竖排', props: { layout: 'vertical', column: 2 } },
    { label: '两列横排', props: { column: 2 } },
  ],
  Countdown: [
    /* autostart 单独覆盖会把倒数停在与基础示例同一秒上，两格读数一模一样，
       归零态要连 remaining 一起给才看得出差别 */
    { label: '归零定格', props: { autostart: false, remaining: 0 } },
    { label: '分秒格式', props: { remaining: 95, format: 'mm:ss' } },
    { label: '纯秒数', props: { remaining: 300, format: 'ss' } },
  ],
  HeatGrid: [
    { label: '加载态', props: { loading: true } },
    { label: '空数据', props: { cells: [] } },
    { label: '单格数据', props: { cells: HEAT_CELLS.slice(0, 1) } },
  ],
  ImagePreview: [
    /* 预览浮层是受控的：一律由「预览弹层」按钮打开，差异做在打开后的真实内容上，
       不能靠 visible:true 自动展开——同分类页多格同时展开会把整页盖住 */
    { label: '示例图二', props: { src: PREVIEW_IMAGES[1].src, title: PREVIEW_IMAGES[1].alt } },
    { label: '禁用缩放', props: { zoomable: false } },
    { label: '无标题', props: { title: '' } },
  ],
  ImagePreviewGroup: [
    { label: '第二张起', props: { initialIndex: 1 } },
    { label: '第三张起', props: { initialIndex: 2 } },
    { label: '两张图组', props: { images: PREVIEW_IMAGES.slice(0, 2) } },
  ],
  Swimlane: [
    { label: '紧凑', props: { compact: true } },
    { label: '限两道', props: { maxLanes: 2 } },
    { label: '限一道', props: { maxLanes: 1 } },
  ],
  /* 反馈类：Spin 的 wrapper 会把内容包进遮罩层，与裸转圈是两种形态；
     Modal / Drawer 的宽度档位由派生器按弹层专属档给出，这里补遮罩关闭与标题差异 */
  Spin: [
    { label: '大号带文案', props: { size: 'lg', tip: '正在加载明细' } },
    { label: '包裹遮罩', props: { wrapper: true, tip: '提交中' }, slots: { default: () => h('p', {}, '被遮罩的内容') } },
  ],
  Modal: [
    { label: '超窄弹窗', props: { width: 360 } },
    { label: '超宽弹窗', props: { width: 880 } },
    { label: '点遮罩关闭', props: { closeOnOverlay: true } },
  ],
  Drawer: [
    { label: '超窄抽屉', props: { width: 320 } },
    { label: '超宽抽屉', props: { width: 820 } },
    { label: '带副标题', props: { sub: '右侧滑出，可放长表单' } },
  ],
  Timeline: [
    { label: '单项', props: { items: TIMELINE_ITEMS.slice(0, 1) } },
    { label: '彩色节点', props: { items: [{ ...TIMELINE_ITEMS[0], color: 'var(--red)' }] } },
  ],
  TimelineItem: [
    { label: '红点', props: { color: 'var(--red)' } },
    { label: '内容差异', props: { content: '节点内容变体', time: '23:59' }, slots: { default: () => h('p', {}, '自定义节点正文。') } },
    { label: '方形节点', props: { dot: 'square', content: '发布 v1.1' } },
  ],
  TreeNode: [
    { label: '叶子层', props: { node: TREE_DATA[0].children?.[0] ?? TREE_DATA[0], depth: 1 } },
    { label: '根层无父', props: { node: TREE_DATA[1], parentKey: null, depth: 0 } },
    { label: '三级缩进', props: { node: TREE_DATA[0].children?.[1]?.children?.[0] ?? TREE_DATA[0], depth: 2, parentKey: 12 } },
  ],
  OverflowList: [
    { label: '全部展开', props: { maxCount: 99 } },
    { label: '单项', props: { items: OVERFLOW_ITEMS.slice(0, 1) } },
  ],
  RelationGraph: [
    /* 舞台版（stage）设计给大画布：配到 320 才看得清珍珠球与刻度表盘，
       小画布下节点会被压到 28×18；light 版另给两档画布高度 */
    { label: '舞台视图', props: { variant: 'stage' }, canvas: 320 },
    { label: '画布 400 高', canvas: 400 },
  ],
  Watermark: [
    { label: '图片水印', props: { image: IMAGE_SRC } },
    { label: '旋转 -20°', props: { rotate: -20 } },
    { label: '双行文字', props: { content: ['内部资料', '禁止外传'], font: { fontSize: 13 } } },
  ],
  HelpTip: [
    /* 无标题只有一句说明，长文本用来验证 260px 上限内的换行与贴边夹取 */
    { label: '纯文字说明', props: { title: undefined, content: '导出范围跟随当前筛选条件，未勾选行时导出全部结果。' } },
    { label: '长文换行', props: { content: '该字段用于对接外部账务系统，填错会导致对账失败；如不确定请联系财务管理员确认后再保存。' } },
    { label: '自定义读屏名', props: { label: '查看审批时限说明' } },
  ],
}
