# VSCode 调试配置模板（Go + WSL）

适用场景：代码位于 `D:\luode\<project>`，WSL 路径为 `/mnt/d/luode/<project>`，调试在 WSL 中执行。直接用 WSL 自动挂载路径，无需 bind mount。

默认使用 WSL 默认发行版（命令省略 `-d`）；如有多个发行版需指定，先用 `wsl.exe -l -v` 查看实际名称，再加 `-d <发行版名>`。

---

## 方式一：命令行直接调试（最简单）

```powershell
wsl.exe --cd /mnt/d/luode/<project> dlv debug ./cmd/<app>
```

## 方式二：VSCode 远程调试（dlv dap）

### .vscode/tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "WSL: Start dlv dap",
      "type": "shell",
      "command": "wsl.exe",
      "args": [
        "--cd",
        "/mnt/d/luode/ellipal_admin",
        "dlv",
        "dap",
        "--listen=:2345",
        "--headless=true",
        "--log",
        "--log-output=debugger,dap"
      ],
      "isBackground": true,
      "problemMatcher": {
        "pattern": { "regexp": ".", "file": 1, "location": 2, "message": 3 },
        "background": {
          "activeOnStart": true,
          "beginsPattern": ".",
          "endsPattern": "DAP server listening"
        }
      },
      "presentation": { "reveal": "always", "panel": "dedicated" }
    }
  ]
}
```

### .vscode/launch.json

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "WSL: Attach to dlv",
      "type": "go",
      "request": "attach",
      "mode": "remote",
      "port": 2345,
      "host": "127.0.0.1",
      "preLaunchTask": "WSL: Start dlv dap",
      "substitutePath": [
        {
          "from": "${workspaceFolder}",
          "to": "/mnt/d/luode/ellipal_admin"
        }
      ]
    }
  ]
}
```

---

## substitutePath 路径换算

`from` 是 VSCode 打开的 Windows 工作目录，`to` 是对应的 WSL 自动挂载路径：

| Windows 路径（from）     | WSL 路径（to）               |
| ------------------------ | ---------------------------- |
| `D:\luode\ellipal_admin` | `/mnt/d/luode/ellipal_admin` |
| `D:\luode\<project>`     | `/mnt/d/luode/<project>`     |

换算规则：盘符转小写 → 去掉 `:` → `\` 改为 `/` → 前缀 `/mnt/`。

---

## 调试流程

1. 确认 WSL 中已安装 `dlv`：
   ```powershell
   wsl.exe --cd /mnt/d/luode/<project> bash -lc "which dlv || go install github.com/go-delve/delve/cmd/dlv@latest"
   ```
2. 在 VSCode 运行任务 `WSL: Start dlv dap`，等待输出 `DAP server listening`
3. 切换到 Run & Debug 面板，选择 `WSL: Attach to dlv`，按 F5 启动
4. 断点在 Windows 侧源码文件上打，`substitutePath` 自动对齐到 WSL 路径

---

## 常见问题

**dlv 连不上（connection refused）**

- 确认 `dlv dap` 已启动并输出 `DAP server listening`
- 确认端口 2345 没被占用：`wsl.exe bash -lc "ss -tlnp | grep 2345"`

**断点不命中**

- 检查 `substitutePath` 的 `from`/`to` 是否与实际路径完全匹配
- 确认 `go build` 时没有使用 `-trimpath`（会裁掉路径信息导致断点失效）

**dlv 版本过旧**

```powershell
wsl.exe --cd /mnt/d/luode/<project> go install github.com/go-delve/delve/cmd/dlv@latest
```
