---
name: windows-encoding-rules
description: 当任务运行在 Windows（Git Bash / bash、PowerShell 或 CMD）且涉及任意代码、文档、配置、脚本、测试资产或生成文本的读写、日志追加、README/Markdown 修改、脚本输出重定向、Git 提交信息或终端显示时触发。用于预防与修复中文乱码（mojibake）、统一跨平台 UTF-8 写入策略，并在落盘前做编码自检；尤其适用于“看到乱码”“中文变成问号/锟斤拷/Ãxx”“同文件中英正常但中文异常”“追加写入后部分行乱码”“担心文件被 GBK/ANSI/默认编码写入”等场景。
---

# Windows 中文编码防护规则

只在“Windows 环境 + 中文文本 + 文件/终端 I/O”问题上使用本 skill。  
它负责提前提醒、统一写入方式、落盘后验证，不替代业务逻辑实现。

## 自动触发信号

- 用户提到 `Windows`、`Git Bash`、`bash`、`PowerShell`、`CMD`、`终端乱码`、`中文乱码`、`编码问题`。
- 用户提到 `WSL`、`\\wsl.localhost`，或者明确希望在 Windows 下建立默认执行约束，避免 Windows 终端编码、换行或 shell 默认编码导致漂移。
- 用户提到“明明没改文件却进了 git diff”“很多文件被带进改动”“`.sh` 只有 mode change”“`LF/CRLF` 被自动转换”“PowerShell 读过就脏了”这类跨平台改动污染。
- 修改 `README.md`、`*.md`、`*.txt`、`*.json`、`*.yaml`、`*.ps1`、代码文件、脚本文件、规则文件、测试资产或生成文本文件。
- 需要用命令行写入或追加文本（`Set-Content`、`Add-Content`、`Out-File`、`>`、`>>`），无论内容是否包含中文，都必须先明确 UTF-8 写入策略。
- 需要输出/拼接 Git 提交信息，或把中文日志落盘。
- 运行 Python、Node、Go 等脚本读取含中文文件，且脚本没有显式声明 `encoding="utf-8"`。
- 已出现乱码现象：问号、`锟斤拷`、`Ã` 前缀、同文件中文异常但英文正常。

## 进入后先做什么

1. 先判定“乱码是在终端显示层，还是文件实际字节层”。
2. 先读取原文件并确认是否已 UTF-8（必要时用 `Format-Hex` 抽样检查）。
3. 写入时强制显式指定 UTF-8，禁止依赖 GBK、ANSI、系统默认编码、编辑器默认编码或 shell 默认编码。
4. 写入后立刻复读验证；若异常，先回滚本次写入再重试。
5. 如果当前运行在 Windows 下，普通仓库命令默认优先使用 Git Bash / bash；PowerShell 只在 `.ps1`、Windows 专用 cmdlet、PowerShell profile / 编码初始化或用户明确要求时使用。
6. 若确实需要使用 PowerShell，先检查当前 PowerShell 会话与用户级 PowerShell 配置是否已经固定为 UTF-8；未固定时，优先执行 `scripts/enable_powershell_utf8.ps1` 完成永久化初始化，再继续 PowerShell 专项命令。
7. Git Bash / bash、PowerShell、Python、Node、Go 等任何写文件入口都必须显式指定或保证 UTF-8，并在落盘后核对换行是否被转换。
8. 先检查仓库是否缺少 `.gitattributes` / `.editorconfig`，以及 Git 是否开启了 `core.autocrlf=true` 或 `core.filemode=true`。

## Windows 防错基线

- 普通仓库命令优先使用 Git Bash / bash，并让 Git 与脚本工具遵守 UTF-8 / 换行约束：
```bash
export LANG=C.UTF-8
export LC_ALL=C.UTF-8
git config --get core.autocrlf
git config --get core.filemode
```

- 只有在 PowerShell 专项场景中，控制台显示前先执行：
```powershell
[Console]::InputEncoding  = [System.Text.UTF8Encoding]::new($false)
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
$OutputEncoding = [System.Text.UTF8Encoding]::new($false)
```
- 若要把当前用户 PowerShell 永久切到 UTF-8，仅在 PowerShell 专项场景中执行：
```powershell
powershell -ExecutionPolicy Bypass -File .\windows-encoding-rules\scripts\enable_powershell_utf8.ps1
```
- 永久化脚本会同时补齐 Windows PowerShell 5.1 与 PowerShell 7 的用户级 profile，并写入 UTF-8 初始化片段；脚本未执行成功时，不得使用 PowerShell 执行需要稳定中文 I/O 的专项命令。
- 永久化脚本还应确保当前用户的 PowerShell 执行策略至少允许本地 profile 加载；若 profile 文件已落盘但新会话仍因 execution policy 被拦截，则视为脚本仍未完成闭环。
- 脚本执行完成后，应继续用新的 PowerShell 子进程验证 `[Console]::InputEncoding`、`[Console]::OutputEncoding`、`$OutputEncoding` 与 `chcp` 是否都已经切到 UTF-8；只有验证通过，才算满足 PowerShell 专项命令前提。
- 读写文件统一使用显式 UTF-8 编码，推荐：
```powershell
Get-Content -Encoding UTF8 <path>
Set-Content -Encoding UTF8 <path> <content>
Add-Content -Encoding UTF8 <path> <content>
Out-File -Encoding utf8 <path>
```
- 运行 Python 脚本处理中文文件时，优先设置：
```powershell
$env:PYTHONUTF8 = "1"
```
- Windows PowerShell 5.1 中，若需要用 `Invoke-WebRequest`、`Invoke-RestMethod`、`iwr`、`irm` 下载文件、拉取远端文本、请求 API 或执行远端安装脚本，默认先执行：
```powershell
$PSDefaultParameterValues['Invoke-WebRequest:UseBasicParsing'] = $true
$PSDefaultParameterValues['Invoke-RestMethod:UseBasicParsing'] = $true
```
- 单次命令也可显式附带 `-UseBasicParsing`；凡是无人值守脚本，默认必须启用，避免弹出“是否继续执行 / 使用 IE 解析”的人工确认框。
- 若只是下载文件到本地，优先使用 `curl.exe` 替代 PowerShell Web Cmdlet，以减少交互提示。
- 禁止直接使用 `>`、`>>` 写入代码、文档、配置、脚本、规则文件、中文关键内容或生成文本（除非已明确当前 shell 的 UTF-8 策略并完成落盘验证）。
- 禁止把 GBK、ANSI 或系统默认编码作为仓库文件写入格式；发现文件已被这些编码污染时，先转回 UTF-8，再继续业务修改。
- 对关键文档（如 `README.md`）优先“整段替换/精确替换”，少用盲目追加。
- 每次中文写入后都执行“回读核对 + Git diff 核对”。
- 对 Windows 下的仓库写入前，优先使用 Git Bash / bash 或显式 UTF-8 的脚本语言入口；若必须使用 PowerShell，则先确认当前 PowerShell 会话是否已完成 UTF-8 初始化。未完成且又无法先运行永久化脚本时，记录为环境阻断，不要直接用未初始化的 PowerShell 写仓库文件。
- 默认建议仓库提交 `.gitattributes` 与 `.editorconfig`，显式固定 `LF`、`UTF-8`、末尾换行和基础编辑器行为。
- 对已有历史仓库，`.gitattributes` 默认先采用“最小约束”策略：先用 `* text=auto`，对 `*.sh` / `*.bash` 这类明确必须 `LF` 的脚本，以及 CI / 工作流 / 配置类文件 `*.yml` / `*.yaml` 显式强制 `eol=lf`；不要一上来对 `*.go`、`*.vue`、`*.sql`、`*.md` 全量强制 `eol=lf`，否则容易触发整仓重规范化。
- Windows 下若 Git 出现 `.sh` 文件仅有 `100755 => 100644` 之类 mode change，优先检查并关闭仓库级与全局 `core.filemode`。
- Windows 下若 Git 出现大量 `LF will be replaced by CRLF`，优先检查并关闭仓库级与全局 `core.autocrlf`，同时为仓库补齐 `.gitattributes`。

## 推荐执行流程

1. 编码前提：Windows 下普通仓库命令优先使用 Git Bash / bash；PowerShell 仅在专项场景中使用，并先完成 `scripts/enable_powershell_utf8.ps1` 与新子进程 UTF-8 验证。
2. 会话预设：Git Bash / bash 确认 `LANG` / `LC_ALL` 为 UTF-8；PowerShell 专项场景设置 `InputEncoding`、`OutputEncoding` 与 `$OutputEncoding` 为 UTF-8。
3. 读取验证：读取目标文件，确认当前文本可正常显示中文。
4. 显式写入：使用带 `-Encoding UTF8` 的写入命令；脚本语言读写文件时也必须显式声明 UTF-8 或启用 UTF-8 运行模式。
5. 落盘复核：`Get-Content` 回读尾部 + `git diff` 检查仅预期行变化。
6. 失败回滚：若出现乱码，撤销本次修改并改用更稳妥写法重做。
7. 如果已出现批量伪改动：先补“最小约束版”`.gitattributes` / `.editorconfig`，再修 Git 配置（`core.autocrlf=false`、`core.eol=lf`、`core.safecrlf=warn`、`core.filemode=false`），最后清理 mode change 和混合换行文件。

## 落盘命令模板

追加单行（中文）：
```powershell
Add-Content -Encoding UTF8 -Path README.md -Value "2026-05-11 12:00:00 docs: [示例] 补充说明"
```

多行写入（中文）：
```powershell
@"
第一行中文
第二行中文
"@ | Out-File -Encoding utf8 -Append README.md
```

验证：
```powershell
Get-Content -Encoding UTF8 README.md -Tail 5
git diff -- README.md
```

## 通过 / 驳回标准

- 通过：中文在终端可读、文件回读正常、`git diff` 无异常乱码片段。
- 通过：仓库存在 `.gitattributes` / `.editorconfig`，Windows 下默认配置不会再把无关文件批量带进改动，`*.sh` / `*.bash` / `*.yml` / `*.yaml` 等需稳定 `LF` 的文件类型有明确换行约束，脚本文件也不再因 mode change 反复脏掉。
- 驳回：依赖默认编码写入、使用 GBK / ANSI / 系统默认编码落盘、写后未验证、发现乱码仍继续后续流程。

## 边界

- 本 skill 只处理编码稳定性，不处理业务需求正确性。
- 若是编辑器字体或 UI 渲染问题，记录为“显示层问题”，不要误判为文件损坏。
