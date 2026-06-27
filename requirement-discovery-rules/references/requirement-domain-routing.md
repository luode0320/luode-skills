# 需求域路由与合并判断

## 总顺序

需求域默认按以下顺序推进：

1. `requirement-discovery-rules`：老板式 idea 或资料不全时，先主动侦察资料、数据、代码、上下游和用户补充线索。
2. `requirement-intake-rules`：把已侦察到的事实、资料和方案收口成同一份需求主文档。
3. `requirement-gap-rules`：只处理侦察后仍无法补齐、且会影响实现方向的缺口。
4. `requirement-boundary-rules`：裁决当前需求、需求变更、历史问题、旧逻辑兼容和影响范围。
5. `requirement-splitting-rules`：当需求体量过大或跨多个子系统时，拆出可独立闭环的子项。
6. `requirement-change-rules`：当已澄清或已实现需求发生新增条件、优先级或交付物变化时，重算影响。
7. `acceptance-criteria-rules`：把稳定后的需求目标转成可验证、可测试、可复核的验收标准。
8. `implementation-plan-rules`：把当前优先闭环转成编码前计划、文件落点、阶段和验证点。

## 合并判断

当前不建议把需求域 skill 合并成一个大 skill。

原因：

- `discovery` 是资料侦察和证据收集，不负责正式需求文档落地。
- `intake` 是需求主文档入口，不负责长期主动找资料。
- `gap` 是缺口阻断，不应该覆盖可通过侦察解决的问题。
- `boundary` 是范围裁决，不能被接入或缺口规则顺手处理。
- `splitting` 是体量和闭环拆分，不是需求补全。
- `change` 是已进入流程后的变更重算，不是初始 idea 接入。
- `acceptance` 和 `implementation-plan` 是下游产物，不能提前吃掉前置不确定性。

## 允许吸收的重叠

- `requirement-intake-rules` 中“查项目上下文”的职责只保留轻量确认；深度侦察交给 `requirement-discovery-rules`。
- `requirement-gap-rules` 中“缺口识别”的职责只保留侦察后仍缺的内容；可主动查到的缺口先回流 discovery。
- `requirement-change-rules` 中“完善需求文档”的职责只处理已存在需求的变更；若新增内容其实是一个新 idea，回到 discovery。

## 跳转规则

- 用户只给 idea：先 discovery。
- 用户给了完整资料包：可直接 intake；如果资料互相矛盾或需要补查，先 discovery。
- 用户给了额外项目路径、URL、数据库或第三方服务线索：回到 discovery 扩展侦察。
- discovery 输出后仍缺关键业务取舍：提出最多 3 个拍板问题。
- discovery 输出后已能形成需求：转 intake。
- intake 文档中仍有关键事实缺失：先判断能否 discovery，不能再 gap。
- 需求稳定后才进入 acceptance 和 implementation-plan。
