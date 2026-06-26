# 插件条目库

每个插件一个条目。安装 / 使用信息一律以官方仓库为准，**不沿用第三方博客 / 公众号转述**。新增插件按下方条目格式追加。

## 条目格式

- 名称 / 官方仓库
- 定位（解决什么问题）
- 支持平台
- 安装（按平台，官方命令）
- 使用 / 配置
- 适用与不适用场景
- 安全边界
- 回退

---

## Ponytail（必装）

- **【默认必装】**：本插件为框架的默认必装插件，会话 / 项目准备时默认安装并启用（强度 `full`），不需要用户额外确认；Claude Code 的 `/plugin` 斜杠命令需提示用户执行。
- **官方仓库**：https://github.com/DietrichGebert/ponytail （MIT，约 58.5k stars）
- **定位**：AI 思维注入器 —— 让 agent 按 YAGNI「懒资深工程师」决策阶梯生成更精简代码，减少过度工程。官方实测：约 -54% 代码行、-22% tokens、-20% 成本、-27% 时间，安全 100% 保持。
- **支持平台**：Claude Code 插件、Codex 插件、GitHub Copilot CLI、Pi / OpenCode / Gemini CLI / Devin CLI；以及 Cursor、Windsurf、Cline、Kiro、VS Code Copilot、Aider 的规则文件。
- **安装（以官方为准）**：
  - Claude Code：`/plugin marketplace add DietrichGebert/ponytail`，然后 `/plugin install ponytail@ponytail`
  - Codex：`codex plugin marketplace add DietrichGebert/ponytail`
  - Devin CLI：`devin plugins install DietrichGebert/ponytail`
  - Pi agent：`pi install git:github.com/DietrichGebert/ponytail`
  - Cursor / Windsurf / Cline / VS Code 等：从仓库对应 `.cursor/rules/`、`.windsurf/rules/` 等复制规则文件
- **使用命令**：
  - `/ponytail [lite|full|ultra|off]`：设置强度（默认 `full`）
  - `/ponytail-review`：检查 diff 中的过度工程
  - `/ponytail-audit`：扫描整个仓库
  - `/ponytail-debt`：跟踪延后的优化
  - `/ponytail-help`：参考指南
- **配置**：可选 `~/.config/ponytail/config.json`，或环境变量 `PONYTAIL_DEFAULT_MODE`（默认 `full`）。
- **决策阶梯**：是否需要存在 → 代码库已有 → 标准库 → 平台原生特性 → 已装依赖 → 一行能否搞定 → 才写最小可行代码。
- **适用**：希望 AI 生成精简代码、减少 review 负担、降低 token 成本；与 `code-minimal-change-rules`、`bug-fix-proposal-rules` 的根因 / 最小改动理念一致。
- **不适用**：生产级金融 / 医疗 / 安全系统的防御性编程、教学样板、有严格代码规范的团队。
- **安全边界**：只砍「为防万一而写的样板代码」，不砍数据校验、访问控制、输入验证等安全代码。
- **回退**：未安装或未激活时，按常规编码流程进行，并可联动 `code-minimal-change-rules` 手动控制代码量。
- **⚠️ 注意**：网上第三方文章给的 `npx ponytail init` / `claude --ponytail` / `npm install -g ponytail` 等命令与官方**不符**，不要使用；一律以官方仓库 README 的 `/plugin marketplace add` 等命令为准。
