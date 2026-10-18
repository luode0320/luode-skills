#!/usr/bin/env node
/**
 * 生成组件目录索引：把全部组件的公开契约、用法骨架与真实引用位置汇总成
 * 一份可被 skill 直接检索的目录（Markdown 速查 + JSON 机器索引）。
 *
 * [用法]
 *   node scripts/build_component_catalog.mjs           # 生成索引
 *   node scripts/build_component_catalog.mjs --check   # 只校验索引与磁盘是否同步
 * [返回] 退出码 0=生成成功或索引一致；1=索引缺失、过期或写入失败。
 * 最近修改时间：2026-10-15 17:40:00；改动原因：用户要求组件库能"一键找到对应组件使用"，需要可信的自动索引而非手抄清单。
 */

import crypto from 'node:crypto'
import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { loadTs, extractApi } from './extract_component_api.mjs'
import { COMPONENT_CATEGORY_OF, COMPONENT_CATEGORY_ORDER } from '../component-library/src/data/component-categories.ts'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const SKILL = path.resolve(HERE, '..')
const LIB = path.join(SKILL, 'component-library')
const SRC = path.join(LIB, 'src')
const OUT_MD = path.join(SKILL, 'references', 'component-catalog.md')
const OUT_JSON = path.join(SKILL, 'references', 'component-catalog.json')

/* 物理目录仍保留（对应上游归属与还原度基线），语义分类从单一数据源派生，不手抄 */
const GROUP_LABEL = {
  root: '根级组件',
  ui: '基础控件',
  business: '业务组件',
  workspace: '工作台版式（本地扩展）',
  extend: 'Arco 品类对齐（本地扩展）',
  charts: '自研图表',
  layout: '外壳布局',
}
const GROUP_ORDER = ['ui', 'business', 'workspace', 'extend', 'charts', 'layout', 'root']
const CATEGORY_LABEL = Object.fromEntries(COMPONENT_CATEGORY_ORDER.map((c) => [c.key, c.label]))
const CATEGORY_ORDER = COMPONENT_CATEGORY_ORDER.map((c) => c.key)

/** 递归收集指定扩展名的文件。 */
function walk(dir, ext, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, ext, acc)
    else if (entry.name.endsWith(ext)) acc.push(p)
  }
  return acc
}

/** 由组件库相对路径推断分组；未知层级归入根级。 */
function groupOf(rel) {
  const m = rel.match(/^src\/components\/([^/]+)\//)
  return m && GROUP_ORDER.includes(m[1]) ? m[1] : 'root'
}

/** 按类型给出最小可用占位值，用于合成可复制的用法骨架。 */
function placeholder(type) {
  const t = type.trim()
  const literal = t.match(/^['"]([^'"]+)['"]/)
  if (literal) return { text: `"${literal[1]}"` }
  if (/^number/.test(t)) return { text: '0', expr: true }
  if (/^boolean/.test(t)) return { text: '', bare: true }
  if (/\[\]|Array</.test(t)) return { text: '[]', expr: true }
  return { text: '"文本"' }
}

/** 合成组件用法骨架：列必填项与枚举项，不臆造业务取值。 */
function usageOf(name, api) {
  const attrs = []
  for (const p of api.props) {
    const optional = p.optional
    if (optional && !/^['"]/.test(p.type.trim())) continue
    const ph = placeholder(p.type)
    if (ph.bare) attrs.push(p.name)
    else attrs.push(ph.expr ? `:${p.name}="${ph.text}"` : `${p.name}=${ph.text}`)
  }
  const open = `<${name}${attrs.length ? ' ' + attrs.join(' ') : ''}`
  return api.slots.includes('default') ? `${open}>内容</${name}>` : `${open} />`
}

/** 扫描组件库源码，建立"组件 → 被哪些文件引用"的反向索引。 */
function collectUsages(names) {
  const usage = Object.fromEntries(names.map((n) => [n, []]))
  const files = [...walk(SRC, '.vue'), ...walk(SRC, '.ts')]
  for (const file of files) {
    const rel = path.relative(LIB, file).replace(/\\/g, '/')
    const raw = fs.readFileSync(file, 'utf8')
    for (const m of raw.matchAll(/import\s+\w+\s+from\s+['"]([^'"]+\.vue)['"]/g)) {
      const base = path.basename(m[1], '.vue')
      if (usage[base] && !usage[base].includes(rel)) usage[base].push(rel)
    }
  }
  return usage
}

/** 组装完整目录数据：契约 + 用法 + 引用位置 + 契约指纹。 */
function build() {
  const ts = loadTs(LIB)
  const files = walk(path.join(SRC, 'components'), '.vue').sort()
  const names = files.map((f) => path.basename(f, '.vue'))
  const usages = collectUsages(names)
  const components = files.map((file) => {
    const name = path.basename(file, '.vue')
    const rel = path.relative(LIB, file).replace(/\\/g, '/')
    const api = extractApi(ts, file)
    const fingerprint = crypto
      .createHash('sha256')
      .update(JSON.stringify({ p: api.props, e: api.emits, s: api.slots, t: api.types }))
      .digest('hex')
      .slice(0, 16)
    return {
      name,
      group: groupOf(rel),
      category: COMPONENT_CATEGORY_OF[name] ?? 'general',
      path: rel,
      import: `@/${rel.replace(/^src\//, '')}`,
      description: api.description,
      props: api.props,
      emits: api.emits,
      slots: api.slots,
      types: api.types,
      usage: usageOf(name, api),
      used_by: usages[name] || [],
      fingerprint,
    }
  })
  const counts = {}
  for (const c of components) counts[c.group] = (counts[c.group] || 0) + 1
  const categoryCounts = {}
  for (const c of components) categoryCounts[c.category] = (categoryCounts[c.category] || 0) + 1
  return { total: components.length, counts, categoryCounts, components }
}

/** 渲染 Markdown 目录：速查表在前，逐组件契约在后。 */
function renderMarkdown(catalog) {
  const esc = (s) => String(s).replace(/\|/g, '\\|')
  const catLine = CATEGORY_ORDER.filter((k) => catalog.categoryCounts[k])
    .map((k) => `${CATEGORY_LABEL[k]} ${catalog.categoryCounts[k]}`).join(' · ')
  const lines = [
    '# 珍珠玻璃组件库 · 组件目录索引',
    '',
    '> 本文件由 `scripts/build_component_catalog.mjs` 从组件源码自动生成，请勿手改；组件契约变化后重跑生成命令。',
    `> 共 ${catalog.total} 个组件。`,
    `> 物理目录：${GROUP_ORDER.filter((g) => catalog.counts[g]).map((g) => `${GROUP_LABEL[g]} ${catalog.counts[g]}`).join(' · ')}。`,
    `> 语义分类（对齐 Arco 组件菜单）：${catLine}。`,
    '',
    '## 速查表',
    '',
    '| 组件 | 分类 | 物理目录 | 引入路径 | 必填 props | 说明 |',
    '| --- | --- | --- | --- | --- | --- |',
  ]
  for (const g of GROUP_ORDER) {
    for (const c of catalog.components.filter((x) => x.group === g)) {
      const required = c.props.filter((p) => !p.optional).map((p) => p.name).join(', ') || '—'
      lines.push(`| ${c.name} | ${CATEGORY_LABEL[c.category]} | ${GROUP_LABEL[g]} | \`${c.import}\` | ${esc(required)} | ${esc(c.description || '—')} |`)
    }
  }
  lines.push('', '## 组件契约', '')
  for (const g of GROUP_ORDER) {
    const items = catalog.components.filter((x) => x.group === g)
    if (!items.length) continue
    lines.push(`### ${GROUP_LABEL[g]}（${items.length}）`, '')
    for (const c of items) {
      lines.push(`#### ${c.name}`, '')
      if (c.description) lines.push(c.description, '')
      lines.push('```vue', c.usage, '```', '')
      if (c.props.length) {
        lines.push('| prop | 类型 | 必填 | 默认 |', '| --- | --- | --- | --- |')
        for (const p of c.props) lines.push(`| ${p.name} | \`${esc(p.type)}\` | ${p.optional ? '否' : '是'} | ${esc(p.default ?? '—')} |`)
        lines.push('')
      }
      if (c.emits.length) lines.push(`**事件**：${c.emits.map((e) => `\`${e.name}\`(${esc(e.payload)})`).join('、')}`, '')
      if (c.slots.length) lines.push(`**插槽**：${c.slots.map((s) => `\`${s}\``).join('、')}`, '')
      if (c.types.length) lines.push(`**导出类型**：${c.types.map((t) => `\`${t}\``).join('、')}`, '')
      if (c.used_by.length) lines.push(`**参考实现**：${c.used_by.slice(0, 8).map((u) => `\`${u}\``).join('、')}`, '')
      lines.push('')
    }
  }
  return lines.join('\n') + '\n'
}

/** 入口：生成索引，或用 --check 校验索引与磁盘是否同步。 */
function main(argv) {
  const catalog = build()
  if (argv.includes('--check')) {
    if (!fs.existsSync(OUT_JSON)) {
      console.log('CATALOG: MISSING（索引未生成，请运行生成命令）')
      return 1
    }
    const prev = JSON.parse(fs.readFileSync(OUT_JSON, 'utf8'))
    /* 签名含 category：分类数据源漂移时 --check 必须报 STALE，不得静默通过 */
    const sig = (list) => JSON.stringify(list.map((c) => [c.name, c.group, c.category, c.fingerprint]))
    const same = prev.total === catalog.total && sig(prev.components) === sig(catalog.components)
    console.log(same ? `CATALOG: PASS (${catalog.total} components)` : 'CATALOG: STALE（磁盘契约与索引不一致，请重新生成）')
    return same ? 0 : 1
  }
  fs.writeFileSync(OUT_JSON, JSON.stringify(catalog, null, 2) + '\n', 'utf8')
  fs.writeFileSync(OUT_MD, renderMarkdown(catalog), 'utf8')
  console.log(`CATALOG_WRITTEN: ${catalog.total} components -> ${path.relative(SKILL, OUT_MD).replace(/\\/g, '/')}`)
  return 0
}

process.exit(main(process.argv.slice(2)))
