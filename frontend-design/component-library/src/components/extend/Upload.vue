<script setup lang="ts">
/* 上传：只做前端文件选择与列表管理，不做真实网络上传。
   选中文件后建一条 ready 记录入列表，列表项展示进度与移除按钮；进度由 autoUpload 模拟推进。 */
import { computed, ref } from 'vue'
import Icon from '@/components/Icon.vue'

export interface UploadFile {
  uid: string
  name: string
  size?: number
  status: 'ready' | 'uploading' | 'success' | 'error'
  percent?: number
  url?: string
}

const props = withDefaults(defineProps<{
  fileList?: UploadFile[]
  accept?: string
  multiple?: boolean
  disabled?: boolean
  limit?: number
  drag?: boolean
  autoUpload?: boolean
}>(), {
  fileList: () => [],
  limit: 0,
  drag: false,
  autoUpload: false,
})

const emit = defineEmits<{
  (e: 'change', fileList: UploadFile[]): void
  (e: 'remove', file: UploadFile): void
  (e: 'progress', file: UploadFile, percent: number): void
  (e: 'success', file: UploadFile): void
}>()

const input = ref<HTMLInputElement | null>(null)
const dragOver = ref(false)

/* 受控优先：外部传了 fileList 就用它，否则用内部记录 */
const files = computed<UploadFile[]>(() => props.fileList)

const reachLimit = computed(() => props.limit > 0 && props.fileList.length >= props.limit)

/** [参数] 无 [返回] 无：点击触发隐藏 input 的选文件 */
function openPicker() {
  if (props.disabled || reachLimit.value) return
  input.value?.click()
}

/** [参数] size 字节数 [返回] 可读尺寸文本 */
function prettySize(size?: number): string {
  if (!size) return ''
  if (size < 1024) return `${size} B`
  if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`
  return `${(size / 1024 / 1024).toFixed(1)} MB`
}

/** [参数] 无 [返回] 无：重置 input 值，保证同一文件可再次选择触发 change */
function resetInput() {
  if (input.value) input.value.value = ''
}

/** [参数] file 原始文件 [返回] 列表记录，uid 用时间戳加随机串兜底唯一 */
function toRecord(file: File): UploadFile {
  return {
    uid: `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`,
    name: file.name,
    size: file.size,
    status: 'ready',
    percent: 0,
  }
}

/**
 * [参数] raw 选中的原始文件数组
 * [返回] 无：过滤后按 limit 截断入列并广播 change
 *        进度推进走 setInterval 模拟，纯前端不发起真实请求
 */
function intake(raw: File[]) {
  const next = raw.map(toRecord)
  const merged = [...props.fileList, ...next].slice(0, props.limit > 0 ? props.limit : undefined)
  emit('change', merged)
  if (props.autoUpload) next.forEach(runProgress)
}

/**
 * [参数] file 列表记录
 * [返回] 无：逐格推进 percent，走完后置 success 并广播进度与成功
 */
function runProgress(file: UploadFile) {
  let percent = 0
  const timer = window.setInterval(() => {
    percent = Math.min(100, percent + 20)
    emit('progress', file, percent)
    if (percent >= 100) {
      window.clearInterval(timer)
      emit('success', file)
    }
  }, 220)
}

/** [参数] event 选择事件 [返回] 无：取文件列表交给 intake 并复位 input */
function onPick(event: Event) {
  const list = (event.target as HTMLInputElement).files
  if (list?.length) intake(Array.from(list))
  resetInput()
}

/** [参数] event 拖拽落点事件 [返回] 无：拖入文件同样走 intake */
function onDrop(event: DragEvent) {
  dragOver.value = false
  if (props.disabled || reachLimit.value) return
  const list = event.dataTransfer?.files
  if (list?.length) intake(Array.from(list))
}

/** [参数] 无 [返回] 无：移除一条记录并广播 remove 与 change */
function remove(file: UploadFile) {
  const next = props.fileList.filter(f => f.uid !== file.uid)
  emit('remove', file)
  emit('change', next)
}
</script>

<template>
  <div :class="['x-upload', disabled && 'is-disabled']">
    <div
      v-if="drag"
      :class="['x-upload-drop', dragOver && 'is-over', disabled && 'is-disabled']"
      role="button"
      :tabindex="disabled ? -1 : 0"
      aria-label="点击或拖拽文件到此处"
      @click="openPicker"
      @keydown.enter.prevent="openPicker"
      @keydown.space.prevent="openPicker"
      @dragover.prevent="dragOver = true"
      @dragleave="dragOver = false"
      @drop.prevent="onDrop"
    >
      <span class="x-upload-ico m-groove"><Icon name="upload" :size="20" /></span>
      <span class="x-upload-main">点击或拖拽文件到此处</span>
      <span v-if="accept" class="x-upload-hint">支持 {{ accept }}</span>
    </div>
    <button
      v-else
      type="button"
      class="btn btn-secondary"
      :disabled="disabled || reachLimit"
      @click="openPicker"
    >
      <Icon name="upload" :size="16" />
      <span>选择文件</span>
    </button>

    <input
      ref="input"
      class="sr-only"
      type="file"
      :accept="accept"
      :multiple="multiple"
      :disabled="disabled"
      @change="onPick"
    />

    <ul v-if="files.length" class="x-upload-list">
      <li v-for="file in files" :key="file.uid" class="x-upload-item m-groove">
        <span class="x-upload-name ellipsis">{{ file.name }}</span>
        <span class="x-upload-size tnum">{{ prettySize(file.size) }}</span>
        <span :class="['tag', file.status === 'success' ? 'tone-ok' : file.status === 'error' ? 'tone-danger' : 'tone-info']">
          {{ file.status === 'success' ? '完成' : file.status === 'error' ? '失败' : file.status === 'uploading' ? '上传中' : '待处理' }}
        </span>
        <span v-if="file.status === 'uploading'" class="x-upload-bar">
          <span class="x-upload-fill" :style="{ width: `${file.percent ?? 0}%` }" />
        </span>
        <button
          type="button"
          class="icon-btn icon-btn-sm"
          :aria-label="`移除 ${file.name}`"
          :disabled="disabled"
          @click="remove(file)"
        ><Icon name="x" :size="14" /></button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.x-upload { display: flex; flex-direction: column; gap: 10px; }
.x-upload.is-disabled { opacity: .6; }
.x-upload-drop {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 24px;
  border: 1px dashed var(--line-strong);
  border-radius: var(--r-md);
  background: var(--input-bg);
  box-shadow: var(--edge);
  cursor: pointer;
  transition: border-color .2s ease, background .2s ease;
}
.x-upload-drop:hover,
.x-upload-drop.is-over { border-color: var(--blue); background: var(--blue-soft); }
.x-upload-drop.is-disabled { cursor: not-allowed; }
.x-upload-drop:focus-visible { outline: 2px solid var(--focus); outline-offset: 2px; }
.x-upload-ico {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--r-sm);
  color: var(--ink-faint);
}
.x-upload-main { font-size: 13px; font-weight: 620; color: var(--ink); }
.x-upload-hint { font-size: 12px; color: var(--ink-faint); }
.x-upload-list { display: flex; flex-direction: column; gap: 6px; margin: 0; padding: 0; list-style: none; }
.x-upload-item {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  min-height: 40px;
  padding: 0 8px 0 12px;
  border-radius: var(--r-sm);
}
.x-upload-name { flex: 1; min-width: 0; font-size: 13px; color: var(--ink); }
.x-upload-size { flex: none; font-size: 12px; color: var(--ink-faint); }
.x-upload-bar {
  position: absolute;
  left: 12px;
  right: 12px;
  bottom: 4px;
  height: 2px;
  border-radius: 999px;
  background: var(--line-strong);
  overflow: hidden;
}
.x-upload-fill { display: block; height: 100%; border-radius: 999px; background: var(--blue); transition: width .22s ease; }
</style>
