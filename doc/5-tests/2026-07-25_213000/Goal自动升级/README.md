---
schema_version: 1
doc_id: "TESTREPORT-RTP-GOAL-001"
doc_type: "test"
source_ids: ["SRC-RTP-005", "CYCLE-RTP-06", "TEST-RTP-013", "TEST-RTP-014", "TEST-RTP-015", "TEST-RTP-016", "TEST-RTP-017", "TEST-RTP-018"]
status: "accepted"
version: "v1.0"
current_slice: "TASK-RTP-20/TASK-RTP-21"
updated_at: "2026-07-25 21:30:00"
reader_level: "business_general"
writing_style: "plain_chinese"
appendix_policy: "preserve_existing_or_one_terminal_appendix"
review_acceptance_gates:
  - stage: acceptance
    applicability: limited
    reason: 正常宿主链路和投影降级入口已通过，但没有可执行宿主编排器模拟 Goal 不匹配、创建结果不明确、投影写失败和 update_plan 失败；Computer Use 安全规则也禁止自动操作或截图 Codex 应用。
    basis: TEST-RTP-015..018、最终只读复审与 Windows Computer Use 非协商安全规则。
    required_by_source: true
    required_now: true
    completed_validation: []
    substitute_validation: ["EVIDENCE-RTP-015", "EVIDENCE-RTP-016", "EVIDENCE-RTP-018-HOST"]
    manual_follow_up: 用户后续确认当前任务中曾显示脱敏 Goal 卡片、安全三步和正式验收任务列表；宿主可测试编排器可用后补测四类失败分支。
    pass_standard: 用户可见内容与 create_goal 目标、update_plan 两次成功 payload 一致，没有第二个 Goal 或遗留测试投影。
---

# 长任务自动 Goal 升级测试报告

结论：只读探测、普通投影降级入口和正常宿主工具链通过，失败编排集成与独立截图观察受限；影响：严格超时、Goal 单次创建、安全三步、正式任务接管和清理有证据，但不能把未执行的宿主失败模拟记为通过；范围：本地 Python、临时目录、当前宿主 Goal 与任务列表工具；非范围：Desktop 产品源码和自动化截图；变化：测试基线从 57 项增至 63 项；完成标准：自动用例无失败、真实 Goal 完成、测试投影清零，未覆盖项明确降级；术语说明：工具成功返回表示该次宿主动作完成，不代表所有失败分支均已执行；验证状态：核心自动化 PASS，失败编排与人工可见确认 LIMITED。图片资产决策：N/A。原因：本报告不交付图片资产；证据：替代证据为结构化工具返回。

## 验证结论

| 测试 | 结果 | 关键证据 |
|---|---|---|
| `TEST-RTP-013/014` | PASS | 599、600、600.001、601 秒、暂停、状态和 session 隔离通过；目录无副作用 |
| `TEST-RTP-015` | LIMITED | 无活动 Goal 的创建与重复查询通过；匹配复用、不匹配降级未做可执行宿主模拟 |
| `TEST-RTP-016` | LIMITED | 原 `ensure-timeout` fallback 真实通过；Goal 失败、结果不明确、投影写失败和 UI 失败仅有规则契约 |
| `TEST-RTP-017` | LIMITED | Plan Mode、许可、完成和计时丢失已有跨文件契约断言，但没有宿主调用拦截器证明零调用 |
| `TEST-RTP-018` | LIMITED | Goal、安全三步、正式任务接管、complete 和清理通过；独立截图受限 |

## 完成标准

63 项测试、py_compile、两个 quick validate、六份严格文档 profile 和 `git diff --check` 全部通过。真实 `create_goal/get_goal/update_plan/update_goal(complete)` 均成功；独立测试投影已删除，其它 5 个会话条目保真。

## 执行附录

证据包括 `EVIDENCE-RTP-013..018`。测试 Goal 使用脱敏单行中文并已真实完成；目标原文、Goal ID、计时事实和宿主响应未写入投影或项目记忆。

## 追踪附录

`SRC-RTP-005 -> CYCLE-RTP-06 -> TASK-RTP-14..21 -> TEST-RTP-013..018 -> EVIDENCE-RTP-013..018 -> AC-RTP-010..013`；`AC-RTP-010` 为 PASS，`AC-RTP-011..013` 的已执行宿主动作、隐私和终态证据有效，未执行的失败编排与独立视觉确认为 LIMITED。
