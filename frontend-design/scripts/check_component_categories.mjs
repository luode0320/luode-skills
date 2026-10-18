#!/usr/bin/env node
/**
 * 组件分类完整性守卫：校验两级分类真相源（父分类 → 子分组 → 组件）对磁盘全集是否闭合。
 *
 * [判据] 当场从磁盘 .vue 与「import 真实模块得到的归类」双向对账，不重解析源文件结构：
 *   1. 覆盖：磁盘每个 .vue 组件都被归类；
 *   2. 唯一：每个组件恰好归入一个子分组（不得跨子分组或跨父分类重复出现）；
 *   3. 无幽灵：归类表里没有磁盘不存在的组件名；
 *   4. 父分类数下限：不得少于 MIN_CATEGORIES（防止退化成粗分桶）；
 *   5. 子分组闭合：子分组键全局唯一、每组至少一个组件（菜单与路由靠它寻址）；
 *   6. 图标已注册：分类与子分组的 icon 必须存在于 src/data/icons.ts，
 *      否则侧栏渲染成空白图标，菜单看着有项实际无图。
 * [约束] 必须 import 生产模块取分类，禁止用正则手抄 component-categories.ts 的结构，
 *   否则源文件写法漂移（引号风格、字段名）会让守卫静默少算却误判通过。
 *
 * [用法] node scripts/check_component_categories.mjs
 * [返回] 退出码 0=通过；1=漂移。输出 CATEGORIES: PASS/FAIL。
 * 最近修改时间：2026-10-17 03:40:00；改动原因：分类真相源升级为两级后守卫需按新结构对账，
 *   补子分组闭合与图标注册判据。
 */

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { COMPONENT_CATEGORY_ORDER } from '../component-library/src/data/component-categories.ts'

const MIN_CATEGORIES = 8
const HERE = path.dirname(fileURLToPath(import.meta.url))
const LIB = path.join(HERE, '..', 'component-library')
const SRC_COMPONENTS = path.join(LIB, 'src', 'components')
const ICONS_FILE = path.join(LIB, 'src', 'data', 'icons.ts')

/** 递归收集磁盘上全部组件文件名（不含 .vue）。 */
function walk(dir, acc = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name)
    if (entry.isDirectory()) walk(p, acc)
    else if (entry.name.endsWith('.vue')) acc.push(entry.name.replace(/\.vue$/, ''))
  }
  return acc
}

/** 读 icons.ts 已注册的图标名集合（顶层两空格缩进的键）。 */
function registeredIcons() {
  const src = fs.readFileSync(ICONS_FILE, 'utf8')
  return new Set([...src.matchAll(/^ {2}([a-zA-Z][a-zA-Z0-9]*):/gm)].map((m) => m[1]))
}

/** 主流程：磁盘全集 vs 两级归类全集双向对账，返回退出码。 */
function main() {
  if (!fs.existsSync(SRC_COMPONENTS)) {
    console.log('CATEGORIES: FAIL（组件目录不存在）')
    return 1
  }
  const disk = new Set(walk(SRC_COMPONENTS))
  const failures = []
  if (COMPONENT_CATEGORY_ORDER.length < MIN_CATEGORIES) {
    failures.push(`父分类数 ${COMPONENT_CATEGORY_ORDER.length} < 下限 ${MIN_CATEGORIES}`)
  }

  const assigned = new Map() // 组件名 -> 出现的「父分类/子分组」列表
  const subKeys = new Map() // 子分组键 -> 出现次数
  const icons = []
  for (const cat of COMPONENT_CATEGORY_ORDER) {
    icons.push(cat.icon)
    if (!cat.subGroups.length) failures.push(`父分类 ${cat.key} 没有子分组`)
    for (const sub of cat.subGroups) {
      icons.push(sub.icon)
      subKeys.set(sub.key, (subKeys.get(sub.key) ?? 0) + 1)
      if (!sub.components.length) failures.push(`子分组 ${cat.key}/${sub.key} 没有组件`)
      for (const name of sub.components) {
        const at = `${cat.key}/${sub.key}`
        if (!assigned.has(name)) assigned.set(name, [])
        assigned.get(name).push(at)
      }
    }
  }

  const dupSub = [...subKeys].filter(([, n]) => n > 1).map(([k]) => k)
  if (dupSub.length) failures.push('子分组键重复: ' + dupSub.join(', '))

  const dup = [...assigned].filter(([, ats]) => ats.length > 1)
  const missing = [...disk].filter((n) => !assigned.has(n)) // 磁盘有、归类无
  const ghost = [...assigned.keys()].filter((n) => !disk.has(n)) // 归类有、磁盘无
  if (dup.length) failures.push('重复归类: ' + dup.map(([n, a]) => `${n}∈${a.join('/')}`).join(', '))
  if (missing.length) failures.push('未归类: ' + missing.sort().join(', '))
  if (ghost.length) failures.push('幽灵组件(归类有磁盘无): ' + ghost.sort().join(', '))

  if (fs.existsSync(ICONS_FILE)) {
    const reg = registeredIcons()
    const bad = [...new Set(icons)].filter((i) => !reg.has(i))
    if (bad.length) failures.push('未注册图标: ' + bad.join(', '))
  }

  if (failures.length) {
    console.log('CATEGORIES: FAIL')
    for (const f of failures) console.log('  -', f)
    console.log(`  父分类=${COMPONENT_CATEGORY_ORDER.length} 子分组=${subKeys.size} 磁盘=${disk.size} 已归类=${assigned.size}`)
    return 1
  }

  const counts = COMPONENT_CATEGORY_ORDER.map((c) => `${c.key}=${c.subGroups.length}组/${c.subGroups.reduce((s, g) => s + g.components.length, 0)}件`).join(' · ')
  const total = [...assigned.keys()].length
  console.log(`CATEGORIES: PASS（${COMPONENT_CATEGORY_ORDER.length} 个父分类、${subKeys.size} 个子分组，覆盖 ${total} 个组件；磁盘 ${disk.size}）`)
  console.log('  分布: ' + counts)
  return 0
}

process.exit(main())
