# 命令模板库（Windows agent → WSL 项目）

> 本文件是 `wsl-host-agent` 的命令模板权威；SKILL.md 正文只保留核心命令，完整变体在此。
> 全部模板经 2026-08-26 真实场景验证（EllipalFinance-go，发行版 Ubuntu-24.04）。

## 变量约定

| 变量 | 本机值 | 说明 |
| --- | --- | --- |
| `DIST` | `Ubuntu-24.04` | WSL 发行版（`wsl.exe -l -v` 确认） |
| `WREPO` | `/home/luode/code/<repo>` | WSL 侧项目真实路径 |
| `PORT` | 如 `12346` | 服务监听端口 |

## 1. 编译 / 构建

```bash
cd /c/ && MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' \
  wsl.exe -d Ubuntu-24.04 --cd /home/luode/code/<repo> -- \
  bash -lc 'cd /home/luode/code/<repo> && go build ./... && echo BUILD_OK' 2>&1 | tr -d '\0'
```

变体：

- 只编译部分包：`go build ./internal/router/... ./internal/controller/...`
- 慢任务放后台：Bash 工具 `run_in_background=true`，完成后自动通知。
- 查看完整输出：不滤 NUL 也行，但 Git Bash 下输出会带 `\0` 难读；`tr -d '\0'` 是安全标配。

## 2. 起服务（可靠姿势）

```bash
# Bash 工具 run_in_background=true 持有；命令内显式 cd，不要依赖调用方 cwd
cd /c/ && MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' \
  wsl.exe -d Ubuntu-24.04 -- \
  bash -lc 'cd /home/luode/code/<repo> && exec go run main.go -env apifox' 2>&1 | tr -d '\0'
```

- `exec` 让 go run 取代 bash，便于按 pid 精确停服。
- go run 首次要编译，探活需留足时间（本机约 30s）；探活循环建议 `for i in $(seq 1 8); do ...; sleep 8; done`。

探活：

```bash
curl -s -o /dev/null -w "%{http_code}" --max-time 3 \
  -X POST http://127.0.0.1:12346/api/exchange/system/version   # 期望 200
curl -s --max-time 5 -X POST http://127.0.0.1:12346/api/swap/v2/mainList \
  -H "Content-Type: application/json" -d '{}'                   # 期望鉴权拦截文案
```

- WSL2 localhost 转发使 Windows 侧 curl 可直接探活，无需 IP。
- version 接口是 POST；GET 会 404 造成"服务没起来"的误判。

## 3. 停服

```bash
# 1) 找 pid（grep 不带引号空格！）
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' wsl.exe -d Ubuntu-24.04 -- bash -lc \
  'ss -ltnp | grep :12346'

# 2) 杀 + 确认
MSYS_NO_PATHCONV=1 wsl.exe -d Ubuntu-24.04 -- bash -lc \
  'kill 12345; sleep 2; ss -ltnp | grep :12346 || echo PORT_FREE_NOW'
```

- 若后台任务持有 wsl.exe，杀服务进程后任务会自然结束；再 `TaskOutput` 回收确认退出。
- 端口残留检查：`ss -ltnp | grep :<port> || echo PORT_FREE`。
- **自动提取 PID 必须脚本文件方式（2026-08-27 实测）**：`wsl.exe ... -- bash -lc 'PID=$(ss -ltnp | grep :12346 | grep -o "pid=[0-9]*" | cut -d= -f2)'` 内联传参时 MSYS 会破坏 grep pattern 的引号/星号，PID 恒提取为空、kill 落空但脚本照常打印 `PORT_FREE` 假象（实测复现两次）。正确做法：把提取脚本写到 Windows Temp（`/mnt/c/Users/<user>/AppData/Local/Temp/stop.sh`）再 `bash /mnt/c/.../stop.sh` 执行；脚本文件方式下 `grep -oP 'pid=\K[0-9]+'` 与 `grep -o 'pid=[0-9]*' | cut -d= -f2` 均验证有效。

## 4. Windows Python 调 shim 工具（apifox 等）

```python
import subprocess
# 无扩展名 shim（如 apifox）对 subprocess PATH 不友好，用 node 直启 cli.js
APIFOX = [r"C:/Users/luode/.workbuddy/binaries/node/versions/22.22.2/node.exe",
          r"C:/Users/luode/.workbuddy/binaries/node/versions/22.22.2/node_modules/apifox-cli/bin/cli.js"]
out = subprocess.run(APIFOX + ["test-case", "get", "407431966", "--project", "8735371"],
                     capture_output=True, text=True)
```

- 或直接调同目录 `apifox.cmd`（Windows cmd 包装器，subprocess 可执行）。
- 判断 shim：`cat <shim路径>` 内容是 `#!/bin/sh` 头 = shell shim，不能直接 exec。

## 5. 端口占用排查（起服务前）

```bash
MSYS_NO_PATHCONV=1 MSYS2_ARG_CONV_EXCL='*' wsl.exe -d Ubuntu-24.04 -- bash -lc \
  'ss -ltnp | grep :12346 || echo PORT_12346_FREE'
```
