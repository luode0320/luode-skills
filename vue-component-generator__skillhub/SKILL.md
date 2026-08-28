---
name: vue-component-generator
description: 生成 Vue 3 单文件组件（SFC）模板代码。支持 Composition API、Options API、script setup 语法、TypeScript 与 SCSS，一键产出 props/emits/样式齐全的组件。适用于组件生成、组件模板、SFC 脚手架、Vue 组件代码产出等场景。
metadata: {"version":"1.1.0","clawdbot":{"emoji":"💚","requires":{},"primaryEnv":""}}
---

# Vue Component Generator

快速生成 Vue 3 单文件组件（SFC）代码：三种 API 风格可选，支持 TypeScript 类型标注与 SCSS 样式，产出 props/emits/样式齐全的组件骨架。

## 适用边界

**适用**：

- 需要快速搭建新组件的代码骨架（按钮、表单、模态框、卡片等）
- 需要固定 API 风格（Composition / Options / `<script setup>`）的团队模板
- 需要 TypeScript 类型标注或 SCSS 样式的组件起步代码
- 脚手架初始化、教学演示、组件库起步

**不适用**：

- 已有组件库（Element Plus / Naive UI 等）时，应优先复用库内组件，不重复造轮子
- 仅需要「组件怎么设计」的规范指导（组件边界、props/emits 合约、目录结构）——那是 `vue-best-practices` 的职责
- 需要排查 Vue 运行时/响应式陷阱（ref 取组件实例、Teleport、onMounted 时序等）——那是 `vue__skillhub` 的职责
- 需要路由级组件或导航守卫模式——那是 `vue-router-best-practices` 的职责

## 使用流程

1. **识别组件需求**：输入=组件名（PascalCase）、职责、需要的 props/emits 清单 → 输出=生成参数草案
2. **选定生成参数**：输入=草案 → 输出=完整 CLI 命令。按团队规范选 `--api` 风格，按项目技术栈决定 `--typescript` / `--scss`，按目录结构决定 `--output`
3. **生成组件**：输入=CLI 命令 → 输出=目标目录下的完整 SFC 文件。从 skill 根目录执行脚本（见「快速开始」）
4. **验收**：输入=生成的 SFC → 输出=已核对、已补充交互逻辑的可用组件。按「验收清单」逐项核对；模板未覆盖的交互逻辑（异步、状态机、动画）在骨架内补充

## 快速开始

先进入本 skill 目录（脚本依赖相对路径），再执行：

```bash
cd <skill根目录>/vue-component-generator__skillhub   # 例如: cd /d/谷歌云盘/luode-skills/vue-component-generator__skillhub

# Composition API（默认）
bash vue-component-generator.sh MyButton

# Options API
bash vue-component-generator.sh MyModal --api options

# <script setup> + TypeScript + SCSS，输出到指定目录
bash vue-component-generator.sh UserCard --api script-setup --typescript --scss -o src/components
```

脚本同时支持从任意目录以绝对路径调用（内部已自定位，不依赖 cwd）。

## 能力矩阵

| 选项 | 别名 | 默认 | 行为 |
|---|---|---|---|
| `<组件名>` | — | 必填 | PascalCase 命名校验（首字母大写）；非法命名 exit 1 |
| `--api <type>` | `-a` | `composition` | `composition` / `options` / `script-setup` 三选一；非法值 exit 1 |
| `--typescript` | `-t` | 关 | 生成 `<script setup lang="ts">` 或 `<script lang="ts">`，props/emits 带类型标注 |
| `--scss` | `-s` | 关 | 样式块带 `lang="scss"` |
| `--output <dir>` | `-o` | 当前目录 | 输出到指定目录（自动创建） |
| `--help` | `-h` | — | 显示用法 |
| `--version` | `-v` | — | 显示版本 1.1.0 |

生成内容随 API 风格变化：

| 能力 | composition | options | script-setup |
|---|---|---|---|
| props 定义 | `defineProps` | `props` 选项 | `defineProps` |
| emits 定义 | `defineEmits` | `emits` 选项 | `defineEmits` |
| 状态与交互 | `ref` + 方法 | `data` + `methods` | 极简（仅 props/emits） |
| TS 标注 | `defineProps<Props>` + `withDefaults` | `defineComponent` + `data as number` | `defineProps<{...}>` 泛型 |

## 内联模板速查

不运行脚本时，以下最小模板可直接作为手写起点。

**Composition API（推荐）**：

```vue
<template>
  <div class="my-button">
    <button type="button" @click="handleClick">{{ label }}</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: { type: String, default: 'Click me' }
})

const emit = defineEmits(['click'])
const count = ref(0)

const handleClick = () => emit('click', count.value)
</script>

<style scoped>
.my-button { /* component styles */ }
</style>
```

**TypeScript 版（composition）**：

```vue
<script setup lang="ts">
import { ref } from 'vue'

interface Props { label?: string }
const props = withDefaults(defineProps<Props>(), { label: 'Click me' })

const emit = defineEmits<{ (e: 'click', value: number): void }>()
const count = ref(0)
</script>
```

**Options API**：

```vue
<script>
export default {
  name: 'MyModal',
  props: { visible: { type: Boolean, default: false } },
  emits: ['close'],
  data() { return { /* state */ } },
  methods: { handleClose() { this.$emit('close') } }
}
</script>
```

**`<script setup>` 极简版**（无组合逻辑，仅 props/emits 声明）：

```vue
<script setup>
defineProps({
  label: { type: String, default: 'Click me' }
})

defineEmits(['click'])
</script>
```

## 验收清单

生成后逐项核对：

- [ ] 组件名为 PascalCase，文件名与组件名一致（`MyButton.vue`）
- [ ] `props` 已定义（类型 + 默认值），未被模板引用的 props 已删除
- [ ] `emits` 已声明，`$emit`/`emit` 调用与声明一致
- [ ] 模板根节点 class 为组件名 kebab-case（`MyButton` → `my-button`）
- [ ] 样式块带 `scoped`；使用 SCSS 时含 `lang="scss"`
- [ ] TypeScript 模式：props/emits 均有类型标注，无隐式 `any`
- [ ] 输出文件位于 `--output` 指定目录，无覆盖风险（脚本直接覆盖同名文件，重名前确认）

## 环境自检

```bash
command -v bash && command -v sed
```

- 依赖 `bash`（4.0+，含 `[[ ]]` 与 `${var:-}`）与 `sed`（含 `-i` 与 `-E`）——Git Bash / WSL / MSYS2 / macOS 均自带
- 无 `bash`/`sed` 时脚本不可用，但本页「内联模板速查」仍可手工产出组件

## 相关技能

- `vue-best-practices`：组件设计规范（组件边界、props/emits 合约、目录结构）——生成前先读
- `vue__skillhub`：Vue 3 陷阱速查（ref 取实例、Teleport、响应式）——生成后排查运行时问题
- `vue-router-best-practices`：路由级组件与导航模式——涉及路由组件时配合使用
