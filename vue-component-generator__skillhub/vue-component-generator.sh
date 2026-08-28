#!/usr/bin/env bash
# vue-component-generator v1.1.0 — Vue 3 SFC 组件生成器
# 支持 Composition API / Options API / <script setup>，可选 TypeScript 与 SCSS。
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

VERSION="1.1.0"
API="composition"
TS=false
SCSS=false
OUTPUT="."

usage() {
  cat << 'EOF'
用法: vue-component-generator.sh <组件名(PascalCase)> [选项]

生成一个 Vue 3 单文件组件（SFC）。

参数:
  组件名                必填，PascalCase 命名，如 MyButton

选项:
  --api, -a <type>      API 风格: composition(默认) | options | script-setup
  --typescript, -t      启用 TypeScript（composition/script-setup 带类型标注）
  --scss, -s            样式使用 SCSS（<style scoped lang="scss">）
  --output, -o <dir>    输出目录（默认当前目录，自动创建）
  --help, -h            显示帮助
  --version, -v         显示版本

示例:
  bash vue-component-generator.sh MyButton
  bash vue-component-generator.sh MyModal --api options
  bash vue-component-generator.sh MyForm --typescript --scss
  bash vue-component-generator.sh UserCard --api script-setup -o src/components
EOF
}

# ---- 参数解析 ----
NAME=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --api|-a)
      API="${2:-}"
      if [[ -z "$API" ]]; then echo "错误: --api 需要参数 (composition/options/script-setup)"; exit 1; fi
      shift 2
      ;;
    --typescript|-t) TS=true; shift ;;
    --scss|-s) SCSS=true; shift ;;
    --output|-o)
      OUTPUT="${2:-}"
      if [[ -z "$OUTPUT" ]]; then echo "错误: --output 需要目录参数"; exit 1; fi
      shift 2
      ;;
    --help|-h) usage; exit 0 ;;
    --version|-v) echo "vue-component-generator $VERSION"; exit 0 ;;
    -*) echo "错误: 未知选项 $1"; usage; exit 1 ;;
    *) NAME="$1"; shift ;;
  esac
done

# ---- 校验 ----
if [[ -z "$NAME" ]]; then
  echo "错误: 缺少组件名（PascalCase，如 MyButton）"
  usage
  exit 1
fi
if ! [[ "$NAME" =~ ^[A-Z][A-Za-z0-9]*$ ]]; then
  echo "错误: 组件名必须为 PascalCase（首字母大写，如 MyButton）"
  exit 1
fi
case "$API" in
  composition|options|script-setup) ;;
  *) echo "错误: --api 仅支持 composition/options/script-setup，收到 '$API'"; exit 1 ;;
esac

# ---- 派生名 ----
# MyButton -> my-button；MyAPIClient -> my-api-client（先拆连续大写，再拆普通边界）
CLASS="$(echo "$NAME" | sed -E 's/([A-Z])([A-Z][a-z])/\1-\2/g; s/([a-z0-9])([A-Z])/\1-\2/g' | tr '[:upper:]' '[:lower:]')"
STYLE_LANG=""
if [[ "$SCSS" == true ]]; then STYLE_LANG=' lang="scss"'; fi

# ---- 平台兼容的 sed -i（GNU: sed -i "..."；BSD/macOS: sed -i "" "..."） ----
if sed --version >/dev/null 2>&1; then
  SED_I=(sed -i)
else
  SED_I=(sed -i "")
fi

mkdir -p "$OUTPUT"
FILE="$OUTPUT/$NAME.vue"

# ---- 模板生成（引号 heredoc 保证 $ 字面；占位符事后替换） ----
case "$API" in
  composition)
    if [[ "$TS" == true ]]; then
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <button type="button" @click="handleClick">
      {{ label }}
    </button>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Props {
  label?: string
}

const props = withDefaults(defineProps<Props>(), {
  label: 'Click me'
})

const emit = defineEmits<{
  (e: 'click', value: number): void
}>()

const count = ref(0)

const handleClick = () => {
  emit('click', count.value)
}
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    else
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <button type="button" @click="handleClick">
      {{ label }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  label: {
    type: String,
    default: 'Click me'
  }
})

const emit = defineEmits(['click'])

const count = ref(0)

const handleClick = () => {
  emit('click', count.value)
}
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    fi
    ;;

  options)
    if [[ "$TS" == true ]]; then
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <button type="button" @click="handleClick">
      {{ label }}
    </button>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: '__NAME__',
  props: {
    label: {
      type: String,
      default: 'Click me'
    }
  },
  emits: ['click'],
  data() {
    return {
      count: 0 as number
    }
  },
  methods: {
    handleClick() {
      this.$emit('click', this.count)
    }
  }
})
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    else
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <button type="button" @click="handleClick">
      {{ label }}
    </button>
  </div>
</template>

<script>
export default {
  name: '__NAME__',
  props: {
    label: {
      type: String,
      default: 'Click me'
    }
  },
  emits: ['click'],
  data() {
    return {
      count: 0
    }
  },
  methods: {
    handleClick() {
      this.$emit('click', this.count)
    }
  }
}
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    fi
    ;;

  script-setup)
    if [[ "$TS" == true ]]; then
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <p>{{ label }}</p>
  </div>
</template>

<script setup lang="ts">
withDefaults(defineProps<{ label?: string }>(), {
  label: 'Click me'
})

defineEmits<{
  (e: 'click', value: number): void
}>()
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    else
      cat > "$FILE" << 'EOF'
<template>
  <div class="__CLASS__">
    <p>{{ label }}</p>
  </div>
</template>

<script setup>
defineProps({
  label: {
    type: String,
    default: 'Click me'
  }
})

defineEmits(['click'])
</script>

<style scoped__STYLE_LANG__>
.__CLASS__ {
  /* component styles */
}
</style>
EOF
    fi
    ;;
esac

# ---- 占位符替换 ----
"${SED_I[@]}" "s/__CLASS__/$CLASS/g; s/__NAME__/$NAME/g; s#__STYLE_LANG__#$STYLE_LANG#g" "$FILE"

echo "Vue component generated: $FILE"
echo "  api=$API typescript=$TS scss=$SCSS"
