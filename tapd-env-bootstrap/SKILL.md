---
name: tapd-env-bootstrap
description: 本机 TAPD 凭据环境事实（luode 专用）。当涉及 TAPD OpenAPI 操作、TAPD 环境预检、TAPD_TOKEN 缺失或配置位置疑问、与 tapd-openapi 等技能配合排查"未配置"报错时自动加载。记录本机 TAPD 凭据的真实存放位置与注入机制：~/.tapd/env.sh（Windows 与 WSL 各一份）+ Windows 用户级环境变量注入，取代 tapd-openapi SKILL.md 中"写入 .codex/config.toml"的旧指引。
allowed-tools: Read,Bash
agent_created: true
---

# TAPD 环境引导（本机事实，2026-08-18 建档）

> 本 skill 记录 luode 机器上 TAPD 凭据的真实配置位置与注入机制，用于对齐 tapd-openapi / tapd-addcomment 等技能的环境预检预期。执行任何 TAPD 动作前先按本文件核对环境。

## 本机 TAPD 凭据配置（唯一权威事实）

| 项                  | 位置/值                                                           |
| ------------------- | ----------------------------------------------------------------- |
| 真源文件（Windows） | `C:\Users\luode\.tapd\env.sh`                                     |
| 真源文件（WSL）     | `/home/luode/.tapd/env.sh`（与 Windows 侧内容一致）               |
| 注入层（Windows）   | 用户级环境变量（注册表 User scope），重启应用后自动继承           |
| 注入层（WSL）       | `~/.bashrc` 末尾 `[ -f ~/.tapd/env.sh ] && source ~/.tapd/env.sh` |
| API 端点            | `https://api.tapd.cn`（TAPD_API_ENDPOINT）                        |
| 站点                | `https://www.tapd.cn`（TAPD_SITE_URL）                            |
| 项目 ID             | `62459836,30399328,36150079`（TAPD_WORKSPACE_IDS，已去重）        |

env.sh 内容为 4 个 export：`TAPD_TOKEN` / `TAPD_API_ENDPOINT` / `TAPD_SITE_URL` / `TAPD_WORKSPACE_IDS`。**Token 明文只存在于 env.sh，禁止写入本 skill 或任何对话输出。**

## 关键事实（与 tapd-openapi 文档的差异）

1. **不再使用 `.codex/config.toml` 的 `[shell_environment_policy.set]` 存 TAPD 变量**（2026-08-18 已迁移并清理，0 残留）。若 tapd-openapi SKILL.md 仍指引"打开项目级配置 ./.codex/config.toml"，以本 skill 为准。
2. **WorkBuddy Bash 工具是隔离 shell**：`BASH_ENV` 指向 WorkBuddy 自带 `safe-delete-bash-env.sh`，非交互 `bash -c` 不读 `~/.bashrc`/`~/.bash_profile`。因此 Windows 侧自动注入只依赖"用户级环境变量"，修改后需重启应用才生效；当前会话内可用临时 `export` 应急。
3. **WSL 侧**：交互终端读 `~/.bashrc` 自动加载；非交互 `wsl -e bash -lc` 不会自动加载（Ubuntu 默认 .bashrc 对非交互直接 return），需手动 `source ~/.tapd/env.sh`。
4. `workspace_list` 接口返回空数组属正常现象，排查定位用 `workspace_id` 直查实体接口即可。

## 验证命令

```bash
# Windows（新会话/重启后）
[ -n "$TAPD_TOKEN" ] && echo "OK len=${#TAPD_TOKEN}" || echo "MISSING"

# WSL 交互终端
source ~/.tapd/env.sh && [ -n "$TAPD_TOKEN" ] && echo "OK len=${#TAPD_TOKEN}"

# API 冒烟测试
curl -s -m 15 -H "Authorization: Bearer $TAPD_TOKEN" "$TAPD_API_ENDPOINT/users/info"
```

## 更新凭据流程

1. 编辑 Windows 侧真源 `C:\Users\luode\.tapd\env.sh`
2. 同步到 WSL：`wsl -e bash -lc 'cp /mnt/c/Users/luode/.tapd/env.sh ~/.tapd/env.sh && chmod 600 ~/.tapd/env.sh'`
3. 同步 Windows 用户级环境变量（PowerShell，4 个变量逐一）：
   ```powershell
   [Environment]::SetEnvironmentVariable('TAPD_TOKEN','新值','User')
   ```
4. 重启应用生效，用上述验证命令确认。
