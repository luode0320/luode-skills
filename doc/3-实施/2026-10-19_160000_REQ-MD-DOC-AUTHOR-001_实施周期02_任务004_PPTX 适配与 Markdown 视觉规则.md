---
template_version: "v4"
doc_id: "IMP-TASK-REQ-MD-DOC-AUTHOR-001-TASK-004"
doc_type: implementation_task
complexity: focused
baseline_commit: "3a9aa97eeafaf202dea63665578eba6f3b9e3254"
status: completed
version: "v1.0"
task_id: "TASK-004"
cycle_id: "CYCLE-02"
source_ids: ["REQ-MD-DOC-AUTHOR-001", "RULE-MD-PPTX-001、RULE-MD-MERMAID-001", "AC-MD-002、AC-MD-003、AC-MD-004、AC-MD-005"]
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
style_regression: required_after_tests
updated_at: "2026-10-19 16:00:00"
---

# 任务004：PPTX 适配与 Markdown 视觉规则

结论：本任务完成创建 PPTX 适配矩阵、Markdown 视觉清单和路由契约；影响：本任务只触达计划中列出的规则资产、文档或 skill 文件；范围：markdown-document-authoring-rules/SKILL.md；references/pptx-absorbed-principles.md；references/markdown-visual-checklist.md；references/route-contract.md；非范围：历史 Markdown、PPTX 业务职责、业务代码、数据库、API、外部项目和 Git 历史；变化：公共 skill 具备可执行的呈现与路由规则；完成标准：references、路由契约和吸收登记通过审计；术语说明：垂直切片指一次只完成一个可独立验证的任务结果；验证状态：任务已完成；真实命令、断言和证据已记录。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 任务 ID | TASK-004 |
| 所属周期 | CYCLE-02 |
| 周期内顺序 | 4 |
| 来源需求 | REQ-MD-DOC-AUTHOR-001 |
| 规则 | RULE-MD-PPTX-001、RULE-MD-MERMAID-001 |
| 验收条件 | AC-MD-002、AC-MD-003、AC-MD-004、AC-MD-005 |
| 主项目 | D:/谷歌云盘/luode-skills |
| 代码基线 | main / 3a9aa97eeafaf202dea63665578eba6f3b9e3254 |
| 当前状态 | completed |
| 外部项目代码引用 | N/A + 本任务只修改当前仓库 + 基线已冻结 |
| 图片资产决策 | N/A + 本任务只处理规则、文档或 skill 文本 + Mermaid 和表格表达结构 |

## 任务目标与唯一垂直切片

- 唯一目标：创建 PPTX 适配矩阵、Markdown 视觉清单和路由契约
- 输入条件：前置任务和周期 profile 已通过；允许文件已核对；工作树既有修改已记录。
- 输出结果：公共 skill 具备可执行的呈现与路由规则。
- 不拆入本任务：其他周期、其他领域 skill、历史 Markdown 和业务运行时。
- 最大推进边界：完成本任务的文件、测试、6-review 和证据后停止，不自动执行下一任务。

## 跨会话执行入口

- 主项目：D:/谷歌云盘/luode-skills。
- 首条检查：读取 AGENTS.md、PROJECT_CURRENT.md、PROJECT_MEMORY.md，并确认分支 main 与基线 3a9aa97eeafaf202dea63665578eba6f3b9e3254。
- 当前任务恢复：确认 TASK-004 的允许文件、前置验收和当前状态。
- local 依赖：Python 3、Node.js、仓库内 validator、skill-creator quick_validate；TASK-008 另外要求本机 mmdc。
- 外部项目：N/A + 没有跨项目代码引用 + 不访问兄弟项目。
- 中断重入：从允许文件核对开始，不跳过真实测试和 6-review。

## 文件与符号操作契约

| 文件 / 符号 | 操作 | 修改前职责 | 修改后职责 | 允许范围 |
| --- | --- | --- | --- | --- |
| markdown-document-authoring-rules/SKILL.md；references/pptx-absorbed-principles.md；references/markdown-visual-checklist.md；references/route-contract.md | 修改 SKILL.md 并新增三份 reference | skill 只有入口职责 | 公共 skill 具备可执行的呈现与路由规则 | 仅限 TASK-004 |
| 计划追踪 | 更新本任务的 TEST、STYLE、EVIDENCE | planned | 记录真实结果 | 不改变其他任务状态 |
| skill-absorption-rules/references/workbuddy-absorption-map.md；skill-absorption-rules/references/source-notes.md | 追加 PPTX→Markdown 裁决与来源证据 | 吸收记录尚未落盘 | 记录来源、拒绝项、同域去重、环境依赖和验证 | 仅限 TASK-004 收口证据 |

## 禁止触碰区

- 不修改 visualization-standard、artifact-storage-rules、artifact-delivery-gate-rules。
- 不修改本任务允许文件之外的文件。
- 不改变既有需求、Bug、计划、架构、测试和交付语义。
- 不删除既有脏工作树文件。
- 不执行 commit、push、rebase、merge。
- 不把静态检查结果写成真实行为证据。

## 实施步骤

1. 写 PPTX 迁移矩阵
2. 写视觉清单
3. 写 Owner 路由契约
4. 在 SKILL.md 接入 references

每一步完成后立即检查目标文件内容和 UTF-8 字节数；发现文件路径、符号或基线不一致时停止。

## 图片资产执行契约

| 字段 | 决定 |
| --- | --- |
| 图片资产决策 | N/A + 纯规则、文档或 skill 文本，不需要 UI、截图或真实产物图片 |
| Mermaid 边界 | 流程、时序、状态、依赖和风险关系继续使用 Mermaid，图片不能替代这些结构图 |
| imagegen | N/A + 本任务没有位图资产 |
| 目标资产路径 | N/A + 不创建 doc/data/images 文件 |
| 资产清单 | N/A + 不生成 IMG-* |

## 真实测试与断言

| 测试 ID | 精确入口 | 依赖环境 | 样本 / 数据 | 通过标准 | 失败预期 | 清理 |
| --- | --- | --- | --- | --- | --- | --- |
| TEST-MD-004 | quick_validate.py + rg 路由检查 | Python 3、Node.js；TASK-008 需要 mmdc | 公共 skill 与 references | 所有 reference 存在、链接有效、迁移边界清楚、无第二 Owner | 发现 Owner 重复或 PPTX 物理规则混入时停止 | 删除临时日志、搜索输出或 Mermaid 产物，不删除正式文件 |

真实测试不能由 build、lint 或人工阅读替代。纯文档和 skill 任务不需要产品运行时测试，理由是 N/A + 不改变业务运行时；仍必须执行本任务定义的文档、skill 或解析验证。

## 测试后 6-review 风格回归

- 入口：本任务卡和最终 doc/6-review/2026-10-19_160000_REQ-MD-DOC-AUTHOR-001_6-review.md。
- 前置：TEST-MD-004 真实测试通过。
- 检查范围：文件位置、UTF-8、标题层级、中文可读性、注释、日志字段、引用路径、公共规则复用和目录归位。
- 不检查：业务正确性、需求是否完整、发布放行和运行时功能。
- 结果：执行后只能写 STYLE: PASS 或 STYLE: FIX_REQUIRED。
- 当前结果：TEST-MD-004 已通过；测试后 6-review 结果：STYLE: PASS。

## 已执行证据

- 测试 ID：TEST-MD-004。
- 精确命令：python -X utf8 .system/skill-creator/scripts/quick_validate.py markdown-document-authoring-rules；rg -n pptx-absorbed-principles|markdown-visual-checklist|route-contract|visualization-standard|artifact-storage-rules|artifact-delivery-gate-rules markdown-document-authoring-rules/SKILL.md。
- 结果：quick validation 退出码 0；references 路由搜索退出码 0；三份 reference 存在且公共 Owner 边界明确。
- 证据编号：EVID-MD-004。
- 吸收登记：已追加 skill-absorption-rules/references/workbuddy-absorption-map.md 与 skill-absorption-rules/references/source-notes.md，记录内部来源、拒绝项、同域去重和验证结果。
- 清理：已删除临时日志、搜索输出和临时产物；正式文件保留。
- 范围核对：未写入本任务允许文件之外的文件。

## 回滚、清理与停止条件

### 回滚

- ROLLBACK-TASK-004-001：只恢复或删除本任务允许文件。
- ROLLBACK-TASK-004-002：保留其他任务和既有工作树改动。
- ROLLBACK-TASK-004-003：字典或生成文件只恢复本轮生成差异，不执行全仓库清理。

### 清理

- 删除本任务临时日志、临时搜索输出和临时 Mermaid 产物。
- 保留正式计划文档、skill 文件、references 和生成字典。

### 停止条件

- 发现 Owner 重复或 PPTX 物理规则混入时停止；
- profile、quick validation、解析器或断言失败；
- 发现范围外文件差异；
- 发现基线漂移；
- 需要猜测路径、符号、依赖、权限、异常或回滚；
- 需要访问外部项目、生产服务或凭据。

## 任务完成条件

1. references 和路由契约通过审计；
2. TEST-MD-004 真实测试通过；
3. 测试后 6-review 写入 STYLE: PASS；
4. EVIDENCE-TASK-004 记录路径、命令、退出码、断言和清理结果；
5. 本任务范围外没有文件变化；
6. 当前任务状态从 planned 变为 completed，才允许进入下一个任务。

## 任务阻断收口

- 阻断记录 ID：N/A + 当前任务尚未执行，暂无阻断记录。
- 任务状态：completed。
- 阻断阶段：N/A。
- 阻断依据与证据：N/A + 任务尚未启动。
- 已尝试与停止边界：N/A + 执行前不进行无变化重试。
- 影响：N/A。
- 解决计划：执行时按停止条件记录。
- 恢复后重入点：从本任务文件核对和前置 profile 开始。
- 去重键：TASK-004-CYCLE-02-3a9aa97eeafaf202dea63665578eba6f3b9e3254。
- 用户授权操作：用户已授权先持久化计划后开始实现；未授权 Git 历史写入。

## 执行附录

任务执行时记录精确命令、实际路径、样本、断言、退出码、临时产物清理和回滚判断。执行附录位于本文末尾，不能用摘要替代命令和证据。

## 追踪附录

| REQ / RULE | AC | CYCLE | TASK | TEST | STYLE | EVIDENCE |
| --- | --- | --- | --- | --- | --- | --- |
| REQ-MD-DOC-AUTHOR-001 | AC-MD-002、AC-MD-003、AC-MD-004、AC-MD-005 | CYCLE-02 | TASK-004 | TEST-MD-004 | STYLE-TASK-004 | EVID-MD-004 |

NaN 的追踪链必须回指需求文档、实施总览和所属周期文档。
