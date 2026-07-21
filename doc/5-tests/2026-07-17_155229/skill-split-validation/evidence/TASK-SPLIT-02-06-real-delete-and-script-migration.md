# TASK-SPLIT-02-06 证据：真实删除执行与脚本迁移补漏

## 背景

`CYCLE-SPLIT-02` 此前五个任务（`TASK-SPLIT-02-01` ~ `05`）均已完成实现、真实测试、审查与验收闭环，路由切换在 `TASK-SPLIT-02-04` 完成，删除前承接检查在 `TASK-SPLIT-02-05` 完成，周期状态停留在 `comparing`，唯一剩余动作是旧 `project-agents-bootstrap` 目录删除，等待用户授权。

用户在本轮明确说明“可以删除”，并额外指出“原来的 `AGENTS.md` 和 `CLAUDE.md` 的规则模板要重新调整，这里面之前有 Skill 命中强制规则，拆分后也要继续调整这里的模板文档”，触发本任务：执行真实删除，并核实/修复删除后模板与脚本的完整性。

## 真实删除执行

1. 复核 5 个旧 skill（含 `project-agents-bootstrap`）的 `SKILL.md`/脚本/references MD5 与字节数，与 `mapping/*.yaml` 冻结基线逐一比对，全部一致（`bootstrap_agents.sh`：57586 字节 / 945 行 / MD5 `26e852920c949e429be6b249ffa4af20`，与基线记录的字节/行数完全一致）。
2. 删除 5 个旧 skill 目录：`project-agents-bootstrap`、`skill-compliance-gate-rules`、`project-release-test-rules`、`agent-browser`、`2d-asset-design`。
3. 重跑 `skill-dictionary/generate_dictionary.py`：`implemented_total=88`、`seed_total=28`（迁移脚本落位后二次重跑同样为 88/28，不受脚本物理迁移影响），退出码 0。
4. 重跑 `run_trigger_cases.ps1 -Phase post-delete`：`compliance`、`release-test`、`agent-browser`、`2d-design` 四组 fixture 全部 `[通过]`，输出显式声明未删除或修改任何真实 skill 目录。`bootstrap` fixture 的 `delete_cases.json`/`trigger_cases.json` 只登记了 `pre-delete` 阶段用例、未登记 `post-delete` 阶段用例（2026-07-18 创建时的既有缺口，与本次删除无关）；`pre-delete` 阶段本轮重跑仍全部 `[通过]`。该项已在本证据文件中登记为已知 fixture 缺口，未回填，因为触碰冻结测试资产不在本任务授权范围内。

## 关键发现：`bootstrap_agents.sh` 未随删除完成迁移

`mapping/bootstrap-rules.yaml` 中 `RES-BOOT-SCRIPT` 的设计是 `migration_action: keep_in_place`——脚本物理保留在旧 `project-agents-bootstrap/scripts/` 下，两个新 skill 通过相对路径 `../project-agents-bootstrap/scripts/bootstrap_agents.sh` 共同引用同一份脚本，而不物理复制。这一设计在旧目录被真正删除前是自洽的；但一旦执行真实删除（本轮），该共享路径就会失效——而 `bootstrap_agents.sh` 是两个新 skill 的**唯一真实执行入口**（`SKILL.md` 中"1. 调用共享脚本"步骤直接依赖该路径），并非仅是文档引用。

修复方式：

1. 通过 `git checkout HEAD -- project-agents-bootstrap/scripts/bootstrap_agents.sh` 从提交历史精确恢复该文件（字节数与迁移前完全一致），复制到 `project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`（新的唯一物理位置，owner 由 group_a 承接，33/55 条原子映射项归属于此），MD5 校验一致（`26e852920c949e429be6b249ffa4af20`）后，再次删除 `project-agents-bootstrap`。
2. 脚本自身通过 `$(pwd)` / `--repo` 定位目标仓库，不使用 `$(dirname "$0")` 定位自身，因此物理迁移不影响脚本运行语义。`wsl.exe bash -n` 语法检查通过（exit=0）。

## 模板与引用路径修复（对应用户"AGENTS.md/CLAUDE.md 规则模板调整"要求）

`bootstrap_agents.sh` 内部同时是 **AGENTS.md/CLAUDE.md 受管章节正文的唯一权威来源**（heredoc 变量如 `BODY_SKILL_HIT`、`BODY_CONTEXT_COMPRESS` 会被 `sync_section` 写入目标仓库的规则文件）。脚本内部发现 5 处仍写死旧 skill 名 `project-agents-bootstrap`，其中 `BODY_SKILL_HIT`（Skill 命中强制规则章节正文）与 `BODY_CONTEXT_COMPRESS`（上下文压缩续做规则正文）两处会被同步进**所有使用本脚本自举的项目**的 `AGENTS.md`/`CLAUDE.md`，若不修复会持续把已废弃的旧 skill 名写入未来所有新建/同步的规则文件。已修复：

| 位置 | 修复前 | 修复后 |
|---|---|---|
| 脚本头注释（第4行） | `# project-agents-bootstrap: 检查并补齐...` | `# bootstrap_agents.sh: ...project-rule-file-bootstrap-rules...project-memory-file-bootstrap-rules...` |
| 章节权威源注释（第157行） | `章节内容以 project-agents-bootstrap 最小模板为权威源` | `章节内容以本脚本（两个新 skill 共用）为权威源` |
| `BODY_SKILL_HIT`（第229行，写入所有项目规则文件） | `默认额外启用 project-agents-bootstrap 进行自举补齐` | `默认额外启用 project-rule-file-bootstrap-rules 进行规则文件自举补齐；若同时涉及项目记忆四件套，联动 project-memory-file-bootstrap-rules` |
| `BODY_CONTEXT_COMPRESS`（第309行，写入所有项目规则文件） | `必须先触发 project-agents-bootstrap 补齐` | `必须先触发 project-rule-file-bootstrap-rules 补齐规则文件；若项目记忆四件套同样缺失，联动 project-memory-file-bootstrap-rules` |
| `PROJECT_HISTORY_TEMPLATE` 示例行（第696行） | `由 project-agents-bootstrap 初始化双区骨架` | `由 project-memory-file-bootstrap-rules 初始化双区骨架` |

同时修复了两个新 skill 自身文档中的相对路径引用（`SKILL.md`、`agents/openai.yaml`、`references/规则文件模板/agents-md-sections-index.md`、`references/项目记忆模板/四件套模板.md`），以及 9 个外部 skill 中对旧路径的活跃引用（`godot-project-bootstrap-rules`、`skill-hit-check-rules`、`mcp-installation-rules`、`windows-wsl-execution-rules`、`project-style-rules`、`context-compression-rules`、`micro-business-architecture-rules` 的 `SKILL.md` 及 `references/*`）与 `项目设计.md` 中的 2 处架构清单条目。`PROJECT_MEMORY.md`、`PROJECT_STYLE.md`、`README.md` 中残留的 `project-agents-bootstrap` 字样均为既有变更日志或证据来源引用的历史记录，按仓库既定规则不回改。

## 修复后回归

- `python -X utf8 skill-dictionary/generate_dictionary.py`：退出码 0，`implemented_total=88`（迁移前后一致）。
- `wsl.exe bash -n project-rule-file-bootstrap-rules/scripts/bootstrap_agents.sh`：exit=0（语法通过）。
- `pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\bootstrap`：全部 `[通过]`（fixture 层面验证不受脚本物理迁移影响，因为 fixture 命令本身不依赖真实脚本路径）。
- `rg -n --fixed-strings "project-agents-bootstrap" --glob "!doc/**"`：仅剩 `PROJECT_MEMORY.md`、`PROJECT_CURRENT.md`、`PROJECT_STYLE.md`、`README.md`、`skill-dictionary/data.js`（机器生成）、两个新 skill 内各一处"旧 skill 已删除"的历史说明；均为预期历史/机器生成内容，无遗留活跃引用。

## 结论

`CYCLE-SPLIT-02` 至此真正完成：删除已执行，脚本物理迁移完成且经 MD5/语法双重校验，所有活跃引用与规则模板正文均已指向新 skill，无功能性回归。周期状态由 `comparing` 收口为 `done`。
