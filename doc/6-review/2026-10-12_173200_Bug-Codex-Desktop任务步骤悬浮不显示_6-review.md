---
schema_version: 1
template_version: 1
doc_id: "STYLE-CODEX-PLAN-UI-20261012"
doc_type: "style_regression"
source_ids: ["SRC-CODEX-PLAN-UI-20261012"]
status: "accepted"
version: "v1.0"
current_slice: "TASK-PLAN-REHYDRATION-ABSORB-20261012"
updated_at: "2026-10-12 17:32:00"
reader_level: business_general
writing_style: plain_chinese
appendix_policy: preserve_existing_or_one_terminal_appendix
---

# 6-review：Codex Desktop 重启后任务步骤清单恢复规则吸收

结论：本轮把 Codex Desktop 重启后恢复同一会话原生任务步骤清单的处理规则吸收到用户级 `task-plan-rehydration-rules` Skill；影响：后续会话会先核验当前回合的 `update_plan` 工具与会话投影，工具同步失败只影响显示验收，不暂停领域任务；范围：本轮任务对应的 Skill、来源记录、吸收登记、复盘案例和项目当前状态记录；非范围：不修改 Codex Desktop 程序，不声称已取得原生悬浮窗截图，也不把同步工具回执等同屏幕可见证明；变化：增加重启后恢复检查和显示证据边界，并将重复的 UI 失败处置合并到唯一规则；完成标准：Skill 校验通过、引用可达、6 维残留逐项有证据、`style_regression` 文档机器校验通过；术语说明：`update_plan` 是同步 Codex 原生任务步骤清单的工具，投影是按当前会话保存的步骤状态；验证状态：Skill 结构检查通过，当前会话 `update_plan` 调用成功，但本轮没有独立屏幕截图，因此不报告原生悬浮窗的视觉验收通过。

## 文档信息

| 字段 | 内容 |
| --- | --- |
| 关联任务 | `TASK-PLAN-REHYDRATION-ABSORB-20261012` |
| 来源对象 | 用户反馈 Codex Desktop 任务步骤悬浮清单在重启后缺失 |
| 来源记录 | `../../task-plan-rehydration-rules/references/source-notes.md` |
| Skill 主入口 | `../../task-plan-rehydration-rules/SKILL.md` |
| 检查时点 | Skill 结构校验与重启后当前会话同步调用完成后 |
| 原生 UI 可见性 | 未获得独立截图证据；不宣称视觉验收通过 |

## 检查范围

- 检查 Skill 文档的编码、格式、命名、引用、规则落点、重复内容收敛和可读性。
- 核对吸收登记、来源记录、案例复盘与 `PROJECT_CURRENT.md` 对本轮裁决和证据边界的表述。
- 本记录不判断 Codex Desktop 内部实现正确性，不替代原生悬浮清单截图验收。
- 图片资产决策：N/A + 原因 + 证据：本记录不需要视觉材料；没有提供可写入项目文档的当前桌面截图。

## 真实测试前置证据

- 真实会话验证：Codex 重启后，当前会话的 `update_plan` 工具已重新注册；当前 session projection 校验通过；向原生计划工具同步当前会话清单的调用成功。该证据证明同步通道可调用，不证明用户界面实际呈现结果。
- `TEST-SKILL-VALIDATE-20261012`：`python -X utf8 -B .system/skill-creator/scripts/quick_validate.py task-plan-rehydration-rules` 返回 `Skill is valid!`。
- `EVIDENCE-PLAN-UI-01`：当前会话投影校验结果为同一 session、状态 `inactive`、三步均 `completed`；完成收口后再次调用 `update_plan` 成功。
- `EVIDENCE-PLAN-UI-02`：当前工具集确实包含 `update_plan`，用户级配置 `[tools.update_plan].enabled=true`；工具调用结果成功。没有独立屏幕截图，故可见性维持未证实。
- `EVIDENCE-PLAN-UI-03`：`git diff --check` 未发现空白错误；输出仅提示既有 `.system/skill-creator/scripts/quick_validate.py` 工作副本行尾转换警告，该文件不属于本轮规则吸收的变更范围。
- 本轮没有改动可执行产品代码，也没有运行行为回归测试。Skill 结构校验与当前会话工具调用分别覆盖规则资产结构和同步入口，不替代真实 UI 截图。

## 6-review 结论

- STYLE: PASS
- 结论范围仅限 Skill 文档写法、引用、落点与格式；当前原生步骤悬浮是否实际可见仍未通过独立视觉证据验收。

## 检查清单

| 步骤 | 覆盖维度 | 规则 Owner | 结果 | 证据 |
| --- | --- | --- | --- | --- |
| STYLE-01 静态格式与编码一致性 | 编写习惯、格式与编码 | `code-style-consistency-rules` | PASS | 下方 6 维记录与 UTF-8 校验说明 |
| STYLE-02 命名与符号引用一致 | 命名、术语与引用 | `naming-rules` | PASS | `SKILL.md` 中链接均指向本轮来源记录、吸收表与案例 |
| STYLE-03 注释分层与定义位置 | 注释分层 | `comment-rules` | N/A + 原因 + 证据：本轮只有 Skill 文档内容，没有代码注释或函数定义；变更文件列表见下方真实变更集 |
| STYLE-04 函数签名与参数结构 | 函数签名 | `code-quality-rules` | N/A + 原因 + 证据：本轮没有新增或修改函数签名；变更文件列表见下方真实变更集 |
| STYLE-09 测试资产与编码前契约 | 测试资产归位与风格契约 | `code-generation-style-rules` | N/A + 原因 + 证据：没有新增测试资产，也没有源代码生成或重构；本轮验证对象是 Skill 规则文档 |

## 交付残留自查（6 维）

本轮真实变更集从 `git status --porcelain=v1 --untracked-files=all` 核对。该仓库在本任务前已有多处未提交改动；本记录只把任务范围内可回指的文件列为本轮交付：`PROJECT_CURRENT.md`、`task-plan-rehydration-rules/SKILL.md`、`task-plan-rehydration-rules/references/source-notes.md`、`task-plan-rehydration-rules/workbuddy-absorption-map.md`、`task-plan-rehydration-rules/references/case-task-plan-rehydration-rules-absorption.md`、本 `6-review` 记录和 `doc/6-review/README.md`；知识库另更新 `20-Knowledge/AI协作/任务投影跨宿主分级适配-20260823.md`。其他工作区改动按既有未提交内容保留，不归入本轮交付。

### 维度 1：需求覆盖对账

| 用户诉求 | 落点 | 结论 |
| --- | --- | --- |
| Codex Desktop 重启后继续时恢复同一会话的任务步骤清单 | `task-plan-rehydration-rules/SKILL.md`“重启后用户明确要求继续”规则；`references/source-notes.md` 本轮来源记录 | 已覆盖规则与恢复步骤 |
| UI 显示失败不得阻断主任务 | `task-plan-rehydration-rules/SKILL.md` 中 `UI_SYNC_BLOCKED` 降级继续规则；吸收表记录用户裁决 | 已覆盖；仅投影持久化失败、会话归属不明或执行状态不明时仍按安全规则阻断 |
| 原生步骤清单可见性必须有证据 | `task-plan-rehydration-rules/SKILL.md` 可见性验收规则；本记录“原生 UI 可见性” | 规则已覆盖；本轮没有截图，视觉验收未证实 |
| 本次经验进入后续会话可用的用户级 Skill | Junction 指向的正式落点 `task-plan-rehydration-rules/`；来源、吸收记录与案例均已建立 | 已覆盖；没有写入 `.agents` 副本 |

### 维度 2：影响面与消费方对账

- 本轮新增的是宿主重启恢复条件和验收证据边界，没有改变公开函数、配置键、数据结构、路径协议或外部接口；不存在需要同步的程序消费方。
- 对同域 Skill 内重复 UI 失败语句已收敛为对唯一 `UI_SYNC_BLOCKED` 规则的引用。核对 `task-plan-rehydration-rules/SKILL.md` 中该标记及“同步失败时按本节前述规则处理”的引用，保留正式计划、Goal 生命周期和普通继续入口所需的路由摘要。
- 下游规则通过正式 Junction 指向的 `task-plan-rehydration-rules/SKILL.md` 使用本规则；用户级 Skill 目录确认指向 `D:\谷歌云盘\luode-skills`。没有改写 Junction 以外的 Skill 副本。

### 维度 3：残留物清扫

- 本轮没有启动后台服务、测试进程或临时脚本；没有新增调试开关、打印、孤儿脚本或未使用导入。
- 新增的吸收案例由 Skill 正文与来源记录链接引用；本 `6-review` 由新建的活动索引入口链接。
- 忽略目录 `.workbuddy/memory/2026-10-12.md` 是本轮工作日志，已回读；它受仓库忽略规则管理，不会出现在 Git 状态中。
- 工作区另有既有未提交改动，未清理、回滚或归属于本轮；`git diff --check` 的行尾提示来源为预存脚本 `.system/skill-creator/scripts/quick_validate.py`。

### 维度 4：文档与引用一致性

- `task-plan-rehydration-rules/SKILL.md` 的本轮新增链接指向 `references/source-notes.md`、`workbuddy-absorption-map.md` 与 `references/case-task-plan-rehydration-rules-absorption.md`；三者均存在。
- 新建案例与来源记录由 Skill 主入口直接引用；新建本 `6-review` 由 `doc/6-review/README.md` 链接；不存在改名或删除文件。
- `PROJECT_CURRENT.md` 的本轮摘要指向 Skill 交付物并说明未获取屏幕截图；本轮报告中的同步成功与视觉证据限制与来源记录一致。

### 维度 5：口径一致性

- 用户裁决统一为“UI 不可用时保留投影并继续领域任务”；只有投影持久化失败、会话归属冲突或执行状态不明才阻断领域动作。
- `update_plan` 已注册且当前会话投影校验成功、同步调用成功；该事实没有被写成截图或视觉验收通过。
- Goal 投影在完成事件后状态为 `inactive`，三步均为 `completed`；`PROJECT_CURRENT.md` 和本报告均按已失活状态记录。
- Skill 字典的 `description` 和 `##` 级标题没有改变，因此没有触发字典生成刷新要求。

### 维度 6：验证有效性反审

- Skill 结构结论由 `quick_validate.py` 独立检查器产生；返回 `Skill is valid!`，没有用人工阅读替代该校验。
- 会话同步结论来自真实 `update_plan` 工具调用；该调用仅能证明工具接受同步请求，不能证明悬浮层像素内容已实际显示。
- 没有当前线程原生 UI 截图或独立屏幕检查证据，所以本记录不把“必须可见”目标标为视觉验收通过，也不把 `STYLE: PASS` 扩大为功能验收结论。
- `knowledge_index.py check` 检查 307 篇笔记、797 条链接，违规数与死链数均为 0；知识库笔记回读一致。`audit_vault_knowledge.py --json` 报告的是既有候选组，本轮未改动这些候选。\n- `git diff --check` 只用于检查空白差异，未作为运行行为验证。Python 首次使用系统默认编码失败后，已按 UTF-8 模式重跑；成功结果只对应 Skill 结构校验。

## 问题与修复

- 发现：早期讨论曾把“清单必须可见”误推成“计划工具缺失或失败就暂停领域任务”。
- 处置：按用户澄清撤销该阻断，统一回归 `UI_SYNC_BLOCKED` 降级继续语义，并要求如实记录显示验收证据。
- 遗留：当前会话工具同步调用成功，但没有独立截图可证明原生步骤悬浮层实际呈现；不影响主任务继续规则，也不改变本次 Skill 结构校验与风格结论。

## 执行与追踪附录

- `TASK-PLAN-REHYDRATION-ABSORB-20261012`：将本次 Codex Desktop 重启恢复经验吸收到用户级 `task-plan-rehydration-rules`。
- `TEST-SKILL-VALIDATE-20261012`：运行 Skill 结构校验，结果通过。
- `EVIDENCE-PLAN-UI-01`：同会话投影校验和完成状态证据。
- `EVIDENCE-PLAN-UI-02`：当前工具注册、配置读取和 `update_plan` 成功调用证据；无截图。
- `EVIDENCE-PLAN-UI-03`：`git diff --check` 结果和预存行尾提示。