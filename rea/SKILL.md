---
name: rea
display_name: REA 逆向工程分析工具
display_name_en: Reverse Engineer Anything (REA)
description: 【强制自动触发】当识别到用户需要逆向、逆向工程、反编译、脱壳、代码抽取、ASAR拆包、Electron应用逆向、APK/IPA包体分析、无源码应用功能原理分析、提取Go/Rust/WASM二进制编译器信息与依赖、分析.NET程序集元数据或PCAP/HAR数据包协议时强制自动触发。提供REA逆向分析工作流与CLI命令；本地未安装时引导从官方Releases页面(https://github.com/morluto/rea/releases)安装。
description_zh: 【强制自动触发】当识别到用户需要逆向、逆向工程、反编译、脱壳、代码抽取、ASAR拆包、Electron应用逆向、APK/IPA包体分析、无源码应用功能原理分析、提取Go/Rust/WASM二进制编译器信息与依赖、分析.NET程序集元数据或PCAP/HAR数据包协议时强制自动触发。提供REA逆向分析工作流与CLI命令；本地未安装时引导从官方Releases页面(https://github.com/morluto/rea/releases)安装。
description_en: Automatically triggers when reverse engineering, decompiling, unpacking, ASAR/Electron analysis, APK analysis, inspecting Go/Rust/WASM binaries, or analyzing PCAP captures. Provides REA reverse engineering workflows and CLI guidance; guides installation from GitHub Releases if not installed.
category: tools
version: 1.0.0
author: morluto / luode
---

# REA：逆向工程分析工具 (Reverse Engineer Anything)

REA（Reverse Engineer Anything）是由 [morluto/rea](https://github.com/morluto/rea) 开源的多目标逆向工程与运行时分析工具。它支持在本地深入分析各类原生二进制文件、打包应用、托管代码、Web 工件以及网络流量，提取代码证据（Evidence）、调用图谱和元数据，帮助理解无源码软件的具体功能实现与行为逻辑。

---

## 一、前置环境检查与安装引导

在执行任何逆向分析任务之前，**必须先检查本地环境中是否已安装 `rea` CLI 工具**。

### 1.1 检查命令
在终端中执行：
```bash
rea --version
```

### 1.2 未安装时的引导说明（重要）
如果终端提示 `command not found`、`未找到命令` 或执行失败，说明本地尚未安装 REA。请按以下指引操作：

1. **官方 Release 页面与下载地址**：
   - 官方 GitHub Releases：[https://github.com/morluto/rea/releases](https://github.com/morluto/rea/releases)
   - 官方网站与文档：[https://rea.tools/](https://rea.tools/)

2. **快速安装方法**：
   - **通过 npm 全局安装（推荐）**：
     ```bash
     npm install --global rea-agents
     ```
     安装后即可在全局使用 `rea` 命令。
   - **通过 npx 免安装运行**：
     若临时无需全局安装，可直接使用 `npx` 执行：
     ```bash
     npx -y rea-agents@latest <command>
     ```
   - **智能体 MCP 自动配置**：
     ```bash
     npx rea-agents setup
     ```
     支持自动向 Codex、Claude Code、Cursor、Gemini CLI、VS Code 等智能体注册 REA MCP 服务。

3. **依赖环境要求**：
   - Node.js >= 22.19、24.11 或 26+，以及 npm。
   - 静态分析大部分目标（JS/Electron/Go/Rust/WASM/.NET）无需原生反编译器；原生二进制高级反编译可选配置 Hopper、Ghidra、IDA 或 Rizin。

---

## 二、目标分类与命令路由速查

针对不同类型的逆向目标，优先选用以下专用子命令：

| 目标类型 | 典型文件 / 格式 | 推荐 REA 命令 | 典型产出与证据 |
|---------|---------------|---------------|--------------|
| **JavaScript / Electron** | `.asar`, 解包目录, `.js`, `.bundle` | `rea analyze-javascript-application <path> --json` | 模块依赖图、IPC 边界、路由、原生扩展关系 |
| **Electron 安全配置** | 打包后的 Electron 可执行程序 | `rea inspect-electron-fuses <binary-path>` | 检查 Electron Fuses（如是否禁用 runAsNode） |
| **Go 二进制** | ELF / PE / Mach-O Go 编译产物 | `rea inspect-go-binary <binary-path>` | 编译器版本、依赖 Module 清单、构建参数 |
| **Rust 二进制** | 带 cargo-auditable 的二进制 | `rea inspect-rust-binary <binary-path>` | 编译内嵌的完整 Rust crates 依赖清单 |
| **WebAssembly** | `.wasm` 模块文件 | `rea inspect-wasm-artifact <wasm-path>` | 节区结构、导入/导出表、反编译后的 WAT 代码 |
| **原生可执行程序** | `.exe`, `.dll`, `.so`, Mach-O | `rea inspect-binary-layout <path>` / `rea decompile <path>` | 节区布局、符号、导入/导出表、反编译伪代码 |
| **.NET 托管程序集** | `.exe`, `.dll` (C# / .NET) | `rea inspect-managed-artifact <path>` / `inspect-managed-members` | PE/CLI 元数据、类型与成员签名、P/Invoke 原生边界 |
| **Android APK** | `.apk` 安装包 | `rea inspect-android-package <apk-path>` | Manifest 声明、权限、组件、类与反编译方法 |
| **Android 资源** | `.apk` 资源与配置 | `rea decode-android-resources <apk-path>` | 解析后的 AndroidManifest.xml 与字符串资源 |
| **网页 / Web 资源** | 目标 URL 或离线 HTML | `rea analyze-web-bundle <url> --json` | 页面 Bundle 构成、依赖脚本提取、导出的 API |
| **网络流量抓包** | `.pcap`, `.pcapng` 数据包 | `rea inspect-pcap-capture <pcap-path>` | 通信端点、DNS 解析记录、TLS SNI、协议分布 |
| **Web 会话捕获** | `.har`, mitmproxy, `.saz` | `rea inspect-web-network-capture <har-path>` | 请求/响应列表、调用栈关联、关键 Payload |
| **SQLite 数据库** | `.db`, `.sqlite`, 本地缓存库 | `rea inspect-sqlite-database <db-path>` | 库表 Schema、索引定义、表数据记录提取 |

---

## 三、常用场景操作示例

### 3.1 环境诊断与就绪检查
在排查 REA 工具链状态或检查外部分析引擎时使用：
```bash
rea doctor
```
如果需要 JSON 格式输出供程序解析：
```bash
rea doctor --format json
```

### 3.2 逆向 Electron / 桌面应用实现逻辑
分析目标 Electron 应用（如 Slack、Notion、Obsidian 等）的 ASAR 文件或解包目录：
```bash
# 静态分析整个应用包结构
rea analyze-javascript-application "C:/path/to/app.asar" --json

# 从中提取可读的源代码文件
rea recover-javascript-sources "C:/path/to/app.asar" --destination "./extracted_src"
```

### 3.3 检查 Go / Rust 二进制依赖与版本
对于无源码的独立二进制文件，提取其编译元数据：
```bash
# 分析 Go 二进制
rea inspect-go-binary ./target_go_app.exe

# 分析 Rust 二进制内嵌依赖
rea inspect-rust-binary ./target_rust_app
```

### 3.4 逆向 Android APK 的组件与核心逻辑
```bash
# 查看 APK 基础信息、权限与组件列表
rea inspect-android-package ./sample.apk

# 反编译指定类中的具体方法（需已提供 JADX）
rea inspect-android-method ./sample.apk --class "com.example.app.AuthManager" --method "login"
```

### 3.5 分析 WebAssembly (WASM) 文件
```bash
# 检查 WASM 模块接口与 WAT 文本
rea inspect-wasm-artifact ./module.wasm
```

### 3.6 分析 PCAP 抓包文件中的通信特征
```bash
# 查看流量包概要、DNS 解析与 TLS 握手域名
rea inspect-pcap-capture ./traffic.pcap
```

---

## 四、全局输出控制选项

REA 支持多种输出格式与 Token 控制参数，适合大模型消费与终端脚本处理：

- `--format <json|yaml|md|toon|jsonl>`：指定输出格式，默认根据终端自适应；脚本与 Agent 交互推荐 `--format json`。
- `--llms` / `--llms-full`：打印适合 LLM 理解的高密度清单与接口摘要。
- `--filter-output <keys>`：根据字段路径过滤输出（例如 `dependencies,modules[0].name`），减少上下文开销。
- `--token-limit <n>`：限制最大输出 token 数量，防止输出过大撑爆上下文窗口。
- `--token-count`：只打印输出内容的 token 计数，不输出实际内容。
- `--mcp`：直接以标准输入输出（stdio）启动 REA MCP 服务。

---

## 五、故障排查与使用建议

1. **未找到命令 (Command Not Found)**：
   - 优先执行 `npm install -g rea-agents` 安装。
   - 若受限于权限，使用 `npx -y rea-agents@latest <command>` 替代。
   - 安装源与 Release 页面详见：[https://github.com/morluto/rea/releases](https://github.com/morluto/rea/releases)。
2. **Missing Analysis Engine 提示**：
   - REA 对许多格式（如 JS/Electron/Go/Rust/WASM/PE 基础信息）支持**纯内置静态分析**，无需第三方引擎。
   - 仅当需要深层汇编/伪代码逆向（原生二进制 decompile）或反编译 Java 类时，才需按需配置 Hopper、Ghidra 或 JADX。
3. **输出过长处理**：
   - 逆向分析完整包体可能产生数万行输出，建议搭配 `--filter-output` 或指定具体的目标子路径，并使用 `--token-limit 4000` 保护会话上下文。
