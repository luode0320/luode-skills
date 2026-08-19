# 来源记录

## 2026-08-19 吸收：skill-autosave（外部 skill，已删除源）

- **来源**：本地安装的 `skill-autosave__skillhub`（`~/.workbuddy/skills/`，OpenClaw 生态 skillhub 安装，无版本号，仅 4 文件：SKILL.md、_icon.png、_meta.json、_skillhub_meta.json）。
- **来源形态**：纯指令型 SKILL.md，无 scripts/references；面向 OpenClaw/Linux（`~/.openclaw/skills/`、`clawhub publish`）。
- **吸收动机**：用户希望把「任务收口自动评估经验沉淀」机制用于项目级 skill 沉淀，替代被动触发的旧 project-local-skills-rules。
- **落点**：`project-local-skills-rules`（SKILL.md + 2 新 references + 3 个 references 调整）。
- **吸收确认后源处置**：已删除（junction 物理路径 `D:\谷歌云盘\luode-skills\skill-autosave__skillhub`）。
- **验证**：`quick_validate.py` PASS；8 维独立评分 88.3（基线 55）；三场景语义命中测试符合预期。

## 历史来源

（无）
