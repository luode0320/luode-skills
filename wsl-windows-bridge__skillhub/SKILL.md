---
name: wsl-windows-bridge
description: 'WSL ↔ Windows cross-system bridge for agents. Provides win-python / win-ps / win-cmd / win-copy / win-run-py / win-path to invoke Windows Python (Anaconda), execute PowerShell/CMD commands, and read/write Windows files from WSL2. Ideal for quantitative trading (QMT/xtquant), cross-system file operations, and Windows environment scripting. Also covers the reverse topology: agent on Windows host working with WSL projects (Temp-copy compile workflow for go.mod RLock, 18080 port, captcha dev bypass, PowerShell interception, Windows Python path style). 也覆盖 agent 在 Windows 宿主、项目在 WSL 的编译启动调试工作流。另含「免桥直读」前置判定：WSL 内只读写 Windows 盘上的文件时走 drvfs /mnt/drive 直读，不用 win-* 命令；只有调用 Windows 侧程序才用桥。并收录 WSL↔Windows 通信静默失败陷阱清单：find 起点是符号链接时零结果、Windows 风格路径被当相对路径、drvfs 以 9p 类型出现、同盘符多挂载点、中文路径分词、heredoc 定界符冲突、管道遮蔽退出码。当 WSL 侧读不到 Windows 盘上的文件、目录看起来是空的、脚本报路径不存在但手敲能进、写出的文件被静默截断时按其排查顺序定位。'
license: MIT
metadata:
  compatibility: 'WSL2 + Windows 10/11, Windows Python (Anaconda or any), PowerShell'
  openclaw:
    emoji: 🪟
    requires:
      bins: ["bash", "wslpath", "powershell.exe", "cmd.exe"]
      env: []
    primaryEnv: null
---

# WSL ↔ Windows Cross-System Bridge

> Seamless access to Windows Python, PowerShell, CMD, and filesystem from WSL2.

## Features

| Command | Purpose |
|---------|---------|
| `win-python` | Invoke Windows Python (Anaconda or any) |
| `win-ps` | Execute PowerShell commands |
| `win-cmd` | Execute CMD commands |
| `win-copy` | Copy files between WSL and Windows |
| `win-run-py` | Run .py scripts with logging |
| `win-path` | Convert paths WSL `/mnt/*` ↔ Windows `D:\*` |

## 前置判定：先确认真的需要桥（免桥直读优先）

bridge 的价值在**跨系统执行**，不在跨系统读文件。WSL 已经把 Windows 盘经 drvfs 挂载到
`/mnt/<drive>`，POSIX 工具可直接读写，多套一层 `win-ps` / `win-copy` 只会增加进程开销、
编码转换风险和失败面。动手前先按下表判定：

| 当前动作 | 走哪条路 |
| --- | --- |
| 读 / 写 / 搜索 / 移动 Windows 盘上的文件 | **免桥直读** `/mnt/<drive>/...`，用 `cat` / `rg` / `find` / `mv` / heredoc |
| 执行 Windows 侧程序（Python、exe、cmdlet、服务查询） | 用桥：`win-python` / `win-ps` / `win-cmd` |
| 把文件从 WSL 家目录搬到 Windows 盘（或反向） | 直接 `cp` 到 `/mnt/<drive>/...` 即可；`win-copy` 只在需要 Windows 侧权限语义时用 |
| 路径形态互转 | `wslpath` / `win-path`，见 `wsl-path-converter__skillhub` |

### 免桥直读要点

```bash
# 1. 确认盘符已挂载。WSL2 现版本 drvfs 以 9p 类型出现，不要因为 type 不是字面 drvfs 就判定未挂载
ls -d /mnt/d
mount | grep -i drvfs        # D:\ on /mnt/d type 9p (...aname=drvfs;path=D:\...)

# 2. 含中文或空格的路径全程加引号，否则被 shell 分词
DIR="/mnt/d/谷歌云盘/知识库"
ls -1 "$DIR"

# 3. 写入用 quoted heredoc，避免正文里的 $ / 反引号 / 反斜杠被 shell 展开
cat > "$DIR/note.md" <<'MD'
正文原样写入
MD

# 4. 回读校验编码与指纹，确认中文未乱码
file -i "$DIR/note.md"       # 应为 charset=utf-8
md5sum "$DIR/note.md"; wc -c "$DIR/note.md"
```

同一盘符可能同时挂载在多个挂载点（`/mnt/d` 与 `~/d/<user>` 等），它们指向同一份文件；
统一只用 `/mnt/<drive>` 这一个规范形态参与路径拼接，避免同一文件在证据里出现两种绝对路径。

**不要因为 WSL 侧一时读不到就上桥**：先按第 1 步确认挂载、按第 2 步确认引号。真正需要桥的
只有「Windows 侧 HOME 与 WSL HOME 是两套独立目录」这类场景（见下文 Sync Windows-side data）。

### 静默失败先查陷阱清单

WSL 侧读不到 Windows 盘上的东西时，绝大多数是**不报错**的静默失败：零结果、`False`、
看起来"目录是空的"。上桥前先按
[references/wsl-windows-comm-pitfalls.md](references/wsl-windows-comm-pitfalls.md)
的排查顺序走一遍——7 个实测陷阱，含 find 起点是符号链接时零结果、Windows 风格路径被当
相对路径、heredoc 定界符与正文冲突导致文件静默截断。**零结果先查起点类型与路径形态，
不要先怀疑编码或权限。**

Google Drive 同步目录（知识库等）在 WSL 内的读写口径见
`knowledge-flow` 的 `references/wsl-access.md`，本 skill 不重复。

## Requirements

- WSL2 (Ubuntu 20.04+)
- Windows 10 or Windows 11
- Windows Python (Anaconda recommended)
- PowerShell

## First-Time Setup

```bash
cd ~/.openclaw/workspace/skillpublish/wsl-windows-bridge/scripts/
bash setup.sh
```

The setup script will:
1. Auto-detect your Windows Python location (supports `/mnt/d`, `/mnt/c`, `/mnt/e`)
2. Copy all wrappers to `~/.openclaw/bin/`
3. Generate `~/.openclaw/env.windows.sh` with correct paths
4. Set permissions and run verification

**Manual setup (without setup.sh):**
```bash
cp -r scripts/* ~/.openclaw/bin/
chmod +x ~/.openclaw/bin/win-*
# Then manually edit env.windows.sh to set correct paths
```

## Quick Start

### Basic Usage

**⚠️ exec non-interactive shell note:**
```bash
# Recommended for exec environment
source ~/.bashrc && source ~/.openclaw/env.windows.sh && win-python ...

# Or directly (wrappers handle .bashrc internally)
~/.openclaw/bin/win-python ...
```

### Common Scenarios

**Invoke Windows Python to run a script:**
```bash
source ~/.bashrc && source ~/.openclaw/env.windows.sh

# Single-line command
win-python -c "import xtquant; print(xtquant.__version__)"

# Run a script file
win-python "$WIN_SCRIPTS/my_task.py" --arg value
```

**Execute PowerShell:**
```bash
win-ps "Get-Process python | Select-Object Name,Id | Format-Table"
win-ps "Get-Service | Where-Object {\$_.DisplayName -like '*QMT*'}"
```

**File copy:**
```bash
win-copy /tmp/result.csv /mnt/d/app/output/result.csv
```

**Sync Windows-side data (credentials/config) that WSL can't see:**
```bash
# C:\Users\<user>\ 下的文件(可能是指向网盘等其他真实位置的软链接)
# 与 WSL 的 ~/ 是两套独立 HOME,不会自动同步。
# 当 WSL 内某工具报"未登录/未配置",但 Windows 侧确认已配置过时:
win-path /mnt/c/Users/<user>/.some-tool/config
mkdir -p ~/.some-tool
win-copy /mnt/c/Users/<user>/.some-tool/config ~/.some-tool/config
```
不要因为 WSL 侧读不到就判定环境不可用或要求用户重新粘贴密钥/token —— 先确认 Windows 侧是否已有,再同步过来。

**Path conversion:**
```bash
win-path /mnt/d/app
# → D:\app

win-path --to-wsl D:\app
# → /mnt/d/app
```

## Windows 宿主侧工作流（agent 在 Windows、项目在 WSL）

bridge 默认方向是「WSL 内 agent 调 Windows」；**反向拓扑**（agent 跑在 Windows 宿主、项目源码在 WSL 时的编译/启动/调试）见 [references/windows-host-side-workflow.md](references/windows-host-side-workflow.md)：Temp 副本编译（`go.mod RLock: Incorrect function`）、18080 端口、验证码 dev 放行、登录断言 HTTP 恒 200、Bash 调 PowerShell 拦截、Windows Python `/tmp` 路径坑。

### Quantitative Trading Example (QMT/xtquant)

```bash
source ~/.bashrc && source ~/.openclaw/env.windows.sh

# Get HS300 constituent stocks
win-python -c "
from xtquant import xtdata
stocks = xtdata.get_stock_list_in_sector('沪深300')
print(f'HS300: {len(stocks)} stocks')
print(stocks[:5])
"

# Download historical data
win-python -c "
from xtquant import xtdata
xtdata.download_history_data('600000.SH', start_time='20260101', end_time='20260405')
print('Download complete')
"
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WIN_ROOT` | `/mnt/d` | Windows root directory |
| `WIN_ANACONDA` | `/mnt/d/app/anaconda` | Anaconda installation path |
| `WIN_PYTHON` | `$WIN_ANACONDA/python.exe` | Python executable |
| `WIN_PS` | `.../powershell.exe` | PowerShell path |
| `WIN_SCRIPTS` | `/mnt/d/app/scripts` | Common scripts directory |

## Troubleshooting

| Error | Cause | Fix |
|-------|-------|-----|
| `command not found: win-python` | env.windows.sh not sourced | `source ~/.bashrc && source ~/.openclaw/env.windows.sh` |
| `Permission denied` | UAC permission | Use `D:\app\` or user directory as target |
| Chinese garbled logs | QMT log encoding | Ignore; actual data is correct |

## File Structure

```
~/.openclaw/workspace/skillpublish/wsl-windows-bridge/
├── SKILL.md
├── _meta.json
├── README.md
└── scripts/
    ├── setup.sh          ← Auto-install (auto-detects Python path)
    ├── env.windows.sh   ← Template (setup.sh generates actual config)
    ├── win-python
    ├── win-ps
    ├── win-cmd
    ├── win-copy
    ├── win-run-py
    └── win-path
```

## Maintenance

- **Author**: @DEACONHAN
- **Version**: 0.1.0 (draft)
- **Issues**: https://github.com/jarvis-agent/wsl-windows-bridge/issues
