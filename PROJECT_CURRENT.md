# 项目当前状态

## 更新时间

- 2026-07-26

## 项目概览

- 当前目标：完成 `BUG-RTP-20260726-001` 的“首次持久化即悬浮窗同步”周期 07。
- 当前范围：`ensure-start` 首次投影、持久化后立即 `update_plan`、session 隔离、active/blocked/inactive 可见性、十分钟异常修复、规则文档、专项回归、审查与验收。
- 非范围：Codex Desktop 产品源码、后台定时器、registry v4 schema、Goal 生命周期、子 Agent 主 UI 权限、非 local 服务和 Git 历史写入。
- 当前状态：投影入口与规则文档已完成，专项投影回归 69/69 通过；实现审查、当前改动总审查、最终验收文档和 strict profile 已完成，真实 Desktop 首显证据尚未取得，最终状态保持 `LIMITED/HOST_BLOCKED`。
- 活动会话数：保留 v4 registry 中其它会话投影；本轮仅维护当前会话投影，不代替其它会话失活或完成。

## 当前任务：Plan Mode 计划出口 Bug

- 来源对象：`BUG-PLAN-OUTPUT-20260726-001`；目标：确保 Plan Mode 不再调用 `reasoning-summary-structure-rules` 生成总结，统一由 `implementation-planning-rules` 输出完整计划。
- 当前范围：计划/总结 Skill 边界、命中总控、压缩恢复、双平台规则、脱敏回归、工程文档、审查与验收。
- 当前状态：`TASK-PLAN-01..10` 已完成；`TASK-PLAN-11` 因当前宿主无法创建真实 Plan 会话保持 `in_progress`，最终验收为 `LIMITED/HOST_BLOCKED`。
- 验证状态：专项契约测试 6/6、永久等待状态模型 10/10、六份工程文档 strict、六个 Skill quick_validate、字典生成和 `git diff --check` 均通过；真实 Desktop 用户可见消息未取得。
- 非范围：产品源码、外部服务、Git 历史和其它会话 projection；Obsidian 仍因 `VAULT_NOT_REGISTERED` 阻断，不绕过桥接器。

## 本轮结果与结论详细度切片

- 来源对象：`REQ-SUMMARY-DETAIL-001`；目标是让 `reasoning-summary-structure-rules` 的结果区适中详细，既不退化为“已完成”等空泛结论，也不扩张为执行流水账。
- 当前状态：已完成规则、模板、条件说明、公开示例和专项回归；简单任务默认 3 句，复杂、受限或有关键边界时按事实扩展至 4–5 句，核心始终覆盖问题、方法和结果/验证状态。
- 验证状态：专项单元测试 9/9、Skill `quick_validate.py`、Python 编译、目标差异检查、六份工程文档 strict、实现审查和最终验收均通过；真实模型输出、Desktop UI 和外部服务不在本来源对象范围内。
- 交接状态：当前会话 `019f9a43-800a-73b0-80bb-2a79bf2abd67` 的 `PLAN-SUMMARY-DETAIL-001` 投影已迁移为 `inactive`，三个最小任务均为 `completed`；其它会话 registry 项保持原状。

## 基线与保护边界

- 当前工作树存在大量其它会话和用户未提交改动；只做 scoped 增量修改，不执行 reset、checkout、commit 或 push。
- Plan Mode 决策调用完全省略 `autoResolutionMs`；空答案、缺失答案和隐式超时只能留在 `WAITING_DECISION` 并串行重发同一未决选择框。
- 未决期间不得输出冻结集合 `commentary`、`limited_plan`、`pending_summary`、`proposed_plan`、`final`、`summary`、`final_answer`、`task_complete`、`result_and_conclusion` 或中文“结果与结论”；部分答案只保存已答项并重发剩余问题，只有完整选择、明确代选授权、明确停止或明确宿主故障才离开等待。
- 当前工作树存在用户既有未提交改动；只做 scoped 增量修改，不执行 reset、checkout、commit 或 push。
- Obsidian 沉淀：阻断。doctor 返回 `VAULT_NOT_REGISTERED`，未绕过为直接文件读写。

## 已完成

- 已落盘首次持久化缺失 Bug README、周期 07 实施文档和验收增量，冻结 `REQ-RTP-010..013`、`RULE-RTP-016..022`、`AC-RTP-014..017`。
- 已新增 `ensure-start`、显式 session 优先解析、payload 返回和完成收口，保留 v1-v4 读取兼容；投影专项测试 69/69 通过。
- 已同步 `AGENTS.md`、`skill-hit-check-rules`、`autonomous-execution-rules`、`context-compression-rules` 与投影 Owner，统一“写盘成功后的下一动作立即 `update_plan`”口径。
- 已落盘实现审查、当前改动总审查和周期 07 最终验收文档；审查与文档 strict profile 均 `valid=true`，最终验收为 `LIMITED/HOST_BLOCKED`，未发现 P0/P1。
- 当前会话 `019f9cf5-ee26-75c0-a639-55a73500c7df` 的投影已绑定周期 07；任务 22-27 已完成，任务 28 正在进行，悬浮任务列表需在验证后继续刷新。

## 待完成

- 真实 Desktop `TEST-RTP-024` 首显证据仍缺失；周期 07 的本地实现、回归、Skill 合规、字典、审查和最终验收文档已收口为 `LIMITED/HOST_BLOCKED`，需保留周期状态 `in_progress` 直到宿主补验。

## 阻断

- 真实 Desktop 首个领域动作后的悬浮列表可见性尚未取得可回放证据；宿主自动化边界不允许在本线程直接操作 Codex Desktop，因此 `TEST-RTP-024` 只能保持 `LIMITED/HOST_BLOCKED`，不能以脚本或文本替代。
- Obsidian 固定 vault 未注册，仅影响知识沉淀，不影响本地实现与验证。

## 验证

- 投影专项回归：69/69 通过；`py_compile` 通过；`task-plan-rehydration-rules`、`autonomous-execution-rules` 与 `context-compression-rules` 的 `quick_validate.py` 均通过。
- 需求、验收、周期、Bug、实现审查、当前改动总审查和最终验收 profile 均 `valid=true`；Bug、审查和最终验收保持 `LIMITED`；字典、UTF-8 和 `git diff --check` 已完成复跑。
- `task_plan_projection.py` 当前 session 已绑定周期 07，registry 保留其它会话投影；未写 Git 历史。
- `PROJECT_CURRENT.md`：UTF-8，低于 51,200 字节，托管 registry 保真。

## 下一执行点

- 保留 `TEST-RTP-024` 的真实宿主补验边界；在补验前不把 CLI、静态规则或本地 payload 写成用户可见性通过，周期 07、Bug 和验收状态继续保持 `LIMITED/HOST_BLOCKED`。

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-26T09:22:20.684816Z",
  "projections": [
    {
      "projection_id": "SESSION/53bbdc7515365d913192a90ec514e04314175256f1b1987074ac04697dda7366",
      "session_id": "019f9819-51c9-7380-8ff2-8b77ff9e7966",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RT-20260712-001/CYCLE-RT-13..18",
      "source_document": "doc/3-实施/2026-07-12_190609_通用上线测试引擎_修订版全量实施计划.md",
      "plan_fingerprint": "115c7cfa1e9da5a7d5c68fde68d664219cf2349f3dc387d9c8c474fedeaf507c",
      "updated_at": "2026-07-25T06:50:26Z",
      "steps": [
        {
          "id": "C13-01",
          "step": "[C13-01] 加载 external-scenario/1.0 并跑通 HTTP JSON 读场景",
          "status": "completed"
        },
        {
          "id": "C13-02",
          "step": "[C13-02] 实现候选生成、验证与生命周期迁移",
          "status": "completed"
        },
        {
          "id": "C14-01",
          "step": "[C14-01] 实现 form/multipart 上传读回与清理",
          "status": "completed"
        },
        {
          "id": "C14-02",
          "step": "[C14-02] 实现下载头与内容摘要验证",
          "status": "completed"
        },
        {
          "id": "C14-03",
          "step": "[C14-03] 实现 SSE 关联、断流与重连场景",
          "status": "completed"
        },
        {
          "id": "C15-01",
          "step": "[C15-01] 实现原生 WebSocket 场景",
          "status": "completed"
        },
        {
          "id": "C15-02",
          "step": "[C15-02] 实现 Socket.IO namespace/event/ack 场景",
          "status": "completed"
        },
        {
          "id": "C15-03",
          "step": "[C15-03] 实现 HTTP 到实时事件再到 HTTP 读回",
          "status": "completed"
        },
        {
          "id": "C16-01",
          "step": "[C16-01] 实现外部结果优先与受控只读探针",
          "status": "completed"
        },
        {
          "id": "C16-02",
          "step": "[C16-02] 实现清理、临时命名空间与污染阻断",
          "status": "completed"
        },
        {
          "id": "C16-03",
          "step": "[C16-03] 实现跨协议确定性 oracle",
          "status": "completed"
        },
        {
          "id": "C17-01",
          "step": "[C17-01] 拆分接口结果与场景结果报告",
          "status": "completed"
        },
        {
          "id": "C17-02",
          "step": "[C17-02] 实现 shadow 双轨对账",
          "status": "completed"
        },
        {
          "id": "C17-03",
          "step": "[C17-03] 实现场景硬门禁切换",
          "status": "completed"
        },
        {
          "id": "C18-01",
          "step": "[C18-01] 实现旧资产与 CLI 兼容迁移",
          "status": "completed"
        },
        {
          "id": "C18-02",
          "step": "[C18-02] 实现隔离工具环境与 doctor",
          "status": "completed"
        },
        {
          "id": "C18-03",
          "step": "[C18-03] 完成字典、回归、审查与最终验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/e3fee3201c0f1a9b557248ded3b4691524dd6d9775d8ec03515471ee4143db9c",
      "session_id": "019f9816-ff13-7072-8560-1e7662073134",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "REQ-RTP-001/CYCLE-RTP-05",
      "source_document": "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md",
      "plan_fingerprint": "8e5add7fbb20ad22002f1aab94b6f63f447e75b4c8497ffd2ac9d257df259d17",
      "updated_at": "2026-07-25T08:53:12Z",
      "steps": [
        {
          "id": "TASK-RTP-10",
          "step": "[TASK-RTP-10] 冻结超时升级需求与验收",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-11",
          "step": "[TASK-RTP-11] 补齐悬浮窗超时触发规则",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-12",
          "step": "[TASK-RTP-12] 实现并测试 ensure-timeout CLI",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-13",
          "step": "[TASK-RTP-13] 完成字典回归审查与验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/c2bcdd2ae69ca02ea8bb2c5245216040be065b9bed627279ea8e46cc319828d1",
      "session_id": "019f9550-ec83-7fe1-a9c2-e76721253920",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "inactive",
      "plan_key": "REQ-RT-20260712-001/CYCLE-RT-13..18",
      "source_document": "doc/3-实施/2026-07-12_190609_通用上线测试引擎_修订版全量实施计划.md",
      "plan_fingerprint": "115c7cfa1e9da5a7d5c68fde68d664219cf2349f3dc387d9c8c474fedeaf507c",
      "updated_at": "2026-07-25T16:00:12.390563Z",
      "steps": [
        {
          "id": "C13-01",
          "step": "[C13-01] 加载 external-scenario/1.0 并跑通 HTTP JSON 读场景",
          "status": "completed"
        },
        {
          "id": "C13-02",
          "step": "[C13-02] 实现候选生成、验证与生命周期迁移",
          "status": "completed"
        },
        {
          "id": "C14-01",
          "step": "[C14-01] 实现 form/multipart 上传读回与清理",
          "status": "completed"
        },
        {
          "id": "C14-02",
          "step": "[C14-02] 实现下载头与内容摘要验证",
          "status": "completed"
        },
        {
          "id": "C14-03",
          "step": "[C14-03] 实现 SSE 关联、断流与重连场景",
          "status": "completed"
        },
        {
          "id": "C15-01",
          "step": "[C15-01] 实现原生 WebSocket 场景",
          "status": "completed"
        },
        {
          "id": "C15-02",
          "step": "[C15-02] 实现 Socket.IO namespace/event/ack 场景",
          "status": "completed"
        },
        {
          "id": "C15-03",
          "step": "[C15-03] 实现 HTTP 到实时事件再到 HTTP 读回",
          "status": "completed"
        },
        {
          "id": "C16-01",
          "step": "[C16-01] 实现外部结果优先与受控只读探针",
          "status": "completed"
        },
        {
          "id": "C16-02",
          "step": "[C16-02] 实现清理、临时命名空间与污染阻断",
          "status": "completed"
        },
        {
          "id": "C16-03",
          "step": "[C16-03] 实现跨协议确定性 oracle",
          "status": "completed"
        },
        {
          "id": "C17-01",
          "step": "[C17-01] 拆分接口结果与场景结果报告",
          "status": "completed"
        },
        {
          "id": "C17-02",
          "step": "[C17-02] 实现 shadow 双轨对账",
          "status": "completed"
        },
        {
          "id": "C17-03",
          "step": "[C17-03] 实现场景硬门禁切换",
          "status": "completed"
        },
        {
          "id": "C18-01",
          "step": "[C18-01] 实现旧资产与 CLI 兼容迁移",
          "status": "completed"
        },
        {
          "id": "C18-02",
          "step": "[C18-02] 实现隔离工具环境与 doctor",
          "status": "completed"
        },
        {
          "id": "C18-03",
          "step": "[C18-03] 完成字典、回归、审查与最终验收",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/e0641079a9b3807614bb7bea657755435440b1b8a87869e3e169419fef60eb93",
      "session_id": "019f98be-5f55-7c40-9dcb-0d31788ff83c",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "CYCLEDOC-RTP-05",
      "source_document": "doc/3-实施/2026-07-25_163230_CodexDesktop任务悬浮窗断点恢复_实施周期05_超时自动升级.md",
      "plan_fingerprint": "78fe389ec6fcf8820370aaee55972c5702eb014a1f1277bc848630786471950f",
      "updated_at": "2026-07-25T10:44:00.535000Z",
      "steps": [
        {
          "id": "TASK-RTP-10",
          "step": "[TASK-RTP-10] 冻结超时需求、验收、总览和周期追踪",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-11",
          "step": "[TASK-RTP-11] 让唯一 Owner 与相邻执行路由表达一致的超时规则",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-12",
          "step": "[TASK-RTP-12] 实现可验证且无 schema 漂移的 `ensure-timeout` CLI",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-13",
          "step": "[TASK-RTP-13] 补齐测试、生成资产、项目状态和合规证据",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/3973c62658af29715b77501632a92f3b40cba5d0771b4b64bb71c98ceb451c21",
      "session_id": "019f98d4-9fd6-73c2-ad35-acf08ad74ac1",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "CYCLEDOC-RTP-06",
      "source_document": "doc/3-实施/2026-07-25_203000_CodexDesktop任务悬浮窗断点恢复_实施周期06_Goal自动升级.md",
      "plan_fingerprint": "73134d0acf46d2ec23f4a9f874465450559529584a17f518ed4ef77f38f252f9",
      "updated_at": "2026-07-25T13:57:52.005254Z",
      "steps": [
        {
          "id": "TASK-RTP-14",
          "step": "[TASK-RTP-14] 冻结需求变更和验收",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-15",
          "step": "[TASK-RTP-15] 冻结 Cycle 06 执行契约",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-16",
          "step": "[TASK-RTP-16] 新增无写入 `probe-timeout`",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-17",
          "step": "[TASK-RTP-17] 冻结 Goal 编排和失败降级",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-18",
          "step": "[TASK-RTP-18] 同步连续执行与 standing authorization",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-19",
          "step": "[TASK-RTP-19] 同步全局规则和项目记忆",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-20",
          "step": "[TASK-RTP-20] 完成字典与自动回归",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-21",
          "step": "[TASK-RTP-21] 完成真实 Desktop 审查验收",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/2ac02581582ba844cadf597eeea6bf0056e817767fe90edffde4a54da2617807",
      "session_id": "019f9a5c-65d7-7312-a3d2-5bd5533dbe1a",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "IMP-PMW-001",
      "source_document": "doc/3-实施/2026-07-26_040639_BUG-PLAN-WAIT-20260726-001_实施总览.md",
      "plan_fingerprint": "803519e47bb6c839a34fa8fbd83fe9dab4f58939090177a4293c777d100e428a",
      "updated_at": "2026-07-25T21:10:00Z",
      "steps": [
        {
          "id": "TASK-PMW-01",
          "step": "[TASK-PMW-01] `TASK-PMW-01`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-02",
          "step": "[TASK-PMW-02] `TASK-PMW-02`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-03",
          "step": "[TASK-PMW-03] `TASK-PMW-03`",
          "status": "completed"
        },
        {
          "id": "TASK-PMW-04",
          "step": "[TASK-PMW-04] `TASK-PMW-04`",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/7931d74771fbbf6f11294b901bd9909bf47008569a75f10070efbb8186297805",
      "session_id": "019f9cf5-ee26-75c0-a639-55a73500c7df",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "active",
      "plan_key": "CYCLE-RTP-07",
      "source_document": "doc/3-实施/2026-07-26_150000_CodexDesktop任务悬浮窗断点恢复_实施周期07_首次持久化即悬浮窗同步.md",
      "plan_fingerprint": "b19faa6359fd7434e012cedaa2cb3e9ae7373b74b8e540e4149f65ece8c4733f",
      "updated_at": "2026-07-26T15:00:00Z",
      "steps": [
        {
          "id": "TASK-RTP-22",
          "step": "[TASK-RTP-22] session 与 ensure-start",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-23",
          "step": "[TASK-RTP-23] 投影回归",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-24",
          "step": "[TASK-RTP-24] Owner UI 闸门",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-25",
          "step": "[TASK-RTP-25] 恢复与状态路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-26",
          "step": "[TASK-RTP-26] 自治与上下文路由",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-27",
          "step": "[TASK-RTP-27] 文档与 profile",
          "status": "completed"
        },
        {
          "id": "TASK-RTP-28",
          "step": "[TASK-RTP-28] 字典、审查与真实验收",
          "status": "in_progress"
        }
      ]
    },
    {
      "projection_id": "SESSION/71df5f38455c3a5ee4c8ff567163229e45ab77d8eb0f40c258f8fcb2cdf9f5df",
      "session_id": "019f9a43-800a-73b0-80bb-2a79bf2abd67",
      "projection_origin": "synthesized",
      "synthesis_mode": "exact",
      "state": "inactive",
      "plan_key": "PLAN-SUMMARY-DETAIL-001",
      "source_document": "doc/3-实施/2026-07-26_073000_reasoning-summary-structure-rules_结果与结论详细度_实施总览.md",
      "plan_fingerprint": "f9311cab0a07ace29835d15029ec024e9318472089444a4878792abba65661fe",
      "updated_at": "2026-07-26T08:25:07.435729Z",
      "steps": [
        {
          "id": "TASK-SUMMARY-DETAIL-01",
          "step": "[TASK-SUMMARY-DETAIL-01] `CYCLE-SUMMARY-DETAIL-01`",
          "status": "completed"
        },
        {
          "id": "TASK-SUMMARY-DETAIL-02",
          "step": "[TASK-SUMMARY-DETAIL-02] `CYCLE-SUMMARY-DETAIL-02`",
          "status": "completed"
        },
        {
          "id": "TASK-SUMMARY-DETAIL-03",
          "step": "[TASK-SUMMARY-DETAIL-03] `CYCLE-SUMMARY-DETAIL-03`",
          "status": "completed"
        }
      ]
    },
    {
      "projection_id": "SESSION/fd59b49ba40d507de38be62f910b6551b82a8d84a2bd733dc080c52dd1d32c06",
      "session_id": "019f9d75-5d5c-7a30-a262-71d2c7806880",
      "projection_origin": "persisted",
      "synthesis_mode": "none",
      "state": "active",
      "plan_key": "IMPLEMENTATION-PLAN-OUTPUT-001",
      "source_document": "doc/3-实施/2026-07-26_BUG-PLAN-OUTPUT-20260726-001_实施总览.md",
      "plan_fingerprint": "6ff907ed2ca8398cf86b7b28800dc5af1111dd2878aaa1a6e26518116b29051a",
      "updated_at": "2026-07-26T09:25:00Z",
      "steps": [
        {
          "id": "TASK-PLAN-01",
          "step": "[TASK-PLAN-01] 建立脱敏会话夹具与失败基线",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-02",
          "step": "[TASK-PLAN-02] 增加总结 Skill 的 Plan Mode 负向退出",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-03",
          "step": "[TASK-PLAN-03] 让计划 Skill 接管唯一计划出口",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-04",
          "step": "[TASK-PLAN-04] 冻结等待闸门与压缩恢复",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-05",
          "step": "[TASK-PLAN-05] 同步命中总控与 Plan Mode 排除路由",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-06",
          "step": "[TASK-PLAN-06] 同步 AGENTS、CLAUDE 与 bootstrap 生成源",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-07",
          "step": "[TASK-PLAN-07] 补齐 Bug、需求、实施与验收文档链",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-08",
          "step": "[TASK-PLAN-08] 生成 Skill 字典并同步项目记忆",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-09",
          "step": "[TASK-PLAN-09] 执行专项回归与合规校验",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-10",
          "step": "[TASK-PLAN-10] 完成实现审查与当前改动审查",
          "status": "completed"
        },
        {
          "id": "TASK-PLAN-11",
          "step": "[TASK-PLAN-11] 验证真实新 Plan 会话的用户可见出口",
          "status": "in_progress"
        }
      ]
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
