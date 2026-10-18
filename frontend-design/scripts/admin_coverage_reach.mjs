#!/usr/bin/env node
/**
 * 后台可达图的遍历侧：从入口集合出发，按真实模块引用边求组件可达闭包。
 *
 * [判据] 边必须同时满足「静态 import / 动态 import 命中该文件」与「导入的本地名在该文件里真的被使用」；
 *   只导入不渲染不算用上，避免一行批量导入刷满覆盖率。
 *
 * [边界] 路径解析、barrel 通道与通配展开由图访问器提供，本文件只编排遍历。
 * 最近修改时间：2026-10-16 20:12:00；改动原因：从可达图工厂中下沉遍历体，使各函数满足行数基准。
 */

import { DYNAMIC_RE, GLOB_RE, IMPORT_RE, parseClause, usedIdentifiers } from './admin_coverage_parse.mjs'

/**
 * 展开一个文件里的 `import.meta.glob` 边。
 *
 * [参数] graph：图访问器；{ rel, raw, isComponent, reached, queue }：当前文件与其遍历状态
 * [返回] 无；命中的组件计入 reached，下钻对象压入 queue
 * 最近修改时间：2026-10-16 20:12:00；改动原因：从可达图工厂中下沉遍历体。
 */
function expandGlobEdges(graph, { rel, raw, isComponent, reached, queue }) {
  // 1. 通配匹配目录下的组件全部计入，并各自继续下钻
  for (const m of raw.matchAll(GLOB_RE)) {
    for (const f of graph.globTargets({ spec: m[1], fromRel: rel })) {
      if (isComponent(f)) reached.add(f)
      queue.push(f)
    }
  }
}

/**
 * 展开一个文件里的静态 import 边。
 *
 * [参数] graph：图访问器；{ rel, raw, used, isComponent, reached, queue }：当前文件、已使用标识符与遍历状态
 * [返回] 无；成立的边计入 reached，下钻对象压入 queue
 * 最近修改时间：2026-10-16 20:12:00；改动原因：从可达图工厂中下沉遍历体。
 */
function expandImportEdges(graph, { rel, raw, used, isComponent, reached, queue }) {
  // 1. 收集本轮真正用到的解析目标，未用到的导入不得进入可达集合
  const touched = new Set()
  for (const m of raw.matchAll(IMPORT_RE)) {
    const target = graph.resolve({ spec: m[2], fromRel: rel })
    if (!target) continue
    // 2. 只保留「导入的本地名真的被使用」的边，必要时沿 barrel 追最终落点
    for (const { local, imported } of parseClause(m[1])) {
      if (!used.has(local)) continue
      const finalFile = target.endsWith('.ts') ? graph.followBarrel({ file: target, name: imported }) : target
      if (finalFile && isComponent(finalFile)) reached.add(finalFile)
      if (finalFile) queue.push(finalFile)
      touched.add(target)
    }
  }
  // 3. 用过的非组件本地模块同样要继续下钻，否则间接引用会断链
  for (const target of touched) queue.push(target)
}

/**
 * 展开一个文件里的动态 import 边。
 *
 * [参数] graph：图访问器；{ rel, raw, isComponent, reached, queue }：当前文件与遍历状态
 * [返回] 无；懒加载命中的组件计入 reached
 * 最近修改时间：2026-10-16 20:12:00；改动原因：从可达图工厂中下沉遍历体。
 */
function expandDynamicEdges(graph, { rel, raw, isComponent, reached, queue }) {
  // 1. 懒加载入口同样构成可达证据
  for (const m of raw.matchAll(DYNAMIC_RE)) {
    const target = graph.resolve({ spec: m[1], fromRel: rel })
    if (!target) continue
    if (isComponent(target)) reached.add(target)
    queue.push(target)
  }
}

/**
 * 从入口集合出发求可达闭包。
 *
 * [参数] graph：图访问器；entries：入口相对路径数组；isComponent：判定某相对路径是否属于组件全集
 * [返回] Set<string> 被真实引用到的组件相对路径集合
 * 最近修改时间：2026-10-16 20:12:00；改动原因：从可达图工厂中下沉遍历体。
 */
export function reach(graph, entries, isComponent) {
  // 1. 初始化队列、已访问集与命中集合
  const reached = new Set()
  const queue = [...entries]
  const seen = new Set()
  while (queue.length) {
    const rel = queue.pop()
    if (seen.has(rel)) continue
    seen.add(rel)
    if (isComponent(rel)) reached.add(rel)

    // 2. 读正文并算出「真的被使用」的标识符集合
    let raw
    try {
      raw = graph.readText(rel)
    } catch {
      continue
    }
    const used = usedIdentifiers(raw)
    const state = { rel, raw, used, isComponent, reached, queue }

    // 3. 三类引用边依次展开
    expandGlobEdges(graph, state)
    expandImportEdges(graph, state)
    expandDynamicEdges(graph, state)
  }
  return reached
}
