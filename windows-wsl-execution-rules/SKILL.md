---
name: windows-wsl-execution-rules
description: 当任务运行在 Windows 上、项目目录位于 Windows 文件系统中、但项目实际需要通过 WSL 内的 Linux 工具链执行启动、调试、测试、构建、安装依赖或脚本时自动触发。适用于 Codex 桌面端、Windows 终端或仓库规则明确要求“Windows 侧编辑、WSL 侧运行”的场景；负责统一把 Windows 项目路径映射到 WSL 路径，通过 `wsl.exe` 或等价方式进入对应 Linux 目录执行命令，并优先避免直接在 PowerShell 中运行本应在 Linux 环境执行的项目命令。不要用它代替具体语言/框架的实现、测试策略、编码规则或 WSL 安装说明。
---

# Windows -> WSL 执行规则

用于统一这类项目的默认执行方式：

- 仓库在 Windows 目录中，例如 `F:\repo\app`
- 编辑发生在 Windows 侧，例如 Codex 桌面端、编辑器、资源管理器
- 启动、调试、测试、构建、依赖安装实际应在 WSL 中执行

核心目标是避免出现以下问题：

- 在 PowerShell 里直接跑 `npm test`、`pnpm dev`、`go test`、`pytest`，导致环境不一致
- 明明仓库在 Windows 盘符下，却没有先切到对应的 WSL 路径
- 命令在 Windows shell 可执行，但结果与用户真实运行环境不一致

## 自动触发信号

- 用户提到 `Windows`、`WSL`、`Git Bash`、`Ubuntu`、`Linux 环境`、`Codex 桌面端`
- 用户说明项目代码位于 `C:`、`D:`、`E:`、`F:` 等 Windows 盘符目录，但运行依赖 WSL
- 当前任务包含启动、调试、测试、构建、安装依赖、运行脚本、查看运行时错误
- 当前工作目录是 Windows 路径，但命令明显属于 Linux 工具链场景
- 用户要求为项目建立“Windows 编辑、WSL 运行”的长期规则

## 进入后先做什么

1. 先判断当前项目根目录是否位于 Windows 文件系统。
2. 若位于 Windows 盘符路径，先把路径转换为对应的 WSL 路径。
3. 执行项目命令时，优先使用 `wsl.exe -e bash -lc "<command>"`。
4. 在 WSL 中先 `cd` 到映射后的项目目录，再运行实际命令。
5. 除非任务本身就是 Windows 专属命令，否则不要直接在 PowerShell 中运行项目测试、构建或调试命令。

## 路径换算规则

将 Windows 路径按以下规则映射到 WSL：

- `C:\repo\app` -> `/mnt/c/repo/app`
- `F:\code\demo` -> `/mnt/f/code/demo`
- 反斜杠 `\` 全部改为正斜杠 `/`
- 盘符转为小写并挂载到 `/mnt/<drive-letter>`

如果项目本身已经位于 WSL 内部路径，例如 `\\wsl$\Ubuntu\home\user\repo`，优先确认是否可直接通过对应发行版中的 Linux 路径执行；不要再强行走 `/mnt/<drive>` 规则。

## 默认执行策略

- Windows 侧负责：
  - 编辑代码
  - 浏览仓库
  - 读取日志文件
  - 调用 `wsl.exe`
- WSL 侧负责：
  - 安装依赖
  - 启动开发服务
  - 跑测试
  - 跑构建
  - 跑格式化、lint、typecheck
  - 运行项目脚本

## 团队推荐目录与工作流

以下内容是推荐流程，不是强制约束。适合“Windows 上用 Codex 桌面端和常规工具编辑，WSL 中用 Linux 工具链运行”的团队协作方式。

### 推荐目录方案

推荐把项目真实文件放在 Windows 盘符目录，例如：

- `F:\code\project-a`
- `F:\code\project-b`

这样做的优点是：

- Windows 侧工具可直接打开真实路径
- WSL 中可直接通过 `/mnt/f/code/project-a` 访问同一份文件
- Windows Codex、资源管理器、常规编辑器与 WSL 看到的是同一份代码

不推荐把“Windows 盘映射进 WSL 的目录”再反向作为 Windows 打开入口，例如：

- 不要把 `\\wsl.localhost\Ubuntu\home\luode\f` 当成 `F:\` 的替代入口

这类路径在 WSL 中可用，但 Windows 通过 `\\wsl.localhost` 再反向访问 Windows 挂载盘时往往不稳定。

### 推荐工作流

推荐团队按下面的角色分工协作：

1. Windows 侧负责编辑
   - Codex 桌面端修改 `F:\...` 中的真实文件
   - 资源管理器、Windows 编辑器直接打开 `F:\...`
2. WSL 侧负责运行
   - 启动项目
   - 调试项目
   - 跑测试
   - 跑构建
   - 安装依赖
3. VS Code 可二选一
   - 直接打开 Windows 目录 `F:\code\project-a`
   - 或使用 WSL/Remote 打开 `/mnt/f/code/project-a`

### 推荐挂载辅助目录

如果团队希望在 WSL 的 home 目录下有更顺手的入口，可以建立一个“仅供 WSL 内使用”的辅助目录，例如：

```bash
mkdir -p /home/luode/work
sudo mount --bind /mnt/f/code /home/luode/work/code
```

或者先创建目录再绑定：

```bash
mkdir -p /home/luode/work/code
sudo mount --bind /mnt/f/code /home/luode/work/code
```

这样在 WSL 中可以使用：

- `/home/luode/work/code/project-a`

但在 Windows 中仍然建议直接打开：

- `F:\code\project-a`

不要把这个 bind mount 目录当成 Windows 访问入口。

### 推荐持久化挂载步骤

如果希望 WSL 每次启动后自动有这个辅助入口，可追加到 `/etc/fstab`：

```bash
sudo mkdir -p /home/luode/work/code
echo '/mnt/f/code /home/luode/work/code none bind 0 0' | sudo tee -a /etc/fstab
sudo mount -a
```

如果只想映射整个 `F:`，可以使用：

```bash
sudo mkdir -p /home/luode/work/f
echo '/mnt/f /home/luode/work/f none bind 0 0' | sudo tee -a /etc/fstab
sudo mount -a
```

### 推荐命令入口

推荐从 Windows 侧始终显式使用 WSL 执行命令，例如：

```powershell
wsl.exe -e bash -lc "cd '/mnt/f/code/project-a' && pnpm test"
wsl.exe -e bash -lc "cd '/mnt/f/code/project-a' && go test ./..."
wsl.exe -e bash -lc "cd '/mnt/f/code/project-a' && pytest"
```

如果团队统一采用 `/home/luode/work/code/project-a` 作为 WSL 内部快捷路径，也可以执行：

```powershell
wsl.exe -e bash -lc "cd '/home/luode/work/code/project-a' && pnpm test"
```

### 推荐边界

- Windows 打开文件优先用真实盘符路径，例如 `F:\...`
- WSL 运行命令优先用 `/mnt/f/...` 或团队约定的 bind mount 快捷路径
- 不把 `\\wsl.localhost\...` 当成 Windows 访问 Windows 挂载盘的稳定入口
- 若代码真实放在 WSL 内部目录，则 Windows 打开和 Codex 协作方式应重新单独规划

## 固定命令模板

默认模板：

```powershell
wsl.exe -e bash -lc "cd '<WSL_PROJECT_PATH>' && <COMMAND>"
```

示例：

```powershell
wsl.exe -e bash -lc "cd '/mnt/f/code/myapp' && npm test"
wsl.exe -e bash -lc "cd '/mnt/f/code/myapp' && pnpm dev"
wsl.exe -e bash -lc "cd '/mnt/f/code/myapp' && pytest"
wsl.exe -e bash -lc "cd '/mnt/f/code/myapp' && go test ./..."
wsl.exe -e bash -lc "cd '/mnt/f/code/myapp' && cargo test"
```

如果需要加载 shell 环境、nvm、asdf、pyenv 或其他 profile 逻辑，可改用：

```powershell
wsl.exe -e bash -lic "cd '<WSL_PROJECT_PATH>' && <COMMAND>"
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

- 不要在 Windows PowerShell 中直接执行本应在 WSL 内运行的 `npm`、`pnpm`、`yarn`、`pytest`、`go test`、`cargo test`、`python manage.py runserver` 等命令
- 不要只切到 Windows 工作目录就假设命令环境已经正确
- 不要忽略路径换算，直接把 `F:\...` 原样塞进 `bash -lc`
- 不要把这个 skill 用成“强制所有命令都走 WSL”；Windows 专属命令仍应留在 Windows

## 与其他规则的协作

- 涉及仓库长期规则沉淀时，联动 `project-agents-bootstrap`，把“Windows 编辑、WSL 执行”的约束写入仓库 `AGENTS.md`
- 涉及测试覆盖和回归策略时，让路给 `test-strategy-rules`、`test-regression-rules`
- 涉及语言或框架本身的命令选择时，让路给对应语言/框架 skill
- 涉及 Windows 中文编码、日志重定向或 PowerShell 落盘时，可联动 `windows-encoding-rules`

## 默认输出要求

当本 skill 被命中且实际执行了项目命令时，结果说明至少应包含：

- Windows 原始项目路径
- 换算后的 WSL 项目路径
- 实际执行的 WSL 命令
- 是否成功进入 WSL 并执行
- 若失败，失败发生在“路径换算 / 进入目录 / 命令执行”哪一层

## 参考资料读取规则

- 默认先读 `references/command-templates.md`
- 只有在需要确认路径转换细节或边界场景时，再读 `references/path-mapping.md`
- 需要团队推荐目录、协作方式或挂载命令时，再读 `references/recommended-workflow.md`
