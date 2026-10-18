/* 数据输入类策展变体：机械派生只能覆盖 enum/boolean/number 三类契约，
   值域不同 / 受控状态切换 / 插槽内容变化等语义维度需人工补齐，
   与 base、generated 归并后每类组件恰好 ≥3 组可用示例。
   最近修改时间：2026-10-17 11:07:00；改动原因：日期时间族迁出到 curated-datetime，
   本文件补空值占位与多值状态等真实可见差异，并合并重复的对象字面量键。 */
import { h } from 'vue'
import Radio from '../../components/extend/Radio.vue'
import TextInput from '../../components/ui/TextInput.vue'
import type { VariantShape } from './demo-variants.types'

/** 输入类组件的策展变体：标签写明差异点，值必须与基础示例不同，否则守卫判为伪变体 */
export const CURATED_INPUTS: Record<string, VariantShape[]> = {
  ColorPicker: [
    /* presets 只在打开面板后渲染，modelValue='' 会被组件回落到同一个默认色，
       两种写法在任何状态下都与基础格看不出差别，故改为收起态就可见的 showText 差异 */
    { label: '自定义色板', props: { presets: ['#236de9', '#3f9d54', '#d97b2b', '#c0392b'] } },
    { label: '不显示色值', props: { showText: false } },
  ],
  CheckboxGroup: [
    { label: '未勾选', props: { modelValue: [] } },
    { label: '只勾 B', props: { modelValue: ['b'] } },
    { label: '勾满三项', props: { modelValue: ['a', 'b', 'c'] } },
  ],
  CollapseItem: [
    { label: '禁用项', props: { name: 'x', title: '禁用面板', disabled: true } },
    { label: '长标题', props: { name: 'y', title: '权限变更审计与回滚记录' } },
    { label: '带正文', props: { name: 'z', title: '展开后可见正文' }, slots: { default: () => h('p', {}, '折叠项正文内容。') } },
  ],
  Field: [
    { label: '错误态', props: { error: '请输入姓名' } },
    { label: '通栏跨度', props: { wide: true, span: true } },
    { label: '分组容器', props: { group: true } },
  ],
  InputGroup: [
    /* 契约只有 direction 一项且基础已横排：竖排改走插槽差异，两行独立输入框 */
    {
      label: '竖排两栏',
      props: { direction: 'vertical' },
      slots: {
        default: () => [
          h(TextInput, { modelValue: '总部', placeholder: '部门' }),
          h(TextInput, { modelValue: '罗德', placeholder: '负责人' }),
        ],
      },
    },
    { label: '插槽内容差异', slots: { default: () => [h(TextInput, { modelValue: '研发部', placeholder: '子部门' })] } },
  ],
  Form: [
    /* 基础示例：两字段必填校验，竖排。这里给「填全可提交」与「只填一项」两种真实可用态，
       再加上派生已覆盖的行内布局 */
    {
      label: '已填全可提交',
      props: { model: { name: '罗德', phone: '13800000001' } },
    },
    {
      label: '只填姓名',
      props: { model: { name: '罗德', phone: '' } },
    },
  ],
  /* 文本/搜索类：基础格都已 clearable，机械派生覆盖 disabled / clearable，
     这里补空值占位与另一组候选，让输入框在收起态也能看出差别 */
  AutoComplete: [
    { label: '空值占位', props: { modelValue: '', placeholder: '输入姓名首字' } },
    { label: '已选林可', props: { modelValue: '林可' } },
  ],
  Cascader: [
    { label: '未选占位', props: { modelValue: [], placeholder: '请选择部门层级' } },
    { label: '选中分公司', props: { modelValue: [2, 21] } },
  ],
  Checkbox: [
    { label: '未勾选', props: { modelValue: false } },
    { label: '半选态', props: { modelValue: false, indeterminate: true } },
  ],
  Mention: [
    { label: '单行高', props: { rows: 1, modelValue: '@林可 ' } },
    { label: '提及两人', props: { modelValue: '@罗德 @林可 ' } },
  ],
  InputNumber: [
    { label: '禁用', props: { disabled: true } },
    { label: '两位小数', props: { precision: 2, step: 0.01, modelValue: 12.34 } },
    { label: '空值占位', props: { modelValue: null, placeholder: '输入数量' } },
  ],
  /* 日期与时间族契约同形、差异维度集中在占位与格式，已整体迁到 demo-variants.curated-datetime.ts */
  InputPassword: [
    { label: '默认可见', props: { defaultVisible: true } },
    { label: '禁用', props: { disabled: true } },
    { label: '空值占位', props: { modelValue: '', placeholder: '请输入初始密码' } },
  ],
  InputTag: [
    /* max=3 / allowDuplicate 在两条标签的样本下都看不出差异（未达上限、也没重复项），
       改成标签数量与空态占位这两项目录里立刻可见的差别 */
    { label: '四个标签换行', props: { modelValue: ['系统管理', '监控管理', '系统工具', '审计日志'] } },
    { label: '空值带占位', props: { modelValue: [], placeholder: '输入后回车添加标签' } },
    { label: '单个标签', props: { modelValue: ['系统管理'] } },
  ],
  CascaderPanel: [
    { label: '窄列宽', props: { columnWidth: 100 } },
    { label: '宽列宽', props: { columnWidth: 180 } },
    { label: '限高滚动', props: { maxHeight: 96, columnWidth: 140 } },
  ],
  VerificationCode: [
    { label: '四位', props: { length: 4, modelValue: '1234' } },
    { label: '空值占位', props: { modelValue: '' } },
  ],
  Upload: [
    { label: '限制三个', props: { limit: 3 } },
    { label: '仅收图片', props: { accept: 'image/*' } },
    { label: '手动上传', props: { autoUpload: false } },
  ],
  Transfer: [
    { label: '自定义标题', props: { titles: ['待授权', '已授权'] } },
    { label: '全部已选', props: { modelValue: [1, 2, 3] } },
    { label: '可搜索', props: { searchable: true } },
    { label: '禁用', props: { disabled: true } },
  ],
  GridCol: [
    { label: '偏移六列', props: { span: 12, offset: 6 } },
    { label: '右侧推两列', props: { span: 12, push: 2 } },
    { label: '响应式窄屏', props: { span: 24, sm: 12 } },
  ],
  Radio: [
    { label: '禁用', props: { disabled: true } },
    { label: '未选中', props: { value: 'b', modelValue: 'a' } },
    { label: '长文案', props: { value: 'c', modelValue: 'c', label: '允许跨部门查看报表' } },
  ],
  RadioGroup: [
    {
      label: '三项竖排',
      props: { modelValue: 'b' },
      slots: {
        default: () => [
          h(Radio, { value: 'a', label: '选项 A' }),
          h(Radio, { value: 'b', label: '选项 B' }),
          h(Radio, { value: 'c', label: '选项 C' }),
        ],
      },
    },
    {
      label: '整组禁用',
      props: { modelValue: 'a' },
      slots: {
        default: () => [
          h(Radio, { value: 'a', label: '已选', disabled: true }),
          h(Radio, { value: 'b', label: '可选', disabled: true }),
        ],
      },
    },
  ],
  SearchForm: [
    { label: '加载态', props: { loading: true } },
    {
      label: '三字段检索',
      slots: {
        default: () => [
          h(TextInput, { modelValue: '', placeholder: '账号' }),
          h(TextInput, { modelValue: '', placeholder: '手机号' }),
          h(TextInput, { modelValue: '', placeholder: '部门' }),
        ],
      },
    },
  ],
  Segmented: [
    { label: '24 小时', props: { modelValue: '24h' } },
    { label: '带标题', props: { label: '时间范围', modelValue: '30d' } },
    { label: '末项选中', props: { modelValue: '90d' } },
  ],
  Slider: [
    { label: '区间双端', props: { range: true, modelValue: [20, 60] } },
    { label: '显示刻度', props: { showTicks: true, step: 10 } },
    { label: '低值', props: { modelValue: 5 } },
  ],
  Switch: [
    { label: '禁用', props: { disabled: true } },
    { label: '关态', props: { modelValue: false } },
    { label: '关态禁用', props: { modelValue: false, disabled: true } },
  ],
  /* Tree 基础格已把 checkable / multiple / defaultExpandAll / showLine 全打开，
     机械派生同值候选被剔除后只剩一条，这里补收起、过滤与单选三态 */
  Tree: [
    { label: '默认收起', props: { defaultExpandAll: false } },
    { label: '按关键词过滤', props: { filterText: '研发' } },
    { label: '单选不勾选', props: { checkable: false, multiple: false } },
  ],
}
