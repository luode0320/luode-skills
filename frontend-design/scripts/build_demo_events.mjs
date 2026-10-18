/**
 * 从组件源码的 defineEmits 机械派生「组件 -> 声明事件名」表，供示例层统一接住事件。
 *
 * [用途] 示例层的可回写状态只自动接 `update:<键>`；组件其余事件（close / select / submit / confirm 等）
 *   没人接时，示例卡上的按钮点了完全没有反馈，看起来像坏控件。这张表让装配层能按组件名
 *   一次性把全部声明事件接上，不必逐组件手写处理器。
 * [约束] 生成物禁止手改；改组件 emits 后必须重跑本脚本，`--check` 用于守卫漂移。
 * [用法] node scripts/build_demo_events.mjs [--check]
 * [返回] 退出码 0=已写入或已同步；1=--check 下发现生成物与源码不一致。
 */
import { readFileSync, readdirSync, writeFileSync } from 'node:fs'
import { join, relative } from 'node:path'
import { fileURLToPath } from 'node:url'

const HERE = fileURLToPath(new URL('.', import.meta.url))
const COMPONENTS = join(HERE, '..', 'component-library', 'src', 'components')
const OUT = join(HERE, '..', 'component-library', 'src', 'views', 'gallery', 'demo-events.generated.ts')

/** 从组件源码里取出 defineEmits 声明的事件名（认类型式与数组式两种写法）。 */
function emitsOf(text) {
  const typed = /defineEmits<\{([\s\S]*?)\}>\(\)/.exec(text)
  if (typed) return [...new Set([...typed[1].matchAll(/\(e:\s*'([^']+)'/g)].map((m) => m[1]))].sort()
  const arr = /defineEmits\(\[([\s\S]*?)\]\)/.exec(text)
  if (arr) return [...new Set([...arr[1].matchAll(/'([^']+)'/g)].map((m) => m[1]))].sort()
  return []
}

/** 递归收集 components 下全部 .vue 文件。 */
function walk(dir) {
  const out = []
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, e.name)
    if (e.isDirectory()) out.push(...walk(p))
    else if (e.name.endsWith('.vue')) out.push(p)
  }
  return out
}

/** 渲染生成物正文。 */
function render(table) {
  const lines = [
    '/* 由 scripts/build_demo_events.mjs 从各组件 defineEmits 机械派生，禁止手改；',
    '   重新生成命令：node scripts/build_demo_events.mjs，漂移守卫：加 --check。',
    '   示例层据此把组件声明的每个事件都接上反馈，避免「按钮点了没人接」的空操作示例。 */',
    'export const COMPONENT_EVENTS: Record<string, string[]> = {',
  ]
  for (const name of Object.keys(table).sort()) {
    lines.push(`  ${name}: [${table[name].map((e) => `'${e}'`).join(', ')}],`)
  }
  lines.push('}', '')
  return lines.join('\n')
}

const table = {}
for (const file of walk(COMPONENTS)) {
  const name = file.split(/[\\/]/).pop().replace(/\.vue$/, '')
  const emits = emitsOf(readFileSync(file, 'utf8'))
  if (emits.length) table[name] = emits
}

const body = render(table)
const total = Object.values(table).reduce((n, v) => n + v.length, 0)
if (process.argv.includes('--check')) {
  let current = ''
  try {
    current = readFileSync(OUT, 'utf8')
  } catch {
    current = ''
  }
  if (current !== body) {
    console.log(`DEMO_EVENTS: FAIL (生成物与源码不一致：${Object.keys(table).length} 个组件 ${total} 个事件；重跑 node scripts/build_demo_events.mjs)`)
    process.exit(1)
  }
  console.log(`DEMO_EVENTS: PASS (${Object.keys(table).length} 个组件共 ${total} 个声明事件，生成物已同步)`)
  process.exit(0)
}
writeFileSync(OUT, body, 'utf8')
console.log(`派生事件表 ${Object.keys(table).length} 个组件 / ${total} 个事件`)
console.log(`DEMO_EVENTS_WRITTEN: ${relative(join(HERE, '..'), OUT)}`)
