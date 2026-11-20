<script setup lang="ts">
/* 组件库侧栏导航：把「父分类标题 + 平铺子项」改成可折叠分组。
   上游 `layout/Sidebar.vue` 逐字节冻结，这里以「缝隙追加一行挂载」的方式接管画廊路由下的导航，
   原有的平铺分组由 overrides.css 的 `:has(> .gn)` 规则隐藏，冻结文件零改动。

   为什么默认只展开当前分类：分类共 6 个、子项 100+，全展开等于回到平铺长列表，
   折叠就失去意义；只在用户点过之后才按他的选择持久化。 */
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Icon from '@/components/Icon.vue'
import { navGroups } from '@/composables/auth'
import { appearance } from '@/composables/appearance'
import { slideThumb } from '@/composables/motion'

const STORAGE_KEY = 'scaffold.galleryNav.open'

const route = useRoute()
const router = useRouter()
const nav = ref<HTMLElement | null>(null)
const host = ref<HTMLElement | null>(null)

/** 只在画廊路由接管；后台其它页面仍走上游侧栏 */
const isGallery = computed(() => route.path.startsWith('/gallery'))
const activeKey = computed(() => String(route.name ?? ''))

/* 示例页里的 AppShell 也会挂这个组件（它挂的是同一个冻结侧栏）。
   那里是「外壳的样本」，必须保持上游的平铺形态，否则演示卡的侧栏会被接管、
   卡内还会多出一整套导航。挂在 .g-cell 里就一律不接管。 */
const inDemoCell = ref(true)

/* 侧栏整体收成图标模式时不接管：分组头只剩条目数和箭头，标签被裁掉后
   一列「6 / 8 / 23」毫无意义，比上游的图标列表更糟。这个模式交还上游。 */
const ready = computed(() => isGallery.value && !inDemoCell.value && !appearance.railCollapsed)

onMounted(() => {
  inDemoCell.value = Boolean(host.value?.closest('.g-cell'))
})

/* 接管条件可能因为路由或侧栏形态变化而翻转，进入接管态时才做初始化 */
watch(ready, (on) => {
  if (!on) return
  seed()
  nextTick(() => syncThumb(true))
}, { immediate: true })

/** 当前路由落在哪个分类里 —— 决定默认展开项与「收起但有活动项」的提示 */
const activeGroupKey = computed(
  () => navGroups.value.find(g => g.items.some(i => i.key === activeKey.value))?.key ?? '',
)

const open = ref<Set<string>>(new Set())

function readStored(): string[] | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const arr = raw ? JSON.parse(raw) : null
    return Array.isArray(arr) ? arr.filter((k): k is string => typeof k === 'string') : null
  } catch {
    return null
  }
}

function persist() {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([...open.value]))
  } catch {
    /* 隐私模式下写入会抛，忽略即可，不影响本次会话 */
  }
}

/** 首次进入：只展开当前所在分类，没有则展开第一个 */
function seed() {
  const stored = readStored()
  if (stored?.length) {
    open.value = new Set(stored)
    return
  }
  const first = activeGroupKey.value || navGroups.value[0]?.key || ''
  open.value = new Set(first ? [first] : [])
}

function toggle(key: string) {
  const next = new Set(open.value)
  if (next.has(key)) next.delete(key)
  else next.add(key)
  open.value = next
  persist()
}

function go(path: string) {
  if (route.path !== path) router.push(path)
}

/** 滑动玻璃块：只给「含活动项且展开」的那一组挂 thumb，位置对齐活动项 */
function syncThumb(instant = false) {
  const list = nav.value?.querySelector<HTMLElement>('.gn-list.is-active-list')
  if (!list) return
  const thumb = list.querySelector<HTMLElement>('.nav-thumb')
  const item = list.querySelector<HTMLElement>('.nav-item.is-active')
  slideThumb(thumb, item, 'y', instant)
}

/* 路由变化：确保目标分类是展开的，否则点了子项却看不见自己 */
watch(activeKey, async () => {
  if (!ready.value) return
  const key = activeGroupKey.value
  if (key && !open.value.has(key)) {
    open.value = new Set([...open.value, key])
    persist()
  }
  await nextTick()
  syncThumb()
})

watch(open, () => nextTick(() => syncThumb()), { deep: true })

/* 分组数据是异步来的（登录后才有），到了再校正一次展开项 */
watch(navGroups, (list) => {
  if (!list.length) return
  if (!open.value.size) seed()
  nextTick(() => syncThumb(true))
})

onBeforeUnmount(() => {
  /* 组件卸载时把持久化结果留着，下次进来沿用用户的选择 */
})
</script>

<template>
  <!-- 外层常驻：要靠它判断自己是不是长在示例卡里，所以不能一起 v-if 掉 -->
  <div ref="host" class="gn-host">
    <div v-if="ready" ref="nav" class="gn">
    <div
      v-for="group in navGroups"
      :key="group.key"
      :class="['gn-group', !group.single && !open.has(group.key) && group.key === activeGroupKey && 'has-active']"
    >
      <button
        v-if="!group.single"
        type="button"
        class="gn-head"
        :class="open.has(group.key) && 'is-open'"
        :aria-expanded="open.has(group.key)"
        :aria-controls="`gn-body-${group.key}`"
        @click="toggle(group.key)"
      >
        <span class="gn-head-label">{{ group.label }}</span>
        <span class="gn-head-count">{{ group.items.length }}</span>
        <Icon class="gn-chevron" name="chevronRight" :size="14" />
      </button>

      <div
        :id="`gn-body-${group.key}`"
        class="gn-body"
        :class="open.has(group.key) && 'is-open'"
        :inert="!group.single && !open.has(group.key) ? true : undefined"
      >
        <div class="gn-inner">
          <div
            :class="['nav-list', 'gn-list', group.key === activeGroupKey && 'is-active-list']"
            :data-key="group.key"
          >
            <span v-if="group.key === activeGroupKey" class="nav-thumb m-pill" aria-hidden="true" />
            <button
              v-for="item in group.items"
              :key="item.key"
              type="button"
              :class="['nav-item', item.key === activeKey && 'is-active']"
              :aria-current="item.key === activeKey ? 'page' : undefined"
              @click="go(item.path)"
            >
              <Icon class="nav-ico" :name="item.icon" :size="18" />
              <span class="nav-label">{{ item.label }}</span>
            </button>
          </div>
        </div>
      </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* 外层只是身份探针，不参与布局：display:contents 让它不产生盒子，
   .gn 直接落进 .rail-nav 的流里，间距与上游一致 */
.gn-host { display: contents; }

.gn { display: flex; flex-direction: column; gap: 2px; }
.gn-group + .gn-group { margin-top: 2px; }

/* 分类头：整行可点，右侧 chevron 指向「点开」而不是「已展开」 */
.gn-head {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 30px;
  padding: 0 10px;
  border-radius: var(--r-xs);
  font-size: var(--fs-caption);
  font-weight: 650;
  letter-spacing: .06em;
  /* 用 --ink-soft 而不是 --ink-faint：后者是「元信息」档，3.1:1 达不到正文 AA，
     而分类头是可点的文字，13 个分组一屏里最需要读清的就是它 */
  color: var(--ink-soft);
  text-align: left;
  transition: color var(--dur-hover) var(--ease-reveal), background var(--dur-hover) var(--ease-reveal);
}
.gn-head:hover { color: var(--ink); background: var(--hover-bg); }
.gn-head:focus-visible { outline-offset: -2px; }

.gn-head-label {
  flex: 1;
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* 收起时显示条目数：让用户知道点开值不值得，而不是盲开。
   字号守 12px 下限（辅助字号 ≥12px 是验收条件），不靠压小 + 降透明度做层级——
   那样会掉到 3:1 以下，等于用一个读不清的数字换一点视觉安静。 */
.gn-head-count {
  flex: none;
  font-size: var(--fs-caption);
  font-weight: 500;
  font-variant-numeric: tabular-nums;
  color: var(--ink-soft);
}

.gn-chevron {
  flex: none;
  color: var(--ink-faint);
  transition: transform var(--dur-swap) var(--ease-swap);
}
.gn-head.is-open .gn-chevron { transform: rotate(90deg); }
.gn-head.is-open { color: var(--ink-muted); }

/* 收起但里面有当前页：留一个蓝点 + 蓝色标题，否则用户会以为导航丢了 */
.gn-group.has-active > .gn-head .gn-head-label { color: var(--blue); }
.gn-group.has-active > .gn-head .gn-head-count {
  color: var(--blue);
  opacity: 1;
}

/* 折叠动画走 grid-template-rows 0fr↔1fr：比 max-height 可靠，不需要猜高度 */
.gn-body {
  display: grid;
  grid-template-rows: 0fr;
  transition: grid-template-rows var(--dur-swap) var(--ease-swap);
}
.gn-body.is-open { grid-template-rows: 1fr; }
.gn-inner { min-height: 0; overflow: hidden; }

.gn-list { padding-top: 2px; padding-bottom: 2px; }

/* 上游 .nav-thumb 的 left/right 12px 是相对 .rail-nav 内边距算的；这里的 .gn-list
   已经在同样的内边距里，再套一次会双重内缩（实测项目 207px、玻璃块只有 183px，
   两边各差 12px），玻璃块就盖不住整行。归零让它对齐项目宽度。 */
.gn-list .nav-thumb { left: 0; right: 0; }
</style>
