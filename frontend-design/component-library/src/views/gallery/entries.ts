/**
 * 组件库示例页的发现与多变体装配层：从磁盘枚举全部组件，把「基础示例 + 机械派生变体 + 策展变体」
 * 展开成每组件多格可用示例。
 *
 * [用途] 页面只消费这里的结论，不维护第二份组件清单——齐全性以文件系统为准。
 * [约束] `import.meta.glob` 必须用静态字面量参数，Vite 才能在构建期展开成真实模块图；
 *   每格示例用 `variantKey`（来源 rel + 序号）寻址，弹层开关与受控回写状态互不串扰；
 *   弹层形态与画布高度也在此收敛，页面侧只按 kind / canvas 分支渲染。
 * 最近修改时间：2026-10-17 02:38:00；改动原因：Goal「一组件多种示例且每组可用」，
 *   单组件单格改为按变体展开，状态键从 rel 升级为 variantKey，画布从布尔升级为高度数值，并按两级子分组补齐分类归属。
 */
import { defineAsyncComponent } from 'vue'
import { COMPONENT_CATEGORY_OF } from '../../data/component-categories'
import { demoProps } from './demo-props'
import { demoSlots } from './demo-slots'
import { DEFAULT_PROPS, GENERATED_VARIANTS } from './demo-variants.generated'
import { CURATED_VARIANTS } from './demo-variants.curated'
import type { DemoFrame, VariantShape } from './demo-variants.types'
import { createLiveProps, type LiveProps } from './use-live-props'

const modules = import.meta.glob('../../components/**/*.vue')

/** 弹层受控形态：open 型走 open，visible 型走 visible，表格型由 Boolean(table) 推导 */
export type OverlayKind = 'open' | 'visible' | 'table'

export interface DemoEntry {
  name: string
  /** 相对 src/components 的路径，用于卡片上展示来源 */
  rel: string
  /** 本格示例的唯一键：rel + 变体序号，弹层开关与回写状态都按它寻址 */
  variantKey: string
  /** 变体标签：直接显示在示例卡上，写明与基础示例的差异点 */
  label: string
  category: string
  comp: ReturnType<typeof defineAsyncComponent>
  props: Record<string, unknown>
  slots: Record<string, (props?: Record<string, unknown>) => unknown>
  overlay: OverlayKind | null
  /** 需要一次交互才出现效果的宿主类组件键 */
  action: string
  /** 示例画布高度：null 按自然高度铺开，数值用于 absolute 铺满的画布与外壳类组件 */
  canvas: number | null
  /** 并排上下文外框：仅依赖邻居撑开的组件使用，缺省按原样单独渲染 */
  frame?: DemoFrame
  /** 本格相对基础示例的 props 覆盖项：提示文案按它说明「这一格在演示什么」 */
  diff: Record<string, unknown>
}

/** 宿主类组件：必须靠一次交互触发，纯挂载看不到效果 */
const ACTION_BY_NAME: Record<string, string> = {
  ToastHost: 'toast',
  ConfirmHost: 'confirm',
}

/** 画布与外壳类组件：靠 absolute 铺满或依赖布局网格，单独挂载会塌成 0 尺寸 */
const CANVAS_NAMES = new Set(['NeuralNet', 'Sidebar', 'Topbar', 'AppShell', 'AskDock', 'RelationGraph'])

/** 画布类组件的默认高度：三列大卡后宽度翻倍，高度必须同步抬高，
    否则外壳/侧栏/关系图会被压成一条扁带，细节全糊在一起 */
const DEFAULT_CANVAS = 240

/**
 * 判定受控弹层形态；非弹层返回 null。
 *
 * [参数] props：该格合并后的样本属性；name：组件名
 * [返回] OverlayKind | null 需要的弹层交互形态，非弹层为 null
 * 最近修改时间：2026-10-16 19:58:00；改动原因：核对示例迁入后台真实路由页。
 */
function overlayKindOf(props: Record<string, unknown>, name: string): OverlayKind | null {
  if (name === 'GeneratorPipeline') return 'table'
  if ('visible' in props) return 'visible'
  if ('open' in props) return 'open'
  return null
}

/**
 * 把单个组件的「基础格 + 派生变体 + 策展变体」展开成多格示例条目。
 *
 * [参数] rel 组件相对路径；name 组件名；loader 懒加载器
 * [返回] DemoEntry[] 该组件的全部示例格，第一格固定为基础示例
 */
function buildEntries(rel: string, name: string, loader: () => Promise<unknown>): DemoEntry[] {
  const baseProps = demoProps(name)
  const baseSlots = demoSlots(name)
  /* 基础示例真实渲染出来的 props：demoProps 没写的键取组件自身默认值，
     只看 demoProps 会把「与默认值相同」的覆盖当成差异，产出重复示例 */
  const effective = { ...(DEFAULT_PROPS[name] ?? {}), ...baseProps }
  const variants: VariantShape[] = [
    ...(GENERATED_VARIANTS[name] ?? []),
    ...(CURATED_VARIANTS[name] ?? []),
  ]
  const comp = defineAsyncComponent(loader as () => Promise<{ default: unknown }>)
  const baseCanvas = CANVAS_NAMES.has(name) ? DEFAULT_CANVAS : null
  const baseAction = ACTION_BY_NAME[name] ?? ''
  const out: DemoEntry[] = [{
    name,
    rel,
    variantKey: `${rel}#0`,
    label: '基础示例',
    category: COMPONENT_CATEGORY_OF[name] ?? 'general',
    comp,
    props: { ...baseProps },
    slots: baseSlots,
    overlay: overlayKindOf(effective, name),
    action: baseAction,
    canvas: baseCanvas,
    diff: {},
  }]
  // 基础格的差异指纹为空差异集；后续每格与基础比，相同即视为重复丢弃
  const seen = new Set<string>([fingerprint(effective, effective, baseSlots, baseCanvas, baseAction)])
  for (const v of variants) {
    // props 增量覆盖；显式 null 也要生效
    const props = { ...effective, ...v.props }
    const slots = { ...baseSlots, ...v.slots }
    const canvas = v.canvas === undefined ? baseCanvas : v.canvas
    const action = v.action ?? baseAction
    const fp = fingerprint(props, effective, slots, canvas, action, v.frame)
    if (seen.has(fp)) continue
    seen.add(fp)
    out.push({
      name,
      rel,
      variantKey: `${rel}#${out.length}`,
      label: v.label,
      category: COMPONENT_CATEGORY_OF[name] ?? 'general',
      comp,
      // 对外只暴露「相对 demoProps 的覆盖结果」，保持与基础格同一比较基准
      props: { ...baseProps, ...v.props },
      slots,
      overlay: overlayKindOf(props, name),
      action,
      canvas,
      frame: v.frame,
      diff: { ...v.props },
    })
  }
  return out
}

/**
 * 算一格示例的差异指纹：props 相对基础有效值的差集 + 插槽身份 + 画布 + 动作。
 *
 * 标签不同但指纹相同 = 渲染结果与基础格一致，属重复示例，装配层直接丢弃。
 *
 * [参数] props 该格有效 props；base 基础格有效 props；slots 合并后插槽；canvas 画布高度；
 *   action 触发动作键；frame 并排上下文外框
 * [返回] string 可比较的指纹
 */
function fingerprint(props: Record<string, unknown>, base: Record<string, unknown>, slots: Record<string, unknown>, canvas: number | null, action: string, frame?: DemoFrame): string {
  const diff = Object.keys(props)
    .filter((k) => identity(props[k]) !== identity(base[k]))
    .sort()
    .map((k) => `${k}:${identity(props[k])}`)
    .join(',')
  const slotSig = Object.keys(slots).sort().map((k) => `${k}:${identity(slots[k])}`).join(',')
  return `${diff}|slots:${slotSig}|canvas:${canvas}|action:${action}|frame:${JSON.stringify(frame ?? null)}`
}

/* 身份表：只为对象与函数发一个稳定编号，同一引用恒等，不同引用必不同。
   数组 / 对象不能按长度或键数比——同样两条数据换一批内容就是不同示例，
   按长度会把它们误判成重复并丢掉一组可用示例。 */
const ids = new WeakMap<object, number>()
let idSeq = 0

/** 取值的可比较身份：标量按值，对象与函数按引用编号。 */
function identity(v: unknown): string {
  if (v === null || v === undefined || typeof v !== 'object' && typeof v !== 'function') return String(v)
  const obj = v as object
  let id = ids.get(obj)
  if (id === undefined) {
    id = ++idSeq
    ids.set(obj, id)
  }
  return `#${id}`
}

/** 磁盘全量组件 → 多变体演示条目（按分类、组件名与变体序号稳定排序，同组件各格相邻） */
export const demoEntries: DemoEntry[] = Object.entries(modules)
  .flatMap(([key, loader]) => {
    const rel = key.replace('../../components/', '')
    const name = rel.split('/').pop()!.replace('.vue', '')
    return buildEntries(rel, name, loader)
  })
  .sort((a, b) => a.category.localeCompare(b.category) || a.name.localeCompare(b.name) || a.variantKey.localeCompare(b.variantKey))

/** 每格示例的可回写状态：受控组件在页面上真能被操作，变体之间互不串扰 */
export const liveOf = new Map<string, LiveProps>(demoEntries.map((e) => [e.variantKey, createLiveProps(e.name, e.props, e.variantKey)]))
