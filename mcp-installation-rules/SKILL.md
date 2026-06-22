---
name: mcp-installation-rules
description: 当用户要求分析项目、检查当前项目是否还需要保留浏览器或 Godot MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定使用哪条本地 CLI 路径时自动触发。兼容“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”“Godot MCP”等旧称呼，但默认结论应收敛为 CLI 优先：浏览器使用 `agent-browser`，Godot 使用本地 `godot4` / `godot` 等命令行入口；除非用户明确要求保留旧 MCP 方案，否则不再推荐安装、补齐或优先使用 MCP。
---

# CLI 接管判定规则（兼容旧 MCP 命名）

只在“当前项目后续浏览器 / Godot 工具链应由谁接管”这个问题上使用本 skill。
如果当前只是单纯做前端实现、浏览器自动化执行或 Godot 代码修改，不要让本 skill 代替对应主域 skill。

## Skill 作用与适用场景

- 在整项目分析、环境准备或工具选型阶段，先判断当前项目应走哪条本地 CLI 路径。
- 识别前端项目标记，并要求优先接入 `agent-browser`。
- 对“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”等旧说法做统一收口，避免继续把历史叫法当成当前默认路线。
- 识别 Godot 项目标记，并要求优先接入本地 `godot4` / `godot` 命令行入口或项目自带启动脚本。
- 当一个项目同时包含前端与 Godot 子项目时，允许两类 CLI 工具链同时成为推荐接管项。
- 为后续浏览器控制和 Godot 编辑器控制建立清晰的优先级，避免同类工具抢主导权。
- 若仓库里已经存在旧 MCP 配置，只做兼容性识别和风险提示，不再默认补齐、扩写或推广它们。

## 自动触发信号

- 用户明确说“检查项目是否需要安装 MCP”“看下这个项目要不要保留 MCP”“帮我判断浏览器或 Godot 现在该用哪个工具”。
- 用户明确提到“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”“浏览器 MCP”“Godot MCP”之类旧说法，希望统一规则或决定后续接管方式。
- 用户要求先分析项目，再决定浏览器、前端验证或 Godot 编辑器要由什么工具接管。
- 当前任务即将涉及前端页面验证、浏览器联动测试、真实页面交互，但仓库中尚未明确 CLI 接管策略。
- 当前任务即将涉及 Godot 编辑器联动、场景编辑、运行项目、抓取编辑器状态，但仓库中尚未明确本地命令行接管策略。

## 进入后先做什么

1. 先读 `references/project-signals.md`，按项目结构判断是否存在前端或 Godot 标记。
2. 再读 `references/tool-priority.md`，确认“谁负责接管”与“回退关系”。
3. 再读 `references/config-bootstrap.md`，确认本轮是否只需读取旧配置、还是根本不应该再补项目级 MCP 配置。
4. 只有在需要给出当前推荐入口时，再读 `references/current-sources.md`。
5. 输出结论时必须明确三件事：
   - 是否命中前端项目标记
   - 是否命中 Godot 项目标记
   - 对应 CLI 工具链的接管结论、旧 MCP 名称归一结果与后续执行优先级

## 默认执行流程

1. 扫描仓库根目录和常见子目录，识别前端标记与 Godot 标记。
2. 若命中前端标记：
   - 若用户使用了“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”等叫法，先解释这是历史称呼，当前默认改走 `agent-browser`
   - 结论写为“不需要新装或补齐浏览器 MCP，后续浏览器控制改由 `agent-browser` CLI 接管”
   - 后续浏览器控制优先级写为“`agent-browser` > 其他本地浏览器兜底方式”
3. 若命中 Godot 标记：
   - 结论写为“不需要新装或补齐 Godot MCP，后续 Godot 编辑器 / 运行控制改由本地 `godot4` / `godot` 或项目自带启动脚本接管”
   - 后续 Godot 控制优先级写为“Godot CLI / 编辑器命令行 > 静态文件读取与人工兜底方式”
4. 若两类标记都命中：
   - 结论写为“两类 CLI 工具链都需要准备”
   - 浏览器相关工作由 `agent-browser` 主导
   - Godot 编辑器相关工作由本地 Godot CLI 主导
5. 若两类标记都未命中：
   - 明确写“当前没有足够证据要求保留浏览器或 Godot MCP，也没有发现必须接管的对应 CLI 场景”
   - 不得机械推荐安装旧 MCP
6. 若仓库中已存在旧 MCP 配置：
   - 可以保留现状，不自动删除
   - 但不得再默认扩写、补齐或把它提升回首选路线
7. 若用户明确要求继续保留旧 MCP：
   - 明确说明这属于历史兼容方案，而不是当前默认推荐
   - 仅在用户确认必须兼容旧链路时，才允许继续围绕旧 MCP 做说明

## 浏览器与 Godot CLI 接管结论模板

- `浏览器工具结论：默认使用 agent-browser CLI，不再推荐安装或补齐浏览器 MCP`
- `Godot 工具结论：默认使用本地 Godot CLI / 编辑器命令行，不再推荐安装或补齐 Godot MCP`
- `后续浏览器控制优先级：agent-browser > 其他本地浏览器兜底方式`
- `后续 Godot 控制优先级：Godot CLI / 编辑器命令行 > 静态文件读取与人工兜底方式`
- `如仓库中仍保留旧 MCP 配置，按历史兼容处理，不作为新的默认接管方案`

## 默认优先级

- 浏览器控制：
  - `agent-browser`
  - 其他本地浏览器兜底方式
- Godot 编辑器控制：
  - `godot4` / `godot` / 项目自带启动脚本
  - 其他静态读取或人工兜底方式

## 与相邻 skill 的边界

- 不代替 `project-design-doc-rules` 做整项目总览同步。
- 不代替 `godot-project-bootstrap-rules` 做 Godot 项目的规则文件（`AGENTS.md` / `CLAUDE.md`）模板补齐、图像配置模板补齐或环境就绪收口；本 skill 只负责旧 MCP 命名兼容与当前 CLI 接管判定。
- 不代替 `agent-browser` 做实际浏览器自动化执行；它只负责确认浏览器任务应让位给 `agent-browser`。
- 不代替 `find-skills` 做开放生态技能搜索；这里只判断当前项目应由哪条本地工具链接管。
- 不代替具体的前端 skill 或 Godot 项目实现规则。

## 需要暂停并确认的条件

- 仓库同时存在大量混合技术栈，但无法判断前端或 Godot 是否为真实主项目。
- 用户明确要求继续维护旧 MCP 方案，并希望把它保留为默认路线。
- 当前只能发现可疑文件名，缺少足够项目结构证据支撑接管结论。

## 执行通过 / 驳回标准

- 通过：能明确指出项目是否命中前端 / Godot 标记，以及后续浏览器 / Godot 编辑器应由哪条 CLI 路径优先接管。
- 通过：能明确指出用户口中的 MCP 说法是否只是历史别名，并明确不再默认推荐安装、补齐或优先使用 MCP。
- 驳回：只泛泛建议“可以考虑装 MCP”，却没有项目证据、没有 CLI 优先级、没有旧路线退场说明。

## references 读取规则

- 默认先读 `references/project-signals.md`。
- 只有在判断优先级和回退关系时，再读 `references/tool-priority.md`。
- 只有在判断是否需要读取旧项目级配置、以及为什么不再默认补齐 MCP 配置时，再读 `references/config-bootstrap.md`。
- 只有在需要给出当前推荐入口时，再读 `references/current-sources.md`。
