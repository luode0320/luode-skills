/* 控件档位：`size` 只表示档位，不表示像素。
   同一档位的高度、内距、字号、图标边长四个维度都来自 `src/styles/overrides.css` 的
   `--control-*` / `--fs-control-*` / `--icon-control-*` 令牌族，本文件不写任何像素数字——
   一旦在 TS 里再抄一份数字，就多了一处必须与 CSS 同步的真相，档位越加越容易漂。

   用法是让组件把档位翻译成四个局部变量，scoped 样式统一读它们，
   于是同一段 CSS 天然支持四档，不需要为每一档重复写四条规则：

     <button :style="controlVars(size)">…</button>

     .x-btn { height: var(--ctl-h); padding-inline: var(--ctl-px); font-size: var(--ctl-fs); }

   兜底档位取 md：它在上游别名到 `--control-h`（36px），既有页面不会因为引入本文件而位移。 */

/** 控件档位。只用于控件尺寸，几何量与数据量各用独立 prop 名，见 LOCAL-GUIDE.md。 */
export type ControlSize = 'xs' | 'sm' | 'md' | 'lg'

/** 档位全集，按由小到大排列，供遍历与校验使用。 */
export const CONTROL_SIZES: readonly ControlSize[] = ['xs', 'sm', 'md', 'lg'] as const

/** 缺省档位：与上游 `--control-h` 同值，保证引入后不产生视觉位移。 */
export const DEFAULT_CONTROL_SIZE: ControlSize = 'md'

/**
 * 判断任意入参是否为合法档位。
 * @param value 待判定值，通常来自组件 props 的宽松入参
 * @returns 是则返回 true 并收窄类型
 */
export function isControlSize(value: unknown): value is ControlSize {
  return typeof value === 'string' && (CONTROL_SIZES as readonly string[]).includes(value)
}

/**
 * 把外部传入的档位收敛为合法值。
 * 组件 props 可能收到 `undefined`、拼写错误或上游语义下的其它字符串，
 * 一律回落到缺省档位，避免把 `var(--control-h-undefined)` 这类空引用写进样式。
 * @param value 宽松入参
 * @returns 合法档位
 */
export function normalizeControlSize(value: unknown): ControlSize {
  return isControlSize(value) ? value : DEFAULT_CONTROL_SIZE
}

/**
 * 生成四个局部 CSS 变量，供组件 scoped 样式消费。
 * 返回的是 `var()` 引用而不是计算后的像素，因此主题、密度与令牌调整都会自动跟随。
 * @param size 档位，非法值自动回落为 md
 * @returns 可直接绑到 `:style` 的对象
 */
export function controlVars(size: unknown): Record<string, string> {
  const tier = normalizeControlSize(size)
  return {
    '--ctl-h': `var(--control-h-${tier})`,
    '--ctl-px': `var(--control-px-${tier})`,
    '--ctl-fs': `var(--fs-control-${tier})`,
    '--ctl-icon': `var(--icon-control-${tier})`,
  }
}

/**
 * 生成 `data-size` 属性，供必须以属性选择器区分档位的场景使用。
 * 多数组件用 `controlVars` 更简洁；仅在需要让子元素跨组件继承档位时才用属性方案。
 * @param size 档位，非法值自动回落为 md
 * @returns 属性对象，如 `{ 'data-size': 'sm' }`
 */
export function controlSizeAttr(size: unknown): Record<string, string> {
  return { 'data-size': normalizeControlSize(size) }
}
