# 项目当前状态

## 目标与范围

- 目标：把需求、验收标准、实施总览、实施周期和最小任务 Skill 升级为“极致详细、结构完整、普通模型零决策执行、图形化且可机器校验”的 Markdown 文档交接体系。
- 范围：`requirement-intake-rules`、`acceptance-criteria-rules`、`implementation-planning-rules`、`artifact-delivery-gate-rules`，以及对应模板、质量 profile、验证脚本、测试和项目规则入口。
- 非范围：不修改业务代码，不连接 test/prod，不执行 Git 历史写入，不创建职责重叠的顶层 Skill。

## 当前状态

- 状态：原文档完备性基线和图片规则/校验实现已完成；`CHG-DOC-IMG-001` 在 CYCLE-05/T05-03 已按最新配置完成真实生图和验收。
- 当前入口：`T05-03` 已完成：真实 PNG、签名、`view_image`、validator 和最终验收均通过，工作树保持未提交。
- 本轮增量：Windows PowerShell 环境 Skill 已完成真实安装与验证；PowerShell 7.6.3 已成为 Windows Terminal 默认专项入口，工具安装与 WSL 隔离复核完成。
- 更新时间：2026-07-12。

## 已完成

- 建立 L1-L4 极致完整性标准、零决策交接、稳定 ID、字段矩阵、图形适用性和双向追踪规则。
- 建立实施总览、实施周期、最小任务执行卡、输出门禁和全量顺序实施方案。
- 扩展文档质量 profile 与 `validate_engineering_docs.py`，覆盖 UTF-8、front matter、章节、ID、表格、N/A 证据、链接、Mermaid 和严格追踪。
- 校验器单测 `21/21 PASS`；需求/验收 strict 报告均为 `status: PASS`；周期 02 行为测试通过；周期 03 `6 tests OK`；周期 04 `3 tests OK`；周期 05 `6 tests OK`。
- C04 Mermaid 真解析覆盖 6 份文档并生成 12 个非空 SVG；C05 生成至少 2 个非空 SVG。
- 四个受影响 Skill 的 quick validator 均从各自 Skill 目录执行并返回 `Skill is valid!`。
- 字典生成结果为 `implemented_total=83`、`planned_missing=0`、`seed_total=25`。
- 已更新旧的当前改动总审查和最终验收，删除过时的静态 Mermaid 阻断结论，并加入最终验收输入一致性断言。
- 完成校验器、校验器单测和 C05 集成测试的注释双 skill 闸门；函数头、步骤编号和补丁原因注释均已核对，并修正最终验收文档中周期 05 的测试口径为 `6/6`。
- 已通过固定 `D:\obsidian_data\知识库` 的 Obsidian CLI 检索、读回和知识沉淀；未使用文件系统替代 vault 操作。
- 已新增并验证 `windows-powershell-environment-rules`：PowerShell 7.6.3、Windows Terminal 默认 profile、PowerShell 5.1/7 UTF-8 profile、Windows 工具 manifest、Audit/Apply/幂等/Rollback 脚本和权限安全边界均已落盘。
- Windows 侧已验证 `rg`、`fd`、`fzf`、`jq`、`yq`、`bat`、`eza`、`delta`、`just`、`sd`、`zoxide`、`wget2`、`aria2c`、`gsudo` 与 Git；`7z.exe`、`tlrc.exe` 因当前用户非管理员且安装器要求提升权限，保留为明确权限阻断。
- WSL 原生工具路径复核通过：PATH 不含 `/mnt`，上述工具在 WSL 中均为 `MISSING`，未发现 Windows `.exe` 误走路径；Windows 工具不替代 WSL 原生工具。
- Windows PowerShell Skill quick validator 输出 `Skill is valid!`；字典生成输出 `implemented_total=83`、`planned_missing=0`、`seed_total=26`。
- 本轮已升级 Windows PowerShell Skill：新增 `SessionEnsure` 会话 TTL/原子锁检查、`RecoverCommand` 命令缺失恢复 wrapper、精确 package 映射、用户级 `discovered-tools.json`、脱敏 `failure-cases.json` 和 Windows owner casebook；canonical manifest 不运行时自改，未知命令无 exact package ID 时只记录 candidate。
- 新增 `doc/5-tests/2026-07-12_135347/windows-powershell-environment-rules/scripts/run_failure_recovery.ps1`；原有环境测试与新增失败恢复测试均真实通过。SessionEnsure 对 7z/tlrc 权限阻断写 `complete=false`，不伪造成功 marker，后续会话可持续重试。
- execution-failure-learning 路由已增加 Windows PowerShell owner 与 WSL/Windows `127` 分流；Skill quick validator、PS5/PS7 parse、UTF-8 和 `git diff --check` 已通过。
- 当前改动总审查已落盘到 `doc/6-审查/2026-07-12_151900_WindowsPowerShell环境自动迭代_当前改动总审查.md`，结论通过；PowerShell 脚本已补 UTF-8 BOM，确保 Windows PowerShell 5.1 的 `-File` 入口可正确解析中文注释。
- 已将图片根目录冻结为 `doc/data/images/`，更新 storage、requirement、implementation 和 delivery gate 规则；validator 已支持图片决策、相对路径、签名、`IMG-*`、HTML/远程/Base64 禁止和 `--check-orphan-images`。

## 待办

- 已完成：local imagegen 使用 `gpt-image-2` 生成真实 PNG，完成 `view_image`、图片引用/清单验证和孤儿扫描；临时资产已清理。

## 阻断

- 机器校验、回归测试和审查无 P0/P1 问题。
- 真实 imagegen 已通过：2026-07-12 使用当前授权配置 `https://xm.aceapi.cc/v1` 和 `gpt-image-2` 生成 `markdown-image-workflow.diagram-v1.png`（867168 bytes，PNG 签名，1254x1254）；`view_image`、`check_images` 和 `check_orphan_images` 均通过。密钥未写入仓库或证据。
- 严格校验 CLI 已修复 JSON 序列化问题和正文回指污染周期归属问题；当前以 `--root .` 扫描受控来源文档集，需求/验收报告均 PASS。

## 验证

- 九份当前需求/验收/总表/总览/周期文档 profile 均 `valid: true`。
- `python -X utf8 doc/5-tests/2026-07-12_061500/artifact_delivery_gate_rules/test_cycle05_global_sync.py`：`6 tests OK`。
- `python -X utf8 -m unittest artifact-delivery-gate-rules/tests/test_validate_engineering_docs.py -v`：`21/21 PASS`。
- 需求与验收 strict 校验：均 `status: PASS`、14 个任务唯一周期归属、四类证据齐全、`unresolved_decisions=0`。
- 受影响 Python 校验/测试文件 `py_compile` 通过；受影响四个 Skill quick validator 均输出 `Skill is valid!`；Skill 合规闸门结论为 `PASS`。
- `python -X utf8 skill-dictionary/generate_dictionary.py`：生成成功。
- `git diff --check`：退出码 0；工作树保持未提交。
- 已验证 path-map v6、quality profile v3、图片规则 quick validator 和 validator 图片/孤儿单测新增用例；完整回归已在主线程收口。
- 执行失败学习：Windows Python 默认编码导致 quick validator 解码失败的恢复方案已按 `WSL-006` 以 `candidate` 写入 `windows-wsl-execution-rules/references/command-failure-recovery.md`。

## 交接点

- 规则资产、机器校验、回归测试、真实生图、图片引用和审查证据已通过；C05 及最终图片验收状态为 `PASS`，工作树保持未提交。
- 未经用户在当前轮明确授权，不执行 `git commit`、`git push`、`git rebase`、`git merge` 或其他历史写入动作。
- Windows PowerShell 环境 Skill 已完成本轮闭环；仅 `7z.exe`、`tlrc.exe` 的管理员权限补装仍未完成，不阻断已验证的核心环境入口。
