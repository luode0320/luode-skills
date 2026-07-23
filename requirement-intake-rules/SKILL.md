---
name: requirement-intake-rules
description: 当用户提出新需求、新功能、新页面、新接口、新模块，且任务刚进入研发阶段、尚未进入实现或 Bug 定位时触发；它是新需求接入唯一自动触发入口和唯一需求主文档 Owner。对一句话 idea、老板式方向、粗略想法，或资料不足但可通过项目、代码、schema、上下游、URL、GitHub、网站、官方资料主动查证的场景，进入 `initial-discovery` 条件路由；对侦察后仍无法补齐、存在多个合理解释，且会影响实现方向的关键缺口进入 `gap-routing`；对已整理资料直接做需求接入。保留“需求信息不全、缺少字段/流程/规则/成功标准/关键前提”等 gap aliases。范围、兼容或旧逻辑归属不清时由 `requirement-boundary-rules` 专项自动触发；需求过大、多模块、多页面、多接口、多角色或多独立子系统时由 `requirement-splitting-rules` 专项自动触发；已确认需求在编码中新增条件、修改默认值、优先级、范围或交付物时由 `requirement-change-rules` 专项自动触发。四个 Owner 均保持自动触发，本 Skill 不吞并专项信号。
---

# 需求接入规则

## 职责

- 只负责新需求接入、需求资料整理和唯一需求主文档维护。
- 同一需求只维护一份主文档；`initial-discovery`、`gap-routing`、边界、拆分和变更结论都回写该文档，不创建竞争入口。
- 正式需求主文档未真实落盘、关键条件路由未收敛、前置验收未建立或实施规划未完成时，不得进入正式编码。
- 需求域路由、共享保护语义和下游移交统一执行 `references/requirement-domain-shared-contract.md`；根文件减重不代表任何规则、别名、local、安全、授权、暂停、停止或回滚语义失效。

## 自动触发与条件路由

1. **直接接入**：需求资料已经足以说明目标、范围、输入输出、约束和成功标准时，直接整理并更新唯一需求主文档。
2. **`initial-discovery`**：一句话 idea、粗略方向、资料可由项目事实、代码、schema、上下游、URL、GitHub、网站或官方文档主动查证时，先侦察再追问。
3. **`gap-routing`**：主动侦察后仍缺少字段、流程、规则、关键前提或成功标准，存在多个合理解释且继续推进会改变方向时，一次只推进一个真实关键缺口。
4. **专项自动触发**：
   - 范围、兼容、上下游或旧逻辑归属不清：`requirement-boundary-rules`。
   - 多模块、多页面、多接口、多角色、多独立子系统或无法形成单一闭环：`requirement-splitting-rules`。
   - 已确认需求新增条件、改变默认值、优先级、范围或交付物：`requirement-change-rules`。
5. **邻域排除**：原实现不符合原需求时进入 Bug 域；实施前定义“做到什么算完成”时进入 `acceptance-criteria-rules`；Plan Mode 或编码前实施拆解进入 `implementation-planning-rules`。

## 最小执行流程

1. 读取 `references/requirement-domain-shared-contract.md`，确认当前 Owner、route 和禁止抢占的邻域。
2. 读取 `references/intake-checklist.md`，结合当前项目和真实资料完成接入。
3. 需要主动侦察时执行 `references/initial-discovery-route.md` 及其条件 references；所有连接只允许使用 local 配置，禁止回退到 test、staging、pre、release、prod/production。
4. 侦察后仍有方向级缺口时执行 `references/gap-routing.md`；禁止 Agent 猜测，缺口关闭后回填主文档并删除临时缺口文档。
5. 需求过大、边界不清或已发生变更时，移交对应专项 Skill；专项 Skill 结论仍回写同一份主文档。
6. 需求稳定后先移交 `acceptance-criteria-rules`，再由 `implementation-planning-rules` 形成实施总览、周期、文件/符号落点和真实测试闭环。
7. 最终落盘、图片、路径和文档存在性由 `artifact-storage-rules` 与 `artifact-delivery-gate-rules` 核验；未落盘不得以最终回复代替。

## 保护闸门

- 一次只推进一个真实关键问题；能主动查证的先查证，不能查证的再提问。
- 不得把 Agent 猜测、未授权默认值或多个合理方向中的任一项写成已确认结论。
- P0/P1 未决、无授权默认值、权限/兼容/数据/异常边界不明时状态为 `blocked`；P2 默认值必须记录授权人、有效期和复核证据。
- 用户明确暂停、停止或不继续时立即停止需求扩散；恢复时从已落盘状态和未关闭 route 继续。
- 需求变化、缺口关闭或路线回退必须保留差异、来源、回滚和关闭证据；不得覆盖历史事实后声称已验证。
- 图片、Mermaid、结构、稳定 ID、`N/A + 原因 + 证据`、追踪字段和普通语言正文规则不得在根文件重复定义，必须执行其唯一 Owner reference。

## References

- 需求域路由、单一主文档、共享保护语义和下游移交：`references/requirement-domain-shared-contract.md`
- 接入检查：`references/intake-checklist.md`
- 接入边界和正反例：`references/intake-boundaries-and-examples.md`
- 极致完整性、稳定 ID、N/A 和追踪：`references/extreme-completeness-standard.md`
- 需求结构与占位模板：`references/requirement-structure-template.md`
- 主动侦察：`references/initial-discovery-route.md`
- 侦察清单：`references/initial-discovery-checklist.md`
- 侦察证据和记忆：`references/initial-discovery-evidence-and-memory.md`
- 侦察输出：`references/initial-discovery-output-template.md`
- 关键缺口：`references/gap-routing.md`
- 缺口清单：`references/missing-info-checklist.md`
- 暂停条件：`references/pause-triggers.md`
- 缺口正反例：`references/requirement-gap-examples.md`
- 文档路径和图片根目录：`../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/update-policy.md`
- 普通语言和最终门禁：`../artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`
