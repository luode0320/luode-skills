# 项目当前状态

## 当前任务

- 目标：按冻结的 Skill 体积治理与职责拆分计划，完成 `CYCLE-SPLIT-02` ~ `CYCLE-SPLIT-06` 五个正式拆分周期的技术拆分、仓库路由切换与真实删除，并对 `CYCLE-SPLIT-07`、`CYCLE-SPLIT-08` 两个候选周期完成复评。
- 范围：对每个正式候选（`project-agents-bootstrap`、`skill-compliance-gate-rules`、`project-release-test-rules`、`agent-browser`、`2d-asset-design`）按语义拆成两个职责单一的新 skill，精确扫描并改写全部活跃引用，重跑字典生成脚本核对增量，回归 pre-delete/post-delete 触发用例，登记证据并收口对应实施周期文档；用户明确授权后执行真实删除并修复共享物理资源断链；对 `mcp-installation-rules`、`implementation-planning-rules` 完成复评并记录结论。
- 非范围：不执行 `git commit`/`push`；不回改历史需求/实施/审查文档与既有变更日志条目、"来源:"证据引用。
- 状态：任务已完整闭环。`CYCLE-SPLIT-01`~`06` 全部收口为 `done`；5 个旧 skill 目录已真实删除；2 处发现的共享物理资源断链已修复；`CYCLE-SPLIT-07`（`mcp-installation-rules`）、`CYCLE-SPLIT-08`（`implementation-planning-rules`）复评结论均为 `no_split`。

## 已完成

- `CYCLE-SPLIT-01`：通用拆分测试入口（`validate_skill_split.py`、`run_trigger_cases.ps1`）实现、真实测试、审查、验收四项闭环全部完成并收口。
- `CYCLE-SPLIT-02`：`project-agents-bootstrap` 拆分为 `project-rule-file-bootstrap-rules` + `project-memory-file-bootstrap-rules`；路由切换、真实删除、`bootstrap_agents.sh` 迁移与回归测试全部完成（`TASK-SPLIT-02-06`）。
- `CYCLE-SPLIT-03`：`skill-compliance-gate-rules` 拆分为 `skill-execution-compliance-gate-rules` + `code-change-finalization-gate-rules`；路由切换、真实删除与回归测试完成，mapping 复核无共享资源风险。
- `CYCLE-SPLIT-04`：`project-release-test-rules` 拆分为 `project-interface-baseline-rules` + `project-interface-release-execution-rules`；路由切换、真实删除、`release_test_engine`（25 模块 + 9 适配器 + 兼容入口）迁移与回归测试全部完成（`TASK-SPLIT-04-06`）。
- `CYCLE-SPLIT-05`：`agent-browser` 拆分为 `browser-session-automation-rules` + `browser-advanced-testing-rules`；路由切换、真实删除与回归测试完成，mapping 复核无共享资源风险。
- `CYCLE-SPLIT-06`：`2d-asset-design` 拆分为 `game-asset-design-gate-rules` + `game-asset-production-handoff-rules`；路由切换、真实删除与回归测试完成；额外发现并修复 2 个 references 文件中 4 处现在时活跃描述；字典口径确认该周期为扩展种子例外，`implemented_total` 保持不变属预期结果。
- `CYCLE-SPLIT-07`/`CYCLE-SPLIT-08`：分别对 `mcp-installation-rules`、`implementation-planning-rules` 完成复评，结论均为 `no_split`。
- 用户额外要求"同步调整 AGENTS.md/CLAUDE.md 规则模板中的 Skill 命中强制规则正文"已落实：根目录 `AGENTS.md`/`CLAUDE.md`、`bootstrap_agents.sh` 内写入所有项目的 `BODY_SKILL_HIT`/`BODY_CONTEXT_COMPRESS` 正文、9 个外部 skill 及 `vercel-react-best-practices/AGENTS.md` 内嵌的规则模板副本，均已同步为新 skill 名。
- 每个正式周期均已在 `doc/3-实施/` 对应实施周期文档写入任务顺序表、文件/符号契约、真实测试断言、验证矩阵与追踪矩阵，状态全部收口为 `done`/`closed`；实施总览已追加最终 `CHG-SPLIT-20260721-001` 变更记录，整体状态收口为 `done`。

## 待完成

- 无。本轮任务已完整闭环，无遗留待办。

## 阻断

- 无。

## 验证

- 5 个正式周期均按统一流程验证：`rg` 精确扫描活跃引用（排除 `doc/**`）-> 按 mapping 文件语义拆分改写并用 `assert text.count(old) == 1` 断言安全网落盘 -> 删除前 `certutil -hashfile`/`md5sum` 核对旧 `SKILL.md`、脚本与 mapping 基线一致 -> 真实删除旧目录 -> 重跑 `skill-dictionary/generate_dictionary.py` 核对 `implemented_total=88`/`seed_total=28` 无回归 -> `run_trigger_cases.ps1 -Phase pre-delete/post-delete` 全部 `[通过]` -> 证据文件登记到 `doc/5-tests/2026-07-17_155229/skill-split-validation/evidence/`。
- 额外发现并修复 2 处 `keep_in_place`/`reference_only` 共享物理资源断链（`bootstrap_agents.sh`、`release_test_engine/`），均通过 `git checkout HEAD --` 精确恢复、物理迁移、MD5/文件数/编译语法三重校验后落位，详见 `evidence/TASK-SPLIT-02-06-real-delete-and-script-migration.md`、`evidence/TASK-SPLIT-04-06-real-delete-and-engine-migration.md`。
- `bootstrap` fixture 的 `post-delete` 阶段用例缺失（2026-07-18 创建时的既有缺口，与本次删除无关）；`pre-delete` 阶段全部 `[通过]`；该缺口已登记未回填，因为回填冻结测试资产不在本任务授权范围内。
- 验证环境：仅使用本地工作区、本地 Python/PowerShell/WSL bash，不连接数据库、缓存、消息队列、HTTP/RPC 或业务服务。

## 交接点

- 当前工作树保持"已改动未提交"；本轮及此前各周期均未执行 `git commit`、`push`。
- 下一步动作：向用户汇报 `CYCLE-SPLIT-02`~`06` 技术拆分、真实删除、共享资源迁移与规则模板同步已全部完成；若用户需要提交，需在当轮消息中显式提出。
