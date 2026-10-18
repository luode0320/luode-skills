// ============================================================
// 珍珠玻璃组件库本地 mock：vite dev 中间件，覆盖 /api 全部端点。
// 目的：npm run dev 零后端即可跑通全部页面；数据形状对齐页面真实消费字段。
// 本文件属于本地增量，不属于上游还原基线；上游升级不受影响。
// ============================================================
import { randomUUID } from 'node:crypto'
import { COMPONENT_CATEGORY_ORDER } from '../src/data/component-categories.ts'

/** 统一响应包装 */
function ok(data) {
  return { code: 200, message: '操作成功', data }
}

function fail(code, message) {
  return { code, message, data: null }
}

/** 稳定伪随机：同一种子每次重跑数据一致，方便视觉对照 */
function seeded(seed) {
  let s = seed % 2147483647
  if (s <= 0) s += 2147483646
  return () => {
    s = (s * 16807) % 2147483647
    return (s - 1) / 2147483646
  }
}

const rand = seeded(20261015)
const pick = list => list[Math.floor(rand() * list.length)]
const int = (min, max) => min + Math.floor(rand() * (max - min + 1))

function pad(n) { return String(n).padStart(2, '0') }
function fmtDate(d) {
  return `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`
}
function fmtTime(d) {
  return `${fmtDate(d)} ${pad(d.getHours())}:${pad(d.getMinutes())}:${pad(d.getSeconds())}`
}
function daysAgo(n) {
  const d = new Date()
  d.setDate(d.getDate() - n)
  return d
}

/* ── 种子数据：菜单 / 部门 / 角色 / 用户 / 岗位 / 字典 / 参数 ── */

/* 组件库菜单由单一分类数据源生成两级：父分类作侧栏分组标题，子分组作可点示例页。
   上游 buildNav 只认「顶层节点 → 带 component 的子项」两级，因此父分类必须直接作顶层节点，
   不能再套一层「组件库」目录，否则子项缺 component 会被整组丢弃、示例菜单全部消失。
   菜单表按项目惯例保持扁平存储，父子靠 id/parentId 关联，不在行内嵌 children。
   组件库排在一级菜单首位：登录后 homePath() 取 navGroups[0].items[0].path，
   落地页因此直接进第一个子分组示例页。 */
/* 组件库菜单从 501 起编号，与业务菜单号段（1~41）完全隔离，
   新增菜单走 Math.max(全部 id)+1，不会与组件库号段撞号。 */
let gallerySeq = 500
const galleryMenus = COMPONENT_CATEGORY_ORDER.flatMap((cat, ci) => {
  const dirId = ++gallerySeq
  return [
    {
      id: dirId, parentId: 0, name: cat.label, type: 'dir', icon: cat.icon,
      path: `/gallery/${cat.key}`, sort: ci + 1, visible: 1, status: 1,
    },
    ...cat.subGroups.map((sub, si) => ({
      id: ++gallerySeq, parentId: dirId, name: sub.label, type: 'menu', icon: sub.icon,
      path: `/gallery/${cat.key}/${sub.key}`, component: 'gallery/index', permission: 'gallery:list',
      sort: si + 1, visible: 1, status: 1,
    })),
  ]
})

const menus = [
  ...galleryMenus,
  { id: 1, parentId: 0, name: '工作台', type: 'menu', icon: 'board', path: '/dashboard', component: 'dashboard/index', permission: 'dashboard:view', sort: 11, visible: 1, status: 1 },
  { id: 2, parentId: 0, name: '系统管理', type: 'dir', icon: 'gear', path: '/system', sort: 12, visible: 1, status: 1 },
  { id: 21, parentId: 2, name: '用户管理', type: 'menu', icon: 'user', path: '/system/users', component: 'system/user/index', permission: 'system:user:list', sort: 1, visible: 1, status: 1 },
  { id: 22, parentId: 2, name: '角色管理', type: 'menu', icon: 'shield', path: '/system/roles', component: 'system/role/index', permission: 'system:role:list', sort: 2, visible: 1, status: 1 },
  { id: 23, parentId: 2, name: '菜单管理', type: 'menu', icon: 'menu', path: '/system/menus', component: 'system/menu/index', permission: 'system:menu:list', sort: 3, visible: 1, status: 1 },
  { id: 24, parentId: 2, name: '部门管理', type: 'menu', icon: 'org', path: '/system/depts', component: 'system/dept/index', permission: 'system:dept:list', sort: 4, visible: 1, status: 1 },
  { id: 25, parentId: 2, name: '岗位管理', type: 'menu', icon: 'ladder', path: '/system/posts', component: 'system/post/index', permission: 'system:post:list', sort: 5, visible: 1, status: 1 },
  { id: 26, parentId: 2, name: '字典管理', type: 'menu', icon: 'book', path: '/system/dict', component: 'system/dict/index', permission: 'system:dict:list', sort: 6, visible: 1, status: 1 },
  { id: 27, parentId: 2, name: '参数管理', type: 'menu', icon: 'sliders', path: '/system/configs', component: 'system/config/index', permission: 'system:config:list', sort: 7, visible: 1, status: 1 },
  { id: 3, parentId: 0, name: '日志监控', type: 'dir', icon: 'monitor', path: '/monitor', sort: 13, visible: 1, status: 1 },
  { id: 31, parentId: 3, name: '操作日志', type: 'menu', icon: 'log', path: '/monitor/oper-logs', component: 'monitor/operlog/index', permission: 'monitor:operlog:list', sort: 1, visible: 1, status: 1 },
  { id: 32, parentId: 3, name: '登录日志', type: 'menu', icon: 'key', path: '/monitor/login-logs', component: 'monitor/loginlog/index', permission: 'monitor:loginlog:list', sort: 2, visible: 1, status: 1 },
  { id: 4, parentId: 0, name: '系统工具', type: 'dir', icon: 'tool', path: '/tool', sort: 14, visible: 1, status: 1 },
  { id: 41, parentId: 4, name: '代码生成', type: 'menu', icon: 'code', path: '/tool/generator', component: 'tool/gen/index', permission: 'tool:generator:list', sort: 1, visible: 1, status: 1 },
]

const depts = [
  { id: 1, parentId: 0, name: '总公司', leader: '罗德', phone: '13800000001', email: 'root@example.com', sort: 1, status: 1, memberCount: 42, children: [
    { id: 11, parentId: 1, name: '研发中心', leader: '韩忠宝', phone: '13800000002', email: 'dev@example.com', sort: 1, status: 1, memberCount: 18, children: [
      { id: 111, parentId: 11, name: '前端组', leader: '杨莹', sort: 1, status: 1, memberCount: 6 },
      { id: 112, parentId: 11, name: '后端组', leader: '李红', sort: 2, status: 1, memberCount: 8 },
    ] },
    { id: 12, parentId: 1, name: '市场中心', leader: '王强', sort: 2, status: 1, memberCount: 10 },
    { id: 13, parentId: 1, name: '职能中心', leader: '赵敏', sort: 3, status: 0, memberCount: 14 },
  ] },
]

const roles = [
  { id: 1, name: '超级管理员', code: 'admin', dataScope: 'all', sort: 1, status: 1, builtin: true, userCount: 1, remark: '内置角色，拥有全部权限', menuIds: [1, 2, 21, 22, 23, 24, 25, 26, 27, 3, 31, 32, 4, 41] },
  { id: 2, name: '业务运营', code: 'ops', dataScope: 'dept', sort: 2, status: 1, builtin: false, userCount: 3, remark: '', menuIds: [1, 2, 21, 24, 26, 3, 31, 32] },
  { id: 3, name: '访客', code: 'guest', dataScope: 'self', sort: 3, status: 0, builtin: false, userCount: 0, remark: '只读演示', menuIds: [1, 3, 31] },
]

const users = [
  { id: 1, username: 'admin', nickname: '罗德', phone: '13800000001', email: 'admin@example.com', deptId: 1, deptName: '总公司', postName: '技术负责人', roleName: '超级管理员', roleIds: [1], postIds: [1], status: 1, createTime: '2026-01-01 09:00:00', lastLogin: fmtTime(daysAgo(0)) },
  { id: 2, username: 'hanzhongbao', nickname: '韩忠宝', phone: '13800000002', email: 'han@example.com', deptId: 11, deptName: '研发中心', postName: '后端工程师', roleName: '业务运营', roleIds: [2], postIds: [2], status: 1, createTime: '2026-02-14 10:30:00', lastLogin: fmtTime(daysAgo(1)) },
  { id: 3, username: 'yangying', nickname: '杨莹', phone: '13800000003', email: 'yang@example.com', deptId: 111, deptName: '前端组', postName: '前端工程师', roleName: '业务运营', roleIds: [2], postIds: [3], status: 1, createTime: '2026-03-02 14:00:00', lastLogin: fmtTime(daysAgo(2)) },
  { id: 4, username: 'lihong', nickname: '李红', phone: '13800000004', email: 'li@example.com', deptId: 112, deptName: '后端组', postName: '测试工程师', roleName: '访客', roleIds: [3], postIds: [4], status: 0, createTime: '2026-04-11 16:20:00', lastLogin: fmtTime(daysAgo(9)) },
  { id: 5, username: 'wangqiang', nickname: '王强', phone: '13800000005', email: 'wang@example.com', deptId: 12, deptName: '市场中心', postName: '运营专员', roleName: '业务运营', roleIds: [2], postIds: [5], status: 1, createTime: '2026-05-20 11:05:00', lastLogin: fmtTime(daysAgo(3)) },
  { id: 6, username: 'zhaomin', nickname: '赵敏', phone: '13800000006', email: 'zhao@example.com', deptId: 13, deptName: '职能中心', postName: '行政专员', roleName: '访客', roleIds: [3], postIds: [6], status: 1, createTime: '2026-06-08 09:45:00', lastLogin: fmtTime(daysAgo(15)) },
]

const posts = [
  { id: 1, postCode: 'CTO', postName: '技术负责人', sort: 1, status: 1, remark: '' },
  { id: 2, postCode: 'BE', postName: '后端工程师', sort: 2, status: 1, remark: '' },
  { id: 3, postCode: 'FE', postName: '前端工程师', sort: 3, status: 1, remark: '' },
  { id: 4, postCode: 'QA', postName: '测试工程师', sort: 4, status: 1, remark: '' },
  { id: 5, postCode: 'OPS', postName: '运营专员', sort: 5, status: 0, remark: '停用演示' },
]

const dictTypes = [
  { id: 1, dictName: '系统状态', dictType: 'sys_status', status: 1, remark: '通用启用/停用', builtin: true },
  { id: 2, dictName: '通知类型', dictType: 'notice_type', status: 1, remark: '', builtin: false },
  { id: 3, dictName: '操作模块', dictType: 'oper_module', status: 1, remark: '', builtin: false },
]

const dictData = [
  { id: 1, dictType: 'sys_status', label: '正常', value: '1', sort: 1, status: 1, tone: 'success', def: true, remark: '' },
  { id: 2, dictType: 'sys_status', label: '停用', value: '0', sort: 2, status: 1, tone: 'danger', def: false, remark: '' },
  { id: 3, dictType: 'sys_status', label: '草稿', value: '2', sort: 3, status: 1, tone: 'info', def: false, remark: '' },
  { id: 4, dictType: 'notice_type', label: '公告', value: '1', sort: 1, status: 1, tone: 'cat-2', def: true, remark: '' },
  { id: 5, dictType: 'notice_type', label: '升级', value: '2', sort: 2, status: 1, tone: 'cat-3', def: false, remark: '' },
  { id: 6, dictType: 'notice_type', label: '安全', value: '3', sort: 3, status: 1, tone: 'cat-4', def: false, remark: '' },
  { id: 7, dictType: 'oper_module', label: '用户管理', value: 'system:user', sort: 1, status: 1, tone: 'cat-1', def: false, remark: '' },
  { id: 8, dictType: 'oper_module', label: '角色管理', value: 'system:role', sort: 2, status: 1, tone: 'cat-5', def: true, remark: '' },
]

const configs = [
  { id: 1, name: '账号初始密码', key: 'sys.user.initPassword', value: '123456', type: 'N', builtin: true, remark: '新用户默认密码' },
  { id: 2, name: '注册开关', key: 'sys.account.register', value: 'false', type: 'Y', builtin: true, remark: '是否允许自注册' },
  { id: 3, name: '会话超时（分钟）', key: 'sys.session.timeout', value: '30', type: 'N', builtin: false, remark: '' },
  { id: 4, name: '皮肤主题', key: 'sys.ui.theme', value: 'pearl', type: 'N', builtin: false, remark: '界面主题标识' },
]

/* ── 日志类：固定条数、稳定伪随机，页面全链路可看 ── */

const MODULES = ['用户管理', '角色管理', '部门管理', '字典管理', '代码生成']
const ACTIONS = ['新增', '修改', '删除', '查询', '导出']
const BROWSERS = ['Chrome 131', 'Edge 130', 'Firefox 133', 'Safari 18']
const OSES = ['Windows 11', 'macOS 15', 'Ubuntu 24.04']
const IPS = ['10.20.30.41', '10.20.30.42', '172.16.8.9', '192.168.1.100', '203.0.113.7']

function buildOperLogs(n) {
  const rows = []
  for (let i = 1; i <= n; i++) {
    const cost = int(30, 900)
    const failed = rand() < 0.12
    const operName = pick(['罗德', '韩忠宝', '杨莹', '王强'])
    rows.push({
      id: i,
      module: pick(MODULES),
      action: pick(ACTIONS),
      operName,
      operUser: operName,
      method: pick(['POST', 'PUT', 'GET', 'DELETE']),
      url: `/api/system/${pick(['users', 'roles', 'depts', 'dicts'])}`,
      ip: pick(IPS),
      location: pick(['内网', '上海市', '北京市', '广州市']),
      browser: pick(BROWSERS),
      os: pick(OSES),
      cost,
      result: failed ? 0 : 1,
      msg: failed ? pick(['字段校验失败', '目标不存在', '权限不足']) : '操作成功',
      operTime: fmtTime(daysAgo(Math.floor(i / 6))),
    })
  }
  return rows
}

function buildLoginLogs(n) {
  const rows = []
  for (let i = 1; i <= n; i++) {
    const failed = rand() < 0.15
    rows.push({
      id: i,
      username: pick(['admin', 'hanzhongbao', 'yangying', 'wangqiang', 'unknown_' + int(1, 3)]),
      ip: pick(IPS),
      location: pick(['内网', '上海市', '北京市', '境外']),
      browser: pick(BROWSERS),
      os: pick(OSES),
      status: failed ? 0 : 1,
      result: failed ? 0 : 1,
      msg: failed ? '密码错误' : '登录成功',
      loginTime: fmtTime(daysAgo(Math.floor(i / 5))),
    })
  }
  return rows
}

const operLogs = buildOperLogs(72)
const loginLogs = buildLoginLogs(60)

const generatorTables = [
  { id: 1, tableName: 'sys_user', tableComment: '用户信息', synced: true, createTime: fmtDate(daysAgo(30)) },
  { id: 2, tableName: 'sys_role', tableComment: '角色信息', synced: true, createTime: fmtDate(daysAgo(29)) },
  { id: 3, tableName: 'sys_dict_type', tableComment: '字典类型', synced: false, createTime: fmtDate(daysAgo(20)) },
  { id: 4, tableName: 'biz_order', tableComment: '业务订单', synced: false, createTime: fmtDate(daysAgo(8)) },
]

function generatorColumns(tableId) {
  const table = generatorTables.find(t => t.id === tableId)
  const base = [
    { name: 'id', type: 'bigint', comment: '主键', pk: true },
    { name: 'create_time', type: 'datetime', comment: '创建时间', pk: false },
  ]
  const extra = table && table.tableName === 'sys_user'
    ? [{ name: 'username', type: 'varchar(64)', comment: '登录账号', pk: false }, { name: 'nickname', type: 'varchar(64)', comment: '昵称', pk: false }]
    : [{ name: 'name', type: 'varchar(128)', comment: '名称', pk: false }]
  return [...base, ...extra]
}

function generatorPreview(tableId) {
  const table = generatorTables.find(t => t.id === tableId)
  const name = table ? table.tableName : 'unknown'
  const files = [
    { name: `${name}.entity.ts`, path: `src/entity/${name}.ts`, code: `export interface ${name} {\n  id: number\n}` },
    { name: `${name}.mapper.ts`, path: `src/mapper/${name}.ts`, code: `// mapper for ${name}` },
    { name: `${name}.service.ts`, path: `src/service/${name}.ts`, code: `// service for ${name}` },
  ]
  return { files, activeFile: files[0].name, code: files[0].code }
}

/* ── 统计聚合（对应 OperLogStats / LoginLogStats / 泳道 / 热力） ── */

function statsOf(rows, range) {
  const total = rows.length
  const failed = rows.filter(r => (r.status !== undefined ? r.status === 0 : r.result === 0)).length
  const buckets = []
  if (range === '24h') {
    for (let h = 0; h < 24; h++) {
      buckets.push({ bucket: `${pad(h)}:00`, total: int(2, 18), failed: int(0, 3) })
    }
  } else {
    const days = range === '7d' ? 7 : 30
    for (let d = days - 1; d >= 0; d--) {
      buckets.push({ bucket: fmtDate(daysAgo(d)), total: int(6, 40), failed: int(0, 5) })
    }
  }
  return { total, failed, buckets }
}

function buildTimeline() {
  const now = new Date()
  const nowSec = now.getHours() * 3600 + now.getMinutes() * 60 + now.getSeconds()
  const lanes = MODULES.map(module => {
    const blocks = []
    for (let b = 0; b < 6; b++) {
      const startSec = int(6, 14) * 3600 + int(0, 55) * 60
      const len = int(3, 25) * 60
      const failed = rand() < 0.1 ? 1 : 0
      blocks.push({ startSec, endSec: startSec + len, count: int(1, 9), failed, maxCost: int(60, 1200), ids: [int(1, 70)] })
    }
    blocks.sort((a, b) => a.startSec - b.startSec)
    return { module, count: blocks.reduce((s, x) => s + x.count, 0), blocks }
  })
  return { date: fmtDate(now), nowSec, lanes }
}

function buildHeatmap(days) {
  const cells = []
  for (let dow = 0; dow < 7; dow++) {
    for (let hour = 0; hour < 24; hour++) {
      const peak = hour >= 9 && hour <= 18 ? 3 : 1
      cells.push({ dow, hour, total: int(1, 6) * peak, failed: rand() < 0.08 ? int(1, 4) : 0 })
    }
  }
  const anomalies = [
    { kind: 'ip', key: '203.0.113.7', failed: 14, total: 16, spread: 3, firstTime: fmtTime(daysAgo(2)), lastTime: fmtTime(daysAgo(0)) },
    { kind: 'user', key: 'unknown_2', failed: 9, total: 9, spread: 2, firstTime: fmtTime(daysAgo(1)), lastTime: fmtTime(daysAgo(0)) },
  ]
  return { days, since: fmtDate(daysAgo(days)), threshold: 8, cells, anomalies }
}

/* ── 工作台概览（DashboardSummary 形状） ── */

function buildDashboard() {
  const trend = []
  for (let i = 0; i < 14; i++) trend.push(int(20, 90))
  const trendTotal = trend.reduce((a, b) => a + b, 0)
  const trendPrev = Math.round(trendTotal * (0.8 + rand() * 0.3))
  return {
    stats: [
      { label: '今日登录', value: int(30, 80), delta: 12.5, unit: '次' },
      { label: '今日操作', value: int(180, 400), delta: -4.2, unit: '次' },
      { label: '活跃账号', value: int(10, 30), delta: 6.0, unit: '人' },
      { label: '成功率', value: 97.8, delta: 0.3, unit: '%' },
    ],
    trend,
    trendTotal,
    trendPrev,
    successRate: 97.8,
    roleDist: [
      { label: '超级管理员', value: 1 },
      { label: '业务运营', value: 3 },
      { label: '访客', value: 2 },
    ],
    activities: loginLogs.slice(0, 8).map(r => ({ who: r.username, target: r.msg, time: r.loginTime, tint: r.result === 1 ? 'danger' : 'ok' })),
    dailyOps: Array.from({ length: 7 }, (_, i) => ({ date: fmtDate(daysAgo(6 - i)), total: int(150, 400), failed: int(0, 12) })),
  }
}

/* ── 令牌态：mock 固定一个有效 token 与权限全集 ── */

const TOKENS = new Set()
const ALL_PERMISSIONS = Array.from(new Set([
  'dashboard:view',
  ...menus.filter(m => m.permission).map(m => m.permission),
])).concat(['system:user:create', 'system:user:update', 'system:user:remove'])

/* ── 路由树（RoutesResponse：与 /auth/routes 契约一致） ── */

function buildRoutes() {
  const roots = menus.filter(m => m.parentId === 0).sort((a, b) => a.sort - b.sort)
  return roots.map(root => {
    const children = menus.filter(m => m.parentId === root.id).sort((a, b) => a.sort - b.sort)
    if (root.type === 'menu' || children.length === 0) {
      return { id: root.id, parentId: 0, name: root.name, path: root.path, component: root.component, icon: root.icon, permission: root.permission }
    }
    return {
      id: root.id, parentId: 0, name: root.name, path: root.path, icon: root.icon,
      children: children.map(c => ({ id: c.id, parentId: root.id, name: c.name, path: c.path, component: c.component, icon: c.icon, permission: c.permission })),
    }
  })
}

/* ── CRUD 通用实现 ── */

function paginate(rows, query) {
  const pageNum = Number(query.pageNum ?? 1)
  const pageSize = Number(query.pageSize ?? 10)
  const start = (pageNum - 1) * pageSize
  return { pageNum, pageSize, total: rows.length, rows: rows.slice(start, start + pageSize) }
}

/** 从 query/body 中取名称类模糊过滤 */
function matchKeyword(row, query, fields) {
  const kw = String(query.keyword ?? '').trim().toLowerCase()
  if (!kw) return true
  return fields.some(f => String(row[f] ?? '').toLowerCase().includes(kw))
}

/* ── 路由匹配与处理器 ── */

const handlers = []
function route(method, pattern, handler) {
  // pattern 例：'/system/users/:id'；编译为正则并记录参数名
  const names = []
  const regex = new RegExp('^' + pattern.replace(/:[a-zA-Z]+/g, (m) => {
    names.push(m.slice(1))
    return '([^/]+)'
  }) + '$')
  handlers.push({ method, regex, names, handler })
}

// —— 认证 ——
route('GET', '/api/auth/captcha', () => ok({ uuid: randomUUID(), code: '1024' }))
route('POST', '/api/auth/login', (ctx) => {
  const token = 'mock-' + randomUUID()
  TOKENS.add(token)
  return ok({ token, expiresIn: 7200 })
})
route('GET', '/api/auth/me', (ctx) => {
  const user = users[0]
  return ok({ id: user.id, username: user.username, nickname: user.nickname, deptId: 1, deptName: '总公司', roles: ['admin'], permissions: ALL_PERMISSIONS })
})
route('GET', '/api/auth/routes', () => ok({ routes: buildRoutes() }))
route('PUT', '/api/auth/password', () => ok(null))
route('POST', '/api/auth/logout', (ctx) => { TOKENS.delete(ctx.token); return ok(null) })

// —— 用户 ——
route('GET', '/api/system/users', (ctx) => {
  const kw = ctx.query
  const filtered = users.filter(u => matchKeyword(u, kw, ['username', 'nickname', 'phone', 'deptName']))
  const status = kw.status
  const finalRows = status !== undefined && status !== '' ? filtered.filter(u => String(u.status) === String(status)) : filtered
  return ok(paginate(finalRows, kw))
})
route('GET', '/api/system/users/options', () => ok({
  depts: JSON.parse(JSON.stringify(depts)),
  roles: roles.map(r => ({ id: r.id, name: r.name })),
  posts: posts.map(p => ({ id: p.id, name: p.postName })),
  initPassword: '123456',
}))
route('POST', '/api/system/users', (ctx) => {
  const body = ctx.body || {}
  const id = Math.max(...users.map(u => u.id)) + 1
  const roleRefs = (body.roleIds || []).map(rid => roles.find(r => r.id === rid)?.name).filter(Boolean).join('、')
  const dept = findDept(body.deptId)
  users.push({ id, username: body.username ?? `user${id}`, nickname: body.nickname ?? body.username ?? `用户${id}`, phone: body.phone ?? '', email: body.email ?? '', deptId: body.deptId ?? 1, deptName: dept?.name ?? '总公司', postName: '未分配', roleName: roleRefs || '访客', roleIds: body.roleIds ?? [], postIds: body.postIds ?? [], status: body.status ?? 1, createTime: fmtTime(new Date()), lastLogin: '' })
  return ok({ id })
})
route('PUT', '/api/system/users/:id', (ctx) => {
  const row = users.find(u => u.id === Number(ctx.params.id))
  if (!row) return fail(404, '用户不存在')
  const body = ctx.body || {}
  Object.assign(row, {
    nickname: body.nickname ?? row.nickname,
    phone: body.phone ?? row.phone,
    email: body.email ?? row.email,
    deptId: body.deptId ?? row.deptId,
    status: body.status ?? row.status,
  })
  const dept = findDept(row.deptId)
  if (dept) row.deptName = dept.name
  return ok(null)
})
route('DELETE', '/api/system/users/:id', (ctx) => {
  const idx = users.findIndex(u => u.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '用户不存在')
  users.splice(idx, 1)
  return ok(null)
})
route('PUT', '/api/system/users/:id/status', (ctx) => {
  const row = users.find(u => u.id === Number(ctx.params.id))
  if (!row) return fail(404, '用户不存在')
  row.status = ctx.body?.status ?? row.status
  return ok(null)
})
route('PUT', '/api/system/users/:id/password', () => ok(null))

// —— 角色 ——
route('GET', '/api/system/roles', (ctx) => ok(paginate(roles.filter(r => matchKeyword(r, ctx.query, ['name', 'code'])), ctx.query)))
route('POST', '/api/system/roles', (ctx) => {
  const id = Math.max(...roles.map(r => r.id)) + 1
  roles.push({ id, name: ctx.body?.name ?? `角色${id}`, code: ctx.body?.code ?? `role${id}`, dataScope: ctx.body?.dataScope ?? 'self', sort: id, status: ctx.body?.status ?? 1, builtin: false, userCount: 0, remark: ctx.body?.remark ?? '', menuIds: ctx.body?.menuIds ?? [] })
  return ok({ id })
})
route('PUT', '/api/system/roles/:id', (ctx) => {
  const row = roles.find(r => r.id === Number(ctx.params.id))
  if (!row) return fail(404, '角色不存在')
  if (row.builtin) return fail(400, '内置角色只读')
  Object.assign(row, { name: ctx.body?.name ?? row.name, code: ctx.body?.code ?? row.code, dataScope: ctx.body?.dataScope ?? row.dataScope, status: ctx.body?.status ?? row.status, remark: ctx.body?.remark ?? row.remark, menuIds: ctx.body?.menuIds ?? row.menuIds })
  return ok(null)
})
route('DELETE', '/api/system/roles/:id', (ctx) => {
  const idx = roles.findIndex(r => r.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '角色不存在')
  if (roles[idx].builtin) return fail(400, '内置角色只读')
  roles.splice(idx, 1)
  return ok(null)
})
route('GET', '/api/system/roles/:id/menus', (ctx) => {
  const row = roles.find(r => r.id === Number(ctx.params.id))
  if (!row) return fail(404, '角色不存在')
  return ok({ menuIds: row.menuIds })
})
route('GET', '/api/system/permissions/graph', () => ok({
  users: users.map(u => ({ id: u.id, username: u.username, nickname: u.nickname, deptName: u.deptName, status: u.status })),
  roles: roles.map(r => ({ id: r.id, name: r.name, code: r.code, dataScope: r.dataScope, status: r.status, builtin: r.builtin, userCount: r.userCount, menuIds: r.menuIds })),
  menus: menus.map(m => ({ id: m.id, parentId: m.parentId, name: m.name, type: m.type, icon: m.icon ?? null, path: m.path ?? null, permission: m.permission ?? null, sort: m.sort, visible: m.visible, status: m.status })),
  userRoles: users.flatMap(u => (u.roleIds || []).map(rid => [u.id, rid])),
  usersVisible: true,
}))

// —— 菜单 / 部门 ——
route('GET', '/api/system/menus/tree', () => ok(JSON.parse(JSON.stringify(buildMenuTree()))))
route('POST', '/api/system/menus', (ctx) => {
  const id = Math.max(...menus.map(m => m.id)) + 1
  menus.push({ id, parentId: ctx.body?.parentId ?? 0, name: ctx.body?.name ?? `菜单${id}`, type: ctx.body?.type ?? 'menu', icon: ctx.body?.icon ?? null, path: ctx.body?.path ?? '', component: ctx.body?.component ?? '', permission: ctx.body?.permission ?? '', sort: ctx.body?.sort ?? id, visible: ctx.body?.visible ?? 1, status: ctx.body?.status ?? 1 })
  return ok({ id })
})
route('PUT', '/api/system/menus/:id', (ctx) => {
  const row = menus.find(m => m.id === Number(ctx.params.id))
  if (!row) return fail(404, '菜单不存在')
  Object.assign(row, { name: ctx.body?.name ?? row.name, path: ctx.body?.path ?? row.path, permission: ctx.body?.permission ?? row.permission, sort: ctx.body?.sort ?? row.sort, visible: ctx.body?.visible ?? row.visible, status: ctx.body?.status ?? row.status })
  return ok(null)
})
route('DELETE', '/api/system/menus/:id', (ctx) => {
  const idx = menus.findIndex(m => m.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '菜单不存在')
  menus.splice(idx, 1)
  return ok(null)
})
route('GET', '/api/system/depts/tree', () => ok(JSON.parse(JSON.stringify(depts))))
route('POST', '/api/system/depts', (ctx) => {
  const id = Math.max(999, ...depts.flatMap(flattenDept).map(d => d.id)) + 1
  const parent = findDept(ctx.body?.parentId)
  const node = { id, parentId: ctx.body?.parentId ?? 0, name: ctx.body?.name ?? `部门${id}`, leader: ctx.body?.leader ?? '', phone: ctx.body?.phone ?? '', email: ctx.body?.email ?? '', sort: ctx.body?.sort ?? id, status: ctx.body?.status ?? 1, memberCount: 0 }
  if (parent) (parent.children = parent.children || []).push(node)
  else depts.push(node)
  return ok({ id })
})
route('PUT', '/api/system/depts/:id', (ctx) => {
  const row = flattenDept().find(d => d.id === Number(ctx.params.id))
  if (!row) return fail(404, '部门不存在')
  Object.assign(row, { name: ctx.body?.name ?? row.name, leader: ctx.body?.leader ?? row.leader, phone: ctx.body?.phone ?? row.phone, email: ctx.body?.email ?? row.email, status: ctx.body?.status ?? row.status })
  return ok(null)
})
route('DELETE', '/api/system/depts/:id', (ctx) => {
  const id = Number(ctx.params.id)
  const parent = flattenDept().find(d => (d.children || []).some(c => c.id === id)) || null
  const list = parent ? parent.children : depts
  const idx = list.findIndex(d => d.id === id)
  if (idx < 0) return fail(404, '部门不存在')
  list.splice(idx, 1)
  return ok(null)
})

// —— 岗位 / 字典 / 参数 ——
route('GET', '/api/system/posts', (ctx) => ok(paginate(posts.filter(p => matchKeyword(p, ctx.query, ['postName', 'postCode'])), ctx.query)))
route('POST', '/api/system/posts', (ctx) => {
  const id = Math.max(...posts.map(p => p.id)) + 1
  posts.push({ id, postCode: ctx.body?.postCode ?? `P${id}`, postName: ctx.body?.postName ?? `岗位${id}`, sort: ctx.body?.sort ?? id, status: ctx.body?.status ?? 1, remark: ctx.body?.remark ?? '' })
  return ok({ id })
})
route('PUT', '/api/system/posts/:id', (ctx) => {
  const row = posts.find(p => p.id === Number(ctx.params.id))
  if (!row) return fail(404, '岗位不存在')
  Object.assign(row, { postCode: ctx.body?.postCode ?? row.postCode, postName: ctx.body?.postName ?? row.postName, sort: ctx.body?.sort ?? row.sort, status: ctx.body?.status ?? row.status, remark: ctx.body?.remark ?? row.remark })
  return ok(null)
})
route('DELETE', '/api/system/posts/:id', (ctx) => {
  const idx = posts.findIndex(p => p.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '岗位不存在')
  posts.splice(idx, 1)
  return ok(null)
})
route('GET', '/api/system/dict/types', (ctx) => ok(paginate(dictTypes.filter(t => matchKeyword(t, ctx.query, ['dictName', 'dictType'])), ctx.query)))
route('POST', '/api/system/dict/types', (ctx) => {
  const id = Math.max(...dictTypes.map(t => t.id)) + 1
  dictTypes.push({ id, dictName: ctx.body?.dictName ?? `字典${id}`, dictType: ctx.body?.dictType ?? `type_${id}`, status: ctx.body?.status ?? 1, remark: ctx.body?.remark ?? '', builtin: false })
  return ok({ id })
})
route('PUT', '/api/system/dict/types/:id', (ctx) => {
  const row = dictTypes.find(t => t.id === Number(ctx.params.id))
  if (!row) return fail(404, '字典类型不存在')
  Object.assign(row, { dictName: ctx.body?.dictName ?? row.dictName, dictType: ctx.body?.dictType ?? row.dictType, status: ctx.body?.status ?? row.status, remark: ctx.body?.remark ?? row.remark })
  return ok(null)
})
route('DELETE', '/api/system/dict/types/:id', (ctx) => {
  const idx = dictTypes.findIndex(t => t.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '字典类型不存在')
  dictTypes.splice(idx, 1)
  return ok(null)
})
route('GET', '/api/system/dict/data/:type', (ctx) => ok(dictData.filter(d => d.dictType === ctx.params.type)))
/* options 必须保留 status / def：上游 useDict 会按 Number(row.status) === 1 过滤并读 row.def，
   只回 label/value/tone 会让前端把全部选项滤空。 */
route('GET', '/api/system/dict/options/:type', (ctx) => ok(dictData.filter(d => d.dictType === ctx.params.type && d.status === 1).map(d => ({ label: d.label, value: d.value, tone: d.tone, status: d.status, def: d.def }))))
route('POST', '/api/system/dict/data', (ctx) => {
  const id = Math.max(...dictData.map(d => d.id)) + 1
  dictData.push({ id, dictType: ctx.body?.dictType ?? '', label: ctx.body?.label ?? `项${id}`, value: ctx.body?.value ?? String(id), sort: ctx.body?.sort ?? id, status: ctx.body?.status ?? 1, tone: ctx.body?.tone ?? 'info', def: Boolean(ctx.body?.def), remark: ctx.body?.remark ?? '' })
  return ok({ id })
})
route('PUT', '/api/system/dict/data/:id', (ctx) => {
  const row = dictData.find(d => d.id === Number(ctx.params.id))
  if (!row) return fail(404, '字典项不存在')
  Object.assign(row, { label: ctx.body?.label ?? row.label, value: ctx.body?.value ?? row.value, sort: ctx.body?.sort ?? row.sort, status: ctx.body?.status ?? row.status, tone: ctx.body?.tone ?? row.tone, def: ctx.body?.def ?? row.def })
  return ok(null)
})
route('DELETE', '/api/system/dict/data/:id', (ctx) => {
  const idx = dictData.findIndex(d => d.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '字典项不存在')
  dictData.splice(idx, 1)
  return ok(null)
})
route('GET', '/api/system/configs', (ctx) => ok(paginate(configs.filter(c => matchKeyword(c, ctx.query, ['name', 'key'])), ctx.query)))
route('POST', '/api/system/configs', (ctx) => {
  const id = Math.max(...configs.map(c => c.id)) + 1
  configs.push({ id, name: ctx.body?.name ?? `参数${id}`, key: ctx.body?.key ?? `sys.param.${id}`, value: ctx.body?.value ?? '', type: ctx.body?.type ?? 'N', builtin: Boolean(ctx.body?.builtin), remark: ctx.body?.remark ?? '' })
  return ok({ id })
})
route('PUT', '/api/system/configs/:id', (ctx) => {
  const row = configs.find(c => c.id === Number(ctx.params.id))
  if (!row) return fail(404, '参数不存在')
  Object.assign(row, { name: ctx.body?.name ?? row.name, value: ctx.body?.value ?? row.value, type: ctx.body?.type ?? row.type, remark: ctx.body?.remark ?? row.remark })
  return ok(null)
})
route('DELETE', '/api/system/configs/:id', (ctx) => {
  const idx = configs.findIndex(c => c.id === Number(ctx.params.id))
  if (idx < 0) return fail(404, '参数不存在')
  configs.splice(idx, 1)
  return ok(null)
})

// —— 监控日志 ——
route('GET', '/api/monitor/oper-logs', (ctx) => ok(paginate(operLogs.filter(r => matchKeyword(r, ctx.query, ['module', 'operName', 'operUser'])), ctx.query)))
route('GET', '/api/monitor/oper-logs/stats', (ctx) => {
  const s = statsOf(operLogs, ctx.query.range ?? '24h')
  const costs = operLogs.map(r => r.cost).sort((a, b) => a - b)
  return ok({ range: ctx.query.range ?? '24h', total: s.total, failed: s.failed, successRate: Number((((s.total - s.failed) / s.total) * 100).toFixed(1)), avgCost: Math.round(costs.reduce((a, b) => a + b, 0) / costs.length), p95Cost: costs[Math.floor(costs.length * 0.95)], activeUsers: 4, series: s.buckets })
})
route('GET', '/api/monitor/oper-logs/timeline', () => ok(buildTimeline()))
route('DELETE', '/api/monitor/oper-logs/:id', (ctx) => {
  const idx = operLogs.findIndex(r => String(r.id) === String(ctx.params.id))
  if (idx >= 0) operLogs.splice(idx, 1)
  return ok(null)
})
route('DELETE', '/api/monitor/oper-logs', () => { operLogs.length = 0; return ok(null) })
route('GET', '/api/monitor/login-logs', (ctx) => ok(paginate(loginLogs.filter(r => matchKeyword(r, ctx.query, ['username', 'ip'])), ctx.query)))
route('GET', '/api/monitor/login-logs/stats', (ctx) => {
  const s = statsOf(loginLogs, ctx.query.range ?? '24h')
  return ok({ range: ctx.query.range ?? '24h', total: s.total, failed: s.failed, successRate: Number((((s.total - s.failed) / s.total) * 100).toFixed(1)), users: new Set(loginLogs.map(r => r.username)).size, ips: new Set(loginLogs.map(r => r.ip)).size, series: s.buckets })
})
route('GET', '/api/monitor/login-logs/heatmap', (ctx) => ok(buildHeatmap(Number(ctx.query.days ?? 7))))
route('DELETE', '/api/monitor/login-logs/:id', (ctx) => {
  const idx = loginLogs.findIndex(r => String(r.id) === String(ctx.params.id))
  if (idx >= 0) loginLogs.splice(idx, 1)
  return ok(null)
})
route('DELETE', '/api/monitor/login-logs', () => { loginLogs.length = 0; return ok(null) })

// —— 代码生成 / 概览 / 健康 ——
route('GET', '/api/tool/generator/tables', (ctx) => ok(paginate(generatorTables, ctx.query)))
route('GET', '/api/tool/generator/importable-tables', () => ok(['biz_coupon', 'biz_ledger', 'biz_settlement']))
route('POST', '/api/tool/generator/import', (ctx) => {
  const names = ctx.body?.tableNames ?? []
  names.forEach((tableName, i) => generatorTables.push({ id: generatorTables.length + 1 + i, tableName, tableComment: tableName, synced: false, createTime: fmtDate(new Date()) }))
  return ok({ imported: names.length })
})
route('GET', '/api/tool/generator/tables/:id/columns', (ctx) => ok(generatorColumns(Number(ctx.params.id))))
route('GET', '/api/tool/generator/tables/:id/preview', (ctx) => ok(generatorPreview(Number(ctx.params.id))))
route('PUT', '/api/tool/generator/tables/:id', (ctx) => {
  const row = generatorTables.find(t => t.id === Number(ctx.params.id))
  if (!row) return fail(404, '表不存在')
  Object.assign(row, { tableComment: ctx.body?.tableComment ?? row.tableComment, synced: ctx.body?.synced ?? row.synced })
  return ok(null)
})
route('POST', '/api/tool/generator/tables/:id/generate', (ctx) => ok({ files: generatorPreview(Number(ctx.params.id)).files.length }))
route('GET', '/api/dashboard/summary', () => ok(buildDashboard()))
route('GET', '/api/health', () => ok({ status: 'UP', time: fmtTime(new Date()) }))

// —— 导出（CSV 下载，全部 list 端点统一） ——
const EXPORT_PATHS = [
  '/api/system/users/export', '/api/system/roles/export', '/api/system/menus/export',
  '/api/system/depts/export', '/api/system/posts/export', '/api/system/dict/types/export',
  '/api/system/configs/export', '/api/monitor/oper-logs/export', '/api/monitor/login-logs/export',
]

function findDept(id) {
  return flattenDept().find(d => d.id === Number(id)) || null
}

function flattenDept(list = depts, out = []) {
  for (const d of list) {
    out.push(d)
    if (d.children) flattenDept(d.children, out)
  }
  return out
}

function buildMenuTree() {
  const roots = menus.filter(m => m.parentId === 0).sort((a, b) => a.sort - b.sort)
  const attach = (node) => {
    const children = menus.filter(m => m.parentId === node.id).sort((a, b) => a.sort - b.sort)
    if (children.length) node.children = children.map(attach)
    return node
  }
  return roots.map(attach)
}

/* ── vite 插件：configureServer 中间件 ── */

export default function pearlMock() {
  return {
    name: 'pearl-glass-mock',
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        const url = new URL(req.url, 'http://localhost')
        const path = url.pathname
        if (!path.startsWith('/api/')) return next()

        // 1. 解析方法与请求体
        const method = (req.method || 'GET').toUpperCase()
        let bodyRaw = ''
        req.on('data', chunk => { bodyRaw += chunk })
        req.on('end', () => {
          let body = null
          if (bodyRaw) {
            try { body = JSON.parse(bodyRaw) } catch { body = null }
          }
          const token = (req.headers.authorization || '').replace(/^Bearer\s+/i, '')
          const params = {}
          const query = Object.fromEntries(url.searchParams)

          // 2. 导出端点返回 CSV；其余匹配处理器返回 JSON
          if (method === 'GET' && EXPORT_PATHS.includes(path)) {
            res.setHeader('Content-Type', 'text/csv; charset=utf-8')
            res.setHeader('Content-Disposition', 'attachment; filename="export.csv"')
            res.end('id,name\n1,示例\n')
            return
          }
          for (const h of handlers) {
            if (h.method !== method) continue
            const m = path.match(h.regex)
            if (!m) continue
            h.names.forEach((name, i) => { params[name] = decodeURIComponent(m[i + 1]) })
            res.setHeader('Content-Type', 'application/json; charset=utf-8')
            res.end(JSON.stringify(h.handler({ body, token, params, query })))
            return
          }
          // 3. 未匹配端点：404 但保持响应形状，页面可见"请求失败"提示而非挂死
          res.statusCode = 404
          res.setHeader('Content-Type', 'application/json; charset=utf-8')
          res.end(JSON.stringify(fail(404, `mock 未实现: ${method} ${path}`)))
        })
      })
    },
  }
}
