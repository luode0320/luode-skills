# REA CLI 命令速查手册

本文档汇总 REA (Reverse Engineer Anything) 常用命令组与参数说明。

## 1. 基础诊断与环境命令

| 命令 | 用途 | 常用选项 |
|------|------|----------|
| `rea --version` | 查看安装的 REA 版本 | - |
| `rea --help` | 查看全局帮助与命令列表 | - |
| `rea doctor` | 检查 Node 环境、已配置的反编译引擎与客户端注册 | `--format json`, `--client <name>` |
| `rea capabilities` | 查看当前已启用的分析引擎能力 | `--format json` |
| `rea update` | 更新全局安装的 REA 到最新版本 | - |
| `rea setup` | 为指定智能体注册 MCP 服务与指引 | `--client <agent>`, `--dry-run`, `-y` |

---

## 2. JavaScript 与 Electron 分析命令

| 命令 | 说明与示例 |
|------|-----------|
| `rea analyze-javascript-application <path>` | 静态解析 Electron 应用（ASAR 或目录）或 JS 结构，提取模块与导入关系。<br>`rea analyze-javascript-application ./app.asar --json` |
| `rea inspect-electron-fuses <path>` | 检查打包后 Electron 程序的 fuse 标记位（如 node 权限控制）。 |
| `rea recover-javascript-sources <path>` | 从 bundle 或 ASAR 中提取恢复可读源代码文件。<br>`rea recover-javascript-sources ./app.asar --destination ./src` |
| `rea trace-javascript-semantics <path>` | 追踪 JavaScript AST 语义关系与敏感调用。 |

---

## 3. 原生与编译语言二进制分析命令

| 命令 | 说明与示例 |
|------|-----------|
| `rea inspect-binary-layout <path>` | 检查二进制（PE/ELF/Mach-O）布局、段表、节区、符号信息。 |
| `rea inspect-go-binary <path>` | 提取 Go 二进制内置的编译器版本、引入的 modules 及构建设置。<br>`rea inspect-go-binary ./server.exe` |
| `rea inspect-rust-binary <path>` | 提取内嵌在 Rust 二进制中的 cargo-auditable 依赖包列表。<br>`rea inspect-rust-binary ./app` |
| `rea inspect-wasm-artifact <path>` | 使用 WABT 分析 WebAssembly 二进制节区、导入导出与反编译 WAT。 |
| `rea inspect-pe-resources <path>` | 分析 Windows PE 资源段（图标、版本信息、清单等）。 |
| `rea decompile <path>` | 反编译指定地址或符号的伪代码（需配置反编译引擎如 Ghidra/Hopper）。 |

---

## 4. 移动端与 Android 分析命令

| 命令 | 说明与示例 |
|------|-----------|
| `rea inspect-android-package <apk-path>` | 解析 APK 清单（AndroidManifest.xml）、包名、权限、组件与代码结构。 |
| `rea decode-android-resources <apk-path>` | 使用 apktool 解码 APK 资源、布局与字符串清单。 |
| `rea inspect-android-class <apk-path>` | 检查 APK 中指定类的成员清单。 |
| `rea inspect-android-method <apk-path>` | 反编译 APK 中指定类的具体方法（需 JADX 引擎）。 |
| `rea list-adb-devices` | 列出当前连接的 Android 设备与模拟器。 |

---

## 5. Web 与网络流量分析命令

| 命令 | 说明与示例 |
|------|-----------|
| `rea analyze-web-bundle <url/path>` | 捕获并静态分析网页 bundle 构成与导出的 API。 |
| `rea export-web-scripts <url/path>` | 导出网站所引用的所有外部与内嵌 JS 脚本供离线分析。 |
| `rea inspect-pcap-capture <pcap-file>` | 分析 `.pcap`/`.pcapng` 数据包：统计通信对端、DNS 请求、TLS SNI。 |
| `rea inspect-web-network-capture <har-file>` | 分析保存的 HAR 网络捕获包，查看请求/响应与 Payload。 |
| `rea inspect-sqlite-database <db-file>` | 查看本地 SQLite 数据库的 Schema、索引与表记录。 |
