#!/usr/bin/env node
/**
 * 生成组件示例变体：从组件公开契约（references/component-catalog.json）机械派生
 * 每个组件的多组示例 props，写入组件库示例页的生成物文件。
 *
 * [用法]
 *   node scripts/build_demo_variants.mjs           # 生成变体
 *   node scripts/build_demo_variants.mjs --report  # 只打印覆盖面，不写文件
 * [返回] 退出码 0=生成成功或报告完成；1=索引缺失或写入失败。
 * 最近修改时间：2026-10-17 04:25:00；改动原因：不可见候选黑名单补入
 * StyledScrollbar direction=both 与 Rate allowClear，剔除无可见差异的派生格。
 */
// exemption: 单文件构建脚本，派生规则表与写出模板强耦合，拆分会把一张表切成两处维护

import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const SKILL = path.resolve(HERE, '..')
const LIB = path.join(SKILL, 'component-library')
const CATALOG = path.join(SKILL, 'references', 'component-catalog.json')
const OUT_TS = path.join(LIB, 'src', 'views', 'gallery', 'demo-variants.generated.ts')

/* 这些布尔开关只改变外观或能力，打开后示例仍能正常渲染，可安全机械派生；
   open / visible 一类会改变挂载形态的开关不在此列，交由策展条目处理。
   除「打开」方向外，凡基础示例默认已打开、关掉后仍有可见差异的开关（bordered /
   closable / hoverable / selectable 等）也派生反向值，见 SAFE_FALSE_BOOLEANS。 */
const SAFE_BOOLEANS = new Set([
  'disabled', 'loading', 'invalid', 'bordered', 'closable', 'showIcon', 'showText',
  'dot', 'compact', 'multiple', 'clearable', 'readonly', 'selectable', 'wrap',
  'underline', 'allowClear', 'draggable', 'split', 'hoverable', 'checkable',
  'showLine', 'filterable', 'indeterminate', 'autoSize', 'expandAll', 'checkAll',
])

/* 反向布尔：基础示例默认开着、关掉后外观或能力确实变化的开关。
   只收「关掉仍能正常渲染」的项：open / visible / loading 关掉会把示例变成空壳或
   常驻加载态，disabled 关掉通常就是基础示例本身，故不在此列。
   与 SAFE_BOOLEANS 取并集，避免同一个 prop 既派生 true 又派生 false 时丢方向。 */
const SAFE_FALSE_BOOLEANS = new Set([
  'bordered', 'closable', 'showIcon', 'showText', 'compact', 'multiple', 'clearable',
  'readonly', 'selectable', 'wrap', 'underline', 'allowClear', 'draggable', 'split',
  'hoverable', 'checkable', 'showLine', 'filterable', 'dot', 'danger', 'accordion',
  'autoplay', 'showZero', 'dashed', 'preview', 'editable', 'pannable', 'group',
  'banner', 'dots', 'loop', 'underline',
])

/* 数值 prop 的名称白名单：只有这些名字改成另一个量级才是可读的示例差异，
   min / max / length 之类改值会让示例变成非法状态，不派生。
   visibilityHeight 不在列内：它是 BackTop 唯一「让按钮浮出来」的条件，
   覆盖成任何正数都会让卡片里看不到按钮，派生出来的是一组不可用示例。
   每项给两到三档：档位必须落到真实可见的尺寸差（尺寸、宽高、列数、刻度量），
   同值档会被装配层按基础值剔除，不会产生重复示例。 */
const NUMBER_VARIANTS = {
  size: [16, 28, 44], span: [6, 24], columns: [2, 3, 4], gutter: [8, 24],
  max: [5, 99], total: [3, 8], count: [3, 8], value: [0, 88], percent: [25, 80],
  heading: [1, 4], rows: [2, 5], display: [2, 6], ticks: [24, 72],
  height: [120, 200, 280], width: [120, 240, 320], offsetTop: [24, 80],
  columnWidth: [100, 180], initialIndex: [1, 2], marker: [0.28, 0.75], pageSize: [5, 20],
  current: [0, 2], min: [], max: [],
}

/* 弹层宽度按组件单独给档：Modal / Drawer 的默认宽度是 560 / 520，
   走通用 width 档（120/240/320）会把弹窗压成一条窄边，看不出真实形态。
   这里的档位围绕默认值上下取值，差异在打开态一眼可辨。 */
const OVERLAY_WIDTH_VARIANTS = {
  Modal: [420, 720],
  Drawer: [380, 680],
  FormDialog: [480, 760],
}

/**
 * 按顶层竖线切分类型串，忽略尖括号、花括号、方括号与圆括号内部的竖线。
 *
 * [参数] type 类型串 [返回] 顶层联合成员数组；不含竖线时返回单元素数组。
 */
function splitTopUnion(type) {
  const parts = []
  let depth = 0
  let start = 0
  for (let i = 0; i < type.length; i++) {
    const ch = type[i]
    if ('<{(['.includes(ch)) depth++
    else if ('>})]'.includes(ch)) depth--
    else if (ch === '|' && depth === 0) {
      parts.push(type.slice(start, i))
      start = i + 1
    }
  }
  parts.push(type.slice(start))
  return parts.map((s) => s.trim()).filter(Boolean)
}

/** 剥掉数组包裹，返回元素类型；不是数组就返回 null。 */
function arrayElementOf(type) {
  const t = (type || '').trim()
  const wrapped = /^Array<([\s\S]*)>$/.exec(t)
  if (wrapped) return wrapped[1].trim()
  if (t.endsWith('[]')) return t.slice(0, -2).trim()
  return null
}

/**
 * 从类型串里取出顶层字符串字面量枚举。
 *
 * [参数] type 类型串 [返回] 字面量数组；顶层字面量不足两个时返回空数组。
 * 只认顶层联合成员：`Array<{ tone?: 'lime' | 'red' }>` 里的字面量属于对象字段，
 * 不是这个 prop 自己的取值域，裸扫引号会把它误当成 rows='lime' 这样的标量枚举。
 * 混合联合（如 `'sm' | 'md' | 'lg' | number`）仍取其中的字面量成员，
 * 非字面量成员只是说明该 prop 还接受别的形态，不影响枚举派生。
 */
function literalsOf(type) {
  if (!type) return []
  const lits = []
  for (const part of splitTopUnion(type)) {
    const m = /^'([^']*)'$/.exec(part)
    if (m) lits.push(m[1])
  }
  return lits.length >= 2 ? lits : []
}

/**
 * 取出 prop 的枚举取值域，并说明取值要不要包成数组。
 *
 * [参数] type 类型串 [返回] { lits, wrap }；无枚举时 lits 为空数组。
 * 数组型 prop 的元素若是字面量联合，派生值必须包成单元素数组（`trigger: ['click']`），
 * 直接给标量会触发 Vue 的 prop 类型校验告警。
 */
function enumOf(type) {
  const direct = literalsOf(type)
  if (direct.length >= 2) return { lits: direct, wrap: false }
  const element = arrayElementOf(type)
  if (element) {
    const nested = literalsOf(element)
    if (nested.length >= 2) return { lits: nested, wrap: true }
  }
  return { lits: [], wrap: false }
}

/** 判断类型串是否是布尔、数值或字符串。 */
function kindOf(type) {
  const t = (type || '').replace(/\s/g, '')
  if (t === 'boolean') return 'boolean'
  if (t === 'number') return 'number'
  return 'other'
}

/**
 * 比较基础示例取值与派生覆盖值是否等价。
 *
 * [参数] a 基础值 [返回] b 覆盖值；相等返回 true。
 * 数组型 prop 的取值（如 `trigger: ['hover']`）用 === 比恒不等，
 * 会把与基础示例完全同形的覆盖当成新差异放进来，因此按结构比。
 */
function sameValue(a, b) {
  if (a === b) return true
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.length === b.length && a.every((v, i) => sameValue(v, b[i]))
  }
  return false
}

/**
 * 把契约里的默认值文本还原成 JS 值。
 *
 * 只认字面量（字符串 / 布尔 / 数字）；`() => []`、`null` 这类还原不了就返回 UNSET，
 * 表示「该 prop 没有可用默认值」，不参与同值剔除。
 */
const UNSET = Symbol('unset')

function parseDefault(text) {
  const t = (text ?? '').trim()
  if (!t || t === 'null' || t === '?' || t.startsWith('(') || t.startsWith('()')) return UNSET
  if (t === 'true') return true
  if (t === 'false') return false
  if (/^-?\d+(\.\d+)?$/.test(t)) return Number(t)
  if ((t.startsWith("'") && t.endsWith("'")) || (t.startsWith('"') && t.endsWith('"'))) return t.slice(1, -1)
  return UNSET
}

/* 门控配对表（按「组件名.prop」作用域）：某些 prop 单独覆盖不会改变渲染结果，
   必须同时带上启用它的前置 prop，否则派生出来的格子与基础格渲染完全一致：
   TextInput 的 rows 只挂在多行分支上（单行态是 <input>，rows 无效果）；
   Checkbox 的 indeterminate 样式条件含 !modelValue，基础示例已勾选时看不出半选。
   不限定组件名会误伤同名 prop（Textarea 的 rows 直接生效、且没有 multiline 契约）。 */
const GATING_PAIRS = {
  'TextInput.rows': { multiline: true },
  'Checkbox.indeterminate': { modelValue: false },
  /* size 只在圆环分支参与几何，条形分支改它看不出差异，因此连带切到 circle */
  'Progress.size': { type: 'circle' },
  /* selectedKeys 只在 multiple 且 modelValue 为数组时取多项，单选值下开 multiple 看不出多选，
     因此配套给两个真实节点键，摘要文案从「研发部」变成「研发部、市场部」 */
  'TreeSelect.multiple': { modelValue: [11, 12] },
}

/* 不可见候选黑名单（按「组件名.变体标签」精确剔除派生侧产出的候选）：这些候选单看 props
   与基础格不同，实际渲染结果却完全一致，属重复凑数，需要从源头不派生：
   - SectionLabel as=h2：模板写 `as ?? 'h2'`，不传时本来就是 h2；
   - Carousel current=2：示例只有两屏且 loop，2 % 2 = 0 回到首屏；
   - DictSwatchbook / PostLadder loading：加载态文案被 !types.length / !steps.length 门控，
     派生版只改 loading、样本数据仍在，渲染与基础格一致；真实加载态由策展条目连空数据一起给；
   - Anchor offsetTop：只作用于滚动补偿与观察 rootMargin，静态渲染不参与外观；
   - StyledScrollbar direction=both：基础槽内容只有纵向溢出，横滑块受 hOverflow 门控，
     单改 direction 不会多出横条；真实双轴差异由策展条目把内容改成两轴都溢出；
   - Rate allowClear：只改变再次点击已选星时的清空行为，星数与样式都不变，收起态与基础格一致，
     属行为型差异，从派生侧剔除以免占用一格却看不出区别；
   - Divider direction=vertical：纵向分割线靠并排邻居撑高，单独挂载只剩一条 1em 短线，
     看不出分隔语义；真实用法由策展条目配并排外框给出。 */
const INVISIBLE_CANDIDATES = new Set([
  'SectionLabel.as=h2',
  'Carousel.current=2',
  'DictSwatchbook.loading',
  'PostLadder.loading',
  'Anchor.offsetTop=24',
  'Anchor.offsetTop=80',
  'StyledScrollbar.direction=both',
  'Rate.allowClear',
  'Divider.direction=vertical',
])

/**
 * 为一个组件派生变体列表。
 *
 * [参数] comp 目录索引里的组件描述对象；base 该组件基础示例的有效 props（含组件默认值）
 * [返回] 变体数组，每项含中文标签、props 覆盖与派生来源
 * 与基础示例同值的候选一律剔除：那种格子渲染结果与基础格完全相同，属重复凑数而不是可用示例。
 * 命中门控表的 prop 会自动附带启用前置，保证覆盖后确实改变渲染形态。
 */
function derive(comp, base = {}) {
  const out = []
  const name = comp.name
  const push = (label, props, source) => {
    if (INVISIBLE_CANDIDATES.has(`${name}.${label}`)) return
    const full = { ...props }
    for (const k of Object.keys(full)) {
      const pair = GATING_PAIRS[`${name}.${k}`]
      if (pair) Object.assign(full, pair)
    }
    if (Object.entries(full).every(([k, v]) => sameValue(base[k], v))) return
    out.push({ label, props: full, source })
  }
  for (const prop of comp.props || []) {
    const { lits, wrap } = enumOf(prop.type)
    if (lits.length >= 2) {
      for (const lit of lits) push(`${prop.name}=${lit}`, { [prop.name]: wrap ? [lit] : lit }, 'enum')
      continue
    }
    const kind = kindOf(prop.type)
    if (kind === 'boolean') {
      /* 布尔开关按基础示例的真实取值取反：基础已开启就派生关闭态，基础关闭就派生开启态。
         只派生「改变后仍可正常渲染」的方向，两个白名单各管一个方向，避免把 open=false
         这类会让示例塌成空壳的覆盖放进来。 */
      const on = base[prop.name] === true
      if (on && SAFE_FALSE_BOOLEANS.has(prop.name)) push(`关闭 ${prop.name}`, { [prop.name]: false }, 'boolean')
      if (!on && SAFE_BOOLEANS.has(prop.name)) push(`开启 ${prop.name}`, { [prop.name]: true }, 'boolean')
    }
    if (kind === 'number' && Array.isArray(NUMBER_VARIANTS[prop.name]) && NUMBER_VARIANTS[prop.name].length) {
      /* 弹层宽度优先取该组件的专属档位，避免被通用 width 档压成窄边 */
      const tiers = (prop.name === 'width' && OVERLAY_WIDTH_VARIANTS[name]) || NUMBER_VARIANTS[prop.name]
      for (const n of tiers) push(`${prop.name}=${n}`, { [prop.name]: n }, 'number')
    }
  }
  return out
}

/** 把变体数组渲染成生成物文件正文。 */
function renderTs(table, defaults) {
  const lines = [
    '/* 由 scripts/build_demo_variants.mjs 从组件公开契约机械派生，禁止手改；',
    '   重新生成命令：node scripts/build_demo_variants.mjs',
    '   每项是「基础示例之外的一组可用示例」，标签用契约语言写明差异点。 */',
    'export interface GeneratedVariant {',
    '  /** 变体标签：直接呈现为示例卡上的差异说明 */',
    '  label: string',
    '  /** 覆盖基础示例的 props 片段 */',
    '  props: Record<string, unknown>',
    '  /** 派生来源：enum / boolean / number */',
    '  source: string',
    '}',
    '',
    'export const GENERATED_VARIANTS: Record<string, GeneratedVariant[]> = ' + JSON.stringify(table, null, 2),
    '',
    '/**',
    ' * 组件自身声明的字面量默认值（只收可还原的字符串 / 布尔 / 数字）。',
    ' *',
    ' * 装配层要拿它算「基础示例真实会渲染出来的 props」：demoProps 没写的键，',
    ' * 组件默认值就是实际值，少了这份事实源会把与默认值相同的覆盖误判成差异，',
    ' * 派生或策展出渲染结果与基础格一致的重复示例。',
    ' */',
    'export const DEFAULT_PROPS: Record<string, Record<string, unknown>> = ' + JSON.stringify(defaults, null, 2),
    '',
  ]
  return lines.join('\n')
}

/**
 * 取全部组件的基础示例 props。
 *
 * 必须通过 Vite 加载组件库真实的 demoProps 入口，不能在派生器里手抄一份基础值：
 * 手抄副本会与 demo-props.ts 漂移，把「和基础示例同值」的伪变体重新放回来。
 *
 * [返回] Record<string, Record<string, unknown>> 组件名 → 基础 props
 */
async function loadBaseProps() {
  const require = createRequire(path.join(LIB, 'package.json'))
  const { createServer } = await import('file://' + require.resolve('vite').replace(/\\/g, '/'))
  const server = await createServer({ root: LIB, server: { middlewareMode: true }, appType: 'custom', logLevel: 'error' })
  try {
    const { demoProps } = await server.ssrLoadModule('/src/views/gallery/demo-props.ts')
    const catalog = JSON.parse(fs.readFileSync(CATALOG, 'utf8'))
    const base = {}
    for (const comp of catalog.components) base[comp.name] = demoProps(comp.name)
    return base
  } finally {
    await server.close()
  }
}

/** 入口：读索引、派生变体、写文件或只打印覆盖面。 */
async function main(argv) {
  if (!fs.existsSync(CATALOG)) {
    console.log('VARIANTS: MISSING（组件索引未生成，请先运行 build_component_catalog.mjs）')
    return 1
  }
  const catalog = JSON.parse(fs.readFileSync(CATALOG, 'utf8'))
  const baseProps = await loadBaseProps()
  const table = {}
  const defaults = {}
  const short = []
  for (const comp of catalog.components) {
    const own = {}
    for (const prop of comp.props || []) {
      const v = parseDefault(prop.default)
      if (v !== UNSET) own[prop.name] = v
    }
    defaults[comp.name] = own
    const variants = derive(comp, { ...own, ...(baseProps[comp.name] ?? {}) })
    table[comp.name] = variants
    /* 基础示例 1 组 + 派生变体，少于 3 组说明机械派生覆盖不到，需要策展补齐 */
    if (variants.length < 2) short.push(`${comp.name}(${variants.length})`)
  }
  const total = Object.values(table).reduce((sum, v) => sum + v.length, 0)
  console.log(`派生变体 ${total} 组，覆盖 ${Object.keys(table).length} 个组件`)
  console.log(`需策展补齐（含基础示例仍不足 3 组）：${short.length} 个`)
  if (short.length) console.log('  ' + short.join(' '))
  if (argv.includes('--report')) return 0
  fs.writeFileSync(OUT_TS, renderTs(table, defaults), 'utf8')
  console.log(`VARIANTS_WRITTEN: ${path.relative(SKILL, OUT_TS).replace(/\\/g, '/')}`)
  return 0
}

process.exit(await main(process.argv.slice(2)))
