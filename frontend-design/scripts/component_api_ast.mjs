/**
 * 组件 API 抽取的 TypeScript AST 读取器：从 <script setup> 源码里读出 props / emits / 导出类型。
 *
 * [用途] 被 extract_component_api.mjs 引入；单独成文件是因为「按 AST 节点取声明」与
 *   「按文本切分 SFC」是两种职责，合在一起会突破仓库单文件 200 行基线。
 * [约束] 必须保留联合类型的字面量原文（如 'light' | 'stage'），不能归一成 String，
 *   否则下游变体派生器读不到可选项，会把枚举变体静默派生成 0 组。
 * 最近修改时间：2026-10-17 02:40:00；改动原因：契约提取器补上双 script 块、defineModel
 *   与类型别名还原后主文件超行，按职责拆出本文件。
 */

/** 在 AST 中深度查找第一个指定名称的调用表达式。 */
export function findCall(ts, sf, callee) {
  let found = null
  const walk = (node) => {
    if (found) return
    if (ts.isCallExpression(node) && node.expression.getText(sf) === callee) {
      found = node
      return
    }
    ts.forEachChild(node, walk)
  }
  walk(sf)
  return found
}

/** 收集同文件内的类型别名文本（`type X = ...`），用于把 props 上的别名还原成真实类型表达式。 */
function readTypeAliases(ts, sf) {
  const alias = new Map()
  for (const stmt of sf.statements) {
    if (ts.isTypeAliasDeclaration(stmt) && stmt.name && stmt.type) {
      alias.set(stmt.name.getText(sf), stmt.type.getText(sf))
    }
  }
  return alias
}

/** 把 props 的类型表达式做一次别名还原（只展开一层，够覆盖本仓库现有写法）。 */
function resolveTypeText(text, alias) {
  const bare = text.trim()
  return alias.has(bare) ? alias.get(bare) : text
}

/** 抽取 defineProps 的类型成员；withDefaults 包装时向内取第一层实参。 */
export function readProps(ts, sf) {
  let call = findCall(ts, sf, 'defineProps')
  if (!call) return []
  if (call.arguments.length && ts.isTypeLiteralNode(call.arguments[0])) call = call.arguments[0]
  const typeArg = call.typeArguments && call.typeArguments[0]
  if (!typeArg || !typeArg.members) return []
  const alias = readTypeAliases(ts, sf)
  return typeArg.members
    .filter((m) => m.name)
    .map((m) => ({
      name: m.name.getText(sf),
      type: m.type ? resolveTypeText(m.type.getText(sf), alias) : 'unknown',
      optional: Boolean(m.questionToken),
    }))
}

/** 读取 withDefaults 第二参数里的默认值文本（对象字面量属性名 → 初值）。 */
export function readDefaults(ts, sf) {
  const call = findCall(ts, sf, 'withDefaults')
  const defaults = {}
  if (!call || call.arguments.length < 2) return defaults
  const obj = call.arguments[1]
  if (!ts.isObjectLiteralExpression(obj)) return defaults
  for (const prop of obj.properties) {
    if (!prop.name) continue
    defaults[prop.name.getText(sf)] = prop.initializer ? prop.initializer.getText(sf) : '?'
  }
  return defaults
}

/**
 * 抽取 defineModel 声明的 prop 名。
 *
 * `defineModel<T>('name')` 与 `defineModel<T>()`（隐式 modelValue）都生成对外可见的 prop
 * 与 update: 事件，但 defineProps 里并不声明它，只看 defineProps 会让契约索引漏掉这些可传属性。
 */
export function readModelProps(ts, sf) {
  const names = []
  const walk = (node) => {
    if (ts.isCallExpression(node) && node.expression.getText(sf) === 'defineModel') {
      const first = node.arguments[0]
      names.push(first && ts.isStringLiteral(first) ? first.text : 'modelValue')
    }
    ts.forEachChild(node, walk)
  }
  walk(sf)
  return names
}

/** 抽取 defineEmits 声明的事件名与载荷类型，兼容调用签名与元组两种写法。 */
export function readEmits(ts, sf) {
  const call = findCall(ts, sf, 'defineEmits')
  if (!call) return []
  const typeArg = call.typeArguments && call.typeArguments[0]
  if (!typeArg || !typeArg.members) return []
  const events = []
  for (const m of typeArg.members) {
    if (ts.isCallSignatureDeclaration(m) && m.parameters.length) {
      const first = m.parameters[0]
      const literal = first.type && ts.isLiteralTypeNode(first.type) ? first.type.literal : null
      const payload = m.parameters.length > 1 ? m.parameters[1].type.getText(sf) : '—'
      events.push({ name: literal ? literal.getText(sf).replace(/['"]/g, '') : first.type.getText(sf), payload })
    } else if (ts.isPropertySignature(m) && m.name) {
      const type = m.type ? m.type.getText(sf) : '—'
      events.push({ name: m.name.getText(sf), payload: type })
    }
  }
  return events
}

/** 抽取导出的 interface / type 名称，供页面引用（如 DataTable 的 Column）。 */
export function readExportedTypes(ts, sf) {
  const names = []
  for (const stmt of sf.statements) {
    const exported = stmt.modifiers && stmt.modifiers.some((mod) => mod.kind === ts.SyntaxKind.ExportKeyword)
    if (!exported) continue
    if ((ts.isInterfaceDeclaration(stmt) || ts.isTypeAliasDeclaration(stmt)) && stmt.name) names.push(stmt.name.getText(sf))
  }
  return names
}
