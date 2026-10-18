<script setup lang="ts">
/* 倒计时：按目标时间戳或剩余秒数逐秒倒数，按格式串渲染，走到零时派发 finish。
   两种输入的分工：target 适合「活动到某时刻结束」这种绝对值，remaining 适合「还剩 N 秒」，
   同时给时以 target 为准——绝对时间不会因为组件晚挂载一秒而整体偏移。
   计时用 setInterval 驱动，但每次 tick 都按真实时钟重算剩余量：
   只用「减一」累加会在浏览器切后台限流后越走越慢，重算能自动纠正累积误差。 */
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

const props = withDefaults(defineProps<{
  target?: number
  remaining?: number
  format?: string
  autostart?: boolean
}>(), {
  format: 'HH:mm:ss',
  autostart: true,
})

const emit = defineEmits<{
  (e: 'finish'): void
  (e: 'change', remaining: number): void
}>()

const left = ref(0)
let timer: number | undefined
/* 结束只派发一次：setInterval 会在归零后继续触发，靠这个标记挡住重复的 finish */
let finished = false

/**
 * [参数] 无
 * [返回] 当前剩余秒数（不小于 0）。给了 target 就按当前时钟算差值，否则回落到 remaining 配置
 */
function readRemaining() {
  if (props.target !== undefined) return Math.max(0, Math.ceil((props.target - Date.now()) / 1000))
  return Math.max(0, Math.floor(props.remaining ?? 0))
}

/**
 * [参数] 无
 * [返回] 无。推进一次：更新剩余量、派发 change，归零时停表并派发 finish
 */
function tick() {
  const next = readRemaining()
  left.value = next
  emit('change', next)
  if (next <= 0) {
    stop()
    if (!finished) {
      finished = true
      emit('finish')
    }
  }
}

/**
 * [参数] 无
 * [返回] 无。清定时器并置空句柄，重复调用是安全的
 */
function stop() {
  window.clearInterval(timer)
  timer = undefined
}

/**
 * [参数] 无
 * [返回] 无。从当前配置重新起算并启动秒表；已归零时直接触发结束，不再空转
 */
function start() {
  stop()
  finished = false
  left.value = readRemaining()
  if (left.value <= 0) {
    finished = true
    emit('finish')
    return
  }
  timer = window.setInterval(tick, 1000)
}

/**
 * [参数] value 秒数 [返回] 补零到两位的字符串
 */
function pad(value: number) {
  return String(Math.floor(value)).padStart(2, '0')
}

/**
 * [参数] 无
 * [返回] 按 format 占位替换后的显示文本；DD 只在格式里出现时才参与，避免默认多出一个 00 天
 */
const text = computed(() => {
  const total = left.value
  const tokens: Record<string, string> = {
    DD: pad(Math.floor(total / 86400)),
    HH: pad(Math.floor(total / 3600) % 24),
    mm: pad(Math.floor(total / 60) % 60),
    ss: pad(total % 60),
  }
  return props.format.replace(/DD|HH|mm|ss/g, (token) => tokens[token] ?? token)
})

/* 目标时刻或剩余秒数变化时按新配置重启，而不是沿用旧起点继续倒数 */
watch(() => [props.target, props.remaining], () => {
  if (props.autostart) start()
  else {
    stop()
    left.value = readRemaining()
  }
})

onMounted(() => {
  if (props.autostart) start()
  else left.value = readRemaining()
})

/* 卸载必须清表：否则组件已销毁但定时器仍在跑，会持续持有闭包并派发到已卸载的实例 */
onBeforeUnmount(stop)

defineExpose({ start, stop, reset: start })
</script>

<template>
  <span class="x-countdown" role="timer" :aria-live="'off'">{{ text }}</span>
</template>

<style scoped>
/* 等宽数字：秒数跳动时每一位的宽度不变，整块文本不会左右抖 */
.x-countdown {
  font-family: var(--font-mono);
  font-size: 13px;
  font-variant-numeric: tabular-nums;
  letter-spacing: .02em;
  color: var(--ink);
}
</style>
