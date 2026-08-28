---
name: "shell"
description: "Shell scripting reference — Bash syntax, redirections, process substitution, signal handling, debugging techniques. 编写、调试 Bash 脚本、排查 shell 行为、自动化系统任务时使用。触发词：shell、bash、shell 脚本、bash 脚本、sh 脚本、脚本报错、管道、重定向、trap、退出码。"
license: MIT
metadata:
  displayName: "Shell 脚本参考"
  version: "1.1.0"
  author: "BytesAgain"
  homepage: "https://bytesagain.com"
  source: "https://github.com/bytesagain/ai-skills"
  tags: [shell, bash, scripting, linux, unix, terminal, automation, devtools]
  category: "devtools"
  env:
    requires: [bash]
    check: "command -v bash && bash --version | head -1"
---

# Shell — Shell 脚本参考

Bash 脚本编写与调试的完整参考：语法、陷阱、重定向、信号处理与工具模式。
速查表直接内联在本文档，全文手册由 `scripts/script.sh` 提供。

## 使用流程

遇到 shell/bash 任务时按以下 4 步执行：

1. **识别场景**：判断任务属于哪一类——
   - 写新脚本 / 补错误处理 → 查「核心陷阱速查」+ 调 `safety` 模块
   - 脚本报错 / 行为异常 → 查「调试检查点」，定位引用、子壳、退出码问题
   - 选工具做文本处理 → 查「工具速查」，确认 grep/sed/awk/jq 的对应模式
   - 处理后台进程 / 信号 / 清理 → 查「信号与清理」
2. **查速查表**：本文档「核心陷阱速查」覆盖 8 大高频坑点，先在此定位问题与修复对。
3. **取全文**：需要完整语法或更多示例时，从 skill 根目录运行 `scripts/script.sh <command>`（命令表见下），输出即对应主题手册。
4. **验收**（分两阶段核对）：
   - 写前：列出目标命令与预期退出码，确认无未加引号变量、无 `cd` 裸调用、临时文件已规划 `mktemp + trap`
   - 写后：`bash -n` 语法检查通过 → 真实执行验证 → 逐项过「调试检查点」清单 → 有 shellcheck 则清零警告

## 场景边界

**使用本 skill**：
- 编写或重构 Bash 脚本（含错误处理、信号清理、参数校验）
- 排查 shell 报错：引用错误、词分割、子壳变量丢失、退出码误判
- 系统管理自动化：文件操作、权限、进程、定时任务
- 文本处理管道：grep / sed / awk / find / xargs / jq 组合

**不使用本 skill**：
- 跨平台交付（需 Windows + Unix 双端运行）→ 改用 Python / Go
- 复杂数据结构或 JSON 深度处理 → 用 Python（`jq` 只够简单场景）
- 超过约 200 行的业务逻辑 → 脚本会失控，改用 Python / Go
- Windows 原生 PowerShell 场景 → 见 `powershell__skillhub`

## 核心陷阱速查

### 1. 引用与词分割

| 问题 | 反例 | 修复 |
|---|---|---|
| 变量未加引号，含空格/通配符时碎裂 | `rm $file` | `rm "$file"` |
| `$(ls)` 拆行导致文件名错乱 | `for f in $(ls)` | `for f in *` |
| 命令替换未加引号 | `echo $(date)` | `echo "$(date)"` |

### 2. set -euo pipefail 三件套

```bash
set -euo pipefail   # 脚本顶部必加：首错即退 + 未定义变量报错 + 管道任一段失败即失败
```

- `set -e` 的合法例外：`cmd || true`、`if cmd; then ...`、`cmd || handle_error`
- `set -u` 可捕获变量名拼写错误
- `set -o pipefail` 防止 `cmd1 | cmd2` 只看到最后一段的退出码

### 3. 子壳陷阱（变量丢失）

| 场景 | 反例 | 修复 |
|---|---|---|
| 管道子壳 | `cat f \| while read ...` 循环内赋值外部丢失 | `while read ... < file` |
| 圆括号子壳 | `( count=5 )` 括号内赋值不持久 | `{ count=5; }` 用花括号（同壳） |
| 进程替换 | `while read ... < <(cmd)` 可跨子壳保留变量 | 同上，避免管道 |

### 4. 数组

```bash
arr=("one" "two")        # 声明
"${arr[@]}"              # 全部元素（保留边界，必须引号）
"${arr[*]}"              # 合并成单字符串（有分隔副作用）
"${#arr[@]}"             # 长度（不是 ${#arr}）
"${!arr[@]}"             # 所有索引
arr+=("three")           # 追加
```

### 5. 参数展开

```bash
"${var:-default}"   # 未设或空 → 用默认值（不改 var）
"${var:=default}"   # 未设或空 → 赋默认值并返回
"${var:?err}"       # 未设或空 → 报错退出（函数必填参数首选）
"${var:+alt}"       # 已设 → 用 alt
"${#var}"           # 字符串长度
"${var#p}" / "${var##p}"   # 去最短/最长前缀
"${var%p}" / "${var%%p}"   # 去最短/最长后缀
"${var//old/new}"   # 全部替换
```

### 6. 信号与清理

```bash
trap 'rm -f "$tmpfile"' EXIT      # 任何退出路径都清理
trap 'exit 130' INT               # Ctrl+C
kill -9  # SIGKILL 不可捕获，最后手段；先 SIGTERM（默认 kill 行为）
```

- 常见信号：SIGINT=2（Ctrl+C）、SIGTERM=15（kill 默认，可捕获优雅退出）、SIGKILL=9（不可捕获）、SIGSTOP=19（不可捕获）
- 后台任务：`cmd &` → `wait $pid` 收尾；`jobs` / `fg %1` / `bg %1` / `disown %1`
- 脱离终端：`nohup cmd &`（输出落 nohup.out）或 `cmd & disown` / `setsid cmd`

### 7. 退出码

| 码 | 含义 |
|---|---|
| 0 | 成功 |
| 1 | 通用错误 |
| 2 | 命令误用 |
| 126 | 找到但不可执行 |
| 127 | 命令不存在 |
| 128+N | 被信号 N 杀死（130=Ctrl+C，143=SIGTERM） |

标准错误处理：`die() { echo "ERROR: $*" >&2; exit 1; }`，临时文件用 `tmpfile=$(mktemp) || die "mktemp failed"`，依赖检查 `command -v jq &>/dev/null || die "jq is required"`。

### 8. 工具速查

| 工具 | 高频模式 |
|---|---|
| grep | `grep -rn "pat" dir/`；`-i` 忽略大小写；`-v` 反选；`-l` 只列文件；`-o` 只取匹配；`-P` Perl 正则 |
| sed | `sed -i 's/old/new/g' file` 原地替换；`sed -n '5,10p'` 打印区间；`sed '/pat/d'` 删行 |
| awk | `awk -F: '{print $1}' file` 按分隔符取字段；`awk '{sum+=$1} END{print sum}'` 求和；`awk '!seen[$0]++'` 去重保序 |
| find | `find . -name "*.log" -mtime -7`；`-size +100M`；`-exec ... {} \;`；危险操作先 `-print` 预览 |
| xargs | `find ... -print0 \| xargs -0 rm` 处理空格路径；`-P 4` 并行；`-I {}` 占位 |
| jq | `jq '.name'`；`jq -r` 去引号；`jq '.items \| length'`；`jq 'select(.age > 30)'` |

**何时不用 shell**：复杂数据结构（超出数组）、健壮错误处理、数学密集、JSON/XML 深度处理、>200 行、跨平台——改用 Python 或 Go。

## 命令参考

全文手册由脚本按主题输出。**断链规避**，两种方式任选：

方式 A（推荐，进入 skill 根后相对路径）：
```bash
cd <skill根目录>/shell__skillhub   # 例如本仓库: cd /d/谷歌云盘/luode-skills/shell__skillhub
bash scripts/script.sh <command>
```

方式 B（任意 cwd 可用，脚本已内置 `SCRIPT_DIR` 自定位）：
```bash
bash <skill根目录>/shell__skillhub/scripts/script.sh <command>
```

| command | 主题 |
|---|---|
| `intro` | Bash 概览、shebang、退出码、何时用 shell |
| `variables` | 变量、数组、参数展开、特殊变量 |
| `control` | if/case/for/while、函数、测试操作符 |
| `redirections` | 管道、heredoc、进程替换、文件描述符 |
| `safety` | set -euo pipefail、引用、ShellCheck、错误处理 |
| `tools` | grep、sed、awk、find、xargs、jq 模式 |
| `signals` | trap、清理、后台任务、并行执行 |
| `checklist` | 脚本质量检查清单（含输入校验与可移植性） |
| `help` / `version` | 帮助与版本 |

## 环境自检

```bash
command -v bash && bash --version | head -1
```

- 无 `bash` 时按以下顺序降级：① SKILL.md 内联速查不依赖运行环境，仍可直接参考；② 纯文本/管道任务改用 Python 或 Go 等价实现；③ Windows 原生场景改用 `powershell__skillhub`；④ 需要真实 bash 时安装 Git Bash / WSL / MSYS2 之一再回来执行

## 调试检查点

脚本出问题时按序核对：

- [ ] 变量全部加引号（`"$var"`），glob/算术除外
- [ ] `set -euo pipefail` 置顶且没有破坏预期（`|| true` 显式豁免）
- [ ] 管道/圆括号没有吞掉循环内赋值（子壳陷阱）
- [ ] `cd` 后跟 `|| exit 1` 或 `|| die`（cd 可能失败）
- [ ] 临时文件用 `mktemp` 且注册 `trap ... EXIT` 清理
- [ ] 退出码按上表语义解读，`$?` 紧跟在目标命令后读取
- [ ] `command -v` 前置检查外部依赖（jq、curl 等）
- [ ] 语法检查 `bash -n script.sh` 通过后再真实执行
- [ ] 有 shellcheck 时运行 `shellcheck script.sh` 清零警告

## 相关技能

| 技能 | 职责边界 | 与本 skill 的关系 |
|---|---|---|
| `bash__skillhub` | Bash 陷阱浓缩速查（引用/展开/数组/子壳） | 高频坑点极简版，先查它再回本 skill 取全文 |
| `linux__skillhub` | Linux 系统运维陷阱（权限/进程/SSH/systemd/cron） | 系统管理上下文，与本 skill 脚本编写互补 |
| `powershell__skillhub` | Windows PowerShell 脚本 | 跨平台需求时替代本 skill 的对应场景 |

---

*Powered by BytesAgain | bytesagain.com*
