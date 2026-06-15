---
name: mcp-installation-rules
description: 当用户要求分析项目、检查当前项目是否需要安装 MCP、判断浏览器或 Godot 编辑器应优先由哪个工具接管，或任务即将涉及前端页面验证、浏览器联动、Godot 编辑器操控且需要先根据项目结构决定是否安装 Chrome DevTools MCP 或 Godot AI MCP 时自动触发。对“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”统一按官方当前名称 `Chrome DevTools MCP` 处理。负责识别前端项目与 Godot 项目标记，给出 MCP 安装结论、优先级、Codex 配置补齐规则和后续工具让路规则；若已具备对应 MCP，应优先使用它们控制浏览器或 Godot 编辑器，再在缺失或不可用时回退到其他本地工具。
---

# MCP 安装判定规则

只在“当前项目需不需要安装 MCP，以及后续浏览器 / Godot 编辑器由谁优先接管”这个问题上使用本 skill。
如果当前只是单纯做前端实现、浏览器自动化执行或 Godot 代码修改，不要让本 skill 代替对应主域 skill。

## Skill 作用与适用场景

- 在整项目分析、环境准备或工具选型阶段，先判断当前项目是否需要补装 MCP。
- 识别前端项目标记，并要求优先接入 Chrome DevTools MCP。
- 对“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”等浏览器 MCP 说法做统一收口，避免同一工具被误当成多个候选。
- 识别 Godot 项目标记，并要求优先接入 Godot AI MCP。
- 当一个项目同时包含前端与 Godot 子项目时，允许两个 MCP 同时成为推荐安装项。
- 覆盖 Codex 本地配置缺口：若项目级 `./codex/config.toml` 或 `./.codex/config.toml` 缺少目标 MCP 配置，默认补齐而不是只停留在口头建议。
- 为后续浏览器控制和 Godot 编辑器控制建立清晰的优先级，避免同类工具抢主导权。

## 自动触发信号

- 用户明确说“检查项目是否需要安装 MCP”“看下这个项目要不要装 MCP”“帮我判断该装哪个 MCP”。
- 用户明确提到“谷歌浏览器 MCP”“Google Chrome MCP”“Chrome MCP”“Chrome DevTools for agents”“浏览器 MCP”之类说法，希望接入或统一浏览器侧 MCP 规则。
- 用户要求先分析项目，再决定浏览器、前端验证或 Godot 编辑器要由什么工具接管。
- 当前任务即将涉及前端页面验证、浏览器联动测试、真实页面交互，但仓库中尚未明确 MCP 接管策略。
- 当前任务即将涉及 Godot 编辑器联动、场景编辑、运行项目、抓取编辑器状态，但仓库中尚未明确 MCP 接管策略。

## 进入后先做什么

1. 先读 `references/project-signals.md`，按项目结构判断是否存在前端或 Godot 标记。
2. 再读 `references/tool-priority.md`，确认“需要安装什么”与“后续谁优先执行”的映射关系。
3. 再读 `references/config-bootstrap.md`，确认 `./codex/config.toml` / `./.codex/config.toml` 的检查顺序与默认补齐动作。
4. 只有在需要给出当前可参考安装来源时，再读 `references/current-sources.md`。
4. 输出结论时必须明确三件事：
   - 是否命中前端项目标记
   - 是否命中 Godot 项目标记
   - 对应 MCP 的安装建议、配置补齐结论、别名归一结果与后续执行优先级

## 默认执行流程

1. 扫描仓库根目录和常见子目录，识别前端标记与 Godot 标记。
2. 若命中前端标记：
   - 若用户使用了“谷歌浏览器 MCP / Google Chrome MCP / Chrome MCP / Chrome DevTools for agents”等叫法，先统一解释为官方当前名称 `Chrome DevTools MCP`
   - 结论写为“需要安装 Chrome DevTools MCP”
   - 检查项目级 `./codex/config.toml` 与 `./.codex/config.toml`；若目标配置不存在，则默认补齐对应 MCP 配置
   - 后续浏览器控制优先级写为“Chrome DevTools MCP > 其他浏览器工具”
   - 若同时命中网页验证、页面调试、网络分析、性能诊断场景，要求优先让位给 Chrome DevTools MCP
3. 若命中 Godot 标记：
   - 结论写为“需要安装 Godot AI MCP”
   - 检查项目级 `./codex/config.toml` 与 `./.codex/config.toml`；若目标配置不存在，则默认补齐对应 MCP 配置
   - 后续 Godot 编辑器控制优先级写为“Godot AI MCP > 其他本地兜底方式”
   - 若同时命中场景编辑、节点调整、运行项目、抓取编辑器状态场景，要求优先让位给 Godot AI MCP
4. 若两类标记都命中：
   - 结论写为“两类 MCP 都需要安装”
   - 浏览器相关工作由 Chrome DevTools MCP 主导
   - Godot 编辑器相关工作由 Godot AI MCP 主导
   - 若项目级 Codex 配置缺失任一 MCP，对缺失项默认补齐
5. 若两类标记都未命中：
   - 明确写“当前没有足够证据要求安装这两个 MCP”
   - 不得机械推荐安装
6. 若已确认需要某个 MCP 且项目级 Codex 配置缺失：
   - 默认补齐 `./codex/config.toml` 或 `./.codex/config.toml` 中对应 MCP 配置；两者都不存在时按 `references/config-bootstrap.md` 约定创建项目级配置文件
   - 不需要、也不得等待用户额外确认
7. 若已确认需要某个 MCP 但当前环境尚未安装或配置补齐后仍不可用：
   - 先阻断对应工具类执行
   - 提醒先按该 MCP 的当前官方或项目主页说明完成安装，不要沿用过期博客或第三方转述里的旧命名、旧参数
   - 安装完成后再回到对应主域 skill

## 默认优先级

- 浏览器控制：
  - `Chrome DevTools MCP`
  - `agent-browser`
  - 其他本地浏览器兜底方式
- Godot 编辑器控制：
  - `Godot AI MCP`
  - 其他 Godot 本地兜底方式（如仅运行命令、静态读文件、人工编辑）

## 与相邻 skill 的边界

- 不代替 `project-design-doc-rules` 做整项目总览同步。
- 不代替 `agent-browser` 做实际浏览器自动化执行；它只负责在需要时让位给更高优先级的 Chrome DevTools MCP。
- 不代替 `find-skills` 做开放生态技能搜索；这里只判断当前项目应安装什么 MCP。
- 不代替具体的前端 skill 或 Godot 项目实现规则。

## 需要暂停并确认的条件

- 仓库同时存在大量混合技术栈，但无法判断前端或 Godot 是否为真实主项目。
- 用户明确要求不要安装任何外部 MCP。
- 当前只能发现可疑文件名，缺少足够项目结构证据支撑安装结论。

## 执行通过 / 驳回标准

- 通过：能明确指出项目是否命中前端 / Godot 标记、需要安装哪个 MCP，以及后续浏览器 / Godot 编辑器该由谁优先接管。
- 通过：能明确指出项目是否命中前端 / Godot 标记、需要安装哪个 MCP、项目级 Codex 配置是否已补齐，以及后续浏览器 / Godot 编辑器该由谁优先接管。
- 驳回：只泛泛建议“可以考虑装 MCP”，却没有项目证据、没有优先级、没有回退策略。

## references 读取规则

- 默认先读 `references/project-signals.md`。
- 只有在判断优先级和回退关系时，再读 `references/tool-priority.md`。
- 只有在判断 `./codex/config.toml` / `./.codex/config.toml` 是否缺失、该补齐哪类 MCP 配置以及如何落盘时，再读 `references/config-bootstrap.md`。
- 只有在需要给出当前推荐来源或安装入口时，再读 `references/current-sources.md`。
