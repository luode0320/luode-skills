# source-notes

## 2026-08-26 内部调整

- 来源：内部调整 `wsl-windows-bridge`，诉求「把 agent 在 Windows、项目在 WSL 的编译启动调试经验吸收进 skill」（用户 2026-08-26 15:03 指令）。
- 素材：知识库笔记 `20-Knowledge/开发环境/agent在Windows项目在WSL的编译启动调试经验.md`（同日沉淀，go-admin 接入 Apifox 实测）。
- 落点：SKILL.md 新增「Windows 宿主侧工作流」节 + description 补反向拓扑触发词 + frontmatter 合规化（compatibility→metadata）；新建 `references/windows-host-side-workflow.md`。
- 同域收敛：apifox 遥测条目收敛至 `apifox-cli` skill 单一权威。

## 2026-10-08 执行中 gap 回补

- 来源：执行中 gap 回补 `wsl-windows-bridge`，诉求「agent 在 Windows 宿主经 Bash 工具执行时，成对反斜杠在进 shell 前被减半、quoted heredoc 挡不住，反向拓扑缺这条提醒和替代写法」（用户 2026-10-08 指令）。
- 素材：知识库执行案例 `20-Knowledge/execution-failure-cases/wsl-windows-bridge/20260930-204809-exec-case-bash-tool-halves-double-backslash.md`（candidate，occurrences 3，2026-09-30 实测）。
- 落点：`references/windows-host-side-workflow.md` 新增配方 5 与触发信号 1 条，引言补一句配方 5 的适用范围；SKILL.md「免桥直读要点」第 3 步后加拓扑限定指针，「Windows 宿主侧工作流」主题列表补 1 项；description 与 `##` 标题未改。独立评分后的修正见本 skill 的 `workbuddy-absorption-map.md`。
- 同域收敛：完整规则只写在配方 5（单一权威），SKILL.md 只留指针；陷阱清单不改，由配方 5「范围」条说明 quoted heredoc 对 Windows 宿主经 Bash 工具执行的命令不成立。
