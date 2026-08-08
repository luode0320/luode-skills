# 配置位置规则

项目只有一套配置根：独立后端使用根级 `config/`；前后端同仓时，后端配置统一使用 `backend/config/`。不得在 `src/config/`、`internal/config/`、工作区根 `config/` 或其他位置重复定义同一套后端配置。

`test/` 与 `mock/` 目录均不承载独立的 `config/` 配置目录。测试和 Mock 所需的配置统一使用项目 `config/` 下的 `test` 环境（例如 `config/embedded/config_test_yaml.go` 或 `config/yaml/config_test.yaml`），不得在 `test/config/` 或 `mock/config/` 下另建配置根。

## 配置模式选择（二选一，互斥）

`config/embedded/` 与 `config/yaml/` 是两种互斥的配置模式，一个项目只能选择其中一种，不可并存。优先使用 `config/embedded/`。

| 路径 | 内容 | 安全边界 |
|---|---|---|
| 独立后端 `config/load.<ext>` | 配置加载与解析入口：读取所选配置模式（`config/embedded/` 或 `config/yaml/`）的对应环境文件，并解析为配置结构；环境识别支持 `-env`、`APP_ENV`、`ENV`，优先级 `-env > APP_ENV > ENV > local`；例如 Go 使用 `config/load.go` | 与普通源码相同；不得输出 embedded 私密配置原值 |
| 独立后端 `config/model.<ext>` | 配置结构定义：声明配置加载与解析结果对应的类型/结构；例如 Go 使用 `config/model.go` | 与普通源码相同；不得输出 embedded 私密配置原值 |
| 独立后端 `config/embedded/` | **（推荐）** 按环境拆分、包含 YAML 字符串的源码文件；Go 例如 `config_prod_yaml.go`、`config_test_yaml.go`、`config_local_yaml.go` | 允许直接写入 API key、密钥、密码等私密信息；源码配置是主来源，默认不依赖环境变量。不得写入 Agent 输出、日志、README、错误或测试报告 |
| 独立后端 `config/yaml/` | 按环境拆分的外部 YAML 配置，例如 `config_prod.yaml`、`config_test.yaml`、`config_local.yaml` | 禁止真实密钥、密码、token、私钥原值；允许占位符或环境变量引用 |
| 同仓后端 `backend/config/load.<ext>` | 与独立后端相同的配置加载与解析入口职责，读取所选配置模式对应环境文件 | 与独立后端相同 |
| 同仓后端 `backend/config/model.<ext>` | 与独立后端相同的配置结构定义职责 | 与独立后端相同 |
| 同仓后端 `backend/config/embedded/` | **（推荐）** 与独立后端相同的 embedded 命名规则，只存放配置数据 | 与独立后端相同 |
| 同仓后端 `backend/config/yaml/` | 与独立后端相同的环境 YAML 命名规则，只存放配置数据 | 与独立后端相同 |

## 环境拆分与命名

选择 `config/embedded/` 模式时：

- Go 文件名使用 `config_<env>_yaml.go`，格式名 `yaml` 必须后置。`config_<env>.go` 会撞上语言保留命名：Go 把 `config_test.go` 当成测试文件，`go build` 会把它排除、`go test` 会把它编译进测试包，而 `test` 恰好是标准环境名。把格式名放到环境名之后，环境文件就不再落进任何语言的保留命名空间。
- 环境名本身不得以 `_yaml` 结尾，避免 `config_test_yaml_yaml.go` 这类无法唯一切分的文件名。
- 其他语言的 embedded 文件只保留该语言既有源码扩展名检查，不套用 Go 的 `config_<env>_yaml.go` 文件名契约。
- 示例：

```text
config/
└── embedded/
    ├── config_prod_yaml.go
    ├── config_test_yaml.go
    └── config_local_yaml.go
```

选择 `config/yaml/` 模式时：

- 外部 YAML 文件名使用 `config_<env>.yaml`；已有项目使用 `.yml` 时，`config_<env>.yml` 也属于兼容合法形式。
- 外部 YAML 文件不加 `_yaml` 后缀：它不参与任何语言的编译，不存在保留命名冲突。
- 示例：

```text
config/
└── yaml/
    ├── config_prod.yaml
    ├── config_test.yaml
    └── config_local.yaml
```

`<env>` 必须使用小写环境名，格式为 `[a-z][a-z0-9_]*`。`local`、`test`、`prod` 是标准环境名；可以按项目需要扩展为 `dev`、`staging`、`pre_prod` 等合法环境名，但扩展名不改变配置根和文件前缀规则。只检查已有文件，不要求三种环境齐全。

## 互斥约束

`config/embedded/` 与 `config/yaml/` 是互斥的配置模式，严格禁止同时存在于同一项目的配置根下：

- 选择了 `config/embedded/` 的项目，不得在其配置根下创建 `config/yaml/` 目录或文件。
- 选择了 `config/yaml/` 的项目，不得在其配置根下创建 `config/embedded/` 目录或文件。
- 检查工具（`check` 命令）在 strict 策略下，若发现 `config/embedded/` 与 `config/yaml/` 同时存在，必须报错并拒绝。
- 旧项目渐进采纳时，若收敛清单已将已存在的配置目录登记为 `legacy_source_roots`，另一模式仍然不允许新建，但已存在的旧模式目录可继续维护。

配置加载、默认值和结构定义只能位于 `config/load.<ext>` 与 `config/model.<ext>`（或同仓的 `backend/config/` 对应文件）；配置数据目录只存放配置数据，不承载加载与结构定义逻辑。禁止创建 `config/examples/`、`config/schema/`、`config/loader/`、`config/defaults/`。

## 环境识别契约

`load.<ext>` 的环境识别按以下优先级返回第一个非空值：命令行 `-env=<value>`（空值视为未设置）> `APP_ENV` > `ENV` > 默认 `local`。`-env` 只支持 `-env=<value>` 等号形式；未知环境沿用 `UnknownEnvironmentError` 非空 + `Validate` 的拒绝启动语义。VSCode 调试启动默认使用 `args: ["-env=local"]`，不依赖 `env.APP_ENV`。

环境确定后，加载器读取所选配置模式下的对应环境文件；未找到对应环境的配置文件则拒绝启动。

## 合法与非法示例

合法示例：

- （embedded 模式）独立 Go 后端：`config/load.go`、`config/model.go`、`config/embedded/config_prod_yaml.go`、`config/embedded/config_local_yaml.go`。
- （embedded 模式）同仓 Go 后端：`backend/config/load.go`、`backend/config/model.go`、`backend/config/embedded/config_local_yaml.go`。
- （yaml 模式）独立 Go 后端：`config/load.go`、`config/model.go`、`config/yaml/config_local.yaml`、`config/yaml/config_pre_prod.yml`。
- （yaml 模式）同仓 Go 后端：`backend/config/load.go`、`backend/config/model.go`、`backend/config/yaml/config_test.yaml`。
- 只有部分环境存在：仅有 `config/embedded/config_test_yaml.go`，不要求补建 `config_local_yaml.go` 或 `config_prod_yaml.go`。

非法示例：

- `config/load.yaml`：`load` 只允许当前语言源码扩展名，不能使用 YAML 扩展名承载加载逻辑。
- `config/helper.go`：config/ 根直接源码文件只允许 `load.<ext>` 或 `model.<ext>`。
- `config/load/load.go`：`load` 是根级源码文件命名，不允许建成子目录。
- `config/yaml/prod.yaml`、`config/yaml/config-qa.yaml`、`config/yaml/config_PROD.yaml`：缺少 `config_` 前缀、使用连字符或大写环境名。
- `config/embedded/config_test.go`：缺少 `_yaml` 后缀，且会被 Go 当成测试文件。
- `config/embedded/config_test_yaml_yaml.go`：环境名以 `_yaml` 结尾，环境名与格式名无法唯一切分。
- `config/embedded/config.yaml.go`：不符合 `config_<env>_yaml.<源码扩展名>` 形式。
- `src/config/config_prod.yaml`、`internal/config/config_local.yaml`、同仓工作区根 `config/yaml/config_test.yaml`：配置根位置错误。
- **`config/embedded/` 与 `config/yaml/` 同时存在**：违反互斥约束，必须只保留一种配置模式。
- 在 YAML 中直接写入真实密码、token、私钥或连接串：违反秘密原值边界；embedded 源码按本规则允许这些私密信息，但仍禁止向 Agent 输出、日志、README、错误或测试报告泄露。

## 二进制入口边界

独立后端的主要入口放在项目根，例如 Go 使用 `main.go`；只有其他独立二进制才使用 `cmd/<binary>/main.go`。`cmd/main.go` 不是合法入口，因为 `cmd/` 只能承载具体二进制目录。前后端同仓时，后端主要入口放在 `backend/main.go`，其他入口放在 `backend/cmd/<binary>/main.go`；工作区根 `main.go` 和工作区根 `cmd/` 均不承担后端入口。
