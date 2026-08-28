---
name: wsl-chrome-cdp
description: 当 WSL2 环境需要访问 Windows Chrome 浏览器（CDP 远程调试）时使用。触发词：打开浏览器 / 打开网页 / 浏览器截图 / chrome / cdp / browser automation。自动检测 CDP 是否就绪、通过 PowerShell 启动 Chrome 调试模式、验证连接后移交网页操作层 skill 执行。
license: MIT
metadata:
  version: "1.1.0"
  author: 杏子
  displayName: WSL Chrome CDP
  compatibility: Windows + WSL2
  environment:
    - google-chrome（Windows 侧，默认路径 C:\Program Files\Google\Chrome\Application\chrome.exe）
    - powershell.exe（Windows 侧，WSL 内 /mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe）
  selfcheck: bash -n enable-browser.sh && curl -s --connect-timeout 2 http://127.0.0.1:9222/json/version
---

# wsl-chrome-cdp — WSL2 访问 Windows Chrome（CDP 桥接启动器）

## 一、定位与适用边界

解决 WSL2 环境中无法访问 Windows Chrome 的问题：检测 CDP（Chrome DevTools Protocol）是否就绪，未就绪时自动启动 Windows Chrome 调试模式并验证连接。

- **职责边界**：本 skill 只做「桥接启动器」——检测 / 启动 / 验证 CDP。打开页面、截图、点击、填表等**网页操作层**动作不在本 skill 范围，见「七、交叉引用」。
- **适用系统**：Windows + WSL2。
- **前置依赖**：Windows 侧安装 Chrome；WSL 内可访问 `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`。

## 二、工作流（4 步）

1. **检测 CDP**：`curl -s --connect-timeout 3 http://127.0.0.1:9222/json/version`，失败则尝试 Windows IP（`/etc/resolv.conf` nameserver）。
2. **启动 Chrome**：CDP 未就绪时，运行 `./enable-browser.sh`（自动经 PowerShell 以 `--remote-debugging-port=9222` 启动 Chrome 调试模式，等待 8 秒）。
3. **验证连接**：再次请求 `/json/version`，解析 `Browser` 版本字段；失败则按「五、故障排查」定位。
4. **移交操作层**：CDP 就绪后，将浏览器操作交给 `browser-session-automation-rules`（见交叉引用），本 skill 收尾。

## 三、脚本调用

```bash
# 一键检测 + 启动 + 验证（skill 根目录，本仓库布局）
./enable-browser.sh
```

脚本行为：取消代理 → 探测 CDP → 未就绪则 PowerShell 启动 Chrome 调试模式 → 等待 8 秒 → 复验 → 输出 Chrome 版本或明确失败原因（exit 1）。

- PowerShell 调用已统一使用标准前缀 `-NoProfile -ExecutionPolicy Bypass`（唯一真源见 `windows-encoding-rules/SKILL.md`「调用 PowerShell 命令时的标准化前缀」，禁止在本 skill 复制或漂移）。
- `get_windows_ip()` 内的 `$_` 已做 bash 转义（`\$_.`），避免双引号内被 bash 先行展开导致 PowerShell 命令失效。

## 四、文件结构

```
wsl-chrome-cdp__skillhub/
├── SKILL.md                          # 技能说明（本文件）
├── README.md                         # 快速入门
├── enable-browser.sh                 # 全自动启用脚本（唯一脚本）
└── docs/
    └── troubleshooting.md            # 故障排查指南
```

> 注意：原仓库声明的 `scripts/start-chrome-debug.bat` 在本仓库**不存在**（无真实来源不补造），Windows 备用启动逻辑已并入 `enable-browser.sh` 的 PowerShell 调用。

## 五、故障排查

### 问题 1：Chrome CDP 启动失败

```bash
# 检查 Chrome 是否安装（硬编码路径）
ls -la "/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
```

未安装则安装 Chrome；已安装但仍失败，检查端口 9222 是否被占用与防火墙是否放行。

### 问题 2：CDP 连接超时

```bash
# 1. 取消代理
unset http_proxy https_proxy

# 2. 尝试 Windows IP
WINDOWS_IP=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}')
curl http://$WINDOWS_IP:9222/json/version
```

### 问题 3：端口被占用

```powershell
netstat -ano | findstr 9222
taskkill /F /PID <进程 ID>
```

### 更多问题

查看 `docs/troubleshooting.md`（完整 5 类问题排查）。

## 六、环境依赖与自检（D4 登记）

| 依赖 | 说明 |
|---|---|
| google-chrome（Windows 侧） | 硬编码路径 `C:\Program Files\Google\Chrome\Application\chrome.exe`；本机缺失时端到端实测不可行，只能做语法与探测级自检 |
| powershell.exe（WSL 内可访问） | `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe` |

**自检命令**（无 Chrome 时仍可执行）：

```bash
bash -n enable-browser.sh                                  # 语法校验
curl -s --connect-timeout 2 http://127.0.0.1:9222/json/version   # CDP 端口探测
```

## 七、交叉引用（不复制正文）

| 场景 | 引用 |
|---|---|
| CDP 就绪后的网页操作（打开页面 / 快照 / 交互） | `browser-session-automation-rules`（agent-browser CLI） |
| 网络 HAR 记录 / 视觉 diff / profiling | `browser-advanced-testing-rules` |
| WSL↔Windows 桥接通用层 / 标准 PowerShell 前缀真源 | `wsl-powershell__skillhub`、`wsl-windows-bridge__skillhub`、`windows-encoding-rules` |

## 八、参考资料

- [Chrome DevTools Protocol](https://chromedevtools.github.io/devtools-protocol/)
- [OpenClaw Browser 文档](https://docs.openclaw.ai/tools/browser)

---

*技能版本：1.1.0 | 更新：2026-08-25（标准前缀修复 + `$_` 转义 + 断链清理 + frontmatter 合规）*
