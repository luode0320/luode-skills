# 来源记录

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
