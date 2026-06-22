---
name: windows-wsl-execution-rules
description: 当当前工作目录位于 Windows 盘符路径（如 C:\、D:\、E:\、F:\）时强制生效，无需用户主动提及 WSL。所有项目的启动、调试、测试、构建、安装依赖、运行脚本均必须通过 WSL 执行，禁止在 PowerShell 或 Git Bash 中直接运行项目命令。代码在 Windows 侧编辑，执行环境强制为 WSL，因为 Windows 无法运行项目二进制文件且存在网络限制，只有 WSL 进程才能正常进行网络通信。VSCode 的 launch.json 和 tasks.json 也必须通过 WSL 管道或 dlv 远程调试协议完成调试。不要用它代替具体语言/框架的实现、测试策略、编码规则或 WSL 安装说明。
---

# Windows -> WSL 强制执行规则

本规则在以下环境中**强制生效**，无需用户手动触发：

- 仓库位于 Windows 目录，例如 `D:\luode\project`、`F:\code\app`
- 代码编辑发生在 Windows 侧（Codex 桌面端、VSCode、资源管理器）
- Windows 目录已挂载到 WSL 路径，例如 `D:\luode\project` → `/mnt/d/luode/project`

**强制 WSL 执行的根本原因（两条硬约束）：**

1. **二进制无法在 Windows 运行**：项目编译产物（Go 二进制等）只能在 Linux 环境执行，直接在 PowerShell 中运行会失败
2. **网络限制**：只有 WSL 进程才能正常进行网络通信，PowerShell / Git Bash 中运行的进程受网络策略限制，无法访问内外网资源

## 自动触发信号

满足以下任一条件，本规则**无条件强制介入**：

- 当前工作目录路径含有 Windows 盘符，例如 `C:\`、`D:\`、`E:\`、`F:\`
- 用户提到 `Windows`、`WSL`、`Git Bash`、`Ubuntu`、`Linux 环境`
- 用户说明项目代码位于 Windows 盘符目录
- 当前任务包含：启动、调试、测试、构建、安装依赖、运行脚本、查看运行时错误
- 项目根目录含有 `go.mod`、`package.json`、`Cargo.toml`、`requirements.txt`、`Makefile` 等项目入口文件

## 进入后先做什么

1. 确认当前项目根目录位于 Windows 盘符路径（如 `D:\luode\project`）。
2. 将路径转换为对应的 WSL 挂载路径（如 `/mnt/d/luode/project`）。
3. 所有项目命令**必须**通过 `wsl.exe -e bash -lc "cd '<WSL_PATH>' && <COMMAND>"` 执行。
4. VSCode 调试任务（`tasks.json`）同样通过 `wsl.exe` shell 执行；调试配置（`launch.json`）通过 `dlv` 远程协议连接 WSL 内的调试器。
5. 不存在"先试 PowerShell，失败再换 WSL"的回退逻辑——直接走 WSL，不走回退。

## 团队默认路径约定

团队项目统一放在 `D:\luode\` 下，路径分三层：

| 层级 | 路径 | 说明 |
|------|------|------|
| Windows 源码路径 | `D:\luode\ellipal_admin` | 代码实际存放位置，VSCode 编辑 |
| WSL 自动挂载路径 | `/mnt/d/luode/ellipal_admin` | WSL 启动时自动挂载，作为 bind 的源 |
| WSL 用户工作路径 | `/home/luode/d/luode/ellipal_admin` | bind mount 目标，**所有项目命令在此执行** |

**项目命令统一使用用户工作路径 `/home/luode/d/luode/<project>`，不使用 `/mnt/d/...`。**

## WSL 挂载检查与挂载流程

**在执行任何 WSL 命令之前，必须先检查用户工作路径是否已 bind mount**，流程如下：

### 第一步：检查 bind mount 是否就绪

```powershell
wsl.exe -e bash -lc "mountpoint -q /home/luode/d/luode/ellipal_admin && echo 'mounted' || echo 'not_mounted'"
```

- 输出 `mounted`：直接进入第三步执行项目命令
- 输出 `not_mounted`：进入第二步执行 bind mount

### 第二步：执行 bind mount

```powershell
wsl.exe -e bash -lc "mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount --bind /mnt/d/luode/ellipal_admin /home/luode/d/luode/ellipal_admin"
```

若需要持久化（WSL 重启后自动挂载），追加 fstab：

```powershell
wsl.exe -e bash -lc "grep -v '/mnt/d/luode/ellipal_admin' /etc/fstab | sudo tee /etc/fstab && echo '/mnt/d/luode/ellipal_admin    /home/luode/d/luode/ellipal_admin    none    bind    0 0' | sudo tee -a /etc/fstab && mkdir -p /home/luode/d/luode/ellipal_admin && sudo mount -a"
```

**⚠️ 如果 sudo 要求交互式输入 root 密码，必须立即停止自动执行，通知用户：**

> "WSL bind mount 需要 root 密码，请在 WSL 终端中手动执行以下命令，完成后告知我：
> ```bash
> mkdir -p /home/luode/d/luode/ellipal_admin
> sudo mount --bind /mnt/d/luode/ellipal_admin /home/luode/d/luode/ellipal_admin
> ```
> 完成后请回复，我将继续执行后续步骤。"

等待用户确认后，重新执行第一步验证挂载成功，再继续。

### 第三步：执行项目命令

挂载确认后，使用用户工作路径执行命令：

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && <COMMAND>"
```

## 路径换算规则

Windows 路径经过两步转换，最终得到 WSL 用户工作路径：

```
D:\luode\ellipal_admin
  → /mnt/d/luode/ellipal_admin      (WSL 自动挂载，第一步)
  → /home/luode/d/luode/ellipal_admin  (bind mount，第二步，实际使用路径)
```

通用换算（第一步，Windows → WSL 自动挂载路径）：
- 盘符转小写，去掉 `:`，`\` 改为 `/`，前缀 `/mnt/`
- `D:\luode\project` → `/mnt/d/luode/project`

bind mount 目标路径规则（第二步）：
- 格式：`/home/<user>/d/<win-path-without-drive>`
- `D:\luode\ellipal_admin` → `/home/luode/d/luode/ellipal_admin`

如果项目本身已经位于 WSL 内部路径，例如 `\\wsl$\Ubuntu\home\user\repo`，优先确认是否可直接通过对应发行版中的 Linux 路径执行；不要再强行走 bind mount 规则。

## 强制执行策略

**Windows 侧只负责**（不执行任何项目命令）：
- 编辑源代码文件
- 浏览仓库目录结构
- 读取日志、产物文件
- 调用 `wsl.exe` 向 WSL 发起命令

**WSL 侧强制承担所有执行任务**：
- 安装依赖（`go mod download`、`pnpm install` 等）
- 启动开发服务
- 构建二进制（`go build`）
- 运行测试（`go test ./...`）
- 格式化、lint、typecheck
- 运行项目脚本
- 启动调试器（`dlv`）
- 所有需要网络通信的进程

**原因**：Windows 无法运行项目二进制，且只有 WSL 进程可以正常使用网络。

## 团队目录与工作流

### 目录约定

项目真实文件放在 `D:\luode\` 下，WSL 通过 bind mount 映射到用户目录：

- Windows：`D:\luode\ellipal_admin`
- WSL 自动挂载：`/mnt/d/luode/ellipal_admin`（桥梁，不直接使用）
- WSL 用户工作路径：`/home/luode/d/luode/ellipal_admin`（**实际执行路径**）

### 工作流分工

1. **Windows 侧负责编辑**
   - VSCode 直接打开 `D:\luode\<project>`
   - 资源管理器、编辑器操作 Windows 真实文件
2. **WSL 侧负责所有执行**
   - 启动项目、调试、测试、构建、安装依赖
   - 所有需要网络的进程均在 WSL 内运行

### bind mount 挂载步骤

首次使用或 WSL 重启后需要挂载：

```bash
# 临时挂载（WSL 重启后失效）
mkdir -p /home/luode/d/luode/ellipal_admin
sudo mount --bind /mnt/d/luode/ellipal_admin /home/luode/d/luode/ellipal_admin
```

持久化（写入 fstab，WSL 重启后自动生效）：

```bash
grep -v '/mnt/d/luode/ellipal_admin' /etc/fstab | sudo tee /etc/fstab
echo '/mnt/d/luode/ellipal_admin    /home/luode/d/luode/ellipal_admin    none    bind    0 0' | sudo tee -a /etc/fstab
mkdir -p /home/luode/d/luode/ellipal_admin
sudo mount -a
```

### 推荐边界

- Windows 打开文件用真实盘符路径 `D:\luode\...`
- WSL 命令执行用 bind mount 后的用户工作路径 `/home/luode/d/luode/...`
- 不把 `\\wsl.localhost\...` 当成 Windows 访问 Windows 挂载盘的稳定入口
- 若代码真实放在 WSL 内部目录，则 Windows 打开和 Codex 协作方式应重新单独规划

## 固定命令模板

默认模板（使用用户 bind mount 路径）：

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/<project>' && <COMMAND>"
```

Go 项目示例（团队主要技术栈）：

```powershell
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go build ./..."
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go test ./..."
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && go run ./cmd/server"
wsl.exe -e bash -lc "cd '/home/luode/d/luode/ellipal_admin' && dlv dap --listen=:2345 --headless=true --log"
```

如果需要加载 shell 环境、nvm、asdf、pyenv 或其他 profile 逻辑，可改用：

```powershell
wsl.exe -e bash -lic "cd '/home/luode/d/luode/<project>' && <COMMAND>"
```

仅当项目明确依赖交互式登录 shell 初始化时才使用 `-lic`；默认优先 `-lc`。

## 命令选择规则

- 用户说“启动项目”“跑测试”“调试一下”“验证构建”时，先推断真实项目命令，再通过 WSL 执行。
- 如果项目已有 `package.json`、`Makefile`、`justfile`、`pytest.ini`、`go.mod`、`Cargo.toml`、`manage.py` 等入口，优先复用项目已有命令。
- 如果项目已有仓库级脚本或 README 说明，遵循项目已有执行入口，不要额外发明 Windows 侧替代命令。

## 允许直接在 Windows 执行的情况

以下情况可以继续在 Windows 侧执行，而不强制切 WSL：

- 纯文件搜索、读文件、列目录
- Git 状态查看、差异查看、日志查看
- 明确属于 Windows 系统管理的命令
- 仅操作 Windows 本地产物，且与 Linux 运行环境无关

## 不要这样做

- 不要在 Windows PowerShell 或 Git Bash 中直接执行 `go build`、`go test`、`go run`、`dlv`、`pnpm`、`npm`、`yarn`、`pytest` 等项目命令
- 不要假设”Git Bash 已经够用”——Git Bash 不是 WSL，网络限制同样存在
- 不要只切到 Windows 工作目录就假设命令环境已经正确
- 不要忽略路径换算，直接把 `D:\...` 原样塞进 `bash -lc`
- 不要在 `tasks.json` 或 `launch.json` 中使用 `cmd`、`powershell` 作为 shell 运行项目命令
- 不要试图在 Windows 侧直接运行 `dlv`——调试器必须在 WSL 内启动

## VSCode 调试配置规范（Go 项目）

项目必须维护 `.vscode/launch.json` 和 `.vscode/tasks.json`，用于在 VSCode 中通过 WSL 完成调试。

**调试架构**：

```
VSCode (Windows) ──DAP协议──► dlv dap (WSL 内)
                                    │
                              /mnt/d/luode/project (WSL 挂载的 Windows 目录)
```

### tasks.json 规范

`tasks.json` 中所有 shell 命令必须使用 `wsl.exe` 作为执行器：

- `”type”: “shell”`
- `”command”: “wsl.exe”`
- args 格式：`[“-e”, “bash”, “-lc”, “cd '<WSL_PATH>' && <COMMAND>”]`

常见任务类型：`go build`、`go test`、启动 `dlv dap` 监听端口。

### launch.json 规范

Go 调试配置必须使用远程附加模式，通过端口连接 WSL 内运行的 `dlv`：

- `”type”: “go”`
- `”request”: “attach”`
- `”mode”: “remote”`
- `”port”: 2345`（与 `dlv dap --listen=:2345` 对应）
- `”substitutePath”`：映射 Windows 工作目录与 WSL 挂载路径，用于断点对齐

详细模板见 `references/vscode-debug-config.md`。

### VSCode 调试流程

1. 在 VSCode 中运行 `tasks.json` 中的”WSL: Start dlv”任务，在 WSL 内启动 `dlv dap`
2. VSCode 的 Go 调试器通过 `localhost:2345` 连接 WSL 内的 `dlv`
3. `substitutePath` 确保 Windows 侧的断点与 WSL 侧的源码路径正确对齐
4. 所有运行时网络请求均由 WSL 内的进程发出，不受 Windows 网络限制

## 与其他规则的协作

- 涉及仓库长期规则沉淀时，联动 `project-agents-bootstrap`，把”Windows 编辑、WSL 执行”的约束写入仓库规则文件（Codex：`AGENTS.md`，Claude Code：`CLAUDE.md`）
- 涉及测试覆盖和回归策略时，让路给 `test-strategy-rules`、`test-regression-rules`
- 涉及语言或框架本身的命令选择时，让路给对应语言/框架 skill（Go 项目联动 `golang-patterns`）
- 涉及 Windows 中文编码、日志重定向或 PowerShell 落盘时，可联动 `windows-encoding-rules`

## 默认输出要求

当本 skill 被命中且实际执行了项目命令时，结果说明至少应包含：

- Windows 原始项目路径
- 换算后的 WSL 项目路径
- 实际执行的 WSL 命令
- 是否成功进入 WSL 并执行
- 若失败，失败发生在”路径换算 / 进入目录 / 命令执行”哪一层

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 需要 VSCode `launch.json` / `tasks.json` 模板时，读 `references/vscode-debug-config.md`
- 只有在需要确认路径转换细节或边界场景时，再读 `references/path-mapping.md`
- 需要团队推荐目录、协作方式或挂载命令时，再读 `references/recommended-workflow.md`
