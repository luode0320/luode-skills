/* 按组件名取插槽样本：插槽驱动组件没有内容时页面只能显示空白卡片，无法核对视觉。
   属于组件库示例页（后台路由 /gallery）的展示样本，不参与组件库生产运行；
   数据形状严格对齐组件真实类型定义。
   最近修改时间：2026-10-17 04:25:00；改动原因：Form 插槽改为读本格 model 样本，
   使「已填全可提交」与「只填姓名」两格渲染出真实不同的输入值。
*/
import { h, type VNodeChild } from 'vue'
import Button from '../../components/ui/Button.vue'
import Avatar from '../../components/ui/Avatar.vue'
import DeltaPill from '../../components/ui/DeltaPill.vue'
import Field from '../../components/ui/Field.vue'
import TextInput from '../../components/ui/TextInput.vue'
import BentoCard from '../../components/workspace/BentoCard.vue'
import Card from '../../components/extend/Card.vue'
import CollapseItem from '../../components/extend/CollapseItem.vue'
import GridCol from '../../components/extend/GridCol.vue'
import Radio from '../../components/extend/Radio.vue'
import TabPane from '../../components/extend/TabPane.vue'
import { phone, required } from '../../utils/validate'

/** 按组件名取 demo 插槽；插槽驱动组件没有内容时核对页只能显示空白卡片，无法核对视觉。 */
export function demoSlots(name: string): Record<string, (props?: Record<string, unknown>) => VNodeChild> {
  switch (name) {
    case 'Button': return { default: () => '保存' }
    case 'Tag': return { default: () => '启用' }
    case 'Field': return { default: () => h(TextInput, { modelValue: '罗德', placeholder: '请输入负责人' }) }
    /* 作用域插槽样本：从插槽参数取 errors 与 submit，演示「点提交→必填未过→错误态落在字段下方」。
       输入框取值必须读本格的 model 样本，否则「已填全」与「只填姓名」两格渲染成一样的空框。 */
    case 'Form': return {
      default: (p?: Record<string, unknown>) => {
        const errors = (p?.errors ?? {}) as Record<string, string | undefined>
        const model = ((p?.state as Record<string, unknown> | undefined)?.model ?? {}) as Record<string, string | undefined>
        return [
          h(Field, { label: '姓名', required: true, error: errors.name }, () => h(TextInput, { modelValue: model.name ?? '', placeholder: '请输入姓名', invalid: !!errors.name })),
          h(Field, { label: '手机号', error: errors.phone, hint: '用于接收通知' }, () => h(TextInput, { modelValue: model.phone ?? '', placeholder: '请输入手机号', invalid: !!errors.phone })),
          h(Field, { span: true }, () => h(Button, { variant: 'primary', onClick: () => (p?.submit as (() => void) | undefined)?.() }, () => '提交校验')),
        ]
      },
    }
    case 'Panel': return {
      default: () => h('p', {}, '面板内容：承载一组相关读数与操作。'),
      tools: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '更多'),
    }
    case 'Metric': return { default: () => h(DeltaPill, { value: 8.6, label: '环比' }) }
    case 'PageHeader': return { default: () => h(Button, { variant: 'primary' }, () => '新增用户') }
    case 'Checkbox': case 'Switch': return {}
    case 'EmptyState': return {}
    case 'HoverCard': return {
      default: () => h('span', {}, '悬停查看'),
      card: () => h('div', {}, [h('strong', {}, '罗德'), h('p', {}, '总部 · 超级管理员')]),
    }
    case 'Band': return {
      default: () => h('p', {}, '横带内容区：放读数条、图表或列表。'),
      tools: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '导出'),
    }
    case 'BentoGrid': return {
      default: () => [
        h(BentoCard, { span: 'third', title: '卡片一', meta: '3 项' }),
        h(BentoCard, { span: 'third', title: '卡片二', meta: '5 项' }),
      ],
    }
    case 'BentoCard': return { default: () => h('p', {}, '工作台卡片内容') }
    case 'Modal': return { default: () => h('p', {}, '弹窗主体内容。') }
    case 'Drawer': return { default: () => h('p', {}, '抽屉主体内容。') }
    case 'FormDialog': return { default: () => h(Field, { label: '名称', required: true }, () => h(TextInput, { modelValue: '', placeholder: '请输入名称' })) }
    /* ── Arco 品类对齐层（extend）：插槽驱动组件必须有内容，否则卡片空白 ── */
    case 'Badge': return { default: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '消息') }
    case 'Tooltip': return { default: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '悬停查看') }
    case 'Popconfirm': return { default: () => h(Button, { variant: 'danger', size: 'sm' }, () => '删除') }
    case 'Popover': return {
      default: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '点我浮出'),
      content: () => h('p', {}, '气泡卡片内可以放任意可交互内容。'),
    }
    case 'Trigger': return {
      default: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '触发器'),
      content: () => h('p', {}, '弹出的内容'),
    }
    case 'Affix': return { default: () => h('p', {}, '固钉内容') }
    case 'BackTop': return {}
    case 'Dropdown': return { default: () => h(Button, { variant: 'secondary', size: 'sm' }, () => '更多操作') }
    case 'DropdownButton': return { default: () => '新建' }
    case 'Menu': return {}
    /* Tabs 的内容区由调用方数据驱动：面板 active 必须跟当前选中键比出来，
       写死某个面板为 active 会让「点标签不换面板」，示例就成了摆设。
       选中键由页面把该格受控状态透传进来（slotScope 的 state）。 */
    case 'Tabs': return {
      default: (p?: Record<string, unknown>) => {
        const cur = (p?.state as Record<string, unknown> | undefined)?.modelValue
        return [
          h(TabPane, { name: 'tab1', active: cur === 'tab1', label: '概览' }, () => h('p', {}, '概览面板内容。')),
          h(TabPane, { name: 'tab2', active: cur === 'tab2', label: '明细' }, () => h('p', {}, '列表面板内容。')),
        ]
      },
    }
    case 'TabPane': return { default: () => h('p', {}, '标签面板内容。') }
    case 'Collapse': return {
      default: () => [
        h(CollapseItem, { name: 'a', title: '折叠面板一' }, () => h('p', {}, '面板一的内容。')),
        h(CollapseItem, { name: 'b', title: '折叠面板二' }, () => h('p', {}, '面板二的内容。')),
      ],
    }
    case 'CollapseItem': return { default: () => h('p', {}, '折叠面板内容。') }
    case 'Carousel': return {
      default: () => [
        h('div', { style: 'padding:20px' }, '第一屏'),
        h('div', { style: 'padding:20px' }, '第二屏'),
      ],
    }
    case 'Comment': return { default: () => h('p', {}, '补充说明：这条记录已复核。') }
    case 'LinkText': return { default: () => '查看详情' }
    case 'DataList': return { item: () => h('span', {}, '列表项') }
    case 'Skeleton': return { default: () => h('p', {}, '骨架屏加载完成后的真实内容') }
    case 'Timeline': return {}
    case 'TimelineItem': return { default: () => h('p', {}, '节点内容') }
    case 'Typography': return { default: () => '排版内容示例' }
    case 'Watermark': return { default: () => h('div', { style: 'padding:18px;min-height:80px' }, '被水印覆盖的内容区') }
    case 'Divider': return { default: () => '分割文字' }
    case 'GridRow': return {
      default: () => [
        h(GridCol, { span: 12 }, () => h('div', { style: 'padding:8px;background:var(--blue-soft)' }, '半宽列')),
        h(GridCol, { span: 12 }, () => h('div', { style: 'padding:8px;background:var(--lime-soft)' }, '半宽列')),
      ],
    }
    case 'GridCol': return { default: () => h('div', {}, '栅格列内容') }
    /* 不覆盖 resize 插槽，否则会把组件自带的拖拽把手顶成空白，核对页就失去了可拖拽的入口 */
    case 'ResizeBox': return { default: () => h('div', { style: 'padding:12px' }, '可拖拽改尺寸') }
    case 'StyledScrollbar': return {
      default: () => h('div', { style: 'height:220px;padding:0 10px' }, Array.from({ length: 14 }, (_, i) => h('p', {}, `第 ${i + 1} 行内容`))),
    }
    case 'Space': return {
      default: () => [
        h(Button, { variant: 'ghost', size: 'sm' }, () => '一'),
        h(Button, { variant: 'ghost', size: 'sm' }, () => '二'),
        h(Button, { variant: 'ghost', size: 'sm' }, () => '三'),
      ],
    }
    case 'SplitPane': return {
      left: () => h('div', { style: 'padding:12px' }, '左栏'),
      right: () => h('div', { style: 'padding:12px' }, '右栏'),
    }
    case 'RadioGroup': return {
      default: () => [
        h(Radio, { value: 'a', label: '选项 A' }),
        h(Radio, { value: 'b', label: '选项 B' }),
      ],
    }
    /* ── 输入与组合容器、卡片族：插槽驱动组件必须有内容，否则卡片空白 ── */
    case 'InputGroup': return {
      default: () => [
        h(TextInput, { modelValue: '总部', placeholder: '部门' }),
        h(Button, { variant: 'ghost', size: 'sm' }, () => '搜索'),
      ],
    }
    case 'ButtonGroup': return {
      default: () => [
        h(Button, { variant: 'ghost', size: 'sm' }, () => '左'),
        h(Button, { variant: 'ghost', size: 'sm' }, () => '中'),
        h(Button, { variant: 'ghost', size: 'sm' }, () => '右'),
      ],
    }
    case 'AvatarGroup': return {
      default: () => [
        h(Avatar, { name: '罗德', size: 32 }),
        h(Avatar, { name: '林可', size: 32 }),
        h(Avatar, { name: '陈默', size: 32 }),
        h(Avatar, { name: '王川', size: 32 }),
        h(Avatar, { name: '赵宁', size: 32 }),
      ],
    }
    case 'Card': return {
      default: () => h('p', {}, '卡片主体内容：承载一组相关信息与操作。'),
      extra: () => h(Button, { variant: 'ghost', size: 'sm' }, () => '更多'),
      footer: () => h(Button, { variant: 'primary', size: 'sm' }, () => '确定'),
    }
    case 'CardMeta': return {}
    case 'CardGrid': return {
      default: () => [
        h(Card, { title: '卡片一' }, () => h('p', {}, '第一张卡片')),
        h(Card, { title: '卡片二' }, () => h('p', {}, '第二张卡片')),
      ],
    }
    case 'CheckboxGroup': return {}
    case 'Transfer': return {}
    case 'Upload': return { default: () => h('span', {}, '点击或拖拽文件到此区域') }
    case 'Result': return { default: () => h('p', {}, '审批单号：AP-20261015-001') }
    default: return {}
  }
}
