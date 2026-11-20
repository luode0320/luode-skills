/* 形变语式：管「形状怎么变」，与 motion.ts 的「变化多顺」分工不同。
   motion.ts 提供曲线与时长（EASE / DUR）；这里提供几何动作本身。

   三条纪律：
   1. **起点必须是「无」**。0.6 → 1 只能看出「弹一下」，0 → 1 才是「长出来」——
      登录按钮的形变感来自「从无到有」，不是「从小到大」。
   2. **只动 transform / opacity**。改宽高会推走相邻元素，在列表里尤其明显。
   3. **说不出语式的不做**：落定（Settle）/ 收拢（Collapse）/ 描线（Draw）/ 展开（Unfold）。
      本模块目前只覆盖「落定」。 */
import { EASE, gsap, motionSkipped, overlayEnter, overlayLeave } from '@/composables/motion'

/** 生长落定：scale 0 → 1，带回弹。用于圆点、勾、选中标记。 */
export function growIn(el: Element | null | undefined, duration = 0.38, delay = 0) {
  if (!el || motionSkipped()) return
  withTransitionOff(el, () => {
    gsap.fromTo(
      el,
      { scale: 0 },
      { scale: 1, duration, delay, ease: EASE.settle, clearProps: 'transform', onComplete: () => restore(el) },
    )
  })
}

/** 按压落定：1 → 0.88 → 1。用于「被点中的那个容器」，给一下按压手感。 */
export function pressSettle(el: Element | null | undefined, dip = 0.88) {
  if (!el || motionSkipped()) return
  withTransitionOff(el, () => {
    const tl = gsap.timeline({ onComplete: () => { gsap.set(el, { clearProps: 'transform' }); restore(el) } })
    tl.to(el, { scale: dip, duration: 0.16, ease: 'power2.out' })
      .to(el, { scale: 1, duration: 0.34, ease: EASE.settle })
  })
}

/* 元素自己可能带 `transition: transform`（例如 Rate 星标的悬停放大）。
   GSAP 每帧写 inline transform 会被这条过渡再插值一次，动作会变软变慢——
   动效期间先关掉它，结束后恢复成空串让 CSS 重新接管。 */
const saved = new WeakMap<Element, string>()

function withTransitionOff(el: Element, run: () => void) {
  const node = el as HTMLElement
  if (node.style) {
    if (!saved.has(el)) saved.set(el, node.style.transition)
    node.style.transition = 'none'
  }
  run()
}

function restore(el: Element) {
  const node = el as HTMLElement
  if (!node.style) return
  node.style.transition = saved.get(el) ?? ''
  saved.delete(el)
}

/**
 * 选中形变：容器按压 + 标记生长，标记比容器晚 60ms 起手。
 * [参数] box 被选中的容器（圆环/方块） / mark 内部标记（圆点/勾）
 * [返回] 无
 */
export function morphSelect(box: Element | null | undefined, mark: Element | null | undefined) {
  if (motionSkipped()) return
  pressSettle(box)
  growIn(mark, 0.38, 0.06)
}

/** 取消选中：只把标记收回去，容器不表演——取消不该有存在感。 */
export function morphUnselect(mark: Element | null | undefined) {
  if (!mark || motionSkipped()) return
  gsap.set(mark, { scale: 0 })
}

/**
 * 浮层入场 / 退场的统一入口。
 *
 * **形态按「面板内有没有可操作项」分派**：
 * - 纯文字提示（Tooltip / HelpTip / BackTop）走上游 `pop` 分支，轻量淡入，别抢注意力。
 * - 内容面板（菜单、下拉、级联、日期）**从锚点缩放展开**——用户实测认为缩放比位移更「丝滑」，
 *   因为缩放有「从触发器长出来」的来源感，位移只是「滑进来」，缺来源。
 *
 * 但上游 `modal` 分支的缩放有三个缺陷，这里自己实现以逐项修掉：
 *
 * 1. **长尾**：`expo.out` 在 46ms 就走到 0.944，之后 150ms 只再走 0.05——观感是「唰一下
 *    然后停着」。改用 `glide`（power4.out），收尾更干净；时长压到 0.28s。
 * 2. **文字重栅格化**：缩放期间的文字会被重新栅格化，动画中发虚。入场时挂
 *    `will-change: transform, opacity`，把元素提升为合成层，用纹理插值代替重排；
 *    结束立刻清理，避免长期占内存。
 * 3. **原点不准**：上游按面板几何算 `transformOrigin`，缩放轴心可能落在面板中部，
 *    看起来像「从肚子鼓起来」。下拉是从触发器往下长，轴心就该在**顶边中心**。
 *
 * `motion.ts` 是逐字节冻结的上游文件，改不了它的分支参数，所以在这里自己实现。
 */
const ACTIONABLE = 'button, [role="menuitem"], [role="option"], [role="treeitem"], input, textarea, select'

export function overlayMenuEnter(el: Element, done: () => void) {
  if (!el.querySelector(ACTIONABLE)) {
    overlayEnter(el, done, 'pop')     // 纯文字提示：保持上游的轻量形态
    return
  }
  if (motionSkipped()) { done(); return }
  const node = el as HTMLElement
  const rect = node.getBoundingClientRect()
  /* 面板落在视口下半 → 从触发器往上长，轴心在底边；反之在顶边 */
  const fromBelow = rect.top + rect.height / 2 < window.innerHeight / 2
  gsap.fromTo(
    node,
    { opacity: 0, scale: 0.88, transformOrigin: `50% ${fromBelow ? '0%' : '100%'}` },
    {
      opacity: 1,
      scale: 1,
      duration: 0.28,
      ease: EASE.glide,
      willChange: 'transform, opacity',
      overwrite: true,
      onComplete: () => {
        gsap.set(node, { clearProps: 'transform,transformOrigin,willChange' })
        done()
      },
    },
  )
}

export function overlayMenuLeave(el: Element, done: () => void) {
  if (!el.querySelector(ACTIONABLE)) {
    overlayLeave(el, done, 'pop')
    return
  }
  if (motionSkipped()) { done(); return }
  gsap.to(el, { opacity: 0, duration: 0.14, ease: EASE.exit, overwrite: true, onComplete: done })
}

/**
 * 弹窗 / 遮罩的入场。与菜单同一套参数规格，**只换轴心**：
 * 菜单从触发器那一侧生长（顶边），弹窗从自身中心升起（中心）。
 *
 * 有内层面板（`.modal` / `.cmd-panel`）时：遮罩淡入 + 面板 `scale 0.92 → 1`。
 * 没有内层面板的（图片预览这类整块遮罩）：**只淡入，不缩放**——
 * 图片的 `zoom` / `pan` 是用户交互状态、写在自己的 inline transform 上，
 * GSAP 直接动 `transform` 会把它覆盖掉。
 *
 * `Drawer` 不走这里：它用上游 `'drawer'` 分支的共享元素 ghost（从被点的行长成抽屉），
 * 那是它专属的形变，不能被通用弹窗形态替代。
 */
const DIALOG_PANEL = '.modal, .cmd-panel'

export function overlayDialogEnter(el: Element, done: () => void) {
  if (motionSkipped()) { done(); return }
  gsap.fromTo(el, { opacity: 0 }, { opacity: 1, duration: 0.2, ease: 'power1.out', overwrite: true })

  const panel = el.querySelector(DIALOG_PANEL)
  if (!panel) { done(); return }   // 只有遮罩：淡入即完整动作
  gsap.fromTo(
    panel,
    { opacity: 0, scale: 0.92, transformOrigin: '50% 50%' },
    {
      opacity: 1,
      scale: 1,
      duration: 0.28,
      ease: EASE.glide,
      willChange: 'transform, opacity',
      overwrite: true,
      onComplete: () => {
        gsap.set(panel, { clearProps: 'transform,transformOrigin,willChange' })
        done()
      },
    },
  )
}

export function overlayDialogLeave(el: Element, done: () => void) {
  if (motionSkipped()) { done(); return }
  gsap.to(el, { opacity: 0, duration: 0.16, ease: EASE.exit, overwrite: true, onComplete: done })
}

/**
 * 收拢消失：宽度与左右内边距一起收到 0，用于标签、胶囊的移出。
 * 这是少数允许动宽高的地方——收拢本来就是「宽度变没」，
 * 用 transform: scaleX 会把文字压扁，比动宽高更假。
 * [参数] el 目标元素，duration 时长（退场比入场快）
 * [返回] 动画结束的 Promise；降级时立即 resolve
 */
export function collapseOut(el: Element | null | undefined, duration = 0.24): Promise<void> {
  if (!el || motionSkipped()) return Promise.resolve()
  const node = el as HTMLElement
  return new Promise((resolve) => {
    gsap.to(node, {
      width: 0,
      paddingLeft: 0,
      paddingRight: 0,
      marginRight: 0,
      opacity: 0,
      duration,
      ease: EASE.exit,
      onComplete: resolve,
    })
  })
}
