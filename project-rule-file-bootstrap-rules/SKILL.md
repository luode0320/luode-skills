---
name: project-rule-file-bootstrap-rules
description: 若当前 AI 为 Claude Code，目标规则文件为 `CLAUDE.md`；若为 Codex，目标规则文件为 `AGENTS.md`；新会话第一轮默认自动触发（不依赖用户意图），且在规则文件、`.gitattributes`、`.editorconfig` 任一缺失或未完成受管章节同步前，阻断其余项目分析、需求、Bug、编码、测试与交付主任务；也可被“创建、补齐或更新 AGENTS.md / CLAUDE.md / 补充仓库级规则”等显式请求触发。负责在项目根目录检测并创建缺失的规则文件、`.gitattributes`、`.editorconfig`，并对已存在的规则文件持续执行受管章节的增量幂等 upsert（覆盖 Skill 强制触发、严禁脑补工具调用、严禁自动提交 Git、Skill 命中强制规则、代码生成风格入口、Windows/WSL 执行、CodeGraph、插件检测、图像生成等章节），保留用户已有的非受管内容。若仓库命中 Godot 项目标记，还需额外补齐 Godot 工具接管与图像生成配置章节。不负责 `PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 四件套内容，四件套自举由 `project-memory-file-bootstrap-rules` 负责；两者共用同一份 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 作为唯一执行入口，不重复实现或复制脚本逻辑。
---

# 规则文件自举 Skill

## AI 环境检测与规则文件约定

本 skill 统一用“规则文件”指代与当前 AI 对应的仓库级配置文件：

- **Codex 环境**：规则文件 = `AGENTS.md`
- **Claude Code 环境**：规则文件 = `CLAUDE.md`

检测方式（按优先级）：

1. 若仓库根目录已存在 `AGENTS.md` 或 `CLAUDE.md` 其中一个，使用已存在的那个。
2. 若两者都不存在，根据当前运行 AI 创建对应文件（Claude → `CLAUDE.md`，Codex → `AGENTS.md`）。
3. 若两者都存在，使用与当前 AI 对应的文件，并在输出中标注另一个文件的存在。

脚本平台传参：`scripts/bootstrap_agents.sh` 默认 `--target codex`。当前 AI 为 Claude Code 时必须显式追加 `--target claude`，否则会按默认值创建/同步 `AGENTS.md` 而非 `CLAUDE.md`；两个规则文件都要同步时传 `--target both`。

## 目标

- 让仓库在新会话中也能稳定执行项目规则，把“会话记忆”转成“仓库常驻约束”。
- 把 `Plan Mode` 的默认计划外壳、代码生成风格入口沉到仓库级规则里，保证计划型提问和代码改动都先经过对应 skill。
- 若仓库是 Godot 项目，自动补齐 Godot 工具接管和图像生成配置模板。

## 触发条件

- 默认自动触发（强制）：
  - 新会话第一轮必须执行本 skill。
  - 首轮执行时必须先做一次根目录规则文件检测，并同时检查 `.gitattributes`、`.editorconfig` 是否存在且满足最小可用约束。
  - 三者全部完成自举前，禁止进入项目分析、架构梳理、代码阅读、需求、Bug、编码、测试与交付主任务。
  - 若当前处于 `Plan Mode`，首轮自举期间必须先把 `implementation-planning-rules` 的默认外壳路由同步进规则文件。
- 用户显式要求：创建 `AGENTS.md` / `CLAUDE.md`；自动检查并补齐规则文件；补充仓库级执行规则；解决“新会话规则遗漏”。
- 兜底触发：任意阶段检测到仓库根目录缺失规则文件，必须立即补齐后再继续主任务。
- 不在本 skill 触发范围：`PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` 四件套缺失、交接或长期记忆初始化，改由 `project-memory-file-bootstrap-rules` 处理；用户给出“根据 skill 更新项目 md”等聚合指令时，两个 skill 一起触发，互不覆盖对方职责。

## 执行步骤

1. 调用共享脚本：`scripts/bootstrap_agents.sh`（默认当前目录，可通过 `--repo` 指定仓库）。Claude Code 环境必须显式追加 `--target claude`；Codex 环境可不传。
2. 只要进入本 skill，就不能停留在“已读取规则但未落盘”的状态；必须真的执行脚本。
3. 若仓库内已存在多个规则文件（例如根目录与 `game/AGENTS.md`），必须同步所有已存在规则文件的受管章节，不能只更新根目录后静默忽略子工程规则文件。
4. 若不存在规则文件：必须创建最小可用规则文件（禁止跳过）。
5. 若存在：对受管章节做增量同步，缺失则追加，已存在则更新为最新规则，非受管内容保持不动。
6. 若仓库根目录缺失 `.gitattributes` 或 `.editorconfig`，必须一并补齐最小可用版本。
7. 若首轮尚未完成规则文件、`.gitattributes`、`.editorconfig` 中任一项，必须立即停止后续主任务，只允许继续完成这些文件更新。
8. 执行脚本后必须核对：受管章节是否真的写入最新内容；是否同步到了所有已存在的规则文件；`git diff -- AGENTS.md CLAUDE.md .gitattributes .editorconfig */AGENTS.md` 或等价检查中是否只出现预期改动。
9. 若脚本未执行、执行失败、只同步了部分规则文件、或执行后未核对结果，判定为阻断，禁止宣称已完成自举。
10. 若仓库命中 Godot 项目标记，还需确认 `Godot 项目工具配置` 与 `图像生成配置` 两个受管章节已写入；图像配置块只能声明读取位置、`baseurl`、模型名、优先级和回退规则，不能写真实密钥。
11. 若当前服务器未安装 `codegraph`，必须从 `colbymchenry/codegraph` 强制下载安装并对当前项目执行 `codegraph init`；失败则回退不阻塞主任务。
12. 输出结果时给出：规则文件是否新建/更新、受影响的规则文件列表、`.gitattributes` / `.editorconfig` 是否新建/更新、更新了哪些受管章节。

## 脚本用法

- 默认当前目录：`scripts/bootstrap_agents.sh`
- 指定仓库：`scripts/bootstrap_agents.sh --repo /path/to/repo`
- Claude Code 环境：`scripts/bootstrap_agents.sh --target claude`
- 两种规则文件都要：`scripts/bootstrap_agents.sh --target both`
- 幂等执行：可重复运行，已有章节不会重复追加；脚本同一次运行内会顺带补齐项目记忆四件套骨架（`ensure_project_current_file`、`ensure_project_history_file`、`sync_project_memory_file`），这是脚本层面的共享单进程副作用，不代表本 skill 接管四件套的结构维护职责——结构维护职责仍在 `project-memory-file-bootstrap-rules`。

## 受管章节内容来源

本 skill 正文不重复受管章节全文，避免与脚本内容产生第二份漂移副本。章节标题、对应脚本变量和用途索引见 [`references/规则文件模板/agents-md-sections-index.md`](references/规则文件模板/agents-md-sections-index.md)；确切文字以 `scripts/bootstrap_agents.sh` 内对应 heredoc 变量为准。

## 边界

- 只负责规则文件（`AGENTS.md` / `CLAUDE.md`）、`.gitattributes`、`.editorconfig` 的检测、创建和受管章节同步。
- 不负责 `PROJECT_CURRENT.md` / `PROJECT_MEMORY.md` / `PROJECT_HISTORY.md` / `PROJECT_STYLE.md` 的结构、大小闸门或事实内容，遇到这些文件的缺失或交接需求时移交 `project-memory-file-bootstrap-rules`（四件套结构）或 `project-memory-rules` / `project-style-rules`（事实与风格抽取）。
- 不新建脚本副本；`scripts/bootstrap_agents.sh` 物理位置保持在本 skill（`project-rule-file-bootstrap-rules/`）目录下，`project-memory-file-bootstrap-rules` 通过相对路径 `../project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh` 引用同一份脚本。
- 旧 `project-agents-bootstrap` 已在 CYCLE-SPLIT-02 全部门禁通过并获用户授权后删除（脚本迁移前完成 MD5/字节数复核，迁移后回归验证通过）；本 skill 是唯一执行入口的现任 owner。
