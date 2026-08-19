# 吸收裁决登记表

> 单一真相源：每次外部 skill 吸收后在此追加一行，必须含「整理去重」列；来源必须可回指。

| 日期 | 来源（可回指） | 吸收精华 | 裁决 | 落点 | 整理去重 | 已删除源 |
|---|---|---|---|---|---|---|
| 2026-08-19 | `skill-autosave__skillhub`（本地安装，OpenClaw 生态自动沉淀 skill，无版本号，见 `source-notes.md`） | 触发条件（5+ tool call / 错误后解法 / 用户纠正 / 复用 workflow）；价值评估门槛（一次性/拒绝/闲聊→不沉淀）；查重（扫描已有 skill 比较 name+description）；更新流程（补步骤/边缘/过时命令）；质量标准（踩坑经验/命令可复制） | 合并 6 条 / 拒绝 3 条（`~/.openclaw` 路径、clawhub 发布、通用非项目沉淀） | `project-local-skills-rules`：新增 `references/auto-trigger-and-evaluation.md`、`references/dedup-and-update.md`；改造 `SKILL.md`（双通道触发 + 价值门槛 + 查重/创建/更新）；模板补质量标准段 | SKILL.md 旧「自动触发信号」5 条并入双通道（净增 2 references 约 +120 行）；scope-and-splitting 11 主题统一加前缀；project-skill-template 命名建议重写 | ✅ `skill-autosave__skillhub`（junction 物理路径 `D:\谷歌云盘\luode-skills\skill-autosave__skillhub`，2026-08-19 删除） |

## 净增减总结

- 新增：2 个 reference（约 120 行）、2 个登记文件。
- 整理：SKILL.md 旧「自动触发信号」清单并入双通道触发；scope-and-splitting 主题清单整体加前缀；project-skill-template 命名建议段重写为新前缀 + 质量标准。
- 删除：外部源 skill 目录 1 个（4 文件）。
