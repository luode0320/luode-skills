# Obsidian CLI 执行失败案例库

本文件保存 Obsidian CLI 版本、注册、vault 路径、超时和读写失败的脱敏经验，归属 `obsidian-knowledge-flow`。vault 笔记正文和用户敏感内容不得复制到这里。

## 统一维护规则

- 状态使用 `candidate`、`active`、`stale`、`superseded`、`rejected`。
- 先通过 CLI 检查版本、注册和固定 vault 根目录；CLI 阻断时不得用文件系统读写伪装成功。
- candidate 自动写入仅保留错误特征、根因、恢复动作和验证证据。

## OBSIDIAN-CLI-001

- 状态：`active`
- 类型：CLI 前置依赖
- 错误特征：`obsidian` 命令不存在、版本检查失败或应用无法启动
- 根因：官方 CLI 未安装、未注册或 Obsidian 应用不可用
- 解决方案：安装/启用官方 CLI，确认 `obsidian version`，再检查 vault 注册；失败时阻断，不使用文件系统 fallback
- 验证：版本命令成功，目标 vault 可被 CLI 限定并可读
- 来源：`obsidian-knowledge-flow/references/cli-operations.md`
- 最后验证：2026-07-12

## OBSIDIAN-CLI-002

- 状态：`active`
- 类型：vault 路径
- 错误特征：命令落到错误 active vault 或 `知识库/` 相对路径不可读
- 根因：未使用固定 `D:\obsidian_data` / `知识库` 映射或 vault 参数位置错误
- 解决方案：先执行 `obsidian vaults verbose`，确认固定 vault 根目录，再使用 `vault=知识库` 和 vault 内相对路径
- 验证：`search` 与 `read` 均命中目标笔记且路径未越界
- 来源：`obsidian-knowledge-flow/SKILL.md`、`references/cli-operations.md`
- 最后验证：2026-07-12
