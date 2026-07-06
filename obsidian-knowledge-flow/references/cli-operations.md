# Obsidian CLI 操作规则

本 skill 默认使用官方 Obsidian CLI 操作 vault。依据官方帮助文档，CLI 需要 Obsidian 1.12.7+ installer，在 Obsidian 设置中启用 Command line interface，并依赖 Obsidian 应用运行；首个命令可以启动 Obsidian，但如果应用无法启动或 CLI 未注册，必须阻断。

参考来源：https://obsidian.md/help/cli

## 必需前置

执行任何 vault 读写前，先完成以下检查：

1. `obsidian` 命令存在于当前 PATH。
2. `obsidian version` 可执行并返回版本信息。
3. Obsidian CLI 已在 Obsidian 设置中启用并注册。
4. 目标 vault 根目录已解析并通过 [vault-layout.md](vault-layout.md) 的根目录校验。
5. CLI 命令能限定到解析出的目标 vault。优先在 vault 根目录作为当前工作目录执行；如果 CLI 使用其他 active vault，必须阻断。

任何一项失败都视为 CLI 硬依赖不满足。不要回退到 `rg`、`Get-Content`、`Set-Content`、Python 或 Node 直接读写 vault Markdown 文件。

## Vault 定位

- 如果当前 shell 的工作目录就是目标 vault 根目录，Obsidian CLI 默认应使用该 vault。
- 如果使用 `vault=<name>` 或 `vault=<id>`，该参数必须放在命令第一个参数位置。
- 使用 `obsidian vaults verbose` 或等价命令确认 CLI 认识的 vault 与解析出的根目录一致。
- 如果默认根目录刚创建但 CLI 还不认识它，停止并提示用户在 Obsidian 中打开/注册该目录一次。

## 常用命令模板

以下命令按当前 shell 调整引号和转义。多行内容使用 `\n` 表达换行。

```bash
obsidian version
obsidian vaults verbose
obsidian search query="关键词" limit=10 format=json
obsidian search:context query="关键词" limit=10
obsidian read path="20-Knowledge/topic/note.md"
obsidian create path="10-Sessions/2026/07/session-title.md" content="# 标题\n\n正文"
obsidian append path="20-Knowledge/topic/note.md" content="\n## 2026-07-06 更新\n\n- 新证据"
obsidian open path="20-Knowledge/topic/note.md"
```

## 读写约束

- 创建或更新笔记前必须先 `search` 或 `search:context` 检索现有笔记。
- 读取内容必须使用 `obsidian read` 或等价 CLI 命令。
- 新建笔记使用 `obsidian create`；若目标已存在，不得盲目 `overwrite`。
- 追加证据优先使用 `obsidian append`；只有必须重排 frontmatter 或替换冲突内容时，才允许选择更精确的 CLI 更新方式。
- 打开笔记可使用 `obsidian open`；它只负责呈现，不作为读取证据。
- 所有 `path=` 都必须是 vault 根目录内的相对路径。

## 阻断文案要点

CLI 阻断时，说明必须包含：

- 失败的前置项：命令不存在、版本/注册失败、应用无法运行、vault 未注册、目标路径不一致或命令执行失败。
- 目标 vault 根目录。
- 用户可执行的恢复动作：安装/升级 Obsidian 1.12.7+ installer，在设置中启用 Command line interface，把默认目录作为 vault 打开/注册，重新运行命令。

阻断时不要写入任何笔记，也不要把直接文件读写结果当成 vault 事实。
