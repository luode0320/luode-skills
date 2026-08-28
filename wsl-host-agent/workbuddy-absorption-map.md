# wsl-host-agent 吸收裁决表（workbuddy-absorption-map）

> 归属 owner：`wsl-host-agent`。本表登记该 skill 的历次吸收/内部更新裁决，保证可追溯。

## 2026-08-26 内部更新通道：Windows agent + WSL 项目经验固化

- 来源：内部调整（自有实测经验）。知识库笔记《agent在Windows项目在WSL的编译启动调试经验.md》路线 B 部分 + 2026-08-26 会话实测（EllipalFinance-go 三接口 URL 改名 → apifox 云端同步 → 真实测试全链路）。
- 通道：**内部更新通道**（无外部 skill 原文；来源 = 知识库笔记 + 实测）。
- 落点：新建自建 skill `wsl-host-agent`（唯一可行路径：7 枚 WSL 相关 skill 全为第三方 skillhub、SkillManage 不可修改，现有 skill 明显承接不住 → 命中裁决矩阵「合并落点选择」例外条款）。
- 环境依赖登记：4 项（wsl.exe + WSL2 发行版 / MSYS_NO_PATHCONV 前缀 / Windows go 与 WSL go 工具链分工 / 符号链接拓扑），已在 SKILL.md「环境自检」小节附带自检能力。

| 来源条目 | 本地现状 | 裁决 | 落点 / 理由 | 整理去重 |
| --- | --- | --- | --- | --- |
| 符号链接拓扑可进空间（编辑走 Windows、构建回 WSL） | 7 枚第三方 WSL skill 无此内容；知识库笔记路线 B 已沉淀 | 合并 | SKILL.md「核心原则」+「前置检查」 | N/A（新 skill 无存量可整；净增即本 skill 本体） |
| Windows go 对 `\\wsl.localhost` RLock 失败 → WSL 工具链编译模板 | 第三方 `wsl-windows-bridge` 仅有 Temp 副本路线（RLock 同一根因但解法不同） | 合并 | SKILL.md「编译模板」+ command-templates.md §1 | 与 wsl-windows-bridge 的 RLock 描述不重复：本 skill 是符号链接路线，模板含 MSYS 前缀 + 滤 NUL，属域专属补充 |
| 起服务姿势（先 cd /c/、nohup 不可靠、后台任务前台持有） | 无覆盖 | 合并 | SKILL.md「起服务模板」+ command-templates.md §2 | N/A |
| 探活/停服（POST 探活、ss 按端口找 pid、MSYS 吃引号） | 无覆盖 | 合并 | SKILL.md「停服模板」+「坑位速查」+ command-templates.md §3/§5 | N/A |
| Windows 无扩展名 shim 子进程 PATH 坑（node cli.js 直启） | 无覆盖 | 合并 | SKILL.md「坑位速查」+ command-templates.md §4 | N/A |
| 路线 A（Temp 副本 + Windows 工具链） | 第三方 `wsl-windows-bridge/references/windows-host-side-workflow.md` 已覆盖 | 保留本地 | 不复制；SKILL.md「边界」引用第三方 skill 即可 | N/A |

- 拒绝条目：无（来源为自有经验，无外部形态冲突）。
- 净增体积：SKILL.md ~6.2KB + references/command-templates.md ~3.5KB + 本表 + source-notes.md；无同域重复段落复制（路线 A 全文保留在第三方 skill 与知识库笔记，未复制）。
- 同域冗余扫描结论：见 SKILL.md 收口说明与当日工作日志（范围 7 枚第三方 WSL skill + 知识库笔记；发现 0 处可清理冗余；PASS）。

## 历史裁决

（暂无）
