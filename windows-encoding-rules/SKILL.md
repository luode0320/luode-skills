---
name: windows-encoding-rules
description: 当任务运行在 Windows（PowerShell 或 CMD）且涉及中文读写、日志追加、README/Markdown 修改、脚本输出重定向、Git 提交信息或终端显示时触发。用于预防与修复中文乱码（mojibake）、统一 UTF-8 写入策略，并在落盘前做编码自检；尤其适用于“看到乱码”“中文变成问号/锟斤拷/Ãxx”“同文件中英正常但中文异常”“追加写入后部分行乱码”等场景。
---

# Windows 中文编码防护规则

只在“Windows 环境 + 中文文本 + 文件/终端 I/O”问题上使用本 skill。  
它负责提前提醒、统一写入方式、落盘后验证，不替代业务逻辑实现。

## 自动触发信号

- 用户提到 `Windows`、`PowerShell`、`CMD`、`终端乱码`、`中文乱码`、`编码问题`。
- 用户提到 `Git Bash`、`WSL`、`\\wsl.localhost`，或者明确希望在 Windows 下建立默认执行约束，避免 Windows PowerShell 直接写入导致换行/编码漂移。
- 用户提到“明明没改文件却进了 git diff”“很多文件被带进改动”“`.sh` 只有 mode change”“`LF/CRLF` 被自动转换”“PowerShell 读过就脏了”这类跨平台改动污染。
- 修改 `README.md`、`*.md`、`*.txt`、`*.json`、`*.yaml`、`*.ps1` 且包含中文。
- 需要用命令行追加文本（`Add-Content`、`Out-File`、`>`、`>>`）且内容含中文。
- 需要输出/拼接 Git 提交信息，或把中文日志落盘。
- 运行 Python、Node、Go 等脚本读取含中文文件，且脚本没有显式声明 `encoding="utf-8"`。
- 已出现乱码现象：问号、`锟斤拷`、`Ã` 前缀、同文件中文异常但英文正常。

## 进入后先做什么

1. 先判定“乱码是在终端显示层，还是文件实际字节层”。
2. 先读取原文件并确认是否已 UTF-8（必要时用 `Format-Hex` 抽样检查）。
3. 写入时强制显式指定编码，禁止依赖默认编码。
4. 写入后立刻复读验证；若异常，先回滚本次写入再重试。
5. 如果当前运行在 Windows 下，必须通过 WSL 执行项目命令（`wsl.exe -e bash -lc "..."`），禁止用 PowerShell 或 Git Bash 直接运行项目命令；涉及写文件操作时必须显式指定 UTF-8 编码。
6. 先检查仓库是否缺少 `.gitattributes` / `.editorconfig`，以及 Git 是否开启了 `core.autocrlf=true` 或 `core.filemode=true`。

## Windows 防错基线

- 控制台显示前先执行：
```powershell
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
```
- 读写文件统一使用显式编码，推荐：
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
- 禁止直接使用 `>`、`>>` 追加中文关键内容（除非已明确编码策略并验证）。
- 对关键文档（如 `README.md`）优先“整段替换/精确替换”，少用盲目追加。
- 每次中文写入后都执行“回读核对 + Git diff 核对”。
- 对 Windows 下的仓库写入前，优先确认当前 shell 是否为 Git Bash/WSL；如果必须用 PowerShell，写入命令必须显式 UTF-8 且落盘后核对换行是否被转换。
- 默认建议仓库提交 `.gitattributes` 与 `.editorconfig`，显式固定 `LF`、`UTF-8`、末尾换行和基础编辑器行为。
- 对已有历史仓库，`.gitattributes` 默认先采用“最小约束”策略：先用 `* text=auto`，对 `*.sh` / `*.bash` 这类明确必须 `LF` 的脚本，以及 CI / 工作流 / 配置类文件 `*.yml` / `*.yaml` 显式强制 `eol=lf`；不要一上来对 `*.go`、`*.vue`、`*.sql`、`*.md` 全量强制 `eol=lf`，否则容易触发整仓重规范化。
- Windows 下若 Git 出现 `.sh` 文件仅有 `100755 => 100644` 之类 mode change，优先检查并关闭仓库级与全局 `core.filemode`。
- Windows 下若 Git 出现大量 `LF will be replaced by CRLF`，优先检查并关闭仓库级与全局 `core.autocrlf`，同时为仓库补齐 `.gitattributes`。

## 推荐执行流程

1. 编码预设：设置 `OutputEncoding` 为 UTF-8。
2. 读取验证：读取目标文件，确认当前文本可正常显示中文。
3. 显式写入：使用带 `-Encoding UTF8` 的写入命令。
4. 落盘复核：`Get-Content` 回读尾部 + `git diff` 检查仅预期行变化。
5. 失败回滚：若出现乱码，撤销本次修改并改用更稳妥写法重做。
6. 如果已出现批量伪改动：先补“最小约束版”`.gitattributes` / `.editorconfig`，再修 Git 配置（`core.autocrlf=false`、`core.eol=lf`、`core.safecrlf=warn`、`core.filemode=false`），最后清理 mode change 和混合换行文件。

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
- 驳回：依赖默认编码写入、写后未验证、发现乱码仍继续后续流程。

## 边界

- 本 skill 只处理编码稳定性，不处理业务需求正确性。
- 若是编辑器字体或 UI 渲染问题，记录为“显示层问题”，不要误判为文件损坏。
