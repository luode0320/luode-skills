<script setup lang="ts">
/* 确认落定按钮：一次操作里走完「提交 → 收拢成圆 → 描环 → 画勾」。
   它是 Button 的**替代**而不是包装——需要形变的是按钮自己的宽度，
   套在 Button 外面就动不了内层。variant / size 与 Button 同名同值，
   换用时只改标签名。

   语态分工（与 motion.ts 一致，不要混用）：
   pending 用 spinner（导 Conduct）/ success 用落定（结 Crystallize）/
   error 用图标 + 危险色（停摆 Halt）。把落定做成转圈，成功会看起来没结束。 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { playCrystallize } from '@/composables/crystallize'

const props = withDefaults(defineProps<{
  /** 不传则自驱：点一下自己走完 pending → success（约 1.8s 后复位，方便反复演示）。
      传了就是受控，状态切换完全由调用方掌握。 */
  status?: 'idle' | 'pending' | 'success' | 'error'
  variant?: 'primary' | 'secondary' | 'ghost' | 'text' | 'danger'
  size?: 'md' | 'sm'
  icon?: string
  disabled?: boolean
  /** 默认铺满：形变需要一个能收拢的宽度，窄按钮上看不出「收拢」 */
  block?: boolean
  type?: 'button' | 'submit'
  /** 成功圆的无障碍文案 */
  successLabel?: string
}>(), {
  variant: 'primary',
  size: 'md',
  block: true,
  type: 'button',
  successLabel: '操作已完成',
})

const orb = ref<HTMLElement | null>(null)
const ring = ref<SVGCircleElement | null>(null)
const check = ref<SVGPathElement | null>(null)

/* 自驱状态：只在未传 status 时生效 */
const auto = ref<'idle' | 'pending' | 'success' | 'error'>('idle')
const controlled = computed(() => props.status !== undefined)
const current = computed(() => props.status ?? auto.value)

const busy = computed(() => current.value === 'pending')
const done = computed(() => current.value === 'success')
const failed = computed(() => current.value === 'error')

let autoTimer = 0
let settledResolve: (() => void) | null = null

/** [参数] 无 [返回] 无；受控模式不动状态，自驱模式播一次完整流程 */
async function onClick() {
  if (controlled.value || props.disabled || busy.value) return
  auto.value = 'pending'
  await new Promise<void>((resolve) => { autoTimer = window.setTimeout(resolve, 620) })
  /* 等落定动画**真正走完**再复位：固定延时会在慢帧机器上把最后的回弹剪掉，
     而回弹正是「确认感」所在的那一下。 */
  const settled = new Promise<void>((resolve) => { settledResolve = resolve })
  auto.value = 'success'
  await settled
  autoTimer = window.setTimeout(() => { auto.value = 'idle' }, 900)
}

/* 只在非 success → success 这一拍播放：来回切状态不该反复表演 */
watch(current, async (next, prev) => {
  if (next !== 'success' || prev === 'success') return
  await nextTick()
  if (!orb.value) return
  await playCrystallize({ orb: orb.value, ring: ring.value, check: check.value })
  settledResolve?.()
  settledResolve = null
})

/* 挂载时就已经是成功态（例如示例静态渲染、列表里回显已完成）：
   没有动画可播，直接给收拢后的宽度，否则会停在一条满宽的空条上。 */
onMounted(async () => {
  if (!done.value) return
  await nextTick()
  if (!orb.value) return
  orb.value.style.width = `${orb.value.getBoundingClientRect().height}px`
})

onBeforeUnmount(() => { window.clearTimeout(autoTimer) })
</script>

<template>
  <!-- 落定后按钮里只剩图形，可访问名必须挂在按钮本体上；
       挂在内层圆上读屏读不到按钮名，守卫会判 noName。 -->
  <button
    :type="type"
    :class="[
      'btn', `btn-${variant}`, 'cx-btn',
      size === 'sm' && 'btn-sm',
      block && 'btn-block',
      done && 'is-done',
      failed && 'is-error',
      variant === 'secondary' && 'm-pill',
    ]"
    :disabled="disabled || busy"
    :aria-busy="busy || undefined"
    :aria-label="done ? successLabel : undefined"
    @click="onClick"
  >
    <span
      v-if="done"
      ref="orb"
      class="cx-orb"
      role="status"
      :aria-label="successLabel"
    >
      <svg viewBox="0 0 46 46" aria-hidden="true">
        <circle ref="ring" cx="23" cy="23" r="20" stroke-dasharray="126" />
        <path ref="check" d="m15 23.5 5.5 5.5L31.5 18" stroke-dasharray="24" />
      </svg>
    </span>
    <template v-else>
      <span v-if="busy" class="spinner" aria-hidden="true" />
      <Icon v-else-if="failed" name="x" :size="size === 'sm' ? 14 : 16" />
      <Icon v-else-if="icon" :name="icon" :size="size === 'sm' ? 14 : 16" />
      <slot />
    </template>
  </button>
</template>

<style scoped>
/* 落定态把按钮自身的填充让给内层圆：外壳透明、内边距归零，
   宽度才能收到和高度相等而成为正圆 */
.cx-btn.is-done {
  padding: 0;
  background: transparent;
  border-color: transparent;
  box-shadow: none;
}

.cx-btn.is-error {
  /* 失败态换成「淡红底 + 深红字」，与 .btn-text.is-danger 同一套语言。
     不要在主色实底上直接压 --red-text：那是给浅底用的字色，红字铺蓝只有 1.01:1。 */
  background: var(--red-soft);
  border-color: color-mix(in srgb, var(--red-text) 38%, transparent);
  color: var(--red-text);
  box-shadow: none;
}

.cx-orb {
  display: grid;
  place-items: center;
  width: 100%;
  height: 100%;
  overflow: hidden;
  border-radius: 9999px;
  background: var(--blue-solid);
  color: var(--plate-ink);
}

/* 让 viewBox 撑满再收到 88%：登录页那颗是 46px 圆、环径 0.87，换算到按钮高度
   36px 时 0.87 会让环贴住蓝底边（只剩 1.3px）。收到 88% 能留出约 2.4px 呼吸，
   尺寸变了比例也不会漂。 */
.cx-orb svg { display: block; width: 88%; height: 88%; }

/* 描线三件套：无填充、圆头圆角，靠 dashoffset 一笔一笔画出来 */
.cx-orb circle,
.cx-orb path {
  fill: none;
  stroke: currentColor;
  stroke-width: 2.6;
  stroke-linecap: round;
  stroke-linejoin: round;
}
</style>
