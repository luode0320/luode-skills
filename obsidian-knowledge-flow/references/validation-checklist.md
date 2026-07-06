# 验证清单

创建、更新或前向测试本 skill 时使用这份清单。

## Skill 资产验证

- `SKILL.md` 的 YAML frontmatter 只包含 `name` 和 `description`。
- `description` 覆盖会话开始检索、总结阶段捕获/沉淀、Obsidian、vault、Markdown 知识库、CLI、本地笔记库和知识库检索等触发场景。
- `SKILL.md` 直接链接所有 references，references 只保持一层深度。
- `agents/openai.yaml` 字符串均已加引号，且 `default_prompt` 提到 `$obsidian-knowledge-flow`。
- 不新增 README、安装指南、changelog 或无关辅助文档。

## CLI 前置验证

在样例 vault 功能测试前先验证：

1. `obsidian` 不在 PATH：
   - 预期：阻断，并说明需要安装/升级 Obsidian 1.12.7+ installer、启用 Command line interface、注册 CLI。
2. `obsidian version` 失败：
   - 预期：阻断，不继续读写 vault。
3. 默认根目录不存在：
   - Windows 预期默认 `D:\obsidian_data`；WSL/Linux 预期默认 `/usr/local/src/obsidian_data`。
   - 预期：自动创建默认目录；若 CLI 不认识该 vault，阻断并提示用户在 Obsidian 中打开/注册一次。
4. 环境变量或 `.obsidian-kb-root` 指向的自定义目录不存在：
   - 预期：阻断，不自动创建自定义目录。
5. CLI active vault 与解析出的根目录不一致：
   - 预期：阻断，不使用 active vault 代替目标 vault。

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
   - 预期：稳定事实被提升；不确定事实留在会话笔记或 `00-Inbox/`。
4. 冲突：
   - 输入：一条新笔记与旧的活跃笔记矛盾，且没有权威证据。
   - 预期：笔记标记为 `conflicted`，同时保留两种说法。
5. 敏感数据：
   - 输入：会话包含 API key。
   - 预期：不保存原值；只产生脱敏占位或不产出笔记。
6. 可读组件：
   - 输入：一段长期流程或决策对比。
   - 预期：笔记正文可使用表格、列表、Obsidian callout 或 Mermaid；仍保持纯 Markdown 可读。

## 仓库验证

在 skill 仓库中修改本 skill 后：

- 对 skill 目录运行 skill creator 校验器。
- 当 `description` 或 `##` 标题变化时，运行仓库 skill 字典生成脚本。
- 检查 `git diff`，确认生成的字典文件由脚本刷新，不是手工修改。
