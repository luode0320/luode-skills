"""事件接线守卫的探针层：页内量测脚本、豁免面与缺口判定。

[职责] 只回答「在页面里量什么、量到的绑定关系怎么和声明事件对账、哪些事件可以豁免」，
  不含路由派生与全量流程（见同目录 check_demo_event_wiring.py）。
[判据] 取运行时事实：从示例卡内容区的 `__vueParentComponent`（DemoCell 实例）出发递归遍历 vnode 子树，
  收集与卡名同名的组件实例，读它 vnode 上真实绑定的 `on*` 处理器，再与派生事件表里
  defineEmits 声明的事件名对账。走 vnode 而不是扫 DOM：弹层类组件的内容被 Teleport 到 body、
  收起时整棵子树不渲染，按 DOM 找永远找不到实例，会把接好的线报成缺口。
  事件名按 Vue 的 camelize 规则归一，`row-click` 对应 `onRowClick`，直接比原文会把带横线的事件全部误报成缺口。
[豁免] 不由一次离散手势触发的事件（逐帧 / 逐秒 / 指针移动）不要求接反馈，豁免面集中一处定义，
  且必须是派生事件表里真实存在的条目，防止豁免面腐烂。
最近修改时间：2026-10-18 19:36:00；改动原因：6-review 发现 check_demo_event_wiring.py 251 行超 200 行基准，按 diamond 拆分，判据字节未改写。
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CL = ROOT / "component-library"
EVENTS_TABLE = CL / "src" / "views" / "gallery" / "demo-events.generated.ts"

SIGN_IN = """async (base) => {
    const login = await fetch(base + '/api/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username: 'admin', password: 'admin123', captcha: '1024', uuid: 'probe' }),
    }).then((r) => r.json())
    localStorage.setItem('scaffold.token', login.data.token)
    localStorage.setItem('scaffold.expiresAt', String(Date.now() + login.data.expiresIn * 1000))
    return Boolean(login.data.token)
}"""

# 每格示例里，该格组件实例上真实绑定的 on* 处理器。
# 不走「扫卡内 DOM 元素再回溯实例」：弹层类组件（Modal / Drawer / FormDialog / CommandPalette 等）
# 的内容被 Teleport 到 body，收起时更是整棵子树不渲染，按 DOM 找永远找不到实例，会把接好的线报成缺口。
# 改从 DemoCell 的 vnode 子树递归收集组件实例，与是否渲染、是否传送无关。
PROBE = r"""() => {
  const out = []
  const collect = (vnode, acc, depth) => {
    if (!vnode || depth > 40) return
    if (vnode.component) {
      acc.push(vnode.component)
      collect(vnode.component.subTree, acc, depth + 1)
    }
    const ch = vnode.children
    if (Array.isArray(ch)) { for (const c of ch) collect(c, acc, depth + 1); return }
    if (vnode.suspense) collect(vnode.suspense.activeBranch, acc, depth + 1)
  }
  for (const cell of document.querySelectorAll('.g-cell')) {
    const name = (cell.querySelector('.g-cell-name')?.childNodes[0]?.textContent || '').trim()
    const variant = (cell.querySelector('.g-cell-variant')?.textContent || '').trim()
    const body = cell.querySelector('.g-cell-body')
    if (!body) continue
    const bound = new Set()
    const host = body.__vueParentComponent
    if (host) {
      const acc = []
      collect(host.subTree, acc, 0)
      for (const inst of acc) {
        const cname = (inst.type && (inst.type.name || inst.type.__name)) || ''
        if (cname !== name) continue
        const p = inst.vnode && inst.vnode.props
        if (p) for (const k of Object.keys(p)) if (k.startsWith('on')) bound.add(k)
      }
    }
    out.push({ name, variant, bound: [...bound] })
  }
  return out
}"""

# 不要求接反馈的事件：不由一次离散手势触发，接上会在加载或拖拽过程中持续弹提示。
# 这些事件的可观察结果本来就在组件自身形态上（图形在动、尺寸在变、读数在跳）。

NO_FEEDBACK = {
    "Image.load": "图片每次加载都触发，不是手势",
    "Image.error": "同上，加载失败即触发",
    "Countdown.change": "每秒触发一次",
    "Upload.progress": "上传过程中逐块触发",
    "RelationGraph.hover": "指针移动即触发",
    "ResizeBox.resize": "拖拽过程中逐帧触发，尺寸变化本身可见",
    "SplitPane.resize": "同上，且开合值已由 update:modelValue 接住",
    "Carousel.change": "自动轮播时会持续触发，当前页已由 update:current 接住",
}



def norm(event: str) -> str:
    """把事件名归一成 Vue 处理器 prop 名的可比形式。

    [参数] event 事件名，如 `row-click` [返回] 去掉分隔符并小写后的串，如 `rowclick`。
    Vue 把 emit('row-click') 映射到 onRowClick，直接比原文会全量误报。
    """
    return re.sub(r"[-:]", "", event).lower()



def handler_keys(bound: list[str]) -> set[str]:
    """把已绑定的 `on*` prop 名归一成事件名可比形式。

    [参数] bound vnode 上的 on* 键列表 [返回] 归一化后的集合。
    """
    return {norm(k[2:]) for k in bound if k.startswith("on")}



def missing_events(emits: list[str], bound: list[str]) -> list[str]:
    """算出声明了却没接处理器、且不在豁免面的事件。

    [参数] emits 组件声明的事件名、bound 该格实际绑定的 on* 键 [返回] 缺口事件名列表。
    `update:*` 由示例层的样本状态写回负责，不在本判据范围内。
    """
    have = handler_keys(bound)
    return [e for e in emits if not e.startswith("update:") and norm(e) not in have]



def load_events_table() -> dict[str, list[str]]:
    """读派生事件表，作为「组件声明了哪些事件」的单一真相源。

    [参数] 无 [返回] 组件名到事件名列表的映射。
    不在守卫里重新解析 .vue：解析口径必须与装配层用的是同一份，否则两侧漂移时守卫仍然绿。
    """
    text = EVENTS_TABLE.read_text(encoding="utf-8")
    table: dict[str, list[str]] = {}
    for m in re.finditer(r"^\s{2}(\w+): \[(.*?)\],$", text, re.M):
        table[m.group(1)] = re.findall(r"'([^']+)'", m.group(2))
    return table
