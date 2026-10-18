/* 核对页样本值可操作化：demoProps 给的是一次性静态字面量，受控组件（TextInput/Switch/Select/Tabs 等）
   绑上去点了不生效——组件回传的新值没人接。这里把每个格子的 props 提升为可回写的响应式状态，
   并按 `update:<已有 prop 键>` 约定自动写回，使核对页上的组件能被真实操作。
   回写键由组件自身已有 props 派生，不另建第二份清单；处理器在 setup 期一次建好，不在渲染期重复构造。
   最近修改时间：2026-10-18 17:55:00；改动原因：只接 `update:<键>` 会漏掉组件其余声明事件——
   Alert / Notification 的关闭按钮、Popconfirm 的确认取消、Form 的提交、Topbar 的整排图标按钮
   在示例卡上点了完全没反应，看起来像坏控件。现按派生事件表把每个声明事件都接上一次可见反馈。 */
import { shallowReactive } from 'vue'
import { pushToast } from '../../composables/toast'
import { COMPONENT_EVENTS } from './demo-events.generated'

/* 少数组件的交互不走 `update:<键>` 而是自定义事件（Steps 用 change 上抛索引），
   按组件名登记事件到状态的写回，让这类点击同样有真实反馈。
   这里的处理器优先级高于通用事件反馈：能落到状态上的就不要退化成一条提示。 */
const EVENT_WRITE_BACK: Record<string, (state: Record<string, unknown>) => Record<string, (value: unknown) => void>> = {
  Steps: (state) => ({ onChange: (index: unknown) => { state.current = index } }),
}

/* 不接通用反馈的事件：它们不由一次离散手势触发，接上会在页面加载或拖拽过程中持续弹提示。
   逐帧 / 逐秒 / 指针移动类事件的可观察结果本来就在组件自身形态上（图形在动、尺寸在变），
   不需要再叠一条提示；`update:<键>` 一律不在这里，它由上面的状态写回接住。 */
const NO_FEEDBACK = new Set([
  'Image.load', 'Image.error',
  'Countdown.change',
  'Upload.progress',
  'RelationGraph.hover',
  'ResizeBox.resize', 'SplitPane.resize',
  'Carousel.change',
])

/* 同格同事件的提示节流窗口（毫秒）：连点或长按不该刷出一串同样的提示 */
const THROTTLE_MS = 1200
const lastFired = new Map<string, number>()

/** 事件名转 Vue 的处理器 prop 名：`row-click` -> `onRowClick`。 */
function handlerKeyOf(event: string): string {
  return 'on' + event.split(/[-:]/).map((s) => s.charAt(0).toUpperCase() + s.slice(1)).join('')
}

/** 把事件首个载荷压成一小段可读文本；非标量只报规模，避免把整张表塞进提示。 */
function briefOf(value: unknown): string {
  if (value === undefined) return ''
  if (typeof value === 'string' || typeof value === 'number' || typeof value === 'boolean') return `：${String(value)}`
  if (Array.isArray(value)) return `：${value.length} 项`
  if (typeof value === 'object' && value !== null) return `：${Object.keys(value).length} 个字段`
  return ''
}

/** 一格可回写的样本状态：state 供渲染读取，handlers 供 v-bind 直接展开 */
export interface LiveProps {
  state: Record<string, unknown>
  handlers: Record<string, (value: unknown) => void>
}

/**
 * 把一格静态样本提升为可回写的受控状态。
 *
 * [参数] name 组件名、source 该格子的静态样本、cellKey 本格唯一键（用于提示节流，缺省按组件名）
 * [返回] LiveProps 可回写的状态与已建好的回写处理器
 * 最近修改时间：2026-10-18 17:55:00；改动原因：补上组件声明事件的通用反馈绑定。
 */
export function createLiveProps(name: string, source: Record<string, unknown>, cellKey = name): LiveProps {
  // 1. 只做顶层响应：深响应会把嵌套 ref 拆包，组件按 `list.rows.value` 读取时会整卡渲染失败
  const state = shallowReactive({ ...source }) as Record<string, unknown>
  const handlers: Record<string, (value: unknown) => void> = {}
  // 2. 按样本已有键逐个建 `onUpdate:<键>` 回写处理器
  for (const key of Object.keys(state)) handlers[`onUpdate:${key}`] = (value: unknown) => { state[key] = value }
  // 3. 再接住组件声明的其余事件：`update:*` 已由状态写回负责，其余事件给一次可见反馈
  for (const event of COMPONENT_EVENTS[name] ?? []) {
    if (event.startsWith('update:') || NO_FEEDBACK.has(`${name}.${event}`)) continue
    const hk = handlerKeyOf(event)
    if (handlers[hk]) continue
    handlers[hk] = (value: unknown) => {
      const now = Date.now()
      const tk = `${cellKey}:${event}`
      if (now - (lastFired.get(tk) ?? 0) < THROTTLE_MS) return
      lastFired.set(tk, now)
      pushToast(`${name} 触发 ${event}${briefOf(value)}`, 'info')
    }
  }
  // 4. 最后补少数组件的自定义事件写回（如 Steps 的 change），能落到状态上的优先于提示
  Object.assign(handlers, EVENT_WRITE_BACK[name]?.(state) ?? {})
  return { state, handlers }
}
