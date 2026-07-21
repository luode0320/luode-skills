---
name: project-memory-file-bootstrap-rules
description: 当项目根目录的记忆四件套（`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`；`PROJECT_STYLE.md` 按需）任一缺失、需要新会话交接、或长期记忆首次初始化时自动触发；也可被用户“根据 skill 更新项目记忆 / 初始化项目四件套 / 补齐 PROJECT_CURRENT|MEMORY|HISTORY”等显式请求触发。负责检测、创建和结构性维护 `PROJECT_CURRENT.md`（当前状态骨架，覆盖式维护，UTF-8 字节数不得超过 51,200）、`PROJECT_MEMORY.md`（人类阅读区 + 底部机器索引区双区骨架，稳定合并维护）、`PROJECT_HISTORY.md`（只追加历史事件骨架，不覆盖已有内容）三个文件的结构与大小闸门；不负责从代码或对话中抽取具体业务事实、实体关系或历史事件内容，事实抽取仍由 `project-memory-rules` 负责，`PROJECT_STYLE.md` 的风格合并仍由 `project-style-rules` 负责。不负责 `AGENTS.md` / `CLAUDE.md` 规则文件或 `.gitattributes` / `.editorconfig`，那部分由 `project-rule-file-bootstrap-rules` 负责；两者共用同一份 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 作为唯一执行入口，不重复实现或复制脚本逻辑。
---

# 项目记忆四件套自举 Skill

## 目标

- 让项目记忆四件套在新会话中稳定可用，把“当前状态、稳定规则、历史事件”从会话记忆转成仓库常驻文件。
- 只负责结构骨架、大小闸门和幂等补齐，不越权替代 `project-memory-rules` 的事实抽取职责。

## 四件套职责边界

| 目标文件 | 本 skill 职责 | 不属于本 skill |
|---|---|---|
| `PROJECT_CURRENT.md` | 缺失时创建状态骨架；已存在时检查 UTF-8 与 51,200 字节上限，不重写已有内容 | 当前状态的具体内容覆盖维护（由记忆流程负责） |
| `PROJECT_MEMORY.md` | 缺失时创建双区骨架；已存在但缺少 `## 机器索引区` 时只补底部受管区；双区完整时只做最小同步 | 事实抽取、实体关系更新（由 `project-memory-rules` 负责） |
| `PROJECT_HISTORY.md` | 创建追加式骨架；已存在时不得覆盖或重排历史内容 | 具体历史事件的追加内容（由记忆流程负责） |
| `PROJECT_STYLE.md` | 不创建、不检测，只在文档中说明其属于 `project-style-rules` | 风格主文档的创建与合并 |

## 触发条件

- 默认自动触发：新会话中若规则文件已存在但四件套（`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md`）任一缺失，或 `PROJECT_MEMORY.md` 缺少 `## 机器索引区`，必须补齐。
- 用户显式要求：初始化项目记忆四件套；补齐 `PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md`；处理“项目记忆交接”“长期记忆初始化”类请求。
- 统一 md 聚合指令：用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md”等聚合表达时，与 `project-rule-file-bootstrap-rules` 一起触发，各自只处理自己的目标文件，不得只更新其中一个就收口。
- 不在本 skill 触发范围：`AGENTS.md` / `CLAUDE.md` / `.gitattributes` / `.editorconfig` 的缺失或同步，改由 `project-rule-file-bootstrap-rules` 处理。

## 执行步骤

1. 调用共享脚本：`../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`（默认当前目录，可通过 `--repo` 指定仓库；脚本单次运行会顺带同步规则文件，这是共享单进程副作用，不代表越权）。
2. 定位项目根目录，检查 `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md` 是否存在。
3. 缺失 `PROJECT_CURRENT.md` 时创建状态骨架；已存在时只检查 UTF-8 与 51,200 字节上限，不重写已有内容。
4. 缺失 `PROJECT_MEMORY.md` 时创建双区骨架；已存在但缺少 `## 机器索引区` 时只补底部受管区；已存在且双区完整时只做最小同步。
5. 缺失 `PROJECT_HISTORY.md` 时创建追加式骨架；已存在时不得覆盖或重排历史内容。
6. 执行脚本后必须核对：三个文件是否都存在；`PROJECT_CURRENT.md` 是否未超过 51,200 字节；`PROJECT_MEMORY.md` 是否具备 `## 机器索引区`；`PROJECT_HISTORY.md` 是否已有内容未被覆盖。
7. 若脚本未执行、执行失败、未补齐 `PROJECT_MEMORY.md` 双区骨架、或执行后未核对结果，判定为阻断，禁止宣称已完成自举。
8. 输出结果时逐文件给出：新建 / 更新 / 跳过原因，禁止只给整体一句“已更新”。
9. 不得新增 `PROJECT_MEMORY_INDEX.yaml` 等平行索引文件。

## 脚本用法

- 默认当前目录：`../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`
- 指定仓库：`../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh --repo /path/to/repo`
- 幂等执行：可重复运行，已有骨架不会被覆盖。

## 模板来源

`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` 机器索引区 / `PROJECT_HISTORY.md` 的骨架文字权威来源是 `../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 内的 `PROJECT_CURRENT_TEMPLATE`、`PROJECT_MEMORY_MACHINE_SECTION`、`PROJECT_HISTORY_TEMPLATE` 变量；只读预览见 [`references/项目记忆模板/四件套模板.md`](references/项目记忆模板/四件套模板.md)。

## 边界

- 只负责 `PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 的结构、大小闸门和幂等补齐。
- 不负责规则文件（`AGENTS.md` / `CLAUDE.md`）、`.gitattributes`、`.editorconfig`，遇到这些缺失时移交 `project-rule-file-bootstrap-rules`。
- 不负责从代码或对话中抽取具体事实、实体关系或历史事件内容，移交 `project-memory-rules`；不负责 `PROJECT_STYLE.md` 的创建与合并，移交 `project-style-rules`。
- 不新建脚本副本；`scripts/bootstrap_agents.sh` 物理位置保持在 `project-rule-file-bootstrap-rules/` 目录下，本 skill 通过相对路径 `../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 引用同一份脚本。
- 旧 `project-agents-bootstrap` 已在 CYCLE-SPLIT-02 全部门禁通过并获用户授权后删除；脚本已迁移至 `project-rule-file-bootstrap-rules/scripts/`，本 skill 不受影响。
