# 测试资产治理条件路由

> 归属 owner：`test-strategy-rules`。本文件合并原测试文档、测试命名、测试资产防散落和测试任务根布局四条规则；仅作为条件路由细则，不产生独立自动触发入口。所有原有触发语义、用户习惯、目录约定、本地环境红线、停止边界和 artifact gate 要求均保留。

## 迁移保留规则：test-strategy-rules 的 test-asset-governance 条件路由

# 测试文档规则

只在“测试说明文档应该怎么写、怎么组织、怎么留痕”这个问题上使用这个 skill。
如果当前争议是测试程序怎么写，请转交 `test-program-rules`；如果是功能到底算不算通过，请转交 `functional-validation-rules`；如果是旧能力有没有被带坏，请转交 `test-regression-rules`。

**重要：本 skill 必须服从 `test-strategy-rules 的 test-asset-governance 条件路由`。中文说明目录只允许存放 `README.md`；如果需要详细说明、案例表、补充报告、截图说明或执行清单，这些文档必须放到同一时间戳根目录下的 ASCII 真实代码路径镜像目录中。**

## 测试隔离红线（强制）

- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 测试文档中若出现“为测试方便新增生产字段/方法”的做法，必须标记为违规并阻断，不得作为可接受方案沉淀。
- 测试说明只记录测试资产与结论，不为生产代码污染行为背书。
- 测试文档若记录执行环境，必须明确本轮自动化属于本地测试，连接信息来自 `local` 环境；不得把 `test` 环境配置、`test` 数据库连接或“修改 test 配置后执行”写成默认测试步骤。

## Skill 作用与适用场景

- 作为测试资源管理链的第四道规则，统一测试文档入口、章节和归档方式。
- 约束测试 README、验证说明、测试报告、覆盖说明和执行记录的最小结构。
- 保证接手人可以先从中文 README 快速理解测试，再按 README 指向找到真实测试代码与证据。
- 防止把测试文档继续散落到 `testing/`、`analysis/`、仓库根目录或中文说明目录之外的随意位置。
- 防止中文说明目录被堆满额外 markdown、截图和报告，重新退化成杂物目录。

## 自动触发信号

- 新增或修改测试 `README.md`、验证说明、测试报告、覆盖说明、测试执行记录。
- 需要给当前测试任务补写执行方法、依赖条件、覆盖范围和验证结论。
- 发现测试已经执行，但没有留下结构化说明和结论。
- 发现有人准备把测试文档写到 `testing/`、`analysis/`、仓库根目录、业务代码目录或中文说明目录之外的任意位置。
- 发现中文说明目录中开始出现多个 `.md`、截图或附件，违反“仅 README”基线。

## 进入后先做什么

1. 先确认测试目录已经遵循 `test-strategy-rules 的 test-asset-governance 条件路由`，即存在独立的中央约定时间戳根目录。
2. 确认中央约定的测试任务主说明 `README.md` 作为当前任务唯一的中文主说明入口。
3. 区分当前文档属于主 README、详细验证说明、覆盖补充、执行记录还是报告摘要。
4. 如果需要额外 markdown、图片说明或附件，先确定它们对应的真实代码路径镜像目录，再放入 ASCII 路径中。
5. 确认 README 是否已经能说明测试目标、运行入口、依赖条件、覆盖范围和最终结论。

## 默认执行流程

1. 默认先确认遵循 `test-strategy-rules 的 test-asset-governance 条件路由`：所有测试文档都属于中央约定的测试时间戳根目录。
2. 再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径和同一轮测试是否继续复用同一根目录。
3. 默认先读 `references/doc-minimums.md`，确认 README 和补充文档的最小字段。
4. 如果当前文档与测试程序、功能结论或回归结论职责混淆，再读 `references/doc-boundaries.md`。
5. 如果需要判断当前文档是否达标，再读 `references/doc-examples.md` 对照正反例。
6. 输出缺失章节、补充建议、应放入 README 的内容，以及应转移到 ASCII 镜像路径的详细文档。
7. 测试文档未稳定前，不进入正式交付总结或发布留痕阶段。

## 权责边界与不负责事项

- 只负责测试文档结构、字段和归档方式，不负责决定测试资产落点，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 只负责把结论记录清楚，不负责判定功能是否通过，那属于 `functional-validation-rules`。
- 只负责把回归范围和结论留痕清楚，不负责决定回归是否充分，那属于 `test-regression-rules`。
- 不负责测试程序实现、断言设计、mock 组织和脚本拆分，那属于 `test-program-rules`。
- 如果文档写不清，是因为测试资产、需求边界或执行事实本身不清，应回流相应上游 skill。

## 需要暂停并确认的条件

- 中文说明目录之外没有找到明确的 ASCII 真实代码路径镜像目录，导致详细文档无处安放。
- 当前 README 既想承载中文总览，又想堆放大量原始日志、截图和明细，结构已经失控。
- 为了补齐文档，需要先补录大量缺失的执行事实、环境信息或测试结果。
- 当前文档准备脱离中央约定的测试时间戳根目录单独放到 `testing/`、`analysis/` 或其他目录。

## 执行通过 / 驳回标准

- 通过：中央约定的测试任务主说明 `README.md` 已经清楚说明测试对象、执行方式、依赖条件、真实资产入口、覆盖范围和最终结论；如有额外文档，也已落在同一时间戳根目录下的 ASCII 镜像路径中，并被 README 正确引用。
- 驳回：README 只剩口头式结论，缺少运行入口和结果依据；补充文档继续散落到 `testing/`、`analysis/`、仓库根目录、业务目录或中文说明目录中，无法支持复现、交接和追溯；或文档把“新增测试专用方法/数据/结构体字段”作为可接受做法记录到生产代码方案中。

## 执行结果归档要求

- 主文档固定归档到 `artifact-storage-rules` 约定的测试任务主说明 `README.md`。
- 主 README 至少包含测试目的、测试对象、执行方式、依赖数据与环境、覆盖范围、真实资产路径和验证结论。
- 额外 markdown、截图说明、执行明细、案例表和附录文档，统一归档到中央约定的测试时间戳根目录下的 ASCII 真实代码路径镜像目录中。
- 测试任务主说明位置、目录命名模板和同一轮测试的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 主 README 必须显式写出这些详细文档或证据文件所在的 ASCII 路径，避免只留一堆孤立附件。
- 如果同一需求拆成多轮独立验证，应分别维护各自时间戳根目录的 README，而不是在一个 README 中持续堆叠历史轮次。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules` 核对测试任务 `README.md` 与引用的 ASCII 证据路径是否已经真实落盘；未落盘不得判定测试文档完成。

## references 读取规则

- 默认先读 `references/doc-minimums.md`。
- 在定位测试时间戳根目录、中文主说明 `README.md`、ASCII 镜像路径或判断是否继续沿用同一轮测试根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在职责边界混淆时，再读 `references/doc-boundaries.md`。
- 只有在需要正反例或模板参考时，再读 `references/doc-examples.md`。
- 输出测试 README 或证据文档前，必须读取 `../artifact-delivery-gate-rules/references/plain-language-document-contract.md`；正文先说明测什么、结论和影响，环境、命令、样本和日志进入附录。
- 涉及审查、验收、浏览器联调或第三方验证时，必须同时读取 `../artifact-delivery-gate-rules/references/review-acceptance-gate-contract.md`，记录适用性和替代验证，不把不适用写成阻断。

## 迁移保留规则：test-strategy-rules 的 test-asset-governance 条件路由

# 测试命名规则

只在"测试资产名称应该怎么起"这个问题上使用这个 skill。
如果当前争议是测试资源放在哪里，请转交 `test-strategy-rules 的 test-asset-governance 条件路由`；如果当前问题是已有测试资产散落在错误目录，还要转交 `test-strategy-rules 的 test-asset-governance 条件路由`；如果是测试程序具体怎么写，请转交 `test-program-rules`。

**重要：本 skill 必须以 `artifact-storage-rules` 与 `test-strategy-rules 的 test-asset-governance 条件路由` 为基础，所有测试资产必须统一放在中央约定的测试根目录下；测试任务根目录命名必须遵循中央模板；中文说明目录单独使用中文任务简介命名；会被 Go 编译的真实测试路径必须保持 ASCII，并服从 `go-test-compile-path-rules`。**

## 测试隔离红线（强制）

- 严禁为了测试目的改动生产代码语义，包括但不限于新增测试专用方法、测试专用数据、测试专用结构体字段。
- 命名阶段若发现“测试专用字段/方法”命名诉求来自生产代码，必须判定为违规来源并回退到测试资产命名方案，不得继续命名落地。
- 若命名涉及环境说明、脚本名或目录说明，必须体现“本地测试 / local 环境”语义；不得用会暗示默认连接 `test` 环境的命名（如 `run-test-env.*`、`config_test_probe.*`）作为本地自动化测试主入口。

## 命名一致性硬规则（时间戳目录）

- 时间戳目录必须由运行时当前时间生成，不允许手写旧日期。
- 时间戳根目录必须使用 `yyyy-MM-DD_HHmmss`，必须包含时分秒；禁止退化为只有日期的 `yyyy-MM-DD`。
- 新增测试文件必须落在当前任务时间戳目录下的真实代码路径镜像目录（如 `api/`、`utils/`）。
- 如果要延续旧任务，必须在提交说明或任务说明中写明“复用旧目录原因 + 旧任务ID”。

## Skill 作用与适用场景

- 作为测试资源管理链的第二道规则，在落点确定后统一命名。
- 统一时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 和 mock 目录的命名方式。
- 提升测试资产的可读性、可检索性和任务对应关系，减少"找不到、看不懂、分不清"的问题。
- 防止使用临时、含糊、重复或风格混乱的测试命名。
- 确保时间戳根目录、中文说明目录和真实代码路径镜像目录各自承担清晰命名职责。

## 自动触发信号

- 新增或修改测试时间戳根目录、中文说明目录、测试文件、测试脚本、测试数据目录、fixture 目录、mock 目录。
- 需要为当前需求、当前 Bug、当前接口、当前页面交互创建新的测试资产名称。
- 发现测试目录或测试文件名称存在 `temp`、`new`、`final`、`test1` 等临时命名痕迹。
- 同类测试资产已经出现多种命名风格并存，需要统一时。
- 测试资产没有放在中央约定的测试根目录下，需要纠正时。
- 时间戳根目录命名不符合 `yyyy-MM-DD_HHmmss` 格式时。
- 中文说明目录没有使用清晰中文简介，或中文进入了 Go 可编译路径时。

## 进入后先做什么

1. 先确认测试资产落点已经稳定，且在中央约定的测试根目录下，不在当前 skill 内重新决定目录位置。
2. 确认时间戳根目录命名符合 `yyyy-MM-DD_HHmmss` 格式。
3. 校验该时间戳由运行时当前时间生成，禁止手写或沿用旧日期。
4. 区分当前名称对象是时间戳根目录、中文说明目录、真实代码路径镜像目录、测试文件、测试脚本还是测试数据目录。
5. 提取命名必须表达的核心信息：业务对象、测试层级、场景目标、是否为公共资源。
6. 对会被 Go 编译的路径，确认目录名和文件名保持 ASCII 且兼容工具链。
7. 优先复用项目现有命名模式，不随意引入新的前后缀和分隔符。
8. 若复用旧时间戳目录，补充“复用旧目录原因 + 旧任务ID”的说明字段。

## 默认执行流程

1. 先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认测试根目录、时间戳根目录模板、中文说明目录命名、ASCII 镜像路径和同一轮测试是否继续复用同一根目录。
2. 再确认遵循 `artifact-storage-rules`、`test-strategy-rules 的 test-asset-governance 条件路由` 与 `go-test-compile-path-rules` 的约定：所有测试资产在中央约定的测试根目录下；任务根目录使用统一模板；中文说明目录单独使用中文任务简介；真实测试路径按真实代码路径镜像组织，并在 Go 可编译路径中保持 ASCII。
3. 对时间戳目录执行一致性检查：目录时间必须来自运行时当前时间，且新增测试文件必须落在当前任务时间戳目录下的镜像路径。
4. 若复用旧任务目录，检查提交说明或任务说明是否包含“复用旧目录原因 + 旧任务ID”；缺任一项则判定命名流程未完成。
5. 默认先读 `references/naming-baseline.md`，确认命名维度、顺序和禁用写法。
6. 如果命名争议涉及落点、职责或需求含义不清，再读 `references/naming-boundaries.md`。
7. 如果需要判断当前名称是否合格，再读 `references/naming-examples.md` 对照正反例。
8. 输出推荐名称、命名问题清单、是否需要统一重命名，以及重命名时的最小改动建议。
9. 确认每个时间戳根目录都包含中文说明目录和其中的 `README.md`。
10. 名称未稳定前，不进入 `test-program-rules` 和 `test-strategy-rules 的 test-asset-governance 条件路由`。

## 权责边界与不负责事项

- 只负责命名规则，不负责测试目录放置方案，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 必须遵循 `artifact-storage-rules` 与 `test-strategy-rules 的 test-asset-governance 条件路由` 的约定：统一使用中央测试根目录；时间戳根目录使用统一模板；中文说明目录单独使用中文任务简介；真实测试路径按真实代码路径镜像命名；涉及 Go 可编译路径时还必须服从 `go-test-compile-path-rules`。
- 不负责测试程序实现、断言方式和脚本内容，那属于 `test-program-rules`。
- 不负责测试说明文档章节和记录格式，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 不负责功能是否正确、覆盖是否充分，那属于 `functional-validation-rules` 和 `test-regression-rules`。
- 如果名称无法确定是因为需求目标、场景边界或 Bug 定义本身不清，应回流 `requirement-gap-rules`、`requirement-boundary-rules` 或 Bug 域相关 skill。

## 需要暂停并确认的条件

- 项目尚无稳定测试命名模式，且当前命名选择会影响整个测试域后续扩展。
- 同一个测试资产同时承载多个业务目标，导致名称无法聚焦。
- 为统一命名需要批量改动大量历史测试文件，已经超出当前最小改动范围。
- 名称变更会影响脚本引用、构建配置或外部约定，但影响面尚未确认。
- 测试资产没有放在中央约定的测试根目录下，需要确认迁移方案。
- 中文目录准备进入 Go 可编译路径，可能直接导致 `go test ./...` 失败。
- 时间戳目录不是由运行时当前时间生成，或出现手写旧日期。
- 计划复用旧目录但未提供“复用旧目录原因 + 旧任务ID”。

## 执行通过 / 驳回标准

- 通过：当前测试目录和文件名称能够稳定表达业务对象、测试层级和场景目标，且与项目现有命名模式一致，没有临时命名和歧义命名问题；所有测试资产都在中央约定的测试根目录下；时间戳根目录命名符合统一模板且由运行时当前时间生成；新增测试文件位于当前任务时间戳目录的镜像路径；复用旧目录时说明中已包含“复用旧目录原因 + 旧任务ID”；中文说明目录清晰表达测试任务简介；Go 可编译路径保持 ASCII；每个时间戳根目录都包含说明 `README.md`。
- 驳回：当前名称含糊、重复、临时化或风格混乱；测试资产不在中央约定的测试根目录下；时间戳根目录命名不符合统一模板或使用手写旧日期；新增测试文件不在当前任务时间戳目录镜像路径；复用旧目录但缺少“复用旧目录原因 + 旧任务ID”；中文进入 Go 可编译路径，继续进入后续测试编写和验证会显著增加维护成本并直接破坏自动化测试链路；或发现测试诉求通过向生产代码新增测试专用方法、测试专用数据、测试专用结构体字段实现。

## 执行结果归档要求

- 将命名结论记录到 `artifact-storage-rules` 约定的测试任务主说明 `README.md` 中。
- 归档内容至少包含命名对象、命名理由、命名模式、禁用名称、ASCII / 中文路径分工和待统一项。
- 测试任务主说明位置、目录命名模板和同一轮测试的复用策略统一遵循 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 如果发生重命名，应在记录中说明影响范围和引用同步要求。
- 提醒用户旧的时间戳根目录以每周日为时间间隔，归档到中央约定的测试根目录下（可创建 `archive/` 子目录存放归档内容）。
- 进入最终回复前，必须联动 `artifact-delivery-gate-rules`，核对命名结论、路径分工和重命名影响是否已经真实记录到测试任务 `README.md`；未落盘不得判定测试命名完成。

## references 读取规则

- 默认先读 `references/naming-baseline.md`。
- 在定位测试根目录、时间戳根目录模板、中文说明目录、ASCII 镜像路径或判断是否继续沿用同一轮测试根目录时，先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
- 只有在职责边界或需求含义不清时，再读 `references/naming-boundaries.md`。
- 只有在需要对照正反例时，再读 `references/naming-examples.md`。

## 迁移保留规则：test-strategy-rules 的 test-asset-governance 条件路由

# 测试资产禁散落规则

只在“测试资产被放错地方了”这个问题上使用本 skill。
它负责识别哪些文件其实属于测试资产、哪些位置属于违规散落，并把相关资产收拢回正确的测试任务目录。

## Skill 作用与适用场景

- 识别散落在业务目录、仓库根目录、`docs/`、`scripts/`、`tools/` 等位置的测试资产。
- 阻断“为了测试方便，把测试脚本、mock 或说明文件顺手塞进生产目录”的行为。
- 在最小改动前提下，把当前任务直接相关的散落测试资产迁移回中央测试根目录。
- 区分“只是位置错了”与“同时触发 Go 编译路径冲突”的场景。

## 自动触发信号

- 发现测试脚本、测试数据、mock、fixture、验证记录或测试说明不在 `doc/5-tests/` 根目录下。
- 发现仓库根目录、业务目录、`docs/`、`wiki/`、`scripts/`、`tools/` 等目录中混入测试资产。
- 发现中文说明目录中混入真实测试代码、脚本、mock、fixture、截图或报告产物。
- 需要决定某个现有文件到底是生产资产还是测试资产，并据此归位。

## 强制规则

- 任何测试相关资产，只要不在 `doc/5-tests/` 根目录下，默认按违规散落处理。
- 严禁为了测试目的向生产代码目录新增测试专用方法、测试专用数据、测试专用结构体字段。
- 迁移时优先处理当前任务直接相关的散落资产，不在当前任务中顺手做全仓库大扫除。
- 若某文件同时承担生产与测试双重职责，先拆分职责，再分别归位。
- 若散落问题同时涉及 Go 编译路径、源码目录 `*_test.go` 或白盒同包诉求，立即转交 `go-test-compile-path-rules` 一并处理。
- 若散落资产中包含指向 `test` 环境配置、`test` 数据库连接或“修改 test 配置后运行”的脚本 / 说明，必须一并判定为本地测试规则违规并迁移或改写为 `local` 环境用法。

## 默认执行流程

1. 先读 `references/scattered-asset-migration.md`，判断当前文件是否属于测试资产以及属于哪种散落类型。
2. 再确认当前任务应归属的测试时间戳根目录；若根布局尚未建立，先转交 `test-strategy-rules 的 test-asset-governance 条件路由`。
3. 只迁移与当前任务直接相关的散落资产，并补齐对应的中文说明或引用路径。
4. 若散落位置位于 Go 可编译路径或源码目录，需要同时触发 `go-test-compile-path-rules`。
5. 迁移后确认：当前任务的测试资产不再散落，且未把生产职责误迁成测试职责。

## 权责边界与不负责事项

- 只负责识别和迁移散落测试资产，不负责创建测试任务根布局。
- 不负责 Go 编译路径 ASCII 约束、源码目录 `*_test.go` 禁放和 seam 方案，那属于 `go-test-compile-path-rules`。
- 不负责测试文件如何命名或测试程序如何编写。
- 不在当前任务中无限扩展为全仓库历史测试资产治理。

## 通过 / 驳回标准

- 通过：当前任务直接相关的散落测试资产已从违规目录迁回 `doc/5-tests/` 根目录下的正确任务目录，生产目录中不再混放测试资产，且没有遗漏中文说明或镜像路径。
- 驳回：测试资产仍散落在业务目录、仓库根目录或非测试目录，或把双重职责文件不加区分地整体迁移，或本应转交 Go 编译路径规则的问题被忽略。

## 执行结果归档要求

- 散落测试资产的迁移清单、原位置、目标测试目录和仍待迁移项，应记录到当前测试任务 `README.md` 或关联 Bug 根目录 / 需求主文档引用的测试任务 `README.md` 中。
- 如果迁移同时影响现有引用路径，记录中必须写明引用同步动作和残留风险。
- 进入最终回复前，若本轮已经完成或调整散落测试资产迁移并准备收口，必须联动 `artifact-delivery-gate-rules`，核对迁移后的资产、引用记录和目标测试目录是否已经真实落盘；未落盘不得判定散落资产治理完成。

## references 读取规则

- 默认先读 `references/scattered-asset-migration.md`。
- 需要确定目标时间戳根目录时，再读 `../artifact-storage-rules/references/path-map.yaml` 与 `../artifact-storage-rules/references/update-policy.md`。

## 迁移保留规则：test-strategy-rules 的 test-asset-governance 条件路由

# 测试任务根布局规则

只在“当前测试任务的根目录和布局该怎么建”这个问题上使用本 skill。
它负责把测试任务先放到正确的根目录和时间戳根目录下，再把中文说明目录和 ASCII 资产镜像目录布置完整。

## Skill 作用与适用场景

- 决定新的测试任务应该放到 `doc/5-tests/` 根目录下的哪个当天时间戳目录。
- 统一中文说明目录、`README.md` 和真实测试资产镜像目录的并列布局。
- 统一“时间戳根目录只放时间戳、不混中文”的根布局规则。
- 统一“真实测试资产按真实代码路径镜像、且保持 ASCII”的落点规则。
- 在进入测试命名、测试程序编写或测试文档组织前，先把目录骨架定准。

## 自动触发信号

- 新增测试任务目录或准备写入新的测试资产。
- 需要决定是否创建新的当天时间戳根目录。
- 需要为当前测试任务创建中文说明目录和 `README.md`。
- 需要把真实测试资产映射到 ASCII 真实代码路径镜像目录。
- 同一需求存在多轮独立验证，需要判断是否拆成多个时间戳根目录。

## 强制规则

- 统一使用 `doc/5-tests/` 作为测试根目录，不得改用 `tests/`、`qa/`、`verify/` 等名称。
- 默认新测试任务必须创建当天时间戳根目录，命名格式为 `yyyy-MM-DD_HHmmss`，必须包含时分秒；禁止退化为只有日期的 `yyyy-MM-DD`。
- 若检测到目标目录日期早于运行时当天日期，必须暂停并询问用户是否明确复用旧目录。
- 未获明确许可前，禁止把新文件写入历史时间戳目录；读取历史目录仅可作为参考。
- 每个时间戳根目录都必须同时包含一个中文说明目录和一个或多个 ASCII 真实代码路径镜像目录。
- 中文说明目录默认只存放 `README.md`，不承载真实测试代码、脚本、mock、fixture、日志或报告产物。
- 真实测试资产必须按真实代码路径镜像组织；若无法精确映射到单一源码文件，至少映射到最接近的源码模块路径。
- 同一需求的多个独立测试验证，默认拆成多个时间戳根目录，而不是强行混在一个目录里。
- 当前仓库所有自动化测试目录默认服务于本地测试；目录骨架与 README 不得引导执行者去修改 `test` 配置或连接 `test` 环境资源，必须明确使用 `local` 环境信息。

## 默认执行流程

1. 先读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`，确认中央约定的测试根目录与复用策略。
2. 再读 `references/task-root-layout.md`，确认时间戳根目录、中文说明目录和 ASCII 镜像目录的布局规则。
3. 判断当前任务应新建当天时间戳根目录，还是在用户明确允许时复用旧目录。
4. 先创建时间戳根目录，再创建中文说明目录和 `README.md`。
5. 最后为真实测试资产准备 ASCII 镜像目录，等待后续 `test-program-rules` 或 `test-strategy-rules 的 test-asset-governance 条件路由` 继续落盘。

## 权责边界与不负责事项

- 只负责测试任务根目录和布局，不负责散落资产迁移。
- 不负责 Go 编译路径冲突、源码目录 `*_test.go` 禁放和 seam 方案，那属于 `go-test-compile-path-rules`。
- 不负责测试名称本身，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。
- 不负责测试程序写法，那属于 `test-program-rules`。
- 不负责测试说明内容结构，那属于 `test-strategy-rules 的 test-asset-governance 条件路由`。

## 通过 / 驳回标准

- 通过：当前测试任务已放在 `doc/5-tests/` 根目录下的当天时间戳根目录中，中文说明目录和 `README.md` 已就位，真实测试资产镜像目录保持 ASCII，且没有把新文件误写到未经允许的历史目录。
- 驳回：根目录名称不合规、时间戳目录不是当天且未获明确复用许可、中文说明目录缺失、`README.md` 缺失，或真实测试资产没有准备 ASCII 镜像目录。

## 执行结果归档要求

- 测试任务根布局的创建结果、复用旧目录说明和 ASCII 镜像目录准备情况，应记录到当前测试任务中文说明目录下的 `README.md` 中。
- 如果本轮只是建立骨架但尚未写入真实测试资产，也要在 `README.md` 中明确记录后续将承接的测试主题与目录分工。
- 进入最终回复前，若本轮已经创建或调整测试任务根布局并准备收口，必须联动 `artifact-delivery-gate-rules`，核对时间戳根目录、中文说明目录、`README.md` 和 ASCII 镜像目录是否已经真实落盘到中央约定位置；未落盘不得判定根布局工作完成。

## references 读取规则

- 默认先读 `references/task-root-layout.md`。
- 需要确认中央约定路径时，再读 `../artifact-storage-rules/references/path-map.yaml`、`../artifact-storage-rules/references/naming-templates.md` 与 `../artifact-storage-rules/references/update-policy.md`。
