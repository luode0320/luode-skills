# 配置位置规则

项目只有一套配置根：独立后端使用根级 `config/`；前后端同仓时，后端配置统一使用 `backend/config/`。不得在 `src/config/`、`internal/config/`、工作区根 `config/` 或其他位置重复定义同一套后端配置。

| 路径 | 内容 | 安全边界 |
|---|---|---|
| 独立后端 `config/yaml/` | 按环境拆分的外部 YAML 配置，例如 `config_prod.yaml`、`config_test.yaml`、`config_local.yaml` | 禁止真实密钥、密码、token、私钥原值；允许占位符或环境变量引用 |
| 独立后端 `config/embedded/` | 按环境拆分、包含 YAML 字符串的源码文件；Go 例如 `config_prod.go`、`config_test.go`、`config_local.go` | 允许直接写入 API key、密钥、密码等私密信息；源码配置是主来源，默认不依赖环境变量。不得写入 Agent 输出、日志、README、错误或测试报告 |
| 同仓后端 `backend/config/yaml/` | 与独立后端相同的环境 YAML 命名规则 | 与独立后端相同 |
| 同仓后端 `backend/config/embedded/` | 与独立后端相同的 embedded 命名规则 | 与独立后端相同 |

## 环境拆分与命名

外部 YAML 文件名使用 `config_<env>.yaml`；已有项目使用 `.yml` 时，`config_<env>.yml` 也属于兼容合法形式。`<env>` 必须使用小写环境名，格式为 `[a-z][a-z0-9_]*`。`local`、`test`、`prod` 是标准环境名；可以按项目需要扩展为 `dev`、`staging`、`pre_prod` 等合法环境名，但扩展名不改变配置根和文件前缀规则。

Go 的 embedded 文件名使用 `config_<env>.go`，例如：

```text
config/
├── yaml/
│   ├── config_prod.yaml
│   ├── config_test.yaml
│   └── config_local.yaml
└── embedded/
    ├── config_prod.go
    ├── config_test.go
    └── config_local.go
```

其他语言的 embedded 文件本周期只保留该语言既有源码扩展名检查，不套用 Go 的 `config_<env>.go` 文件名契约，也不新增环境名校验。例如 Java、Node.js 或 Python 继续使用项目已有的源码扩展名规则；Go 文件才必须使用 `config_<env>.go`。

`local`、`test`、`prod` 仅定义标准名称，不表示每个项目必须同时提交三种环境文件。目录检查只检查项目中已经存在的文件，不创建或补齐缺失环境；例如只有 `config_local.yaml` 和 `config_prod.go` 也可以通过命名检查。`yaml/` 与 `embedded/` 的环境文件不要求一一配对，文件存在性和命名分别判断，不因缺少对应环境的另一种格式而失败。

配置加载、默认值和结构定义只能位于对应项目配置根及其允许的语言源码中；环境拆分不产生第二套配置根。禁止创建 `config/examples/`、`config/schema/`、`config/loader/`、`config/defaults/`。

## 合法与非法示例

合法示例：

- 独立 Go 后端：`config/yaml/config_local.yaml`、`config/yaml/config_pre_prod.yml`、`config/embedded/config_prod.go`。
- 同仓 Go 后端：`backend/config/yaml/config_test.yaml`、`backend/config/embedded/config_local.go`。
- 只有部分环境存在：仅有 `config/yaml/config_test.yaml`，不要求补建 `config_local.yaml` 或 `config_prod.yaml`。
- 环境未配对：存在 `config/yaml/config_prod.yaml` 但没有 `config/embedded/config_prod.go`，仍不因配对缺失而失败。

非法示例：

- `config/yaml/prod.yaml`、`config/yaml/config-qa.yaml`、`config/yaml/config_PROD.yaml`：缺少 `config_` 前缀、使用连字符或大写环境名。
- `config/embedded/config_test_yaml.go`、`config/embedded/config.yaml.go`：不符合 `config_<env>.<源码扩展名>` 形式。
- `src/config/config_prod.yaml`、`internal/config/config_local.yaml`、同仓工作区根 `config/yaml/config_test.yaml`：配置根位置错误。
- 在 YAML 中直接写入真实密码、token、私钥或连接串：违反秘密原值边界；embedded 源码按本规则允许这些私密信息，但仍禁止向 Agent 输出、日志、README、错误或测试报告泄露。

## 二进制入口边界

独立后端的主要入口放在项目根，例如 Go 使用 `main.go`；只有其他独立二进制才使用 `cmd/<binary>/main.go`。`cmd/main.go` 不是合法入口，因为 `cmd/` 只能承载具体二进制目录。前后端同仓时，后端主要入口放在 `backend/main.go`，其他入口放在 `backend/cmd/<binary>/main.go`；工作区根 `main.go` 和工作区根 `cmd/` 均不承担后端入口。
