<script setup lang="ts">
/* 输入组：把多个输入框 / 按钮横向或纵向拼成一条，整组读作「一个控件」而不是几个并排控件。
   接缝靠两条规则合成：相邻项负外边距吃掉重复的 1px 边框，中间项内侧圆角归零，
   于是整组只留下最外一圈描边和首尾一对圆角。用结构选择器而不是具体类名，
   是因为组内可以放输入框、按钮、下拉触发器任意组合，写死类名会在换控件时失效。
   边界：本组件只做排布，不接管子项的取值、校验与事件；子项各自受控。 */
withDefaults(defineProps<{
  direction?: 'horizontal' | 'vertical'
}>(), {
  direction: 'horizontal',
})
</script>

<template>
  <div :class="['x-input-group', `is-${direction}`]">
    <slot />
  </div>
</template>

<style scoped>
/* 组只决定排布方向，宽度留给调用方：整条铺满用 width: 100%，随内容收窄就用默认 inline-flex */
.x-input-group { display: inline-flex; min-width: 0; }
.x-input-group.is-horizontal { flex-direction: row; align-items: stretch; }
.x-input-group.is-vertical { flex-direction: column; align-items: stretch; }

/* ── 横排接缝：中间项左右圆角归零，相邻项左移 1px 让两条描边重叠成一条 ── */
.x-input-group.is-horizontal :deep(> *:not(:first-child)) {
  border-top-left-radius: 0;
  border-bottom-left-radius: 0;
}
.x-input-group.is-horizontal :deep(> *:not(:last-child)) {
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
}
.x-input-group.is-horizontal :deep(> * + *) { margin-left: -1px; }

/* ── 竖排接缝：同理，圆角换成上下两侧，重叠靠上移 1px ── */
.x-input-group.is-vertical :deep(> *:not(:first-child)) {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
.x-input-group.is-vertical :deep(> *:not(:last-child)) {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}
.x-input-group.is-vertical :deep(> * + *) { margin-top: -1px; }

/* 负边距让描边重叠后，后一项会盖住前一项；聚焦项必须抬到最上层，
   否则键盘走到中间那格时，焦点环会被右边邻居裁掉一半，用户看不出焦点在哪 */
.x-input-group :deep(> *:focus-within) { position: relative; z-index: 1; }
</style>
