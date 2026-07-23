---
schema_version: 1
doc_id: "TESTDOC-RTP-PRE-RESTART-001"
doc_type: "test"
source_ids: ["SRC-RTP-001", "SRC-RTP-002", "SRC-RTP-003", "PLAN-RTP-001", "CYCLE-RTP-04"]
status: "accepted"
version: "v1.0"
current_slice: "TASK-RTP-01 至 TASK-RTP-07 本地验证完成"
updated_at: "2026-07-23 02:02:02"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
review_acceptance_gates:
  - stage: functional_validation
    applicability: applicable
    reason: 投影脚本、相邻 Skill、自举模板和严格追踪修复均可在 local 工作区真实验证。
    basis: 用户实施计划中的 TEST-RTP-001 至 TEST-RTP-007。
    required_by_source: true
    required_now: true
    completed_validation: ["EVD-TASK-RTP-01-TEST", "EVD-TASK-RTP-02-TEST", "EVD-TASK-RTP-03-TEST", "EVD-TASK-RTP-04-TEST", "EVD-TASK-RTP-05-TEST", "EVD-TASK-RTP-06-TEST", "EVD-TASK-RTP-07-TEST"]
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: 本地命令全部满足各自断言，失败样本不破坏原文件。
  - stage: acceptance
    applicability: limited
    reason: Desktop 真实关闭重开必须由用户操作，当前只能完成重启前本地验证。
    basis: TEST-RTP-008 明确要求关闭并重新打开同一任务。
    required_by_source: true
    required_now: false
    completed_validation: []
    substitute_validation: ["活动投影跨进程读取与 update_plan payload 重建已通过"]
    manual_follow_up: 关闭 Codex Desktop，重新打开同一任务并发送“继续任务”。
    pass_standard: 首次继续回合恢复九个步骤及原状态，进行中步骤只核验不重放写操作。
  - stage: third_party
    applicability: not_applicable
    reason: 本轮不调用第三方业务服务。
    basis: 所有验证均限定在当前 local 文件系统和 Codex Desktop。
    required_by_source: false
    required_now: false
    completed_validation: []
    substitute_validation: []
    manual_follow_up: N/A
    pass_standard: N/A
---

# Codex Desktop 任务悬浮窗断点恢复本地测试记录

结论：真实重启前的本地验证通过；影响：任务投影脚本、相邻规则、自举模板和字典已具备进入 Desktop 关闭重开验收的条件；范围：当前 local Skills 工作区和临时目录；非范围：尚未执行的真实 Desktop 关闭重开；变化：已验证活动投影可跨进程读取并生成一致的悬浮任务列表参数；完成标准：任务一至任务七的命令与断言全部通过；术语说明：悬浮任务列表参数是交给 Codex 任务工具重建界面的步骤和状态；验证状态：本地验证通过，最终验收受限；图片资产决策：N/A + 原因 + 证据：本测试不涉及位图资产。

## 验证结论

`TASK-RTP-01` 至 `TASK-RTP-07` 的本地实现和验证均已完成。对会话 `019f851d-f04d-75f1-87c3-7bb2290d43c4` 的核验确认它属于另一项“继续精简需求流程 skill”任务，不能错误显示 `REQ-RTP-001` 九步计划；其首条继续路由仍漏掉恢复 Owner，现已补齐并增加归属阻断。`TASK-RTP-08` 仍须在正确的“恢复任务悬浮计划”会话中完成真实关闭重开验收。

## 完成标准

- 投影脚本 17 项单元测试全部通过。
- 严格追踪修复的 3 项定向回归全部通过。
- 6 个受影响 Skill 的 UTF-8 quick validate 全部通过。
- 自举脚本在临时目录创建合法失活槽位，重复运行哈希不变。
- 字典生成结果为 `implemented_total=73`、`planned_missing=0`、`seed_total=34`。
- `git diff --check` 无错误；工作树行尾提示不属于格式错误。

## 本地证据矩阵

| 任务 | 实现证据 | 测试证据 | 结果 |
|---|---|---|---|
| `TASK-RTP-01` | `EVD-TASK-RTP-01-IMPL`：8 份工程文档已落盘 | `EVD-TASK-RTP-01-TEST`：8 个 profile 已通过 | 通过 |
| `TASK-RTP-02` | `EVD-TASK-RTP-02-IMPL`：新 Skill、agent 元数据和契约已落盘 | `EVD-TASK-RTP-02-TEST`：quick validate 通过 | 通过 |
| `TASK-RTP-03` | `EVD-TASK-RTP-03-IMPL`：原子投影脚本和测试已落盘 | `EVD-TASK-RTP-03-TEST`：17/17 单元测试通过 | 通过 |
| `TASK-RTP-04` | `EVD-TASK-RTP-04-IMPL`：项目记忆和自举模板已接入 | `EVD-TASK-RTP-04-TEST`：临时目录自举与重复运行幂等 | 通过 |
| `TASK-RTP-05` | `EVD-TASK-RTP-05-IMPL`：状态迁移固定为先持久化再调用工具 | `EVD-TASK-RTP-05-TEST`：三态迁移跨新读取保持一致 | 通过 |
| `TASK-RTP-06` | `EVD-TASK-RTP-06-IMPL`：继续回合、压缩恢复和 L5 边界已接入 | `EVD-TASK-RTP-06-TEST`：有效、过期、完成和中断样本通过 | 通过 |
| `TASK-RTP-07` | `EVD-TASK-RTP-07-IMPL`：根规则、字典和项目记忆已刷新 | `EVD-TASK-RTP-07-TEST`：生成器、quick validate、diff check 通过 | 通过 |

## 命令与结果

| 命令 | 结果 |
|---|---|
| `python -B task-plan-rehydration-rules/tests/test_task_plan_projection.py` | 17 项通过 |
| `python -X utf8 -m unittest ...test_strict_trace_* -v` | 3 项通过 |
| `python -X utf8 .system/skill-creator/scripts/quick_validate.py <skill>` | 6 个受影响 Skill 全部有效 |
| `python -X utf8 skill-dictionary/generate_dictionary.py` | 73 个已实现 Skill、0 个缺失 |
| `git diff --check` | 退出码 0 |
| `python -X utf8 -m unittest artifact-delivery-gate-rules.tests.test_validate_engineering_docs -v` | 53 项通过；`test-strategy-rules/references/doc-minimums.md` 已恢复并修正模板注册表路径 |

## 首次真实继续失败与修复

- 证据来源：会话 `019f851d-f04d-75f1-87c3-7bb2290d43c4` 的用户消息为“继续”，其标题和历史内容属于“继续精简需求流程 skill (2)”，不属于 `REQ-RTP-001/CYCLE-RTP-04`；因此该会话不应显示九步恢复计划。其首条命中列表仍未包含 `task-plan-rehydration-rules`，也没有 `update_plan` 工具调用。
- 根因：总控入口没有强制继续类消息先检查恢复 Owner；同时旧规则缺少“当前会话与活动投影来源不匹配时明确阻断”的安全边界，恢复 Skill 文案还使用了不存在的 `--file` 参数。
- 修复：总控入口、命中清单、平台规则和自举模板均要求继续类消息先列出恢复 Owner；来源无法确认或不匹配时禁止错投；恢复 Owner 文案改为 `--project-current`；新增三项回归断言。
- 本地复验：`python3 -X utf8 -B task-plan-rehydration-rules/tests/test_task_plan_projection.py` 通过 20/20；三个受影响 Skill 的 quick validate 与自举脚本语法检查通过；当前“恢复任务悬浮计划”会话已使用有效活动投影真实调用 `update_plan`。
- 剩余人工验收：在正确的“恢复任务悬浮计划”会话中完成关闭重开并发送“继续任务”；其它任务会话应先出现恢复 Owner 的归属校验结论，但不得显示不属于自己的九步计划。

## 清理与保护

- 自举验证使用系统临时目录并由 `trap` 清理，没有修改真实项目状态文件。
- 投影脚本负向测试只写临时目录，损坏、超限和替换失败样本均保持原文件不变。
- 未连接 test、staging 或 production 环境。

## 受限项

`TASK-RTP-08` 尚未完成。人工补验入口是关闭 Codex Desktop、重新打开同一任务并发送“继续任务”；通过标准是悬浮窗恢复九个步骤及状态，且 `TASK-RTP-08` 只进入中断点核验。
