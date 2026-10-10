# Windows 宿主侧工作流（agent 在 Windows、项目在 WSL）

> 本 skill 的默认方向是「WSL 内 agent 调 Windows」（win-python / win-ps / win-copy / win-path 等 wrapper）。
> 本文是**反向拓扑**补充：agent（WorkBuddy）运行在 **Windows 宿主**、项目源码在 **WSL**（如 `/home/luode/code/ellipal_admin`）时的编译、启动、调试工作流。2026-08-26 在 go-admin 接入 Apifox 测试全程实测。配方 5 不受此限：只要 agent 在 Windows 宿主经 Bash 工具执行就适用，与项目在哪无关。

## 触发信号

- 编译/启动 WSL 项目时报文件系统错误（典型：`go.mod RLock: Incorrect function`）。
- 本地起服务后 Windows 侧连不上端口（典型：128xx 段）。
- 从 Git Bash 调 PowerShell 被安全策略拦截。
- Windows Python 报找不到脚本/路径（典型：把 `/tmp/...` 当成 `c:\tmp\...`）。
- Bash 工具里的内联脚本：匹配反斜杠的正则静默漏检或报正则语法错误，或 Python 报 `SyntaxError: unterminated string literal`（3.9 及以下为 `EOL while scanning string literal`），见配方 5。

## 核心原则（双路线）

1. 读写、搜索、规则检查、普通 git 盘点：留在 Windows 侧（Git Bash），不强行切 WSL。
2. 编译、运行、启动、测试等执行类动作，二选一：
   - **路线 A（实测可靠）**：把源码同步到 Windows 本地 Temp 副本，用 Windows 侧工具链（go/swag/python/node）执行。绕开 WSL 挂载文件系统的文件锁问题。
   - **路线 B（AGENTS.md 规则）**：`wsl.exe --cd /home/<user>/<project> <command>` 进 WSL 执行。WSL 进程能正常联网、产物面向 Linux 时优先。

## 配方

### 1. Temp 副本工作流（路线 A 前提）

- 触发信号：`go.mod RLock: Incorrect function`——挂载/虚拟文件系统不支持文件锁操作，go 工具链无法在 WSL 挂载视图上直接跑。
- 步骤：
  1. `git archive HEAD` 起底到本地 Temp（或整目录 rsync，排除 `.git`）。
  2. 增量同步工作区**未提交改动**到副本。
  3. 在副本上编译、运行。
- 坑 1（重同步覆盖）：重同步 `config/` 等目录会覆盖副本的本地修改（如端口 18080）→ 端口/验证码等 hack 必须放在「重同步之后、编译之前」。
- 坑 2（陈旧文件）：副本残留陈旧文件会导致重复声明编译失败（如 config 目录 ObsConfig/StatDatabase 双重声明）→ 编译失败先整目录重同步再重试，不要只删单个文件。

### 2. 端口选择

- Windows 128xx 端口段被 svchost 接管（有监听但连不上）→ 本地服务统一用 **18080**。
- go-admin 端口写在 `config/config_local_yaml.go`（编译进二进制）与 `config/yaml/config.local.yaml` 双处；`-c` 参数只识别环境、不读文件。改 yaml 的 `port` 后**必须重编译**。

### 3. 本地联调（go-admin 示例）

- 登录验证码：Login struct 字段全 `binding:"required"`，缺 uuid/code 报 "missing Username or Password or Code"；`captcha.Verify` 无 dev 放行 → 只在 Temp 副本 `common/middleware/handler/auth.go` 改 `if false && !captcha.Verify(...)`，**工作区代码不动**。
- **登录失败 HTTP 恒 200**：jwtauth 默认 Unauthorized 返回 `c.JSON(http.StatusOK, {code,message})` → 自动化断言用 `httpCode=200` + `$.code=400`，不要按 401 期望。

### 4. 跨工具调用

- 从 Bash 调 PowerShell 被安全策略拦截（`powershell -Command ...`）→ 改用独立 PowerShell 入口/工具执行（Stop-Process 等 Windows 专用操作）。
- Windows Python 不认 Git Bash 的 `/tmp` 绝对路径（会解析成 `c:\tmp\...`）→ 传 `C:/Users/...` 风格路径。
- apifox CLI 遥测弹窗与禁用（`APIFOX_CLI_TELEMETRY=0`）：**权威源为 `apifox-cli` skill**（含兼容变量与残留进程清理），本文不重复。

### 5. Bash 工具会把成对反斜杠减半（与项目在哪无关）

- 现象：agent 在 Windows 宿主经 Bash 工具（Git Bash）执行时，命令文本里每两个连续反斜杠在进入 shell 前就被折成一个，单引号和 `<<'EOF'` 都挡不住；单个反斜杠、经文件写入工具（如 Write / Edit）落盘的内容不受影响。匹配「反斜杠或正斜杠」的字符类 `[\\/]` 折成 `[\/]`，只剩正斜杠：文本里有正斜杠时照常命中、退出码为 0，反斜杠路径静默漏检，只有反斜杠时零命中（rg 退出码 1）；写成 `[/\\]` 则折成 `[/\]`，rg 报正则解析错误（退出码 2），Python 抛 `re.error`。Python 里表示一个反斜杠的字面量 `'\\'` 变成未闭合字符串，报 `SyntaxError`。
- 做法：命令文本里不写两个连续反斜杠，按用途选：
  - 原样写正文，或必须保留字面反斜杠的脚本：用文件写入工具写成文件（脚本写完再执行），不经命令文本。
  - 内联 Python：用 `chr(92)` 构造反斜杠，匹配路径前先 `.replace(chr(92), '/')`。
  - 路径：传给 Windows 程序（Python、PowerShell 等）写 `C:/Users/...`；`/d/...` 只作 Git Bash 命令的参数，Windows 程序会把它解析成当前盘根下的 `\d\...`（同配方 4 的 `/tmp`）；确需反斜杠形式时用 `cygpath -w` 在运行时生成。
  - 不要改写成四个反斜杠去凑数，换一种执行方式就会错；扫描类结论要带一个已知命中项作对照组。
- 范围：已在 Claude Code 桌面版 + Git Bash 实测，其他宿主未验证。文件写入工具和 `chr(92)` 不依赖宿主；`cygpath` 只在 Git Bash / MSYS2 / Cygwin 里有，WSL 内对应 `wslpath -w`。本 skill 其他小节（如「免桥直读要点」第 3 步、陷阱清单）推荐的 quoted heredoc，对 Windows 宿主经 Bash 工具执行的命令不成立。案例：知识库 `20-Knowledge/execution-failure-cases/wsl-windows-bridge/20260930-204809-exec-case-bash-tool-halves-double-backslash.md`。

## 边界与交叉引用

- 凭据两套 `$HOME`（WSL 与 Windows 不共享）：见本 skill「Common Scenarios」的 win-path/win-copy 同步流程，本文不重复。
- shell 选择策略：`wsl-shell-reliability`。
- 编码与换行：`windows-encoding-rules`。
- apifox CLI 细节：`apifox-cli`。
- 叙述版经验（发生了什么、环境拓扑、证据）：知识库 `20-Knowledge/开发环境/agent在Windows项目在WSL的编译启动调试经验.md`。

## 环境依赖

| 依赖 | 类型 | 说明 |
| --- | --- | --- |
| `APIFOX_CLI_TELEMETRY=0` | 用户级环境变量 | 仅 apifox 场景；重启宿主后全局生效 |
| 端口 18080 | 本机约定 | 128xx 段不可用时的本地服务端口 |
