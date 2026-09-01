---
name: github-release-pipeline
description: 通用 GitHub Actions 手动发布流水线（workflow_dispatch 驱动）。当任何仓库需要走「bump 版本 → commit/push → dispatch CI → 轮询 run → 下载 release assets → git add 资产 → 运行 registry/发布脚本 → 远端 raw URL 验证 → 二进制级产物验证」的发版链路（用户说"发布/发版"）时使用。沉淀了 GitHub API 层与 Actions 层的通用陷阱：dispatch 422（choice 枚举）、runs API 判重（display_title 恒为 Build）、head_sha 40 位、TLS 通道选择（PowerShell vs curl）、raw URL CDN 延迟、git add 顺序、二进制验证。不含任何项目特定事实（路径/仓库名/脚本名），项目专属版见对应项目的 cpa-plugin-release 类技能。

---

# GitHub Actions 手动发布流水线（通用）

> 用于 `workflow_dispatch` 驱动的 GitHub Release 发版。**本 skill 只含 GitHub/CI 层通用知识**；项目特定事实（仓库名、版本文件位置、provider/模块 id 映射、脚本路径、registry 结构）由各项目级技能提供，引用本 skill 的通用步骤。

## 通用步骤（不可跳步）

### 1. 前置检查
```bash
git status --short && git branch --show-current
git log --oneline -3
```
- 工作树若有与本次发布无关的改动，**不要混入发布 commit**，只 `git add` 发布相关文件。

### 2. bump 版本
- 版本声明若有多处（如 `VERSION` 文件 + 源码 `var version`），**必须全部同步**，漏一处会导致产物版本与 registry 不一致。

### 3. commit + push
- commit message 写清改动根因与验证结论；push 后 `git rev-parse HEAD` 拿**完整 40 位** sha 备用。

### 4. dispatch CI（workflow_dispatch）
```powershell
$token = (Get-Content -Raw "<pat 文件路径>").Trim()
[Net.ServicePointManager]::SecurityProtocol = 3072
$body = '{"ref":"<分支>","inputs":{<inputs 按工作流定义>}}'
$headers = @{ Authorization = "Bearer $token"; "User-Agent" = "wb-release"; "Accept" = "application/vnd.github+json" }
Invoke-RestMethod -Method Post -Uri "https://api.github.com/repos/<owner>/<repo>/actions/workflows/<workflow.yml>/dispatches" -Headers $headers -Body $body -ContentType "application/json" -TimeoutSec 30
```
通用陷阱：
- **`inputs` 的值必须匹配工作流声明的枚举**：`type: choice` 的 input 传了不在 options 里的值 → **HTTP 422 且响应体为空**（两条通道都拿不到 body，别误判为 token 问题）。先读 `.github/workflows/*.yml` 的 `workflow_dispatch.inputs` 定义再构造 body。
- **优先 PowerShell 通道**：curl/urllib 对 api.github.com 的 TLS 握手间歇性失败（schannel UNEXPECTED_EOF / SSL EOF）；curl 还可能出现 403「无权访问 vip 分组」这类**代理层误报**——不是 GitHub 真错，别据此改参数。
- dispatch 成功是 204 无 body，`Invoke-RestMethod` 不抛错即为成功。

### 5. 轮询 run
- **head_sha 必须传完整 40 位**，截断会让 runs API 静默返回 0 条。
- runs API 的 `name`/`display_title` **恒为工作流名（如 'Build'）**，**判重/定位不能用 name**，用 `head_sha + created_at + run 数量`。
- 单个 run：`GET /actions/runs/{run_id}`，直到 `status=completed`。
- **轮询上限按 15 分钟设计**：正常 1-2 分钟，但实测出现过 12-13 分钟（in_progress → queued 6 分钟 → in_progress），勿按旧经验提前判超时。
- **PowerShell 后台轮询任务的 timeout 参数就是硬上限**（到点强杀、输出以当时进度为准）：长轮询拆成多段（每段 ≤ 轮询循环自然结束），前段把 run id 落盘文件供后段复用。字符串插值注意 `$i:` 会被解析为作用域变量，写 `${i}:`。
- 若误触发了重复 run：`POST /actions/runs/{id}/cancel`（异步生效，最终 completed cancelled），判重教训同上。

### 6. 下载资产 → 先 git add → 再发布
- 下载脚本若走 urllib/curl 可能遇到 release 下载 URL（objects.githubusercontent.com 重定向）连接超时（如 WinError 10060）且重试耗尽——**备用通道：PowerShell `Invoke-WebRequest -OutFile` 逐文件下载 `releases/download/<tag>/<name>` + 本地按 checksums.txt 逐文件比对 sha256**。PS 5.1 先设 `$ProgressPreference='SilentlyContinue'` 降噪，输出看最终逐文件 OK 行。
- **release 资产传播非原子**：CI success 后立即下载，可能部分平台 OK、部分连续 FAIL（如 darwin/freebsd 挂而 linux/windows 秒下）——这是资产 objects 传播延迟，**等待后重试即可（通常一两轮内全过），勿误判为 release 缺失**。下载循环内建 4-6 次重试 + 每次间隔 5-10s。
- 下载后先校验 checksums，全部 OK 再：
```bash
git add <assets 目录> && git commit -m "chore: 添加 <id> <version> 发布资产" && git push origin <分支>
```
- **必须先 add assets + push，再跑修改 manifest/registry 的发布脚本**——否则发布脚本指向的 raw URL 会指向不存在的文件。
- **并行会话撞车检查**：同一仓库可能被多个 AI 会话/终端同时操作（工作树共享）。每次 git add/commit 前先 `git fetch && git log origin/main --oneline -3` 对齐；若 commit 报 "nothing added to commit" 但文件确实该提交，先 `git log --oneline -3` 查是否已有并行会话以同模板提交过——核对内容一致即可直接复用，勿重复提交。

### 7. 更新 manifest/registry
- 跑项目发布脚本（如 publish-assets.py / 版本清单工具）→ 校验脚本（validate）→ commit + push。
- 注意：CI runner 里对清单的修改往往不提交，需本地跑脚本后手动 commit。

### 8. 远端验证（raw URL）
- `HEAD` 验证 manifest + 各平台资产 URL；**404 时等待约 5 秒重试**（刚 push 有 CDN 缓存延迟，短暂 404 后自愈）。
- 文件名/目录名格式差异（如目录 `{id}-{version}` vs 文件 `{id}_{version}_{goos}_{goarch}.zip`）按项目实际，勿用变量直接拼接。

### 9. 二进制级实锤（编译型产物/内嵌资源修复必做）
```python
import zipfile
z = zipfile.ZipFile('<asset zip>')
data = z.read('<二进制名>')
data.count(b'<修复后的关键字符串>')   # 应 >= 1
```
源码改了 ≠ 产物改了。内嵌资源（HTML/JS/配置）被编译进二进制、运行时从二进制读取；漏 bump 版本或 CI 用旧产物时，前面所有验证会全绿而线上依旧报错。
- **字面量探测有假阳性/假阴性**：Go 把字符串常量打包进连续 blob，相邻字符串拼接会产生巧合子串（如删掉某拼接后 `count` 仍为 1）。探测结果异常时，先 `grep` 源码确认该字面量是否还有代码引用，**最终以接口响应体/运行时行为为准**；另可比对新旧两版 `.so` 的 sha256 确认产物确实更新。

## 收尾
- 追加项目工作记忆：提交链、run id、本次踩坑。
- 告知用户：发布完成 ≠ 线上已更新，需部署侧拉取新产物并重启生效。

## 通用陷阱速查表
| 现象 | 根因 | 对策 |
|---|---|---|
| 422 空 body | choice input 值不在 options | 读工作流 inputs 定义，用枚举值 |
| curl 403 中文「无权访问 vip 分组」 | 代理层误报 | 换 PowerShell 通道 |
| TLS UNEXPECTED_EOF | schannel 间歇性失败 | PowerShell + `SecurityProtocol=3072` + `-TimeoutSec 30` |
| 下载 10060 连接超时 | release 下载 URL 重定向通道挂 | PowerShell `Invoke-WebRequest -OutFile` 备用 + sha256 比对 |
| 部分平台下载 FAIL | release 资产传播非原子 | 重试 + 等待（间隔 5-10s），勿判 release 缺失 |
| commit 报 nothing added | 并行会话已提交同内容 | fetch + log origin/main 对齐，复用已有提交 |
| runs 查不到 | head_sha 截断 / 用 name 判重 | 完整 40 位 sha；head_sha+created_at+数量 |
| raw URL 短暂 404 | CDN 缓存延迟 | 5s 重试，自愈 |
| 产物无修复内容 | 漏 bump 或 CI 旧产物 | 解压二进制查关键字符串（注意 blob 假阳性） |
