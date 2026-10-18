/* 外壳、宿主与工作台类策展变体：这些组件对外契约窄（宿主类甚至无 props），
   可用差异来自触发动作、画布高度与数据长度，而不是伪造 props。
   AppearanceDialog / CommandPalette / PasswordDialog 属上游冻结文件：公开契约只有 open 一个布尔、
   没有插槽、内容硬编码，除「点按钮展开同一块面板」外不存在第二种可用差异，
   因此不给它们凑伪变体，由守卫按契约特征识别为单维组件并单独留痕。
   最近修改时间：2026-10-17 11:00:00；改动原因：画布档位随三列大卡上调到 320/440/560，
   读数与动态列表补全量数据差异。 */
import { h } from 'vue'
import BentoCard from '../../components/workspace/BentoCard.vue'
import type { VariantShape } from './demo-variants.types'
import { ACTIVITY_ITEMS, READOUT_ITEMS, READOUT_ROWS, SHARE_ITEMS, SHORTCUT_ITEMS } from './demo-display-samples'

/** 外壳、宿主与工作台类组件的策展变体 */
export const CURATED_SHELL: Record<string, VariantShape[]> = {
  ActivityList: [
    { label: '两条活动', props: { items: ACTIVITY_ITEMS.slice(0, 2) } },
    { label: '大头像', props: { avatarSize: 48 } },
    { label: '全部三条', props: { items: ACTIVITY_ITEMS } },
    { label: '小头像', props: { avatarSize: 24 } },
  ],
  AppShell: [
    { label: '画布 320 高', canvas: 320 },
    { label: '画布 440 高', canvas: 440 },
    { label: '画布 560 高', canvas: 560 },
  ],
  BentoGrid: [
    {
      label: '两列窄卡',
      slots: {
        default: () => [
          h(BentoCard, { span: 'half', title: '左半', meta: '2 项' }, () => h('p', {}, '左半内容')),
          h(BentoCard, { span: 'half', title: '右半', meta: '4 项' }, () => h('p', {}, '右半内容')),
        ],
      },
    },
    {
      label: '通栏单卡',
      slots: {
        default: () => [h(BentoCard, { span: 'full', title: '通栏', meta: '9 项' }, () => h('p', {}, '通栏内容'))],
      },
    },
    {
      label: '三分之一三卡',
      slots: {
        default: () => [
          h(BentoCard, { span: 'third', title: '一', meta: '1 项' }, () => h('p', {}, '第一格')),
          h(BentoCard, { span: 'third', title: '二', meta: '2 项' }, () => h('p', {}, '第二格')),
          h(BentoCard, { span: 'third', title: '三', meta: '3 项' }, () => h('p', {}, '第三格')),
        ],
      },
    },
  ],
  Band: [
    { label: '无标题', props: { title: '' } },
    { label: '不做入场动画', props: { reveal: false } },
    { label: '带工具区', props: { title: '最近操作' }, slots: { tools: () => h('span', {}, '刷新') } },
  ],
  ConfirmHost: [
    { label: '危险确认', action: 'confirm-danger' },
    { label: '普通确认', action: 'confirm-plain' },
  ],
  KeyValueReadout: [
    { label: '单行', props: { rows: READOUT_ROWS.slice(0, 1) } },
    { label: '双行', props: { rows: READOUT_ROWS.slice(0, 2) } },
    { label: '三行', props: { rows: READOUT_ROWS } },
  ],
  NeuralNet: [
    { label: '画布 320 高', canvas: 320 },
    { label: '登录成功收束', props: { burstKey: 'gallery-burst' }, canvas: 320 },
    { label: '画布 520 高', canvas: 520 },
  ],
  ReadoutStrip: [
    { label: '两项读数', props: { items: READOUT_ITEMS.slice(0, 2) } },
    { label: '单项读数', props: { items: READOUT_ITEMS.slice(0, 1) } },
    { label: '三项含告警', props: { items: READOUT_ITEMS } },
    { label: '仅告警项', props: { items: READOUT_ITEMS.slice(2) } },
  ],
  ShareList: [
    { label: '百分比单位', props: { unit: '%' } },
    { label: '两条分享', props: { items: SHARE_ITEMS.slice(0, 2) } },
    { label: '全部四项', props: { items: SHARE_ITEMS } },
    { label: '单项分享', props: { items: SHARE_ITEMS.slice(0, 1) } },
  ],
  ShortcutGrid: [
    { label: '两宫格', props: { items: SHORTCUT_ITEMS.slice(0, 2) } },
    { label: '单宫格', props: { items: SHORTCUT_ITEMS.slice(0, 1) } },
    { label: '三宫格', props: { items: SHORTCUT_ITEMS } },
    { label: '换一组入口', props: { items: [SHORTCUT_ITEMS[2], SHORTCUT_ITEMS[0]] } },
  ],
  Sidebar: [
    { label: '画布 320 高', canvas: 320 },
    { label: '画布 440 高', canvas: 440 },
    { label: '画布 560 高', canvas: 560 },
  ],
  ToastHost: [
    { label: '失败提示', action: 'toast-danger' },
    { label: '信息提示', action: 'toast-info' },
    { label: '成功提示', action: 'toast' },
  ],
  Topbar: [
    { label: '画布 320 高', canvas: 320 },
    { label: '画布 440 高', canvas: 440 },
    { label: '画布 560 高', canvas: 560 },
  ],
}
