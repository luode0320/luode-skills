# Obsidian 知识流跨 Windows 与 WSL 桥接验证

## 任务信息

- 来源对象：`REQDOC-OBS-20260713`
- 当前周期：`CYCLE-OBS-02`
- 当前任务：`TASK-OBS-08`
- 环境：仅 local Windows / WSL；不连接 test、staging 或 production。

## 目录分工

- 本中文目录仅保存本任务验证说明。
- `../skills/obsidian-knowledge-flow/` 是 ASCII 测试资产镜像目录，保存 Python 测试与 fixture。

## 当前验证口径

`test_obsidian_cli_bridge.py` 与 `test_obsidian_cli_contract.py` 覆盖 path traversal、Windows/WSL/UNC 项目身份、UTF-8 JSON、结构化错误码、应用恢复、唯一 vault、10KB 中文分块、长 stdout、readback、`limit=1..100` 直调校验，以及预检/写命令语义错误与 `Error:` 正文的边界。`test_distill_vault.py` 通过 mock bridge 覆盖批处理的 3 批次 4 篇、目标路径、rollup、INDEX、脱敏与旧 nested root；离线测试不调用真实 Obsidian CLI。

## 执行结果（2026-07-13 17:17:55）

- 自动化：bridge 单元测试 `16/16 PASS`；adapter 契约测试 `17/17 PASS`，合计 `33/33 PASS`；Python 编译与 PowerShell parser PASS。
- Windows 实机：`doctor` 返回 `ok=true`、selector=`obsidian_data`、`verified=true`；受控 smoke 的 create/read/append/read 均返回 `verified=true`。
- WSL 实机：通过 `wsl-powershell-interop` 的 `doctor`、read、append 均返回 `ok=true`、`verified=true`；WSL 仍输出 `/etc/fstab` 挂载警告，但不影响 JSON 成功结果。
- 清理：smoke note 已覆盖回固定 `status: test-fixture` 的中性内容；临时 JSON 由 bridge scope 自动删除。
- 检索复验：修复 PowerShell 参数数组拆分后，Windows `search`、Windows `search-context` 与 WSL `search` 均返回 `ok=true`、`verified=true`。
- 契约复验：fake CLI 会断言 `query=`、`limit=` 必须分别为完整 argv；adapter 对直调 `limit` 强制整数 `1..100`。`Error:` 仅在 version、无结构 vault listing 与 create/append 的无正文输出中映射 `CLI_FAILED`，read/search 的合法 Markdown 正文保持原样。
- 自动启动实机：用户关闭 Obsidian 后，Windows `doctor` 返回 `started_app=true`、`attempts=3`、`ok=true`、`verified=true`，满足 `TEST-OBS-006` 与 `AC-OBS-003`。
- 结论：`TASK-OBS-04` 与 `CYCLE-OBS-01` 已收口；允许进入 `CYCLE-OBS-02`，但仍须逐个完成 TASK-OBS-05 至 TASK-OBS-08。

## TASK-OBS-05 执行结果（2026-07-13 17:32:38）

- 自动化：`test_distill_vault.py` 为 `2/2 PASS`；本目录完整 `unittest discover` 为 `35/35 PASS`。测试仅使用临时 source fixture 和 mock bridge，不读取或写入用户 vault。
- 实机只读：Windows bridge `doctor --json` 返回 `ok=true`、`vault_selector=obsidian_data`、`verified=true`；受控 source fixture 的 `distill_vault.py --dry-run` 返回 `total_files=2`、`total_read=2`、`total_errors=0`。
- 负向：`--target-root D:\obsidian_data\知识库 --dry-run` 返回 `LEGACY_NESTED_VAULT_MODEL`，无 create/append。
- 资产：新增 ASCII 测试资产 `../skills/obsidian-knowledge-flow/test_distill_vault.py`；生产脚本不含独立 target CLI transport。

## TASK-OBS-06 执行结果（2026-07-13 17:47:22）

- 规则路由：Windows、WSL、历史检索、普通任务和 bridge doctor failure 的语义断言均 PASS。WSL 缺少原生 `obsidian` 不再单独阻断，且 prompt 禁止 Agent 自行选择 shell、CLI 路径和 vault selector。
- 身份：schema 已覆盖 canonical `project_id`、`project_root_native`、`project_root_windows`、`project_root_wsl` 与 `path_aliases`；同一 WSL 项目的 Linux/UNC/Git Bash 仅保留一个实体。
- Skill：未命中硬编码知识库 selector、PATH CLI 阻断或直接 transport 拼接；description 更新后已运行 `python skill-dictionary/generate_dictionary.py` 成功。

## TASK-OBS-07 执行结果（2026-07-13 18:12:37）

- 测试对象：`obsidian-knowledge-flow/references/cli-operations.md`、`vault-layout.md`、`capture-retrieve-distill.md`、`validation-checklist.md`、`cli-failure-casebook.md`。
- 执行环境：local Windows 工作区；本任务只读取和校验仓库文档，不直接读取或写入 `D:\obsidian_data` vault。
- 验证入口：五份 reference 的 bridge-only 禁止词扫描、`TEST-OBS-*` 映射扫描，以及本目录完整 `unittest discover` 回归；真实测试代码和 fixture 位于 `../skills/obsidian-knowledge-flow/`。
- 文档断言：五份 reference 均明确固定 root、动态 selector、Windows/WSL transport、`verified=true` readback、自动启动一次/15 秒/最多一次重试和不使用文件系统 fallback；每类能力均映射到 `TEST-OBS-001/003/004/006/007/008/010/011/012/013/014/015/016`。
- 禁止词扫描：未发现硬编码知识库 selector、直接版本/注册列表子命令、绕过 bridge 的 vault 文件系统写入或无限重试指引；结果为 PASS。
- 审查证据：[`2026-07-13_181500_REQDOC-OBS-20260713_TASK-OBS-07_参考规则与失败案例当前改动总审查.md`](../../../6-审查/2026-07-13_181500_REQDOC-OBS-20260713_TASK-OBS-07_参考规则与失败案例当前改动总审查.md)。
- 结论：TASK-OBS-07 文档实现、测试、审查和验收闭环完成；允许进入 TASK-OBS-08。10KB 中文正文的真实 WSL create/readback 仍按 TASK-OBS-08 单独记录，不在本任务提前宣称完成。

## TASK-OBS-08 执行结果（2026-07-13 18:28:00）

- 自动化回归：bridge、adapter contract 与 distill 测试目录合计 `35/35 PASS`；PowerShell parser PASS；Python `py_compile` PASS。长正文契约覆盖 fake CLI 的 append 前置换行语义，避免分块边界误报 `READBACK_MISMATCH`。
- retrieve：Windows `search --query task08-long-note --limit 10` 与 WSL 同命令均返回 `ok=true`、`verified=true`；WSL transport=`wsl-powershell-interop`，Windows transport=`windows-direct`。
- capture：WSL bridge create 长正文 `知识库/90-Archive/_system-tests/task08-long-note-20260713.md` 返回 `ok=true`、`verified=true`；Windows/WSL readback 完全一致，字符数 `13321`、LF `181`、UTF-8 MD5 `C46A83642C092EF2185BD74572302FB0`。
- distill/append：WSL create + append `知识库/90-Archive/_system-tests/task08-append-20260713.md` 后，Windows 与 WSL readback 均 `ok=true`、`verified=true`；字符数 `172`、LF `11`、`contains_append=true`、两侧 UTF-8 MD5 `27ec6c195d225b9d6f602d42394a0baa`。
- identity：`project-context` 的 Linux、UNC 与 Git Bash 路径归一断言已由 bridge 单测覆盖；同一项目仅保留一个 canonical `wsl://` ID。
- failure matrix：离线契约覆盖 interop、应用启动恢复、零/多 vault、path traversal、timeout、legacy nested root；所有失败均返回稳定错误码，未执行 vault 文件系统 fallback。
- 审查：TASK-OBS-07 参考规则审查 PASS；TASK-OBS-08 实机证据由 bridge JSON readback 产生，临时 response 文件由 bridge 作用域清理，测试笔记保留在 `_system-tests` 以避免越过 bridge 删除限制。
- 审查文档：[`2026-07-13_184500_REQDOC-OBS-20260713_TASK-OBS-08_端到端验证当前改动总审查.md`](../../../6-审查/2026-07-13_184500_REQDOC-OBS-20260713_TASK-OBS-08_端到端验证当前改动总审查.md) 结论 PASS。
- 结论：TASK-OBS-08 实现、真实测试、审查和验收闭环完成；CYCLE-OBS-02 满足收口条件，允许进入 CYCLE-OBS-03。

## 清理

测试创建的临时请求、响应和目录必须在测试结束时删除；任何残留视为 `TASK-OBS-02` 未验收。
