# 合并来源说明

当前 skill 已合并外部种子能力，来源如下：

- 来源仓库：`https://github.com/nextlevelbuilder/ui-ux-pro-max-skill`
- 合并日期：`2026-03-28`
- 当前保留内容：`data/`、`scripts/` 和许可文件 `LICENSE.seed.txt`
- 吸收来源：`https://github.com/anthropics/claude-code`
- 参考路径：`plugins/frontend-design/skills/frontend-design/SKILL.md`
- 参考提交：`2923bc87d10da4fda57570313f2abbc5b457fed1`
- 吸收日期：`2026-03-29`

## 当前保留方式

- 外部大种子的搜索脚本已经并入本 skill
- 原本单独的 `downloaded-seeds/ui-ux-pro-max-skill` 已不再保留
- 正式使用只走 `frontend-ui-visual-rules`
- `anthropics/claude-code` 的 `frontend-design` 未作为独立 seed 长期保留，而是只吸收“审美方向、记忆点、空间张力、动效强度匹配、避免 AI 味模板化”等工作流规则

## 许可说明

- 原项目许可为 MIT
- 原始许可文本已保留在当前 skill 目录的 `LICENSE.seed.txt`
- `anthropics/claude-code` 该 skill 的 frontmatter 标记为 `license: Complete terms in LICENSE.txt`
- 当前上游 skill 目录接口返回仅看到 `SKILL.md`，未看到同目录 `LICENSE.txt`
- 因此这里未直接保留其原文副本，只吸收并改写为中文规则；如果后续需要对外再分发该部分内容，建议再次核查上游许可条款

## 维护建议

- 后续如继续吸收外部数据，优先补到当前 skill 内部，而不是重新造第二个前端视觉种子目录
- 吸收时优先保留能稳定自动触发的规则，不要把大而全的数据量直接等于质量
- 吸收这类前端设计种子时，优先补“决策规则”和“自审标准”，不要简单复制风格词表
