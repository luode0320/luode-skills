# 项目当前状态

## 更新时间

- 2026-07-24

## 当前任务

- 目标：实现 Codex Desktop 在“继续”但无历史任务投影时，也能正式补建悬浮任务列表。
- 范围：`version: 2` 投影 schema、`synthesize` 脚本入口、只读子代理证据契约、继续路由、规则文案、测试、字典、项目记忆与审查收口。
- 非范围：修改 Codex Desktop 产品代码、跨会话搜索、自动恢复未知幂等性的写操作、无用户新消息时自动显示悬浮窗。
- 状态：实施中；`TASK-SYN-01`、`TASK-SYN-02`、`TASK-SYN-03` 已完成，`TASK-SYN-04` 正在进行真实重开前的最终验证与验收收口。

## 基线与保护边界

- 基线 commit：`76ee419d59396d919fea04ed55ea373ddeb8cb26`。
- 当前工作树存在大量用户未提交改动；所有编辑基于当前磁盘内容增量完成，不执行 reset、checkout 或覆盖式回退。
- 投影只保存任务 ID、悬浮文案和三态状态，不保存 prompt、响应、凭据、线程 ID、业务数据或原始用户输入。
- 无投影补建只允许使用当前会话与项目文档证据；子代理只做只读证据收集，不做最终归属裁决。
- 当前轮没有 Git 写历史授权，最终保持已改动未提交。

## 已完成

- 落盘需求、验收标准、全量顺序、实施总览和四个实施周期共 8 份文档，全部通过各自 profile。
- 修复严格追踪校验器按目标文档根 `source_ids` 选域，并通过 3 项定向回归。
- 创建 `task-plan-rehydration-rules`、投影契约、原子读写脚本和 16 项单元测试；UTF-8 quick validate 通过。
- 完成项目记忆、自举模板、自主执行、上下文恢复和运行时恢复的规则接入补丁。
- 完成 6 个受影响 Skill 的 UTF-8 quick validate、字典刷新、临时目录自举幂等验证和 `git diff --check`。
- 落盘真实重启前测试记录、阶段审查和阶段验收；任务一至任务七具备实现、测试、审查和验收证据。
- 已从会话 `019f851d-f04d-75f1-87c3-7bb2290d43c4` 取得真实证据：该会话标题为“继续精简需求流程 skill (2)”，与当前 `REQ-RTP-001/CYCLE-RTP-04` 投影不是同一来源；它不应错误重建九步恢复计划。该会话首条命中列表同时漏掉 `task-plan-rehydration-rules`，已补齐继续类消息路由、来源不确定阻断、精确 CLI 参数和 20 项回归测试。
- 修正 Plan Mode 与任务投影的阶段边界：Plan Mode 只形成、修改或确认执行计划并保留用户选择；不读取投影、不调用 `update_plan`、不创建任务悬浮窗。只有 Plan Mode 结束后进入执行阶段，才允许重建 UI 并核验中断点。
- 已实现 `version: 2` 投影 schema、`projection_origin/synthesis_mode` 与 `synthesize` CLI，覆盖 `exact` 正式补建和固定三步 `fallback` 安全恢复列表。
- 已完成 30 项任务投影脚本与恢复路由回归，其中包含无投影精确补建、证据不足回退、payload explanation 分支和文档契约断言。

## 待完成

- 在 Codex Desktop 中分别完成 persisted、exact synth 与 fallback synth 三条路径的真实关闭/重开验收。
- 验收通过后把当前 `TASK-SYN-*` 活动投影设为 `inactive`，再决定是否回到旧 `REQ-RTP-001` 验收链路。

## 阻断

- Obsidian 固定 vault 当前未注册；仅阻断可复用知识沉淀，不阻断本地实现与验证。
- 校验器整套回归：`test-strategy-rules/references/doc-minimums.md` 已恢复到唯一 Owner，工程文档校验器 53/53 通过。
- 真实 Desktop 关闭重开验收需要用户操作；完成前只能给出本地契约通过的受限结论。

## 验证

- 8 份工程文档 profile：通过。
- 严格追踪定向回归：3/3 通过。
- `PROJECT_CURRENT` 投影校验与 payload 生成：通过；当前活动投影已升级到 `version: 2`，并可稳定生成 `TASK-SYN-*` 悬浮列表 payload。
- 任务投影脚本及恢复路由回归：30/30 通过。
- `task-plan-rehydration-rules`、`skill-hit-check-rules`、`project-rule-file-bootstrap-rules` quick validate：通过；`bootstrap_agents.sh` 的 `bash -n` 通过。
- 字典刷新：通过；`implemented_total=73`、`planned_missing=0`、`seed_total=34`。
- `git diff --check`：通过（仅剩现有 LF->CRLF warning，无 diff 硬错误）。
- Plan Mode 不恢复任务悬浮窗回归：21/21 通过；`task-plan-rehydration-rules`、`skill-hit-check-rules` 与 `implementation-planning-rules` 的 UTF-8 quick validate 通过。
- 当前“恢复任务悬浮计划”会话已真实调用 `update_plan`，九步 `TASK-RTP` 悬浮列表重建成功；该结果不代表其它任务会话应显示这九步。
- 严格追踪修复定向回归：3/3 通过。
- 6 个受影响 Skill quick validate：UTF-8 模式全部通过。
- bootstrap 临时项目：合法失活槽位、重复运行哈希一致。
- 字典：`implemented_total=73`、`planned_missing=0`、`seed_total=34`。
- `git diff --check`：通过。
- validator 全量回归：53/53 通过；`doc-minimums.md` 路径与模板注册表引用均已修正。

## 下一执行点

- 在 Codex Desktop 中执行真实关闭/重开验收，分别覆盖 persisted、exact synth 和 fallback synth 三条路径；验收完成后把当前活动投影失活，并决定是否并回旧 `REQ-RTP-001` 收口链路。

<!-- BEGIN TASK PLAN PROJECTION -->
```json
{
  "version": 2,
  "state": "active",
  "projection_origin": "persisted",
  "synthesis_mode": "none",
  "plan_key": "REQ-RTP-001/SYNTH-CYCLE-01",
  "source_document": "doc/3-实施/2026-07-23_012302_CodexDesktop任务悬浮窗断点恢复_实施总览.md",
  "plan_fingerprint": "d3a583e140cf5500adec980a5491a97ead5ca20163a5b0371851b3e577385b9e",
  "updated_at": "2026-07-24T01:00:00Z",
  "steps": [
    {
      "id": "TASK-SYN-01",
      "step": "[TASK-SYN-01] 冻结补建 schema、证据边界与 explanation 契约",
      "status": "completed"
    },
    {
      "id": "TASK-SYN-02",
      "step": "[TASK-SYN-02] 实现 synthesize 脚本与 exact/fallback 状态映射",
      "status": "completed"
    },
    {
      "id": "TASK-SYN-03",
      "step": "[TASK-SYN-03] 接入继续路由、规则同步与 PROJECT_CURRENT 投影升级",
      "status": "completed"
    },
    {
      "id": "TASK-SYN-04",
      "step": "[TASK-SYN-04] 完成 quick validate、字典刷新与真实重开验收",
      "status": "in_progress"
    }
  ]
}
```
<!-- END TASK PLAN PROJECTION -->
