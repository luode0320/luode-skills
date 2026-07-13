# 项目四件套记忆布局

## 目标

项目本地记忆负责当前项目的启动上下文；Obsidian vault 负责跨项目、跨会话的选择性知识检索与沉淀。两条链路必须分开管理。

## 四件套

| 文件 | 位置 | 内容 | 默认策略 |
| --- | --- | --- | --- |
| `AGENTS.md` / `CLAUDE.md` | 项目目录父目录 | 跨项目通用规则 | 新项目或新线程先读 |
| `PROJECT_CURRENT.md` | 项目根目录 | 当前目标、范围、状态、已完成、待办、阻断、验证、交接点 | 读取并覆盖式维护 |
| `PROJECT_MEMORY.md` | 项目根目录 | 稳定项目规则、关键决策和少量长期事实 | 读取并合并维护 |
| `PROJECT_HISTORY.md` | 项目根目录 | 关键历史事件流水 | 默认不读，只追加；卡点或历史追问时窄读 |

## 启动顺序

1. 读取项目目录父目录的当前平台规则文件。
2. 定位项目根目录；缺失 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md` 或 `PROJECT_HISTORY.md` 时创建最小 UTF-8 模板。
3. 读取 `PROJECT_CURRENT.md`。
4. 读取 `PROJECT_MEMORY.md`。
5. 只有历史追问、当前状态不足或出现真实卡点时，才读取 `PROJECT_HISTORY.md`。

## 更新规则

- `PROJECT_CURRENT.md` 覆盖式维护，必须保持在 51,200 字节以内；超限时阻断并先压缩，不得静默截断。
- `PROJECT_MEMORY.md` 只写稳定规则、关键决策和长期事实；同一口径优先回写原条目。已有机器索引区可以继续保留，但不得把当前状态或历史流水写入其中。
- `PROJECT_HISTORY.md` 只追加重要事件，保留日期、事件、影响、结果和关联来源，不覆盖旧事件。
- 不记录或回显 API key、token、密码、私钥、连接串原值和其他敏感配置。
- 项目本地 Markdown 文件使用标准文件工具；Obsidian vault 的检索、读取、创建和追加只能通过公开 bridge（bridge 调用官方 Windows CLI）完成，并固定为 vault root `D:\obsidian_data` 与相对路径前缀 `知识库/`。
- 跨 Windows / WSL 项目身份以 bridge `project-context --root <项目根>` 的 `project_id` 为唯一键；同一 WSL 项目的 Linux、UNC 和 Git Bash 路径只能维护同一个实体，路径别名写入实体字段而不创建重复笔记。

## 优先级

当前用户指令和项目当前代码优先于项目记忆；项目记忆优先于旧历史和 vault 中的旧笔记。存在冲突时保留证据并标记待裁决，不把猜测写成启用事实。
