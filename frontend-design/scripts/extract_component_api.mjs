/**
 * 从 Vue SFC 源码抽取组件公开 API（props / emits / slots / 导出类型）。
 *
 * [用法] 作为模块被 build_component_catalog.mjs 引入，不单独执行。
 * [返回] 每个组件一个 { props, emits, slots, types, description } 描述对象。
 * [约束] AST 节点级的声明读取在 component_api_ast.mjs，本文件只管 SFC 文本切分与装配。
 * 最近修改时间：2026-10-17 02:45:00；改动原因：契约提取器补上双 script 块、defineModel
 *   与类型别名还原后本文件超 200 行基线，按职责拆出 AST 读取器同级文件。
 */

import { createRequire } from 'node:module'
import path from 'node:path'
import fs from 'node:fs'
import { readDefaults, readEmits, readExportedTypes, readModelProps, readProps } from './component_api_ast.mjs'

const require = createRequire(import.meta.url)

/** 加载组件库自带的 TypeScript 编译器（版本随组件库依赖，不额外安装）。 */
export function loadTs(libDir) {
  return require(path.join(libDir, 'node_modules', 'typescript'))
}

/**
 * 从 SFC 原文里剥出 script 与 template 两段。
 *
 * 双 script 块组件（普通块导出类型 + `<script setup>` 写 defineProps）必须取 setup 块做 API 抽取，
 * 只取第一个块会漏掉全部 props；说明与导出类型仍按全部块拼接取，两类信息都可能写在普通块里。
 */
function splitSfc(raw) {
  const blocks = [...raw.matchAll(/<script([^>]*)>([\s\S]*?)<\/script>/g)].map((m) => ({ attrs: m[1], body: m[2] }))
  const setupBlock = blocks.find((b) => /\bsetup\b/.test(b.attrs)) ?? blocks[0]
  const template = raw.match(/<template>([\s\S]*)<\/template>/)
  return {
    script: setupBlock ? setupBlock.body : '',
    scriptAll: blocks.map((b) => b.body).join('\n'),
    template: template ? template[1] : '',
  }
}

/** 抽取模板里的具名与默认插槽；$slots 动态透传单独标注。 */
function readSlots(template) {
  const slots = []
  for (const m of template.matchAll(/<slot\b([^>]*)>/g)) {
    const name = /name="([^"]+)"/.exec(m[1])
    slots.push(name ? name[1] : 'default')
  }
  if (/\$slots|useSlots/.test(template)) slots.push('(动态透传)')
  return [...new Set(slots)]
}

/** 取 script 顶部块注释首行作为组件说明；跳过装饰性分隔线，无有效文本时回退为空串。 */
function readDescription(script) {
  const m = script.match(/\/\*+\s*([\s\S]*?)\*\//)
  if (!m) return ''
  const lines = m[1]
    .split('\n')
    .map((l) => l.replace(/^\s*\*?\s*/, '').trim())
    .filter((l) => l && !/^[=\-*_#~]{3,}$/.test(l))
  return lines[0] || ''
}

/**
 * 抽取单个 SFC 文件的公开 API。
 *
 * [参数] ts: TypeScript 模块；file: SFC 绝对路径
 * [返回] { props, emits, slots, types, description }
 */
export function extractApi(ts, file) {
  const raw = fs.readFileSync(file, 'utf8')
  const { script, scriptAll, template } = splitSfc(raw)
  const sf = ts.createSourceFile('api.ts', script, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS)
  const sfAll = ts.createSourceFile('all.ts', scriptAll, ts.ScriptTarget.Latest, true, ts.ScriptKind.TS)
  const defaults = readDefaults(ts, sf)
  const props = readProps(ts, sf).map((p) => ({
    ...p,
    default: Object.prototype.hasOwnProperty.call(defaults, p.name) ? defaults[p.name] : null,
  }))
  /* defineModel 的 prop 名补进 props：已声明同名项时以 defineProps 的类型为准，只补缺 */
  const declared = new Set(props.map((p) => p.name))
  for (const name of readModelProps(ts, sf)) {
    if (!declared.has(name)) props.push({ name, type: 'unknown', optional: true, default: null })
  }
  return {
    props,
    emits: readEmits(ts, sf),
    slots: readSlots(template),
    types: readExportedTypes(ts, sfAll),
    description: readDescription(scriptAll),
  }
}
