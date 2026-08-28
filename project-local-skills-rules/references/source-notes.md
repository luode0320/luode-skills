# 来源记录

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
