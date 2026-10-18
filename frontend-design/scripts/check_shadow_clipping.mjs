#!/usr/bin/env node
/**
 * 投影裁切守卫：按「容器四向留白 ≥ 该容器内投影的四向延展上限」这条不变量把关。
 *
 * [判据] 当场从源码推导，不写死数字（测量体见 shadow_clip_measure.mjs）：
 *   1. 外壳：.app-frame 自身声明的柔影由 .stage 留白承接；
 *   2. 示例卡：卡内组件（排除页面级与外壳样式）的柔影由 .g-cell-body 留白承接；
 *   3. 登录页：.login-canvas 的柔影由 .login 留白承接。
 *   几何：层 left = blur/2 + spread - ox，right = +ox，top = -oy，bottom = +oy。
 * [边界] 本文件只做落点定义、对账与裁决；变量表、投影几何与留白读取见测量模块。
 *
 * [用法] node frontend-design/scripts/check_shadow_clipping.mjs
 * [返回] 退出码 0=留白足够；1=存在投影会被裁切边界切成方形暗块。输出 SHADOW_CLIP: PASS/FAIL。
 * 最近修改时间：2026-10-17 09:17:00；改动原因：测量体下沉独立模块，本文件回到仓库 200
 *   行文件基准内；阳性对照由「总条数≥3」改为「每落点四向全中」，防止某落点读不到留白时对照仍假绿。
 */
import { SRC_ROOT, budget, collectTokens, paddingOf, read, relPosix, ruleBody, shadowsIn, shortfall, walk } from './shadow_clip_measure.mjs'

// 示例卡预算排除页面级容器（登录卡、暗页面板）与外壳/工作区（顶栏、导航轨、.content）：
// 前者由自身 overflow 吸收、后者由 .stage 留白承接，都不属于卡内示例内容。
// 排除面与浏览器实测 579 格的卡内四向上限（6/25/47/25）逐维一致。
const EXCLUDE_FROM_CELL = new Set(['src/styles/pages.css', 'src/styles/layout.css'])

/**
 * [参数] files 样式与组件文件绝对路径集合
 * [返回] [{src, layers}] 每个源文件贡献的柔影层（已按文件聚合，无投影的文件不出现）
 * 最近修改时间：2026-10-17 09:25:00
 */
function layersByFile(files) {
  const out = []
  for (const f of files) {
    const layers = shadowsIn(read(relPosix(f)), tokens)
    if (layers.length) out.push({ src: relPosix(f), layers })
  }
  return out
}

const files = walk(SRC_ROOT)
const tokens = collectTokens(files)
const byFile = layersByFile(files)
const all = byFile.flatMap((p) => p.layers)
if (!all.length) {
  console.log('SHADOW_CLIP: FAIL (未解析到任何柔影层，判据失效)')
  process.exit(1)
}

const layout = read('src/styles/layout.css')
const pages = read('src/styles/pages.css')
const overrides = read('src/styles/overrides.css')
const demoCell = read('src/views/gallery/DemoCell.vue')
const card = byFile.filter((p) => !EXCLUDE_FROM_CELL.has(p.src)).flatMap((p) => p.layers)

/* 三个落点：label 同时是读取留白用的选择器；need 由该容器承接的投影求四向上限；
   pad 是本地留白声明所在文本，fallback 让上游自身缺陷在没有覆盖层时也能被抓到。 */
const POINTS = [
  { label: '.stage', need: budget(shadowsIn(ruleBody(layout, '.app-frame'), tokens)), pad: overrides, fallback: layout },
  { label: '.g-cell-body', need: budget(card), pad: demoCell, fallback: demoCell },
  { label: '.login', need: budget(shadowsIn(ruleBody(pages, '.login-canvas'), tokens)), pad: overrides, fallback: pages },
]

/**
 * [参数] padText 留白文本；p 落点定义
 * [返回] 该落点的 [上,右,下,左] 留白；文本读不到时回落上游原值
 * 最近修改时间：2026-10-17 09:36:00
 */
function padOf(padText, p) {
  return paddingOf(padText ?? p.pad, p.label, tokens) ?? paddingOf(p.fallback, p.label, tokens)
}

/**
 * [参数] points 参与对账的落点；padText 覆盖用的留白文本
 * [返回] 不足方向的描述数组
 * 最近修改时间：2026-10-17 09:25:00
 */
function judge(points, padText) {
  const bad = []
  for (const p of points) bad.push(...shortfall(padOf(padText, p), p.need, p.label))
  return bad
}

// 阳性对照必须走与诊断完全相同的比较：把留白清零后，每个落点的四个方向都要报缺，
// 条数不足即说明判据退化成空判定，或某落点根本读不到留白却被当成通过。
const zeroedCell = demoCell.replace(/\.g-cell-body \{([^}]*)\}/, (m, body) => '.g-cell-body {' + body.replace(/padding:[^;]+/, 'padding: 0px') + '}')
const zeroedOverride = overrides.replace(/padding:\s*[^;]+;/g, 'padding: 0px;')
const ctrl = [...judge([POINTS[0], POINTS[2]], zeroedOverride), ...judge([POINTS[1]], zeroedCell)]
if (ctrl.length !== POINTS.length * 4) {
  console.log(`SHADOW_CLIP: FAIL (阳性对照失效：留白清零后报出 ${ctrl.length} 条，应为 ${POINTS.length * 4} 条)`)
  process.exit(1)
}

const problems = judge(POINTS)
console.log(`柔影层=${all.length}（来自 ${byFile.length} 个文件，卡片需承接 ${card.length} 层）`)
for (const p of POINTS) {
  const pad = padOf(null, p)
  console.log(`${p.label} 四向预算=${JSON.stringify(p.need)} 留白=${pad ? pad.join('/') : '缺'}`)
}
if (problems.length) {
  for (const q of problems) console.log('  RISK: ' + q)
  console.log(`SHADOW_CLIP: FAIL (${problems.length} 处投影会被切成暗块)`)
  process.exit(1)
}
console.log('SHADOW_CLIP: PASS (四向留白均覆盖对应投影延展，阳性对照有效)')
