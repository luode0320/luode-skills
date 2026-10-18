/* 组件示例变体的共享类型：一组在基础示例之上的「增量覆盖」。
   props 覆盖基础样本的同名键，slots 覆盖同名插槽；两者可只给其一。
   生成物（demo-variants.generated）与策展条目（demo-variants.curated.*）都归一到这个形状，
   所以类型名不叫 Curated 也不叫 Generated，避免装配层混用时语义误导。 */
import type { VNodeChild } from 'vue'

/** 示例外框：给依赖邻居上下文的组件（如纵向分割线）补并排布局与两侧文字 */
export interface DemoFrame {
  /** 组件左侧的上下文文字 */
  before?: string
  /** 组件右侧的上下文文字 */
  after?: string
  /** 并排行高（像素）：纵向分割线靠 stretch 撑满，没有高度就只剩一行字高 */
  height?: number
}

/** 一组示例变体的覆盖声明 */
export interface VariantShape {
  /** 变体标签：直接显示在示例卡上，说明与基础示例的差异点 */
  label: string
  /** 覆盖基础示例的 props 片段 */
  props?: Record<string, unknown>
  /** 覆盖基础示例的插槽渲染函数 */
  slots?: Record<string, (props?: Record<string, unknown>) => VNodeChild>
  /** 覆盖宿主类组件的触发动作键（toast / confirm），让无 props 的宿主也能给出可用差异 */
  action?: string
  /** 覆盖示例画布高度（像素）：null 表示不套定高容器、按自然高度铺开 */
  canvas?: number | null
  /** 并排上下文外框：依赖邻居撑开的组件（纵向分割线）用它补真实用法 */
  frame?: DemoFrame
  /** 派生来源标记：机械派生写 enum / boolean / number，策展条目不填 */
  source?: string
}
