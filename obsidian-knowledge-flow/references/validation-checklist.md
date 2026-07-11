# 验证清单

创建、更新或前向测试本 skill 时使用这份清单。

## Skill 资产验证

- `SKILL.md` 的 YAML frontmatter 只包含 `name` 和 `description`。
- `description` 覆盖选择性默认判断、固定根目录 `D:\obsidian_data`、`知识库/` 工作区、会话开始检索、总结阶段捕获/沉淀、Obsidian、vault、Markdown 知识库、CLI、本地笔记库和知识库检索等触发场景。
- `SKILL.md` 直接链接所有 references，references 只保持一层深度。
- `agents/openai.yaml` 字符串均已加引号，且 `default_prompt` 提到 `$obsidian-knowledge-flow`。
- 不新增 README、安装指南、changelog 或无关辅助文档。

## 选择性默认验证

0. 项目本地四件套启动：
   - 输入：临时项目目录缺少 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`。
   - 预期：先创建三个 UTF-8 文件，读取 current 后读取 memory；普通启动不读取 history。
   - 追加场景：已有 history 内容时重复初始化不得覆盖；current 超过 51,200 字节时阻断。

1. 普通仓库任务：
   - 输入：一次不依赖历史知识、也没有可复用沉淀价值的普通文档或实现任务。
   - 预期：输出 `Obsidian:不适用`，不调用 `obsidian` CLI，不读取 vault。
2. 历史知识问题：
   - 输入：用户询问“上次怎么定的”“之前 Obsidian 里有没有记录”。
   - 预期：输出 `Obsidian:检索`，通过 `obsidian search` / `search:context` 检索，并用 `obsidian read` 读取匹配笔记。
3. 收口沉淀：
   - 输入：阶段收口时形成可复用规则、流程、事实或调试经验。
   - 预期：输出 `Obsidian:沉淀`，先通过 CLI 检索已有承接笔记，再决定 `create` 或 `append`。
4. CLI / vault 不可用：
   - 输入：本应检索或沉淀，但 `obsidian version` 失败、vault 未注册或根目录不一致。
   - 预期：输出 `Obsidian:阻断`，说明恢复动作，不用直接文件系统读写作为 fallback。

## CLI 前置验证

在样例 vault 功能测试前先验证：

1. `obsidian` 不在 PATH：
   - 预期：阻断，并说明需要安装/升级 Obsidian 1.12.7+ installer、启用 Command line interface、注册 CLI。
   - 如果已定位到官方 installer 自带的 `Obsidian.com` 绝对路径，预期：允许把该路径作为 CLI 命令继续前置校验，并在证据中记录。
2. `obsidian version` 失败：
   - 预期：阻断，不继续读写 vault。
3. 默认根目录不存在：
   - Windows 预期固定 `D:\obsidian_data`。
   - 预期：自动创建该固定目录；若 CLI 不认识该 vault，阻断并提示用户在 Obsidian 中打开/注册一次。
4. `D:\obsidian_data` 下的 `知识库/` 目录不存在：
   - 预期：只允许在固定根目录内补齐，不得改用其它路径。
5. CLI active vault 与固定根目录不一致：
   - 预期：阻断，不使用 active vault 代替目标 vault。
6. CLI 返回 `unable to find Obsidian` 或命令超时：
   - 预期：有限等待或重启 Obsidian 后重试前置校验；仍失败则阻断，不进行目标 vault 写入。
7. CLI 命令参数被误拼接，例如 `vault=知识库 vault info=path`：
   - 预期：判定为非法命令模板，改用 `vaults verbose` 或明确的 `vault=<name>` 首参命令。
8. 误用写入命令查帮助，例如 `create help`：
   - 预期：判定为风险命令，改用只读 help 入口。
9. 长 `content=` 参数、多行表格或 Mermaid append：
   - 预期：拆成小块追加，并在最终读回校验中确认内容完整。
10. 长任务后出现挂起的 Obsidian CLI 进程：
   - 预期：记录并清理本轮挂起进程，重新执行 `version` 和 `vaults verbose` 证明 CLI 恢复。

## 样例 Vault 功能测试

创建或使用一次性本地样例 vault 做验证。不要直接在生产 vault 上测试。

1. 会话开始检索：
   - 输入：用户用别名询问之前的决策。
   - 预期：通过 CLI 扩展别名检索，读取匹配笔记，并引用笔记路径。
2. 总结阶段捕获：
   - 输入：一段会话包含一个稳定决策、一个来源链接和一个反复出现的项目实体。
   - 预期：通过 CLI 创建或更新一篇会话笔记、一篇知识笔记、一篇来源笔记和一篇实体笔记，并补齐 backlinks。
3. 沉淀：
   - 输入：一篇会话笔记同时包含稳定事实和不确定事实。
   - 预期：稳定事实被提升；不确定事实留在会话笔记或 `知识库/00-Inbox/`。
4. 冲突：
   - 输入：一条新笔记与旧的活跃笔记矛盾，且没有权威证据。
   - 预期：笔记标记为 `conflicted`，同时保留两种说法。
5. 敏感数据：
   - 输入：会话包含 API key。
   - 预期：不保存原值；只产生脱敏占位或不产出笔记。
6. 可读组件：
   - 输入：一段长期流程或决策对比。
   - 预期：笔记正文可使用表格、列表、Obsidian callout 或 Mermaid；仍保持纯 Markdown 可读。
7. 全量 vault 沉淀：
   - 输入：一个已由 CLI 注册的源 vault 和一个已注册的目标 vault。
   - 预期：先统计源 Markdown 总数；每个顶层分类生成逐篇沉淀笔记；全量总览汇总所有批次；逐篇表格数据行数等于来源 Markdown 数；总和等于源总数；敏感主题只保存脱敏后的通用线索。

## 仓库验证

在 skill 仓库中修改本 skill 后：

- 对 skill 目录运行 skill creator 校验器。
- 当 `description` 或 `##` 标题变化时，运行仓库 skill 字典生成脚本。
- 检查 `git diff`，确认生成的字典文件由脚本刷新，不是手工修改。
- 同时确认项目本地四件套与 vault 分层：项目 Markdown 使用标准文件工具，vault 检索和沉淀只能使用 Obsidian CLI。
