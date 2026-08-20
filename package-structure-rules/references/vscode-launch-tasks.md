# VSCode 启动与编译任务规则

`.vscode/launch.json` 与 `.vscode/tasks.json` 是前后端同仓、独立后端、独立前端三类项目的必需提交文件（路径与提交属性见 `project-layout-v2.md` 与 `placement-catalog.yaml`）。本文件只定义它们的**最小启动内容规则**：至少必须有哪条启动配置、环境怎么注入、需要先编译时怎么挂任务。

配置根、配置文件命名与环境识别优先级由 `configuration-layout.md` 唯一定义，本文件不重复声明。

## 最小要求：一条 local 调试配置

`.vscode/launch.json` 唯一强制项是**至少保留一条本地开发调试配置**：

- `name` 为 `local开发环境启动`（历史 `dev开发环境启动` 兼容合法）。
- `args` 为 `["-env=local"]`。
- 不挂 `preLaunchTask`，直连调试器，保最快调试回环。

除此之外，`launch.json` 里有几条配置、叫什么名字，由项目自行决定，本规则不限制、不补齐、不强制统一。

## 不强制按环境铺满启动配置

`config/yaml/` 存在 `config.test.yaml`、`config.prod.yaml` **不构成**在 `launch.json` 补对应启动配置的义务：

- `test`、`prod` 属人工发布与人工验证链路，用本地调试器直接启动这些环境没有实际意义，也与本地连接红线冲突。
- 因此不存在「配置文件与启动配置一一对应」的要求，缺少 test/prod 启动配置不算漏配。

反向约束仍然硬性成立：任何已存在的启动配置，其 `-env=<env>` 必须能在配置数据目录找到对应的 `config.<env>.yaml`（独立后端 `config/yaml/`，同仓后端 `backend/config/yaml/`）；指向不存在的环境文件时启动必然被 `load.<ext>` 拒绝，属非法残留。

## 启动配置分类

| 类别 | 是否强制 | `name` | `args` | `preLaunchTask` |
|---|---|---|---|---|
| 本地开发调试 | **必需（至少一条）** | `local开发环境启动` | `["-env=local"]` | 无 |
| 项目自定义启动（如先编译签名再启动、attach、指定端口） | 可选，由项目自行决定 | 项目自定，如 `编译签名并启动` | 指向已存在环境的 `-env=<env>`，默认 `local` | 允许挂 `tasks.json` 的 label |
| 面向真实环境（`test`、`prod` 等）的启动 | 不建议；确有人工需要才保留 | 项目自定 | 对应 `-env=<env>` | 必须挂编译任务，且 Agent 禁止使用 |

## 硬规则

1. 至少保留一条 `local开发环境启动`（`args ["-env=local"]`、无 `preLaunchTask`）；其余启动配置数量与命名不受约束。
2. 环境注入只允许命令行 `-env=<env>`。禁止在 `launch.json` 用 `env: {"APP_ENV": ...}` / `env: {"ENV": ...}` 注入环境，否则启动配置的环境来源与 `load.<ext>` 的优先级契约（`-env > APP_ENV > ENV > local`）脱钩，排障时无法从启动配置直接读出实际环境。
3. `-env=<env>` 的 `<env>` 必须与配置文件名 `config.<env>.yaml` 中的 `<env>` 逐字一致，且为小写 `[a-z][a-z0-9_]*`；不得出现 `-env=PROD`、`-env=pre-prod` 这类大写或连字符写法，也不得指向不存在的环境文件。
4. `args` 标准形式为数组 `["-env=<env>"]`；历史单参数字符串形式 `"-env=<env>"` 兼容合法，不强制改写。
5. `program` 固定指向该项目的二进制入口所在目录：独立后端 `${workspaceFolder}`，前后端同仓后端 `${workspaceFolder}/backend`；不得指向入口边界之外的子目录。
6. Go 项目启动配置固定 `"type": "go"`、`"request": "launch"`、`"mode": "debug"`；调试产物统一落 `output: "${workspaceFolder}/debug.exe"`，该产物与其它调试可执行文件必须写入 `.gitignore`，不得提交。`dlvFlags` 只放环境兼容参数（如 `--check-go-version=false`），不放业务参数。
7. 需要先编译、签名或归档再启动的配置，必须通过 `preLaunchTask` 引用 `tasks.json` 的 label，不在 `launch.json` 内联 shell 命令；默认的 `local开发环境启动` 保持无 `preLaunchTask`。
8. 编译任务 label 不按环境分裂成 `build-test`、`build-prod`：全部环境 yaml 已在编译期嵌入同一二进制，产物与环境无关，环境只在运行时由 `-env` 决定。签名工具路径、产物名、归档目录等差异用 `tasks.json` 的 `inputs` 参数化，不复制多份 label。
9. 配置改为编译期嵌入（Go `//go:embed yaml/config.*.yaml`）后，`launch.json` 与 `tasks.json` 不得再通过复制 yaml 到产物目录、传 `-config=<path>`、修改工作目录等方式提供配置；编译与归档任务只允许附带部署必需的非配置文件。

`check` 命令只做路径与目录事实校验，不解析 JSON 内容；上述内容规则属于人工与评审检查项，不是脚本闸门。

## tasks.json 任务规则

| label | 职责 | `group` | 被谁引用 |
|---|---|---|---|
| `build` | 编译二进制，并按项目需要执行签名与归档 | `build`（`isDefault: true`） | 需要先编译的启动配置的 `preLaunchTask` |
| 平台专用发布任务（如 `win-sign-and-publish`） | 平台特有的签名与发布脚本包装 | `build` | 人工手动执行 |

- 任务 label 不带环境后缀；同一任务的平台差异用 `windows` / `linux` / `osx` 覆盖块或独立 label 表达，不用环境名区分。
- 平台专用发布任务不得成为默认本地调试配置的 `preLaunchTask`。
- 任务里的 shell 命令按 UTF-8 处理输出（Windows 下需要时显式切码页），避免中文提示与归档目录名乱码。

## 本地连接红线联动

Agent 在需求侦察、Bug 复现、功能验证、回归测试、联调中只能使用 `local` 启动配置与 `local` 配置数据。项目若保留了面向 `test`、`prod` 的启动配置，那只服务人工发布与人工验证；即使这些环境的 yaml 已随二进制嵌入，也不构成 Agent 使用它们的授权。

## 参考示例（Go 独立后端）

一条强制的本地调试配置，加一条项目自定义的先编译签名再启动配置：

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "local开发环境启动",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "args": ["-env=local"],
            "program": "${workspaceFolder}",
            "output": "${workspaceFolder}/debug.exe",
            "dlvFlags": ["--check-go-version=false"]
        },
        {
            "name": "编译签名并启动",
            "type": "go",
            "request": "launch",
            "mode": "debug",
            "args": ["-env=local"],
            "program": "${workspaceFolder}",
            "preLaunchTask": "build",
            "output": "${workspaceFolder}/debug.exe",
            "dlvFlags": ["--check-go-version=false"]
        }
    ]
}
```

## 合法与非法示例

合法示例：

- `launch.json` 只有一条 `local开发环境启动`，`config/yaml/` 同时存在 local、test、prod 三份配置：不要求补 test/prod 启动配置。
- 在 `local开发环境启动` 之外增加项目自定义的 `编译签名并启动`（`-env=local` + `preLaunchTask: "build"`）。
- 同仓后端启动配置 `program` 为 `${workspaceFolder}/backend`，`args` 为 `["-env=local"]`。

非法示例：

- `launch.json` 没有任何本地开发调试配置，或唯一的 local 配置挂了 `preLaunchTask`。
- 启动配置写 `-env=dev`，但 `config/yaml/` 没有 `config.dev.yaml`。
- 用 `env: {"APP_ENV": "test"}` 代替 `args: ["-env=test"]`。
- `tasks.json` 同时存在 `build-test` 与 `build-prod` 两个只有签名参数不同的 label。
- 编译任务把 `config/yaml/*.yaml` 复制进产物目录，或启动配置传 `-config=./config.prod.yaml`。
- 提交 `debug.exe` 等调试产物到仓库。
