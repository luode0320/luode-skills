<script setup lang="ts">
/* 按钮组：把若干个按钮拼成一条，相邻处只留一道描边、首尾各留一次圆角。
   接缝的成因是每个按钮自带 1px 边框（次级按钮的玻璃块边），并排就会出现 2px 双线；
   用负外边距把相邻两条重叠成一条，再把中间项的内侧圆角归零，整组才读成一个控件。
   尺寸不给子按钮逐个传 props，而是就地重声明 --control-h：按钮高度读的就是这个令牌，
   改一处就能整体收放，不必知道组里放的是哪种按钮。
   边界：本组件只做排布与尺寸收敛，不接管按钮的点击、变体与禁用态，各按钮仍由调用方受控。 */
withDefaults(defineProps<{
  size?: 'md' | 'sm'
  direction?: 'horizontal' | 'vertical'
}>(), {
  size: 'md',
  direction: 'horizontal',
})
</script>

<template>
  <div :class="['x-btn-group', `is-${direction}`, size === 'sm' && 'is-sm']">
    <slot />
  </div>
</template>

<style scoped>
/* 组默认随内容收窄；需要铺满时由调用方在自身给宽度 */
.x-btn-group { display: inline-flex; min-width: 0; }
.x-btn-group.is-horizontal { flex-direction: row; align-items: stretch; }
.x-btn-group.is-vertical { flex-direction: column; align-items: stretch; }

/* 小号只改令牌与字号：按钮自身高度、内距都从令牌派生，重声明令牌即整组收放 */
.x-btn-group.is-sm { --control-h: var(--control-h-sm); }
.x-btn-group.is-sm :deep(> *) { font-size: 13px; }

/* ── 横排接缝 ── */
.x-btn-group.is-horizontal :deep(> *:not(:first-child)) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.x-btn-group.is-horizontal :deep(> *:not(:last-child)) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.x-btn-group.is-horizontal :deep(> * + *) { margin-left: -1px; }

/* ── 竖排接缝 ── */
.x-btn-group.is-vertical :deep(> *:not(:first-child)) {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
.x-btn-group.is-vertical :deep(> *:not(:last-child)) {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.x-btn-group.is-vertical :deep(> * + *) { margin-top: -1px; }

/* 后一项压住前一项时，悬停与键盘聚焦的按钮必须抬到最上层，
   否则它的焦点环会被右邻居裁掉一半，用户看不出焦点落在哪一格 */
.x-btn-group :deep(> *:hover),
.x-btn-group :deep(> *:focus-visible) { position: relative; z-index: 1; }
</style>
