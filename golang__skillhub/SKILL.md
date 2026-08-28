---
name: golang
description: "Go 开发操作日志与审计追踪工具：记录构建/测试/lint/格式化/生成/修复等开发操作的时间戳条目，支持按命令回看、全文搜索、导出 JSON/CSV/TXT 与统计。当用户需要给 Go 开发过程留痕、记录构建测试结果、跟踪 lint/格式化操作、检索历史开发记录、导出开发日志做周报或审计时触发。触发词：golang、go 日志、开发日志、构建记录、测试记录、lint 记录、审计追踪、导出日志、代码操作记录。真正的 Go 工程实践（代码风格/模式/构建测试写法）见 golang-patterns。"
license: MIT-0
metadata:
  displayName: "Go 开发日志工具"
  version: "2.0.1"
  author: "BytesAgain"
  homepage: "https://bytesagain.com"
  source: "https://github.com/bytesagain/ai-skills"
  tags: [golang, tool, utility]
allowed-tools: Read, Write, Bash
---

# Go 开发日志工具

Go 开发操作的本地日志与审计追踪工具：把构建、测试、lint、格式化、生成、修复等操作以时间戳条目落盘，供回看、检索、导出与统计。**注意：本工具只记录操作日志，不执行构建/测试/lint 本身**（那是 `go build` / `go test` / `golangci-lint` 等命令的职责）。

## 适用边界

- **做**：记录开发操作条目（带时间戳）、按命令回看最近 20 条、跨日志全文搜索、导出 JSON/CSV/TXT、统计各类型条目数、健康检查。
- **不做（转交）**：
  - Go 代码风格、惯用模式、构建/测试写法 → `golang-patterns`
  - 代码质量规则（注释/命名/错误处理等）→ `code-quality-rules` 相关域

## 工作流（4 步）

### 第 1 步：记录操作

- **输入**：一次真实发生的 Go 开发操作（如 `go build ./...` 通过、`golangci-lint` 发现 3 个问题）。
- **动作**：选择对应命令记录，如 `golang check "go vet ./... clean"`、`golang lint "3 issues in pkg/handler"`。
- **检查点**：记录内容含敏感信息（密钥、内网路径、个人信息）时，先脱敏再写入——日志文件是明文本地存储。
- **输出**：带时间戳的日志条目（写入 `<command>.log` + `history.log`）。

### 第 2 步：回看与检索

- **输入**：想查的历史记录（某个命令最近操作 / 某个关键词 / 某包某文件）。
- **动作**：`golang lint`（无参回看该命令最近 20 条）、`golang search "handler"`（跨全部日志搜索）。
- **输出**：命中条目列表；无命中时输出空结果提示（不是报错）。

### 第 3 步：导出与统计

- **输入**：周报/审计/复盘需要的结构化数据。
- **动作**：`golang export json|csv|txt` 导出到数据目录；`golang stats` 查看各类型条目数。
- **输出**：导出文件（`export.json/csv/txt`）或统计摘要。

### 第 4 步：健康检查与复盘

- **输入**：数据目录状态 / 长期使用后的整理需求。
- **动作**：`golang status` 查看版本、条目总数、磁盘占用、最后活动；据此决定归档或清理。
- **输出**：健康状态报告。

## 命令速查表

脚本：`scripts/script.sh`（`golang <command> [args]`，支持任意 cwd 以绝对路径调用）。

| 命令 | 用途 |
|---|---|
| `check/validate/generate/format/lint/explain/convert/template/diff/preview/fix/report <input>` | 记录一条带时间戳的日志；无参时回看该命令最近 20 条 |
| `stats` | 各日志类型条目数统计 |
| `export json\|csv\|txt` | 导出全部条目（非法格式返回退出码 1） |
| `search <term>` | 跨全部日志文件搜索关键词 |
| `recent` | 最近 20 条跨命令活动 |
| `status` | 健康检查：版本/条目数/磁盘/最后活动 |
| `help` / `version` | 帮助 / 版本 |

## 数据存储

- 位置：`~/.local/share/golang/`（`<command>.log` 各命令独立日志、`history.log` 统一流水、`export.*` 导出文件）。
- 全离线：无云、无网络调用、无 API key。

## 边界条件与异常处理

- **脚本不可用**（bash 缺失或执行失败）：降级为纯文本记录——直接在本轮对话输出带时间戳的条目，并提示用户数据未落盘。
- **写入失败**（数据目录不可写、磁盘满）：脚本报错退出，不静默吞掉；用户看到错误后换可写路径（改 `HOME` 或手工建目录）。
- **非法导出格式**：`export xml` 输出可用格式提示并返回退出码 1（实测行为）。
- **搜索无结果**：输出空结果说明，不伪造命中。
- **敏感信息**：写入前脱敏（见第 1 步检查点）。

## 退出机制

用户输入「结束」→ 停止，回复「日志记录完成。」；记录内容为空或命令含义不明时先向用户确认再写入。

## 约束

- 日志是审计凭据：条目必须真实对应发生的操作，禁止编造或补记未发生的事件。
- 只记录操作摘要（谁/何时/做了什么/结果），不复制源码大段内容。
- 数据目录在 `~/.local/share/golang/`，跨机器迁移时需自行备份该目录。
