# workbuddy-absorption-map

本文件登记 `wsl-windows-bridge` 的吸收/调整裁决历史（外部吸收 + 内部更新）。

## 2026-08-26 内部更新：Windows 宿主侧工作流吸收

| 来源 | 条目 | 本地现状 | 裁决 | 落点 | 整理去重 |
| --- | --- | --- | --- | --- | --- |
| 知识库 `开发环境/agent在Windows项目在WSL的编译启动调试经验.md`（2026-08-26 实测沉淀） | 双路线原则（读写留 Windows / 执行进 WSL 或 Temp 副本） | AGENTS.md 内联 + wsl-shell-reliability 仅覆盖 shell 选择 | 合并 | SKILL.md「Windows 宿主侧工作流」节 + `references/windows-host-side-workflow.md` | N/A（新 reference，无存量可清） |
| 同上 | go.mod RLock → Temp 副本；重同步覆盖坑；陈旧文件坑 | 无 | 合并 | 同上（配方 1） | N/A |
| 同上 | 128xx 端口段被 svchost 接管 → 18080 | 无 | 合并 | 同上（配方 2） | N/A |
| 同上 | 验证码 dev 放行、登录失败 HTTP 恒 200 | 无 | 合并 | 同上（配方 3） | N/A |
| 同上 | Bash 调 PowerShell 拦截、Windows Python /tmp 路径坑 | 无 | 合并 | 同上（配方 4） | N/A |
| 同上 | apifox 遥测弹窗 | `apifox-cli` SKILL.md 61-77 行已详细覆盖 | 保留本地（本地更强） | 引用 `apifox-cli` | **收敛 1 处**：reference 初稿含重复细节 → 改为「权威源引用」，删除重复段落 |
| 同上 | 两套 $HOME 凭据不共享 | 本 skill Common Scenarios 已有 win-path/win-copy 流程 | 保留本地 | 交叉引用，不复制 | N/A |
| 同上 | 空间不支持 WSL/UNC、回复路径口径 | 用户级 MEMORY + AGENTS.md 已有 | 保留本地 | 未写入 | N/A |

- 环境依赖登记：`APIFOX_CLI_TELEMETRY=0`（用户级环境变量，详见 apifox-cli）、端口 18080（本机约定）。reference 附「环境依赖」表。
- 同域冗余扫描：范围 = wsl-windows-bridge / wsl-shell-reliability / windows-encoding-rules / apifox-cli / wsl-powershell / wsl-path-converter。发现 1 处重复（apifox 遥测，与 apifox-cli 61-77 行），已收敛为引用；无门控层叠；无散落产物；引用链可达。**PASS**。
- 结构校验：`quick_validate.py` 基线报 `compatibility` 违规键 → 本次一并合规化（移入 metadata）→ 修改后 `Skill is valid!` EXIT=0。
- 净增体积：+1 reference（约 3.2KB）+ SKILL.md +1 节/-1 行 frontmatter 调整。
