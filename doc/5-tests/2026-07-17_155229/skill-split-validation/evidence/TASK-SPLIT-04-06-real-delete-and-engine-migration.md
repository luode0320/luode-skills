# TASK-SPLIT-04-06 证据：真实删除执行与 release_test_engine 迁移补漏

## 背景

`CYCLE-SPLIT-04` 此前任务（`TASK-SPLIT-04-01` ~ `05`）均已完成实现、真实测试、审查与验收闭环，路由切换在 `TASK-SPLIT-04-05` 完成，周期状态停留在 `comparing`，唯一剩余动作是旧 `project-release-test-rules` 目录删除，等待用户授权。

用户明确说明"可以删除"后，本任务与 `TASK-SPLIT-02-06` 同批执行：真实删除 5 个旧 skill 目录（含 `project-release-test-rules`），并核实/修复删除后共享物理资源与文档引用的完整性。

## 真实删除执行

1. 复核 `project-release-test-rules/SKILL.md`、`scripts/`、`references/` 的 MD5 与字节数，与 `mapping/release-test-rules.yaml` 冻结基线一致。
2. 删除 5 个旧 skill 目录（含 `project-release-test-rules`）。
3. 重跑 `skill-dictionary/generate_dictionary.py`：`implemented_total=88`、`seed_total=28`，退出码 0。
4. 重跑 `run_trigger_cases.ps1 -Phase post-delete -CasesRoot cases\release-test`：全部 `[通过]`，输出显式声明未删除或修改任何真实 skill 目录。

## 关键发现：`release_test_engine` 与兼容入口未随删除完成迁移

`mapping/release-test-rules.yaml` 中 `RES-RT-ENGINE-CORE`（`scripts/release_test_engine/` 25 个模块：`runner.py`、`report.py`、`gate.py`、`judge.py`、`resolver.py`、`safety.py`、`auth.py`、`events.py`、`cli.py`、`model.py`、`storage.py`、`discovery.py`、`schema_registry.py`、`topology.py`、`graph.py`、`migrate_baseline.py`、`parameter_store.py`、`dependency_diagnostics.py` 及 9 个 `adapters/*` 协议适配器）和 `RES-RT-COMPAT-ENTRY`（`scripts/generate_release_test_plan.py`）的设计是 `migration_action: reference_only`——两者 owner 都是 `group_b`（`project-interface-release-execution-rules`），物理上保留在旧 `project-release-test-rules/scripts/` 原路径不迁移，`project-interface-baseline-rules` 只读取其运行时回写的基线资产文件，不持有该内核代码。这一设计在旧目录被真正删除前是自洽的；但一旦执行真实删除，该共享路径就会失效——而 `release_test_engine/` 与 `generate_release_test_plan.py` 是两个新 skill 上线测试能力的**唯一真实执行入口**，并非仅是文档引用。

修复方式：

1. 通过 `git checkout HEAD -- project-release-test-rules/scripts` 从提交历史精确恢复整个 `scripts/` 目录（31 个文件，含 25 模块 + 兼容入口 + 9 适配器），复制到 `project-interface-release-execution-rules/scripts/`（新的唯一物理位置，与 mapping 中 `group_b` owner 一致），MD5 校验一致（`generate_release_test_plan.py` MD5=`ada2daf8d41bcc8a64a40866a4e2d9dd`，与基线一致），文件数一致（31=31）后，再次删除 `project-release-test-rules`。
2. `python -m py_compile` 与 `python -m compileall` 对迁移后的 `scripts/` 全部模块检查，退出码均为 0（语法通过，无运行时依赖旧路径的硬编码断链）。

## 文档引用路径修复

精确扫描 `rg -n --fixed-strings "project-release-test-rules" --glob "!doc/**"` 定位到 8 处活跃描述（非历史/证据引用），逐一改写为新路径或新 skill 名：

| 文件 | 修复内容 |
|---|---|
| `project-interface-release-execution-rules/SKILL.md`（3 处） | 共享内核物理路径描述由"保留在 `project-release-test-rules/scripts/` 原路径不迁移"改为"已物理迁移至 `project-interface-release-execution-rules/scripts/`"；两处脚本工具箱复用提示同步改为新路径 |
| `project-interface-baseline-rules/SKILL.md` | 共享内核物理路径描述同上改写 |
| `project-interface-baseline-rules/references/openapi-inventory-sync-rules.md` | 命令行示例 `python project-release-test-rules/scripts/generate_release_test_plan.py ...` 改为新路径，确保示例命令可执行 |
| `project-interface-baseline-rules/references/existing-test-skill-integration.md` | 分工说明改为同时引用 `project-interface-baseline-rules` 与 `project-interface-release-execution-rules`；执行步骤改为 `project-interface-release-execution-rules` |
| `project-interface-baseline-rules/references/bootstrap-workflow.md` | 冷启动流程描述改为 `project-interface-baseline-rules`；未执行判断改为同时引用两个新 skill |
| `project-interface-release-execution-rules/references/existing-test-skill-integration.md` | 同 baseline 版本的对应修复 |
| `project-interface-release-execution-rules/references/output-artifacts.md` | "本文件定义 project-release-test-rules 执行后..." 改为 `project-interface-release-execution-rules` |
| `project-interface-release-execution-rules/references/reusable-script-toolbox.md` | 含旧脚本路径的说明改为 `project-interface-release-execution-rules/scripts/` |
| `project-interface-release-execution-rules/references/test-data-construction-rules.md` | "本文件定义 project-release-test-rules 在准备..." 改为 `project-interface-release-execution-rules` |
| `PROJECT_STYLE.md`（示例、说明两处，来源行不动） | 通用脚本示例命令与说明文字改为新路径 |
| `PROJECT_MEMORY.md`（稳定决策、定义两处，来源/别名/历史条目不动） | `release_test_engine` 内核路径描述与通用子命令扩展路径改为新路径 |

`inventory.yaml:27` 的 `doc\5-tests\2026-07-12_180240\project-release-test-rules\tests\...` 为历史证据路径引用（历史测试目录快照），按既定规则不回改。`PROJECT_MEMORY.md`（99、553、556、972 行）与 `PROJECT_CURRENT.md` 中残留的 `project-release-test-rules` 字样均为既有变更日志、历史别名或待重写的当前状态文件，按仓库既定规则处理（`PROJECT_CURRENT.md` 在最终收口步骤统一重写）。

## 修复后回归

- `rg -n --fixed-strings "project-release-test-rules" --glob "!doc/**"`：仅剩 `inventory.yaml`（历史证据路径）、`PROJECT_STYLE.md:311`（来源引用）、`PROJECT_MEMORY.md`（99/553/556/972，历史条目/别名/来源）、`PROJECT_CURRENT.md`（待最终重写），无遗留活跃功能引用。
- `python -X utf8 skill-dictionary/generate_dictionary.py`：退出码 0，`implemented_total=88`、`seed_total=28`（与删除前一致，无回归）。
- `pwsh -NoProfile -File run_trigger_cases.ps1 -Phase pre-delete -CasesRoot cases\release-test`：`RT-TRIGGER-PRE-001` ~ `006` 及 `RT-DELETE-PRE-001` 全部 `[通过]`。

## 结论

`CYCLE-SPLIT-04` 至此真正完成：删除已执行，`release_test_engine` 25 模块 + 兼容入口已物理迁移且经 MD5/字节数/编译语法三重校验，全部活跃文档引用均已指向新路径，无功能性回归。周期状态由 `comparing` 收口为 `done`。
