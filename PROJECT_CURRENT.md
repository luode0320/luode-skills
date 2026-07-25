# 项目当前状态

## 更新时间

- 2026-07-25

## 项目概览

- 当前目标：实施“主动执行严格超过 600 秒时优先自动创建或复用 Goal，失败降级普通任务悬浮窗”的跨会话策略。
- 当前范围：只读超时资格探测、Goal 宿主编排契约、连续执行与平台授权、工程文档、项目记忆、字典、回归、审查和最终验收。
- 非范围：Codex Desktop 产品代码、后台定时器、Goal 工具内部实现、非 local 服务和 Git 历史写入。
- 当前状态：核心实现、自动化回归、严格文档门禁、正常宿主 Goal 工具链和测试投影清理均完成；宿主失败编排缺少可执行模拟，独立用户可见截图受 Computer Use 安全规则限制，最终验收保持 LIMITED。
- 活动会话数：保留 v4 registry 中其它会话投影；本轮仅维护当前会话投影，不代替其它会话失活或完成。

## 基线与保护边界

- 当前工作树存在大量其它会话和用户未提交改动；只做 scoped 增量修改，不执行 reset、checkout、commit 或 push。
- `probe-timeout` 只读且无锁文件、临时文件或 projection 副作用；原 `ensure-timeout` 保持普通 exact/fallback 降级入口。
- Goal 工具只由当前主 Agent 调用；Plan Mode、许可不足、任务完成、计时丢失、不匹配或状态不明确时不创建 Goal。
- Goal 摘要只传给 `create_goal`，单行中文、不超过 80 字并脱敏；不得进入项目文件、fixture、工程文档或知识库。
- Obsidian 沉淀：阻断。doctor 返回 `VAULT_NOT_REGISTERED`，未绕过为直接文件读写。

## 已完成

- 新增无写入 `probe-timeout` CLI，严格覆盖 599/600/600.001/601 秒、暂停扣除、active/blocked/inactive、其它 session 和损坏 registry。
- 修复实现审查发现的瞬时锁文件副作用；专项回归增至 63 项并全部通过。
- 冻结 `probe-timeout -> get_goal -> 复用匹配 Goal 或 create_goal 一次 -> goal create -> update_plan` 顺序、单次创建、结果不明确一次复核和失败降级。
- 同步任务投影 Owner、OpenAI agent 提示、自主执行规则、仓库和父目录 standing authorization、项目记忆与字典。
- 真实宿主 `create_goal/get_goal/update_plan/update_goal(complete)` 通过；正式任务接管返回 `preserved_formal`；测试投影已清理。
- 需求、验收、实施总览、全量顺序、周期 06、测试报告、实现审查、当前改动总审查和最终验收文档已落盘。

## 待完成

- 仅剩人工确认当前任务中 Goal 卡片、固定安全三步和正式任务替换的用户可见结果，以及未来具备宿主调用拦截器后补测四类失败编排；无需重新等待十分钟。

## 阻断

- Computer Use 安全规则禁止自动操作或截图 ChatGPT/Codex Desktop，独立视觉证据受限；Goal 不匹配、创建结果不明确、投影写失败和 update_plan 失败也缺少可执行宿主模拟，均未伪报完整 PASS。
- Obsidian 固定 vault 未注册，仅影响知识沉淀，不影响本地实现与验证。

## 验证

- `task_plan_projection.py`：63 项通过；`py_compile` 通过。
- `quick_validate.py task-plan-rehydration-rules` 与 `autonomous-execution-rules`：通过。
- 六份核心工程文档严格 profile：全部通过；新增测试/审查/最终验收文档 profile：通过，最终验收状态 LIMITED。
- 字典生成器成功刷新 `skill-dictionary/data.js` 与 `字典.md`。
- `git diff --check`：退出码 0，仅既有 LF/CRLF 提示。
- `PROJECT_CURRENT.md`：UTF-8，低于 51,200 字节，托管 registry 保真。

## 下一执行点

- 用户确认视觉结果后，仅需把最终验收从 LIMITED 改为 PASS；在此之前不继续扩散实现范围。

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 4,
  "registry_schema": "task_plan_projection_registry",
  "registry_updated_at": "2026-07-25T16:00:12.398746Z",
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
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
