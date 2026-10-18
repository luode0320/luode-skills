# 珍珠玻璃组件库 · 组件目录索引

> 本文件由 `scripts/build_component_catalog.mjs` 从组件源码自动生成，请勿手改；组件契约变化后重跑生成命令。
> 共 152 个组件。
> 物理目录：基础控件 27 · 业务组件 20 · 工作台版式（本地扩展） 8 · Arco 品类对齐（本地扩展） 83 · 自研图表 6 · 外壳布局 6 · 根级组件 2。
> 语义分类（对齐 Arco 组件菜单）：通用 11 · 布局 8 · 导航 16 · 数据输入 33 · 数据展示 32 · 反馈 12 · 图表 6 · 业务组件 20 · 工作台版式 8 · 外壳与系统 6。

## 速查表

| 组件 | 分类 | 物理目录 | 引入路径 | 必填 props | 说明 |
| --- | --- | --- | --- | --- | --- |
| Avatar | 通用 | 基础控件 | `@/components/ui/Avatar.vue` | — | — |
| Button | 通用 | 基础控件 | `@/components/ui/Button.vue` | — | — |
| Checkbox | 数据输入 | 基础控件 | `@/components/ui/Checkbox.vue` | modelValue | — |
| ConfirmHost | 反馈 | 基础控件 | `@/components/ui/ConfirmHost.vue` | — | — |
| DataTable | 数据展示 | 基础控件 | `@/components/ui/DataTable.vue` | columns, data | 树形表格：按 children 展开，首列带缩进与展开按钮 |
| DeltaPill | 数据展示 | 基础控件 | `@/components/ui/DeltaPill.vue` | value | 环比胶囊：上升青柠、下降红、持平中性；上一周期为 0（fresh）时显示「新增」中性态，不给出误导的百分比 |
| Drawer | 反馈 | 基础控件 | `@/components/ui/Drawer.vue` | open | 共享元素来处：传入选择器（如 'tr'），打开时从最近一次被点的该元素生长成抽屉 |
| EmptyState | 数据展示 | 基础控件 | `@/components/ui/EmptyState.vue` | — | — |
| Field | 数据输入 | 基础控件 | `@/components/ui/Field.vue` | — | 表单字段。默认根节点是 <label>，点标题即可聚焦输入； |
| HoverCard | 数据展示 | 基础控件 | `@/components/ui/HoverCard.vue` | — | 悬停名片：指针停留 300ms 或键盘聚焦时出现的轻玻璃预览卡。 |
| IconButton | 通用 | 基础控件 | `@/components/ui/IconButton.vue` | name, label | — |
| Metric | 数据展示 | 基础控件 | `@/components/ui/Metric.vue` | value | 显示级读数：等宽大数字 + 上标单位。size 对应 --fs-display-xl / l / m 三档 |
| Modal | 反馈 | 基础控件 | `@/components/ui/Modal.vue` | open | 点击遮罩是否关闭（表单弹窗默认不关，避免误触丢失输入） |
| Odometer | 数据展示 | 基础控件 | `@/components/ui/Odometer.vue` | value | 逐位滚动读数（结 Crystallize）：每一位是一条 0–9 的竖带，只有变化的位会滚。 |
| PageHeader | 导航 | 基础控件 | `@/components/ui/PageHeader.vue` | title | 页面头：大标题 + 说明；右侧放规格铭牌（#spec）与主操作（默认插槽）。位置信息由顶栏面包屑承担，不再放英文眉标 |
| Pagination | 导航 | 基础控件 | `@/components/ui/Pagination.vue` | total, page, pageSize | — |
| Panel | 布局 | 基础控件 | `@/components/ui/Panel.vue` | — | — |
| Ruler | 数据展示 | 基础控件 | `@/components/ui/Ruler.vue` | — | 刻度尺：细刻度 + 主刻度标签，marker 为 0–1 的当前位置（一根亮刻度） |
| SectionLabel | 数据展示 | 基础控件 | `@/components/ui/SectionLabel.vue` | — | 区块标题：横带分层与仪器化面板的中文小标题（不再使用英文眉标与编号） |
| Segmented | 导航 | 基础控件 | `@/components/ui/Segmented.vue` | modelValue, options | 容器或任一选项尺寸变化都重新对位：拉伸布局里网页字体加载完成只改选项宽度，不改容器宽度 |
| Select | 数据输入 | 基础控件 | `@/components/ui/Select.vue` | modelValue, options | 树形选项的缩进层级 |
| SpecPlate | 数据展示 | 基础控件 | `@/components/ui/SpecPlate.vue` | rows | 规格铭牌：深色玻璃小板，等宽键值行。只读读数，不带可点的样子 |
| StatusTag | 通用 | 基础控件 | `@/components/ui/StatusTag.vue` | status | — |
| Switch | 数据输入 | 基础控件 | `@/components/ui/Switch.vue` | modelValue | — |
| Tag | 通用 | 基础控件 | `@/components/ui/Tag.vue` | — | 语义色只有四种；字典里的历史色值就近归档 |
| TextInput | 数据输入 | 基础控件 | `@/components/ui/TextInput.vue` | — | — |
| ToastHost | 反馈 | 基础控件 | `@/components/ui/ToastHost.vue` | — | 提示牌堆：最新一条在最前，较早的缩小叠在后面；悬停展开成列表并暂停计时。 |
| AskDock | 业务组件 | 业务组件 | `@/components/business/AskDock.vue` | — | 问答坞：输入问题或点预设，问题逐字打出（蓄 Charge）→ 答案卡级联浮现（结 Crystallize）。 |
| BoardView | 业务组件 | 业务组件 | `@/components/business/BoardView.vue` | columns, itemKey | 看板分列：按状态 / 部门 / 角色等分列展示卡片，列头着分类色。 |
| DeptSelect | 业务组件 | 业务组件 | `@/components/business/DeptSelect.vue` | modelValue | 部门下拉：按组织层级缩进，可搜索。exclude 用于编辑部门时排除自身及下级。 |
| DeptTree | 业务组件 | 业务组件 | `@/components/business/DeptTree.vue` | modelValue | 部门树：左栏筛选用。选中节点即 emit 部门 ID，再点一次取消。 |
| DictSelect | 业务组件 | 业务组件 | `@/components/business/DictSelect.vue` | type, modelValue | 字典下拉：选项来自「字典管理」中的字典数据，值统一为字符串。 |
| DictSwatchbook | 业务组件 | 业务组件 | `@/components/business/DictSwatchbook.vue` | types | 字典样本册：每个字典类型一张卡，直接渲染真实标签样式与色调分布条。 |
| DictTag | 业务组件 | 业务组件 | `@/components/business/DictTag.vue` | type, value | 字典值展示：按字典数据的标签文本与样式渲染，找不到时原样显示。 |
| FormDialog | 业务组件 | 业务组件 | `@/components/business/FormDialog.vue` | open, title | 表单弹窗：两列网格 + 取消 / 保存。页面只写字段与校验。 |
| GeneratorPipeline | 业务组件 | 业务组件 | `@/components/business/GeneratorPipeline.vue` | table | 代码生成流水线：① 表信息 → ② 字段映射 → ③ 代码预览，一个弹窗走完。 |
| InsightPanel | 业务组件 | 业务组件 | `@/components/business/InsightPanel.vue` | contentKey, kind, title | 分析栏：关系图 / 画布的右侧详情。头部分类 → 标题与状态 → 主读数 + 迷你柱 → |
| ListPage | 业务组件 | 业务组件 | `@/components/business/ListPage.vue` | title, list, columns | 统一列表页：页面头 → 查询区 → 表格面板（刷新 / 导出 / 批量条）→ 分页。 |
| MenuStarMap | 业务组件 | 业务组件 | `@/components/business/MenuStarMap.vue` | tree | 导航星系（图谱舞台，三层下钻）： |
| OrgCanvas | 业务组件 | 业务组件 | `@/components/business/OrgCanvas.vue` | tree, selectedId | 组织架构画布：整齐树布局铺满内容区，四角留给页面放浮动玻璃面板（#tl / #tr / #bl / #br）。 |
| PermissionButton | 业务组件 | 业务组件 | `@/components/business/PermissionButton.vue` | — | 权限按钮：没有权限码时不渲染（而不是禁用），与后端 @RequiresPermission 使用同一套编码。 |
| PermissionMatrix | 业务组件 | 业务组件 | `@/components/business/PermissionMatrix.vue` | menus, roles, grants, editable | 权限矩阵：行 = 菜单树（目录可折叠），列 = 角色。 |
| PermissionTrace | 业务组件 | 业务组件 | `@/components/business/PermissionTrace.vue` | — | 权限溯源（图谱舞台，三层下钻）： |
| PermissionTree | 业务组件 | 业务组件 | `@/components/business/PermissionTree.vue` | menus, modelValue | 菜单权限树：目录 / 菜单为树节点（勾选含全部下级），按钮权限渲染为节点下方的标签。 |
| PostLadder | 业务组件 | 业务组件 | `@/components/business/PostLadder.vue` | posts | 岗位阶梯（图谱舞台）：岗位按 sort 沿对角线自左下向右上等距铺满舞台， |
| SearchForm | 业务组件 | 业务组件 | `@/components/business/SearchForm.vue` | — | 查询区：字段放默认插槽，回车即查询。查询 / 重置按钮统一在右侧。 |
| UserSelect | 业务组件 | 业务组件 | `@/components/business/UserSelect.vue` | modelValue | 用户下拉：可搜索。valueKey 决定绑定的是用户 ID 还是昵称（部门负责人按昵称存储）。 |
| ActivityList | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/ActivityList.vue` | items | 动态列表：头像 + 主文 + 时间 + 右侧标记，用于「最近登录」这类流水。 |
| Band | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/Band.vue` | — | 横带分层容器：监控页与详情页的整块分区（Stacked Bands）。 |
| BentoCard | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/BentoCard.vue` | — | 工作台卡片：主次布局的基本单元。span 决定栅格占位（复用 pages.css 的 bento-* 变体）， |
| BentoGrid | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/BentoGrid.vue` | — | 工作台网格：12 列自适应栅格容器，卡片按 BentoCard 的 span 语义落位。 |
| KeyValueReadout | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/KeyValueReadout.vue` | rows | 键值读数组：主卡与刻度环旁的「峰值 / 均值 / 范围」小表。 |
| ReadoutStrip | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/ReadoutStrip.vue` | items | 读数条：一排并列的 Metric，带分隔线；用于概览统计。 |
| ShareList | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/ShareList.vue` | items | 占比条列表：横向条形 + 数值，用于「数据权限分布」这类按数量排序的构成展示。 |
| ShortcutGrid | 工作台版式 | 工作台版式（本地扩展） | `@/components/workspace/ShortcutGrid.vue` | items | 快捷入口宫格：图标 + 标题 + 分组副标题，点击上抛 key 与路径。 |
| Affix | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Affix.vue` | — | 固钉：让内容在滚动容器内吸附在顶部或底部，滚出后仍保持可见。 |
| Alert | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Alert.vue` | — | 提示条：页内静态提示，四型语义色 + 可关闭。 |
| Anchor | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Anchor.vue` | items | 锚点导航：列出页内小节，点击平滑滚动，滚动时按可见性高亮当前小节。 |
| AutoComplete | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/AutoComplete.vue` | options | 自动补全：输入框敲字时在下方浮出匹配候选，上下键切换、回车落定。 |
| AvatarGroup | 通用 | Arco 品类对齐（本地扩展） | `@/components/extend/AvatarGroup.vue` | — | 头像组：多个头像叠压成一摞，超出 max 的部分收成末尾的 +N。 |
| BackTop | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/BackTop.vue` | — | 回到顶部：滚动超过阈值后浮出圆形按钮，点击平滑回顶。 |
| Badge | 通用 | Arco 品类对齐（本地扩展） | `@/components/extend/Badge.vue` | — | 徽标：挂在任意元素右上角的数字 / 圆点角标，数字超过 max 显示为 max+。 |
| Breadcrumb | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Breadcrumb.vue` | items | 面包屑：展示层级路径，末项是当前页，前面的项只有给了 to 才可点。 |
| ButtonGroup | 通用 | Arco 品类对齐（本地扩展） | `@/components/extend/ButtonGroup.vue` | — | 按钮组：把若干个按钮拼成一条，相邻处只留一道描边、首尾各留一次圆角。 |
| Calendar | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Calendar.vue` | — | 日历：月 / 年两种粒度，月网格含上下月补白，今天与选中高亮。 |
| Card | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Card.vue` | — | 通用卡片：header / body / footer 三区，外加可选的顶部封面。 |
| CardGrid | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/CardGrid.vue` | — | 卡片网格：把若干张卡按固定列数排布，列宽等分、间距统一。 |
| CardMeta | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/CardMeta.vue` | — | 卡片元信息区：头像 + 标题 + 描述的一行横排，供 Card 主体或列表项复用。 |
| Carousel | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Carousel.vue` | — | 走马灯：CSS transform 位移切换，支持自动播放、循环、指示点与箭头。 |
| Cascader | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Cascader.vue` | options | 级联选择：按层级逐列展开，每点一层同步回写路径，选到叶子即落定。 |
| CascaderPanel | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/CascaderPanel.vue` | options | 级联选择面板：Cascader 里被下拉触发器包住的那部分，抽出来后可独立嵌进页面 |
| CheckboxGroup | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/CheckboxGroup.vue` | options | 复选组的对外契约：子项靠 checkboxGroupKey 注入上下文，与组件的 setup 逻辑无关， |
| Collapse | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Collapse.vue` | — | 折叠面板：以 modelValue 数组承载展开项，accordion 下互斥展开。 |
| CollapseItem | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/CollapseItem.vue` | name | 折叠子项：标题行 + 内容区，展开态、图标位置全部从父级 Collapse inject 读取。 |
| ColorPicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/ColorPicker.vue` | — | 取色器：色块按钮点开面板，预设色板、原生取色盘与十六进制输入三路同源。 |
| Comment | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Comment.vue` | — | 评论：头像 + 作者 + 时间 + 正文，底部动作条可点或走 actions 插槽。 |
| Countdown | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Countdown.vue` | — | 倒计时：按目标时间戳或剩余秒数逐秒倒数，按格式串渲染，走到零时派发 finish。 |
| DataList | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/DataList.vue` | data | 数据列表：一份 data 数组 + item 插槽渲染每行，支持分割线、加载骨架与空态。 |
| DatePicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/DatePicker.vue` | — | 日期选择：用原生 Date 自绘月历网格，支持上下月切换、选日、今天与选中高亮。 |
| Descriptions | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Descriptions.vue` | data | 定义列表（Descriptions）：详情页/订单页常见的「一组字段标签—值」只读卡片， |
| Divider | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/Divider.vue` | — | 分割线：横向分隔段落、纵向分隔并排区块，可带文字居中或靠左靠右。 |
| Dropdown | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Dropdown.vue` | items | 下拉菜单：点或悬停触发区后浮出选项列表，选中即派发 key 并关闭。 |
| DropdownButton | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/DropdownButton.vue` | items | 下拉按钮：按钮主体点一下走默认动作，右侧小箭头单独点开菜单，两件事互不干扰。 |
| DropdownSubmenu | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/DropdownSubmenu.vue` | label, items | 下拉子菜单：把一组二级选项收在一个菜单项后面，指针悬停时在右侧浮出面板。 |
| Form | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Form.vue` | model | 表单容器：把「数据模型 + 校验规则 + 错误态 + 提交」这一套编排收到一处。 |
| GridCol | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/GridCol.vue` | — | 栅格列：24 栅格制，span 决定占比，offset 前置留白，push / pull 做顺序视觉交换。 |
| GridRow | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/GridRow.vue` | — | 栅格行：24 栅格制的 flex 轨道容器，横纵两个方向各有一份间距。 |
| HelpTip | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/HelpTip.vue` | content | 图标式帮助：一个小图标按钮，悬停或键盘聚焦时浮出功能 / 字段 / 业务说明。 |
| Image | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Image.vue` | src | 图片：加载中显示骨架，失败回落 fallback 或占位图标；preview 时点击开全屏遮罩。 |
| ImagePreview | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/ImagePreview.vue` | src | 图片预览器：全屏遮罩里看单张大图，支持滚轮与按钮缩放、旋转、Esc / 点遮罩关闭。 |
| ImagePreviewGroup | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/ImagePreviewGroup.vue` | images | 图片预览组：一组图共用一个全屏预览器，底部缩略图导航，左右箭头或方向键切上下张。 |
| InputGroup | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/InputGroup.vue` | — | 输入组：把多个输入框 / 按钮横向或纵向拼成一条，整组读作「一个控件」而不是几个并排控件。 |
| InputNumber | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/InputNumber.vue` | — | 数字输入：左右步进按钮夹住中间输入框，越界钳制、按 precision 定小数位。 |
| InputPassword | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/InputPassword.vue` | — | 密码输入框：在输入框内自带一个「明文/密文」切换钮，点击即在 password 与 text 间切换。 |
| InputSearch | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/InputSearch.vue` | — | 搜索输入：把「填词 + 触发搜索」收成一个控件，回车与点右侧按钮完全等价。 |
| InputTag | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/InputTag.vue` | — | 标签输入：回车把当前文本收成标签，退格在空输入时删末尾，标签上的叉逐个移除。 |
| LinkText | 通用 | Arco 品类对齐（本地扩展） | `@/components/extend/LinkText.vue` | — | 链接文字：语义色 + 可选下划线，禁用态降级为纯文本，无 href 时退化为 span。 |
| Mention | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Mention.vue` | options | 提及输入：textarea 里敲出 trigger（默认 @）即浮出候选，选中后把触发词替换成候选值。 |
| Menu | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Menu.vue` | items | 菜单：纵向或横向的导航列表，支持子菜单递归展开与折叠态。 |
| MenuNode | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/MenuNode.vue` | item, depth, vertical | 菜单节点：菜单的递归单元，自身承载子项列表。 |
| MonthPicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/MonthPicker.vue` | — | 月份选择：一格一月共 12 格，头部只翻年不翻月，选完立即回写。 |
| Notification | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Notification.vue` | — | 通知卡片：单条展示型，只负责一条通知的排版与关闭。 |
| OverflowList | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/OverflowList.vue` | items | 溢出列表：按容器宽度逐项排布，放不下的项收进 +N 下拉，点开可看全部。 |
| Popconfirm | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Popconfirm.vue` | — | 气泡确认：点触发区浮出一个小气泡，确认或取消后收起。 |
| Popover | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Popover.vue` | — | 气泡卡片：比 Tooltip 更重的一块浮层，可放标题、正文与可点内容。 |
| Progress | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Progress.vue` | percent | 进度条：line 用宽度过渡、circle 用 SVG 描边偏移，两条实现共用一套状态色。 |
| QuarterPicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/QuarterPicker.vue` | — | 季度选择：一格一季共 4 格，头部只翻年。 |
| Radio | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Radio.vue` | value | 单选框：优先读最近 RadioGroup 的上下文，独立使用时退回自身 props。 |
| RadioGroup | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/RadioGroup.vue` | modelValue | 单选组的对外契约：Radio 依赖 radioGroupKey 注入上下文，独立于组件的 setup 逻辑， |
| RangePicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/RangePicker.vue` | — | 日期区间选择：单个月历网格里两步连选，先点开始再点结束。 |
| Rate | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Rate.vue` | — | 评分：五角星按整数或半星打分，hover 预览、点击定值、再点同一值得可清空。 |
| ResizeBox | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/ResizeBox.vue` | — | 伸缩框：拖动右下角把手把内容压成指定宽高，宽高直接落到容器尺寸上。 |
| Result | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Result.vue` | — | 结果页：一次操作或一个错误码的终态陈述。 |
| Skeleton | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Skeleton.vue` | — | 骨架屏：loading 为 true 时按 type / rows 渲染占位块，否则渲染 default 插槽。 |
| Slider | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Slider.vue` | — | 滑块：原生 <input type="range"> 作无障碍底座，视觉轨道与滑块叠在其上。 |
| Space | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/Space.vue` | — | 间距：给一组子项之间垫出统一距离，方向与对齐由一行 flex 决定。 |
| Spin | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Spin.vue` | — | 加载中：只渲染一个转圈，或用 wrapper 在内容上叠一层遮罩。 |
| SplitPane | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/SplitPane.vue` | — | 分栏：一块区域按可拖动的分隔条切成两半，横向出左右、纵向出上下。 |
| Steps | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Steps.vue` | current, items | 步骤条：横向或纵向的工序进度，已完成打勾、当前高亮、未开始置灰。 |
| StyledScrollbar | 布局 | Arco 品类对齐（本地扩展） | `@/components/extend/StyledScrollbar.vue` | — | 自定义滚动条：滚动容器保持原生 overflow / 键盘 / 触控板行为，只额外画一条浮动滑块压在上面。 |
| TabPane | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/TabPane.vue` | — | 标签面板：Tabs 内容区的单页容器，active 为真才显示，切换只切可见性不销毁内容。 |
| Tabs | 导航 | Arco 品类对齐（本地扩展） | `@/components/extend/Tabs.vue` | modelValue, items | 标签页：横向切换一组视图，line 型用滑动下划线、card 型用底色切换。 |
| Textarea | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Textarea.vue` | — | 多行文本域：在 TextInput 的 multiline 之外补两项真实能力——自动高度与字数统计。 |
| TimePicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/TimePicker.vue` | — | 时间选择：触发区 + 下拉面板，面板里时 / 分两列滚动选择，底部提供「此刻」快捷。 |
| Timeline | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Timeline.vue` | items | 时间轴：由 items 数据派生节点，左侧 / 右侧 / 交替三种排布，可反向。 |
| TimelineItem | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/TimelineItem.vue` | — | 时间轴节点：圆点 + 竖线 + 时间 / 标题 / 内容，可单独使用也可被 Timeline 批量渲染。 |
| Tooltip | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Tooltip.vue` | — | 提示气泡：hover / focus 时在目标旁浮出说明，位置自动避让视口边缘。 |
| Transfer | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Transfer.vue` | data | 穿梭框：左「待选」右「已选」两栏，中间箭头把勾选项推过去。 |
| Tree | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Tree.vue` | data | 通用递归树：只认 key/label/children 这套通用结构，不绑定任何业务数据模型， |
| TreeNode | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/TreeNode.vue` | node, depth, parentKey | 树的递归单元：一行 = 展开箭头 + 可选复选框 + 图标 + 标签，下方按需渲染子级。 |
| TreeSelect | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/TreeSelect.vue` | data | 树选择：触发区点开一个下拉树面板，支持层级缩进、展开折叠、单选与多选。 |
| Trigger | 反馈 | Arco 品类对齐（本地扩展） | `@/components/extend/Trigger.vue` | — | 触发器：通用「定位 + 显隐」底层原语，Dropdown / Popover 这类浮层都由它派生。 |
| Typography | 通用 | Arco 品类对齐（本地扩展） | `@/components/extend/Typography.vue` | — | 排版：按 type / heading 决定语义标签，叠加加粗、高亮、下划线、删除线、行内代码、省略、复制等修饰。 |
| Upload | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/Upload.vue` | — | 上传：只做前端文件选择与列表管理，不做真实网络上传。 |
| VerificationCode | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/VerificationCode.vue` | — | 验证码输入：定长数字格，逐格输入自动跳格，退格回跳，支持整串粘贴。 |
| Watermark | 数据展示 | Arco 品类对齐（本地扩展） | `@/components/extend/Watermark.vue` | — | 水印：用 canvas 把文字 / 图片绘成 dataURL，作为背景图平铺在内容之上。 |
| WeekPicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/WeekPicker.vue` | — | 周选择：列出 ISO 周（周一开头，第 1 周含当年首个周四），每行显示周序号与起止日期。 |
| YearPicker | 数据输入 | Arco 品类对齐（本地扩展） | `@/components/extend/YearPicker.vue` | — | 年份选择：一页 12 年（十年跨度加前后各一年的缓冲），头部显示跨度并整页翻。 |
| BarChart | 图表 | 自研图表 | `@/components/charts/BarChart.vue` | values, labels | 柱状图：柱子从基线生长（结 Crystallize），highlight 柱用斜线填充表示「当前」。 |
| HeatGrid | 图表 | 自研图表 | `@/components/charts/HeatGrid.vue` | cells | 星期 × 小时热力格：格子按分位分 5 级（青柠由浅到深），失败占比高的格子叠斜线（--hatch）。 |
| RelationGraph | 图表 | 自研图表 | `@/components/charts/RelationGraph.vue` | nodes, links | 关系图：节点与连线由页面按当前层级算好目标坐标，本组件负责「活起来」—— |
| Swimlane | 图表 | 自研图表 | `@/components/charts/Swimlane.vue` | lanes | 时间轴泳道：泳道 × 时间轴。默认聚焦到 [首条 −1h, 现在 +1h]（至少 6 小时），可切回全天。 |
| TickRing | 图表 | 自研图表 | `@/components/charts/TickRing.vue` | value | 刻度环：60 根径向刻度按顺时针逐根点亮（导 Conduct）， |
| TrendChart | 图表 | 自研图表 | `@/components/charts/TrendChart.vue` | values, labels | 纯 SVG 趋势图：按容器真实宽度计算路径，线宽不被拉伸。 |
| AppShell | 外壳与系统 | 外壳布局 | `@/components/layout/AppShell.vue` | — | — |
| AppearanceDialog | 外壳与系统 | 外壳布局 | `@/components/layout/AppearanceDialog.vue` | open | — |
| CommandPalette | 导航 | 外壳布局 | `@/components/layout/CommandPalette.vue` | open | 命令面板：最近访问 / 页面 / 用户 / 快捷动作 四组结果， |
| PasswordDialog | 外壳与系统 | 外壳布局 | `@/components/layout/PasswordDialog.vue` | open | — |
| Sidebar | 外壳与系统 | 外壳布局 | `@/components/layout/Sidebar.vue` | — | — |
| Topbar | 外壳与系统 | 外壳布局 | `@/components/layout/Topbar.vue` | — | — |
| Icon | 通用 | 根级组件 | `@/components/Icon.vue` | name | — |
| NeuralNet | 外壳与系统 | 根级组件 | `@/components/NeuralNet.vue` | — | 神经网络画布：能力模块节点缓慢呼吸，脉冲沿连线往返（导 Conduct）。 |

## 组件契约

### 基础控件（27）

#### Avatar

```vue
<Avatar />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| name | `string` | 否 | '' |
| size | `number` | 否 | 32 |

**参考实现**：`src/components/extend/CardMeta.vue`、`src/components/extend/Comment.vue`、`src/components/layout/CommandPalette.vue`、`src/components/layout/Topbar.vue`、`src/components/workspace/ActivityList.vue`、`src/views/Dashboard.vue`、`src/views/gallery/demo-slots.ts`、`src/views/gallery/demo-variants.curated-general.ts`


#### Button

```vue
<Button variant="primary" size="md" type="button">内容</Button>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| variant | `'primary' \| 'secondary' \| 'ghost' \| 'text' \| 'danger'` | 否 | 'secondary' |
| size | `'md' \| 'sm'` | 否 | 'md' |
| icon | `string` | 否 | — |
| loading | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| danger | `boolean` | 否 | — |
| block | `boolean` | 否 | — |
| type | `'button' \| 'submit'` | 否 | 'button' |

**插槽**：`default`

**参考实现**：`src/components/business/FormDialog.vue`、`src/components/business/GeneratorPipeline.vue`、`src/components/business/ListPage.vue`、`src/components/business/PermissionButton.vue`、`src/components/business/PermissionMatrix.vue`、`src/components/business/SearchForm.vue`、`src/components/extend/DropdownButton.vue`、`src/components/extend/Popconfirm.vue`


#### Checkbox

```vue
<Checkbox modelValue>内容</Checkbox>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `boolean` | 是 | — |
| indeterminate | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| label | `string` | 否 | — |

**事件**：`update:modelValue`(boolean)

**插槽**：`default`

**参考实现**：`src/components/business/PermissionTree.vue`、`src/components/extend/CheckboxGroup.vue`、`src/components/extend/Transfer.vue`、`src/components/extend/TreeNode.vue`、`src/components/ui/DataTable.vue`、`src/views/Login.vue`


#### ConfirmHost

```vue
<ConfirmHost />
```

**参考实现**：`src/App.vue`


#### DataTable

树形表格：按 children 展开，首列带缩进与展开按钮

```vue
<DataTable :columns="[]" :data="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| columns | `Column[]` | 是 | — |
| data | `Row[]` | 是 | — |
| rowKey | `string` | 否 | 'id' |
| selectable | `boolean` | 否 | — |
| selected | `(string \| number)[]` | 否 | () => [] |
| loading | `boolean` | 否 | — |
| emptyText | `string` | 否 | '暂无数据' |
| tree | `boolean` | 否 | — |
| expandDepth | `number` | 否 | 1 |
| minWidth | `number` | 否 | — |

**事件**：`update:selected`((string \| number)[])、`row-click`(Row)

**插槽**：``cell-${col.key}``、`(动态透传)`

**导出类型**：`Column`


#### DeltaPill

环比胶囊：上升青柠、下降红、持平中性；上一周期为 0（fresh）时显示「新增」中性态，不给出误导的百分比

```vue
<DeltaPill :value="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| value | `number \| null \| undefined` | 是 | — |
| up | `boolean \| null` | 否 | null |
| fresh | `boolean` | 否 | false |
| suffix | `string` | 否 | '%' |
| label | `string` | 否 | — |

**参考实现**：`src/views/Dashboard.vue`、`src/views/gallery/demo-slots.ts`


#### Drawer

共享元素来处：传入选择器（如 'tr'），打开时从最近一次被点的该元素生长成抽屉

```vue
<Drawer open>内容</Drawer>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |
| title | `string` | 否 | — |
| sub | `string` | 否 | — |
| width | `number` | 否 | 520 |
| originFrom | `string` | 否 | — |

**事件**：`close`(—)

**插槽**：`default`、`footer`、`(动态透传)`


#### EmptyState

```vue
<EmptyState>内容</EmptyState>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | '暂无数据' |
| desc | `string` | 否 | — |
| icon | `string` | 否 | 'search' |

**插槽**：`default`

**参考实现**：`src/components/business/PostLadder.vue`、`src/components/extend/DataList.vue`、`src/components/extend/Transfer.vue`、`src/components/ui/DataTable.vue`、`src/views/Dashboard.vue`、`src/views/gallery/Gallery.vue`、`src/views/NoAccess.vue`、`src/views/NotFound.vue`


#### Field

表单字段。默认根节点是 <label>，点标题即可聚焦输入；

```vue
<Field>内容</Field>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| label | `string` | 否 | — |
| required | `boolean` | 否 | — |
| error | `string` | 否 | — |
| hint | `string` | 否 | — |
| wide | `boolean` | 否 | — |
| span | `boolean` | 否 | — |
| group | `boolean` | 否 | — |

**插槽**：`default`

**参考实现**：`src/components/business/GeneratorPipeline.vue`、`src/components/layout/PasswordDialog.vue`、`src/views/Login.vue`、`src/views/gallery/demo-slots.ts`


#### HoverCard

悬停名片：指针停留 300ms 或键盘聚焦时出现的轻玻璃预览卡。

```vue
<HoverCard placement="bottom">内容</HoverCard>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| delay | `number` | 否 | 300 |
| placement | `'bottom' \| 'top'` | 否 | 'bottom' |
| width | `number` | 否 | 260 |

**插槽**：`default`、`card`


#### IconButton

```vue
<IconButton name="文本" label="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| name | `string` | 是 | — |
| label | `string` | 是 | — |
| size | `number` | 否 | 17 |
| bordered | `boolean` | 否 | — |
| danger | `boolean` | 否 | — |
| small | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |

**参考实现**：`src/components/business/AskDock.vue`、`src/components/business/DictSwatchbook.vue`、`src/components/business/InsightPanel.vue`、`src/components/business/ListPage.vue`、`src/components/business/MenuStarMap.vue`、`src/components/business/OrgCanvas.vue`、`src/components/business/PermissionButton.vue`、`src/components/business/PermissionTrace.vue`


#### Metric

显示级读数：等宽大数字 + 上标单位。size 对应 --fs-display-xl / l / m 三档

```vue
<Metric :value="0" size="xl">内容</Metric>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| value | `number \| null \| undefined` | 是 | — |
| unit | `string` | 否 | — |
| decimals | `number` | 否 | 0 |
| size | `'xl' \| 'l' \| 'm' \| 's'` | 否 | 'm' |
| label | `string` | 否 | — |

**插槽**：`default`

**参考实现**：`src/components/business/InsightPanel.vue`、`src/components/workspace/ReadoutStrip.vue`、`src/views/Dashboard.vue`


#### Modal

点击遮罩是否关闭（表单弹窗默认不关，避免误触丢失输入）

```vue
<Modal open>内容</Modal>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |
| title | `string` | 否 | — |
| sub | `string` | 否 | — |
| width | `number` | 否 | 560 |
| closeOnOverlay | `boolean` | 否 | — |

**事件**：`close`(—)

**插槽**：`default`、`footer`、`(动态透传)`

**参考实现**：`src/components/business/FormDialog.vue`、`src/components/business/GeneratorPipeline.vue`、`src/components/layout/AppearanceDialog.vue`、`src/components/ui/ConfirmHost.vue`


#### Odometer

逐位滚动读数（结 Crystallize）：每一位是一条 0–9 的竖带，只有变化的位会滚。

```vue
<Odometer :value="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| value | `number \| null \| undefined` | 是 | — |
| decimals | `number` | 否 | 0 |
| group | `boolean` | 否 | true |

**参考实现**：`src/components/charts/TickRing.vue`、`src/components/ui/Metric.vue`


#### PageHeader

页面头：大标题 + 说明；右侧放规格铭牌（#spec）与主操作（默认插槽）。位置信息由顶栏面包屑承担，不再放英文眉标

```vue
<PageHeader title="文本">内容</PageHeader>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 是 | — |
| desc | `string` | 否 | — |

**插槽**：`spec`、`default`、`(动态透传)`

**参考实现**：`src/components/business/ListPage.vue`、`src/views/gallery/Gallery.vue`


#### Pagination

```vue
<Pagination :total="0" :page="0" :pageSize="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| total | `number` | 是 | — |
| page | `number` | 是 | — |
| pageSize | `number` | 是 | — |
| sizes | `number[]` | 否 | () => [10, 20, 50, 100] |

**事件**：`update:page`(number)、`update:pageSize`(number)

**参考实现**：`src/components/business/ListPage.vue`


#### Panel

```vue
<Panel>内容</Panel>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| meta | `string` | 否 | — |

**插槽**：`head`、`tools`、`default`、`(动态透传)`

**参考实现**：`src/components/business/ListPage.vue`


#### Ruler

刻度尺：细刻度 + 主刻度标签，marker 为 0–1 的当前位置（一根亮刻度）

```vue
<Ruler />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| labels | `string[]` | 否 | () => [] |
| marker | `number \| null` | 否 | null |
| markerLabel | `string` | 否 | — |
| minor | `number` | 否 | 4 |

**参考实现**：`src/components/charts/Swimlane.vue`


#### SectionLabel

区块标题：横带分层与仪器化面板的中文小标题（不再使用英文眉标与编号）

```vue
<SectionLabel as="h2" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| as | `'h2' \| 'h3'` | 否 | — |

**参考实现**：`src/components/workspace/Band.vue`、`src/components/workspace/BentoCard.vue`、`src/views/Dashboard.vue`


#### Segmented

容器或任一选项尺寸变化都重新对位：拉伸布局里网页字体加载完成只改选项宽度，不改容器宽度

```vue
<Segmented modelValue="文本" :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `T` | 是 | — |
| options | `Array<{ label: string; value: T }>` | 是 | — |
| label | `string` | 否 | — |

**事件**：`update:modelValue`(T)

**参考实现**：`src/components/layout/AppearanceDialog.vue`、`src/views/Dashboard.vue`


#### Select

树形选项的缩进层级

```vue
<Select modelValue="文本" :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string \| number \| null \| undefined` | 是 | — |
| options | `Array<SelectOption \| string \| number>` | 是 | — |
| placeholder | `string` | 否 | '请选择' |
| filterable | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| invalid | `boolean` | 否 | — |
| emptyText | `string` | 否 | '无匹配项' |

**事件**：`update:modelValue`(Value)

**导出类型**：`SelectOption`

**参考实现**：`src/components/business/DeptSelect.vue`、`src/components/business/DictSelect.vue`、`src/components/business/UserSelect.vue`、`src/components/ui/Pagination.vue`


#### SpecPlate

规格铭牌：深色玻璃小板，等宽键值行。只读读数，不带可点的样子

```vue
<SpecPlate :rows="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| rows | `Array<{ label: string; value: string \| number \| null \| undefined; tone?: 'lime' \| 'red' }>` | 是 | — |
| title | `string` | 否 | — |


#### StatusTag

```vue
<StatusTag :status="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| status | `number \| boolean` | 是 | — |
| on | `string` | 否 | '正常' |
| off | `string` | 否 | '停用' |

**参考实现**：`src/components/business/DictSwatchbook.vue`、`src/components/business/PostLadder.vue`


#### Switch

```vue
<Switch modelValue>内容</Switch>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `boolean` | 是 | — |
| disabled | `boolean` | 否 | — |
| label | `string` | 否 | — |

**事件**：`update:modelValue`(boolean)

**插槽**：`default`

**参考实现**：`src/components/business/DictSwatchbook.vue`、`src/components/business/GeneratorPipeline.vue`


#### Tag

语义色只有四种；字典里的历史色值就近归档

```vue
<Tag>内容</Tag>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| tone | `string` | 否 | — |
| dot | `boolean` | 否 | — |

**插槽**：`default`

**参考实现**：`src/components/business/DictSwatchbook.vue`、`src/components/business/DictTag.vue`、`src/components/ui/StatusTag.vue`、`src/components/workspace/ActivityList.vue`、`src/views/Dashboard.vue`


#### TextInput

```vue
<TextInput type="text" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string \| number \| null` | 否 | — |
| placeholder | `string` | 否 | — |
| type | `'text' \| 'password' \| 'number' \| 'email' \| 'tel'` | 否 | 'text' |
| icon | `string` | 否 | — |
| invalid | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| readonly | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| multiline | `boolean` | 否 | — |
| rows | `number` | 否 | 3 |
| maxlength | `number` | 否 | — |
| autocomplete | `string` | 否 | — |

**事件**：`update:modelValue`(string \| number \| null)、`enter`(—)

**参考实现**：`src/components/business/DeptTree.vue`、`src/components/business/GeneratorPipeline.vue`、`src/components/layout/PasswordDialog.vue`、`src/views/Login.vue`、`src/views/gallery/demo-slots.ts`、`src/views/gallery/demo-variants.curated-inputs.ts`


#### ToastHost

提示牌堆：最新一条在最前，较早的缩小叠在后面；悬停展开成列表并暂停计时。

```vue
<ToastHost />
```

**参考实现**：`src/App.vue`


### 业务组件（20）

#### AskDock

问答坞：输入问题或点预设，问题逐字打出（蓄 Charge）→ 答案卡级联浮现（结 Crystallize）。

```vue
<AskDock />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| group | `string` | 否 | — |
| placeholder | `string` | 否 | '问问系统…例如「谁能删除用户」' |
| compact | `boolean` | 否 | — |

**事件**：`chip`(AnswerChip)

**参考实现**：`src/components/business/PermissionTrace.vue`


#### BoardView

看板分列：按状态 / 部门 / 角色等分列展示卡片，列头着分类色。

```vue
<BoardView :columns="[]" itemKey="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| columns | `BoardColumn<T>[]` | 是 | — |
| itemKey | `string` | 是 | — |
| draggable | `boolean` | 否 | false |
| onMove | `(payload: { item: T; from: BoardColumn<T>; to: BoardColumn<T> }) => Promise<boolean>` | 否 | — |
| emptyText | `string` | 否 | '暂无' |

**插槽**：`card`

**导出类型**：`BoardColumn`


#### DeptSelect

部门下拉：按组织层级缩进，可搜索。exclude 用于编辑部门时排除自身及下级。

```vue
<DeptSelect :modelValue="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `number \| null \| undefined` | 是 | — |
| data | `Dept[]` | 否 | — |
| placeholder | `string` | 否 | '请选择部门' |
| rootLabel | `string` | 否 | — |
| excludeIds | `number[]` | 否 | — |
| invalid | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(number \| null)


#### DeptTree

部门树：左栏筛选用。选中节点即 emit 部门 ID，再点一次取消。

```vue
<DeptTree :modelValue="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `number \| null` | 是 | — |
| data | `Dept[]` | 否 | — |

**事件**：`update:modelValue`(number \| null)


#### DictSelect

字典下拉：选项来自「字典管理」中的字典数据，值统一为字符串。

```vue
<DictSelect type="文本" modelValue="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| type | `string` | 是 | — |
| modelValue | `string \| number \| null \| undefined` | 是 | — |
| placeholder | `string` | 否 | '请选择' |
| allLabel | `string` | 否 | — |
| invalid | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


#### DictSwatchbook

字典样本册：每个字典类型一张卡，直接渲染真实标签样式与色调分布条。

```vue
<DictSwatchbook :types="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| types | `DictTypeRow[]` | 是 | — |
| loading | `boolean` | 否 | — |

**事件**：`create-item`(DictTypeRow)、`edit-item`(DictTypeRow)、`edit-type`(DictTypeRow)

**导出类型**：`DictTypeRow`、`DictItem`

**参考实现**：`src/views/system/Dict.vue`


#### DictTag

字典值展示：按字典数据的标签文本与样式渲染，找不到时原样显示。

```vue
<DictTag type="文本" value="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| type | `string` | 是 | — |
| value | `string \| number \| null \| undefined` | 是 | — |


#### FormDialog

表单弹窗：两列网格 + 取消 / 保存。页面只写字段与校验。

```vue
<FormDialog open title="文本">内容</FormDialog>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |
| title | `string` | 是 | — |
| sub | `string` | 否 | — |
| width | `number` | 否 | 620 |
| saving | `boolean` | 否 | — |
| submitText | `string` | 否 | '保存' |

**事件**：`close`(—)、`submit`(—)

**插槽**：`default`、`extra`

**参考实现**：`src/components/layout/PasswordDialog.vue`


#### GeneratorPipeline

代码生成流水线：① 表信息 → ② 字段映射 → ③ 代码预览，一个弹窗走完。

```vue
<GeneratorPipeline table="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| table | `GenTable \| null` | 是 | — |
| step | `1 \| 2 \| 3` | 否 | — |

**事件**：`close`(—)、`saved`(—)、`generate`(GenTable)

**导出类型**：`GenTable`

**参考实现**：`src/views/tool/Generator.vue`


#### InsightPanel

分析栏：关系图 / 画布的右侧详情。头部分类 → 标题与状态 → 主读数 + 迷你柱 →

```vue
<InsightPanel contentKey="文本" kind="文本" title="文本">内容</InsightPanel>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| contentKey | `string` | 是 | — |
| kind | `string` | 是 | — |
| kindIcon | `string` | 否 | — |
| cat | `number` | 否 | — |
| title | `string` | 是 | — |
| subtitle | `string` | 否 | — |
| status | `string` | 否 | — |
| metric | `{ label: string; value: number \| null; unit?: string; bars?: number[] }` | 否 | — |
| tiles | `InsightTile[]` | 否 | — |
| insights | `InsightCard[]` | 否 | — |
| groups | `InsightGroup[]` | 否 | — |

**事件**：`close`(—)、`chip`(InsightChip)

**插槽**：`default`

**导出类型**：`InsightTile`、`InsightCard`、`InsightChip`、`InsightGroup`


#### ListPage

统一列表页：页面头 → 查询区 → 表格面板（刷新 / 导出 / 批量条）→ 分页。

```vue
<ListPage title="文本" list="文本" :columns="[]">内容</ListPage>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 是 | — |
| desc | `string` | 否 | — |
| list | `ListPageState` | 是 | — |
| columns | `Column[]` | 是 | — |
| tableTitle | `string` | 否 | '数据列表' |
| selectable | `boolean` | 否 | — |
| rowKey | `string` | 否 | 'id' |
| minWidth | `number` | 否 | — |
| altView | `boolean` | 否 | — |

**插槽**：`spec`、`actions`、`before`、`alt`、`side`、`search`、`tools`、`name`、`batch`、`default`、`(动态透传)`


#### MenuStarMap

导航星系（图谱舞台，三层下钻）：

```vue
<MenuStarMap :tree="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| tree | `Menu[]` | 是 | — |

**事件**：`edit`(Menu)、`create`(Menu)

**参考实现**：`src/views/system/Menus.vue`


#### OrgCanvas

组织架构画布：整齐树布局铺满内容区，四角留给页面放浮动玻璃面板（#tl / #tr / #bl / #br）。

```vue
<OrgCanvas :tree="[]" :selectedId="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| tree | `Dept[]` | 是 | — |
| selectedId | `number \| null` | 是 | — |

**事件**：`select`(Dept)

**插槽**：`tl`、`tr`、`bl`、`br`

**参考实现**：`src/views/system/Depts.vue`


#### PermissionButton

权限按钮：没有权限码时不渲染（而不是禁用），与后端 @RequiresPermission 使用同一套编码。

```vue
<PermissionButton variant="primary" size="md">内容</PermissionButton>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| perm | `string \| string[]` | 否 | — |
| variant | `'primary' \| 'secondary' \| 'ghost' \| 'text' \| 'danger'` | 否 | 'secondary' |
| icon | `string` | 否 | — |
| label | `string` | 否 | — |
| iconOnly | `boolean` | 否 | — |
| danger | `boolean` | 否 | — |
| size | `'md' \| 'sm'` | 否 | 'md' |
| loading | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |

**插槽**：`default`

**参考实现**：`src/components/business/DictSwatchbook.vue`、`src/components/business/MenuStarMap.vue`、`src/components/business/PostLadder.vue`


#### PermissionMatrix

权限矩阵：行 = 菜单树（目录可折叠），列 = 角色。

```vue
<PermissionMatrix :menus="[]" :roles="[]" :grants="[]" editable />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| menus | `Menu[]` | 是 | — |
| roles | `MatrixRole[]` | 是 | — |
| grants | `Record<number, number[]>` | 是 | — |
| editable | `boolean` | 是 | — |
| saving | `boolean` | 否 | — |

**事件**：`save`(Array<{ roleId: number; menuIds: number[] }>)

**导出类型**：`MatrixRole`


#### PermissionTrace

权限溯源（图谱舞台，三层下钻）：

```vue
<PermissionTrace />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| focus | `unknown` | 否 | — |

**参考实现**：`src/views/system/Roles.vue`


#### PermissionTree

菜单权限树：目录 / 菜单为树节点（勾选含全部下级），按钮权限渲染为节点下方的标签。

```vue
<PermissionTree :menus="[]" :modelValue="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| menus | `Menu[]` | 是 | — |
| modelValue | `number[]` | 是 | — |

**事件**：`update:modelValue`(number[])


#### PostLadder

岗位阶梯（图谱舞台）：岗位按 sort 沿对角线自左下向右上等距铺满舞台，

```vue
<PostLadder :posts="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| posts | `LadderPost[]` | 是 | — |
| loading | `boolean` | 否 | false |

**事件**：`edit`(LadderPost)

**导出类型**：`LadderPost`

**参考实现**：`src/views/system/Posts.vue`


#### SearchForm

查询区：字段放默认插槽，回车即查询。查询 / 重置按钮统一在右侧。

```vue
<SearchForm>内容</SearchForm>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| loading | `boolean` | 否 | — |

**事件**：`search`(—)、`reset`(—)

**插槽**：`default`

**参考实现**：`src/components/business/ListPage.vue`


#### UserSelect

用户下拉：可搜索。valueKey 决定绑定的是用户 ID 还是昵称（部门负责人按昵称存储）。

```vue
<UserSelect modelValue="文本" valueKey="id" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string \| number \| null \| undefined` | 是 | — |
| valueKey | `'id' \| 'nickname'` | 否 | 'id' |
| placeholder | `string` | 否 | '请选择用户' |
| clearable | `boolean` | 否 | true |

**事件**：`update:modelValue`(string \| number \| null)


### 工作台版式（本地扩展）（8）

#### ActivityList

动态列表：头像 + 主文 + 时间 + 右侧标记，用于「最近登录」这类流水。

```vue
<ActivityList :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `ActivityItem[]` | 是 | — |
| avatarSize | `number` | 否 | 30 |

**导出类型**：`ActivityItem`


#### Band

横带分层容器：监控页与详情页的整块分区（Stacked Bands）。

```vue
<Band>内容</Band>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| reveal | `boolean` | 否 | true |

**插槽**：`tools`、`default`


#### BentoCard

工作台卡片：主次布局的基本单元。span 决定栅格占位（复用 pages.css 的 bento-* 变体），

```vue
<BentoCard span="hero">内容</BentoCard>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| span | `'hero' \| 'side' \| 'third' \| 'wide' \| 'narrow' \| 'half' \| 'full'` | 否 | 'third' |
| title | `string` | 否 | — |
| meta | `string` | 否 | — |
| glow | `boolean` | 否 | false |

**插槽**：`tools`、`default`

**参考实现**：`src/views/gallery/demo-slots.ts`、`src/views/gallery/demo-variants.curated-shell.ts`


#### BentoGrid

工作台网格：12 列自适应栅格容器，卡片按 BentoCard 的 span 语义落位。

```vue
<BentoGrid>内容</BentoGrid>
```

**插槽**：`default`


#### KeyValueReadout

键值读数组：主卡与刻度环旁的「峰值 / 均值 / 范围」小表。

```vue
<KeyValueReadout :rows="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| rows | `ReadoutRow[]` | 是 | — |
| columns | `number` | 否 | 3 |

**导出类型**：`ReadoutRow`


#### ReadoutStrip

读数条：一排并列的 Metric，带分隔线；用于概览统计。

```vue
<ReadoutStrip :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `ReadoutItem[]` | 是 | — |

**导出类型**：`ReadoutItem`


#### ShareList

占比条列表：横向条形 + 数值，用于「数据权限分布」这类按数量排序的构成展示。

```vue
<ShareList :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `ShareItem[]` | 是 | — |
| unit | `string` | 否 | '' |

**导出类型**：`ShareItem`


#### ShortcutGrid

快捷入口宫格：图标 + 标题 + 分组副标题，点击上抛 key 与路径。

```vue
<ShortcutGrid :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `ShortcutItem[]` | 是 | — |

**事件**：`select`(ShortcutItem)

**导出类型**：`ShortcutItem`


### Arco 品类对齐（本地扩展）（83）

#### Affix

固钉：让内容在滚动容器内吸附在顶部或底部，滚出后仍保持可见。

```vue
<Affix>内容</Affix>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| offsetTop | `number` | 否 | — |
| offsetBottom | `number` | 否 | — |
| target | `string` | 否 | — |

**插槽**：`default`


#### Alert

提示条：页内静态提示，四型语义色 + 可关闭。

```vue
<Alert type="info">内容</Alert>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| type | `'info' \| 'success' \| 'warning' \| 'error'` | 否 | 'info' |
| title | `string` | 否 | — |
| closable | `boolean` | 否 | — |
| showIcon | `boolean` | 否 | true |
| banner | `boolean` | 否 | — |

**事件**：`close`(—)

**插槽**：`default`、`(动态透传)`


#### Anchor

锚点导航：列出页内小节，点击平滑滚动，滚动时按可见性高亮当前小节。

```vue
<Anchor :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `AnchorItem[]` | 是 | — |
| offsetTop | `number` | 否 | 0 |

**导出类型**：`AnchorItem`


#### AutoComplete

自动补全：输入框敲字时在下方浮出匹配候选，上下键切换、回车落定。

```vue
<AutoComplete :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| options | `AutoCompleteOption[]` | 是 | — |
| placeholder | `string` | 否 | '' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| filter | `(input: string, option: AutoCompleteOption) => boolean` | 否 | — |

**事件**：`update:modelValue`(string)、`select`(string)

**导出类型**：`AutoCompleteOption`


#### AvatarGroup

头像组：多个头像叠压成一摞，超出 max 的部分收成末尾的 +N。

```vue
<AvatarGroup />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| max | `number` | 否 | — |
| size | `number` | 否 | 32 |
| total | `number` | 否 | — |


#### BackTop

回到顶部：滚动超过阈值后浮出圆形按钮，点击平滑回顶。

```vue
<BackTop />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| target | `string` | 否 | — |
| container | `HTMLElement \| null` | 否 | — |
| visibilityHeight | `number` | 否 | 400 |
| right | `number` | 否 | 28 |
| bottom | `number` | 否 | 28 |


#### Badge

徽标：挂在任意元素右上角的数字 / 圆点角标，数字超过 max 显示为 max+。

```vue
<Badge tone="danger">内容</Badge>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| value | `string \| number` | 否 | — |
| dot | `boolean` | 否 | — |
| max | `number` | 否 | 99 |
| tone | `'danger' \| 'info' \| 'ok' \| 'neutral'` | 否 | 'danger' |
| showZero | `boolean` | 否 | — |
| offset | `[number, number]` | 否 | — |

**插槽**：`default`


#### Breadcrumb

面包屑：展示层级路径，末项是当前页，前面的项只有给了 to 才可点。

```vue
<Breadcrumb :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `CrumbItem[]` | 是 | — |

**导出类型**：`CrumbItem`

**参考实现**：`src/views/gallery/Gallery.vue`


#### ButtonGroup

按钮组：把若干个按钮拼成一条，相邻处只留一道描边、首尾各留一次圆角。

```vue
<ButtonGroup size="md" direction="horizontal">内容</ButtonGroup>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| size | `'md' \| 'sm'` | 否 | 'md' |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |

**插槽**：`default`


#### Calendar

日历：月 / 年两种粒度，月网格含上下月补白，今天与选中高亮。

```vue
<Calendar mode="month">内容</Calendar>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| mode | `'month' \| 'year'` | 否 | 'month' |

**事件**：`update:modelValue`(string)

**插槽**：`default`


#### Card

通用卡片：header / body / footer 三区，外加可选的顶部封面。

```vue
<Card>内容</Card>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| subtitle | `string` | 否 | — |
| bordered | `boolean` | 否 | true |
| hoverable | `boolean` | 否 | false |
| loading | `boolean` | 否 | false |

**插槽**：`cover`、`extra`、`default`、`footer`、`(动态透传)`

**参考实现**：`src/views/gallery/demo-slots.ts`


#### CardGrid

卡片网格：把若干张卡按固定列数排布，列宽等分、间距统一。

```vue
<CardGrid>内容</CardGrid>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| columns | `number` | 否 | 3 |
| gutter | `number` | 否 | 16 |

**插槽**：`default`


#### CardMeta

卡片元信息区：头像 + 标题 + 描述的一行横排，供 Card 主体或列表项复用。

```vue
<CardMeta />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | '' |
| description | `string` | 否 | '' |
| avatar | `string` | 否 | '' |

**插槽**：`avatar`、`title`、`description`、`(动态透传)`


#### Carousel

走马灯：CSS transform 位移切换，支持自动播放、循环、指示点与箭头。

```vue
<Carousel indicatorPosition="inside" showArrow="always">内容</Carousel>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| autoplay | `boolean` | 否 | — |
| interval | `number` | 否 | 3000 |
| loop | `boolean` | 否 | true |
| indicatorPosition | `'inside' \| 'outside' \| 'none'` | 否 | 'inside' |
| showArrow | `'always' \| 'hover' \| 'never'` | 否 | 'hover' |
| current | `number` | 否 | 0 |

**事件**：`update:current`(number)、`change`(number)

**插槽**：`default`


#### Cascader

级联选择：按层级逐列展开，每点一层同步回写路径，选到叶子即落定。

```vue
<Cascader :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `Array<string \| number>` | 否 | — |
| options | `CascaderOption[]` | 是 | — |
| placeholder | `string` | 否 | '请选择' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(Array<string \| number>)

**导出类型**：`CascaderOption`


#### CascaderPanel

级联选择面板：Cascader 里被下拉触发器包住的那部分，抽出来后可独立嵌进页面

```vue
<CascaderPanel :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| options | `CascaderPanelOption[]` | 是 | — |
| modelValue | `Array<string \| number>` | 否 | () => [] |
| columnWidth | `number` | 否 | 152 |
| maxHeight | `number` | 否 | 300 |

**事件**：`update:modelValue`(Array<string \| number>)、`change`(Array<string \| number>)

**导出类型**：`CascaderPanelOption`


#### CheckboxGroup

复选组的对外契约：子项靠 checkboxGroupKey 注入上下文，与组件的 setup 逻辑无关，

```vue
<CheckboxGroup :options="[]" direction="horizontal">内容</CheckboxGroup>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `CheckboxValue[]` | 否 | () => [] |
| options | `CheckboxOption[]` | 是 | — |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| max | `number` | 否 | — |
| min | `number` | 否 | — |
| checkAll | `boolean` | 否 | — |

**事件**：`update:modelValue`(CheckboxValue[])、`change`(CheckboxValue[])

**插槽**：`default`

**导出类型**：`CheckboxValue`、`CheckboxOption`、`CheckboxGroupContext`


#### Collapse

折叠面板：以 modelValue 数组承载展开项，accordion 下互斥展开。

```vue
<Collapse expandIconPosition="left">内容</Collapse>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string[]` | 否 | () => [] |
| accordion | `boolean` | 否 | — |
| bordered | `boolean` | 否 | — |
| expandIconPosition | `'left' \| 'right'` | 否 | 'left' |

**事件**：`update:modelValue`(string[])

**插槽**：`default`


#### CollapseItem

折叠子项：标题行 + 内容区，展开态、图标位置全部从父级 Collapse inject 读取。

```vue
<CollapseItem name="文本">内容</CollapseItem>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| name | `string` | 是 | — |
| title | `string` | 否 | '' |
| disabled | `boolean` | 否 | — |

**插槽**：`title`、`extra`、`default`、`(动态透传)`

**参考实现**：`src/views/gallery/demo-slots.ts`


#### ColorPicker

取色器：色块按钮点开面板，预设色板、原生取色盘与十六进制输入三路同源。

```vue
<ColorPicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| presets | `string[]` | 否 | — |
| disabled | `boolean` | 否 | — |
| showText | `boolean` | 否 | false |

**事件**：`update:modelValue`(string)


#### Comment

评论：头像 + 作者 + 时间 + 正文，底部动作条可点或走 actions 插槽。

```vue
<Comment>内容</Comment>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| author | `string` | 否 | '' |
| avatar | `string` | 否 | — |
| content | `string` | 否 | '' |
| datetime | `string` | 否 | '' |
| actions | `string[]` | 否 | () => [] |

**插槽**：`default`、`actions`、`(动态透传)`


#### Countdown

倒计时：按目标时间戳或剩余秒数逐秒倒数，按格式串渲染，走到零时派发 finish。

```vue
<Countdown />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| target | `number` | 否 | — |
| remaining | `number` | 否 | — |
| format | `string` | 否 | 'HH:mm:ss' |
| autostart | `boolean` | 否 | true |

**事件**：`finish`(—)、`change`(number)


#### DataList

数据列表：一份 data 数组 + item 插槽渲染每行，支持分割线、加载骨架与空态。

```vue
<DataList :data="[]" size="sm" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| data | `Array<Record<string, any>>` | 是 | — |
| bordered | `boolean` | 否 | — |
| size | `'sm' \| 'md' \| 'lg'` | 否 | 'md' |
| split | `boolean` | 否 | true |
| loading | `boolean` | 否 | — |

**插槽**：`item`、`empty`


#### DatePicker

日期选择：用原生 Date 自绘月历网格，支持上下月切换、选日、今天与选中高亮。

```vue
<DatePicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '请选择日期' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| format | `string` | 否 | 'YYYY-MM-DD' |

**事件**：`update:modelValue`(string)


#### Descriptions

定义列表（Descriptions）：详情页/订单页常见的「一组字段标签—值」只读卡片，

```vue
<Descriptions :data="[]" layout="horizontal" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| data | `DescriptionItem[]` | 是 | — |
| title | `string` | 否 | — |
| column | `number` | 否 | 3 |
| bordered | `boolean` | 否 | false |
| layout | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |

**插槽**：`extra`、`(动态透传)`

**导出类型**：`DescriptionItem`


#### Divider

分割线：横向分隔段落、纵向分隔并排区块，可带文字居中或靠左靠右。

```vue
<Divider direction="horizontal" orientation="left">内容</Divider>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| orientation | `'left' \| 'right' \| 'center'` | 否 | 'center' |
| dashed | `boolean` | 否 | — |
| margin | `number \| string` | 否 | — |

**插槽**：`default`、`(动态透传)`


#### Dropdown

下拉菜单：点或悬停触发区后浮出选项列表，选中即派发 key 并关闭。

```vue
<Dropdown :items="[]" trigger="click" placement="bottom">内容</Dropdown>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `DropdownItem[]` | 是 | — |
| trigger | `'click' \| 'hover'` | 否 | 'click' |
| placement | `'bottom' \| 'top'` | 否 | 'bottom' |

**事件**：`select`(string)

**插槽**：`default`

**导出类型**：`DropdownItem`


#### DropdownButton

下拉按钮：按钮主体点一下走默认动作，右侧小箭头单独点开菜单，两件事互不干扰。

```vue
<DropdownButton :items="[]" type="primary">内容</DropdownButton>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `DropdownButtonItem[]` | 是 | — |
| type | `'primary' \| 'secondary' \| 'ghost' \| 'text' \| 'danger'` | 否 | 'secondary' |

**事件**：`click`(—)、`select`(string)

**插槽**：`default`

**导出类型**：`DropdownButtonItem`


#### DropdownSubmenu

下拉子菜单：把一组二级选项收在一个菜单项后面，指针悬停时在右侧浮出面板。

```vue
<DropdownSubmenu label="文本" :items="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| label | `string` | 是 | — |
| items | `SubMenuItem[]` | 是 | — |
| disabled | `boolean` | 否 | false |

**事件**：`select`(string)

**导出类型**：`SubMenuItem`


#### Form

表单容器：把「数据模型 + 校验规则 + 错误态 + 提交」这一套编排收到一处。

```vue
<Form model="文本" layout="vertical">内容</Form>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| model | `Record<string, unknown>` | 是 | — |
| rules | `Rules<Record<string, unknown>>` | 否 | — |
| layout | `'vertical' \| 'inline'` | 否 | 'vertical' |

**事件**：`submit`(—)、`invalid`(FormErrors)

**插槽**：`default`

**导出类型**：`FormErrors`


#### GridCol

栅格列：24 栅格制，span 决定占比，offset 前置留白，push / pull 做顺序视觉交换。

```vue
<GridCol>内容</GridCol>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| span | `number` | 否 | 24 |
| offset | `number` | 否 | — |
| push | `number` | 否 | — |
| pull | `number` | 否 | — |
| xs | `number` | 否 | — |
| sm | `number` | 否 | — |
| md | `number` | 否 | — |
| lg | `number` | 否 | — |
| xl | `number` | 否 | — |

**插槽**：`default`

**参考实现**：`src/views/gallery/demo-slots.ts`


#### GridRow

栅格行：24 栅格制的 flex 轨道容器，横纵两个方向各有一份间距。

```vue
<GridRow justify="start" align="start">内容</GridRow>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| gutter | `number \| [number, number]` | 否 | 0 |
| justify | `'start' \| 'center' \| 'end' \| 'space-between' \| 'space-around'` | 否 | 'start' |
| align | `'start' \| 'center' \| 'end' \| 'stretch'` | 否 | 'stretch' |
| wrap | `boolean` | 否 | true |

**插槽**：`default`


#### HelpTip

图标式帮助：一个小图标按钮，悬停或键盘聚焦时浮出功能 / 字段 / 业务说明。

```vue
<HelpTip content="文本" tone="info" placement="top" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| content | `string` | 是 | — |
| title | `string` | 否 | — |
| tone | `'info' \| 'help'` | 否 | 'info' |
| placement | `'top' \| 'bottom' \| 'left' \| 'right'` | 否 | 'top' |
| size | `number` | 否 | 15 |
| label | `string` | 否 | '查看说明' |
| disabled | `boolean` | 否 | — |
| delay | `number` | 否 | 120 |

**参考实现**：`src/views/gallery/DemoCell.vue`


#### Image

图片：加载中显示骨架，失败回落 fallback 或占位图标；preview 时点击开全屏遮罩。

```vue
<Image src="文本" fit="fill" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| src | `string` | 是 | — |
| alt | `string` | 否 | '' |
| width | `number \| string` | 否 | — |
| height | `number \| string` | 否 | — |
| fit | `'fill' \| 'contain' \| 'cover' \| 'none' \| 'scale-down'` | 否 | 'cover' |
| preview | `boolean` | 否 | — |
| fallback | `string` | 否 | — |

**事件**：`load`(—)、`error`(—)


#### ImagePreview

图片预览器：全屏遮罩里看单张大图，支持滚轮与按钮缩放、旋转、Esc / 点遮罩关闭。

```vue
<ImagePreview src="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| src | `string` | 是 | — |
| visible | `boolean` | 否 | false |
| title | `string` | 否 | — |
| zoomable | `boolean` | 否 | true |

**事件**：`update:visible`(boolean)、`close`(—)


#### ImagePreviewGroup

图片预览组：一组图共用一个全屏预览器，底部缩略图导航，左右箭头或方向键切上下张。

```vue
<ImagePreviewGroup :images="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| images | `PreviewImage[]` | 是 | — |
| visible | `boolean` | 否 | false |
| initialIndex | `number` | 否 | 0 |

**事件**：`update:visible`(boolean)、`change`(number)

**导出类型**：`PreviewImage`


#### InputGroup

输入组：把多个输入框 / 按钮横向或纵向拼成一条，整组读作「一个控件」而不是几个并排控件。

```vue
<InputGroup direction="horizontal">内容</InputGroup>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |

**插槽**：`default`


#### InputNumber

数字输入：左右步进按钮夹住中间输入框，越界钳制、按 precision 定小数位。

```vue
<InputNumber />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `number \| null` | 否 | — |
| min | `number` | 否 | — |
| max | `number` | 否 | — |
| step | `number` | 否 | 1 |
| precision | `number` | 否 | 0 |
| disabled | `boolean` | 否 | — |
| placeholder | `string` | 否 | — |

**事件**：`update:modelValue`(number \| null)


#### InputPassword

密码输入框：在输入框内自带一个「明文/密文」切换钮，点击即在 password 与 text 间切换。

```vue
<InputPassword />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | '' |
| placeholder | `string` | 否 | '请输入密码' |
| disabled | `boolean` | 否 | — |
| defaultVisible | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


#### InputSearch

搜索输入：把「填词 + 触发搜索」收成一个控件，回车与点右侧按钮完全等价。

```vue
<InputSearch />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | '' |
| placeholder | `string` | 否 | '' |
| loading | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| allowClear | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)、`search`(string)

**参考实现**：`src/views/gallery/Gallery.vue`


#### InputTag

标签输入：回车把当前文本收成标签，退格在空输入时删末尾，标签上的叉逐个移除。

```vue
<InputTag />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string[]` | 否 | — |
| placeholder | `string` | 否 | '' |
| max | `number` | 否 | — |
| disabled | `boolean` | 否 | — |
| allowDuplicate | `boolean` | 否 | — |

**事件**：`update:modelValue`(string[])


#### LinkText

链接文字：语义色 + 可选下划线，禁用态降级为纯文本，无 href 时退化为 span。

```vue
<LinkText target="_blank" type="default">内容</LinkText>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| href | `string` | 否 | — |
| target | `'_blank' \| '_self'` | 否 | '_self' |
| disabled | `boolean` | 否 | — |
| underline | `boolean` | 否 | — |
| type | `'default' \| 'primary' \| 'success' \| 'warning' \| 'danger'` | 否 | 'primary' |

**插槽**：`default`


#### Mention

提及输入：textarea 里敲出 trigger（默认 @）即浮出候选，选中后把触发词替换成候选值。

```vue
<Mention :options="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| options | `MentionOption[]` | 是 | — |
| trigger | `string` | 否 | '@' |
| placeholder | `string` | 否 | — |
| rows | `number` | 否 | 3 |

**事件**：`update:modelValue`(string)

**导出类型**：`MentionOption`


#### Menu

菜单：纵向或横向的导航列表，支持子菜单递归展开与折叠态。

```vue
<Menu :items="[]" mode="vertical" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `MenuItem[]` | 是 | — |
| modelValue | `string` | 否 | — |
| collapsed | `boolean` | 否 | — |
| mode | `'vertical' \| 'horizontal'` | 否 | 'vertical' |

**事件**：`update:modelValue`(string)

**导出类型**：`MenuItem`


#### MenuNode

菜单节点：菜单的递归单元，自身承载子项列表。

```vue
<MenuNode item="文本" :depth="0" vertical />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| item | `MenuNodeItem` | 是 | — |
| depth | `number` | 是 | — |
| vertical | `boolean` | 是 | — |
| collapsed | `boolean` | 否 | — |
| selected | `string` | 否 | — |

**事件**：`select`(string)

**参考实现**：`src/components/extend/Menu.vue`


#### MonthPicker

月份选择：一格一月共 12 格，头部只翻年不翻月，选完立即回写。

```vue
<MonthPicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '请选择月份' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


#### Notification

通知卡片：单条展示型，只负责一条通知的排版与关闭。

```vue
<Notification type="info">内容</Notification>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| type | `'info' \| 'success' \| 'warning' \| 'error'` | 否 | 'info' |
| title | `string` | 否 | — |
| message | `string` | 否 | — |
| closable | `boolean` | 否 | — |
| showIcon | `boolean` | 否 | true |

**事件**：`close`(—)

**插槽**：`default`


#### OverflowList

溢出列表：按容器宽度逐项排布，放不下的项收进 +N 下拉，点开可看全部。

```vue
<OverflowList :items="[]" collapseFrom="start">内容</OverflowList>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `Array<{ key: string \| number; label: string }>` | 是 | — |
| maxCount | `number` | 否 | — |
| collapseFrom | `'start' \| 'end'` | 否 | 'end' |

**插槽**：`default`


#### Popconfirm

气泡确认：点触发区浮出一个小气泡，确认或取消后收起。

```vue
<Popconfirm placement="top">内容</Popconfirm>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| message | `string` | 否 | — |
| okText | `string` | 否 | '确定' |
| cancelText | `string` | 否 | '取消' |
| danger | `boolean` | 否 | — |
| placement | `'top' \| 'bottom' \| 'left' \| 'right'` | 否 | 'top' |

**事件**：`ok`(—)、`confirm`(—)、`cancel`(—)

**插槽**：`default`


#### Popover

气泡卡片：比 Tooltip 更重的一块浮层，可放标题、正文与可点内容。

```vue
<Popover trigger="click" placement="top">内容</Popover>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| title | `string` | 否 | — |
| content | `string` | 否 | — |
| trigger | `'click' \| 'hover'` | 否 | 'hover' |
| placement | `'top' \| 'bottom' \| 'left' \| 'right'` | 否 | 'top' |
| width | `number` | 否 | 240 |

**插槽**：`default`、`content`、`(动态透传)`


#### Progress

进度条：line 用宽度过渡、circle 用 SVG 描边偏移，两条实现共用一套状态色。

```vue
<Progress :percent="0" type="line" status="normal" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| percent | `number` | 是 | — |
| type | `'line' \| 'circle'` | 否 | 'line' |
| status | `'normal' \| 'success' \| 'error' \| 'warning'` | 否 | 'normal' |
| size | `number` | 否 | 120 |
| showText | `boolean` | 否 | true |
| strokeWidth | `number` | 否 | 8 |


#### QuarterPicker

季度选择：一格一季共 4 格，头部只翻年。

```vue
<QuarterPicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '请选择季度' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


#### Radio

单选框：优先读最近 RadioGroup 的上下文，独立使用时退回自身 props。

```vue
<Radio value="文本">内容</Radio>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `RadioValue` | 否 | — |
| value | `RadioValue` | 是 | — |
| disabled | `boolean` | 否 | — |
| label | `string` | 否 | — |

**事件**：`update:modelValue`(RadioValue)

**插槽**：`default`

**参考实现**：`src/views/gallery/demo-slots.ts`、`src/views/gallery/demo-variants.curated-inputs.ts`


#### RadioGroup

单选组的对外契约：Radio 依赖 radioGroupKey 注入上下文，独立于组件的 setup 逻辑，

```vue
<RadioGroup modelValue="文本" direction="horizontal">内容</RadioGroup>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `RadioValue` | 是 | — |
| disabled | `boolean` | 否 | — |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |

**事件**：`update:modelValue`(RadioValue)

**插槽**：`default`

**导出类型**：`RadioValue`、`RadioGroupContext`


#### RangePicker

日期区间选择：单个月历网格里两步连选，先点开始再点结束。

```vue
<RangePicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `[string, string]` | 否 | — |
| placeholder | `string` | 否 | '请选择日期区间' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| format | `string` | 否 | 'YYYY-MM-DD' |

**事件**：`update:modelValue`([string, string])


#### Rate

评分：五角星按整数或半星打分，hover 预览、点击定值、再点同一值得可清空。

```vue
<Rate />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `number` | 否 | 0 |
| count | `number` | 否 | 5 |
| allowHalf | `boolean` | 否 | — |
| readonly | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| allowClear | `boolean` | 否 | — |

**事件**：`update:modelValue`(number)


#### ResizeBox

伸缩框：拖动右下角把手把内容压成指定宽高，宽高直接落到容器尺寸上。

```vue
<ResizeBox direction="horizontal">内容</ResizeBox>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| width | `number` | 否 | — |
| height | `number` | 否 | — |
| minWidth | `number` | 否 | — |
| maxWidth | `number` | 否 | — |
| minHeight | `number` | 否 | — |
| maxHeight | `number` | 否 | — |

**事件**：`resize`({ width: number; height: number })

**插槽**：`default`、`resize`


#### Result

结果页：一次操作或一个错误码的终态陈述。

```vue
<Result status="success">内容</Result>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| status | `'success' \| 'error' \| 'warning' \| 'info' \| '404' \| '403' \| '500'` | 否 | 'info' |
| title | `string` | 否 | — |
| subTitle | `string` | 否 | — |

**插槽**：`default`、`extra`、`(动态透传)`


#### Skeleton

骨架屏：loading 为 true 时按 type / rows 渲染占位块，否则渲染 default 插槽。

```vue
<Skeleton type="text">内容</Skeleton>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| loading | `boolean` | 否 | true |
| animation | `boolean` | 否 | true |
| rows | `number` | 否 | 1 |
| type | `'text' \| 'image' \| 'circle' \| 'rect'` | 否 | 'text' |
| width | `number \| string` | 否 | — |
| height | `number \| string` | 否 | — |

**插槽**：`default`

**参考实现**：`src/components/extend/Card.vue`


#### Slider

滑块：原生 <input type="range"> 作无障碍底座，视觉轨道与滑块叠在其上。

```vue
<Slider />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `number \| [number, number]` | 否 | 0 |
| min | `number` | 否 | 0 |
| max | `number` | 否 | 100 |
| step | `number` | 否 | 1 |
| disabled | `boolean` | 否 | — |
| showTicks | `boolean` | 否 | — |
| range | `boolean` | 否 | — |

**事件**：`update:modelValue`(number \| [number, number])


#### Space

间距：给一组子项之间垫出统一距离，方向与对齐由一行 flex 决定。

```vue
<Space direction="horizontal" size="sm" align="start">内容</Space>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| size | `'sm' \| 'md' \| 'lg' \| number` | 否 | 'md' |
| align | `'start' \| 'center' \| 'end' \| 'baseline'` | 否 | 'center' |
| wrap | `boolean` | 否 | false |
| split | `boolean` | 否 | — |

**插槽**：`default`


#### Spin

加载中：只渲染一个转圈，或用 wrapper 在内容上叠一层遮罩。

```vue
<Spin size="sm">内容</Spin>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| loading | `boolean` | 否 | true |
| size | `'sm' \| 'md' \| 'lg'` | 否 | 'md' |
| tip | `string` | 否 | — |
| wrapper | `boolean` | 否 | — |

**插槽**：`default`


#### SplitPane

分栏：一块区域按可拖动的分隔条切成两半，横向出左右、纵向出上下。

```vue
<SplitPane direction="horizontal" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| modelValue | `number` | 否 | — |
| min | `number` | 否 | — |
| max | `number` | 否 | — |

**事件**：`update:modelValue`(number)、`resize`(number)

**插槽**：`isHorizontal ? 'left' : 'top'`、`isHorizontal ? 'right' : 'bottom'`


#### Steps

步骤条：横向或纵向的工序进度，已完成打勾、当前高亮、未开始置灰。

```vue
<Steps :current="0" :items="[]" direction="horizontal" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| current | `number` | 是 | — |
| items | `StepItem[]` | 是 | — |
| direction | `'horizontal' \| 'vertical'` | 否 | 'horizontal' |
| clickable | `boolean` | 否 | — |

**事件**：`change`(number)

**导出类型**：`StepItem`


#### StyledScrollbar

自定义滚动条：滚动容器保持原生 overflow / 键盘 / 触控板行为，只额外画一条浮动滑块压在上面。

```vue
<StyledScrollbar direction="vertical">内容</StyledScrollbar>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| direction | `'vertical' \| 'horizontal' \| 'both'` | 否 | 'vertical' |
| maxHeight | `number \| string` | 否 | — |
| maxWidth | `number \| string` | 否 | — |
| always | `boolean` | 否 | — |

**插槽**：`default`


#### TabPane

标签面板：Tabs 内容区的单页容器，active 为真才显示，切换只切可见性不销毁内容。

```vue
<TabPane>内容</TabPane>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| name | `string` | 否 | — |
| label | `string` | 否 | — |
| active | `boolean` | 否 | — |

**插槽**：`default`

**参考实现**：`src/views/gallery/demo-slots.ts`


#### Tabs

标签页：横向切换一组视图，line 型用滑动下划线、card 型用底色切换。

```vue
<Tabs modelValue="文本" :items="[]" type="line">内容</Tabs>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 是 | — |
| items | `TabItem[]` | 是 | — |
| type | `'line' \| 'card'` | 否 | 'line' |
| closable | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)、`close`(string)

**插槽**：`default`

**导出类型**：`TabItem`


#### Textarea

多行文本域：在 TextInput 的 multiline 之外补两项真实能力——自动高度与字数统计。

```vue
<Textarea />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | '' |
| placeholder | `string` | 否 | — |
| disabled | `boolean` | 否 | — |
| readonly | `boolean` | 否 | — |
| invalid | `boolean` | 否 | — |
| rows | `number` | 否 | 3 |
| autoSize | `boolean` | 否 | — |
| maxRows | `number` | 否 | 8 |
| maxlength | `number` | 否 | — |
| showCount | `boolean` | 否 | true |

**事件**：`update:modelValue`(string)


#### TimePicker

时间选择：触发区 + 下拉面板，面板里时 / 分两列滚动选择，底部提供「此刻」快捷。

```vue
<TimePicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '选择时间' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| format | `string` | 否 | 'HH:mm:ss' |

**事件**：`update:modelValue`(string)


#### Timeline

时间轴：由 items 数据派生节点，左侧 / 右侧 / 交替三种排布，可反向。

```vue
<Timeline :items="[]" mode="left" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| items | `TimelineEntry[]` | 是 | — |
| mode | `'left' \| 'right' \| 'alternate'` | 否 | 'left' |
| reverse | `boolean` | 否 | — |

**导出类型**：`TimelineEntry`


#### TimelineItem

时间轴节点：圆点 + 竖线 + 时间 / 标题 / 内容，可单独使用也可被 Timeline 批量渲染。

```vue
<TimelineItem>内容</TimelineItem>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| label | `string` | 否 | '' |
| content | `string` | 否 | '' |
| time | `string` | 否 | '' |
| color | `string` | 否 | — |
| dot | `string` | 否 | 'default' |

**插槽**：`dot`、`default`、`(动态透传)`

**参考实现**：`src/components/extend/Timeline.vue`


#### Tooltip

提示气泡：hover / focus 时在目标旁浮出说明，位置自动避让视口边缘。

```vue
<Tooltip placement="top">内容</Tooltip>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| content | `string` | 否 | — |
| placement | `'top' \| 'bottom' \| 'left' \| 'right'` | 否 | 'top' |
| disabled | `boolean` | 否 | — |
| delay | `number` | 否 | 120 |

**插槽**：`default`


#### Transfer

穿梭框：左「待选」右「已选」两栏，中间箭头把勾选项推过去。

```vue
<Transfer :data="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `Array<string \| number>` | 否 | () => [] |
| data | `TransferItem[]` | 是 | — |
| titles | `[string, string]` | 否 | () => ['待选', '已选'] |
| searchable | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |

**事件**：`update:modelValue`(Array<string \| number>)、`change`(any[])

**导出类型**：`TransferItem`


#### Tree

通用递归树：只认 key/label/children 这套通用结构，不绑定任何业务数据模型，

```vue
<Tree :data="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| data | `TreeNode[]` | 是 | — |
| modelValue | `TreeKey[]` | 否 | () => [] |
| checkable | `boolean` | 否 | false |
| selectable | `boolean` | 否 | true |
| multiple | `boolean` | 否 | false |
| defaultExpandAll | `boolean` | 否 | false |
| showLine | `boolean` | 否 | false |
| filterText | `string` | 否 | '' |

**事件**：`update:modelValue`(TreeKey[])、`select`(TreeKey)、`check`(TreeKey[])、`expand`(TreeKey[])

**导出类型**：`TreeNode`、`TreeKey`、`TreeCheckState`、`TreeContext`


#### TreeNode

树的递归单元：一行 = 展开箭头 + 可选复选框 + 图标 + 标签，下方按需渲染子级。

```vue
<TreeNode node="文本" :depth="0" parentKey="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| node | `TreeNode` | 是 | — |
| depth | `number` | 是 | — |
| parentKey | `TreeKey \| null` | 是 | — |

**参考实现**：`src/components/extend/Tree.vue`


#### TreeSelect

树选择：触发区点开一个下拉树面板，支持层级缩进、展开折叠、单选与多选。

```vue
<TreeSelect :data="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string \| number \| Array<string \| number> \| null` | 否 | null |
| data | `TreeNode[]` | 是 | — |
| placeholder | `string` | 否 | '请选择' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |
| multiple | `boolean` | 否 | — |

**事件**：`update:modelValue`(TreeSelectValue)

**导出类型**：`TreeNode`、`TreeSelectValue`


#### Trigger

触发器：通用「定位 + 显隐」底层原语，Dropdown / Popover 这类浮层都由它派生。

```vue
<Trigger placement="top">内容</Trigger>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| trigger | `Array<'click' \| 'hover' \| 'focus' \| 'contextmenu'>` | 否 | () => ['hover'] |
| placement | `'top' \| 'bottom' \| 'left' \| 'right' \| 'bottom-start' \| 'bottom-end'` | 否 | 'bottom' |
| popupVisible | `boolean` | 否 | false |
| disabled | `boolean` | 否 | — |
| popupClass | `string` | 否 | — |

**事件**：`update:popupVisible`(boolean)

**插槽**：`default`、`content`


#### Typography

排版：按 type / heading 决定语义标签，叠加加粗、高亮、下划线、删除线、行内代码、省略、复制等修饰。

```vue
<Typography type="title">内容</Typography>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| type | `'title' \| 'text' \| 'paragraph'` | 否 | 'text' |
| heading | `1 \| 2 \| 3 \| 4 \| 5` | 否 | — |
| ellipsis | `boolean \| number` | 否 | — |
| bold | `boolean` | 否 | — |
| mark | `boolean` | 否 | — |
| underline | `boolean` | 否 | — |
| delete | `boolean` | 否 | — |
| code | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| copyable | `boolean` | 否 | — |
| content | `string` | 否 | — |

**事件**：`copy`(—)

**插槽**：`default`


#### Upload

上传：只做前端文件选择与列表管理，不做真实网络上传。

```vue
<Upload />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| fileList | `UploadFile[]` | 否 | () => [] |
| accept | `string` | 否 | — |
| multiple | `boolean` | 否 | — |
| disabled | `boolean` | 否 | — |
| limit | `number` | 否 | 0 |
| drag | `boolean` | 否 | false |
| autoUpload | `boolean` | 否 | false |

**事件**：`change`(UploadFile[])、`remove`(UploadFile)、`progress`(UploadFile)、`success`(UploadFile)

**导出类型**：`UploadFile`


#### VerificationCode

验证码输入：定长数字格，逐格输入自动跳格，退格回跳，支持整串粘贴。

```vue
<VerificationCode />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| length | `number` | 否 | 6 |
| disabled | `boolean` | 否 | — |
| invalid | `boolean` | 否 | — |
| numeric | `boolean` | 否 | true |
| placeholder | `string` | 否 | — |
| autofocus | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)、`complete`(string)


#### Watermark

水印：用 canvas 把文字 / 图片绘成 dataURL，作为背景图平铺在内容之上。

```vue
<Watermark>内容</Watermark>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| content | `string \| string[]` | 否 | () => [] |
| image | `string` | 否 | — |
| rotate | `number` | 否 | -22 |
| gap | `[number, number]` | 否 | () => [100, 100] |
| font | `{ fontSize?: number; color?: string }` | 否 | — |
| zIndex | `number` | 否 | 9 |

**插槽**：`default`


#### WeekPicker

周选择：列出 ISO 周（周一开头，第 1 周含当年首个周四），每行显示周序号与起止日期。

```vue
<WeekPicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '请选择周' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


#### YearPicker

年份选择：一页 12 年（十年跨度加前后各一年的缓冲），头部显示跨度并整页翻。

```vue
<YearPicker />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| modelValue | `string` | 否 | — |
| placeholder | `string` | 否 | '请选择年份' |
| disabled | `boolean` | 否 | — |
| clearable | `boolean` | 否 | — |

**事件**：`update:modelValue`(string)


### 自研图表（6）

#### BarChart

柱状图：柱子从基线生长（结 Crystallize），highlight 柱用斜线填充表示「当前」。

```vue
<BarChart :values="0" :labels="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| values | `number[]` | 是 | — |
| labels | `string[]` | 是 | — |
| failed | `number[]` | 否 | () => [] |
| highlight | `number \| null` | 否 | null |
| height | `number` | 否 | 168 |
| unit | `string` | 否 | '' |

**参考实现**：`src/views/Dashboard.vue`


#### HeatGrid

星期 × 小时热力格：格子按分位分 5 级（青柠由浅到深），失败占比高的格子叠斜线（--hatch）。

```vue
<HeatGrid :cells="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| cells | `HeatCell[]` | 是 | — |
| loading | `boolean` | 否 | — |

**参考实现**：`src/views/monitor/LoginLog.vue`


#### RelationGraph

关系图：节点与连线由页面按当前层级算好目标坐标，本组件负责「活起来」——

```vue
<RelationGraph :nodes="[]" :links="[]" variant="light">内容</RelationGraph>
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| nodes | `GraphNode[]` | 是 | — |
| links | `GraphLink[]` | 是 | — |
| activeId | `string \| null` | 否 | null |
| highlight | `string[] \| null` | 否 | null |
| variant | `'light' \| 'stage'` | 否 | 'light' |
| network | `NetworkData \| null` | 否 | null |
| networkFocus | `number \| null` | 否 | null |
| networkAlpha | `number` | 否 | 1 |
| orbits | `Array<{ rx: number; ry: number }>` | 否 | () => [] |
| burstKey | `number \| string` | 否 | 0 |
| label | `string` | 否 | '关系图' |
| pannable | `boolean` | 否 | false |
| size | `unknown` | 否 | — |

**事件**：`select`(GraphNode)、`back`(—)、`hover`(string \| null)

**插槽**：`tl`、`tr`、`bl`、`br`、`default`

**导出类型**：`GraphNode`、`GraphLink`


#### Swimlane

时间轴泳道：泳道 × 时间轴。默认聚焦到 [首条 −1h, 现在 +1h]（至少 6 小时），可切回全天。

```vue
<Swimlane :lanes="[]" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| lanes | `SwimlaneLane[]` | 是 | — |
| nowSec | `number \| null` | 否 | null |
| compact | `boolean` | 否 | false |
| maxLanes | `number` | 否 | 8 |
| slowMs | `number` | 否 | 1000 |

**事件**：`select`({ lane: SwimlaneLane; block: TimelineBlock })

**导出类型**：`SwimlaneLane`

**参考实现**：`src/views/Dashboard.vue`、`src/views/monitor/OperLog.vue`


#### TickRing

刻度环：60 根径向刻度按顺时针逐根点亮（导 Conduct），

```vue
<TickRing :value="0" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| value | `number \| null \| undefined` | 是 | — |
| display | `number` | 否 | — |
| unit | `string` | 否 | '%' |
| label | `string` | 否 | — |
| size | `number` | 否 | 168 |
| ticks | `number` | 否 | 60 |
| decimals | `number` | 否 | 1 |

**参考实现**：`src/views/Dashboard.vue`


#### TrendChart

纯 SVG 趋势图：按容器真实宽度计算路径，线宽不被拉伸。

```vue
<TrendChart :values="0" :labels="[]" tone="blue" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| values | `number[]` | 是 | — |
| labels | `string[]` | 是 | — |
| secondary | `number[]` | 否 | — |
| secondaryLabel | `string` | 否 | '失败' |
| primaryLabel | `string` | 否 | '数值' |
| height | `number` | 否 | 220 |
| unit | `string` | 否 | '' |
| band | `[number, number] \| null` | 否 | null |
| dots | `boolean` | 否 | true |
| tone | `'blue' \| 'ink'` | 否 | 'blue' |

**参考实现**：`src/views/Dashboard.vue`、`src/views/monitor/LoginLog.vue`、`src/views/monitor/OperLog.vue`


### 外壳布局（6）

#### AppShell

```vue
<AppShell />
```

**参考实现**：`src/router/index.ts`


#### AppearanceDialog

```vue
<AppearanceDialog open />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |

**事件**：`close`(—)

**参考实现**：`src/components/layout/AppShell.vue`


#### CommandPalette

命令面板：最近访问 / 页面 / 用户 / 快捷动作 四组结果，

```vue
<CommandPalette open />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |

**事件**：`close`(—)、`action`('appearance' \| 'password' \| 'logout')

**参考实现**：`src/components/layout/AppShell.vue`


#### PasswordDialog

```vue
<PasswordDialog open />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| open | `boolean` | 是 | — |

**事件**：`close`(—)

**参考实现**：`src/components/layout/AppShell.vue`


#### Sidebar

```vue
<Sidebar />
```

**事件**：`navigate`(—)

**参考实现**：`src/components/layout/AppShell.vue`


#### Topbar

```vue
<Topbar />
```

**事件**：`toggle-rail`(—)、`command`(—)、`appearance`(—)、`password`(—)、`logout`(—)

**参考实现**：`src/components/layout/AppShell.vue`


### 根级组件（2）

#### Icon

```vue
<Icon name="文本" />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| name | `string` | 是 | — |
| size | `number` | 否 | 18 |
| stroke | `number` | 否 | 1.6 |

**参考实现**：`src/components/business/AskDock.vue`、`src/components/business/BoardView.vue`、`src/components/business/DeptTree.vue`、`src/components/business/DictSwatchbook.vue`、`src/components/business/GeneratorPipeline.vue`、`src/components/business/InsightPanel.vue`、`src/components/business/MenuStarMap.vue`、`src/components/business/PermissionMatrix.vue`


#### NeuralNet

神经网络画布：能力模块节点缓慢呼吸，脉冲沿连线往返（导 Conduct）。

```vue
<NeuralNet />
```

| prop | 类型 | 必填 | 默认 |
| --- | --- | --- | --- |
| burstKey | `number \| string` | 否 | 0 |

**参考实现**：`src/views/Login.vue`
