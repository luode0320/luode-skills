<script setup lang="ts">
/* 头像组：多个头像叠压成一摞，超出 max 的部分收成末尾的 +N。
   叠压是为了在有限宽度里表达「一群人」而不是逐个排开占满一行；
   靠负外边距制造压边，再给每个头像套一圈与底同色的环，压住的头像才不会被糊成一团。
   环画在外层包裹元素上而不是头像本体，因为头像自身已带一道内高光阴影，直接覆盖会把它抹掉。
   边界：本组件不产出头像内容，头像由调用方放进默认插槽（通常是 <Avatar>）；
   max 不传即不裁剪，total 用于「服务端只返回了部分头像但知道总数」的场景。 */
import { computed, useSlots, Comment, Fragment, type VNode } from 'vue'

const props = withDefaults(defineProps<{
  /** 最多展示几个头像，不传则不裁剪 */
  max?: number
  /** 单个头像直径，px；同时决定 +N 气泡与叠压量，三者同源才不会错位 */
  size?: number
  /** 头像总数，用于服务端只返回部分头像时算 +N；不传则按实际子项数算 */
  total?: number
}>(), {
  size: 32,
})

const slots = useSlots()

/**
 * [参数] 无
 * [返回] 展开后的头像节点数组，已剔除条件渲染留下的注释占位；
 *         多子节点会被包进 Fragment，不拆开就无法按 max 逐个裁剪。
 *         与 Space 同一口径：子项数量只有拆平之后才是可信的。
 */
const children = computed<VNode[]>(() => {
  const out: VNode[] = []
  ;(slots.default?.() ?? []).forEach((node) => {
    if (node.type === Comment) return
    if (node.type === Fragment) (node.children as VNode[]).forEach(child => out.push(child))
    else out.push(node)
  })
  return out
})

/** [返回] 实际渲染的头像节点；max 未传或大于子项数时全部渲染 */
const visible = computed(() => (props.max === undefined ? children.value : children.value.slice(0, props.max)))

/**
 * [返回] +N 的 N。优先用 total 减可见数，这样服务端只回传前几个头像时
 *         仍能报出真实总数；total 缺席才退回按实际子项数算，避免虚报。
 */
const overflow = computed(() => {
  const remain = (props.total ?? children.value.length) - visible.value.length
  return remain > 0 ? remain : 0
})

/* 叠压量与环宽都由 size 推导：写死像素会在换尺寸后与头像直径脱节，露出压边错位 */
const stack = computed(() => ({ marginLeft: `${-Math.round(props.size * 0.28)}px` }))
const ring = { boxShadow: '0 0 0 2px var(--surface-solid)' }

/* +N 紧跟前一个头像，两者共用同一份叠压量；前面没有头像时不能负移，否则会向左多缩一截 */
const moreStyle = computed(() => [
  visible.value.length ? stack.value : undefined,
  ring,
  { width: `${props.size}px`, height: `${props.size}px`, fontSize: `${Math.round(props.size * 0.36)}px` },
])
</script>

<template>
  <div class="x-avatar-group" role="group">
    <span v-for="(node, i) in visible" :key="i" class="x-avatar-slot" :style="i ? stack : undefined">
      <component :is="node" />
    </span>
    <span
      v-if="overflow"
      class="x-avatar-more"
      :style="moreStyle"
      :aria-label="`另有 ${overflow} 个头像`"
    >+{{ overflow }}</span>
  </div>
</template>

<style scoped>
.x-avatar-group { display: inline-flex; align-items: center; }
.x-avatar-slot {
  position: relative;
  display: inline-flex;
  flex: none;
  border-radius: 999px;
  box-shadow: 0 0 0 2px var(--surface-solid);
}

/* +N 与头像同形同尺寸：圆形、同字号、同环宽，读作这一摞里的最后一个，而不是外挂的标签 */
.x-avatar-more {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex: none;
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  background: var(--surface-solid);
  color: var(--ink-muted);
  font-weight: 640;
  letter-spacing: -.02em;
  user-select: none;
}
</style>
