---
name: windows-wsl-execution-rules
description: 当项目代码位于 WSL 文件系统内（如 `/home/user/project`）、且当前任务发生在 Windows 环境时触发。核心边界：普通仓库命令默认优先使用 Git Bash / bash，只有执行类动作才优先进入 WSL，例如编译、运行/启动程序、测试、调试、会真实启动运行时的依赖安装；看代码、改代码、搜索、读写规则文件、普通 git 操作与多数只读检查默认留在 Git Bash / bash。PowerShell 不作为 Windows 下普通仓库命令入口，只在 `.ps1` 脚本、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用；一旦进入这些 PowerShell 专项场景，还必须遵守本 skill 内吸收自热门社区 skill `powershell-windows` 的保底模式（逻辑运算括号、ASCII-only、null check、Join-Path、ConvertTo-Json -Depth、重定向与编码防护等）。agent 在 WSL 时直接访问代码与执行；agent 在 Windows 时（如 Claude Desktop GUI），普通命令通过 Git Bash / bash 访问 `//wsl.localhost/distro/...` 或等价 Windows 可访问路径，执行类动作再用 `wsl.exe --cd /home/user/project target-command` 进 WSL。无论文件写入发生在 Windows、WSL 还是 Linux，都必须遵守 UTF-8 文件写入规则，禁止 GBK/ANSI/默认编码落盘。回复中需要引用项目内文件路径（Markdown 链接、审查证据路径、截图说明、最终总结里的文件路径等）时同样触发本 skill：这条只看用户查看环境，与 agent 自身运行在 WSL 还是 Windows 无关——只要用户从 Windows 桌面 / GUI 客户端访问、项目代码在 WSL，就必须输出 `\\wsl.localhost\distro\...`，不能因为 agent 本身直接跑在 WSL 内（无需 `wsl.exe` 包裹）就顺手把 `/home/...` 当成用户可打开路径输出。纯 Windows 项目或不需要启动执行的任务，不要误切到 WSL。
---

# Windows / WSL 执行规范（代码在 WSL）

## 适用场景

项目代码放在 WSL 文件系统内（如 `/home/<user>/<project>`），开发在 Windows 环境进行，且需要明确区分“普通命令”和“执行类命令”。

## 核心架构：先看 agent 在哪运行

### 情况一：agent 在 WSL（推荐，最简单）

- 代码在 WSL、agent 在 WSL，本地直接访问
- 直接执行 `go build` / `go test` / `go run` / `dlv`，**无需任何包裹**
- 进程天然在 WSL，联网正常
- **但“面向用户输出的项目内文件引用”不因此改变**：这条规则只看用户查看环境，不看 agent 运行位置；agent 直接跑在 WSL 内不代表可以对着 Windows 桌面用户输出 `/home/...`，判定与格式见下方「路径约定」
- 新会话第一次在这个 WSL 项目里执行命令时，建议顺手跑一次 `command -v rg fd fzf 2>/dev/null`（按项目实际常用工具调整）自检；输出路径落在 `/mnt/` 下说明该工具还是 Windows 版，按 `references/tool-path-interop.md` 提前原生装包，不必等真的报错再排查。这是一次性建议，不是每条命令前都要跑的强制检查

### 情况二：agent 在 Windows（如 Claude Desktop GUI）

- **shell 选择**：普通仓库命令优先使用 Git Bash / bash；PowerShell 不作为普通仓库命令入口，只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用
- **PowerShell 运行时预检**：进入上述专项场景前先检查 `pwsh` 是否存在且主版本至少为 7；优先使用 `pwsh -NoProfile`。缺少 PowerShell 7 时，调用 `windows-powershell-environment-rules` 的环境审计/安装入口；只有升级或安装被权限、网络或包管理器阻断时，才允许使用 `powershell.exe` 5.1 作为兼容回退。
- **Windows Terminal 默认项**：PowerShell 7 的 Windows Terminal 用户级默认 profile 由 `windows-powershell-environment-rules` 负责设置与验证；本 skill 只负责命令路由，不替换系统 `powershell.exe`。
- **看代码、改代码**：通过 `\\wsl.localhost\<distro>\home\<user>\<project>` 访问 WSL 文件
- **普通命令默认不切 WSL**：搜索、读文件、改文件、规则检查、普通 `git status` / `git diff` / `git log` 等，默认留在 Git Bash / bash
- **文件写入仍按 UTF-8**：普通读写留在 Git Bash / bash 时，脚本语言读写必须显式声明 UTF-8；不得因为路径在 WSL 或命令未进 WSL 就依赖 GBK / ANSI / shell 默认编码
- **执行类命令再进 WSL**：编译、运行、启动程序、测试、调试，以及会真实启动运行时的依赖安装，通过 `wsl.exe --cd /home/<user>/<project> <command>` 执行

## PowerShell 专项场景的保底模式

这部分把社区热门 skill `powershell-windows` 的高价值规则吸收到本地，但定位是 **PowerShell 专项兜底**，不是把 PowerShell 重新升格成 Windows 默认仓库 shell。专项运行时默认是 PowerShell 7+ 的 `pwsh`，`powershell.exe` 5.1 只用于明确记录的兼容回退。

### 什么时候才进入 PowerShell

- 运行 `.ps1` 脚本
- 使用 Windows 专用 cmdlet（如 `Get-ItemProperty`、`Get-Service`、`Get-Clipboard`）
- 做 PowerShell profile / 编码初始化
- 用户明确要求 PowerShell

### 进入 PowerShell 后必须遵守的规则

1. 逻辑运算里，每个 cmdlet 调用都单独加括号，例如 `if ((Test-Path "a") -or (Test-Path "b"))`
2. 脚本默认只用 ASCII 状态文本，不在 `.ps1` 和 inline PowerShell 里放 emoji 或花体符号
3. 访问 `.Count`、`.Length`、属性链前先做 null check，不直接假设对象存在
4. 复杂属性链不要直接塞进插值字符串，先落到变量，再输出
5. 拼变量路径优先用 `Join-Path`；带空格的可执行文件路径要加引号，并配合 `&` 调用运算符
6. `ConvertTo-Json` 默认显式带 `-Depth`
7. PowerShell 专项写文件、导日志和重定向时继续遵守 UTF-8 防护，必要时联动 `windows-encoding-rules`

### 运行时选择与 5.1 回退

1. Windows 专项命令先用 `pwsh -NoProfile`，并确认 `$PSVersionTable.PSVersion.Major -ge 7`。
2. 如果 `pwsh` 不存在或版本不满足，先调用 `windows-powershell-environment-rules` 完成审计/安装；环境准备未获授权或执行被阻断时，才允许回退 `powershell.exe -NoProfile`。
3. 在 5.1 回退路径中，`Invoke-WebRequest`、`Invoke-RestMethod`、`iwr`、`irm` 必须显式使用 `-UseBasicParsing`；不得把 5.1 回退写成新的默认入口。

### PowerShell 与主路由的关系

- 如果任务本质只是 `rg` 搜索、读文件、普通 `git status` / `git diff`、规则检查或仓库盘点，**不要因为会写 PowerShell 就切到 PowerShell**
- 如果任务本质是 Linux 运行链路里的编译、测试、调试或启动，**不要因为机器是 Windows 就放弃 WSL 执行**
- PowerShell 在本 skill 里是专项入口，不是普通仓库命令入口；专项入口默认使用 `pwsh`，普通入口仍然是 Git Bash / bash，执行类动作仍然使用 `wsl.exe --cd`

## PowerShell 使用优先级阶梯（硬约束）

本节是全仓库 PowerShell / bash / WSL 选择的**唯一硬约束真源（canonical）**。其它规则文件只做指向与收紧，冲突时以本节为准。四级优先级必须**从上往下逐级判断，停在成立的那一级**：

1. **能用 bash 就不用 PowerShell（普通仓库命令红线）**：凡是搜索、读写文件、规则检查、普通 `git status` / `git diff` / `git log` 盘点等普通仓库命令，只要 Git Bash / bash 能完成，一律用 bash，禁止因为身处 Windows 或顺手就切到 PowerShell。
2. **执行类命令优先进 WSL（不用 PowerShell）**：编译、运行、测试、调试，以及会真实联网启动运行时的依赖安装等执行类命令，优先用 `wsl.exe --cd /home/<user>/<project> <command>` 在 WSL 内执行，同样不落到 PowerShell。
3. **仅 PowerShell 专项场景才允许 PowerShell**：只有运行 `.ps1`、使用 Windows 专用 cmdlet、做 PowerShell profile / 编码初始化、或用户明确要求 PowerShell 时，才允许进入 PowerShell；PowerShell 不是普通仓库命令入口。
4. **进入 PS 专项场景必须优先 PowerShell 7**：专项运行时先用 `pwsh -NoProfile` 并确认 `$PSVersionTable.PSVersion.Major -ge 7`；`powershell.exe` 5.1 仅在 `pwsh` 缺失或版本不足、且升级被权限 / 网络 / 包管理器阻断时才允许回退，回退时必须显式记录阻断原因，禁止把 5.1 写成默认入口。

## 跨环境命令失败恢复与经验沉淀

命令执行前后由 `execution-failure-learning-rules` 路由本 skill 的 `prevent`、`recover`、`learn` 三种模式。这里的命令包括普通仓库命令、执行类命令、JSON/编码处理、测试与验证脚本、`pre-commit` / `post-commit` gate 以及它们的回退检查；这是一条 agent 执行期规则，不表示有后台监控进程。

### 三种模式

1. `prevent`：执行前按 shell、agent 运行侧、工作目录、工具来源和 local 配置匹配 `active` 案例；精确命中时先采用已验证路径。`candidate`、`conflicted`、`stale`、`superseded` 和 `rejected` 不能直接驱动命令。
2. `recover`：失败后先保留脱敏证据并按实际根因分类；同一失败假设最多无变化重试一次，第二次仍失败必须改变 shell、路径、工具来源或输入处理方式之一，再重新诊断。
3. `learn`：恢复成功且同一输入、同一成功标准复验通过后，自动将脱敏候选写入本 skill 案例库的 `candidate`；满足晋级门禁并取得当前任务 skill 维护授权后，才可转为 `active`。

### 失败后的最小闭环

1. 记录失败命令的 shell、agent 运行侧、工作目录、退出码、最小错误文本和是否触及 local 环境；先脱敏路径、用户名、token、连接串和业务数据。
2. 只执行一个能区分根因的窄诊断：例如用 `command -v <tool>` / `type <tool>` 查工具来源，用 `pwd` / `Get-Location` 查工作目录，用 `$LASTEXITCODE` 查原生命令退出码，用原始文本回读定位 JSON 或编码问题。
3. 按根因选择最小替代路径：shell 语法错误回到对应 shell，路径语境错误统一 Windows UNC 或 WSL `/home/...`，工具 interop 问题优先换 WSL 原生工具，JSON 解析问题先分离 stdout/stderr 并保存原文，编码问题改为显式 UTF-8。
4. 修复后使用同一输入和同一成功标准重跑；除退出码外，还要验证输出可解析、产物/差异正确、运行配置仍为 local，避免“命令成功但环境错了”。
5. 只有恢复成功且证据足够时才回写案例库；失败未定位、仅靠猜测、一次性网络抖动或包含敏感原文的案例不得直接写成规则。

### 状态、冲突与授权

- 案例状态统一为 `candidate`、`active`、`conflicted`、`stale`、`superseded`、`rejected`；只有 `active` 可在 `prevent` 中自动执行。
- 新方案与现有 `active` 冲突时，先保留为 `candidate` 并标记 `conflicted`、记录替代关系；新方案完成同输入复验、去重、脱敏、唯一 owner 检查且获得授权后，旧方案才转 `superseded`。无法证明可复用或更优的候选转 `rejected`，历史上仍有价值但不应优先采用的方案转 `stale`。
- `learn` 自动回写仅表示已验证候选，不等于允许改变 `active` 规则；Git 提交、推送和跨项目知识沉淀仍按各自授权边界执行。

### 防止错误恢复失控

- 同一失败假设最多无变化重试一次；第二次仍失败时必须改变 shell、路径、工具来源或输入处理方式之一，并重新诊断。
- 不要把 PowerShell、Git Bash 和 WSL 的路径、重定向、变量语法混写在同一命令上下文；遇到嵌套引号或 JSON 解析异常，优先拆成脚本文件或分步变量，再做机器可读输出。
- 不要因 `permission denied` 直接 `chmod` / `sudo`；先确认 `command -v <tool>` 是否命中 `/mnt/` 下的 Windows 版工具，再判断真实文件权限。
- 不要为了修复当前命令关闭 WSL interop、修改 `/etc/wsl.conf`、切换到 test/prod 或放宽安全边界；这些只能在用户明确要求且风险已说明时处理。
- 案例库写入采用“同根因合并、不同边界分条”；先检索已有案例，避免把同一错误追加成多个互相冲突的答案。

## 什么算执行类命令

- 会产出或启动可执行程序的命令：如 `go build`、`go run`、`npm start`、`pnpm dev`、`python app.py`
- 会真实跑测试或调试器的命令：如 `go test`、`pytest`、`dlv debug`
- 启动程序、测试、调试和联调命令必须使用 local 本地配置、本地数据库和本地服务；不得通过 WSL 启动连接 `test` / `prod` / `staging` 数据库、缓存、消息队列、HTTP/RPC 上游或其他非 local 服务。
- 会依赖 WSL 运行时环境才能正确完成的安装/准备动作：如 `go mod download`、需要 Linux 环境的 `npm install`
- 不启动程序的普通仓库操作 **不算** 执行类命令：如 `rg`、`ls`、`cat`、规则文件检查、文档修改、普通 git 盘点

## 为什么只有执行类动作优先在 WSL

- 只有 WSL 进程才能正常联网（Windows 上启动的进程受网络管控）
- 运行产物与调试链路面向 Linux，执行时需要留在 WSL
- 普通读写、搜索、git 盘点不依赖 Linux 运行时，强行切 WSL 反而容易引入路径、权限和工具解析问题

## 路径约定

代码在 WSL 内，两种访问方式：

| 用途 | 路径形式 |
|------|---------|
| WSL 内执行类动作（agent 在 WSL，或 `wsl.exe --cd`） | `/home/<user>/<project>` |
| Windows 侧普通命令、看代码、改代码（agent 在 Windows） | Git Bash / bash 使用 `//wsl.localhost/<distro>/home/<user>/<project>`；Windows 工具显示使用 `\\wsl.localhost\<distro>\home\<user>\<project>` |
| 面向用户输出的项目内文件引用（与 agent 运行位置无关，只看用户查看环境） | `\\wsl.localhost\<distro>\home\<user>\<project>\<relative-path>` |

- `<distro>` 是 WSL 发行版名，用 `wsl.exe -l -v` 查看。
- 回复用户时，凡引用项目内文件都按用户当前环境可打开的路径输出；项目在 WSL 且用户从 Windows 桌面访问时，Markdown 链接、普通文本路径、审查证据路径、截图说明和最终总结中的项目内文件路径都使用 `\\wsl.localhost\<distro>\...`。
- **这条判定只看“用户查看环境”，不看“agent 运行位置”**：即使 agent 本身直接跑在 WSL 内（上面的情况一，执行不需要任何包裹），只要用户是从 Windows 桌面 / GUI 客户端查看回复，也必须输出 `\\wsl.localhost\...`；不要因为“我自己就在 WSL 里，直接用 `/home/...` 更省事”而跳过转换。
- 只有命令参数、WSL shell 上下文和日志原文保留 `/home/<user>/<project>`。
- **不再使用 `/mnt/<drive>`**——代码不在 Windows 盘。

## 执行环境分工（agent 在 Windows 时）

| 操作类型 | 执行方式 |
|---------|---------|
| 看代码、改代码、读写文件、搜索、规则检查 | Git Bash / bash，经 `//wsl.localhost/...` 或等价 Windows 可访问路径访问 |
| 普通 git 盘点、提交、拉取 | Git Bash / bash（经 `//wsl.localhost/...`），仅在仓库本身要求时再切 WSL |
| 编译 / 运行 / 启动程序 / 测试 / 调试 / 执行类依赖安装 | `wsl.exe --cd /home/<user>/<project> <command>` |

读写文件无论落在哪一层执行，都必须保持 UTF-8；Git Bash / bash 下优先使用脚本或工具的显式 UTF-8 选项，PowerShell 专项写文件时显式带 `-Encoding UTF8`，WSL / Linux 侧不把仓库文本转换为 GBK、ANSI 或其他本地编码。

## 命令模板（agent 在 Windows 时）

默认发行版省略 `-d`；多发行版时用 `wsl.exe -l -v` 查名后加 `-d <发行版名>`：

```bash
# 测试
wsl.exe --cd /home/<user>/<project> go test ./...
# 运行
wsl.exe --cd /home/<user>/<project> go run ./cmd/<app>
# 调试
wsl.exe --cd /home/<user>/<project> dlv debug ./cmd/<app>
# 依赖
wsl.exe --cd /home/<user>/<project> go mod download
```

agent 在 WSL 时直接执行，无需 `wsl.exe`：

```bash
cd /home/<user>/<project> && go test ./...
```

## WSL 内缓存目录建议

代码在 WSL 原生文件系统，I/O 性能好。Go 缓存默认即可，如需显式设置：

```bash
export GOCACHE=$HOME/.cache/go-build
export GOMODCACHE=$HOME/go/pkg/mod
```

## 不推荐做法

- 不要在 Windows 原生 Go 环境跑需联网的项目。
- 不要为了调试或测试方便，把启动参数、环境变量或配置文件切到 `test` / `prod` / `staging` 等非 local 环境；local 不可用时记录为本地环境阻断。
- 不要把“普通仓库命令也能写成 PowerShell”误当成推荐路径；普通搜索、读文件、规则检查和多数 git 盘点仍优先 Git Bash / bash。
- 不要把 WSL 路径（`/home/...`）和 Windows 路径混用在同一命令上下文。
- 不要在面向 Windows 桌面用户的项目内文件引用里输出 `/home/...` 作为可打开路径；这类路径应转换成 `\\wsl.localhost\...`。
- 不要因为 agent 自身运行在 WSL 内（情况一，执行不需要包裹）就认为面向用户的文件引用也可以直接用 `/home/...` 输出；这条规则只看用户查看环境，不看 agent 运行位置。
- 不要在 WSL 内命令（如 `rg`）报 `permission denied` 或行为异常时，直接当成 Linux 权限问题就 `chmod`/`sudo`；先用 `command -v <tool>` 确认路径是否落在 `/mnt/` 下——那意味着解析到了 Windows 版同名工具，详见 `references/tool-path-interop.md`。
- 不要把修改 `/etc/wsl.conf`（如关闭 `appendWindowsPath`）当成默认排查手段；这是影响整个 WSL 发行版的重量级改动，只在用户明确要求时才做。
- 不要把普通搜索、读文件、规则检查这类非执行动作一律切进 WSL。
- agent 在 Windows 时，不要把 PowerShell 当普通仓库命令的默认 shell；只有 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时才使用 PowerShell。
- 不要在 PowerShell 脚本里直接复用 CMD 风格命令，或假设 PowerShell 与 CMD/Bash 重定向完全等价；进入 PowerShell 后按 `references/powershell-fallback-patterns.md` 的模式写。
- 纯 Windows 项目，或本轮根本不会启动/执行程序的任务，不要为了“统一口径”硬套 WSL。
- 不要再用 `/mnt/<drive>`——代码已在 WSL，用 `/home/<user>/...` 与 `\\wsl.localhost\...`。

## 约束总结

**代码在 WSL 时：agent 在 WSL 直接干；agent 在 Windows 时普通仓库命令优先使用 Git Bash / bash，仅在编译、运行、启动程序、测试、调试等执行类动作时再用 `wsl.exe --cd` 进 WSL；PowerShell 只用于 Windows 专项场景。**

**所有代码、文档、配置、脚本、测试资产和生成类文本写入都必须保持 UTF-8；执行环境分层只决定命令在哪一侧运行，不改变文件编码规则。**

## 与其他规则的协作

- 涉及文件写入编码、Windows 中文编码、Git Bash / bash UTF-8 基线、PowerShell 专项 UTF-8 初始化与落盘细节时，联动 `windows-encoding-rules`。
- 涉及仓库长期规则沉淀时，联动 `project-rule-file-bootstrap-rules`，把本规范写入仓库规则文件（`AGENTS.md` / `CLAUDE.md`）。
- 命令执行失败且已完成恢复时，先读并按 `references/command-failure-recovery.md` 回写已验证 `candidate`；只有满足晋级门禁并取得当前任务维护授权时才转 `active`。涉及中文乱码、换行或重定向时同时联动 `windows-encoding-rules`。
- 如果当前任务已经明确进入 PowerShell 专项场景，且出现逻辑运算括号、`Join-Path`、`ConvertTo-Json -Depth`、null check 或 ASCII-only 这类语法/风格坑，优先按本 skill 的 PowerShell 保底模式处理，不再临时口头补规则。

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 需要路径访问细节时读 `references/path-mapping.md`
- 需要团队工作流时读 `references/recommended-workflow.md`
- 需要进入 PowerShell 专项场景时读 `references/powershell-fallback-patterns.md`
- 首次进入 WSL 项目做一次性工具自检、或怀疑命令解析到 Windows 侧同名工具（如报 `permission denied`）时读 `references/tool-path-interop.md`
