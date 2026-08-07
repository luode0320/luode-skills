# VSCode Mock 调试任务模板

本文档提供 `.vscode/launch.json` 中运行时 Mock 模式的标准配置模板。所有 Go 后端项目在启用运行时 Mock 后，应至少包含 `normal` 与 `mock` 两套调试配置。

## 标准模板

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug <project> (local)",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}",
      "cwd": "${workspaceFolder}",
      "buildFlags": "-mod=vendor",
      "args": ["-env=local"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug <project> (mock)",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}",
      "cwd": "${workspaceFolder}",
      "buildFlags": "-tags=mock -mod=vendor",
      "args": ["-env=local"],
      "console": "integratedTerminal"
    }
  ]
}
```

## 配置说明

| 字段 | normal | mock | 说明 |
|------|--------|------|------|
| `name` | `Debug <project> (local)` | `Debug <project> (mock)` | 明确区分两种模式 |
| `buildFlags` | `-mod=vendor` | `-tags=mock -mod=vendor` | mock 必须携带 `-tags=mock` |
| `args` | `["-env=local"]` | `["-env=local"]` | 本地调试固定传 local 环境 |
| `program` | `${workspaceFolder}` | `${workspaceFolder}` | 主程序入口 |

## 多配置场景

当项目有多个二进制入口（`cmd/<binary>/main.go`）时，每个入口都应提供 normal 与 mock 两套配置：

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug api-server (local)",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/cmd/api-server",
      "cwd": "${workspaceFolder}",
      "buildFlags": "-mod=vendor",
      "args": ["-env=local"],
      "console": "integratedTerminal"
    },
    {
      "name": "Debug api-server (mock)",
      "type": "go",
      "request": "launch",
      "mode": "debug",
      "program": "${workspaceFolder}/cmd/api-server",
      "cwd": "${workspaceFolder}",
      "buildFlags": "-tags=mock -mod=vendor",
      "args": ["-env=local"],
      "console": "integratedTerminal"
    }
  ]
}
```

## 验证方式

1. 打开项目，在调试面板应能看到 `Debug <project> (local)` 和 `Debug <project> (mock)` 两个配置。
2. 选择 `(mock)` 配置启动，若构建成功，说明 `-tags=mock` 传递正确。
3. 选择 `(local)` 配置启动，若构建成功且不包含 mock 代码，说明排除正确。
4. 检查 `go build -tags mock ./...` 在终端正常工作。

## 任务模板（tasks.json）

如需将 mock 构建作为独立任务，可使用以下模板：

```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "build:mock",
      "type": "shell",
      "command": "go build -tags mock -o bin/app-mock.exe .",
      "group": {
        "kind": "build",
        "isDefault": true
      },
      "problemMatcher": ["$go"]
    },
    {
      "label": "run:mock",
      "type": "shell",
      "command": "go run -tags mock . -env=local",
      "group": "build",
      "problemMatcher": ["$go"]
    }
  ]
}
```
