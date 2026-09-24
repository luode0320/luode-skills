# 来源记录

## 2026-09-20 更新：project-ellipal-admin-vue-tab-page-rules（内部更新通道，骨架去页头卡）

- **来源**：用户看着页面截图指出——「这个头部的展示对于 tab 多功能切换已经完全不需要了，多余了，删除他，把 tab 的切换移动到这个头部的位置，设计一个新的 tab 切换的样式」。内部更新通道，无外部源。
- **推翻的旧结论**：原骨架「页头 `a-card`（`a-list-item-meta` 标题块）+ 内容 `a-card` 包 `a-tabs`」与原样式条款「`type="rounded"` 是既定样式，不要换成 `line` / `card`」，两条都已作废。
- **核心新增**：多功能 tab 页的页签名本身就是功能索引，再挂「XX管控 + 一句话把四个页签念一遍」的标题卡纯属占一屏高度；页签条顶到卡片最上方兼任页面头部，但要担得起头部的视觉重量必须换 `type="line" size="large"` + `.page-head-tabs`（nav 分隔线 / 16px 字号 / 3px 圆角 ink 三条 `:deep()` 缺一不可，arco 把这三层样式分挂在三个类上）——rounded 的胶囊选中态在没有页头卡托底时压不住。
- **落点**：SKILL.md 骨架段、约定一样式条款、约定三代码示例、「进入后先做什么」第 1 步，共 4 处同步改写。
- **规则文件声明**：`AGENTS.md` / `CLAUDE.md` 的「## 多功能 tab 页优先规则」各加一条骨架条款（两份 md5 一致 `7de543291a4996b540b078fcd1b038dd`）。
- **验证**：`PYTHONUTF8=1 quick_validate.py` → `Skill is valid!`；实现侧浏览器实测四页签可切、复用组件出数、零 console error、`npm run build-test` 退出码 0。
- **字典刷新**：不适用——同下。

## 2026-09-20 新建：project-ellipal-admin-vue-tab-page-rules（通道 B 主动点名，多功能 tab 页）

- **来源**：用户主动点名——「我们币对管理做的不错，就是一个页面通过 tab 切换多个功能的，我们希望吸收到项目 skill，我们后续有其他功能也可以使用，做成多功能 tab 切换」。无外部源。
- **证据**：同会话真实落地的 `go-admin-vue3/src/views/exchange/pair-control/index.vue`（四页签：临时下架 / 永久下架内联，服务商链币映射 / 热门列表复用组件）；`embedded` prop 实现在 `views/backend/exchangeProviderChainMap/index.vue:268-274` 与 `views/backend/exchangeCoinsOrdered/index.vue`；`lazy-load` 边界结论来自浏览器 `read_network_requests` 实测（进页面只发 3 条内联 pane 的请求，两条组件式 pane 的 getPage 在切页签后才发）。
- **落点**：`ellipal_admin/skills/project-ellipal-admin-vue-tab-page-rules/SKILL.md`（单文件，暂无 references——五条约定的代码片段都在 20 行内，不够拆 recipe）。
- **分层判定**：五条约定均依赖本仓库事实（arco 2.57、`.container` + 双 card 骨架、`section-tip-icon` 类名、`DEFAULT_PAGE_SIZE` 既有约定、菜单 API 权限人工勾选），换项目不成立 → 项目级，不抽用户级通用层。
- **核心新增（此前无处记载）**：`lazy-load` 只延迟组件式 pane 的挂载，内联 pane 的数据加载写在页面 `onMounted` 里完全不受它管——加了 `lazy-load` 就以为全部懒加载是错的。
- **同域冗余扫描**：范围 = 项目根 `skills/` 全部 5 个 skill。与 `project-ellipal-admin-vue-table-page-rules`（表格列宽 / 拖拽 / 分页器）、`project-ellipal-admin-form-help-tooltip-rules`（字段级 tooltip）边界互斥，已在两侧「权责边界」互引；`DEFAULT_PAGE_SIZE` 只在本 skill 提一句并指回表格 skill 约定三，不重复定义 → **PASS**。
- **规则文件声明**：`AGENTS.md` / `CLAUDE.md` 同步新增「## 多功能 tab 页优先规则」章节（两份 md5 一致）。
- **验证**：`PYTHONUTF8=1 quick_validate.py` → `Skill is valid!`；SKILL.md 内 6 条相对引用路径逐一 `test -e` 全部可达；文件 UTF-8。
- **字典刷新**：不适用——同下（`ROOT` 固定 `~/.claude/skills`，不扫描项目根 `skills/`）。
- **关联记忆**：`browser-pane-hidden-breaks-css-transition`、`vite-dev-needs-mode-dev-flag`、`vue-admin-ui-verify-without-login`。

## 2026-09-02 更新：project-ellipal-admin-vue-table-page-rules（内部更新通道，补列宽拖拽）

- **来源**：用户主动点名——「把这个支持表头拖宽的也吸收到项目的 skill 中，之前已经吸收了表头拖动了」。内部更新通道，无外部源。
- **证据**：同会话在 `go-admin-vue3/src/views/reqsend/index.vue`（转账流水页）真实落地并通过 `npm run build-test`；arco 结论来自读源码——`table.js` `contentStyle`（`<table>` width 由 `scroll.x` 硬设）、`table-col-group.js:52`（`columnWidth[dataIndex] || column.width`）、`table.js:1247`（末列无拖宽把手）、`utils.js:91`（拖宽按 dataIndex 存）、`style/index.less:86`（handle 绝对定位 z-index:1）。
- **裁决**：7 条原子条目 → 合并 6 / 保留本地 1（build-test + 产物 grep 验证法本地已有且更完整）。agent 通用性：全部「通用」，无单 agent 绑定。环境依赖：N/A（纯前端约定，无环境变量 / hook / 依赖安装）。
- **落点**：约定二扩为「表头拖动交互（换列位置 + 调列宽）」两个子节，不新开约定四——避免 `scroll.x` 规则在两节重复讲；成套代码进 `references/column-drag-recipe.md` 第 5 段。
- **核心新增**：只加 `:column-resizable="true"` 不够——`scroll.x` 大于列宽之和时多余宽度被 `table-layout: fixed` 摊回每列，拖 10px 实际变 `10 × (scroll.x / 列宽之和)` px；必须把 `scroll.x` 做成响应式求和，并把字符串权重 width 按 `X / S` 倍率换算成真实像素（转账流水页实测 3000/1480 = 2.03，换算后新和 2960，差 1.4% 肉眼无差别）。
- **整理去重（3 处）**：① 约定一的静态 `TABLE_SCROLL_X` 常量升级为响应式 `tableScrollX`，SKILL.md 与 recipe 两处同步，不并存两套写法（全仓库 grep `TABLE_SCROLL_X` 残留为 0）；② 约定一「既有页面跟随字面量 `x: 2000` 即可」补例外限定，消除与 resizable 场景的自相矛盾；③ 落盘后自查发现 SKILL.md 2.2 的 JS 代码段与 recipe 第 5 段逐字重复，按「单一权威 + 引用」收敛——SKILL.md 只留判据与坑，成套代码归 recipe。
- **同域冗余扫描**：范围 = 项目根 `skills/` 全部 2 个 skill。`project-ellipal-admin-route-interface-mapping-rules` grep `scroll.x` / `a-table` / `columns` 零命中，无交叉重复。发现 1 处（本文件族内部 2.2↔recipe 重复）、清理 1 处 → **PASS**。
- **净增**：SKILL.md +89 行、recipe +66 行、openai.yaml +4/-2；约定数保持三条不膨胀，收敛后 SKILL.md 13,064 字节 / recipe 9,641 字节。
- **验证**：`PYTHONUTF8=1 quick_validate.py` → `Skill is valid!`；回归校验同域兄弟 skill 亦 PASS；三文件均 UTF-8，引用链 `references/column-drag-recipe.md` 可达无断链。
- **字典刷新**：不适用——同下（`ROOT` 固定 `~/.claude/skills`，不扫描项目根 `skills/`）。
- **关联记忆**：新增 `arco-resizable-needs-scrollx-equals-sum`；已有 `arco-column-drag-via-titleslotname`。

## 2026-09-01 创建：project-ellipal-admin-vue-table-page-rules（项目本地 skill）

- **来源**：用户主动点名（通道 B）——「列表数据支持左右滚动查看和支持将表头拖动左右切换位置、默认10条一页吸收到我们项目本地skill」。
- **证据**：同会话在 `go-admin-vue3/src/views/backend/exchangeCoinsOrdered/index.vue` 三次真实落地（横向滚动 `scroll.x` 求和、`titleSlotName` 拖拽换列、`DEFAULT_PAGE_SIZE = 10`），每次 `npm run build-test` 通过；arco 插槽结论来自读 `node_modules/@arco-design/web-vue/es/table/table-th.js` 源码（2.57.0 无 `thTitle` 插槽，`#th` 会接管整个 th 导致丢排序箭头）。
- **落点**：`ellipal_admin/skills/project-ellipal-admin-vue-table-page-rules/`（SKILL.md + agents/openai.yaml + references/column-drag-recipe.md）。
- **分层判定**：arco 机制细节本可上升为用户级通用层，但本仓库 admin 前端栈锁定 arco 2.57 且约定含项目产品口径（默认 10 条/页、既有 30 多页 `:scroll="{ x: 2000 }"` 字面量惯例、本环境 vite 不可达只能构建验证），整体判为项目层；SKILL.md 内已注明"换到非 arco 项目本 skill 不成立"。
- **踩坑（写 skill 时命中）**：`quick_validate.py` 用系统 GBK 读文件，读 UTF-8 中文 SKILL.md 会 `UnicodeDecodeError`，须 `PYTHONUTF8=1`；首版 description 含 `: ` 与 `{` 导致 YAML frontmatter 解析失败（`mapping values are not allowed here`），改写措辞后通过。
- **验证**：`PYTHONUTF8=1 quick_validate.py` → `Skill is valid!`；同时回归校验既有 `project-ellipal-admin-route-interface-mapping-rules` 亦 PASS。
- **字典刷新**：不适用——`skill-dictionary/generate_dictionary.py` 的 `ROOT` 固定为 `~/.claude/skills`，不扫描项目根 `skills/`。
- **关联记忆**：`arco-column-drag-via-titleslotname`、`arco-table-sortable-needs-sorter-true`、`wsl-vite-unreachable-from-windows`。

## 2026-08-26 创建：project-ellipal-admin-route-interface-mapping-rules（项目本地 skill）

- **来源**：用户主动点名（通道 B）——「为项目新增一个规则，写成项目 skill：前端路由 Path /backend/业务名/index 对应后端同名业务接口 /api/v1/业务名，方便跨端定位」。
- **证据**：迁移脚本 `cmd/migrate/migration/version/` 的 `Path:` 与后端 `app/*/router/*.go` 的 `v1.Group(...)` 全量扫描；exchangePartnerUser 全链路实例（router/apis/service/views/api/迁移脚本 6 处同名）。
- **落点**：`ellipal_admin/skills/project-ellipal-admin-route-interface-mapping-rules/`（SKILL.md + agents/openai.yaml + references/mapping-examples.md）。
- **盘点发现**：12 个管理页同名成立；report 报表域为例外（/api/v1/report/语义路径，不同名）；历史偏差 ucardCard ↔ ucardCards（前端单数/后端复数）等。
- **验证**：`quick_validate.py` PASS。
- **关联既有记忆**：PROJECT_MEMORY「sys_menu 的 path 必须等于 component」「新增业务页面闭环」。

## 2026-08-19 吸收：skill-autosave（外部 skill，已删除源）

- **来源**：本地安装的 `skill-autosave__skillhub`（`~/.workbuddy/skills/`，OpenClaw 生态 skillhub 安装，无版本号，仅 4 文件：SKILL.md、_icon.png、_meta.json、_skillhub_meta.json）。
- **来源形态**：纯指令型 SKILL.md，无 scripts/references；面向 OpenClaw/Linux（`~/.openclaw/skills/`、`clawhub publish`）。
- **吸收动机**：用户希望把「任务收口自动评估经验沉淀」机制用于项目级 skill 沉淀，替代被动触发的旧 project-local-skills-rules。
- **落点**：`project-local-skills-rules`（SKILL.md + 2 新 references + 3 个 references 调整）。
- **吸收确认后源处置**：已删除（junction 物理路径 `D:\谷歌云盘\luode-skills\skill-autosave__skillhub`）。
- **验证**：`quick_validate.py` PASS；8 维独立评分 88.3（基线 55）；三场景语义命中测试符合预期。

## 历史来源

（无）
