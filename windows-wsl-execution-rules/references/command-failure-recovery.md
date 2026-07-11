# 跨环境命令失败恢复案例库

这份案例库承接 Windows、PowerShell、Git Bash、WSL 和 Linux 执行链路中已经验证的失败恢复经验。它不是错误日志仓库，也不是命令重试清单：只记录脱敏后的最小错误、可复现根因、最小修复和验证证据。

## 自动回写规则

- **回写时机**：普通命令、执行类命令、测试/验证脚本、`pre-commit` / `post-commit` gate 或回退检查失败后，修复成功并使用同一输入验证通过时，在当前任务收口前回写。
- **覆盖范围**：shell 解析、Windows/WSL 路径、工具缺失或误用、JSON 解析、编码/重定向、权限、依赖、gate 和验证脚本误报都进入同一恢复流程；不因“只是检查脚本失败”而跳过记录。
- **不回写条件**：根因未确认、修复未验证、仅有网络偶发抖动、只适用于一次性项目路径，或错误输出包含 secret、token、密码、连接串原值和业务数据。
- **去重方式**：先按“环境 + 失败症状 + 根因”检索；已有相同根因时合并验证命令和适用边界，不追加平行答案。
- **证据要求**：至少保留一个可复用的诊断动作和一个修复后的验证动作；只写退出码为 0 不算验证完成。
- **安全要求**：路径中的用户名、项目名、主机名和业务标识使用占位符；错误文本只保留定位根因所需的最小片段。
- **维护要求**：发现旧案例不再成立时，回写原案例的状态、适用范围和替代方案，不删除仍有历史价值的事实。

## 恢复路由

| 失败信号 | 先确认 | 最小恢复方向 | 不能直接做 |
| --- | --- | --- | --- |
| PowerShell 解析错误、`Unexpected token`、变量或重定向行为异常 | 当前命令是否混入 Bash/CMD 语法，是否存在嵌套引号 | 拆成变量或脚本；按 PowerShell 语法使用括号、`Join-Path`、`&`，必要时改回 Git Bash / WSL | 把同一条混合语法命令反复重试 |
| WSL 中 `permission denied`，或输出格式不像 Linux 工具 | `command -v <tool>` / `type <tool>` 是否命中 `/mnt/` 下的 Windows 可执行文件 | 优先使用 WSL 原生工具或等价工具，再验证实际路径 | 先 `chmod`、`sudo` 或关闭 `appendWindowsPath` |
| `wsl.exe` 找不到目录、项目文件找不到或路径参数被截断 | 当前命令是否在 Windows 侧使用 UNC，或在 WSL 侧使用 `/home/...`；工作目录是否正确 | Windows 侧通过 `wsl.exe --cd /home/<user>/<project>` 执行，普通读写使用 `//wsl.localhost/...`；不要混用 | 把 UNC 路径传给 WSL 内命令，或把 `/home/...` 当 Windows 文件引用 |
| `ConvertFrom-Json` / JSON 解析失败 | 原始 stdout 是否混入日志、警告或编码标记；JSON 是否被截断；PowerShell 序列化是否缺 `-Depth` | 分离 stdout/stderr，保存并回读原文；`ConvertTo-Json -Depth 10`；再解析纯 JSON | 直接删除异常字符或用正则“修 JSON” |
| 中文乱码、`锟斤拷`、`Ã` 或追加后部分内容异常 | 终端显示层还是文件字节层；当前 shell 是否使用默认编码 | 显式 UTF-8 读写，回读关键文件并检查 `git diff`；必要时联动 `windows-encoding-rules` | 继续在未确认编码的重定向或默认 `Out-File` 上追加 |
| 命令成功但验证结果不可信 | 退出码、输出、产物、工作目录和 local 配置是否都满足成功标准 | 用同一输入做结果校验，并确认没有切到 test/prod/staging | 只凭“没有报错”宣布成功 |

## 可复用记录模板

新增案例时使用以下字段；`状态` 只能写 `active`、`stale` 或 `deprecated`。

```markdown
### YYYY-MM-DD：<短标题>

- 环境：<Windows/PowerShell/Git Bash/WSL/Linux + agent 运行侧>
- 失败信号：`<最小脱敏错误文本>`
- 触发命令类别：<普通仓库命令/执行类命令/编码 I/O/JSON/依赖安装>
- 根因：<由什么诊断证据确认>
- 修复：<最小替代命令或执行路径>
- 验证：<使用什么同输入检查证明恢复>
- 适用边界：<何时适用，何时转交相邻 skill>
- 状态：active
```

## 已验证案例

### 2026-07-12：PowerShell 默认读取导致 UTF-8 中文显示为乱码

- 环境：Windows PowerShell，读取 UTF-8 仓库规则文件
- 失败信号：`Get-Content -Raw` 返回的中文出现 mojibake，英文和 Markdown 结构仍可见
- 触发命令类别：规则文件读取 / 编码 I/O
- 根因：读取入口依赖当前 PowerShell 会话的默认编码，而不是显式按 UTF-8 解码
- 修复：使用 `Get-Content -Encoding UTF8`，或使用 `[IO.File]::ReadAllText($path, [Text.UTF8Encoding]::new($false))` 明确指定 UTF-8
- 验证：显式 UTF-8 回读文件，中文恢复可读；随后检查关键文件字节和 `git diff`，确认没有产生写入污染
- 适用边界：只解决文件编码读取问题；如果文件字节本身已被错误编码写入，先按 `windows-encoding-rules` 的失败回滚与转码流程处理
- 状态：active

### 2026-07-12：PowerShell 哈希值误传给 `BitConverter`

- 环境：Windows PowerShell，执行关键文件的 MD5 校验
- 失败信号：`Cannot convert argument "value" ... to type "System.Byte[]"`
- 触发命令类别：规则文件验证 / PowerShell 对象处理
- 根因：`Get-FileHash` 返回对象的 `.Hash` 属性已经是十六进制字符串，不是可直接传给 `BitConverter.ToString` 的字节数组
- 修复：直接输出 `(Get-FileHash $path -Algorithm MD5).Hash`；只有手里确实是字节数组时才使用 `BitConverter.ToString`
- 验证：直接读取三个目标文件的哈希字符串并完成 UTF-8 内容检查，命令退出码为 0
- 适用边界：只适用于 PowerShell 的 `Get-FileHash` 对象；不要把该写法推广到任意哈希库的返回值
- 状态：active

### 2026-07-12：WSL gate 脚本依赖的 `rg` 未安装

- 环境：Windows agent 通过 WSL 执行 Git pre-commit gate
- 失败信号：`rg: command not found`，脚本后续标题校验因此返回误导性的失败结果
- 触发命令类别：提交前检查 / WSL 工具依赖
- 根因：WSL 环境中没有 Linux 原生 `rg`，但 gate 脚本把 `rg` 作为必需命令使用；`command -v rg` 无输出，`command -v grep` 命中 `/usr/bin/grep`
- 修复：优先在 WSL 原生安装 `ripgrep`；当前无法安装时，按 gate 的等价回退规则用现有 shell 工具完成标题、README、staged diff、域隔离和禁放扫描，并明确记录为回退检查
- 验证：确认 `grep` 与 `git` 可用，回退检查通过后继续提交；不要把 gate 的依赖错误当成标题或代码错误
- 适用边界：只适用于 WSL 工具缺失；如果 `command -v rg` 命中 `/mnt/` 下的 Windows 版工具，应转到工具 interop 案例，不要直接安装或修改 PATH
- 状态：active

### 2026-07-12：把 Windows 路径传给了 WSL bash

- 环境：Windows agent，`bash` 实际解析为 `C:\Windows\System32\bash.exe` 对应的 WSL 入口
- 失败信号：`/bin/bash: F:/.../pre_commit_gate.sh: No such file or directory`
- 触发命令类别：提交前检查 / 跨 shell 脚本调用
- 根因：当前不是 Git Bash；`F:/...` 不是该 WSL bash 的 Linux 路径，Git Bash 的 `/f/...` 也不能直接套用到 WSL
- 修复：先用 `Get-Command bash` 或 `where.exe bash` 确认 shell 来源；实际使用 WSL 时改为 `wsl.exe --cd /mnt/c/<repo> bash /mnt/f/<script>`，只有确认是 Git Bash 时才使用 `/f/<script>`
- 验证：确认脚本路径和仓库工作目录分别能在 WSL 中访问，再重跑 gate；路径转换后若出现新的工具依赖错误，按工具来源继续诊断
- 适用边界：只适用于 Windows、Git Bash 与 WSL 的路径语境混淆；不要把 `/mnt/f/...` 当作面向 Windows 用户展示的项目文件引用
- 状态：active

### 2026-07-12：WSL 执行 CRLF shell gate 脚本失败

- 环境：Windows agent 通过 WSL 执行 `post_commit_gate.sh`
- 失败信号：`set: pipefail\r: invalid option name`
- 触发命令类别：提交后检查 / shell 脚本执行
- 根因：shell 脚本物理行尾为 CRLF，WSL 将回车符拼进 `pipefail` 参数；这不是脚本逻辑本身失败
- 修复：shell 脚本统一保存为 UTF-8 + LF 后再执行；如果当前 gate 不能立即转换，按 post gate 的等价规则检查最新提交标题和正文是否含字面量 `\\n`
- 验证：检查脚本无 CRLF 后重新执行，或完成等价 post-check，并确认 `git status --short` 为空
- 适用边界：只适用于 Linux/WSL 执行的 shell 脚本；PowerShell、Windows 原生工具和文档文件按各自编码/换行规则处理
- 状态：active

## 回写前检查

- [ ] 已记录 shell、agent 侧、工作目录和退出码
- [ ] 已脱敏路径、用户标识、主机名、业务数据和凭据
- [ ] 已完成根因诊断，不是只记录表面错误
- [ ] 已用同一输入验证修复结果和运行环境
- [ ] 已检索并合并相同根因的旧案例
- [ ] 已明确适用边界和相邻 skill 的责任边界
