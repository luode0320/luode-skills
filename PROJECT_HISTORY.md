# 项目历史事件

> 本文件只追加关键历史事件。普通新线程默认不读取，只有历史追问、当前状态不足或真实卡点时才窄检索。

## 事件

- 2026-07-14：完成任务阻断收口与恢复计划。新增唯一 `BLK-*` 共享契约并接入审查、验收、功能验证、Bug 验证、执行失败、运行时恢复和最终总结；真实阻断在最终结尾输出状态、证据、已尝试动作、停止边界、影响、至多三步解决计划和重入点，`limited`/`not_applicable`/P2/P3 不误报。文档门禁 52 项、运行时阻断事实 3 项、七份文档 profile、Python 编译、JSON schema 解析和字典生成均通过；Obsidian 沉淀因固定 vault 未注册而阻断，未执行 Git 历史写入。

- 2026-07-13：完成 Windows PowerShell 环境可靠性升级。RequiredOnly、可选工具降级、精确包源、JSON 状态、WhatIf、profile/Terminal 事务、hash 回滚、Git Bash/WSL 分流和 UTF-8 BOM 兼容均已收口；PowerShell 5.1 与 PowerShell 7 的九项隔离回归、相关文档 profile、两个 Skill quick validator 和字典生成均通过，未执行 Git 历史写入。

- 2026-07-13：完成 Obsidian 知识流跨 Windows/WSL bridge 的 TASK-OBS-08；35/35 离线回归、PowerShell parser、Python 编译、search、长正文双端 readback（13321 chars/LF181/MD5 C46A...）与 append 双端 readback（172 chars/LF11/MD5 27ec...）通过；CYCLE-OBS-02 收口，未执行 Git 历史写入。
- 2026-07-13：完成 CYCLE-OBS-03 TASK-OBS-09~12；字典、项目记忆、周期 strict、验收 profile、当前改动审查和独立最终验收均 PASS，AC-OBS-001~010 全部放行，工作树保持未提交。

- 2026-07-12：补齐 Markdown 图片资产 validator 的文件命名、九字段资产清单一致性、共享引用和 `doc/data/` 根目录错位扫描，新增正反单测后校验器达到 `21/21 PASS`；README、编码总规和最终验收状态同步，真实 imagegen 仍因 `gpt-image-2` 503 / `gpt-image-1.5` 403 保持阻断。

- 2026-07-12：按 `CHG-DOC-IMG-001` 实施 Markdown 图片资产闭环；冻结 `doc/data/images/` 唯一根目录，更新 storage/requirement/implementation/delivery 规则、profile v3、validator 图片与孤儿检查，并将来源需求、验收、实施总览、全量顺序和周期 01 回写为增量执行入口；工作树保持未提交。

- 2026-07-11：确认采用“项目本地四件套 + Obsidian 选择性知识流”方案；项目当前状态与稳定规则分离维护，历史事件保持追加式记录。
- 2026-07-11：完成四件套规则闭环；同步 Obsidian、项目记忆、自举脚本、仓库规则和字典，验证缺失创建、幂等运行、历史追加保护、current 超限阻断及固定 vault CLI 沉淀。
- 2026-07-12：完善 `windows-wsl-execution-rules` 的跨环境命令失败恢复闭环；新增脱敏去重案例库、PowerShell/WSL/JSON/编码恢复路由和收口前自动回写规则，刷新字典并完成 UTF-8、内容存在性和差异检查。
- 2026-07-12：为权威 `imagegen` skill 增加错误案例持续迭代规则与脱敏案例库，收录 gpt-image-2 参数、透明背景、依赖/鉴权和瞬态网络错误，刷新字典并完成本地 dry-run/check、UTF-8 与敏感信息检查。
- 2026-07-12：完成 imagegen 错误案例演进的当前改动总审查，收窄瞬态重试案例到 `generate-batch` 实际覆盖范围，并通过本地伪客户端重试验证；改动保持未提交。
- 2026-07-12：按用户授权完成 imagegen 实现与审查文档提交，提交为 `26f763a` 与 `83e9576`；随后同步项目当前状态。
- 2026-07-12：按用户确认计划新增 `execution-failure-learning-rules` 元 Skill，统一 prevent/recover/learn、唯一 owner、candidate/active 授权、脱敏去重和冲突门禁；接入首批高风险 owner，完成字典刷新与 AC-001 至 AC-008 前向行为验证，改动保持未提交。
- 2026-07-12：完成执行失败持续学习与主动预防的当前改动总审查和最终验收，结论通过；Obsidian 知识笔记与 INDEX 已通过 CLI 沉淀，Git 提交仍未执行。
- 2026-07-12：按用户要求升级需求、验收和实施文档交接规则，新增 L1-L4 极致完整性标准、零决策执行契约、实施总览/周期/任务卡模板、图形化标准和文档 profile 校验器；新增需求与实施基线文档及正反验证，四类 Skill 自检和文档 profile 均通过，未执行本轮 Git 历史写入。
- 2026-07-12：通过固定 `D:\\obsidian_data` vault 的 Obsidian CLI 检索并沉淀“需求与实施文档零决策交接”知识笔记，创建 `知识库/INDEX.md` 入口，未使用文件系统读写替代 CLI。
- 2026-07-12：复核并统一三份实施文档的权威来源 ID 为 `REQ-DOC-20260712-033322`，将已落盘入口的状态从历史占位语义修正为真实状态，五类文档 profile、单元测试、Skill 校验、字典生成和差异检查再次通过。
- 2026-07-12：完成需求与实施文档极致完备化周期 01-04 收口并启动周期 05；补齐周期 04 当前 profile 所需章节，创建周期 05 全局同步/最终验收实施文档与测试入口，后续以全量回归、审查和验收证据作为最终放行依据，改动保持未提交。
- 2026-07-12：完成周期 05 全局同步与最终验收；更新旧的当前改动总审查和最终验收文档，补齐 C02-C05 证据互链及最终验收一致性断言；九份文档 profile、校验器单测 7/7、周期 02/03/04/05 测试、四个 Skill quick validator、Mermaid 真解析、字典和固定 Obsidian CLI 均通过，工作树保持未提交。
- 2026-07-12：完成最终注释双 skill 闸门与实现审查收口；为校验器、测试函数和 C05 集成测试补齐中文函数头、步骤编号及补丁原因注释，修正最终验收的周期 05 测试口径为 6/6，重跑单测、集成测试、编译、quick validator 和差异检查均通过，未执行 Git 历史写入。
- 2026-07-12：修复严格文档校验器的 JSON 集合序列化、正文回指污染周期归属和“禁用”规范词误报；补齐周期 01 任务级验收证据与 `--root .` 严格命令，需求/验收 strict 报告均为 `status: PASS`，校验器单测更新为 9/9，工作树保持未提交。
- 2026-07-12：执行 Markdown 图片资产闭环的真实 imagegen 验证；`gpt-image-2` 返回 HTTP 503 `model_not_found`，回退 `gpt-image-1.5` 返回 HTTP 403 权限错误。未生成伪图，临时资产已清理；机器校验、回归测试和审查保持通过，C05/最终验收状态改为 `blocked`，工作树未提交。
- 2026-07-12：记录 Windows Python 默认编码导致 quick validator 解码失败的可复用恢复方案；使用 `python -X utf8` 对同一输入复验通过，并按 `WSL-006` 以 `candidate` 写入跨环境命令失败案例库。
- 2026-07-12：按用户授权完成 Windows PowerShell 环境准备：安装并验证 PowerShell 7.6.3，设置 Windows Terminal 用户级默认 profile，初始化 PowerShell 5.1/7 UTF-8 profile，安装并验证 manifest 工具；7z/tlrc 因管理员权限阻断，未绕过 UAC。
- 2026-07-12：完成 Windows PowerShell Skill 的 Audit、JSONC Apply、重复 Apply 幂等、Rollback、quick validator、字典刷新和 WSL 原生工具路径复核；WSL PATH 无 `/mnt` 且无 Windows `.exe` 误走，改动保持未提交。
- 2026-07-12：按用户要求升级 Windows PowerShell Skill 的自动迭代闭环；新增 SessionEnsure 会话 TTL/原子锁、RecoverCommand/wrapper 命令缺失恢复、精确 package 映射、verified discovered-tools、脱敏 failure casebook、Windows/WSL owner 分流和真实失败恢复测试。PS5/PS7 解析、两个 Skill quick validator、原有环境测试、新增恢复测试、字典、UTF-8 与 diff 检查通过；7z/tlrc 权限阻断保留，未执行 Git 历史写入。
- 2026-07-12：针对通用上线测试引擎并行补丁后的 `23 passed, 2 errors, 1 failure` 真实状态，新增受限修订版全量实施计划，冻结 R1 回归恢复、C02-C08 垂直切片、local-only、真实测试、停止/回滚和 C08 证据门禁；本轮未获得代码实施授权，未执行 Git 历史写入。
- 2026-07-12：按修订版上线测试引擎计划完成 R1 与 C02-C08 窄闭环实现；修复 gRPC discovery、RPC local provenance、CLI 兼容、参数位置/provider、doctor 矩阵、协议判定、报告/基线产物和 v1 migration CLI。旧轮 27/27、本轮新增 11/11 测试通过；C08-03 因非 HTTP local runtime 与最终验收输入缺失保持 BLOCKED，未执行 Git 历史写入。
- 2026-07-12：将通用上线测试引擎修订计划升级为极致完整执行契约；校正当前证据目录为 `2026-07-12_191712`，新增 C09 双索引、C10 真实 local runtime、C11 P0/P1 全量门禁、C12 跨项目复用与证据互链任务，strict implementation validator PASS；本轮只更新计划，未授权继续编码或 Git 历史写入。

- 2026-07-12：完成研发文档白话化与附录分层规则。新增共享契约并接入需求、实施、Bug、测试、审查、验收、架构、交付和报告类 Skill；校验器新增正文/附录门禁与八类文档 profile，`26/26` 单测通过。不适用的第三方审查或验收需记录原因和依据但不再默认阻断；本轮未执行 Git 历史写入。
- 2026-07-13：完成文档白话化与审查验收条件化门禁升级收口；六类代表性 profile 全部 `PASS`，校验器单测 `30/30 PASS`，Python 编译、技能字典生成和 `git diff --check` 均通过。保留现有标题结构，不新增独立 Skill；不适用验证不阻断，受限验证可继续但不正式放行，明确必需且无替代验证才阻断；本轮未执行 Git 历史写入。
- 2026-07-13：按审计结果修复白话契约绕过、HEAD 标题编号比较、通用 profile 空壳和 `limited` 顶层状态误报；补齐新旧文档兼容、审查提交边界、最终验收 N/A 依据和项目记忆索引。校验器单测 `37/37 PASS`，六类代表性 profile、编译、字典和差异检查通过；本轮未执行 Git 历史写入。
- 2026-07-15：按用户要求补充 `code-generation-style-rules` 的局部一致性与接口实现对照规则；统一局部上下文只做必要模板替换，接口实现优先参考既有实现，风格契约记录局部证据、参考实现、最小新增内容和禁用写法；同步需求/验收/实施文档与项目记忆，当前改动未提交。
- 2026-07-15：完成局部一致性与接口实现规则收口；TEST-06 至 TEST-11、五个工程文档 profile、字典、UTF-8、差异、实现自审、当前改动总审查、skill 合规和最终验收均通过；通过 Obsidian bridge 新增规则知识笔记并更新 INDEX，未执行 Git 历史写入。
