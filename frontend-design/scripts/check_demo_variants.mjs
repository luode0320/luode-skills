#!/usr/bin/env node
/**
 * 组件示例变体覆盖守卫：校验「每个组件都给了多组可用示例」这一验收面是否闭合。
 *
 * [判据] 当场 import 生产装配层（entries.ts）取真实展开结果，不手抄变体清单：
 *   1. 覆盖：磁盘每个 .vue 组件都至少有一格示例；
 *   2. 多组：每个组件的示例格数 ≥ MIN_VARIANTS；契约冻结组件（对外只有 open 一个 props、
 *      内容硬编码）允许降到 MIN_VARIANTS_FROZEN，并在输出中显式列出，避免用假变体凑数；
 *   3. 标签唯一：同组件内标签不得重复（重复说明策展与派生互相吃掉）；
 *   4. props 合法：每格覆盖的 prop 名必须在组件公开契约里存在，防止传错名让示例静默失效；
 *   5. 子分组可进：分类数据源里每个子分组都至少有一格示例，防止菜单登记了页面却点出空白。
 * [约束] 参照物稳健性要求本守卫复用真实模块入口而不是正则解析源文件；
 *   Vite 只能从组件库自身 node_modules 解析，故 createServer 的 root 固定为 component-library。
 *
 * [用法] node frontend-design/scripts/check_demo_variants.mjs
 * [返回] 退出码 0=通过；1=漂移。输出 DEMO_VARIANTS: PASS/FAIL。
 * 最近修改时间：2026-10-17 02:45:00；改动原因：两级菜单后新增空子分组判据。
 *   每个子分组都有示例，否则菜单点进去是空白页。
 */

import fs from 'node:fs'
import path from 'node:path'
import { createRequire } from 'node:module'
import { fileURLToPath } from 'node:url'
import { COMPONENT_SUB_GROUPS } from '../component-library/src/data/component-categories.ts'

const MIN_VARIANTS = 3
/* 单维契约组件：公开 props 只有一个开关布尔、没有任何插槽、内容硬编码（上游冻结文件），
   除「收起 / 展开」外不存在第二种可用差异。给它们凑第三组只能造渲染结果相同的伪变体，
   因此按契约特征识别后下限降到 1，并在输出里显式列出，不拿伪差异冒充达标。 */
const MIN_VARIANTS_SINGLE_DIM = 1
const HERE = path.dirname(fileURLToPath(import.meta.url))
const LIB = path.join(HERE, '..', 'component-library')
const SRC_COMPONENTS = path.join(LIB, 'src', 'components')
const CATALOG = path.join(HERE, '..', 'references', 'component-catalog.json')
const ENTRIES = '/src/views/gallery/entries.ts'

/** 递归收集磁盘上全部组件文件名（不含 .vue）。 */
function walk(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, acc)
    else if (entry.name.endsWith('.vue')) acc.push(entry.name.replace(/\.vue$/, ''))
  }
  return acc
}

/**
 * 算一格的渲染结果指纹：props 内容 + 插槽源码 + 画布高度 + 触发动作。
 *
 * props 走 JSON 序列化而不是对象引用——同一份样本在装配层会被展开成不同对象，
 * 只有内容口径能判出「这两格渲染出来一模一样」。
 *
 * [参数] e 装配后的示例格
 * [返回] string 可比较指纹
 */
function renderFingerprint(e) {
  const props = Object.keys(e.props).sort().map((k) => `${k}=${JSON.stringify(e.props[k]) ?? String(e.props[k])}`).join(',')
  const slots = Object.keys(e.slots).sort().map((k) => `${k}:${e.slots[k].toString()}`).join(',')
  return `${props}|${slots}|${e.canvas}|${e.action}|frame:${JSON.stringify(e.frame ?? null)}`
}

/** 在组件库自身 node_modules 里起一个 Vite，把源码模块当模块加载取真实装配结论。 */
async function openServer() {
  const require = createRequire(path.join(LIB, 'package.json'))
  const viteEntry = require.resolve('vite')
  const { createServer } = await import('file://' + viteEntry.replace(/\\/g, '/'))
  return createServer({ root: LIB, server: { middlewareMode: true }, appType: 'custom', logLevel: 'error' })
}

/** 主流程：磁盘全集 vs 装配结果对账，返回退出码。 */
async function main() {
  if (!fs.existsSync(SRC_COMPONENTS) || !fs.existsSync(CATALOG)) {
    console.log('DEMO_VARIANTS: FAIL（组件目录或契约索引不存在）')
    return 1
  }
  const disk = new Set(walk(SRC_COMPONENTS))
  const catalog = JSON.parse(fs.readFileSync(CATALOG, 'utf8'))
  /* 契约索引 components 是 151 项扁平数组，按组件名索引 props 与 slots */
  const propsOf = new Map()
  const slotsOf = new Map()
  for (const c of catalog.components) {
    propsOf.set(c.name, new Set((c.props || []).map((p) => p.name)))
    slotsOf.set(c.name, new Set(c.slots || []))
  }

  const server = await openServer()
  let demoEntries
  try {
    demoEntries = (await server.ssrLoadModule(ENTRIES)).demoEntries
  } finally {
    await server.close()
  }
  const byComponent = new Map()
  for (const e of demoEntries) {
    if (!byComponent.has(e.name)) byComponent.set(e.name, [])
    byComponent.get(e.name).push(e)
  }

  /* 渲染结果重复：同组件内两格的可观测输入（props 内容 + 插槽源码 + 画布 + 动作）完全一致，
     说明其中一格是白写的示例。按内容而不是按标签比，才能抓到「标签不同、渲染相同」。 */
  const duplicate = []
  for (const [name, list] of byComponent) {
    const seen = new Map()
    for (const e of list) {
      const fp = renderFingerprint(e)
      if (seen.has(fp)) duplicate.push(`${name}: ${seen.get(fp)} ≡ ${e.label}`)
      else seen.set(fp, e.label)
    }
  }

  const failures = []
  const missing = [...disk].filter((n) => !byComponent.has(n))
  if (missing.length) failures.push('无示例组件: ' + missing.sort().join(', '))

  /* 子分组空页：菜单按「父分类/子分组」登记路由，页面用 sub.components 过滤示例，
     若某个子分组里一个组件都没落到示例（改名、漏归类），点进去就是空白页，必须抓到。 */
  const emptySubs = []
  for (const sub of COMPONENT_SUB_GROUPS) {
    const hit = sub.components.some((n) => byComponent.has(n))
    if (!hit) emptySubs.push(`${sub.categoryKey}/${sub.key}`)
  }
  if (emptySubs.length) failures.push('子分组无示例(点进空白页): ' + emptySubs.join(', '))

  const under = []
  const singleDim = []
  for (const [name, list] of byComponent) {
    if (isSingleDimContract(propsOf.get(name), slotsOf.get(name))) {
      singleDim.push(`${name}=${list.length}`)
      if (list.length < MIN_VARIANTS_SINGLE_DIM) under.push(`${name}=${list.length}`)
      continue
    }
    if (list.length < MIN_VARIANTS) under.push(`${name}=${list.length}`)
  }
  if (under.length) failures.push(`示例不足 ${MIN_VARIANTS} 组: ${under.sort().join(', ')}`)

  const dupLabels = []
  const badProps = []
  for (const [name, list] of byComponent) {
    const labels = list.map((e) => e.label)
    const dup = labels.filter((l, i) => labels.indexOf(l) !== i)
    if (dup.length) dupLabels.push(`${name}: ${[...new Set(dup)].join('/')}`)
    const known = propsOf.get(name)
    if (!known) continue
    // props 合法性按「该组件全部示例用到的 prop 名并集」判：装配层只并基础样本与变体覆盖，
    // open 型弹层在收起态不声明 open 属正常结果，按单格判会误报
    const used = new Set(list.flatMap((e) => Object.keys(e.props)))
    const illegal = [...used].filter((k) => !known.has(k))
    if (illegal.length) badProps.push(`${name}: ${illegal.join('/')}`)
  }
  if (dupLabels.length) failures.push('同组件标签重复: ' + dupLabels.join(', '))
  if (badProps.length) failures.push('props 不在公开契约内: ' + badProps.slice(0, 12).join(', '))
  if (duplicate.length) failures.push(`渲染结果重复的示例: ${duplicate.slice(0, 15).join(' ; ')}`)

  if (failures.length) {
    console.log('DEMO_VARIANTS: FAIL')
    for (const f of failures) console.log('  -', f)
    console.log(`  组件=${byComponent.size} 示例格=${demoEntries.length}`)
    return 1
  }

  const total = demoEntries.length
  const avg = (total / byComponent.size).toFixed(2)
  console.log(`DEMO_VARIANTS: PASS（${byComponent.size} 个组件共 ${total} 组示例，平均 ${avg} 组/组件；磁盘 ${disk.size}）`)
  if (singleDim.length) console.log(`  单维契约降档至 ${MIN_VARIANTS_SINGLE_DIM} 组: ${singleDim.sort().join(', ')}`)
  return 0
}

/**
 * 判定组件是否属单维契约：公开 props 只有一个布尔开关，且没有任何插槽。
 *
 * [参数] props 该组件公开 props 名集合；slots 该组件插槽名集合
 * [返回] boolean 是否按降档下限校验
 */
function isSingleDimContract(props, slots) {
  if (!props || props.size !== 1) return false
  const only = [...props][0]
  const switchLike = only === 'open' || only === 'visible'
  return switchLike && (!slots || slots.size === 0)
}

process.exit(await main())
