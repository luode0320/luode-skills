---
name: vscode-fullstack-debug
description: 为 Go 后端 + 前端全栈仓库生成/更新 .vscode 调试配置，支持一键启动前后端。当用户提到"在 .vscode 加一个前后端同时启动的任务/配置"、"一键启动前后端"、"添加 vscode 调试配置"、"为项目配置 launch.json/tasks.json"时使用，即使他们没明确说"调试"。
---

# VS Code 全栈调试配置（Go 后端 + 前端）

为 Go 后端 + 前端（Vite/Rsbuild 等）的全栈仓库生成或更新 `.vscode/launch.json` 与 `.vscode/tasks.json`，
使开发者能在 VS Code 里一键同时启动后端和前端（Run and Debug 下拉框或 Tasks: Run Task）。

## 触发与范围

- 用户想让前后端一键启动（无论提的是"任务"还是"调试配置"）。
- 用户提到要新增/修改 `.vscode/` 下的 `launch.json`、`tasks.json`。
- 只做调试/启动配置，不涉及业务代码改动。

## 动手前先探测仓库（必须）

不要凭经验写死路径、端口或工具链。先并行读取以下信息：

1. `package.json` 的 `scripts`，判断前端工具链：Vite / Rsbuild / vue-cli / 其他，包管理器 npm/pnpm/bun/yarn。
2. 前端 dev server 端口与代理：看 `vite.config.*`、`rsbuild.config.*` 或 `.env.development`。
3. 后端入口与启动方式：`main.go`（或 main 包目录）、启动参数（如 `-env=local`）、后端端口。
4. 现有 `.vscode/launch.json` 与 `tasks.json`（可能已有部分配置，要合并而非覆盖）。

**从零生成 Go 配置时也要探测后端启动参数**：看 `main.go` 是否读取 `-env` / 环境变量、`config` 里默认端口、
是否有 `go:embed` 等，把必要的 `args`/`env` 带进生成的配置。参考 web-xiaoshuo（`args: ["-env=local"]`）与
new-api（后端在仓库根、用 `env` 注入 `SQLITE_PATH` 等）的差异——不要只生成一个裸 `program`。

## launch.json 的两种前端启动方式（按场景选）

前端配置有两种形态，用途不同：

- **要调试前端代码（断点、检查器）** → 用 `type: "pwa-chrome"` + `preLaunchTask`：
  先用一个后台任务把 dev server 拉起来，再让调试器打开浏览器附加调试。Vite 项目：
  ```jsonc
  {
    "name": "启动前端 (vite dev)",
    "type": "pwa-chrome",
    "request": "launch",
    "url": "http://localhost:<端口>",
    "webRoot": "${workspaceFolder}/<前端目录>/src",
    "preLaunchTask": "启动前端 (npm run dev)"
  }
  ```
  对应的 tasks.json 后台任务必须带 `problemMatcher`（监听 dev server 的"就绪"输出，如 Vite 的
  `ready in` / `Local:`）作为就绪信号，否则 preLaunchTask 会在服务还没起来时就结束、浏览器打开后 404。
- **只想在 Debug 视图一起拉起 dev server，不调前端** → 用 `type: "node-terminal"`：
  ```jsonc
  {
    "name": "Frontend: Dev Server",
    "type": "node-terminal",
    "request": "launch",
    "command": "<包管理器> install && <包管理器> run dev -- --port <端口>",
    "cwd": "${workspaceFolder}/<前端目录>"
  }
  ```

选择依据：用户提到"断点调前端/调试前端代码"→ 用 pwa-chrome + preLaunchTask；只是"一键启动/看效果"→
node-terminal 更轻（纯终端面板）。pwa-chrome 是 VS Code 内置类型，无需安装 Debugger for Chrome 扩展。

## 用 compounds 实现"一键启动"

后端 Go 调试配置 + 前端 dev server 配置，用 `compounds` 组合，`stopAll: true` 保证一起停：

```jsonc
{
  "compounds": [
    {
      "name": "前后端同时启动",
      "configurations": ["调试后端 main.go (local)", "启动前端 (vite dev)"],
      "stopAll": true
    }
  ]
}
```

`compounds.configurations` 里引用的名字必须与 `configurations[]` 里的 `name` 完全一致（大小写、空格）。
Go 配置保持用户已有的调试参数（mode、args、env、buildFlags 等），不要为了统一而改掉。

## tasks.json 的一键任务（可选项）

若用户提到"任务"或需要在终端面板跑，另建 `.vscode/tasks.json`，两个后台任务 + 一个 compound：

```jsonc
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "启动后端 (go run -env=local)",
      "type": "shell",
      "command": "go run main.go -env=local",
      "options": { "cwd": "${workspaceFolder}/<后端目录>" },
      "isBackground": true,
      "problemMatcher": [],
      "presentation": { "group": "dev", "panel": "dedicated" }
    },
    {
      "label": "启动前端 (npm run dev)",
      "type": "shell",
      "command": "npm run dev",
      "options": { "cwd": "${workspaceFolder}/<前端目录>" },
      "isBackground": true,
      // 前端任务务必带就绪检测：被 launch.json 的 preLaunchTask 复用时，
      // 空 problemMatcher 会让 preLaunchTask 在 dev server 未就绪时就结束。
      "problemMatcher": {
        "owner": "vite",
        "pattern": { "regexp": "." },
        "background": {
          "activeOnStart": true,
          "beginsPattern": ".*",
          "endsPattern": "ready in|Local:"
        }
      },
      "presentation": { "group": "dev", "panel": "dedicated" }
    },
    {
      "label": "前后端同时启动",
      "dependsOn": ["启动后端 (go run -env=local)", "启动前端 (npm run dev)"],
      "dependsOrder": "parallel",
      "problemMatcher": []
    }
  ]
}
```

## 已知的坑

- **JSON 里不能有注释**：`launch.json`/`tasks.json` 是标准 JSON 不是 JSONC。写完务必用 `JSON.parse` 校验，
  并检查 compound 引用的 `name` 都存在。可以用：
  `node -e "JSON.parse(require('fs').readFileSync('.vscode/launch.json','utf8')); console.log('ok')"`
- **端口/代理要一致**：前端 dev server 端口、代理目标（`/api` → 后端端口）必须与后端实际端口对齐，否则一键启动后接口 404。
- **不要用 `runtimeExecutable` 去"启动 dev server"**：在 `pwa-chrome`/`chrome` 配置里，`runtimeExecutable`
  的语义是**浏览器通道名或可执行文件路径**（`stable`、`canary`，或 `chrome.exe` 绝对路径），不是"要运行的命令"。
  写成 `"runtimeExecutable": "vite"` 会报「找不到 Chrome 版本 vite」，因为调试器把它当成了浏览器。
  想让调试器自动拉起 dev server，正确做法是 `pwa-chrome` + `preLaunchTask`（见上文模板）。
- **`chrome` 类型需要 Debugger for Chrome 扩展**（`msjsdiag.debugger-for-chrome`）；改用内置的 `pwa-chrome` 类型则无需装扩展。
- **`.vscode/` 可能在 `.gitignore` 里被忽略**：检查 `git check-ignore .vscode/tasks.json`。被忽略时改动只在本机生效，
  要向用户说明；用户想共享则需从 `.gitignore` 移除 `.vscode/`。
- **`go:embed` 后端**（如 new-api 把 `web/dist` 打进二进制）：后端编译会因 dist 缺失失败，需要先有占位文件。
  tasks.json 里可加一个 `preLaunchTask`/前置任务生成占位 `index.html`。

## 校验与交付

- 改完用 `node -e "JSON.parse(...)"` 校验两个文件，并确认 compounds/dependsOn 引用的名字都匹配。
- 向用户说明：一键启动的入口（Run and Debug 下拉框 / Tasks: Run Task）、各自端口、前端是否可断点调试、
  以及 `.vscode/` 是否被 gitignore（决定是否提交）。
