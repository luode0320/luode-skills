# Obsidian CLI 执行失败案例库

本文件保存 bridge、官方 Obsidian CLI、vault 路径、超时和读写失败的脱敏经验，归属 `obsidian-knowledge-flow`。vault 笔记正文和用户敏感内容不得复制到这里。

本文件是仓库内的静态规则种子和验证基线，不承载动态执行案例正文。命令、编码、JSON、路径、工具契约等新失败经过同输入 local 复验后，必须按 [execution-case-notes.md](execution-case-notes.md) 追加到固定 vault；不得把静态 casebook 作为 vault 写入失败时的 fallback。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`。
- 先通过 bridge doctor 检查版本、注册和固定 vault 根目录；bridge 阻断时不得用文件系统读写伪装成功。
- candidate 自动写入仅保留错误特征、根因、恢复动作和验证证据。
- 每个案例必须绑定至少一个 `TEST-OBS-*`；自动恢复只允许 bridge 已定义的一次有限策略，禁止以“再试几次”替代明确上限。

## OBSIDIAN-CLI-001

- 状态：`active`
- 类型：bridge 前置依赖
- 错误特征：bridge doctor 返回 `CLI_NOT_FOUND`、`OBSIDIAN_APP_UNAVAILABLE`、`WSL_INTEROP_UNAVAILABLE` 或 `POWERSHELL_UNAVAILABLE`
- 根因：官方 CLI 未安装/未启用、应用不可用，或 WSL 无法调用 Windows transport
- 解决方案：安装/启用官方 CLI，确认 bridge doctor；WSL 先恢复 interop/PowerShell，再检查固定 vault 注册；失败时阻断，不使用文件系统 fallback
- 验证：doctor 返回 `ok=true`、`verified=true` 与固定 vault selector
- 来源：`obsidian-knowledge-flow/references/cli-operations.md`
- 最后验证：2026-07-12

## OBSIDIAN-CLI-003

- 状态：`active`
- 类型：WSL transport
- 错误特征：bridge 返回 `WSL_INTEROP_UNAVAILABLE` 或 `POWERSHELL_UNAVAILABLE`
- 根因：WSL 无法调用 Windows PowerShell/进程，不是 WSL 缺少原生 `obsidian`
- 解决方案：恢复 WSL interop 或允许的 PowerShell 后重跑 bridge doctor；不得安装第二套 Linux CLI
- 验证：TEST-OBS-003/007，WSL doctor 返回 `ok=true`、`verified=true`

## OBSIDIAN-CLI-004

- 状态：`active`
- 类型：应用恢复
- 错误特征：bridge 返回 `OBSIDIAN_APP_UNAVAILABLE`
- 根因：官方 CLI 无法连接已关闭或未完成启动的 Obsidian 应用
- 解决方案：bridge 仅隐藏启动一次、最长等待 15 秒并有限重试；不杀用户已有进程，仍失败即阻断
- 验证：TEST-OBS-006，成功响应包含 `started_app=true` 和 `verified=true`

## OBSIDIAN-CLI-005

- 状态：`active`
- 类型：路径与读回
- 错误特征：`PATH_OUTSIDE_KNOWLEDGE`、`READBACK_MISMATCH` 或超时
- 根因：path 不以 `知识库/` 开头、正文超长未分块，或写入未能读回
- 解决方案：只传 bridge allowlist path，UTF-8 正文由 bridge/adapter 分块；每次 create/append 必须 `verified=true`
- 验证：TEST-OBS-004/008/010/013

## OBSIDIAN-CLI-006

- 状态：`active`
- 类型：vault selector
- 错误特征：`VAULT_NOT_REGISTERED`、`VAULT_ROOT_AMBIGUOUS` 或 `LEGACY_NESTED_VAULT_MODEL`
- 根因：固定 root 未注册/不唯一，或把 `知识库/` 错当 vault root
- 解决方案：只用 bridge doctor 动态唯一解析 `D:\obsidian_data`；目标 path 固定以 `知识库/` 开头
- 验证：TEST-OBS-011/014

## OBSIDIAN-CLI-002

- 状态：`active`
- 类型：vault 路径
- 错误特征：bridge 返回 `VAULT_NOT_REGISTERED`、`VAULT_ROOT_AMBIGUOUS`、`LEGACY_NESTED_VAULT_MODEL` 或 `PATH_OUTSIDE_KNOWLEDGE`
- 根因：固定 `D:\obsidian_data` 未注册/不唯一、误把 `知识库/` 当作 vault root，或目标路径越界
- 解决方案：用 bridge doctor 动态唯一解析 selector；保持 vault root 为 `D:\obsidian_data`，只传以 `知识库/` 开头的相对 path，不传 `vault=<name>`
- 验证：bridge `search` 与 `read` 均返回 `ok=true`、`verified=true`，路径未越界
- 来源：`obsidian-knowledge-flow/SKILL.md`、`references/cli-operations.md`
- 最后验证：2026-07-12

## OBSIDIAN-CLI-007

- 状态：`active`
- 类型：规则资产漂移
- 错误特征：references 出现直接 CLI transport、硬编码 vault selector、filesystem fallback、无 readback 证据或未声明重试上限
- 根因：规则文档与 bridge 契约不同步，执行模型可能绕过唯一 root、Windows/WSL interop 或有限恢复边界
- 解决方案：对五份 reference 运行禁止词与 TEST 映射扫描；所有操作模板只指向 bridge，并显式写出 selector、interop、readback、自动启动和重试上限
- 验证：TEST-OBS-016；扫描无硬编码知识库 selector、直接版本/注册列表子命令或文件系统 vault fallback，且每项能力均有 TEST 映射
