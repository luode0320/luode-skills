# VSCode 调试配置模板（Go + WSL）

适用场景：代码位于 `D:\luode\<project>`，WSL 用户工作路径为 `/home/luode/d/luode/<project>`，调试在 WSL 中执行。

**使用前提**：确认 `/home/luode/d/luode/<project>` 已 bind mount（参考 `path-mapping.md` 挂载检查步骤）。

---

## .vscode/tasks.json

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "WSL: go build",
      "type": "shell",
      "command": "wsl.exe",
      "args": [
        "-e", "bash", "-lc",
        "cd '/home/luode/d/luode/ellipal_admin' && go build ./..."
      ],
      "group": "build",
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    },
    {
      "label": "WSL: go test",
      "type": "shell",
      "command": "wsl.exe",
      "args": [
        "-e", "bash", "-lc",
        "cd '/home/luode/d/luode/ellipal_admin' && go test ./..."
      ],
      "group": "test",
      "presentation": {
        "reveal": "always",
        "panel": "shared"
      }
    },
    {
      "label": "WSL: Start dlv dap",
      "type": "shell",
      "command": "wsl.exe",
      "args": [
        "-e", "bash", "-lc",
        "cd '/home/luode/d/luode/ellipal_admin' && dlv dap --listen=:2345 --headless=true --log --log-output=debugger,dap"
      ],
      "isBackground": true,
      "problemMatcher": {
        "pattern": {
          "regexp": ".",
          "file": 1,
          "location": 2,
          "message": 3
        },
        "background": {
          "activeOnStart": true,
          "beginsPattern": ".",
          "endsPattern": "DAP server listening"
        }
      },
      "presentation": {
        "reveal": "always",
        "panel": "dedicated"
      }
    },
    {
      "label": "WSL: Start dlv dap (specific package)",
      "type": "shell",
      "command": "wsl.exe",
      "args": [
        "-e", "bash", "-lc",
        "cd '/home/luode/d/luode/ellipal_admin' && dlv dap --listen=:2345 --headless=true --log -- ./cmd/server"
      ],
      "isBackground": true,
      "problemMatcher": {
        "pattern": {
          "regexp": ".",
          "file": 1,
          "location": 2,
          "message": 3
        },
        "background": {
          "activeOnStart": true,
          "beginsPattern": ".",
          "endsPattern": "DAP server listening"
        }
      }
    }
  ]
}
```

---

## .vscode/launch.json

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
      "substitutePath": [
        {
          "from": "${workspaceFolder}",
          "to": "/home/luode/d/luode/ellipal_admin"
        }
      ]
    },
    {
      "name": "WSL: Launch & Debug (via task)",
      "type": "go",
      "request": "attach",
      "mode": "remote",
      "port": 2345,
      "host": "127.0.0.1",
      "preLaunchTask": "WSL: Start dlv dap",
      "substitutePath": [
        {
          "from": "${workspaceFolder}",
          "to": "/home/luode/d/luode/ellipal_admin"
        }
      ]
    }
  ]
}
```

---

## substitutePath 路径换算规则

`substitutePath` 用于对齐 Windows 侧断点与 WSL 侧源码路径。
`from` 是 VSCode 打开的 Windows 工作目录，`to` 是 bind mount 后的用户工作路径：

| Windows 路径（from） | WSL 用户工作路径（to） |
|---------------------|----------------------|
| `D:\luode\ellipal_admin` | `/home/luode/d/luode/ellipal_admin` |
| `D:\luode\<project>` | `/home/luode/d/luode/<project>` |

换算规则：`${workspaceFolder}` → bind mount 目标路径（`/home/luode/d/<win-path-without-drive>`）

---

## 调试流程

1. 确认 bind mount 已就绪：
   ```powershell
   wsl.exe -e bash -lc "mountpoint -q /home/luode/d/luode/ellipal_admin && echo 'mounted' || echo 'not_mounted'"
   ```
   未挂载时先执行挂载（见 `path-mapping.md`）

2. 确认 WSL 中已安装 `dlv`：
   ```powershell
   wsl.exe -e bash -lc "which dlv || go install github.com/go-delve/delve/cmd/dlv@latest"
   ```

3. 在 VSCode 终端运行任务 `WSL: Start dlv dap`，等待输出 `DAP server listening`

4. 切换到 Run & Debug 面板，选择 `WSL: Attach to dlv`，按 F5 启动

5. 断点在 Windows 侧的源码文件上打，`substitutePath` 自动对齐到 WSL 路径

---

## 常见问题

**dlv 连不上（connection refused）**
- 确认 `dlv dap` 已启动并输出 `DAP server listening`
- 确认端口 2345 没有被占用：`wsl.exe -e bash -lc "ss -tlnp | grep 2345"`

**断点不命中**
- 检查 `substitutePath` 的 `from`/`to` 是否与实际路径完全匹配
- 确认 `go build` 时没有使用 `-trimpath`（会裁掉路径信息导致断点失效）
- 确认 bind mount 正常，`ls /home/luode/d/luode/ellipal_admin` 能看到源码文件

**dlv 版本过旧**
```powershell
wsl.exe -e bash -lc "go install github.com/go-delve/delve/cmd/dlv@latest"
```
