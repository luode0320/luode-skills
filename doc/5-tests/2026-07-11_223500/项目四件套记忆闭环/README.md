# 项目四件套记忆闭环测试

## 测试目的

验证项目本地四件套的缺失创建、幂等复跑、职责边界和 current 大小闸门，并确认 Obsidian 固定 vault 的 CLI 读写链路可用。

## 测试对象

- `project-agents-bootstrap/scripts/bootstrap_agents.sh`
- `obsidian-knowledge-flow`、`project-memory-rules`、`project-agents-bootstrap` 三个 skill 资产
- 项目根目录 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`

## 执行方式与环境

- 执行环境：Windows 本地临时仓库；不连接数据库、缓存、消息队列或业务服务。
- Shell：Git Bash；脚本入口：`project-agents-bootstrap/scripts/bootstrap_agents.sh --target both`。
- Python：`python -X utf8`；skill 校验使用 `.system/skill-creator/scripts/quick_validate.py`。
- Obsidian CLI：固定 vault `D:\obsidian_data\知识库`，版本 `1.12.7`。

## 覆盖范围

1. 三个项目记忆文件全部缺失时创建。
2. 重复运行不覆盖已有 `PROJECT_HISTORY.md` 内容。
3. `PROJECT_CURRENT.md` 超过 51,200 字节时以非零退出阻断。
4. 三个受影响 skill 的 frontmatter 校验。
5. Obsidian `version`、`vaults verbose`、目标笔记 `search`、`read`、`append` 和读回。

## 真实证据

- ASCII 证据：`../project-agents-bootstrap/verification-results.txt`
- 真实测试入口：`../../../../project-agents-bootstrap/scripts/bootstrap_agents.sh`

## 验证结论

通过。缺失创建、幂等复跑、历史追加保护、current 超限阻断、skill 校验、字典生成、UTF-8 回读、`git diff --check` 和固定 vault CLI 验证均已完成。
