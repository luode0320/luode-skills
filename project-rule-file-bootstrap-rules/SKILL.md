---
name: project-rule-file-bootstrap-rules
description: 新会话第一轮默认自动触发，不依赖用户点名；当 Codex 的 `AGENTS.md`、Claude Code 的 `CLAUDE.md`、`.gitattributes`、`.editorconfig`，或项目记忆四件套（`PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md`，`PROJECT_STYLE.md` 按需）任一缺失、结构不完整、需要新会话交接或长期记忆首次初始化时也自动触发；同时兼容“创建、补齐或更新 AGENTS.md / CLAUDE.md”“补充仓库级规则”“根据 skill 更新项目 md”“初始化项目四件套”“补齐 PROJECT_CURRENT / MEMORY / HISTORY”等显式请求。作为项目自举唯一 owner，统一提供 `rule-bootstrap` 与 `memory-bootstrap` 两个条件路由：前者幂等创建或同步规则文件、`.gitattributes`、`.editorconfig` 及受管章节并保护非受管内容，后者维护 `PROJECT_CURRENT.md` 的 UTF-8 与 51,200 字节闸门、`PROJECT_MEMORY.md` 的人类区和机器索引区、`PROJECT_HISTORY.md` 的只追加骨架；不替代 `project-memory-rules` 的事实抽取或 `project-style-rules` 的风格维护。两个路由只使用 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`，不得复制第二份实现；CodeGraph 自动准备语义与触发时机保持不变。
---

# 项目规则与记忆自举 Skill

## AI 环境检测与规则文件约定

本 skill 统一用“规则文件”指代与当前 AI 对应的仓库级配置文件：

- **Codex 环境**：规则文件 = `AGENTS.md`
- **Claude Code 环境**：规则文件 = `CLAUDE.md`

检测方式（按优先级）：

1. 若仓库根目录已存在 `AGENTS.md` 或 `CLAUDE.md` 其中一个，使用已存在的那个。
2. 若两者都不存在，根据当前运行 AI 创建对应文件（Claude → `CLAUDE.md`，Codex → `AGENTS.md`）。
3. 若两者都存在，使用与当前 AI 对应的文件，并在输出中标注另一个文件的存在。

脚本平台传参：`scripts/bootstrap_agents.sh` 默认 `--target codex`。当前 AI 为 Claude Code 时必须显式追加 `--target claude`；两个规则文件都要同步时传 `--target both`。

## 目标

- 以一个 owner 和一个脚本完成仓库规则文件与项目记忆骨架自举，避免重复入口、重复实现和职责漂移。
- 让新会话稳定获得仓库常驻规则、当前状态、稳定记忆与追加式历史记录。
- 保留 `Plan Mode`、代码生成风格、Godot、图像生成、CodeGraph 等既有受管规则和自动准备语义。
- 只维护文件存在性、结构、大小和受管区，不越权抽取业务事实或合并编码风格。

## 条件路由与自动触发

| 路由 | 自动触发条件 | 显式触发别名 | 负责产物 |
|---|---|---|---|
| `rule-bootstrap` | 新会话第一轮；规则文件、`.gitattributes`、`.editorconfig` 任一缺失或受管章节未同步 | 创建、补齐或更新 `AGENTS.md` / `CLAUDE.md`；补充仓库级规则；解决新会话规则遗漏 | `AGENTS.md` / `CLAUDE.md`、`.gitattributes`、`.editorconfig` |
| `memory-bootstrap` | 项目记忆四件套任一缺失；`PROJECT_MEMORY.md` 缺少机器索引区；需要新会话交接或长期记忆首次初始化 | 根据 skill 更新项目 md；初始化项目四件套；补齐 `PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md`；项目记忆交接 | `PROJECT_CURRENT.md`、`PROJECT_MEMORY.md`、`PROJECT_HISTORY.md` |

路由规则：

1. 新会话第一轮默认同时检查两个路由，不依赖用户主动通知。
2. 用户给出“根据 skill 补充更新 md / 根据规则更新 md / 按 skill 更新项目 md”等聚合表达时，同时验收两个路由，不得只完成其中一组文件就收口。
3. 两个路由共享一次脚本执行；路由只决定触发原因、核对重点和逐文件结果，不产生第二套实现。
4. 任一路由未完成前，阻断项目分析、架构梳理、需求、Bug、编码、测试与交付主任务。
5. 若当前处于 `Plan Mode`，首轮自举期间仍须把 `implementation-planning-rules` 默认外壳路由同步进规则文件。

## `rule-bootstrap` 职责

1. 检测并创建当前 AI 对应的根目录规则文件。
2. 同步根目录及子目录所有已存在的 `AGENTS.md` / `CLAUDE.md` 受管章节。
3. 受管章节缺失时追加、已存在时原位更新；用户非受管内容必须保持不变。
4. 缺失 `.gitattributes` 或 `.editorconfig` 时创建最小可用版本；已存在时不得覆盖或反向调整。
5. Godot 项目继续补齐 `Godot 项目工具配置` 与 `图像生成配置`，不得写入真实密钥。

受管章节索引见 [`references/规则文件模板/agents-md-sections-index.md`](references/规则文件模板/agents-md-sections-index.md)，确切写入文字以 `scripts/bootstrap_agents.sh` 对应 heredoc 变量为唯一权威源。

## `memory-bootstrap` 职责

| 目标文件 | 本 skill 职责 | 不属于本 skill |
|---|---|---|
| `PROJECT_CURRENT.md` | 缺失时创建当前状态骨架和唯一失活任务投影槽位；已存在时验证 UTF-8 与 51,200 字节上限，不重写已有内容 | 当前状态的具体内容覆盖维护、活动投影更新和 `update_plan` payload |
| `PROJECT_MEMORY.md` | 缺失时创建人类阅读区与机器索引区双区骨架；机器索引区缺失或 schema 不完整时只补最小受管结构 | 事实抽取、实体关系和长期事实更新 |
| `PROJECT_HISTORY.md` | 缺失时创建追加式骨架；已存在时只验证 UTF-8，不覆盖、不重排历史内容 | 具体历史事件追加 |
| `PROJECT_STYLE.md` | 不创建、不检测，仅保留其由 `project-style-rules` 按需维护的边界 | 风格主文档创建与合并 |

额外约束：

- 不得新增 `PROJECT_MEMORY_INDEX.yaml` 或其他平行机器索引文件。
- `PROJECT_MEMORY.md` 的人类正文属于非受管内容，补齐机器索引区时不得覆盖。
- 新项目模板只提供 `state: inactive` 的空任务投影槽位；既有项目首次补齐、活动状态、指纹、原子写入和失活均由 `task-plan-rehydration-rules` 负责，本 Skill 不扩大“既有文件不重写”边界。
- 模板只读预览见 [`references/项目记忆模板/四件套模板.md`](references/项目记忆模板/四件套模板.md)；执行时写入源仍以唯一脚本内的 `PROJECT_CURRENT_TEMPLATE`、`PROJECT_MEMORY_MACHINE_SECTION`、`PROJECT_HISTORY_TEMPLATE` 为准。

## 统一执行步骤

1. 调用唯一入口 `scripts/bootstrap_agents.sh`；Claude Code 使用 `--target claude`，需要同步双平台规则文件时使用 `--target both`。
2. 只要进入本 skill，就不能停留在“已读取但未落盘”；必须真实执行脚本并核对结果。
3. 按 `rule-bootstrap` 核对规则文件、`.gitattributes`、`.editorconfig` 和全部受管章节，确认非受管内容未被覆盖。
4. 按 `memory-bootstrap` 核对三个项目记忆文件、51,200 字节闸门、机器索引区和历史只追加保护。
5. 输出逐文件结果：新建、更新或跳过及原因；禁止只给整体一句“已更新”。
6. 若脚本失败、只完成部分文件、未核对结果、覆盖非受管内容、`PROJECT_CURRENT.md` 超限、机器索引区未补齐或历史内容被覆盖，判定为阻断。
7. 若仓库命中 Godot 项目标记，额外核对两个 Godot 受管章节及图片配置中不存在密钥原值。
8. 若当前服务器未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载安装并对当前项目执行 `codegraph init`；失败则回退不阻塞主任务。该自动准备仍发生在本 skill 的项目自举阶段，不因 owner 合并而提前、延后或取消。

## 脚本用法

- 默认当前目录：`scripts/bootstrap_agents.sh`
- 指定仓库：`scripts/bootstrap_agents.sh --repo /path/to/repo`
- Claude Code 环境：`scripts/bootstrap_agents.sh --target claude`
- 两种规则文件都要：`scripts/bootstrap_agents.sh --target both`
- 幂等执行：可重复运行，已有受管章节不会重复追加，已有项目记忆正文和历史内容不会被覆盖。

## 边界

- 本 skill 是 `rule-bootstrap` 与 `memory-bootstrap` 的唯一入口和资产 owner。
- 不负责从代码、对话或外部知识库抽取具体事实、实体关系或历史事件内容，移交 `project-memory-rules`。
- 不负责 `PROJECT_STYLE.md` 的创建与合并，移交 `project-style-rules`。
- 不创建第二份脚本；`scripts/bootstrap_agents.sh` 的物理位置和唯一执行入口保持不变。
- CodeGraph 自动安装、初始化、失败回退和项目自举阶段触发语义保持不变，仅由本 owner 继续声明。
- 被合并入口的触发别名、模板和 agent 元数据迁入本 skill 后删除旧目录，不保留竞争入口。
