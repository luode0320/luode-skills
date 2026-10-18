#!/usr/bin/env node
/**
 * 投影裁切守卫的测量侧：样式文件枚举、变量表合成、柔影几何与容器留白读取。
 *
 * [判据] 全部从磁盘源码当场推导，不写死数字：变量表由 src 下全部 .css/.vue 的自定义
 *   属性声明合成；柔影层只取非 inset 且 blur>=4 的层；留白按 padding 简写一到四值展开。
 * [边界] 本文件不含落点对账与裁决：三落点比较、阳性对照与输出见 check_shadow_clipping.mjs。
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉测量体，让入口回到仓库
 *   200 行文件基准内，与后台覆盖率守卫「裁决入口 + 测量模块」的拆分口径一致。
 */
import fs from 'node:fs'
import path from 'node:path'

export const LIB_ROOT = path.join(import.meta.dirname, '..', 'component-library')
export const SRC_ROOT = path.join(LIB_ROOT, 'src')
const DIRS = ['top', 'right', 'bottom', 'left']
const COLOR = /(?:rgba?|hsla?|color|lab|lch|oklch|oklab)\([^)]*\)|#[0-9a-fA-F]{3,8}|\binset\b|\bnone\b/g
const VAR = /var\((--[\w-]+)[^)]*\)/g

/**
 * [参数] dir 目录
 * [返回] 目录内全部 .css/.vue 绝对路径
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
export function walk(dir) {
  const out = []
  for (const name of fs.readdirSync(dir)) {
    const p = path.join(dir, name)
    if (fs.statSync(p).isDirectory()) out.push(...walk(p))
    else if (/\.(css|vue)$/.test(name)) out.push(p)
  }
  return out
}

/**
 * [参数] rel 相对 component-library 的 POSIX 风格路径
 * [返回] 该文件的文本内容
 * 最近修改时间：2026-10-17 09:12:00
 */
export function read(rel) {
  return fs.readFileSync(path.join(LIB_ROOT, ...rel.split('/')), 'utf8')
}

/**
 * [参数] abs 绝对路径
 * [返回] 相对组件库根的 POSIX 分隔符路径
 * 最近修改时间：2026-10-17 09:12:00；改动原因：Windows 下 relative() 返回反斜杠，
 * 不归一会让排除表永不命中，把页面级投影误算进卡片预算。
 */
export function relPosix(abs) {
  return path.relative(LIB_ROOT, abs).split(path.sep).join('/')
}

/**
 * [参数] files 样式与组件文件绝对路径集合
 * [返回] 自定义属性名到声明值的映射表
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
export function collectTokens(files) {
  const tokens = new Map()
  for (const f of files) {
    for (const m of fs.readFileSync(f, 'utf8').matchAll(/(--[\w-]+):\s*([^;]+);/g)) tokens.set(m[1], m[2])
  }
  return tokens
}

/**
 * [参数] text 文件文本；selector 规则选择器
 * [返回] 该规则声明块正文（含末尾右括号）；未找到返回空串
 * 最近修改时间：2026-10-17 09:12:00
 */
export function ruleBody(text, selector) {
  const at = text.indexOf(selector + ' {')
  if (at < 0) return ''
  return text.slice(at, text.indexOf('}', at) + 1)
}

/**
 * [参数] s CSS 值；tokens 变量表
 * [返回] 展开 var() 后的字符串（最多迭代 6 层，防止变量环导致死循环）
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
function expand(s, tokens) {
  let cur = s
  for (let i = 0; i < 6; i++) {
    const next = cur.replace(VAR, (_, k) => tokens.get(k) ?? '0')
    if (next === cur) break
    cur = next
  }
  return cur
}

/**
 * [参数] value box-shadow 值；tokens 变量表
 * [返回] 非 inset、blur>=4 的柔影层 [{top,right,bottom,left,layer}]
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
export function softLayers(value, tokens) {
  const out = []
  for (const layer of expand(value, tokens).split(/,(?![^(]*\))/)) {
    const t = layer.trim()
    // 1. 内阴影与被裁切无关，none 与空值不产出几何。
    if (!t || t.includes('none') || t.includes('inset')) continue
    const nums = (t.replace(COLOR, ' ').match(/-?\d*\.?\d+/g) ?? []).map(Number)
    // 2. 只有颜色无偏移的层（如纯描边式投影）不参与留白对账。
    if (nums.length < 3) continue
    const [ox, oy, blur, spread = 0] = nums
    // 3. blur 小于 4px 的硬边投影本就贴合元素轮廓，不算会被切成暗块的柔影。
    if (blur < 4) continue
    const half = blur / 2 + spread
    out.push({ top: half - oy, right: half + ox, bottom: half + oy, left: half - ox, layer: t.slice(0, 38) })
  }
  return out
}

/**
 * [参数] text 文本；tokens 变量表
 * [返回] 该文本声明的全部柔影层
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
export function shadowsIn(text, tokens) {
  const out = []
  for (const m of text.matchAll(/box-shadow:\s*([^;{}]+)/g)) out.push(...softLayers(m[1], tokens))
  return out
}

/**
 * [参数] layers 柔影层集合
 * [返回] 四向各自需要的留白上限
 * 最近修改时间：2026-10-17 09:12:00；改动原因：从守卫入口下沉。
 */
export function budget(layers) {
  const b = { top: 0, right: 0, bottom: 0, left: 0 }
  for (const l of layers) for (const d of DIRS) b[d] = Math.max(b[d], l[d])
  return b
}

/**
 * [参数] text 文件文本；selector 规则选择器；tokens 变量表
 * [返回] 该规则 padding 的 [上,右,下,左]；未声明返回 null
 * 最近修改时间：2026-10-17 09:26:00；改动原因：从守卫入口下沉。
 */
// exemption: 极简查询函数，文本、选择器与变量表是它的三个原生入参，封装结构体只会造一次性包装
export function paddingOf(text, selector, tokens) {
  const block = ruleBody(text, selector)
  if (!block) return null
  const m = block.match(/padding:\s*([^;]+)/)
  if (!m) return null
  const nums = (expand(m[1], tokens).match(/\d+(?:\.\d+)?px/g) ?? []).map(parseFloat)
  if (!nums.length) return null
  if (nums.length === 1) return [nums[0], nums[0], nums[0], nums[0]]
  if (nums.length === 2) return [nums[0], nums[1], nums[0], nums[1]]
  if (nums.length === 3) return [nums[0], nums[1], nums[2], nums[1]]
  return nums.slice(0, 4)
}

/**
 * [参数] pad [上,右,下,左]；need 四向预算；label 落点名
 * [返回] 不足方向的描述数组
 * 最近修改时间：2026-10-17 09:26:00；改动原因：从守卫入口下沉。
 */
// exemption: 纯比较函数，留白、预算与落点名三者是它的最小原生入参，封装结构体只会造一次性包装
export function shortfall(pad, need, label) {
  if (!pad) return [`${label} 未声明留白`]
  const bad = []
  DIRS.forEach((d, i) => {
    if (need[d] > pad[i] + 0.01) bad.push(`${label}.${d} 需 ${Math.round(need[d])}px 只有 ${pad[i]}px`)
  })
  return bad
}
