# 快速入门 — login / project

> 本模块覆盖 `apifox login`、`apifox project`、CLI 基础用法与升级。已从 SKILL.md 继承：安装指引、全局参数、写入标准流程、AI 权限规则。

## 何时加载

- 用户第一次使用 Apifox CLI，或需要登录/切换项目
- 查看/切换/列出项目
- 升级 CLI 或检查版本

## 登录

```bash
apifox login --with-token <TOKEN>
```

Token 从 Apifox 客户端「用户头像 → 账号设置 → API 访问令牌」创建。

> WSL 环境下 `apifox whoami` 显示未登录，但怀疑 Windows 侧已经登录过时，先看 `SKILL.md` 的“跨系统凭据同步（WSL ↔ Windows）”小节，检查并同步 Windows 侧 `~/.apifox/config.toml`，避免不必要的重复 `login --with-token`。

## 项目管理

```bash
# 列出可访问项目
apifox project list

# 查看当前登录状态
apifox whoami
```

## CLI 升级

```bash
# 交互式升级
apifox update

# 非交互/CI 环境
apifox update --yes
```

禁用每日检查（不影响手动 update）：

```bash
export APIFOX_CLI_DISABLE_UPDATE_CHECK=1
```

## cli-schema 命令

```bash
# 列出所有可用 schema
apifox cli-schema list

# 获取某个 schema 定义（create/update 前必做）
apifox cli-schema get <schemaKey>

# 校验 JSON 数据
apifox cli-schema validate <schemaKey> --file <path>
```

## 常用检查流程

1. `apifox --version` — 确认 CLI 可用
2. `apifox --help` — 查看顶层命令
3. `apifox project list` — 确认目标项目
4. `apifox <command> --help` — 查看具体命令参数
5. `apifox cli-schema get <key>` — 获取写入 schema
