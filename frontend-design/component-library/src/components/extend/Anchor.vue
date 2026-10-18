<script setup lang="ts">
/* 锚点导航：列出页内小节，点击平滑滚动，滚动时按可见性高亮当前小节。
   高亮交给 IntersectionObserver，点击落点用 offsetTop 补偿固定头部高度。 */
import { onBeforeUnmount, onMounted, reactive, ref, watch } from 'vue'

export interface AnchorItem {
  id: string
  title: string
  /** 缩进层级，0 为顶层 */
  depth?: number
}

const props = withDefaults(defineProps<{
  items: AnchorItem[]
  /** 滚动落点上方预留的高度，通常等于固定头部高度 */
  offsetTop?: number
}>(), {
  offsetTop: 0,
})

const active = ref('')
const visible = reactive(new Set<string>())
let observer: IntersectionObserver | null = null

/** [参数] item 目标小节 [返回] 无；平滑滚到小节顶部并扣掉预留高度 */
function go(item: AnchorItem) {
  const el = document.getElementById(item.id)
  if (!el) return
  active.value = item.id
  window.scrollTo({ top: el.getBoundingClientRect().top + window.scrollY - props.offsetTop, behavior: 'smooth' })
}

/** [参数] 无 [返回] 无；按 items 重建观察列表，取阅读序里第一个可见小节作为高亮项 */
function observe() {
  observer?.disconnect()
  visible.clear()
  if (!props.items.length) return
  observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      const id = (entry.target as HTMLElement).dataset.xAnchor
      if (!id) return
      if (entry.isIntersecting) visible.add(id)
      else visible.delete(id)
    })
    const hit = props.items.find(item => visible.has(item.id))
    if (hit) active.value = hit.id
  }, { rootMargin: `-${props.offsetTop}px 0px -60% 0px`, threshold: 0 })
  props.items.forEach((item) => {
    const el = document.getElementById(item.id)
    if (!el) return
    el.dataset.xAnchor = item.id
    observer?.observe(el)
  })
}

onMounted(observe)
onBeforeUnmount(() => observer?.disconnect())
watch(() => props.items.map(item => item.id).join('\u0000'), observe)
</script>

<template>
  <nav class="x-anchor" aria-label="页内导航">
    <span class="x-anchor-rail" aria-hidden="true" />
    <a
      v-for="item in items"
      :key="item.id"
      class="x-anchor-link"
      :class="{ 'is-active': item.id === active }"
      :href="`#${item.id}`"
      :style="{ paddingLeft: `${10 + (item.depth ?? 0) * 14}px` }"
      :aria-current="item.id === active ? 'location' : undefined"
      @click.prevent="go(item)"
    >{{ item.title }}</a>
  </nav>
</template>

<style scoped>
.x-anchor { position: relative; display: flex; flex-direction: column; gap: 2px; }
/* 左侧竖轨：高亮条压在它上面，形成「当前项」的定位感 */
.x-anchor-rail { position: absolute; left: 0; top: 4px; bottom: 4px; width: 1px; background: var(--line-strong); }
.x-anchor-link {
  position: relative;
  display: block;
  padding: 6px 10px;
  border-radius: var(--r-xs);
  font-size: 13px;
  line-height: 1.4;
  color: var(--ink-muted);
  text-decoration: none;
  transition: color .2s ease, background .2s ease;
}
.x-anchor-link:hover { color: var(--ink); background: var(--hover-bg); }
.x-anchor-link.is-active { color: var(--blue); font-weight: 620; background: var(--blue-soft); }
.x-anchor-link.is-active::before {
  content: '';
  position: absolute;
  left: -1px;
  top: 6px;
  bottom: 6px;
  width: 2px;
  border-radius: 9999px;
  background: var(--blue);
}
</style>
