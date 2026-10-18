#!/usr/bin/env node
/**
 * 后台可达图的访问器：磁盘目录遍历、说明符解析、barrel 通道与通配展开。
 *
 * [判据] `import.meta.glob` 指向某目录的运行时磁盘发现视为命中该目录下全部组件文件；
 *   组件目录下的 barrel 索引文件只做名称到文件的解析通道，本身不构成使用证据。
 *
 * [边界] 本文件不含闭包遍历与覆盖率裁决：引用边遍历见 admin_coverage_reach.mjs，
 *   导入子句拆解与「标识符是否真被使用」口径见 admin_coverage_parse.mjs，裁决见 check_admin_component_coverage.mjs。
 * 最近修改时间：2026-10-16 20:12:00；改动原因：遍历体下沉到独立模块，本文件只保留访问器并回到函数行数基准内。
 */

import fs from 'node:fs'
import path from 'node:path'
import { EXPORT_FROM_RE, EXPORT_STAR_RE, parseReExports } from './admin_coverage_parse.mjs'

/**
 * 递归收集指定目录下的文件（相对 lib 根的统一正斜杠路径）。
 *
 * [参数] lib：计算相对路径用的库根；dir：当前目录；filter：文件命中判据；acc：累积结果数组
 * [返回] string[] 命中过滤器的文件相对路径列表
 * 最近修改时间：2026-10-16 19:58:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function walk(lib, dir, filter, acc = []) {
  // 1. 目录不存在直接返回累积器，让调用方对缺失目录保持宽容
  if (!fs.existsSync(dir)) return acc
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    // 2. 子目录递归下钻，命中过滤器则记为相对路径
    if (entry.isDirectory()) walk(lib, p, filter, acc)
    else if (filter(p)) acc.push(path.relative(lib, p).replace(/\\/g, '/'))
  }
  return acc
}

/**
 * 建立组件库的模块图上下文。
 *
 * [参数] lib：组件库根绝对路径；alias：说明符前缀到绝对目录的映射（如 `@` → `lib/src`）
 * [返回] { lib, alias, textCache, barrelCache } 供各访问器按名取用
 * 最近修改时间：2026-10-16 20:12:00；改动原因：闭包工厂改为显式上下文，各函数独立满足行数基准。
 */
function createContext(lib, alias) {
  return { lib, alias, textCache: new Map(), barrelCache: new Map() }
}

/**
 * 读取文件正文并按相对路径缓存。
 *
 * [参数] ctx：图上下文；rel：文件相对路径
 * [返回] string 文件正文
 * 最近修改时间：2026-10-16 20:12:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function readText(ctx, rel) {
  // 1. 首次读取即入缓存，后续遍历复用同一份正文
  if (!ctx.textCache.has(rel)) ctx.textCache.set(rel, fs.readFileSync(path.join(ctx.lib, rel), 'utf8'))
  return ctx.textCache.get(rel)
}

/**
 * 把导入说明符解析成磁盘真实文件。
 *
 * [参数] ctx：图上下文；params：`{ spec, fromRel }` 说明符原文与发起导入的文件相对路径
 * [返回] string | null 命中文件相对路径；第三方包、样式等解析不到时为 null
 * 最近修改时间：2026-10-16 20:12:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function resolve(ctx, params) {
  const { spec, fromRel } = params
  // 1. 找出命中的别名前缀；相对与别名之外的说明符（第三方包、样式）判为不可解析
  const aliasKey = Object.keys(ctx.alias).find((k) => spec.startsWith(`${k}/`))
  if (!aliasKey && !spec.startsWith('.')) return null
  // 2. 按别名或所在目录算出基路径
  const base = aliasKey
    ? path.join(ctx.alias[aliasKey], spec.slice(aliasKey.length + 1))
    : path.join(ctx.lib, path.dirname(fromRel), spec)
  // 3. 依次尝试裸路径与补全后缀的候选，命中真实文件即返回
  const candidates = [base, `${base}.vue`, `${base}.ts`, path.join(base, 'index.ts'), path.join(base, 'index.vue')]
  for (const c of candidates) {
    const rel = path.relative(ctx.lib, c).replace(/\\/g, '/')
    if (rel.startsWith('..')) continue
    if (fs.existsSync(c) && fs.statSync(c).isFile()) return rel
  }
  return null
}

/**
 * 解析 barrel 文件，建立「导出名 -> 源文件」通道。
 *
 * [参数] ctx：图上下文；rel：barrel 文件相对路径
 * [返回] Map<string, {file, name}> 导出名到源文件与原始导出名的映射
 * 最近修改时间：2026-10-16 20:12:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function barrelsOf(ctx, rel) {
  // 1. 同一 barrel 只解析一次，命中缓存直接返回
  if (ctx.barrelCache.has(rel)) return ctx.barrelCache.get(rel)
  const map = new Map()
  const raw = readText(ctx, rel)
  // 2. 具名再导出：按再导出口径拆出对外名与源名，登记到源文件
  for (const m of raw.matchAll(EXPORT_FROM_RE)) {
    const target = resolve(ctx, { spec: m[2], fromRel: rel })
    if (!target) continue
    for (const item of parseReExports(m[1])) map.set(item.exported, { file: target, name: item.source })
  }
  // 3. 整表再导出记为通配通道，供后续按名继续追
  for (const m of raw.matchAll(EXPORT_STAR_RE)) {
    const target = resolve(ctx, { spec: m[1], fromRel: rel })
    if (target) map.set('*', { file: target, name: '*' })
  }
  ctx.barrelCache.set(rel, map)
  return map
}

/**
 * 沿 barrel 追一个导出名最终落在哪个文件。
 *
 * [参数] ctx：图上下文；params：`{ file, name, depth }` 当前文件、导出名与递归深度
 * [返回] string | null 最终落点文件；追不到或超出深度上限时为 null
 * 最近修改时间：2026-10-16 20:12:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function followBarrel(ctx, params) {
  const { file, name, depth = 0 } = params
  // 1. 深度上限保护，避免异常环形再导出把遍历拖死
  if (depth > 6) return null
  // 2. 非 barrel（.vue 与数据文件）本身就是落点
  if (!file.endsWith('.ts')) return file
  const hit = barrelsOf(ctx, file).get(name)
  if (!hit) return null
  // 3. 通配通道按同名继续下钻，具名通道按其原始名下钻
  return followBarrel(ctx, { file: hit.file, name: hit.name === '*' ? name : hit.name, depth: depth + 1 })
}

/**
 * 展开 `import.meta.glob` 说明符为其匹配目录下的全部 vue 文件。
 *
 * [参数] ctx：图上下文；params：`{ spec, fromRel }` 通配说明符原文与发起文件相对路径
 * [返回] string[] 匹配目录下的全部 vue 文件相对路径
 * 最近修改时间：2026-10-16 20:12:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function globTargets(ctx, params) {
  const { spec, fromRel } = params
  // 1. 取通配前缀目录并换算为相对路径，越出库根的忽略
  const cleaned = spec.replace(/\*\*.*$/, '').replace(/[`'"]/g, '')
  const absBase = path.resolve(path.join(ctx.lib, path.dirname(fromRel)), cleaned)
  const relBase = path.relative(ctx.lib, absBase).replace(/\\/g, '/')
  if (relBase.startsWith('..')) return []
  // 2. 该目录下的 vue 文件即为运行时可发现集合
  return walk(ctx.lib, path.join(ctx.lib, relBase), (p) => p.endsWith('.vue'))
}

/**
 * 建立组件库的模块图访问器集合。
 *
 * [参数] lib：组件库根绝对路径；alias：说明符前缀到绝对目录的映射（如 `@` → `lib/src`）
 * [返回] { walk, readText, resolve, followBarrel, globTargets } 按名调用的只读访问器
 * 最近修改时间：2026-10-16 20:12:00；改动原因：只绑定上下文并暴露同名窄接口，供遍历侧使用。
 */
export function createModuleGraph(lib, alias = { '@': path.join(lib, 'src') }) {
  // 1. 建上下文持有库根、别名与两份缓存
  const ctx = createContext(lib, alias)
  // 2. 把上下文绑定到同名窄接口上暴露给遍历侧
  return {
    walk: (dir, filter) => walk(lib, dir, filter),
    readText: (rel) => readText(ctx, rel),
    resolve: (params) => resolve(ctx, params),
    followBarrel: (params) => followBarrel(ctx, params),
    globTargets: (params) => globTargets(ctx, params),
  }
}
