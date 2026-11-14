# 来源记录（source-notes）

按时间追加。每次吸收外部 skill / 文档 / 开源项目流程时记一行，说明做了什么、改写了什么，避免后续重复吸收或误以为原样搬运。

| 日期 | 来源 | 主题 | 做了什么 |
|---|---|---|---|
| 2026-11-14 | `novel-writing-ai-skill-pack-20`（20 张设计卡，含 NovelClaw / bibisco / dramatica-flow / SillyTavern / ink / twinejs / KoboldAI-Client / Sigil+pandoc+typst 等上游） | 长篇记忆分层、人物弧光与工具人判据、伏笔三点制、声线压力测试、互动叙事、成稿转档 | 逐卡对照本地现状裁决：8 张卡合并为 6 条真增量，12 张卡保留现状，2 类模板填充拒绝。新建 `references/11-互动叙事.md`、`references/12-成稿转档与交付.md`；改写 `references/02a-bible-guide.md`、`references/04-正文技法.md`、`templates/character-card.md`、`templates/plot-board.md`；`SKILL.md` 增补 2 条路由与 1 个记忆分层小节。完整裁决表见 `references/SOURCES.md` 第七节与 `workbuddy-absorption-map.md` |

## 改写说明

- **未搬运原文**：所有条目按本地术语与文件结构重写，判据用本地口径（如硬事实/软倾向/临时计划对应 bible 四件套与章纲草稿区），不保留上游卡的 4 步工作流与输出模板。
- **未落盘模板填充**：20 张卡逐字相同的 3 条边界声明与 description 中重复的「时使用。」均不承接；本地创作立场统一由 `references/10-content-safety.md` 表述。
- **三卡合一**：ink / twinejs / KoboldAI-Client 三张互动叙事卡合并为一份 reference，避免三份重复解释「分支」「选择」「状态」。
- **环境依赖降级**：pandoc / typst / Sigil 在本机实测缺失，`12-成稿转档与交付.md` 将其列为可选依赖，核心交付物仍是 Markdown 整合稿。
