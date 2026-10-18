#!/usr/bin/env node
/**
 * 后台组件覆盖率守卫：判定组件库全部组件是否真的被管理后台用上。
 *
 * [判据] 当场从磁盘推导，不复用任何手抄清单：
 *   1. 组件全集 = 对 `src/components` 目录递归取全部 vue 文件（与目录索引守卫同一枚举口径）；
 *   2. 后台入口 = `src/views/**` + `src/router/**` + `src/App.vue`（真实路由装配的页面根）；
 *   3. 可达闭包由 admin_coverage_reach.mjs 按真实引用边求得，边的成立条件见该文件头注释；
 *      本文件只负责全集枚举、入口选取与缺口裁决。
 *
 * [约束] 禁止把组件名单硬编码进本脚本：名单来自磁盘遍历，引用关系来自源码解析。
 *
 * [用法] node frontend-design/scripts/check_admin_component_coverage.mjs
 * [返回] 退出码 0=全部覆盖；1=存在未覆盖组件或入口缺失。输出 ADMIN_COVERAGE: PASS/FAIL。
 * 最近修改时间：2026-10-16 20:12:00；改动原因：遍历侧再拆出 admin_coverage_reach.mjs，本文件只做枚举与裁决。
 */

import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'
import { createModuleGraph } from './admin_coverage_graph.mjs'
import { reach } from './admin_coverage_reach.mjs'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const LIB = path.join(HERE, '..', 'component-library')
const SRC = path.join(LIB, 'src')

const graph = createModuleGraph(LIB, { '@': SRC })
const COMPONENTS = path.join(SRC, 'components')

/**
 * 后台入口集合：真实路由装配的页面根。
 *
 * [参数] None
 * [返回] string[] 相对 LIB 的入口文件路径
 * 最近修改时间：2026-10-16 19:58:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function collectEntries() {
  // 1. 三类根：路由装配的页面、路由声明本身、应用外壳入口
  return [
    ...graph.walk(path.join(SRC, 'views'), (p) => p.endsWith('.vue')),
    ...graph.walk(path.join(SRC, 'router'), (p) => /\.(vue|ts)$/.test(p)),
    'src/App.vue',
  ].filter((f) => fs.existsSync(path.join(LIB, f)))
}

/**
 * 主流程：磁盘组件全集 ∩ 后台入口可达闭包 → 覆盖率裁决。
 *
 * [参数] None
 * [返回] number 退出码；0 表示全部可达
 * 最近修改时间：2026-10-16 19:58:00；改动原因：随守卫拆分迁移，判定口径不变。
 */
function main() {
  // 1. 组件目录缺失属于环境异常，直接失败并给出原因
  if (!fs.existsSync(COMPONENTS)) {
    console.log('ADMIN_COVERAGE: FAIL（组件目录不存在）')
    return 1
  }
  // 2. 当场枚举磁盘组件全集，不接受任何硬编码名单
  const allComponents = new Set(graph.walk(COMPONENTS, (p) => p.endsWith('.vue')))
  if (!allComponents.size) {
    console.log('ADMIN_COVERAGE: FAIL（磁盘未发现任何组件）')
    return 1
  }
  // 3. 后台入口缺失时覆盖率没有意义，直接失败
  const entries = collectEntries()
  if (!entries.length) {
    console.log('ADMIN_COVERAGE: FAIL（后台入口缺失）')
    return 1
  }

  // 4. 沿真实引用边求可达闭包，再与全集做差得到缺口
  const isComponent = (rel) => allComponents.has(rel)
  const reached = reach(graph, entries, isComponent)
  const uncovered = [...allComponents].filter((f) => !reached.has(f)).sort()
  const total = allComponents.size
  const hit = total - uncovered.length

  // 5. 有缺口则逐条列出组件路径并失败；无缺口输出全量覆盖
  if (uncovered.length) {
    console.log(`ADMIN_COVERAGE: FAIL (${hit}/${total} 组件在后台可达，缺口 ${uncovered.length})`)
    for (const f of uncovered) console.log('  -', f)
    return 1
  }
  console.log(`ADMIN_COVERAGE: PASS (${hit}/${total} 组件全部在后台可达)`)
  return 0
}

process.exit(main())
