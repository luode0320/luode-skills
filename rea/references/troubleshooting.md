# REA 环境检测与故障排查指南

## 1. 未安装 CLI 工具处理

如果终端执行 `rea` 报错：
```text
bash: rea: command not found
# 或 Windows CMD/PowerShell:
'rea' 不是内部或外部命令，也不是可运行的程序或批处理文件。
```

### 解决步骤：
1. **获取官方 Releases 与安装文件**：
   - 官方 Releases：[https://github.com/morluto/rea/releases](https://github.com/morluto/rea/releases)
   - npm 包主页：[https://www.npmjs.com/package/rea-agents](https://www.npmjs.com/package/rea-agents)
2. **执行安装命令**：
   ```bash
   npm install --global rea-agents
   ```
3. **确认 Node.js 版本**：
   REA 要求 Node.js >= 22.19、24.11 或 26+。若 Node 版本过低，请先升级 Node.js。
4. **临时执行（免安装）**：
   无需全局安装即可直接执行：
   ```bash
   npx -y rea-agents@latest --help
   ```

---

## 2. REA Doctor 诊断

安装后可通过 `rea doctor` 查看环境健康状态：
```bash
rea doctor
```

常见状态说明：
- `node` / `host`: 基础运行环境，正常为 healthy。
- `missing_analysis_engine`（如 hopper, ghidra, ida, jadx）:
  - **无需惊慌**：针对绝大多数静态分析（JS、Electron、Go、Rust、WASM、PE/ELF 基础信息、PCAP、SQLite、Web），**纯内置分析器即可完全胜任**。
  - 只有在需要生成高级 C 伪代码、反编译 Android Java 类时，才需要按需提供外部引擎（如设置 `GHIDRA_INSTALL_DIR` 或通过 `rea setup` 安装 Hopper）。
- `config_drift`: 提示某个 Agent（如 codex, cursor, claude_desktop 等）尚未注册 REA MCP 服务。可通过 `rea setup --client <agent>` 进行注册。

---

## 3. 输出保护与性能优化

- **Token 保护**：逆向复杂大型二进制或几十万行 JS 包时，避免一次性在终端输出全部内容：
  ```bash
  rea analyze-javascript-application ./app.asar --format json --token-limit 3000
  ```
- **输出过滤**：使用 `--filter-output` 只提取感兴趣的节点：
  ```bash
  rea inspect-go-binary ./app.exe --filter-output "compiler,modules"
  ```
