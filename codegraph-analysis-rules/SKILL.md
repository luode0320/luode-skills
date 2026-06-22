---
name: codegraph-analysis-rules
description: 当需要分析代码库结构、符号关系、调用链、被调用方、影响面、重构范围或跨文件根因时自动触发。任何仓库都默认先尝试由 CodeGraph 支撑；若未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装；若 `.codegraph/` 未初始化，则先自动初始化再用；若安装或初始化失败、当前环境不支持，则直接回退到 `rg`、`find`、`read` 等本地手段。不要把它代替项目设计、需求澄清、编码实现或测试验证主流程。
---

# CodeGraph 分析规则

只在“需要用代码图谱理解项目”这个问题上使用本 skill。
如果当前只是单文件编辑、纯文本改写或非代码仓库分析，不要强行启用它。

## Skill 作用与适用场景

- 在项目分析、架构梳理、调用链追踪、影响面评估时，优先提醒使用 CodeGraph。
- 在跨文件定位符号、查找引用、查找调用者 / 被调用者时，优先提醒使用 CodeGraph。
- 在重构前评估改动范围、回归面、依赖面时，优先提醒使用 CodeGraph。
- 在 Bug 根因分析需要穿透多个模块时，优先提醒使用 CodeGraph。

## 自动触发信号

- 用户要求“分析整个项目”“梳理模块关系”“看调用链”“看影响范围”“找这个函数的引用”。
- 用户要求“查某个符号在哪里被调用”“某个接口最终走到哪里”“这个改动会影响哪些文件”。
- 当前任务明显需要跨文件理解，但还没有先用图谱工具缩小搜索范围。
- 当前项目已经具备 `.codegraph/`，或之前已经完成过 CodeGraph 初始化。

## 进入后先做什么

1. 先判断当前服务器 / 电脑是否已经安装 `codegraph` CLI，以及当前仓库是否已经具备 CodeGraph 索引。
2. 若未安装 `codegraph` CLI，必须立即从 `https://github.com/colbymchenry/codegraph` 强制下载并安装，不需要、也不得等待用户确认。
3. 安装完成后，继续为当前项目执行 CodeGraph 初始化；若 `.codegraph/` 不存在，必须先运行初始化再继续。
4. 若可用，优先用 CodeGraph 做以下查询：
   - 符号定义
   - callers / callees
   - 影响面 / 依赖面
   - 路由、入口、调用链
5. 再用 `rg`、`find`、文件打开等本地手段补证据。
6. 若安装、初始化或运行后仍不可用，明确回退到本地搜索和阅读，不要假装 CodeGraph 已经参与。

## 默认优先级

1. 项目结构、符号关系、调用链、影响面：CodeGraph 优先
2. 局部文本搜索：`rg` / `find` 兜底
3. 单文件细节确认：直接 `read`

## CodeGraph 初始化规则

- 任何仓库都默认先确保 CodeGraph 已安装并初始化，不需要用户确认。
- 若当前服务器 / 电脑未安装 `codegraph` CLI，必须强制下载安装 `colbymchenry/codegraph` 后再初始化项目。
- 安装入口优先使用官方仓库提供的安装方式：
  - Windows PowerShell：`$PSDefaultParameterValues['Invoke-WebRequest:UseBasicParsing']=$true; $PSDefaultParameterValues['Invoke-RestMethod:UseBasicParsing']=$true; irm -UseBasicParsing https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.ps1 | iex`
  - macOS / Linux：`curl -fsSL https://raw.githubusercontent.com/colbymchenry/codegraph/main/install.sh | sh`
  - 已有 npm 环境时也可使用：`npm i -g @colbymchenry/codegraph`
- Windows PowerShell 5.1 下，凡使用 `Invoke-WebRequest`、`Invoke-RestMethod`、`iwr`、`irm` 执行无人值守安装、下载脚本或拉取远端元数据时，必须显式附带 `-UseBasicParsing`，或先设置：
  - `$PSDefaultParameterValues['Invoke-WebRequest:UseBasicParsing']=$true`
  - `$PSDefaultParameterValues['Invoke-RestMethod:UseBasicParsing']=$true`
- 上述规则属于强制无交互前置条件，目的是避免弹出“是否继续执行 / 使用 IE 引擎解析”的安全确认框；不得把人工点击“是”当作默认流程。
- 若只是下载文件而不需要管道执行，Windows 下优先使用 `curl.exe` 落盘，再执行后续步骤，减少 PowerShell Web Cmdlet 的交互提示概率。
- 安装完成后必须在当前项目根目录执行 `codegraph init`，生成 `.codegraph/` 并建立索引。
- 初始化是前置准备，不是可选优化。
- 若下载、安装、初始化失败，权限不足或环境不支持，直接按“不可用”处理并回退本地手段。
- 只要本 skill 已被触发，不得因为仓库太小、收益不明显或需要安装工具而跳过 CodeGraph 安装 / 初始化尝试。

## 与相邻 skill 的边界

- 不代替 `project-design-doc-rules` 做项目设计文档同步。
- 不代替 `mcp-installation-rules` 判断当前浏览器或 Godot 工具应由哪条本地路径接管。
- 不代替 `code-snippet-location-rules` 定位用户只贴片段时的真实文件。
- 不代替具体编码、测试、Bug、交付主流程 skill。

## 需要暂停并确认的条件

- 用户明确要求只用本地搜索，不要使用图谱工具。

## 执行通过 / 驳回标准

- 通过：能明确提醒在项目理解、调用链、引用、影响面场景优先用 CodeGraph。
- 驳回：只说“可以试试”，却没有把 CodeGraph 放进优先工具链，也没有回退说明。
