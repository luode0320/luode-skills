import { reactive, watch } from 'vue'
import { ACCENT_PALETTES, DEFAULT_ACCENT } from '@/data/accent-palettes.generated'

/* 外观扩展维度：主色色板与字号档位。

   为什么单独成模块：上游的 `appearance.ts` 只管理主题、密度与导航折叠，且属逐字节冻结文件，
   不能在其上扩展。更要紧的是它会用整对象回写 `scaffold.appearance`——若把新字段塞进同一个键，
   任何一次主题或密度切换都会把新字段冲掉。所以这里用独立的 `scaffold.appearance.ext`。

   两个维度都只写根元素属性，组件靠 CSS 变量自动跟随，不需要任何组件感知。
   与主题、密度不同的是：这两个维度用不绑 `:root` 的选择器，因此可以打在任意容器上，
   只影响该子树（主题与密度绑死在 `:root`，只能全局切换）。 */

export type FontScale = 'compact' | 'regular' | 'large'

export interface AppearanceExt {
  accent: string
  fontScale: FontScale
}

const STORAGE_KEY = 'scaffold.appearance.ext'
const FONT_SCALES: readonly FontScale[] = ['compact', 'regular', 'large']

const DEFAULTS: AppearanceExt = { accent: DEFAULT_ACCENT, fontScale: 'regular' }

function load(): AppearanceExt {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const saved = JSON.parse(raw) as Partial<AppearanceExt>
      return {
        // 按生成器产出的色板清单校验：历史值里可能残留已删除的色板键，
        // 不校验会让选择器停在一个不存在的选中态上。
        accent: ACCENT_PALETTES.some(palette => palette.key === saved.accent)
          ? String(saved.accent)
          : DEFAULTS.accent,
        fontScale: FONT_SCALES.includes(saved.fontScale as FontScale)
          ? saved.fontScale as FontScale
          : DEFAULTS.fontScale,
      }
    }
  } catch { /* 存储不可用时使用默认值 */ }
  return { ...DEFAULTS }
}

export const appearanceExt = reactive<AppearanceExt>(load())

function apply() {
  const root = document.documentElement
  root.dataset.accent = appearanceExt.accent
  root.dataset.fontScale = appearanceExt.fontScale
}

watch(() => [appearanceExt.accent, appearanceExt.fontScale], apply, { immediate: true })

watch(appearanceExt, (value) => {
  try { localStorage.setItem(STORAGE_KEY, JSON.stringify(value)) } catch { /* 忽略 */ }
}, { deep: true })
