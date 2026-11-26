# 计划完善度闸门（plan-readiness-gate）

本 reference 是「计划 READY 才准开写」这道收口闸门的唯一判据来源。它把已有的 `plan-output-gate`、`plan-feasibility-probe`、`plan-devils-advocate-review` 从「字段齐全与否」收敛成「可机器判定、可阻断的三态结论」，解决"计划不完善就开写、写完又回到老问题"的根因。

## 适用范围与强制时机

- 任何会改变可执行行为的代码任务（新增 / 修改 / 重构 / Bug 修复），在 agent 动手写码前，计划必须先被判定为 `READY`。
- Plan Mode 正式计划在 `<proposed_plan>` 输出前过闸门；非 Plan Mode 的 `minimum-plan-grading` 轻量通道也要过 **lite 档**闸门，不豁免。
- 纯文档、纯注释、纯排版、纯静态资源改名 / 搬运等不改变运行结果的场景，可写明免测理由，但仍需过来源落盘与决策无未决两项。
- 本闸门与「反打补丁 / 重构立即提示」并行生效：计划 READY 不等于可绕过根因或跳过重构提示。

## 两档判据

### 定档规则

未显式 `--tier` 时，脚本按 `plan-output-gate` 的复杂任务判据自动选档：实施周期≥2 / 最小任务≥3 / 跨≥2 模块 / 含时序或状态迁移 → `full`，否则 `lite`。可用 `--tier full|lite` 强制。

### lite 档（中等改动：五项核心，缺任一 NEEDS_REFINEMENT）

1. **来源落盘**：需求 / Bug 主文档路径真实存在（检查路径与文件存在性）。
2. **边界清楚**：范围 / 归属 / 兼容性章节齐全，不是空的 N/A 占位。
3. **完成条件可测**：AC 含可验证动作（运行 / 测试 / 断言 / 退出码等），禁「完成即可 / 正常即可」类空话。
4. **决策无未决**：出现 `WAITING_DECISION` / 未决 / 待确认 / TBD / TODO → 直接 BLOCKED。
5. **反方批判**：含 `plan-devils-advocate-review` 的 3 选 1 结论段。

### full 档（重大改动：lite 五项 + 追加四项）

6. **plan-output-gate 必填字段**：实施周期、最小任务、真实测试安排、验证点齐全。
7. **FEAS-* 清单**：存在可行性探针清单；方向级假设必须为「已探针验证」，未验证 / 待验证 → BLOCKED。
8. **追踪链**：REQ → AC → CYCLE → TASK → TEST → EVIDENCE 覆盖完整（至少 4 段标记）。
9. **跨会话可执行性**：说明脱离当前会话后仍可独立执行。

## 机器校验脚本

- 路径：`scripts/check_plan_readiness.py`（随本 skill 分发）。
- 用法：`python scripts/check_plan_readiness.py <plan.md> [--tier full|lite] [--explain]`。
- 三态与退出码：**READY=0 / NEEDS_REFINEMENT=1 / BLOCKED=2**；`--explain` 逐项打印命中 / 未命中，便于人工复核启发式误判。
- 判定原则：只认章节标题 + 字段标记 + 非占位内容（保守阈值 + 空话词表），**不认自评词**；宁可漏判不可误杀 READY。

## 三态处置

| 判定 | 含义 | 动作 |
|---|---|---|
| READY (0) | 计划满足当前档全部判据 | 放行开写 |
| NEEDS_REFINEMENT (1) | 有字段缺失或空话，但无未决决策 | 回到计划补齐缺失项后重跑，禁止带病开写 |
| BLOCKED (2) | 存在未决决策 / 未验证方向级假设 / 计划文档不存在 | 先解决决策探针与文档落盘，重跑闸门 |

脚本启发式存在误杀可能：agent 若认定判定错误，须在计划文档写明理由并让人为复核，不得直接忽略闸门结果继续开写。

## 回归样例

`tests/fixtures/` 下保留四份：`lite_ready.md`（期望 0）、`full_ready.md`（期望 0）、`missing_ac.md`（期望 1）、`undecided.md`（期望 2）；配套 `docs/requirement-demo.md` 供来源落盘检查。修改判据后必须重跑四份并核对退出码。

## 与相邻 reference 的边界

- `plan-output-gate`：定义"计划要写哪些字段"；本文件定义"这些字段是否达标到可开写"，并把达标与否收敛成三态。
- `plan-feasibility-probe`：定义 FEAS-* 探针怎么做；本文件消费其"已探针验证"结论，未验证即 BLOCKED。
- `plan-devils-advocate-review`：定义反方批判怎么做；本文件只要求批判结论段存在。
- `minimum-plan-grading`：定义非 Plan Mode 如何分级；本文件要求分级后的最小计划也必须过 lite 档。
- `plan-question-coverage`：定义未决决策如何弹窗；本文件把未决命中为 BLOCKED，与 `WAITING_DECISION` 永久等待契约衔接。
