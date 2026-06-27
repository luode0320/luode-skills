# 验收标准边界说明

## 和相邻 skill 的边界

- 信息缺失：先转 `requirement-gap-rules`。
- 范围争议：先转 `requirement-boundary-rules`。
- 真正执行验证：转 `functional-validation-rules` 或 `test-regression-rules`。
- 最终放行结论：转 `final-acceptance-rules`。

## 使用提醒

- 验收标准负责“判定口径”，不是“执行动作”。
- 实施前若标准仍为空，通常说明需求阶段没有真正收口。
- 验收标准应单独沉淀到 `doc/验收/<需求文档同名主干>验收标准.md`，不与需求文档、实施文档或最终验收文档混写。
