# AGENTS.md

> Codex 使用 `AGENTS.md`，Claude Code 使用 `CLAUDE.md`，内容规则相同。

## 适用范围

- 本文件适用于本仓库下所有代码与文档变更。

## Skill 强制自动触发规则（最高优先级）

- **所有 skill 的触发不依赖用户主动通知**，AI 必须基于任务内容、工作目录、用户意图主动检测并触发
- 每轮处理用户消息时，必须主动扫描所有可用 skill 的触发条件，符合条件的 skill 必须被调用
- `skill-hit-check-rules` 每轮必须作为第一个 tool call 被调用，无例外
- 禁止以下理由跳过应触发的 skill：
  - “用户没有明确说需要这个 skill”
  - “任务看起来简单，不需要 skill”
  - “我已经知道怎么做了”
  - “这不是核心 skill”
- 违反本规则视为流程违规，必须立即停止当前执行，回到命中检查重走

## Skill 命中强制规则

- 处理本仓库任务时，必须先命中并加载至少两个基础 skill。
- 最低要求：至少命中 `skill-hit-check-rules`、`parallel-task-dispatch-rules`。
- 若本轮涉及创建、补齐或更新仓库级规则文件（`AGENTS.md` / `CLAUDE.md`），默认额外启用 `project-agents-bootstrap` 进行自举补齐；该规则同样适用于其他项目仓库。
- 对已经存在的规则文件，也必须继续做增量同步与受管章节 upsert，而不是只初始化一次。
- 必须在首条中间进度明确输出当前命中的 skill 列表。
- 若命中 `parallel-task-dispatch-rules`，中间进度必须额外输出当前并行技能列表；若最终未并行，明确写 `并行技能:无`。
- 若连 `skill-hit-check-rules` 或 `parallel-task-dispatch-rules` 任一都未命中，视为上下文丢失严重、当前基础规则没有正确加载；此时禁止直接进入主任务，必须先补做 skill 命中检查与上下文重同步。
- 若本轮任务存在多 skill 组合、并行拆分或规则收口风险，默认应额外启用 `skill-audit-rules` 进行只读审计。
- 所有审查类 skill 统一按强制自动触发处理；只要是只读检查、规则核对、实现自审、归位审查或回归风险审查，默认优先并行。

## 上下文压缩续做规则

- 若当前会话刚发生”压缩上下文 / 自动压缩上下文 / 上下文太多”后的重组，默认强制命中 `context-compression-rules`。
- 压缩后继续执行前，必须重新读取当前项目根目录规则文件（`AGENTS.md` / `CLAUDE.md`），恢复仓库级硬规则、必命中 skill 和阻断条件。
- 若压缩后未重新读取规则文件，禁止直接进入任何需求、Bug、编码、测试或交付主任务。
- 若压缩后发现规则文件缺失、损坏或规则不完整，必须先触发 `project-agents-bootstrap` 补齐，再继续主任务。

## 注释任务强制流程

- 触发词：补充注释 / 注意中文编码 / 只补注释 / 注释完善 / 加注释。
- 第一步：先声明命中的注释类 skill。
- 第二步：读取对应 `SKILL.md` 后再改代码。
- 第三步：最终回复给执行证据：改动点、UTF-8、格式化/编译/测试结果。

## 中文编码规则

- 新增或修改注释默认使用中文。
- 文件编码保持 UTF-8，禁止乱码。

## 变更最小化

- 注释补充不改变业务逻辑。

## Windows / WSL 执行规则

> 详细规则见 `windows-wsl-execution-rules` skill。

**操作类型分工：**

| 操作类型 | 执行环境 |
|---------|---------|
| 看代码、改代码（读写文件、搜索、列目录） | Git Bash |
| git 提交、拉取、status / diff / log | Git Bash |
| 编译 `go build` | **必须 WSL** |
| 运行 `go run` / 启动服务 | **必须 WSL** |
| 测试 `go test` | **必须 WSL** |
| 调试 `dlv` | **必须 WSL** |
| 依赖 `go mod download` / `tidy` | **必须 WSL** |

**WSL 执行两条硬约束：**
- Windows 无法运行项目二进制文件，编译产物只能在 WSL 内执行
- 只有 WSL 进程可正常进行网络通信，PowerShell / Git Bash 受网络策略限制

**WSL 执行命令格式：**`wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && <COMMAND>"`

**启动/调试前必须检查 bind mount：**
- 检查：`wsl.exe -e bash -lc "mountpoint -q /home/luode/d/luode/<project> && echo 'mounted' || echo 'not_mounted'"`
- 未挂载：`wsl.exe -e bash -lc "mkdir -p /home/luode/d/luode/<project> && sudo mount --bind /mnt/d/luode/<project> /home/luode/d/luode/<project>"`
- sudo 需要 root 密码时停止，通知用户手动完成后回复再继续

**路径三层结构（执行时使用）：**
- Windows 源码：`D:\luode\<project>`（编辑，Git Bash 直接访问）
- WSL 自动挂载：`/mnt/d/luode/<project>`（桥梁）
- WSL 用户工作路径：`/home/luode/d/luode/<project>`（执行命令）

**编码约束：**
- 仓库提交 `.gitattributes` 与 `.editorconfig`，固定 UTF-8 和换行策略
- `.gitattributes` 默认 `* text=auto`，`*.sh`/`*.yaml` 显式 `eol=lf`
- 不对 `*.go`、`*.vue`、`*.md` 等全量强制 `eol=lf`
- 出现大量无关改动优先检查 `core.autocrlf`；`.sh` filemode 伪改动优先关闭 `core.filemode`

## CodeGraph 强制准备规则

- 若当前服务器 / 电脑未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载并安装，不需要用户确认。
- 若在 Windows PowerShell 5.1 下执行安装，必须默认启用 `Invoke-WebRequest` / `Invoke-RestMethod` 的 `UseBasicParsing`，不得把人工点击确认当作标准流程。
- 安装完成后必须为当前项目执行 `codegraph init`，生成 `.codegraph/` 并建立索引。
- 若下载、安装或初始化失败，明确记录不可用并回退到本地搜索与文件读取。
