<script setup lang="ts">
/* 单卡隔离渲染：一个组件炸了不影响其余组件；把失败原因留在卡内而不是全局崩页。
   卡头给出组件名、变体标签与仓库内路径，便于人工核对时直接定位源码。
   最近修改时间：2026-10-17 09:28:00；改动原因：修「边角阴影块」——示例内容区原本
   无留白，组件柔影被滚动容器裁切边界切成方形暗块，现按实测延展加四周留白，
   并同步抬高高度上限以保持内容可视高度不变。 */
import { ref, onErrorCaptured } from 'vue'
import HelpTip from '../../components/extend/HelpTip.vue'

const props = defineProps<{ name: string; variant?: string; rel?: string; guide?: string }>()
const error = ref('')

onErrorCaptured((err) => {
  error.value = err.message || String(err)
  return false
})
</script>

<template>
  <div class="g-cell">
    <div class="g-cell-head">
      <span class="g-cell-name">{{ name }}<em v-if="variant" class="g-cell-variant">{{ variant }}</em><HelpTip v-if="guide" :content="guide" tone="help" :label="`查看 ${name} 的说明`" /></span>
      <span class="g-cell-status" :class="error ? 'is-bad' : 'is-ok'">{{ error ? '渲染异常' : '已挂载' }}</span>
    </div>
    <div class="g-cell-path">{{ rel }}</div>
    <div v-if="error" class="g-cell-err">{{ error }}</div>
    <div v-else class="g-cell-body"><slot /></div>
  </div>
</template>

<style scoped>
/* 卡片样式随组件本地下沉：示例页原依赖独立核对页的全局样式块，迁入后台后必须自带。
   三列布局后单卡更宽，标题与路径字号随之上调一档，避免大卡里配一行小字显得失衡。 */
.g-cell { border: 1px solid var(--line); border-radius: var(--r-md); background: var(--surface); box-shadow: var(--e1); padding: 14px; display: flex; flex-direction: column; gap: 9px; min-height: 96px; }
.g-cell-head { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
.g-cell-name { font-weight: 600; font-size: 14px; display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.g-cell-variant { font-style: normal; font-weight: 500; font-size: 12px; padding: 2px 8px; border-radius: 999px; background: var(--blue-soft); color: var(--blue); }
.g-cell-path { font-size: 11px; color: var(--ink-faint); word-break: break-all; }
.g-cell-status { font-size: 12px; padding: 2px 8px; border-radius: 999px; }
.g-cell-status.is-ok { background: var(--lime-soft); color: var(--leaf-text); }
.g-cell-status.is-bad { background: var(--red-soft); color: var(--red-text); }
.g-cell-err { font-size: 12px; color: var(--red-text); word-break: break-all; }
/* 内容比卡片宽/高时给滚动条而不是裁掉：示例必须完整可见，窄屏也不能丢样式。
   padding 是投影留白：滚动容器的裁切边落在 padding 外沿，留白把示例柔影推回裁切线之内，
   否则会在卡片边缘被切成方形暗块。取值按 579 格实测四向上限（上 6 / 侧 25 / 下 47）；
   A/B 对照（38 页，唯一变量是留白）净增 3 横 1 竖滚动条换来卡内柔影零裁切。
   max-height 同步加高（560+26+48=634），三列大卡下内容可视高度随之上调。 */
.g-cell-body { flex: 1; display: block; overflow: auto; max-height: 634px; padding: 26px 26px 48px; }
</style>
