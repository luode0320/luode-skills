<script setup lang="ts">
/* 组件库示例页：管理后台内的组件用法目录。
   组件全集由 entries.ts 从磁盘发现并按变体展开，页面不维护第二份清单；
   分类口径取自单一数据源，路由用「父分类/子分组」两段决定当前页，
   因此「菜单登记 + 分类数据源」两处一致即可，无需改页面代码。
   每格示例用 variantKey 独立寻址，弹层开关与受控回写互不串扰。 */
import { computed, reactive, ref } from 'vue'
import { useRoute } from 'vue-router'
import PageHeader from '../../components/ui/PageHeader.vue'
import Breadcrumb from '../../components/extend/Breadcrumb.vue'
import InputSearch from '../../components/extend/InputSearch.vue'
import Button from '../../components/ui/Button.vue'
import EmptyState from '../../components/ui/EmptyState.vue'
import { confirm } from '../../composables/confirm'
import { pushToast } from '../../composables/toast'
import { COMPONENT_CATEGORY_ORDER } from '../../data/component-categories'
import { GEN_TABLE } from './demo-business-samples'
import { demoEntries, liveOf, type DemoEntry } from './entries'
import { demoGuideOf } from './demo-guides'
import DemoCell from './DemoCell.vue'

const route = useRoute()
const keyword = ref('')
/* 弹层开关按 variantKey 逐格记录：同一组件的多个示例互不同开同关 */
const openState = reactive<Record<string, boolean>>({})

/* 路径由「父分类/子分组」两段决定：菜单里父分类只是侧栏分组标题、本身不带 component，
   「组件库」同样不是页面，所以这两级在面包屑里只作层级说明不可点，点进去会落到 404。 */
const current = computed(() => {
  const seg = String(route.path).split('/').filter(Boolean).slice(1)
  const cat = COMPONENT_CATEGORY_ORDER.find((c) => c.key === seg[0]) ?? null
  const sub = cat?.subGroups.find((s) => s.key === seg[1]) ?? null
  return { cat, sub }
})
const pageLabel = computed(() => current.value.sub?.label ?? current.value.cat?.label ?? '全部组件')
const pageDesc = computed(() => {
  const { cat, sub } = current.value
  const scope = sub?.desc ?? cat?.desc ?? '全部组件示例'
  return `${scope}；本组 ${items.value.length} 组示例，由磁盘自动发现并按变体展开且可直接操作`
})
const crumbs = computed(() => {
  const { cat, sub } = current.value
  const trail = [{ label: '首页', to: '/' }, { label: '组件库' }]
  if (cat) trail.push({ label: cat.label })
  if (sub) trail.push({ label: sub.label })
  return trail
})

const items = computed(() => {
  const { cat, sub } = current.value
  const kw = keyword.value.trim().toLowerCase()
  return demoEntries.filter((e) => {
    if (cat && e.category !== cat.key) return false
    if (sub && !sub.components.includes(e.name)) return false
    if (!kw) return true
    return e.name.toLowerCase().includes(kw) || e.rel.toLowerCase().includes(kw) || e.label.toLowerCase().includes(kw)
  })
})

/** 每格弹层是否展开：一律从收起起步——同分类页里多格自动展开会用模态层盖住整页，
    收起态配「预览弹层」按钮、点开后各格按自身 props 呈现差异才是可用示例 */
function isOpen(e: DemoEntry) {
  return openState[e.variantKey] === true
}

/**
 * 拼出示例单元格的绑定对象：受控弹层按形态挂不同开关属性。
 *
 * [参数] entry 该格的组件条目（含 variantKey 与弹层形态）
 * [返回] 传给单元格的 props 与事件绑定
 * 最近修改时间：2026-10-17 03:42:00；改动原因：状态键从 rel 升级为 variantKey，
 *   弹层开关初值统一为收起，并按路由两段决定父分类与子分组、不可路由层级只作文本面包屑。
 */
function bindOf(entry: DemoEntry) {
  const { state, handlers } = liveOf.get(entry.variantKey)!
  // 1. 非弹层组件直接透传受控状态与回写处理器
  if (!entry.overlay) return { ...state, ...handlers }
  const onClose = () => { openState[entry.variantKey] = false }
  // 2. 表格型弹层把样本表数据按开关状态下发
  if (entry.overlay === 'table') return { ...state, ...handlers, table: isOpen(entry) ? GEN_TABLE : null, onClose }
  // 3. visible 型弹层额外回写自身 visible
  if (entry.overlay === 'visible') {
    return { ...state, ...handlers, visible: isOpen(entry), 'onUpdate:visible': (v: boolean) => { openState[entry.variantKey] = v; state.visible = v } }
  }
  // 4. open 型弹层只下发 open 与关闭回调
  return { ...state, ...handlers, open: isOpen(entry), onClose }
}

/**
 * 取该格的受控状态，作为插槽参数透传给示例插槽函数。
 *
 * Tabs 这类「内容区由调用方数据驱动」的组件，default 插槽自身不透出选中键，
 * 插槽必须读到本格实时状态才能把面板 active 算出来；状态在渲染期读取，回写后随本格重渲染。
 *
 * [参数] entry 该格组件条目
 * [返回] Record<string, unknown> 该格受控状态
 */
function stateOf(entry: DemoEntry) {
  return liveOf.get(entry.variantKey)!.state
}

/**
 * 宿主类组件需要一次真实交互才出现，按钮调用全局组合式函数而不是组件自身 props。
 *
 * [参数] action 动作标识（toast / toast-danger / toast-info / confirm / confirm-danger / confirm-plain）
 * [返回] 无
 * 最近修改时间：2026-10-17 01:00:00；改动原因：为策展出的 tone 变体分派不同提示语义。
 */
function runAction(action: string) {
  if (action === 'toast') pushToast('这是一条演示提示', 'ok')
  else if (action === 'toast-danger') pushToast('这是一条失败演示提示', 'danger')
  else if (action === 'toast-info') pushToast('这是一条信息演示提示', 'info')
  else if (action === 'confirm-plain') void confirm({ title: '操作确认', message: '确定执行这条演示操作吗？' })
  else void confirm({ title: '删除确认', message: '确定要删除这条记录吗？', danger: true })
}
</script>

<template>
  <div class="gallery">
    <PageHeader :title="pageLabel" :desc="pageDesc">
      <template #spec><Breadcrumb :items="crumbs" /></template>
      <InputSearch v-model="keyword" allow-clear placeholder="搜索组件名 / 变体标签 / 路径" />
    </PageHeader>

    <EmptyState v-if="!items.length" title="没有匹配的组件" desc="换个关键词或切换到其他分类" />
    <div v-else class="gallery-grid">
      <DemoCell v-for="e in items" :key="e.variantKey" :name="e.name" :variant="e.label" :rel="e.rel" :guide="demoGuideOf(e.name, e.label, e.diff)">
        <Button v-if="e.overlay" variant="ghost" size="sm" @click="openState[e.variantKey] = true">预览弹层</Button>
        <Button v-else-if="e.action" variant="ghost" size="sm" @click="runAction(e.action)">触发宿主</Button>
        <div v-if="e.canvas !== null" class="gallery-canvas" :style="{ height: `${e.canvas}px` }">
          <component :is="e.comp" v-bind="bindOf(e)">
            <template v-for="(slot, key) in e.slots" :key="key" #[key]="p"><component :is="slot" v-bind="{ ...p, state: stateOf(e) }" /></template>
          </component>
        </div>
        <div v-else-if="e.frame" class="gallery-frame" :style="{ minHeight: `${e.frame.height ?? 72}px` }">
          <span v-if="e.frame.before" class="gallery-frame-side">{{ e.frame.before }}</span>
          <component :is="e.comp" v-bind="bindOf(e)">
            <template v-for="(slot, key) in e.slots" :key="key" #[key]="p"><component :is="slot" v-bind="{ ...p, state: stateOf(e) }" /></template>
          </component>
          <span v-if="e.frame.after" class="gallery-frame-side">{{ e.frame.after }}</span>
        </div>
        <component v-else :is="e.comp" v-bind="bindOf(e)">
          <template v-for="(slot, key) in e.slots" :key="key" #[key]="p"><component :is="slot" v-bind="{ ...p, state: stateOf(e) }" /></template>
        </component>
      </DemoCell>
    </div>
  </div>
</template>

<style>
/* 示例页只定义网格骨架，视觉取值全部来自组件库令牌，深色主题与密度随全局翻转。
   列数按断点写死而不是 auto-fill：自适应会把宽屏切成 5 列，每格只剩 250px 上下，
   组件被压到看不清细节；宽屏固定 3 列让每格拿到 320px 以上，示例才按真实尺寸呈现。
   降列断点按「三列每卡不低于 300px」反推：实测 1320px 视口三列只有 297px，
   比两列的 454px 更小，说明降列必须再往上收；1360px 起三列约 307px 才稳定大于
   中等宽度的两列卡宽，故 1360 以下降两列，820 以下与外壳移动断点对齐降单列。 */
.gallery { padding: 18px clamp(12px, 2.5vw, 30px) 40px; }
.gallery-grid { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 18px; margin-top: 14px; }
@media (max-width: 1359px) { .gallery-grid { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
@media (max-width: 820px) { .gallery-grid { grid-template-columns: minmax(0, 1fr); } }
/* 画布类组件用 absolute 铺满，必须给定位容器并由 height 内联决定档位；
   最小高度兜住 120px 以下的窄档，避免外壳类示例被压成一条看不清的横带 */
.gallery-canvas { position: relative; isolation: isolate; width: 100%; min-height: 200px; }
/* 画布容器的高度只归容器自己：关系图这类根节点没有固有高度（内部节点是 0 尺寸锚点），
   不继承父高的话会被自身 overflow:hidden 裁成 2px，整卡看不出内容 */
.gallery-canvas > :first-child { height: 100%; }
/* 并排外框给纵向分割线这类靠邻居撑开的组件补真实用法：
   组件走 align-self: stretch 才能拿到外框行高，两侧文字是它真正分隔的对象 */
.gallery-frame { display: flex; align-items: center; justify-content: center; gap: 12px; }
.gallery-frame-side { font-size: 13px; color: var(--ink-soft); white-space: nowrap; }
</style>
