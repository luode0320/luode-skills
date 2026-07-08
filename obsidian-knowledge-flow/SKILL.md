---
name: obsidian-knowledge-flow
description: 将固定根目录的 Obsidian vault 作为 Codex 会话知识库管理，并在仓库任务中采用“选择性默认”触发：每轮先轻量判断 `Obsidian:<检索/沉淀/不适用/阻断>`，只有问题依赖历史决策、项目事实、用户偏好、重复实体、知识库内容或“上次/之前/我们约定/当时怎么说”等历史信息时，才通过 Obsidian CLI 检索相关笔记；会话总结、阶段收口或最终回复前，只有存在可复用的事实、决策、流程、定义、偏好、来源或调试经验时，才通过 Obsidian CLI 捕获/沉淀为 Markdown 笔记。适用于 Obsidian、vault、Markdown 知识库、第二大脑、知识图谱、自动会话笔记、知识提取、快速回忆、本地笔记库、知识库检索、会话总结沉淀和 CLI 笔记操作场景。
---

# Obsidian 知识流

## 目标

用本 skill 把一个 Obsidian vault 变成固定根目录、CLI 驱动、本地优先、可自生长的会话知识库。它围绕三条循环工作：

- `retrieve`: 在会话开始、上下文恢复或回答依赖历史知识的问题前，先从 vault 检索相关笔记。
- `capture`: 在会话总结或阶段收口时，把有复用价值的会话信息保存为 Markdown 笔记。
- `distill`: 把会话中的稳定事实、决策、流程、定义和偏好沉淀为长期知识。

默认使用官方 Obsidian CLI 操作 vault。CLI 不可用、Obsidian 应用无法启动、目标 vault 未注册或命令无法限定到解析出的 vault 根目录时，必须阻断；不得退回到直接文件系统读写笔记来伪装成功。

## 选择性默认判定

仓库任务默认先做轻量判断，但不默认调用 CLI。判断结果必须归入以下四类：

- `不适用`: 当前问题不依赖历史知识、知识库内容、长期用户偏好或重复实体，本轮也没有值得未来复用的事实、决策、流程、定义、来源或调试经验；记录判断即可，不调用 Obsidian CLI。
- `检索`: 当前问题依赖历史决策、项目事实、用户偏好、重复实体、知识库内容，或出现“上次”“之前”“我们约定”“当时怎么说”“Obsidian 里”“知识库里”等信号；必须通过 Obsidian CLI 检索并读取匹配笔记后再引用。
- `沉淀`: 会话总结、阶段收口或最终回复前，确认本轮形成可复用事实、决策、流程、定义、偏好、来源、调试经验或规则口径；必须先通过 Obsidian CLI 检索现有承接笔记，再决定创建、追加或沉淀。
- `阻断`: 本应检索或沉淀，但 Obsidian CLI 不可用、目标 vault 未注册、根目录不一致、命令无法限定到目标 vault，或读写命令失败；必须说明阻断原因，不得直接读写 vault 文件作为替代。

路径已经固定到 `D:\obsidian_data` + `知识库/` 之后，判断过程只负责决定是否需要检索、沉淀或阻断，不再把 root probing、环境变量回查或候选 vault 比较当成独立步骤。

## 固定根目录

本 skill 只认一个固定的 Obsidian 入口：

- Windows 固定根目录：`D:\obsidian_data`
- 真实知识工作区：`D:\obsidian_data\知识库\`

不要再通过 `OBSIDIAN_KB_ROOT`、`OBSIDIAN_VAULT_ROOT`、`.obsidian-kb-root` 或其它候选路径重新推导根目录。固定映射一旦已知，后续所有检索、捕获和沉淀都直接以这个 vault 和 `知识库/` 目录为准。

所有笔记读写都必须限制在 `D:\obsidian_data` 这个 vault 内，并优先落到 `知识库/`。禁止通过符号链接、相对路径 `..`、复制来的绝对路径或 CLI 当前活跃 vault 写出该范围。若 CLI 不能对这一固定 vault 执行命令，直接判定为 `阻断`，不要继续猜测其他路径。

## 工作流程

1. 先判断当前阶段和 Obsidian 状态：
   - 判定为 `检索` 时，回答前先走 `retrieve`。
   - 判定为 `沉淀` 时，阶段收口或最终回复前走 `capture` 或 `distill`。
   - 判定为 `不适用` 时，只记录判断，不读取 vault、不写笔记。
   - 判定为 `阻断` 时，输出 CLI / vault 阻断事实和恢复动作，不使用文件系统 fallback。
2. 直接使用固定映射 `D:\obsidian_data` + `知识库/`，并按场景读取参考文件：
   - 决定目录落点时读 [vault-layout.md](references/vault-layout.md)。
   - 使用 Obsidian CLI 前读 [cli-operations.md](references/cli-operations.md)。
   - 决定笔记字段、组件和双链规则时读 [note-schema.md](references/note-schema.md)。
   - 执行捕获、检索、沉淀流程时读 [capture-retrieve-distill.md](references/capture-retrieve-distill.md)。
   - 处理冲突、过期笔记或敏感信息时读 [conflict-staleness.md](references/conflict-staleness.md)。
   - 做行为验证时读 [validation-checklist.md](references/validation-checklist.md)。
3. 写入前必须先通过 CLI 检索。优先更新或链接现有笔记，避免创建重复笔记。
4. 保护用户手写内容。只做窄范围编辑，保持 frontmatter 合法，不批量重写无关段落。
5. 写入长期笔记后，补齐必要的 backlinks、MOC 和 `知识库/INDEX.md` 入口，让 Obsidian 知识图谱和 CLI 检索都能找到新知识。

## 捕获规则

- 只有未来检索确实有价值时，才把原始会话上下文写入 `知识库/10-Sessions/`。
- 稳定事实、决策、流程、定义、偏好和可复用模式沉淀到 `知识库/20-Knowledge/`。
- 人、项目、仓库、工具、术语、产品、组织和反复出现的概念，创建或更新 `知识库/40-Entities/` 笔记。
- 只有多个相关笔记已经形成主题网络，或明显能提升检索效率时，才创建或更新 `知识库/30-MOCs/`。
- 不确定材料放入 `知识库/00-Inbox/`，不要把未确认内容伪装成长期知识。
- 不捕获纯闲聊、临时过程话术、未确认猜测、一次性中间草稿或对未来没有检索价值的信息。
- 除非用户明确要求且内容已脱敏或限定访问范围，否则不要捕获 secret、API key、密码、私有 token 或凭据。

## 检索规则

- 用别名、标签、wikilink、实体名、来源名，以及可能的中英文变体扩展检索词。
- 按顺序检索：`知识库/INDEX.md` 与 `知识库/30-MOCs/`、精确标题与别名、标签、backlinks、全文。
- 回答前通过 CLI 读取最强匹配笔记。本轮没有实际读过的笔记，不得声称其中有某个 vault 事实。
- 回答依赖检索结果时，引用本地笔记路径作为证据。
- `stale`、`deprecated`、`retired`、`conflicted` 状态的笔记只能作为谨慎上下文，不作为当前启用事实。

## 命令行约定

- 默认使用 `obsidian` CLI 的 `search`、`search:context`、`read`、`create`、`append`、`open` 等命令操作 vault。
- CLI 版本、安装启用、目标 vault、阻断条件和命令模板统一见 [cli-operations.md](references/cli-operations.md)。
- 不使用 `rg`、`Get-Content`、`Set-Content` 等文件系统读写作为正常笔记操作 fallback；这些工具只可用于验证 skill 文件自身、检查仓库 diff 或处理非 vault 资产。
- 后续若增加确定性辅助脚本，统一放在本 skill 的 `scripts/` 目录下，并先在样例 vault 上验证后再依赖。
