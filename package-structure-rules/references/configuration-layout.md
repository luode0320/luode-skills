# 配置位置规则

项目只有一套配置根：独立后端使用根级 `config/`；前后端同仓时，后端配置统一使用 `backend/config/`。不得在 `src/config/`、`internal/config/`、工作区根 `config/` 或其他位置重复定义同一套后端配置。

`test/` 与 `mock/` 目录不承载独立配置数据源。测试和 Mock 所需的运行时配置数据统一使用项目 `config/` 下的 `test` 环境（例如 `config/yaml/config.test.yaml`）。但 `test/config/` 和 `mock/config/` 允许作为测试配置加载/解析逻辑的目录（如 `test/config/config_load_test.go`），这不属于配置数据源，而是测试代码的一部分，不受该禁止约束。

## 配置模式（yaml/ 唯一）

`config/yaml/` 是唯一配置模式，所有配置数据统一写入其中，不再提供源码内配置模式。`config/embedded/` 已废弃，strict 检查下存在即报错；旧项目遗留的 embedded 目录须经收敛清单登记为 `legacy_source_roots` 才能继续维护，新配置一律进 `config/yaml/`。

| 路径 | 内容 | 安全边界 |
|---|---|---|
| 独立后端 `config/load.<ext>` | 配置加载与解析入口：读取 `config/yaml/` 的对应环境文件，并解析为配置结构；环境识别支持 `-env`、`APP_ENV`、`ENV`，优先级 `-env > APP_ENV > ENV > local`；例如 Go 使用 `config/load.go`，通过 `//go:embed yaml/config.*.yaml` 编译期嵌入并按环境读取 | 与普通源码相同；不得输出 yaml 私密配置原值 |
| 独立后端 `config/model.<ext>` | 配置结构定义：声明配置加载与解析结果对应的类型/结构；例如 Go 使用 `config/model.go` | 与普通源码相同；不得输出 yaml 私密配置原值 |
| 独立后端 `config/yaml/` | 按环境拆分的外部 YAML 配置，例如 `config.prod.yaml`、`config.test.yaml`、`config.local.yaml`；唯一配置模式，只存放配置数据 | 允许有意持久化真实密钥、密码、token、私钥原值；默认不依赖环境变量；不得写入 Agent 输出、日志、README、错误或测试报告 |
| 同仓后端 `backend/config/load.<ext>` | 与独立后端相同的配置加载与解析入口职责，读取 `backend/config/yaml/` 对应环境文件 | 与独立后端相同 |
| 同仓后端 `backend/config/model.<ext>` | 与独立后端相同的配置结构定义职责 | 与独立后端相同 |
| 同仓后端 `backend/config/yaml/` | 与独立后端相同的环境 YAML 命名规则，只存放配置数据 | 与独立后端相同 |

## 环境拆分与命名

`config/yaml/` 模式下：

- 外部 YAML 文件名使用点中缀 `config.<env>.yaml`（Go 生态主流命名，如 `config.local.yaml`）；已有项目使用 `.yml` 时，`config.<env>.yml` 也属于兼容合法形式。
- 外部 YAML 文件不加 `_yaml` 后缀：它保持外部配置文件形态，不存在语言保留命名冲突；Go 语言通过编译期嵌入（见下节）编入二进制。
- 示例：

```text
config/
└── yaml/
    ├── config.prod.yaml
    ├── config.test.yaml
    └── config.local.yaml
```

## Go 编译期嵌入（config/load.go）

Go 项目推荐在 `config/load.go` 中使用标准库 `embed` 将 `config/yaml/` 下的 YAML 在编译期嵌入二进制。配置保持外部 YAML 文件形态（业界模式），运行时按环境从 `embed.FS` 读取，不依赖部署目录或环境变量：

```go
// config/load.go
package config

import (
    "embed"
    "fmt"
)

//go:embed yaml/config.*.yaml
var configFiles embed.FS

// Load 按环境返回 yaml/ 下对应配置文件的原始内容。
func Load(env string) ([]byte, error) {
    name := "yaml/config." + env + ".yaml"
    data, err := configFiles.ReadFile(name)
    if err != nil {
        return nil, fmt.Errorf("读取配置 %s: %w", name, err)
    }
    return data, nil
}
```

- 该方案参考业界 go:embed 编译加载实践（例如 EllipalNodeSync 的 `//go:embed config*.yml` 模式），落点统一为 `config/load.go`，不引入 build tag 与全局 reader 注入。
- `//go:embed yaml/config.*.yaml` 只嵌入 `yaml/` 下匹配 `config.*.yaml` 的配置文件，不嵌入目录内其他文件；使用 `.yml` 扩展名的项目将 embed 模式与 Load 中的扩展名相应改为 `yaml/config.*.yml` / `.yml`。
- 选用该方案的项目必须先提交至少一个环境配置（建议 `config.local.yaml` 作为默认环境基线）：`//go:embed` 在 `config/yaml/` 无匹配文件时 `go build` 会报 `no matching files found`。
- 编译期嵌入意味着所有环境的配置（含私密原值）随二进制分发，仍禁止向 Agent 输出、日志、README、错误或测试报告泄露。
- 非 Go 语言（Java/Node/Python）的 `load.<ext>` 从文件系统读取 `yaml/config.<env>.yaml`，go:embed 仅 Go 适用。

`<env>` 必须使用小写环境名，格式为 `[a-z][a-z0-9_]*`。`local`、`test`、`prod` 是标准环境名；可以按项目需要扩展为 `dev`、`staging`、`pre_prod` 等合法环境名，但扩展名不改变配置根和文件前缀规则。只检查已有文件，不要求三种环境齐全。

## embedded/ 禁止

`config/embedded/`（含同仓 `backend/config/embedded/`）已废弃，统一使用 `config/yaml/`：

- 新项目不得创建 `config/embedded/` 目录或文件。
- 检查工具（`check` 命令）在 strict 策略下，若发现 `config/embedded/` 存在，必须报错并拒绝（提示已废弃、统一放入 `config/yaml/`）。
- 旧项目渐进采纳时，若收敛清单已将已存在的 `config/embedded/` 目录登记为 `legacy_source_roots`，已登记内容可继续维护，但新配置一律写入 `config/yaml/`；未登记则拒绝。

配置加载、默认值和结构定义只能位于 `config/load.<ext>` 与 `config/model.<ext>`（或同仓的 `backend/config/` 对应文件）；配置数据目录只存放配置数据，不承载加载与结构定义逻辑。禁止创建 `config/examples/`、`config/schema/`、`config/loader/`、`config/defaults/`。

## 环境识别契约

`load.<ext>` 的环境识别按以下优先级返回第一个非空值：命令行 `-env=<value>`（空值视为未设置）> `APP_ENV` > `ENV` > 默认 `local`。`-env` 只支持 `-env=<value>` 等号形式；未知环境沿用 `UnknownEnvironmentError` 非空 + `Validate` 的拒绝启动语义。VSCode 调试启动默认使用 `args: ["-env=local"]`，不依赖 `env.APP_ENV`；`.vscode/launch.json` 只强制至少保留一条 `local开发环境启动`（无 `preLaunchTask`），不要求为 `config.test.yaml`、`config.prod.yaml` 铺满启动配置，但已存在的启动配置其 `-env=<env>` 必须能找到对应环境文件，完整规则见 `vscode-launch-tasks.md`。

环境确定后，加载器读取 `config/yaml/`（或同仓 `backend/config/yaml/`）下的对应环境文件；未找到对应环境的配置文件则拒绝启动。

## 合法与非法示例

合法示例：

- （yaml 模式）独立 Go 后端：`config/load.go`、`config/model.go`、`config/yaml/config.local.yaml`、`config/yaml/config.pre_prod.yml`；`config/load.go` 内通过 `//go:embed yaml/config.*.yaml` 编译期嵌入。
- （yaml 模式）同仓 Go 后端：`backend/config/load.go`、`backend/config/model.go`、`backend/config/yaml/config.test.yaml`。
- 只有部分环境存在：仅有 `config/yaml/config.test.yaml`，不要求补建 `config.local.yaml` 或 `config.prod.yaml`。

非法示例：

- `config/load.yaml`：`load` 只允许当前语言源码扩展名，不能使用 YAML 扩展名承载加载逻辑。
- `config/helper.go`：config/ 根直接源码文件只允许 `load.<ext>` 或 `model.<ext>`。
- `config/load/load.go`：`load` 是根级源码文件命名，不允许建成子目录。
- `config/yaml/prod.yaml`、`config/yaml/config-qa.yaml`、`config/yaml/config.PROD.yaml`：缺少 `config.` 前缀、使用连字符或大写环境名。
- `src/config/config.prod.yaml`、`internal/config/config.local.yaml`、同仓工作区根 `config/yaml/config.test.yaml`：配置根位置错误。
- **`config/embedded/`（含 `backend/config/embedded/`）存在**：已废弃，必须迁入 `config/yaml/`。
- 在 YAML 中有意持久化真实密码、token、私钥或连接串是允许的；仍禁止向 Agent 输出、日志、README、错误或测试报告泄露。

## 二进制入口边界

独立后端的主要入口放在项目根，例如 Go 使用 `main.go`；只有其他独立二进制才使用 `cmd/<binary>/main.go`。`cmd/main.go` 不是合法入口，因为 `cmd/` 只能承载具体二进制目录。前后端同仓时，后端主要入口放在 `backend/main.go`，其他入口放在 `backend/cmd/<binary>/main.go`；工作区根 `main.go` 和工作区根 `cmd/` 均不承担后端入口。
