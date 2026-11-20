/* 确认落定（Crystallize）：从登录页那套「收拢成圆 → 描环 → 画勾 → 回弹」
   抽出来的单拍动效。
   语态是「结」（Crystallize），只用于操作**真正成功**的那一刻。
   加载中请用 spinner（「导」Conduct），失败请用图标 + 危险色（「停摆」Halt），
   三种语态不要混用——把落定做成加载转圈，会让成功看起来还没结束。 */
import { EASE, gsap, motionSkipped } from '@/composables/motion'

/** 参与落定的三个元素：收拢的容器、圆环、对勾 */
export interface CrystallizeTargets {
  /** 要收拢成圆的容器，宽度会从当前实测值收到 size */
  orb: HTMLElement
  /** 圆环，靠 stroke-dashoffset 描出 */
  ring?: SVGCircleElement | SVGPathElement | null
  /** 对勾，比圆环晚一点起笔 */
  check?: SVGPathElement | null
}

export interface CrystallizeOptions {
  /** 收拢后的直径；不传则取当前高度（按钮自带高度即为圆的大小，不会跳高） */
  size?: number
  /** 圆环 stroke-dasharray 总长，默认与 r=20 的周长对齐（2πr≈126） */
  ringDash?: number
  /** 对勾 stroke-dasharray 总长 */
  checkDash?: number
}

/**
 * 播放一次确认落定。
 * [参数] targets 三个目标元素 / options 尺寸与 dash 长度
 * [返回] 时间线走完后 resolve 的 Promise；降级时立即 resolve
 */
export function playCrystallize(targets: CrystallizeTargets, options: CrystallizeOptions = {}): Promise<void> {
  const { orb, ring, check } = targets
  const rect = orb.getBoundingClientRect()
  const size = options.size ?? rect.height
  const ringDash = options.ringDash ?? 126
  const checkDash = options.checkDash ?? 24

  /* 降级：保留语义、去掉过程。直接给终态，绝不能停在半收拢的中间态 */
  if (motionSkipped()) {
    gsap.set(orb, { width: size })
    if (ring) gsap.set(ring, { strokeDashoffset: 0 })
    if (check) gsap.set(check, { strokeDashoffset: 0 })
    return Promise.resolve()
  }

  return new Promise<void>((resolve) => {
    const tl = gsap.timeline({ onComplete: resolve })
    /* 第一拍 放 Discharge：收拢。0.42s + swap 曲线，起手快、落位稳 */
    tl.fromTo(orb, { width: rect.width }, { width: size, duration: 0.42, ease: EASE.swap })
    /* 第二拍 结 Crystallize：圆环先描，提前 0.08s 交接，不等第一拍完全停下 */
    if (ring) tl.fromTo(ring, { strokeDashoffset: ringDash }, { strokeDashoffset: 0, duration: 0.5, ease: EASE.reveal }, '-=0.08')
    /* 对勾再压 0.22s 起笔：笔顺感靠这 0.22s 的错位，同时起笔会读成一闪而过 */
    if (check) tl.fromTo(check, { strokeDashoffset: checkDash }, { strokeDashoffset: 0, duration: 0.32, ease: EASE.settle }, '-=0.22')
    /* 最后一拍回弹：先过冲 6% 再落回 1，确认感来自这一下，不是靠放大停留 */
    tl.to(orb, { scale: 1.06, duration: 0.16, ease: 'power1.out' })
      .to(orb, { scale: 1, duration: 0.3, ease: EASE.settle })
  })
}
