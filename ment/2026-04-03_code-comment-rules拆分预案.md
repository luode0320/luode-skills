# `code-comment-rules` 拆分预案（测试版样本）

更新时间：`2026-04-03 01:53`

## 1. 进入结论

- 目标旧 skill：`code-comment-rules`
- 关联既有 skill：`chinese-comment-rules`
- 当前结论：`进入拆分`
- 当前状态：`deleted-ready`
- 说明：
  - 本文已从“拆分预案”升级为“可执行的测试版拆分样本”。
  - `comment-placement-granularity-rules` 与 `comment-completion-gate-rules` 已创建完成。
  - 旧 `code-comment-rules` 已作为冻结对照基线完成首轮对照验证，并准备在删除后继续执行冒烟验证。
  - 详细测试证据统一沉淀在 `test/2026-04-03_012320/` 下。

## 2. 测试版样本目标

本样本不是单纯的分析文档，而是首个 `code-comment-rules` 实战拆分时可直接执行的测试版样本。判断“拆分完成”的标准，不是新目录建好了，而是以下条件同时成立：

1. 旧 `code-comment-rules` 的任何规则都没有丢失、弱化或变成承接空洞。
2. 新 skill 集合在真实提问中仍能自动触发，不能写出来却命不中。
3. 相邻 skill 的边界仍清晰，没有明显误命中、漏命中或职责漂移。
4. 删除前承接检查、外部入口迁移和对照记录全部完成。

阻断口径：

- 只要发现一条旧规则没有落点，就直接阻断删除。
- 只要发现自动触发不稳定、必须依赖额外口头提醒才能命中，也直接判定拆分未完成。

## 3. 为什么判断应进入拆分

按 `skill-split-preserve-rules/references/entry-and-splitting.md` 的进入门槛，`code-comment-rules` 已同时满足“功能性变化 + 原边界难以自然承接新增规则”的前提，并额外命中多个结构信号：

1. 同一 skill 已出现多个可独立命中的并列职责组。
2. `description` 已同时覆盖“注释必要性、位置、颗粒度、字段注释、函数头元信息、步骤编号、改动位点闸门、过期注释治理”等多个触发对象。
3. 正文已膨胀到 100+ 行，新增规则只能继续堆进同一 skill，边界越来越难解释。
4. 若继续留在原 skill，会继续削弱“不要用它代替中文语言表达规则”的边界声明，因为正文内部仍保留了完整的中文注释语言规则。

## 4. 为什么 `chinese-comment-rules` 暂不拆

`chinese-comment-rules` 当前仍围绕单一触发对象运转，主要处理“注释语言是否必须中文、哪些术语保留原文、中文表达该怎么写”这一个稳定职责组。

它暂时不满足继续拆分的结构信号：

- 触发对象单一，仍是“注释语言表达”。
- 正文体量可控，没有明显过载。
- 权责边界相对清晰，问题主要是与 `code-comment-rules` 存在重复覆盖，而不是自身内部再混了多个独立类别。

因此当前更合理的动作不是拆 `chinese-comment-rules`，而是：

1. 把 `code-comment-rules` 中“强制中文表达”的规则收回给 `chinese-comment-rules` 主承接。
2. 收紧两个 skill 的互相引用关系，避免再次双向重叠。

## 5. 可识别的并列职责组

当前至少可以识别出以下三组并列职责：

### 5.1 注释结构与颗粒度组

负责：

- 判断注释是否必要
- 注释放在哪里
- 注释写多细
- 字段定义、初始化和使用位点如何补注释
- 过期注释、错位注释、误导性注释如何治理

这组的处理对象是“注释结构设计”。

### 5.2 注释补齐闸门组

负责：

- 改动位点必须补齐哪些注释
- 补注释时为什么优先处理未提交改动
- 函数头 `[参数]` / `[返回]` / `最近修改时间` 顺序与必填要求
- 方法体 `1.` `2.` `3.` 步骤编号及其就近落位规则
- 哪些缺失直接判定不通过、不得进入收口或提交

这组的处理对象是“改动位点补齐与阻断闸门”。

### 5.3 注释语言表达组

负责：

- 注释必须中文
- 协议字段和第三方固定原文何时保留原文
- 中文表达如何避免翻译腔、空话和机翻痕迹

这组的处理对象是“注释语言表达”，应由既有 `chinese-comment-rules` 主承接。

## 6. 首轮二分方案

按 `skill-split-preserve-rules` 的二分要求，首轮不继续细碎拆分，而是先做一次稳定二分：

### 6.1 新 skill A：`comment-placement-granularity-rules`

建议 `description`：

当需要判断代码注释是否有必要、应放在哪里、写到什么颗粒度，以及字段注释、边界注释和过期注释如何治理时触发。负责统一注释位置、颗粒度、字段相关注释和过期注释治理；不要用它代替注释语言表达、改动位点补齐闸门或 Swagger/OpenAPI 注解规则。

命名理由：

- 名称直接由 `description` 反推。
- 主触发对象是 `placement + granularity`，不是旧 skill 名称前缀的机械延续。

### 6.2 新 skill B：`comment-completion-gate-rules`

建议 `description`：

当本轮代码新增或修改，或用户请求补充注释、只补注释、注释完善，需要核验改动位点注释是否补齐时触发。负责统一补注释优先范围、函数头元信息、方法块步骤编号和注释缺失阻断闸门；不要用它代替注释语言表达、一般性的注释位置判断或 Swagger/OpenAPI 注解规则。

命名理由：

- 名称由“改动位点补齐 + 阻断闸门”这一主职责直接反推。
- 能和“位置/颗粒度”职责稳定区分。

### 6.3 既有承接 skill：`chinese-comment-rules`

本轮不新建第三个语言 skill，直接让既有 `chinese-comment-rules` 主承接以下内容：

- 中文注释强制规则
- 第三方固定原文的例外边界
- 中文表达方式与禁忌

## 7. 首轮覆盖映射草案

说明：

- 当前是测试版样本中的首轮草案，已按“最小可迁移规则组”完成第一版原子化。
- 若正式进入实现，再继续细化到更小的规则 ID。
- 该映射表本身也是第 1 轮测试的核心输入，不是只读附件。

| 原规则ID | 原规则摘要 | 特例标记 | 新 skill 名称 | 新规则落点 | 迁移动作 | 状态 | 主落点 | 等价性说明 | 组合覆盖说明 |
|---|---|---|---|---|---|---|---|---|---|
| R-CC-001 | 判断注释是否必要，避免无效注释泛滥 | 否 | `comment-placement-granularity-rules` | 新 `SKILL.md / Skill 作用与适用场景` | 原样迁移 | 测试版草案 | `comment-placement-granularity-rules` | 无 | 无 |
| R-CC-002 | 规范块注释、边界注释、风险注释和字段注释的放置方式 | 否 | `comment-placement-granularity-rules` | 新 `SKILL.md / Skill 作用与适用场景`、`references/comment-placement.md` | 等价改写 | 测试版草案 | `comment-placement-granularity-rules` | 从旧 skill 总述拆到位置类规则 | 无 |
| R-CC-003 | 控制注释颗粒度，避免逐行复述代码 | 否 | `comment-placement-granularity-rules` | 新 `references/comment-granularity.md` | 原样迁移 | 测试版草案 | `comment-placement-granularity-rules` | 无 | 无 |
| R-CC-004 | 治理过期注释、错位注释和误导性注释 | 否 | `comment-placement-granularity-rules` | 新 `SKILL.md / 权责边界与不负责事项` + `references/comment-examples.md` | 等价改写 | 测试版草案 | `comment-placement-granularity-rules` | 位置治理与示例对照拆开表达 | 无 |
| R-CC-005 | 补注释请求优先处理未提交改动位点 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：补注释优先范围` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-006 | 未提交改动中若存在函数、方法改动，必须优先补函数头注释与方法块注释 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：补注释优先范围` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-007 | 所有改动位点必须补齐注释，缺失则不得进入通过/可提交结论 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制门禁：改动位点注释补齐` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-008 | 方法体存在 2 个及以上连续步骤时，必须补顶层 `1.` `2.` `3.` 编号，必要时可用 `1.1` 等细分 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：步骤编号` | 等价改写 | 测试版草案 | `comment-completion-gate-rules` | 合并“步骤注释位置”与“分层编号”两组规则统一表述 | 无 |
| R-CC-009 | 编号步骤注释必须就近落位，不得集中写在函数开头，也不得用普通流程注释替代 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：步骤编号` | 等价改写 | 测试版草案 | `comment-completion-gate-rules` | 旧 skill 的两组相邻规则合并为同一约束组 | 无 |
| R-CC-010 | 函数、方法必须补 `[参数]` / `[返回]` / `最近修改时间`，且顺序固定 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：函数头元信息` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-011 | 最近修改时间必须包含本次改动原因，且最后一行写入 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 强制规则：函数头元信息` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-012 | 注释必须中文，协议字段和第三方固定原文可保留原文 | 否 | `chinese-comment-rules` | 既有 `SKILL.md / 强制规则：注释语言` | 原样迁移 | 测试版草案 | `chinese-comment-rules` | 当前由相邻既有 skill 主承接 | 无 |
| R-CC-013 | 用户请求补注释时，也不能跳过方法体步骤编号检查 | 否 | `comment-completion-gate-rules` | 新 `SKILL.md / 默认执行流程`、`执行通过 / 驳回标准` | 原样迁移 | 测试版草案 | `comment-completion-gate-rules` | 无 | 无 |
| R-CC-014 | 若主要争议是中文表达，应转交 `chinese-comment-rules`；若是 Swagger 注解，应转交 `api-swagger-rules` | 否 | `comment-placement-granularity-rules`、`comment-completion-gate-rules`、`chinese-comment-rules` | 各自 `SKILL.md / 权责边界与不负责事项` | 组合覆盖 | 测试版草案 | `comment-placement-granularity-rules` | 拆分后每个 skill 都需重写边界声明 | 语言边界由 `chinese-comment-rules` 主承接，Swagger 边界由两个新 skill 同步声明 |
| R-CC-015 | 默认读取 `comment-placement` / `comment-granularity` / `comment-examples` 三类 references | 否 | `comment-placement-granularity-rules`、`comment-completion-gate-rules` | 新 skill 的 `references 读取规则` | 增强补充 | 测试版草案 | `comment-placement-granularity-rules` | 旧 references 需重新分配给两个新 skill | 新 gate skill 需要新增“步骤编号与函数头元信息”相关 references |

## 8. 多轮多模式测试设计

### 8.1 测试总原则

- 本样本默认至少执行 4 轮测试，且每轮测试模式不同。
- 每轮都要同时记录“旧 skill 预期结论”和“新 skill 集合预期结论”，避免只看新 skill 自说自话。
- 旧 `code-comment-rules` 在本阶段只是冻结对照基线，不再继续吸收新规则。
- 任一轮发现旧规则丢失、承接弱化、自动触发失效或边界漂移，都直接阻断删除。
- 不允许跳过失败轮次，直接用后续轮次覆盖前面的失败结论。

### 8.2 第 1 轮：静态覆盖对照

目的：

- 验证旧 `code-comment-rules` 的规则、特例和 references 是否都能在新 skill 集合中找到明确落点。

执行步骤：

1. 以本文件第 7 节映射表为基础，逐条检查原规则 ID 是否有主落点。
2. 对每条“组合覆盖”的规则，补齐主落点、次落点和组合后等价性说明。
3. 检查旧 skill 中所有强约束语句是否仍保留原强度，不得弱化成模糊建议。
4. 检查 `references/` 是否完成重分配，不能只迁正文不迁引用资源。

通过标准：

1. 原规则映射覆盖率必须达到 100%。
2. 不存在“无落点”“只剩口头说明”“落点不唯一且解释不清”的规则。
3. 不存在把旧“必须 / 不得 / 阻断”弱化成“建议 / 可选”的情况。

### 8.3 第 2 轮：自动触发与路由验证

目的：

- 验证新 skill 是否真的能按 `description` 自动命中，并且没有把边界漂移到相邻 skill。

测试样本：

| 测试ID | 输入样本 | 旧 skill 预期命中 | 新 skill 集合预期命中 | 不应命中 / 路由要求 |
|---|---|---|---|---|
| T2-01 | 这个注释该不该写，应该放在哪一段代码上方？ | `code-comment-rules` | `comment-placement-granularity-rules` | 不应主命中 `comment-completion-gate-rules` |
| T2-02 | 这个方法补注释时，`[参数]`、`[返回]`、最近修改时间怎么补？ | `code-comment-rules` | `comment-completion-gate-rules` | 不应主命中 `comment-placement-granularity-rules` |
| T2-03 | 这个方法已经写了“查询订单/更新状态”两个普通注释，要不要改成 `1.` `2.` 编号？ | `code-comment-rules` | `comment-completion-gate-rules` | 不能只回答一般注释写法 |
| T2-04 | 这个英文错误注释要不要保留原文，中文解释怎么写？ | `code-comment-rules` | `chinese-comment-rules` | 两个新 comment skill 不应抢语言主职责 |
| T2-05 | Swagger 接口注释怎么写？ | `code-comment-rules` 可能历史上误吸收 | `api-swagger-rules` | 两个新 comment skill 与 `chinese-comment-rules` 都不应主命中 |
| T2-06 | 这个新改的方法既要补函数头注释，也想判断缓存失效分支要不要加风险注释。 | `code-comment-rules` | `comment-completion-gate-rules` + `comment-placement-granularity-rules` | 若涉及中文措辞，再追加 `chinese-comment-rules` |

通过标准：

1. 每个新 skill 都至少有稳定的“应命中”样本。
2. 相邻 skill 至少有一组“不得误命中”样本。
3. 不出现“新 skill 写出来了，但没有任何真实提问能稳定命中”的空壳状态。

### 8.4 第 3 轮：组合场景与多 skill 协同验证

目的：

- 验证拆分后是否仍能覆盖真实复合型提问，而不是只适合单句、单一职责的样例。

建议场景：

1. 补注释请求 + 结构判断：
   输入样本：`这个 Go 方法刚改过，请优先看未提交改动，补 [参数] / [返回] / 最近修改时间，并判断重试分支是否需要步骤注释。`
   预期：`comment-completion-gate-rules` 主命中，`comment-placement-granularity-rules` 次命中。
2. 补注释请求 + 中文表达边界：
   输入样本：`这个方法要补注释，第三方返回的 fixed error message 要不要保留原文，中文怎么写更自然？`
   预期：`comment-completion-gate-rules` + `chinese-comment-rules`。
3. 位置判断 + 语言边界：
   输入样本：`这个结构体字段注释该写在字段上方还是行尾？里面的 HTTP header 名称要不要翻译成中文？`
   预期：`comment-placement-granularity-rules` + `chinese-comment-rules`。

通过标准：

1. 复合型问题不需要依赖旧 `code-comment-rules` 才能得到完整承接。
2. 新 skill 的组合数量仍可解释，不能把一个常见问题拆成过多 skill 才能回答。
3. 每个组合场景都能明确谁是主承接 skill，避免互相抢答。

### 8.5 第 4 轮：真实代码改动演练

目的：

- 在真实或拟真代码改动样本上验证新 skill 集合是否能完整承接旧 skill 的能力。

建议演练内容：

1. 准备一个真实改动样本，至少同时包含：
   - 一个缺少函数头元信息的方法
   - 一个需要 `1.` `2.` 编号的连续步骤方法体
   - 一个需要判断是否应补风险注释的分支
   - 一处涉及英文固定原文是否保留的注释
2. 用冻结的旧 `code-comment-rules` 得出基线结论。
3. 用新 skill 集合重新跑一轮，逐项比对：
   - 是否有旧规则未被承接
   - 是否有回答力度变弱
   - 是否有自动触发漏命中
   - 是否有边界被错误分配给相邻 skill

通过标准：

1. 旧 skill 能给出的关键结论，新 skill 集合也都能给出。
2. 新 skill 集合没有出现“回答更碎，但反而漏了规则”的情况。
3. 若本轮失败，必须回到拆分设计或 `description` 调整阶段，不得进入删除评估。

## 9. 测试记录模板

执行每一轮测试时，至少记录以下字段：

```md
### 测试轮次：第 X 轮

- 测试模式：
- 测试目标：
- 输入样本：
- 旧 skill 预期结论：
- 新 skill 集合预期结论：
- 实际命中 skill：
- 实际结论：
- 是否发现旧规则丢失：
- 是否发现自动触发失效：
- 是否发现边界漂移：
- 是否通过：
- 发现的问题：
- 回到哪一步修正：
```

补充要求：

1. 每轮测试都必须单独记录，不得只写总评。
2. 若是首个实战拆分样本，必须保留“旧 skill vs 新 skill 集合”的对照结论。
3. 测试未完成前，不得把“拆分完成”写成结论。

## 10. 对外命中链路的影响

如果正式拆分，下面这些现有 skill 或入口也要同步迁移，不然会继续误命中旧边界：

- `skill-hit-check-rules`
- `skill-compliance-gate-rules`
- `implementation-review-rules`
- `code-readability-rules`
- `code-minimal-change-rules`
- `team-development-rules`
- `编码skill.md`
- `README.md`
- `字典.md`
- `skill-dictionary/data.js`

## 11. 可能的第二轮拆分条件

首轮完成后，如果 `comment-completion-gate-rules` 仍然持续过载，再考虑第二轮递归拆分：

1. `comment-method-metadata-rules`
负责 `[参数]` / `[返回]` / `最近修改时间` / 改动原因。
2. `comment-step-numbering-gate-rules`
负责 `1.` `2.` `3.` 步骤编号、就近落位、普通流程注释替代拦截和不通过闸门。

只有在首轮落地后仍明显过载时，才进入第二轮，不在本轮样本里提前细碎拆分。

## 12. 删除前承接检查草案

删除前承接检查：

- 旧 skill：`code-comment-rules`
- 当前状态：`testing-ready`
- 主承接新 skill：`comment-placement-granularity-rules`
- 次承接新 skill：`comment-completion-gate-rules`
- 并列承接既有 skill：`chinese-comment-rules`
- 删除前临时保留：旧 skill 冻结版本、覆盖映射表、多轮测试记录、对外入口迁移清单

删除前测试材料：

1. 第 7 节覆盖映射表的最终版。
2. 第 8 节 4 轮测试的完整记录。
3. “旧 skill vs 新 skill 集合”的对照结论。
4. 相邻 skill 路由验证样本与误命中说明。
5. 外部入口迁移清单完成记录。

删除前检查闸门：

1. 映射表必须证明旧规则 100% 已承接。
2. 多轮多模式测试必须全部通过，不能只过其中一轮。
3. 必须明确证明不存在旧规则丢失、弱化或承接空洞。
4. 必须明确证明新 skill 可以自动触发，且边界没有明显漂移。
5. `skill-hit-check-rules` 与 `skill-compliance-gate-rules` 已切到新入口。
6. `implementation-review-rules` 等外部依赖入口已完成迁移。
7. `chinese-comment-rules` 已补齐语言承接规则。
8. 删除后不再依赖旧 `code-comment-rules` 作为主入口。

删除动作：

1. 先冻结最终对照记录，再删除旧 `code-comment-rules` 目录。
2. 同步删除旧 skill 在命中清单、字典索引和提示文案中的主入口位置。
3. 若任一测试闸门未通过，则旧 skill 保持临时保留状态，并回到拆分设计或测试补齐阶段。

## 13. 当前建议

1. 下一步先按本样本创建 `comment-placement-granularity-rules` 和 `comment-completion-gate-rules`，不要先删旧 skill。
2. 新 skill 创建后，按第 8 节顺序执行 4 轮测试，并把测试记录补齐后再评估删除。
3. 首轮只拆 `code-comment-rules`，不要同步拆 `chinese-comment-rules`。
4. 若测试显示“命中边界仍混乱”或“一个常见问题必须同时命中过多 skill”，则回到拆分设计阶段重新收敛职责分组。
