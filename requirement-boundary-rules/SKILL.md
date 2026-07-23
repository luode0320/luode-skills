---
name: requirement-boundary-rules
description: 当需求边界不清、影响范围不明、兼容性不明确、是否允许改旧逻辑不清楚，或需要区分当前需求、历史问题、需求变更和验收偏差时专项自动触发。负责范围、归属、兼容性和上下游影响裁决，并将结论回写到 `requirement-intake-rules` 维护、由 `artifact-storage-rules` 定位的同一份需求主文档；信息缺失转 `requirement-intake-rules#gap-routing`，历史缺陷转 Bug 域，不代替需求接入、拆分、变更、验收或实施规划。
---

# 需求边界判定规则

## 职责与触发

- 只负责判断“是否属于本次需求、是否允许修改旧逻辑、影响哪些上下游、采用什么兼容边界”。
- 用户提出“顺手改旧逻辑”、当前需求暴露历史问题、验收偏差归因不清、旧接口/页面/流程可能受影响时自动触发。
- 边界结论必须唯一归属为：当前需求、明确排除项、独立变更、Bug 或历史问题；不得重复归属或留空。
- `BOUND-*` 字段、证据、权限、兼容、数据影响、回滚和验收回指只由 `references/boundary-checklist.md` 定义，根文件不复制细则。

## 路由

- 资料、字段、流程、规则或关键前提缺失：转 `requirement-intake-rules#gap-routing`；能主动查证时先走 `initial-discovery`。
- 原实现不符合原需求、脱离当前需求仍客观存在：转 Bug 域。
- 已确认需求新增条件、改变范围、默认值、优先级或交付物：转 `requirement-change-rules`。
- 边界稳定但需求体量过大：转 `requirement-splitting-rules`。
- 边界稳定后才允许进入 `acceptance-criteria-rules`，随后进入 `implementation-planning-rules`。

## 最小执行流程

1. 读取 `../requirement-intake-rules/references/requirement-domain-shared-contract.md`，确认唯一主文档和 Owner 边界。
2. 读取 `references/boundary-checklist.md`，冻结 In Scope、Out of Scope、允许/禁止修改层、上下游、权限、兼容和数据影响。
3. 历史问题与变更难以区分时读取 `references/history-vs-change.md`；验收偏差归因时读取 `references/acceptance-routing-examples.md`。
4. 将边界、排除项、兼容影响和流转结论回写同一份需求主文档；路径、图片和更新策略由 `artifact-storage-rules` 负责。
5. 边界变化影响正文、矩阵、Mermaid、拆分、验收或实施计划时，声明受影响项并移交对应 Owner 更新；最终落盘由 `artifact-delivery-gate-rules` 核验。

## 暂停、通过与驳回

- 暂停：当前问题既像需求变更又像历史缺陷；兼容调整会显著扩大范围；多个历史问题是否并入未获确认；验收失败无法归因。
- 暂停期间保持 `blocked`，不得进入前置验收、实施规划或编码；未授权兼容、权限、数据迁移和回滚方案不得写成确定结论。
- 通过：范围、排除项、归属、兼容和上下游影响清晰，结论已回写同一主文档并保留证据与回滚路径。
- 驳回：历史问题与当前需求混做、需求偏差直接误判为 Bug、边界未稳定即进入下游，或只改文字未声明受影响图表和下游结论。
- 用户明确暂停、停止或不继续时立即停止扩散；恢复时从已落盘的 `BOUND-*` 状态继续。

## References

- 共享路由与保护语义：`../requirement-intake-rules/references/requirement-domain-shared-contract.md`
- 边界字段与 `BOUND-*`：`references/boundary-checklist.md`
- 历史问题与需求变更：`references/history-vs-change.md`
- 验收偏差路由样例：`references/acceptance-routing-examples.md`
- 文档路径和同文档更新：`../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/update-policy.md`
- 普通语言与落盘门禁：`../artifact-delivery-gate-rules/references/plain-language-document-contract.md`、`../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`
