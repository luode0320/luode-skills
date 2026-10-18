<script setup lang="ts">
/* 溢出列表：按容器宽度逐项排布，放不下的项收进 +N 下拉，点开可看全部。
   maxCount 作为项数上限与宽度二者取小；宽度探测用 ResizeObserver，无现成工具可复用。 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import Icon from '@/components/Icon.vue'
import { overlayEnter, overlayLeave } from '@/composables/motion'
import { floatingLayerFor } from '@/composables/focus'

const props = withDefaults(defineProps<{
  items: Array<{ key: string | number; label: string }>
  maxCount?: number
  collapseFrom?: 'start' | 'end'
}>(), {
  collapseFrom: 'end',
})

const host = ref<HTMLElement | null>(null)
const measure = ref<HTMLElement | null>(null)
const moreBtn = ref<HTMLElement | null>(null)
const visibleCount = ref(Infinity)
const open = ref(false)
const pos = ref({ top: 0, left: 0 })
let observer: ResizeObserver | null = null

/** [参数] 无 [返回] 逐项累加宽度，算出当前容器能完整容纳的项数 */
function recalc() {
  const box = host.value
  const strip = measure.value
  if (!box || !strip) return
  const limit = props.maxCount && props.maxCount > 0 ? props.maxCount : Infinity
  const kids = Array.from(strip.children) as HTMLElement[]
  /* 预留 +N 触发器自身的宽度，避免刚好放下却被挤掉 */
  const reserve = 46
  const avail = box.clientWidth - reserve
  let used = 0
  let fit = 0
  for (const kid of kids) {
    used += kid.offsetWidth + 6
    if (used > avail) break
    fit += 1
  }
  visibleCount.value = Math.min(Math.max(fit, 1), limit, props.items.length)
}

onMounted(() => {
  observer = new ResizeObserver(() => recalc())
  if (host.value) observer.observe(host.value)
  nextTick(recalc)
})

onBeforeUnmount(() => observer?.disconnect())

watch(() => [props.items, props.maxCount, props.collapseFrom], () => nextTick(recalc))

/** [参数] 无 [返回] 按 collapseFrom 决定可见项与溢出项 */
const visible = computed(() => {
  if (visibleCount.value >= props.items.length) return props.items
  return props.collapseFrom === 'start'
    ? props.items.slice(props.items.length - visibleCount.value)
    : props.items.slice(0, visibleCount.value)
})

/** [参数] 无 [返回] 被收进下拉的溢出项 */
const hidden = computed(() => {
  if (visibleCount.value >= props.items.length) return []
  return props.collapseFrom === 'start'
    ? props.items.slice(0, props.items.length - visibleCount.value)
    : props.items.slice(visibleCount.value)
})

/** [参数] 无 [返回] 开合下拉；打开时按触发器位置定锚点 */
async function toggle() {
  open.value = !open.value
  if (!open.value) return
  await nextTick()
  place()
}

/** [参数] 无 [返回] 测量触发器矩形，把下拉固定在它下方并夹在视口内 */
function place() {
  const rect = moreBtn.value?.getBoundingClientRect()
  if (!rect) return
  const width = 200
  const gap = 6
  const left = Math.min(Math.max(8, rect.left), window.innerWidth - width - 8)
  pos.value = { top: rect.bottom + gap, left }
}

/** [参数] 无 [返回] 关闭下拉 */
function close() {
  open.value = false
}

/** [参数] 无 [返回] 弹层与点击捕层的层级，捕层比弹层低 1 */
const layer = computed(() => floatingLayerFor(host.value))
</script>

<template>
  <div ref="host" class="x-overflow" :class="collapseFrom === 'start' && 'is-reverse'">
    <div class="x-overflow-strip">
      <span v-for="item in visible" :key="item.key" class="x-overflow-item">
        <slot :item="item">{{ item.label }}</slot>
      </span>
      <button v-if="hidden.length" ref="moreBtn" class="x-overflow-more btn-text" type="button" :aria-expanded="open" @click="toggle">
        +{{ hidden.length }}
        <Icon name="chevronDown" :size="12" />
      </button>
    </div>

    <!-- 离屏测量条：与可见项同宽，仅用于逐项量宽 -->
    <div ref="measure" class="x-overflow-strip is-measure" aria-hidden="true">
      <span v-for="item in items" :key="item.key" class="x-overflow-item">
        <slot :item="item">{{ item.label }}</slot>
      </span>
    </div>

    <Teleport to="body">
      <Transition :css="false" @enter="(el, done) => overlayEnter(el, done, 'pop')" @leave="(el, done) => overlayLeave(el, done, 'pop')">
        <div
          v-if="open"
          class="x-overflow-pop m-float"
          :style="{ top: `${pos.top}px`, left: `${pos.left}px`, zIndex: layer + 1 }"
        >
          <span v-for="item in hidden" :key="item.key" class="x-overflow-pop-item">
            <slot :item="item">{{ item.label }}</slot>
          </span>
        </div>
      </Transition>
      <button v-if="open" class="x-overflow-backdrop" type="button" aria-label="关闭" :style="{ zIndex: layer }" @click="close" />
    </Teleport>
  </div>
</template>

<style scoped>
.x-overflow { position: relative; min-width: 0; }
.x-overflow-strip { display: flex; align-items: center; gap: 6px; }
.x-overflow-strip.is-measure {
  position: absolute;
  top: 0;
  left: 0;
  visibility: hidden;
  pointer-events: none;
  white-space: nowrap;
  width: max-content;
}
.x-overflow-item { flex: none; white-space: nowrap; }
.x-overflow-more {
  flex: none;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  padding: 0 4px;
  border: 0;
  background: transparent;
  font: inherit;
  font-size: 12px;
  color: var(--blue);
  cursor: pointer;
}
.x-overflow-pop {
  position: fixed;
  min-width: 160px;
  max-width: 240px;
  max-height: 280px;
  overflow: auto;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding: 10px 12px;
  border-radius: var(--r-sm);
  font-size: 12px;
  color: var(--ink);
  box-shadow: var(--e3);
}
.x-overflow-pop-item { white-space: nowrap; }
.x-overflow-backdrop {
  position: fixed;
  inset: 0;
  border: 0;
  background: transparent;
  cursor: default;
}
</style>
