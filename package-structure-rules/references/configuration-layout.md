# 配置位置规则

项目只有根级 `config/`，不得在 `src/config/`、`internal/config/` 或第二套配置目录重复定义。

| 路径 | 内容 | 安全边界 |
|---|---|---|
| `config/yaml/` | 外部 YAML 配置 | 禁止真实密钥、密码、token、私钥原值 |
| `config/embedded/` | `config_test_yaml.go` 等包含 YAML 字符串的源码文件 | 仅后端受限私有仓库在明确授权后可编译秘密进二进制；不得写入日志、README、错误或测试报告 |

配置加载、默认值和结构定义直接位于根 `config/` 的语言文件中；禁止创建 `config/examples/`、`config/schema/`、`config/loader/`、`config/defaults/`。
