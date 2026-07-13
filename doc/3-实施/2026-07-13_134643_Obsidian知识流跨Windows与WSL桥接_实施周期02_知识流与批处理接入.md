---
schema_version: 1
doc_id: CYCLE-OBS-02-IMPL
doc_type: implementation_cycle
source_ids: [REQDOC-OBS-20260713]
status: confirmed
version: 1.0
template_version: 1
complexity: L2
baseline_commit: unknown
current_slice: CYCLE-OBS-03
updated_at: 2026-07-13 18:28:00
---

# CYCLE-OBS-02 知识流与批处理接入

图片资产决策：N/A + 原因：本周期只迁移 CLI 入口、规则和测试资产 + 证据：TASK-OBS-05 至 TASK-OBS-08。

## 当前代码/文档基线

CYCLE-OBS-01 已以 Windows 自动启动 `started_app=true`、Windows/WSL smoke 和 `33/33` 离线测试收口。CYCLE-OBS-02 继续保持目标 vault 操作归并到 bridge；TASK-OBS-08 完成后允许进入 CYCLE-OBS-03。

## 当前周期目标、边界与进入条件

目标：`distill_vault.py`、Skill 入口和 references 都通过固定 bridge 使用 `D:\obsidian_data` 与 `知识库/`。边界：不扩展 Linux CLI、远程 vault 或常驻服务。进入条件：CYCLE-OBS-01 已通过，P0/P1 bridge 缺口为零。

## 周期内最小任务执行顺序

图形目的：保证每项接入先完成自己的实现、真实测试、审查和验收。关联 ID：CYCLE-OBS-02、TASK-OBS-05 至 TASK-OBS-08。

```mermaid
flowchart LR
  T5[TASK-OBS-05 批处理迁移] --> T6[TASK-OBS-06 Skill 入口]
  T6 --> T7[TASK-OBS-07 references]
  T7 --> T8[TASK-OBS-08 端到端验证]
```

## 最小任务闭环

| 任务 | 文件/符号 | 真实测试 | 完成条件 | 停止/回滚 |
| --- | --- | --- | --- | --- |
| TASK-OBS-05 | `scripts/distill_vault.py`、`skills/obsidian-knowledge-flow/test_distill_vault.py` | mock bridge fixture、受控实机 dry-run、nested root 负向测试 | 目标路径以 `知识库/` 开头；无旧 target transport；所有目标操作只调用 bridge | nested root 返回 `LEGACY_NESTED_VAULT_MODEL`，不写目标 vault |
| TASK-OBS-06 | `SKILL.md`、`agents/openai.yaml`、`project-memory-layout.md`、`note-schema.md` | Windows/WSL/检索/不适用/doctor failure 路由断言 | 所有 Agent 入口指向 bridge，canonical project ID 只保留一个实体 | 若仍将 WSL 无原生 CLI 当阻断或直接拼 CLI 则停止；原因：会绕过 bridge；证据：TEST-OBS-015 |
| TASK-OBS-07 | CLI/vault/流程/案例/清单 references | bridge 场景与 TEST 映射断言 | 唯一 root、有限恢复和 CLI-only 一致 | 出现文件系统 fallback 或硬编码知识库 selector 则停止 |
| TASK-OBS-08 | 当前测试时间戳目录 | Windows/WSL search/create/append/read、10KB、failure matrix | 无重复笔记且每写入有 readback | 任一写入无 CLI read 证据则停止 |

## 当前周期验证矩阵

| TEST | 断言 | 状态 |
| --- | --- | --- |
| TEST-OBS-014 | 3 批次 4 篇 fixture、目标路径、rollup、INDEX、脱敏与 legacy root | PASS |
| TEST-OBS-015 | Windows/WSL/检索/普通任务/doctor failure 规则路由 | PASS |
| TEST-OBS-016 | CLI/vault/流程/案例/清单 bridge-only 与 TEST 映射 | PASS |
| TEST-OBS-004/013 | WSL create/append 与 Windows readback | PASS |
| TEST-OBS-010 | 10KB 中文分块 readback | PASS |

## 周期阻断、停止与回滚

若 bridge doctor 失败、旧 nested root 未阻断、任一写入没有 readback 或文档仍指导直接 CLI/file fallback，停止当前任务；仅撤回本周期新增接入资产，不删除用户笔记。

| 类型 | 停止条件 | 回滚 |
| --- | --- | --- |
| TASK-OBS-05 | target root 不等于固定根或 fixture 写入无 readback | 回退 `distill_vault.py` 本周期 bridge 接入，不恢复 nested root 默认值 |
| TASK-OBS-06~08 | 任一入口绕过 bridge 或测试矩阵失败 | 停在当前任务，不进入 CYCLE-OBS-03 |

## 自审结论

### TASK-OBS-05 实现、测试、审查与验收

- 实现：删除 `run_cli()`、vault listing/path comparison 与旧 create/append transport；移除无效 `--cli`、`--target-vault`、`--cli-timeout`。目标 create、append、rollup read/INDEX append 直接调用 `run_bridge()`，默认根为 `D:\obsidian_data`，目标路径前缀为 `知识库/30-MOCs/blog-data`。
- 测试：新增 `skills/obsidian-knowledge-flow/test_distill_vault.py`。离线 mock bridge 覆盖 3 批次 4 篇、所有写路径 `知识库/`、rollup、INDEX、敏感值脱敏以及 legacy nested root 无写入；单文件 `2/2 PASS`，目录回归 `35/35 PASS`。
- 实机：Windows `doctor --json` 返回 `ok=true`、`vault_selector=obsidian_data`、`verified=true`；fixture source 的 `distill_vault.py --dry-run` 返回 `total_files=2`、`total_read=2`、`total_errors=0`，未调用 create/append。
- 负向：`--target-root D:\obsidian_data\知识库 --dry-run` 在写入前稳定抛出 `LEGACY_NESTED_VAULT_MODEL`。
- 审查：旧 transport 与无效参数已无调用；`py_compile`、测试与 `git diff --check` 通过。当前任务无 P0/P1；TASK-OBS-05 验收通过，允许进入 TASK-OBS-06。

### TASK-OBS-06 实现、测试、审查与验收

- 实现：Skill、Agent prompt 与项目身份/schema 统一要求 Windows/WSL 只调用 bridge；WSL 缺少原生 CLI 不再单独阻断，只有 bridge doctor 失败才可输出 `Obsidian:阻断`。项目实体新增 `project_id`、三种规范根路径和 `path_aliases`，同一 WSL 项目不创建重复实体。
- 测试：规则路由断言覆盖 Windows、WSL、历史检索、普通任务与 bridge doctor failure，输出 PASS；禁止词扫描未发现硬编码知识库 selector、PATH CLI 阻断或直接 transport 拼接。
- 合规：Skill description 的 stable bridge 路由缺口已最小回补，并已重新生成 `skill-dictionary/data.js` 与 `字典.md`。
- 审查：只修改计划允许的四个入口文件和字典生成物；无 P0/P1。TASK-OBS-06 验收通过，允许进入 TASK-OBS-07。

### TASK-OBS-07 实现、测试、审查与验收

- 实现：CLI 操作、vault 布局、捕获流程、验证清单和失败案例均改为 bridge-only；固定 root `D:\obsidian_data`、prefix `知识库/`、Windows/WSL transport、自动启动限次、UTF-8 分块、readback、有限恢复与 filesystem fallback 禁止已统一。
- 测试：reference scenario 断言 PASS，禁止词扫描没有硬编码知识库 selector、直接版本/注册列表子命令或进程清理指示；TEST-OBS-001/003/004/006/007/008/010/011/013/014/015/016 已映射到相应规则。
- 审查：修复 failure casebook 的硬编码知识库 selector P0 漂移，并拆分 interop、自动启动、路径/readback、selector 失败案例；`doc/6-审查/2026-07-13_181500_REQDOC-OBS-20260713_TASK-OBS-07_参考规则与失败案例当前改动总审查.md` 已落盘，无 P0/P1。TASK-OBS-07 验收通过，允许进入 TASK-OBS-08。

### TASK-OBS-08 实现、测试、审查与验收

- 实现：保持知识流 retrieve/capture/distill 全部走 bridge allowlist；长正文分块按自然换行消费边界，adapter readback 允许 append 的隐含换行，fake CLI 契约模拟官方 append 前置换行。
- 测试：`python -X utf8 -m unittest discover -s doc/5-tests/2026-07-13_134643/skills/obsidian-knowledge-flow -p 'test_*.py' -v` 返回 `35/35 PASS`；PowerShell parser 与 Python `py_compile` 均 PASS。
- 实机：Windows/WSL search 均 `ok=true`、`verified=true`；WSL 长正文 create 后 Windows/WSL readback 完全一致（13321 chars、LF 181、MD5 `C46A83642C092EF2185BD74572302FB0`）；WSL append 后双端 readback 一致（172 chars、LF 11、MD5 `27ec6c195d225b9d6f602d42394a0baa`）。
- 审查：失败矩阵覆盖 interop、应用恢复、vault selector、path traversal、timeout 与 legacy nested root；未发现重复项目实体、重复目标笔记或 filesystem fallback。`doc/6-审查/2026-07-13_184500_REQDOC-OBS-20260713_TASK-OBS-08_端到端验证当前改动总审查.md` 结论 PASS。TASK-OBS-08 验收通过，CYCLE-OBS-02 收口。

## 追踪矩阵

| CYCLE | TASK | AC | TEST | EVIDENCE |
| --- | --- | --- | --- | --- |
| CYCLE-OBS-02 | TASK-OBS-05 | AC-OBS-008 | TEST-OBS-014 | EVD-TASK-OBS-05-* |
| CYCLE-OBS-02 | TASK-OBS-06/07 | AC-OBS-001/002 | 路由案例 | EVD-TASK-OBS-06/07-* |
| CYCLE-OBS-02 | TASK-OBS-08 | AC-OBS-002/007/010 | TEST-OBS-004/010/013 | EVD-TASK-OBS-08-* |
