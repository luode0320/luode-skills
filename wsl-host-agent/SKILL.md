---
name: wsl-host-agent
description: >-
  Windows 侧 agent 操作 WSL 项目（agent 在 Windows 宿主、项目源码在 WSL）的
  编译 / 启动 / 调试完整工作流。当项目通过符号链接（如 C:\Users\luode\WorkBuddy\兑换
  → \\wsl.localhost\...\EllipalFinance-go）挂载进 Windows 工作区、需要编译、
  起服务、探活、停服，或遇到 Windows go 报 "Incorrect function"/RLock 失败、
  wsl.exe chdir 失败、nohup 启动后端口没监听、Git Bash 路径被 MSYS 转换、
  WSL 输出 NUL 乱码、Windows Python 找不到无扩展名 shim 工具时触发。核心原则：
  编辑搜索走 Windows 侧符号链接（无锁操作正常），构建与运行必须显式切 WSL 工具链。
  当用户提到"Windows agent + WSL 项目""符号链接挂载编译""go build 报错
  Incorrect function""wsl.exe 编译/起服务""WSL 里启动调试""\\wsl.localhost 文件锁"
  时使用。

---

# Windows 宿主 Agent + WSL 项目（符号链接拓扑）编译启动调试

## 目的与适用范围

让跑在 **Windows 宿主** 的 agent 操作源码在 **WSL** 里的项目（通过符号链接把 WSL 目录挂载进 Windows 工作区，如 `C:\Users\luode\WorkBuddy\兑换 → \\wsl.localhost\Ubuntu-24.04\home\luode\code\EllipalFinance-go`）。

- 适用于：项目在 WSL、agent 在 Windows、已用符号链接进工作区/空间的场景；Go 等语言项目的编译、起服务、探活、停服、调试。
- 前提：WSL2 + 具体发行版（本机 `Ubuntu-24.04`）；项目在 Windows 侧通过符号链接可达；符号链接只解决"编辑/搜索可读"，**构建写锁必须回 WSL**。
- 关键事实：Windows 版 go 对 `\\wsl.localhost` 路径做 RLock 失败（报 `Incorrect function`），所以**编译只能走 WSL 工具链**；从符号链接 cwd 直接调 `wsl.exe` 会 chdir 失败，必须先 `cd /c/` 脱离。

## 核心原则（为什么）

- **编辑搜索走 Windows，构建运行回 WSL**：文件读写/搜索/git 盘点等无锁操作走 Windows 侧符号链接路径，正常无痛；构建类写锁操作（go build、服务启动）在 Windows 侧必失败，必须切 WSL 工具链。
- **符号链接是"进空间"的钥匙**：实测符号链接目录可被 WorkBuddy 登记为工作区/空间（`.workbuddy/` 正常生成），并非不可行——但构建必须在 WSL 侧。这与"Temp 副本 + Windows 工具链"（路线 A）是两条平行路线，本 skill 是符号链接路线（路线 B）。
- **wsl.exe 是桥**：通过 `wsl.exe -d <发行版> -- bash -lc '...'` 执行 WSL 命令；Git Bash 下必须加 MSYS 前缀防路径转换，管道尾滤 NUL。

## 前置检查（每轮必做）

1. 拓扑确认：`cmd //c "dir C:\Users\<user>\WorkBuddy"` 看项目项是否 `-> \\wsl.localhost\...`（符号链接）还是真实目录；同时确认 `.workbuddy/` 存在（进空间成功标志）。
2. 发行版确认：`wsl.exe -l -v` 记下发行版名（本机 `Ubuntu-24.04`），命令模板里的 `-d` 参数用它。
3. 项目真实路径确认：WSL 侧 `ls -d /home/<user>/code/<repo>` 必须可达（Windows 符号链接目标就是它）。
4. 端口占用检查（起服务前）：`wsl.exe -d Ubuntu-24.04 -- bash -lc 'ss -ltnp | grep :<port> || echo PORT_FREE'`。

## 编译模板（WSL 工具链）

```bash
cd /c/ && MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' \
  wsl.exe -d Ubuntu-24.04 --cd /home/luode/code/<repo> -- \
  bash -lc 'cd /home/luode/code/<repo> && go build ./... && echo BUILD_OK' 2>&1 | tr -d '\0'
```

- `cd /c/`：脱离符号链接 cwd（否则 wsl chdir 失败）。
- `MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'`：防 Git Bash 把 `/home/...` 转成 Windows 路径。
- `| tr -d '\0'`：滤 WSL 输出里的 NUL 字符。
- 不要用 Windows 版 go 编译符号链接路径下的项目（RLock 失败 `Incorrect function`）。

## 起服务模板（后台任务前台持有）

```bash
# 在 Bash 工具里 run_in_background=true 执行；wsl.exe 进程被任务持有，服务随任务存活
cd /c/ && MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' \
  wsl.exe -d Ubuntu-24.04 -- \
  bash -lc 'cd /home/luode/code/<repo> && exec go run main.go -env <env>' 2>&1 | tr -d '\0'
```

- **不要用 nohup**：从符号链接 cwd 启动时后台进程建立失败（WSL 继承 cwd 失败），服务起不来；后台任务前台持有 wsl.exe 是可靠方式。
- 探活用 **POST**（如 `/api/exchange/system/version` 是 POST 不是 GET，GET 会 404 误判未启动）；v2 接口无签名请求返回 HTTP 200 + `missing api key or authorization` 属**鉴权拦截正常**，不是路由问题。
- 新 URL 路由验证：直接 POST 新路径应拿到鉴权拦截文案（证明路由生效）；旧 URL 应 404（证明无残留双份路由）。

## 停服模板（按端口找 pid）

```bash
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' wsl.exe -d Ubuntu-24.04 -- bash -lc \
  'ss -ltnp | grep :<port>'    # 找 listener pid
MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-24.04 -- bash -lc \
  'kill <pid>; sleep 2; ss -ltnp | grep :<port> || echo PORT_FREE'   # 杀后确认
```

- `grep` 表达式**不要带引号空格**（如 `grep ":12346 "`）：MSYS 会转义弄坏引号导致匹配失败；直接 `grep :12346`。
- 按端口定位 pid 比 `pgrep main` 更准（避免杀错同名进程）。

## 坑位速查

| 症状 | 原因 | 处理 |
| --- | --- | --- |
| Windows go 编译报 `Incorrect function` / RLock 失败 | Windows go 对 `\\wsl.localhost` 做文件锁失败 | 编译走 WSL 工具链（见编译模板） |
| `wsl.exe` 启动报 chdir 失败 | 从 Windows 符号链接 cwd 调 wsl.exe | 先 `cd /c/` 脱离再调 |
| nohup 启动后端口没监听 | WSL 继承符号链接 cwd 失败，后台进程未建立 | 改用 Bash 后台任务前台持有 wsl.exe |
| wsl 输出乱码 / NUL | Git Bash 管道透传 | 命令尾 `\| tr -d '\0'` |
| `/home/...` 路径被转成 `C:\...` | Git Bash MSYS 路径转换 | 命令前缀 `MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*'` |
| 探活 GET 返回 404 | 接口是 POST（如 version） | 用 POST 探活 |
| 无签名请求返回 200 + `missing api key` | 鉴权拦截在 HTTP 层之后 | 属正常鉴权拦截，不是路由问题 |
| 停服 `grep ":<port> "` 匹配不到 | MSYS 转义弄坏引号 | 用 `grep :<port>`（不带引号空格） |
| Windows Python 报找不到 apifox 等命令 | 无扩展名 shim 对子进程 PATH 不友好 | `node <cli>/bin/cli.js` 直启，或调 `.cmd` 包装器 |

## 环境自检（换机器/干净环境先跑）

- `wsl.exe -l -v`：确认 WSL2 + 目标发行版存在。
- `cmd //c "dir <项目父目录>"`：确认符号链接指向 `\\wsl.localhost\...`。
- `echo $MSYS_NO_PATHCONV` 为空是正常（命令前缀里临时设置，不持久化）；验证方式：带前缀跑一条 `wsl.exe -d <发行版> -- bash -lc 'echo /home/ok'`，输出应为 `/home/ok` 而非 `C:\...\home\ok`。
- `wsl.exe -d <发行版> -- bash -lc 'ls -d /home/<user>/code/<repo>'`：项目真实路径可达。
- Windows 侧 python 调 shim 工具前先确认真实入口：`ls <node>/node_modules/<cli>/bin/` 找 `cli.js`。

## 边界与不负责事项

- 只负责 **Windows agent → WSL 项目**方向（符号链接拓扑）；反向（WSL 内 agent 调 Windows 工具）见第三方 `wsl-windows-bridge`。
- shell 选择策略（何时 WSL / 何时 PowerShell）见第三方 `wsl-shell-reliability`；本 skill 默认已在 WSL 场景内。
- 项目自身业务逻辑、接口契约、测试断言不在本 skill 范围。
- 符号链接的创建/回滚、junction 挂载云盘见自建 `gdrive-junction-mount`。

## References

- 深度参考（单一权威，含路线 A/B 对比与完整背景）：`D:\谷歌云盘\知识库\20-Knowledge\开发环境\agent在Windows项目在WSL的编译启动调试经验.md`
- 命令模板库：`references/command-templates.md`
- 吸收裁决表：`workbuddy-absorption-map.md`；来源记录：`references/source-notes.md`
