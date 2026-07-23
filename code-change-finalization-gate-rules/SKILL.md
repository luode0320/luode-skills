---
name: code-change-finalization-gate-rules
description: 只要本轮存在代码新增/修改（含测试文件），最终回复前必须命中本 skill 作为默认收口闸门。负责校验注释双 skill（`comment-placement-granularity-rules` 与 `comment-completion-gate-rules`）终检、新增测试文件的当天时间戳目录一致性、补注释优先级闸门、`implementation-review-rules` 最低测试前收口、真实运行验证闸门、`internal/router` 提交前风格检查、用户手改保护（`code-context-resync-rules`）。若存在计划内未完成必需项或阻断级规则缺口，禁止给“已完成/已验证可用”结论；真实 `blocked/manual_handoff` 时只校验共享阻断契约，不生成面向用户的阻断区块或解决计划，用户可见渲染仍唯一由 `reasoning-summary-structure-rules` 完成。
---


# 代码变更最终收口闸门规则

只在“本轮存在代码或测试改动，且准备最终回复”时使用这个 skill。
目标不是重复实现业务，而是在收口前确认代码改动相关的专项终检已经真实执行。

本 skill 与 `skill-execution-compliance-gate-rules` 保持独立：本 skill 负责代码/测试改动专项闸门；通用 Skill 执行完整性、失败学习、执行证据和运行时状态真收口由后者负责。

## Skill 作用与适用场景

- 代码或测试新增/修改后，在最终回复前自动触发并核验专项收口。
- 注释链只消费 `comment-completion-gate-rules` 的 PASS/FAIL；该 PASS 必须包含其对 `comment-placement-granularity-rules` 的适用性处理证据，本入口不复制任何注释字段、编号或清单细则。
- 核验新增测试文件的当天时间戳目录一致性、补注释优先级、`implementation-review-rules` 最低测试前收口、真实运行验证状态、`internal/router` 风格和用户手改保护。
- Go 测试资产链只消费 `go-test-compile-path-rules`、`test-program-rules` 与 `test-strategy-rules` 的适用性结论和 PASS/FAIL；源码目录禁放、ASCII 镜像和 seam 细则由这些 Owner 唯一定义，本闸门不复制目录清单或扫描命令。
- 只产出专项闸门 PASS/FAIL 与证据；最终输出和后续内容统一由 `reasoning-summary-structure-rules` 渲染。

## 自动触发信号

- 本轮发生任意代码新增或修改（含测试文件），且准备最终回复。
- 本轮代码改动需要确认注释完成、实现自审、真实验证、测试落点、router 风格或用户手改保护是否漏检。

## 进入后先做什么

1. 涉及 Go 测试资产时，先核验 `go-test-compile-path-rules`、`test-program-rules` 与 test-asset-governance 的适用性结论和 PASS/FAIL；再检查新增测试文件是否全部位于同一个当天时间戳目录。
2. 核验 `comment-completion-gate-rules` 的 PASS/FAIL 和可追溯证据；FAIL 或无证据直接不通过，不在本入口重复字段级注释检查。
3. 补注释请求只核验 comment-completion 的优先范围结论，不复制函数头、方法块或补丁字段定义。
4. 核验 `implementation-review-rules` 已完成最低测试前收口。
5. 核验核心接口、页面、导出、查询、提交或任务入口的真实运行验证状态；仅有静态证据时必须降级。
6. 若出现用户手改与旧上下文冲突，核验 `code-context-resync-rules` 已执行且最终 diff 未回退用户内容。

## 默认执行流程

1. 确认本轮存在代码/测试改动并冻结最终 diff 范围。
2. 执行测试目录一致性检查；涉及 `internal/router` 时执行 router 专项检查。
3. 收集 comment-completion PASS/FAIL、implementation-review 结论、真实运行证据和用户手改保护证据。
4. 对真实运行证据不足的路径明确标记“仅静态验证”或“未完成真实验证”，并提供可执行的人工验证交接；不得宣称功能可用。
5. 形成专项闸门 PASS/FAIL；最终用户结构读取 `reasoning-summary-structure-rules`，本 skill 不生成独立后续或阻断模板。

## 提交前闸门检查（internal/router）

- 若本次改动包含 `internal/router`，必须检查：
- 不存在 `.GET(`、`.PUT(`、`.PATCH(`、`.DELETE(`。
- 不存在 `:id` 或 `{id}` 路径参数。
- 不存在 `registerPostRoutes` 或 route 列表驱动注册模式。
- 路由 path 未通过本地常量引用（允许全局根前缀常量）。
- 任一不满足则阻断交付，先回改再继续。

## 阻断判定与处理

属于阻断级：

- Go 测试资产适用但专职 Owner 未执行、为 FAIL 或缺少可追溯证据。
- 新增测试文件跨天或未统一落到同一个当天时间戳目录。
- `comment-completion-gate-rules` 为 FAIL、缺少结果或缺少其适用性联动证据。
- `implementation-review-rules` 最低测试前收口未完成。
- 核心运行路径没有真实验证，且未明确降级并提供人工验证交接。
- 仅有 build、lint、静态搜索、代码审查或实现自审，却宣称功能、接口已验证可用。
- 补注释优先范围未通过 comment-completion 闸门。
- 用户手改冲突未执行 `code-context-resync-rules`，或最终 diff 回退用户内容。

属于非阻断级：

- 缺口不影响当前结论正确性，且不属于原执行计划当前阶段必需项。
- 非阻断事实交给最终总结 owner 按条件决定是否展示。

## 权责边界与不负责事项

- 只负责代码/测试改动专项最终闸门，不代替业务实现、功能测试或通用 Skill 合规检查。
- 不复制注释字段细则，不代替 comment-completion、comment-placement 或用户手改保护 owner。
- 不把当前阶段不适用项误报为未执行缺口。
- 不拥有最终输出模板、后续内容或任务阻断渲染权。

## 执行通过 / 驳回标准

- 通过：测试目录、comment-completion PASS、implementation-review、真实运行验证状态、router 适用项和用户手改保护均按适用性完成并有证据。
- 驳回：任一阻断级专项缺口存在，却仍给出“可继续 / 已完成 / 已验证可用”结论。
- 驳回：本 skill 自行渲染后续内容、阻断区块、解决计划或等待类占位文案。

## references 读取规则

- 最终条件区块统一读取 `../reasoning-summary-structure-rules/references/conditional-sections-rules.md`。
- 不再维护本 skill 私有的 next-step 模板。

## 回到主流程的重启点

- FAIL 时回到对应专项 owner 补齐并重新执行本闸门。
- 达到停止边界仍无法补齐时，只提交结构化阻断事实给最终总结 owner。

## 输出要求（简化版）

- 只输出 `代码收口:PASS/FAIL`、验证降级状态和可核验证据。
- 最终总结结构、后续内容、阻断区块与无后续收口规则统一读取 `reasoning-summary-structure-rules`，本 skill 不复制。
