# 需求域路由与合并判断

## 对外心智模型

对外统一使用“需求接入前半段 + 条件闸门 + 下游移交”：

- 需求域主流程：`Idea / Discovery -> Intake`
- 条件步骤：`Gap / Boundary / Splitting / Change`
- 下游移交：`Acceptance Criteria -> Implementation -> Test -> Review -> Final Acceptance`

其中：

- `discovery` 负责主动侦察和找资料。
- `intake` 负责把 discovery 结果接成唯一主需求文档。
- `acceptance criteria` 和 `implementation` 已不再属于需求域主流程；需求稳定后由需求域移交到验收域与实施域。
- `gap / boundary / splitting / change` 都是按条件插入的闸门，不是每次都默认完整走一遍的长链路。

## 内部默认顺序

需求域内部只承接到“需求稳定前”为止：

1. `requirement-discovery-rules`：老板式 idea 或资料不全时，先主动侦察资料、数据、代码、上下游、关联项目、GitHub、相关网站和官方 API 文档。
2. `requirement-intake-rules`：discovery 形成初稿后，立即把已侦察到的事实、资料和方案收口成同一份需求主文档。
3. `requirement-gap-rules`：只处理侦察后仍无法补齐、且会影响实现方向的缺口。
4. `requirement-boundary-rules`：在范围、兼容、历史问题归属不清时裁决当前需求与影响范围。
5. `requirement-splitting-rules`：在需求体量过大或跨多个子系统时，拆出可独立闭环的子项。
6. `requirement-change-rules`：当已澄清或已实现需求发生新增条件、优先级或交付物变化时，重算影响。
7. 当 gap / boundary / splitting / change 已收敛后，需求域结束并向下游移交。

## 下游移交顺序

需求域完成后，按以下顺序移交到后续大类：

1. `acceptance-criteria-rules`：把稳定后的需求目标转成可验证、可测试、可复核的前置验收标准。
2. `implementation-planning-rules`：把当前优先闭环转成编码前实施总览、实施周期、文件落点和验证点。
3. 用户明确“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现”，且已有执行计划、完成定义、停止条件和最大推进边界后，才允许从实施文档切入正式编码；缺少计划或停止边界时，只能先补受限计划并停在计划收口处。
4. 测试域：按实施周期执行功能验证、回归验证和测试收口。
5. 审核域：按实施周期完成实现审查和当前改动审查。
6. `final-acceptance-rules`：在测试和审核完成后做最终放行。

## 合并判断

当前不建议把需求域 skill 合并成一个大 skill。

原因：

- `discovery` 是资料侦察和证据收集，不负责正式需求文档的长期维护。
- `intake` 是需求主文档入口，不负责长期主动找资料。
- `gap` 是缺口阻断，不应该覆盖可通过侦察解决的问题。
- `boundary` 是范围裁决，不能被接入或缺口规则顺手处理。
- `splitting` 是体量和闭环拆分，不是需求补全。
- `change` 是已进入流程后的变更重算，不是初始 idea 接入。
- `acceptance criteria`、`implementation` 和 `final acceptance` 都是下游产物，不能提前吃掉前置不确定性。

## 允许吸收的重叠

- `requirement-intake-rules` 中“查项目上下文”的职责只保留轻量确认；深度侦察交给 `requirement-discovery-rules`。
- `requirement-gap-rules` 中“缺口识别”的职责只保留侦察后仍缺的内容；可主动查到的缺口先回流 discovery。
- `requirement-change-rules` 中“完善需求文档”的职责只处理已存在需求的变更；若新增内容其实是一个新 idea，回到 discovery。

## 跳转规则

- 用户只给 idea：先 discovery。
- 用户给了完整资料包：可直接 intake；如果资料互相矛盾或需要补查，先 discovery。
- 用户给了额外项目路径、URL、数据库、GitHub 仓库、第三方服务线索或 API 文档入口：回到 discovery 扩展侦察。
- discovery 输出后立即创建主需求文档，再继续按需进入 gap / boundary / splitting / change。
- discovery 输出后仍缺关键业务取舍：提出最多 3 个拍板问题。
- discovery 输出后已能形成需求：转 intake。
- intake 文档中仍有关键事实缺失：先判断能否 discovery，不能再 gap。
- gap 未关闭、boundary 未裁清、splitting 未完成或 change 未重算时，阻断进入 `acceptance-criteria-rules` 与 `implementation-planning-rules`。
- 需求稳定后才移交前置验收标准与实施域；实施文档确认后，仍必须等待用户明确“开始实施 / 开始实现 / 开始执行 / 直接做 / 继续做完 / 按文档实现”，并确认执行计划、完成定义、停止条件和最大推进边界齐备，才能进入正式编码。
- 一旦用户已明确开始实施，且计划与停止边界齐备，后续应按实施周期自动串行推进“实现 -> 测试 -> 审核 -> 周期收口 -> 下一周期”，而不是每步重新向用户要指令。
