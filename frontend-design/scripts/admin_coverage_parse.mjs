#!/usr/bin/env node
/**
 * 后台可达图的源码解析侧：正则口径、说明符拆解与「标识符是否真被使用」判定。
 *
 * [判据] 「用上」以导入的本地名在剔除导入/导出语句后的正文（模板 + 脚本）中真实出现为准：
 *   .vue 的 `<script setup>` 里对发现层、组合式函数的调用与模板里的 `<Component>`、`:is="X"` 同等算使用；
 *   只导入不使用不构成使用证据，因此批量导入刷满覆盖率会被本口径挡住。
 *
 * [边界] 本文件不读磁盘、不解析路径，只做单文件文本层面的判定。
 * 最近修改时间：2026-10-16 19:34:00；改动原因：从覆盖率守卫拆出解析口径，使各文件回到 200 行基准内。
 */

export const IMPORT_RE = /import\s+([\s\S]*?)\s+from\s+['"]([^'"]+)['"]/g
export const EXPORT_FROM_RE = /export\s*\{([^}]*)\}\s*from\s*['"]([^'"]+)['"]/g
export const EXPORT_STAR_RE = /export\s*\*\s*from\s*['"]([^'"]+)['"]/g
export const DYNAMIC_RE = /import\(\s*['"]([^'"]+)['"]\s*\)/g
export const GLOB_RE = /import\.meta\.glob\(\s*[`'"]([^`'"]+)[`'"]/g

/**
 * 拆解 `import { A, B as C } from 'x'` / `import D from 'x'` 子句。
 *
 * [参数] clause：import 关键字与 from 之间的原文
 * [返回] Array<{local: string, imported: string}> 本地名到导出名的映射
 * 最近修改时间：2026-10-16 19:58:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
export function parseClause(clause) {
  const out = []
  // 1. 去掉 type 前缀后判断子句是否含具名导入的花括号段
  const trimmed = clause.trim().replace(/^type\s+/, '')
  const brace = trimmed.match(/\{([\s\S]*)\}/)
  const before = trimmed.slice(0, brace ? trimmed.indexOf('{') : trimmed.length)
  // 2. 花括号之前的第一个标识符按默认导入处理
  const defaultName = before.split(',')[0].trim().split(/\s+as\s+/).pop().trim()
  if (defaultName && /^[A-Za-z_$][\w$]*$/.test(defaultName) && !defaultName.startsWith('type')) {
    out.push({ local: defaultName, imported: 'default' })
  }
  if (!brace) return out
  // 3. 逐个具名项拆 `X as Y`，得到导出名与本地名
  for (const raw of brace[1].split(',')) {
    const item = raw.trim().replace(/^type\s+/, '')
    if (!item) continue
    const parts = item.split(/\s+as\s+/)
    const imported = parts[0].trim()
    const local = (parts[1] ?? parts[0]).trim()
    if (/^[A-Za-z_$][\w$]*$/.test(local)) out.push({ local, imported })
  }
  return out
}

/**
 * 拆解 `export { A, default as X } from 'x'` 的具名再导出子句。
 *
 * [参数] clause：花括号内的原文
 * [返回] Array<{exported: string, source: string}> 对外导出名到源文件内原始名的映射
 * 最近修改时间：2026-10-16 20:20:00；改动原因：barrel 通道需要与导入子句不同的拆解口径（default 作为源名）。
 */
export function parseReExports(clause) {
  const out = []
  // 1. 逐项拆开，空项与纯 type 项跳过
  for (const raw of clause.split(',')) {
    const item = raw.trim().replace(/^type\s+/, '')
    if (!item) continue
    // 2. `X as Y` 的对外名是 Y、源名是 X；无 as 时两者同名
    const parts = item.split(/\s+as\s+/)
    const source = parts[0].trim()
    const exported = (parts[1] ?? parts[0]).trim()
    if (exported) out.push({ exported, source })
  }
  return out
}

/**
 * 收集一个文件里真的用到的标识符。
 *
 * [参数] raw：文件全文
 * [返回] Set<string> 被使用的标识符集合
 * 最近修改时间：2026-10-16 21:20:00；改动原因：原口径对 .vue 只看模板，漏掉 `<script setup>`
 *   里的真实引用（如示例页对发现层 `demoEntries` 的调用），改为模板与脚本统一取正文标识符。
 */
export function usedIdentifiers(raw) {
  const used = new Set()
  // 1. 先剔除导入与再导出语句，避免把纯导入文本算作使用
  const body = raw.replace(IMPORT_RE, ' ').replace(EXPORT_FROM_RE, ' ').replace(EXPORT_STAR_RE, ' ')
  // 2. 剩下的正文（模板 + 脚本）里出现过的标识符即为使用面
  for (const m of body.matchAll(/\b([A-Za-z_$][\w$]*)\b/g)) used.add(m[1])
  return used
}
