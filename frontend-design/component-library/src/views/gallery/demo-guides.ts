/* 示例说明：把「组件是什么」与「这一格示例在演示什么」拼成一条可直接悬停阅读的提示。
   组件说明来自 component-guides 的唯一数据源；示例差异由本文件按变体标签与 props 推导，
   不要求调用方逐格手写，避免 752 格示例各写一句造成的重复与漂移。
   最近修改时间：2026-10-18 04:20:00；改动原因：用户要求每格示例的提示对应当前这一格。 */
import { COMPONENT_GUIDES } from '../../data/component-guides'

/** 基础示例的固定说明：没有任何覆盖，展示组件默认形态 */
const BASE_TEXT = '默认形态，未覆盖任何属性'

/** 提示正文里单个属性值的最长展示长度：超长文案（如说明正文）截断，避免浮层被撑爆 */
const VALUE_LIMIT = 18

/** props 值的中文呈现：未定义与空值直译，布尔转开关，长文本截断，数组与对象给出可读摘要 */
function showValue(value: unknown): string {
  if (value === undefined) return '未设置'
  if (value === null) return '空'
  if (typeof value === 'boolean') return value ? '开启' : '关闭'
  if (typeof value === 'string') {
    if (value === '') return '空字符串'
    return value.length > VALUE_LIMIT ? `${value.slice(0, VALUE_LIMIT)}…` : value
  }
  if (typeof value === 'number') return String(value)
  if (Array.isArray(value)) return `共 ${value.length} 项`
  if (typeof value === 'object') return '对象'
  return String(value)
}

/** 提示正文里最多列出的属性个数：超出部分只报总数，避免长串属性把浮层撑成一面墙 */
const PROP_LIMIT = 3

/**
 * 把一组 props 覆盖描述成一句中文差异说明。
 *
 * [参数] props 该格相对基础示例的覆盖项
 * [返回] string 形如「size=sm、disabled=开启」的说明；无覆盖时为空串
 */
function describeProps(props: Record<string, unknown>): string {
  const entries = Object.entries(props)
  if (!entries.length) return ''
  const shown = entries.slice(0, PROP_LIMIT).map(([k, v]) => `${k}=${showValue(v)}`).join('、')
  const rest = entries.length - PROP_LIMIT
  return rest > 0 ? `${shown} 等 ${entries.length} 项` : shown
}

/**
 * 生成某一格示例的完整提示正文。
 *
 * [参数] name 组件名；variant 变体标签（基础示例传「基础示例」）；props 该格覆盖项
 * [返回] string 组件说明 + 本格差异；组件无说明时退回只讲差异
 */
export function demoGuideOf(name: string, variant: string, props: Record<string, unknown>): string {
  const head = COMPONENT_GUIDES[name] ?? ''
  const diff = variant === '基础示例' ? BASE_TEXT : describeProps(props)
  const tail = diff ? `本格示例：${diff}` : `本格示例：${variant}`
  return head ? `${head}。${tail}` : tail
}
